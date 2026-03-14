#!/usr/bin/env python3
"""Download and parse official Senado CPI/CPMI historical archive PDFs.

This module is intentionally reusable by `download_senado_cpis.py`.
"""

from __future__ import annotations

import csv
import hashlib
import json
import logging
import re
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import click
import httpx

logger = logging.getLogger(__name__)

REQ_MARKER_RE = re.compile(r"\b(?:RSF|RQN|RCN)\s*\d+/\d{4}\b", re.IGNORECASE)
DATE_RE = re.compile(r"\b\d{2}/\d{2}/\d{4}\b")


@dataclass(frozen=True)
class ArchiveSource:
    url: str
    kind: str
    house: str
    period_start: str
    period_end: str


ARCHIVE_SOURCES: tuple[ArchiveSource, ...] = (
    ArchiveSource(
        url=(
            "https://www12.senado.leg.br/institucional/arquivo/imagens/"
            "tabela-de-cpis-de-1946-1975-2"
        ),
        kind="CPI",
        house="senado",
        period_start="1946-01-01",
        period_end="1975-12-31",
    ),
    ArchiveSource(
        url=(
            "https://www12.senado.leg.br/institucional/arquivo/outras-publicacoes/pdfs/"
            "TABELA%20DE%20CPIs%20de%201975%20-%202015.pdf/"
        ),
        kind="CPI",
        house="senado",
        period_start="1975-01-01",
        period_end="2015-12-31",
    ),
    ArchiveSource(
        url=(
            "https://www12.senado.leg.br/institucional/arquivo/imagens/"
            "tabela-de-cpmis-de-1967-2016"
        ),
        kind="CPMI",
        house="congresso",
        period_start="1967-01-01",
        period_end="2016-12-31",
    ),
)


def _slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "unknown"


def _clean_text(value: str) -> str:
    text = value.replace("\xa0", " ").replace("\n", " | ")
    text = re.sub(r"\s*\|\s*", " | ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip(" |")


def _parse_date(value: str) -> str:
    raw = value.strip()
    if not raw:
        return ""
    try:
        return datetime.strptime(raw, "%d/%m/%Y").replace(tzinfo=UTC).strftime("%Y-%m-%d")
    except ValueError:
        return ""


def _extract_author_name(segment: str) -> str:
    match = re.search(r"\b(?:Senador(?:a)?|Deputado(?:a)?)\s+(.+?)\b(?:SIM|N[ÃA]O)\b", segment)
    if match:
        return re.sub(r"\s+", " ", match.group(1)).strip(" |,.-")

    fallback = re.search(r"\b(?:Senador(?:a)?|Deputado(?:a)?)\s+(.+)", segment)
    if not fallback:
        return ""
    candidate = fallback.group(1)
    stop = re.search(r"\b[A-Z]{2,6}/[A-Z]{2}\b|\bSIM\b|\bN[ÃA]O\b", candidate)
    if stop:
        candidate = candidate[: stop.start()]
    return re.sub(r"\s+", " ", candidate).strip(" |,.-")


def _extract_status(segment: str) -> str:
    lowered = segment.lower()
    if "decurso de prazo" in lowered:
        return "decurso de prazo"
    if "comissão concluída" in lowered or "comissao concluida" in lowered:
        return "comissao concluida"
    if "arquivado" in lowered:
        return "arquivado"
    return ""


def _extract_title(segment: str, first_date: str) -> str:
    start = segment.find(first_date)
    tail = segment[start + len(first_date):] if start >= 0 else segment
    cut = len(tail)
    author = re.search(r"\b(?:Senador(?:a)?|Deputado(?:a)?)\b", tail)
    if author:
        cut = min(cut, author.start())
    sim = re.search(r"\bSIM\b|\bN[ÃA]O\b", tail)
    if sim:
        cut = min(cut, sim.start())
    title = tail[:cut]
    title = re.sub(r"\b(?:RSF|RQN|RCN)\s*\d+/\d{4}\b", " ", title, flags=re.IGNORECASE)
    title = re.sub(r"\s*\|\s*", " ", title)
    title = re.sub(r"\s+", " ", title).strip(" -|,.;")
    return title


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: list[str] = []
    seen: set[str] = set()
    for row in rows:
        for key in row:
            if key not in seen:
                seen.add(key)
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _dedupe(rows: list[dict[str, Any]], key: str) -> list[dict[str, Any]]:
    seen: set[str] = set()
    out: list[dict[str, Any]] = []
    for row in rows:
        value = str(row.get(key, "")).strip()
        if not value or value in seen:
            continue
        seen.add(value)
        out.append(row)
    return out


def _read_pdf_text(pdf_bytes: bytes) -> str:
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise RuntimeError("Missing dependency pypdf. Install optional dep and retry.") from exc

    import io

    reader = PdfReader(io.BytesIO(pdf_bytes))
    return "\n".join((page.extract_text() or "") for page in reader.pages)


def parse_archive_text(
    text: str,
    source: ArchiveSource,
    run_id: str,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    normalized = _clean_text(text)
    markers = list(REQ_MARKER_RE.finditer(normalized))

    inquiries: list[dict[str, Any]] = []
    requirements: list[dict[str, Any]] = []
    sessions: list[dict[str, Any]] = []

    for idx, marker in enumerate(markers):
        segment_start = marker.start()
        segment_end = markers[idx + 1].start() if idx + 1 < len(markers) else len(normalized)
        segment = normalized[segment_start:segment_end].strip(" |")
        req_code = re.sub(r"\s+", " ", marker.group(0).upper()).strip()
        if not req_code:
            continue

        raw_dates = DATE_RE.findall(segment)
        parsed_dates = [_parse_date(value) for value in raw_dates]
        parsed_dates = [value for value in parsed_dates if value]
        date_start = parsed_dates[0] if parsed_dates else ""
        date_end = max(parsed_dates) if len(parsed_dates) > 1 else ""

        title = _extract_title(segment, raw_dates[0] if raw_dates else "")
        if not title:
            title = req_code

        inquiry_id = f"senado-{source.kind.lower()}-{_slugify(req_code)}"
        requirement_id = f"senado-req-{_slugify(req_code)}"
        status = _extract_status(segment)
        author_name = _extract_author_name(segment)

        inquiries.append({
            "inquiry_id": inquiry_id,
            "inquiry_code": req_code,
            "name": title,
            "kind": source.kind,
            "house": source.house,
            "status": status,
            "subject": title,
            "date_start": date_start,
            "date_end": date_end,
            "source_url": source.url,
            "source_system": "senado_archive",
            "extraction_method": "pdf_table_regex",
            "source_ref": req_code,
            "date_precision": "day" if date_start else "unknown",
            "run_id": run_id,
        })

        requirements.append({
            "requirement_id": requirement_id,
            "inquiry_id": inquiry_id,
            "type": "REQUERIMENTO",
            "date": date_start,
            "text": title,
            "status": status,
            "author_name": author_name,
            "author_cpf": "",
            "source_url": source.url,
            "source_system": "senado_archive",
            "extraction_method": "pdf_table_regex",
            "source_ref": req_code,
            "date_precision": "day" if date_start else "unknown",
            "run_id": run_id,
        })

        if date_end:
            sessions.append({
                "session_id": f"{inquiry_id}-closing-{date_end}",
                "inquiry_id": inquiry_id,
                "date": date_end,
                "topic": "encerramento da comissao",
                "source_url": source.url,
                "source_system": "senado_archive",
                "extraction_method": "pdf_table_regex",
                "source_ref": f"{req_code}:closing",
                "date_precision": "day",
                "run_id": run_id,
            })

    return (
        _dedupe(inquiries, "inquiry_id"),
        _dedupe(requirements, "requirement_id"),
        _dedupe(sessions, "session_id"),
    )


def fetch_archive_historical(
    client: httpx.Client,
    run_id: str,
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    inquiries: list[dict[str, Any]] = []
    requirements: list[dict[str, Any]] = []
    sessions: list[dict[str, Any]] = []
    history_sources: list[dict[str, Any]] = []

    for source in ARCHIVE_SOURCES:
        response = client.get(source.url, timeout=120, follow_redirects=True)
        response.raise_for_status()
        payload = response.content
        checksum = hashlib.sha256(payload).hexdigest()
        text = _read_pdf_text(payload)
        parsed_inquiries, parsed_requirements, parsed_sessions = parse_archive_text(
            text=text,
            source=source,
            run_id=run_id,
        )

        inquiries.extend(parsed_inquiries)
        requirements.extend(parsed_requirements)
        sessions.extend(parsed_sessions)
        history_sources.append({
            "source_url": source.url,
            "doc_type": "pdf",
            "period_start": source.period_start,
            "period_end": source.period_end,
            "house": source.house,
            "kind": source.kind,
            "parser_method": "pypdf_regex_table",
            "checksum": checksum,
            "retrieved_at_utc": datetime.now(tz=UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        })

    return (
        _dedupe(inquiries, "inquiry_id"),
        _dedupe(requirements, "requirement_id"),
        _dedupe(sessions, "session_id"),
        history_sources,
    )


@click.command()
@click.option("--output-dir", default="./data/senado_cpis", help="Output directory")
@click.option(
    "--strict-history-completeness/--allow-partial-history",
    default=True,
    help="Fail if historical archive parsing yields zero inquiries.",
)
@click.option(
    "--manifest-path",
    default=None,
    help="Optional manifest JSON output path (default: <output-dir>/archive_manifest.json).",
)
def main(
    output_dir: str,
    strict_history_completeness: bool,
    manifest_path: str | None,
) -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    run_id = f"senado_archive_{datetime.now(tz=UTC).strftime('%Y%m%d%H%M%S')}"
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    status = "ok"
    error: str | None = None
    inquiries: list[dict[str, Any]] = []
    requirements: list[dict[str, Any]] = []
    sessions: list[dict[str, Any]] = []
    history_sources: list[dict[str, Any]] = []

    try:
        with httpx.Client(follow_redirects=True) as client:
            inquiries, requirements, sessions, history_sources = fetch_archive_historical(
                client=client,
                run_id=run_id,
            )
        if strict_history_completeness and not inquiries:
            raise click.ClickException("Historical archive returned zero inquiries in strict mode.")

        _write_csv(output / "inquiries.csv", inquiries)
        _write_csv(output / "requirements.csv", requirements)
        _write_csv(output / "sessions.csv", sessions)
        _write_csv(output / "members.csv", [])
        _write_csv(output / "history_sources.csv", history_sources)
    except Exception as exc:  # noqa: BLE001
        status = "error"
        error = str(exc)
        if strict_history_completeness:
            raise
        logger.warning("Archive extraction failed in partial mode: %s", exc)

    manifest = {
        "generated_at_utc": datetime.now(tz=UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "run_id": run_id,
        "source_id": "senado_cpis_archive",
        "window_start": (
            min(
                (row.get("date_start", "") for row in inquiries if row.get("date_start")),
                default="",
            )
        ),
        "window_end": (
            max((row.get("date_end", "") for row in inquiries if row.get("date_end")), default="")
        ),
        "rows": len(inquiries) + len(requirements) + len(sessions),
        "checksum": hashlib.sha256(
            "|".join(sorted(row.get("inquiry_id", "") for row in inquiries)).encode("utf-8")
        ).hexdigest(),
        "retrieved_at_utc": datetime.now(tz=UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "status": status,
        "strict_history_completeness": strict_history_completeness,
        "counts": {
            "inquiries": len(inquiries),
            "requirements": len(requirements),
            "sessions": len(sessions),
            "history_sources": len(history_sources),
        },
        "error": error,
    }
    manifest_file = Path(manifest_path) if manifest_path else output / "archive_manifest.json"
    manifest_file.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    logger.info("Wrote archive manifest: %s", manifest_file)


if __name__ == "__main__":
    main()
