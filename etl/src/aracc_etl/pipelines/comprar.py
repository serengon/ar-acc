"""COMPR.AR — Sistema de Contrataciones Electrónicas del Estado.

Ingests public procurement data: contracts, bids, and supplier information.
Analogous to Brazil's ComprasNet / PNCP.

Source: https://comprar.gob.ar/
API: https://datos.gob.ar/dataset/otros-contrataciones-702
Status: STUB
"""

import logging

from aracc_etl.base import Pipeline

logger = logging.getLogger(__name__)


class ComprarPipeline(Pipeline):
    name = "comprar"
    source_id = "comprar"

    def extract(self) -> None:
        raise NotImplementedError("Comprar extract not yet implemented")

    def transform(self) -> None:
        raise NotImplementedError("Comprar transform not yet implemented")

    def load(self) -> None:
        raise NotImplementedError("Comprar load not yet implemented")
