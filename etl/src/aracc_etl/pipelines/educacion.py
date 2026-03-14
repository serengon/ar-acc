"""DINIECE / Ministerio de Educación — Establecimientos educativos.

Ingests school and educational establishment census data.
Analogous to Brazil's INEP.

Source: https://datos.gob.ar/ (education datasets)
Status: STUB
"""

import logging

from aracc_etl.base import Pipeline

logger = logging.getLogger(__name__)


class EducacionPipeline(Pipeline):
    name = "educacion"
    source_id = "educacion"

    def extract(self) -> None:
        raise NotImplementedError("Educación extract not yet implemented")

    def transform(self) -> None:
        raise NotImplementedError("Educación transform not yet implemented")

    def load(self) -> None:
        raise NotImplementedError("Educación load not yet implemented")
