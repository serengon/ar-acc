"""AGN — Auditoría General de la Nación.

Ingests audit reports and findings from the national audit body.
Analogous to Brazil's TCU.

Source: https://www.agn.gob.ar/
Status: STUB
"""

import logging

from aracc_etl.base import Pipeline

logger = logging.getLogger(__name__)


class AgnPipeline(Pipeline):
    name = "agn"
    source_id = "agn"

    def extract(self) -> None:
        raise NotImplementedError("AGN extract not yet implemented")

    def transform(self) -> None:
        raise NotImplementedError("AGN transform not yet implemented")

    def load(self) -> None:
        raise NotImplementedError("AGN load not yet implemented")
