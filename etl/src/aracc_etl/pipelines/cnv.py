"""CNV — Comisión Nacional de Valores.

Ingests securities market data: sanctions, issuers, and enforcement actions.
Analogous to Brazil's CVM.

Source: https://www.cnv.gov.ar/
Status: STUB
"""

import logging

from aracc_etl.base import Pipeline

logger = logging.getLogger(__name__)


class CnvPipeline(Pipeline):
    name = "cnv"
    source_id = "cnv"

    def extract(self) -> None:
        raise NotImplementedError("CNV extract not yet implemented")

    def transform(self) -> None:
        raise NotImplementedError("CNV transform not yet implemented")

    def load(self) -> None:
        raise NotImplementedError("CNV load not yet implemented")
