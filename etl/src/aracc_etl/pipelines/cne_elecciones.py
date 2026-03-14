"""CNE — Cámara Nacional Electoral / Resultados Electorales.

Ingests election results, candidate data, and campaign financing.
Analogous to Brazil's TSE.

Source: https://www.electoral.gob.ar/
Data: https://datos.gob.ar/dataset/dine-resultados-electorales
Status: STUB
"""

import logging

from aracc_etl.base import Pipeline

logger = logging.getLogger(__name__)


class CneEleccionesPipeline(Pipeline):
    name = "cne_elecciones"
    source_id = "cne_elecciones"

    def extract(self) -> None:
        raise NotImplementedError("CNE elecciones extract not yet implemented")

    def transform(self) -> None:
        raise NotImplementedError("CNE elecciones transform not yet implemented")

    def load(self) -> None:
        raise NotImplementedError("CNE elecciones load not yet implemented")
