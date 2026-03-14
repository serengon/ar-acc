"""Presupuesto Abierto — Ejecución presupuestaria del Estado Nacional.

Ingests national budget execution data.
Analogous to Brazil's SICONFI / SIOP.

Source: https://www.presupuestoabierto.gob.ar/
Status: STUB
"""

import logging

from aracc_etl.base import Pipeline

logger = logging.getLogger(__name__)


class PresupuestoAbiertoPipeline(Pipeline):
    name = "presupuesto_abierto"
    source_id = "presupuesto_abierto"

    def extract(self) -> None:
        raise NotImplementedError("Presupuesto Abierto extract not yet implemented")

    def transform(self) -> None:
        raise NotImplementedError("Presupuesto Abierto transform not yet implemented")

    def load(self) -> None:
        raise NotImplementedError("Presupuesto Abierto load not yet implemented")
