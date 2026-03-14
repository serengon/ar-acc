"""HSN — Honorable Senado de la Nación.

Ingests senate expense data and parliamentary activity.
Analogous to Brazil's Senado CEAPS expenses.

Source: https://www.senado.gob.ar/
Status: STUB
"""

import logging

from aracc_etl.base import Pipeline

logger = logging.getLogger(__name__)


class HsnGastosPipeline(Pipeline):
    name = "hsn_gastos"
    source_id = "hsn_gastos"

    def extract(self) -> None:
        raise NotImplementedError("HSN gastos extract not yet implemented")

    def transform(self) -> None:
        raise NotImplementedError("HSN gastos transform not yet implemented")

    def load(self) -> None:
        raise NotImplementedError("HSN gastos load not yet implemented")
