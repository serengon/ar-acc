import logging
import os
import re
import time
from typing import Any

from neo4j import Driver
from neo4j.exceptions import TransientError

logger = logging.getLogger(__name__)

_SAFE_KEY = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")

_MAX_RETRIES = 5


class Neo4jBatchLoader:
    """Bulk loader using UNWIND for efficient Neo4j writes."""

    def __init__(
        self,
        driver: Driver,
        batch_size: int = 10_000,
        neo4j_database: str | None = None,
    ) -> None:
        self.driver = driver
        self.batch_size = batch_size
        self.neo4j_database = neo4j_database or os.getenv("NEO4J_DATABASE", "neo4j")
        self._total_written = 0

    def _run_batch_once(self, query: str, batch: list[dict[str, Any]]) -> None:
        with self.driver.session(database=self.neo4j_database) as session:
            session.run(query, {"rows": batch})

    def _run_batches(self, query: str, rows: list[dict[str, Any]]) -> int:
        total = 0
        for i in range(0, len(rows), self.batch_size):
            batch = rows[i : i + self.batch_size]
            self._run_batch_once(query, batch)
            total += len(batch)
            self._total_written += len(batch)
        if total >= 10_000:
            logger.info("  Batch written: %d rows (cumulative: %d)", total, self._total_written)
        return total

    def run_query_with_retry(
        self,
        query: str,
        rows: list[dict[str, Any]],
        batch_size: int = 500,
    ) -> int:
        """Run query in batches with exponential-backoff retry on deadlocks."""
        total = 0
        for i in range(0, len(rows), batch_size):
            batch = rows[i : i + batch_size]
            for attempt in range(_MAX_RETRIES):
                try:
                    self._run_batch_once(query, batch)
                    total += len(batch)
                    self._total_written += len(batch)
                    break
                except TransientError:
                    wait = 2 ** attempt
                    logger.warning(
                        "Deadlock on batch %d, retry %d/%d in %ds",
                        i // batch_size,
                        attempt + 1,
                        _MAX_RETRIES,
                        wait,
                    )
                    time.sleep(wait)
            else:
                logger.error(
                    "Failed batch %d after %d retries, skipping",
                    i // batch_size,
                    _MAX_RETRIES,
                )
            if total > 0 and total % 100_000 == 0:
                logger.info("  Progress: %d rows loaded", total)
        return total

    def load_nodes(
        self,
        label: str,
        rows: list[dict[str, Any]],
        key_field: str,
    ) -> int:
        rows = [r for r in rows if r.get(key_field)]
        all_keys: set[str] = set()
        for r in rows:
            all_keys.update(r.keys())
        all_keys.discard(key_field)
        all_keys = {k for k in all_keys if _SAFE_KEY.match(k)}
        props = ", ".join(
            f"n.{k} = row.{k}" for k in sorted(all_keys)
        ) if rows else ""
        set_clause = f"SET {props}" if props else ""
        query = (
            f"UNWIND $rows AS row "
            f"MERGE (n:{label} {{{key_field}: row.{key_field}}}) "
            f"{set_clause}"
        )
        return self._run_batches(query, rows)

    def load_relationships(
        self,
        rel_type: str,
        rows: list[dict[str, Any]],
        source_label: str,
        source_key: str,
        target_label: str,
        target_key: str,
        properties: list[str] | None = None,
    ) -> int:
        rows = [r for r in rows if r.get("source_key") and r.get("target_key")]
        props = ""
        if properties:
            prop_str = ", ".join(f"r.{p} = row.{p}" for p in properties)
            props = f"SET {prop_str}"
        query = (
            f"UNWIND $rows AS row "
            f"MATCH (a:{source_label} {{{source_key}: row.source_key}}) "
            f"MATCH (b:{target_label} {{{target_key}: row.target_key}}) "
            f"MERGE (a)-[r:{rel_type}]->(b) "
            f"{props}"
        )
        return self._run_batches(query, rows)

    def run_query(self, query: str, rows: list[dict[str, Any]]) -> int:
        return self._run_batches(query, rows)
