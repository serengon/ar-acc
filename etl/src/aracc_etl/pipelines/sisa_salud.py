"""SISA/REFES — Sistema Integrado de Información Sanitaria Argentina.

Ingests health establishment data (hospitals, clinics).
Analogous to Brazil's DataSUS CNES.

Source: https://sisa.msal.gov.ar/
Status: STUB
"""

import logging

from aracc_etl.base import Pipeline

logger = logging.getLogger(__name__)


class SisaSaludPipeline(Pipeline):
    name = "sisa_salud"
    source_id = "sisa_salud"

    def extract(self) -> None:
        raise NotImplementedError("SISA salud extract not yet implemented")

    def transform(self) -> None:
        raise NotImplementedError("SISA salud transform not yet implemented")

    def load(self) -> None:
        raise NotImplementedError("SISA salud load not yet implemented")
