"""Boletín Oficial de la República Argentina.

Ingests decrees, resolutions, appointments, and regulatory acts.
Analogous to Brazil's DOU (Diário Oficial da União).

Source: https://www.boletinoficial.gob.ar/
"""

from __future__ import annotations

import json
import logging
import re
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any
from urllib.parse import urljoin

import httpx
import pandas as pd
from lxml import html

from aracc_etl.base import Pipeline
from aracc_etl.loader import Neo4jBatchLoader

logger = logging.getLogger(__name__)


def extract_person_mentions(text: str) -> list[dict[str, Any]]:
    """Extract person mentions from text using regex patterns.

    Detects DNI and CUIL patterns, extracts names from context.
    Returns list of dicts with: {'name': str | None, 'cuil': str | None, 'confidence': float}
    """
    results: list[dict[str, Any]] = []

    # DNI patterns
    dni_patterns = [
        r'(?:D\.?N\.?I\.?\s*(?:Nº|N°|Nro\.?|#)?)\s*([0-9]{1,2}\.?[0-9]{3}\.?[0-9]{3})',
        r'(?:D\.?N\.?I\.?)\s*([0-9]{7,8})',
        r'([0-9]{1,2}\.[0-9]{3}\.[0-9]{3})',
    ]

    # CUIL pattern (11 digits total)
    cuil_pattern = r'(\d{2})[-.]?(\d{7,8})[-.]?(\d{1})'

    # Name patterns - matches "Ezequiel GALLI", "Juan PEREZ", etc.
    # Avoids matching common words before names
    name_before_pattern = (
        r'(?:a|de|por|nombre|señor|señora|sr\.?|sra\.?|don|doña|d\.?|'
        r'sr\.?a\.?|el|la|los|las|al|del)\s+(?:abogado|abogada|doctor|doctora|licenciado|licenciada|ingeniero|ingeniera)?\s*([A-Z][a-zA-Z]*(?:\s+[A-Z][a-zA-Z]*)?(?:\s+[A-Z]+)?)'
    )
    # Pattern for names right before DNI/CUIL reference
    name_after_pattern = (
        r'([A-Z][a-zA-Z]*(?:\s+[A-Z]+)?),?\s*'
        r'(?:D\.?N\.?I\.?|CUIL)'
    )

    found_docs: list[dict[str, Any]] = []
    seen_values: set[str] = set()

    # Find DNIs (only first match to avoid duplicates)
    for pattern in dni_patterns:
        match = next(re.finditer(pattern, text, re.IGNORECASE), None)
        if match:
            dni_raw = match.group(1) if match.group(1) else match.group(0)
            dni_digits = re.sub(r'[^0-9]', '', dni_raw)
            if len(dni_digits) in {7, 8} and dni_digits not in seen_values:
                found_docs.append({'type': 'dni', 'value': dni_digits, 'pos': match.start()})
                seen_values.add(dni_digits)
                break  # Only one DNI pattern should match

    # Find CUILs
    for match in re.finditer(cuil_pattern, text):
        prefix, body, digit = match.group(1), match.group(2), match.group(3)
        if prefix in {'20', '23', '24', '27'}:
            cuil = f"{prefix}-{body.zfill(7)}-{digit}"
            if cuil not in seen_values:
                found_docs.append({'type': 'cuil', 'value': cuil, 'pos': match.start()})
                seen_values.add(cuil)

    # Extract names
    for doc in found_docs:
        name: str | None = None
        pos = doc['pos']
        
        # Search BEFORE the document number (up to 80 chars)
        search_start = max(0, pos - 80)
        search_text_before = text[search_start:pos]
        
        # Find last match (closest to DNI)
        last_match = None
        for match in re.finditer(name_before_pattern, search_text_before, re.IGNORECASE):
            last_match = match
        if last_match:
            name = last_match.group(1).strip()

        # If no name found before, search AFTER the document number
        if not name and pos + 100 < len(text):
            search_after = text[pos:min(pos + 100, len(text))]
            name_match_after = re.search(name_after_pattern, search_after)
            if name_match_after:
                name = name_match_after.group(1).strip()

        results.append({
            'name': name,
            'cuil': doc['value'],
            'confidence': 0.9 if doc['type'] == 'cuil' else 0.75,
        })

    return results


def extract_company_mentions(text: str) -> list[dict[str, Any]]:
    """Extract company mentions from text using regex patterns."""
    results: list[dict[str, Any]] = []

    company_pattern = r'([A-Z][a-zA-Z0-9\s&\.]+(?:S\.?A\.?|S\.?R\.?L\.?|S\.?A\.?S\.?|S\.?C\.?|S\.?E\.?A\.?))'
    cuit_pattern = r'(30|33|34|35)[-.]?(\d{7,8})[-.]?(\d{1})'

    for match in re.finditer(company_pattern, text):
        company_name = match.group(1).strip()
        if len(company_name) > 3:
            results.append({'name': company_name, 'cuit': None, 'confidence': 0.6})

    for match in re.finditer(cuit_pattern, text):
        prefix, body, digit = match.group(1), match.group(2), match.group(3)
        cuit = f"{prefix}-{body.zfill(7)}-{digit}"
        results.append({'name': None, 'cuit': cuit, 'confidence': 0.85})

    return results


def normalize_text(data: str | list[str]) -> str:
    """Normalize text data by joining lists and cleaning whitespace."""
    if isinstance(data, list):
        return "".join([i.replace("\xa0", " ") for i in data]).strip()
    if isinstance(data, str):
        return " ".join([i.replace("\xa0", " ") for i in data.split()]).strip()
    return ""


class BoletinOficialPipeline(Pipeline):
    name = "boletin_oficial"
    source_id = "boletin_oficial"

    def __init__(
        self,
        *args: object,
        start_date: str | None = None,
        end_date: str | None = None,
        extract_entities: bool = True,
        **kwargs: object,
    ) -> None:
        super().__init__(*args, **kwargs)  # type: ignore[arg-type]
        self.df_documents: pd.DataFrame = pd.DataFrame()
        self.df_entity_mentions: pd.DataFrame = pd.DataFrame()

        self._start_date_param = start_date
        self._end_date_param = end_date
        self._extract_entities = extract_entities

        self.headers = {
            "Host": "www.boletinoficial.gob.ar",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://www.boletinoficial.gob.ar/seccion/primera",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Cache-Control": "max-age=0"
        }

    def _determine_dates(self) -> tuple[datetime, datetime]:
        """Determine start and end dates for scraping."""
        if self._end_date_param:
            end_date_dt = datetime.strptime(self._end_date_param, "%Y-%m-%d")
        else:
            end_date_dt = datetime.today()

        if self._start_date_param:
            start_date_dt = datetime.strptime(self._start_date_param, "%Y-%m-%d")
        else:
            if not self.history:
                try:
                    with self.driver.session(database=self.neo4j_database) as session:
                        res = session.run("MATCH (d:BoletinDocument) RETURN max(d.publication_date) AS dt")
                        max_dt = res.single()["dt"]
                        if max_dt:
                            start_date_dt = datetime.strptime(max_dt, "%Y-%m-%d")
                            logger.info("[%s] Resuming scraping from last db date: %s", self.name, max_dt)
                            return start_date_dt, end_date_dt
                except Exception as e:
                    logger.warning("[%s] Failed to fetch last scrape date from DB: %s", self.name, e)

            if self.history:
                start_date_dt = end_date_dt - timedelta(days=30)
            else:
                start_date_dt = end_date_dt - timedelta(days=3)

        return start_date_dt, end_date_dt

    def extract(self) -> None:
        start_date_dt, end_date_dt = self._determine_dates()

        out_dir = Path(self.data_dir) / "boletin_oficial"
        out_dir.mkdir(parents=True, exist_ok=True)
        dest_file = out_dir / "boletin_raw.jsonl"

        existing_ids = set()
        if dest_file.exists():
            with open(dest_file, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        record = json.loads(line)
                        if "id" in record:
                            existing_ids.add(record["id"])
                    except json.JSONDecodeError:
                        pass

        logger.info("[%s] Starting scraping from %s to %s", self.name, start_date_dt.date(), end_date_dt.date())

        with httpx.Client(timeout=60.0, follow_redirects=True, headers=self.headers) as client:
            client.get("https://www.boletinoficial.gob.ar/seccion/primera")

            current_date = start_date_dt
            items_scraped = 0

            with open(dest_file, "a", encoding="utf-8") as f:
                while current_date <= end_date_dt:
                    if self.limit and items_scraped >= self.limit:
                        logger.info("[%s] Reached limit of %d items", self.name, self.limit)
                        break

                    date_str = current_date.strftime("%d-%m-%Y")
                    date_url = f"https://www.boletinoficial.gob.ar/edicion/actualizar/{date_str}"

                    decreto_urls = []
                    try:
                        client.get(date_url)
                        initial_url = "https://www.boletinoficial.gob.ar/seccion/primera"
                        resp = client.get(initial_url)
                        resp.raise_for_status()

                        tree = html.fromstring(resp.content)
                        links = tree.xpath("//*[@id='avisosSeccionDiv']//a[child::div[@class='linea-aviso']]/@href")
                        decreto_urls = [urljoin(initial_url, u) for u in links if isinstance(u, str)]
                    except Exception as e:
                        logger.warning("[%s] Failed to fetch decretos for %s: %s", self.name, current_date.strftime("%Y-%m-%d"), e)

                    if decreto_urls:
                        logger.info("[%s] Found %d decretos for %s", self.name, len(decreto_urls), current_date.strftime("%Y-%m-%d"))

                    for dec_url in decreto_urls:
                        if self.limit and items_scraped >= self.limit:
                            break

                        parts = dec_url.split("/")
                        doc_id = parts[-2] if len(parts) > 2 else None
                        if doc_id and doc_id in existing_ids:
                            continue

                        try:
                            time.sleep(1.0)
                            r = client.get(dec_url)
                            r.raise_for_status()

                            doc_tree = html.fromstring(r.content)
                            item: dict[str, Any] = {}
                            item["titulo_decreto"] = normalize_text(doc_tree.xpath('string(//*[@id="tituloDetalleAviso"]/h1)'))
                            item["resolucion"] = normalize_text(doc_tree.xpath('string(//*[@id="tituloDetalleAviso"]/h2)'))
                            item["resolucion_code"] = normalize_text(doc_tree.xpath('string(//*[@id="tituloDetalleAviso"]/h6)'))
                            item["corpus"] = normalize_text(doc_tree.xpath('//*[@id="cuerpoDetalleAviso"]//text()[not(parent::style)]'))
                            item["fecha_publicacion"] = re.sub(r"[^\d\/]", "", doc_tree.xpath('string(//*[@class="text-muted"])'))
                            item['rubro'] = normalize_text(doc_tree.xpath('string(//a[@class="puntero first-section"])'))

                            try:
                                rubro_href = doc_tree.xpath('string(//a[@class="puntero first-section"]/@href)')
                                item['rubro_id'] = int(rubro_href.split('=')[-1]) if rubro_href and '=' in rubro_href else None
                            except (ValueError, IndexError):
                                item['rubro_id'] = None

                            item["url"] = dec_url
                            item["id"] = doc_id

                            f.write(json.dumps(item, ensure_ascii=False) + "\n")
                            f.flush()
                            if doc_id:
                                existing_ids.add(doc_id)
                                items_scraped += 1

                        except Exception as e:
                            logger.warning("[%s] Failed to parse decreto %s: %s", self.name, dec_url, e)

                    current_date += timedelta(days=1)

    def transform(self) -> None:
        source_file = Path(self.data_dir) / "boletin_oficial" / "boletin_raw.jsonl"
        if not source_file.exists():
            logger.warning("[%s] Source file %s does not exist", self.name, source_file)
            return

        records = []
        with open(source_file, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        records.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass

        df = pd.DataFrame(records)
        self.rows_in = len(df)

        if df.empty:
            logger.info("[%s] No data to transform", self.name)
            return

        if "id" in df.columns:
            df = df.drop_duplicates(subset=["id"], keep="last")

        if self.limit:
            df = df.head(self.limit)

        df = df.rename(columns={
            "id": "doc_id",
            "titulo_decreto": "title",
            "resolucion": "document_type",
            "resolucion_code": "document_code",
            "corpus": "body",
            "fecha_publicacion": "publication_date",
            "rubro": "category",
            "rubro_id": "category_id"
        })

        def parse_pub_date(d: str) -> str:
            if not d:
                return ""
            try:
                return datetime.strptime(d.strip(), "%d/%m/%Y").strftime("%Y-%m-%d")
            except ValueError:
                return d

        if "publication_date" in df.columns:
            df["publication_date"] = df["publication_date"].apply(parse_pub_date)

        if "category_id" in df.columns:
            df["category_id"] = pd.to_numeric(df["category_id"], errors="coerce")
            df["category_id"] = df["category_id"].where(df["category_id"].notna(), pd.NA)

        self.df_documents = df

        if self._extract_entities:
            self._extract_entities_from_documents(df)

        logger.info("[%s] Transform complete: %d documents ready", self.name, len(self.df_documents))

    def _extract_entities_from_documents(self, df: pd.DataFrame) -> None:
        """Extract person and company mentions from documents."""
        entity_mentions: list[dict[str, Any]] = []

        for _, row in df.iterrows():
            doc_id = row.get("doc_id")
            body = row.get("body", "")

            if not body:
                continue

            persons = extract_person_mentions(body)
            for person in persons:
                entity_mentions.append({
                    "doc_id": doc_id,
                    "entity_type": "person",
                    "entity_name": person.get("name") or "",
                    "entity_identifier": person.get("cuil") or "",
                    "confidence": person.get("confidence", 0.5),
                })

            companies = extract_company_mentions(body)
            for company in companies:
                entity_mentions.append({
                    "doc_id": doc_id,
                    "entity_type": "company",
                    "entity_name": company.get("name") or "",
                    "entity_identifier": company.get("cuit") or "",
                    "confidence": company.get("confidence", 0.5),
                })

        if entity_mentions:
            self.df_entity_mentions = pd.DataFrame(entity_mentions)
            logger.info(
                "[%s] Extracted %d entity mentions from %d documents",
                self.name,
                len(self.df_entity_mentions),
                len(df),
            )

    def load(self) -> None:
        if self.df_documents.empty:
            logger.info("[%s] Load skipped, no documents to load", self.name)
            return

        loader = Neo4jBatchLoader(
            self.driver,
            batch_size=self.chunk_size,
            neo4j_database=self.neo4j_database,
        )

        doc_rows: list[dict[str, Any]] = self.df_documents.to_dict(orient="records")  # type: ignore[assignment]
        for row in doc_rows:
            for k, v in list(row.items()):
                if pd.isna(v):
                    row[k] = None

        n = loader.load_nodes("BoletinDocument", doc_rows, "doc_id")
        logger.info("[%s] Loaded %d BoletinDocument nodes", self.name, n)

        if not self.df_entity_mentions.empty:
            self._load_entity_mentions(loader)

        self.rows_loaded = len(doc_rows)
        logger.info("[%s] Load complete: %d rows loaded", self.name, self.rows_loaded)

    def _load_entity_mentions(self, loader: Neo4jBatchLoader) -> None:
        """Load entity mentions: create Person/Company nodes and relationships."""
        mention_rows = self.df_entity_mentions.to_dict("records")

        person_mentions = [m for m in mention_rows if m.get("entity_type") == "person"]
        company_mentions = [m for m in mention_rows if m.get("entity_type") == "company"]

        if person_mentions:
            person_nodes_dict: dict[str, dict[str, Any]] = {}
            for m in person_mentions:
                cuil = m.get("entity_identifier", "")
                name = m.get("entity_name", "")
                if cuil and cuil not in person_nodes_dict:
                    person_nodes_dict[cuil] = {"cuil": cuil, "name": name}

            if person_nodes_dict:
                person_nodes = list(person_nodes_dict.values())
                n = loader.load_nodes("Person", person_nodes, "cuil")
                logger.info("[%s] Loaded/updated %d Person nodes", self.name, n)

            person_rels = [
                {
                    "source_key": m.get("entity_identifier") or m.get("entity_name"),
                    "target_key": m["doc_id"],
                    "confidence": m.get("confidence", 0.5),
                }
                for m in person_mentions
            ]
            n = loader.load_relationships(
                "MENCIONADA_EN",
                person_rels,
                "Person",
                "cuil",
                "BoletinDocument",
                "doc_id",
                properties=["confidence"],
            )
            logger.info("[%s] Loaded %d Person-MENCIONADA_EN-BoletinDocument relationships", self.name, n)

        if company_mentions:
            company_nodes_dict: dict[str, dict[str, Any]] = {}
            for m in company_mentions:
                cuit = m.get("entity_identifier", "")
                name = m.get("entity_name", "")
                if cuit and cuit not in company_nodes_dict:
                    company_nodes_dict[cuit] = {"cuit": cuit, "name": name}

            if company_nodes_dict:
                company_nodes = list(company_nodes_dict.values())
                n = loader.load_nodes("Company", company_nodes, "cuit")
                logger.info("[%s] Loaded/updated %d Company nodes", self.name, n)

            company_rels = [
                {
                    "source_key": m.get("entity_identifier") or m.get("entity_name"),
                    "target_key": m["doc_id"],
                    "confidence": m.get("confidence", 0.5),
                }
                for m in company_mentions
            ]
            n = loader.load_relationships(
                "MENCIONADA_EN",
                company_rels,
                "Company",
                "cuit",
                "BoletinDocument",
                "doc_id",
                properties=["confidence"],
            )
            logger.info("[%s] Loaded %d Company-MENCIONADA_EN-BoletinDocument relationships", self.name, n)
