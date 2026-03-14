"""AFIP Padrón de Contribuyentes pipeline.

Ingests CUIT/CUIL registry data from AFIP (Administración Federal de Ingresos
Públicos). This is the core identity source for Argentine companies and persons,
analogous to Brazil's CNPJ/CPF from Receita Federal.

Source: https://www.afip.gob.ar/genericos/cInscripcion/
Status: STUB — extract logic pending (requires scraping or AFIP web services)
"""

import logging

from aracc_etl.base import Pipeline

logger = logging.getLogger(__name__)


class AfipContribuyentesPipeline(Pipeline):
    name = "afip_contribuyentes"
    source_id = "afip_contribuyentes"

    def extract(self) -> None:
        raise NotImplementedError("AFIP contribuyentes extract not yet implemented")

    def transform(self) -> None:
        raise NotImplementedError("AFIP contribuyentes transform not yet implemented")

    def load(self) -> None:
        raise NotImplementedError("AFIP contribuyentes load not yet implemented")
