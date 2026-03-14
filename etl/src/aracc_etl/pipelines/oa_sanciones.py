"""OA — Oficina Anticorrupción / Sanciones e inhabilitados.

Ingests sanctions, debarment, and integrity data.
Analogous to Brazil's CEIS/CNEP.

Source: https://www.argentina.gob.ar/anticorrupcion
Status: STUB
"""

import logging

from aracc_etl.base import Pipeline

logger = logging.getLogger(__name__)


class OaSancionesPipeline(Pipeline):
    name = "oa_sanciones"
    source_id = "oa_sanciones"

    def extract(self) -> None:
        raise NotImplementedError("OA sanciones extract not yet implemented")

    def transform(self) -> None:
        raise NotImplementedError("OA sanciones transform not yet implemented")

    def load(self) -> None:
        raise NotImplementedError("OA sanciones load not yet implemented")
