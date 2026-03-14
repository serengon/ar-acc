"""CIJ — Centro de Información Judicial.

Ingests judicial resolution data from the Argentine judiciary.
Analogous to Brazil's DataJud.

Source: https://www.cij.gov.ar/
Status: STUB
"""

import logging

from aracc_etl.base import Pipeline

logger = logging.getLogger(__name__)


class CijJudicialPipeline(Pipeline):
    name = "cij_judicial"
    source_id = "cij_judicial"

    def extract(self) -> None:
        raise NotImplementedError("CIJ judicial extract not yet implemented")

    def transform(self) -> None:
        raise NotImplementedError("CIJ judicial transform not yet implemented")

    def load(self) -> None:
        raise NotImplementedError("CIJ judicial load not yet implemented")
