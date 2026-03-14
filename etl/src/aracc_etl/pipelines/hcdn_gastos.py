"""HCDN — Honorable Cámara de Diputados de la Nación.

Ingests legislative expense data, voting records, and parliamentary activity.
Analogous to Brazil's Câmara CEAP expenses.

Source: https://www.hcdn.gob.ar/
Data: https://datos.hcdn.gob.ar/
Status: STUB
"""

import logging

from aracc_etl.base import Pipeline

logger = logging.getLogger(__name__)


class HcdnGastosPipeline(Pipeline):
    name = "hcdn_gastos"
    source_id = "hcdn_gastos"

    def extract(self) -> None:
        raise NotImplementedError("HCDN gastos extract not yet implemented")

    def transform(self) -> None:
        raise NotImplementedError("HCDN gastos transform not yet implemented")

    def load(self) -> None:
        raise NotImplementedError("HCDN gastos load not yet implemented")
