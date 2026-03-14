"""Boletín Oficial de la República Argentina.

Ingests decrees, resolutions, appointments, and regulatory acts.
Analogous to Brazil's DOU (Diário Oficial da União).

Source: https://www.boletinoficial.gob.ar/
Status: STUB
"""

import logging

from aracc_etl.base import Pipeline

logger = logging.getLogger(__name__)


class BoletinOficialPipeline(Pipeline):
    name = "boletin_oficial"
    source_id = "boletin_oficial"

    def extract(self) -> None:
        raise NotImplementedError("Boletín Oficial extract not yet implemented")

    def transform(self) -> None:
        raise NotImplementedError("Boletín Oficial transform not yet implemented")

    def load(self) -> None:
        raise NotImplementedError("Boletín Oficial load not yet implemented")
