"""BCRA — Central de Deudores del Sistema Financiero.

Ingests debtor records from the Argentine Central Bank.
Analogous to Brazil's PGFN (deuda activa).

Source: https://www.bcra.gob.ar/BCRAyVos/Situacion_Crediticia.asp
Status: STUB
"""

import logging

from aracc_etl.base import Pipeline

logger = logging.getLogger(__name__)


class BcraDeudoresPipeline(Pipeline):
    name = "bcra_deudores"
    source_id = "bcra_deudores"

    def extract(self) -> None:
        raise NotImplementedError("BCRA deudores extract not yet implemented")

    def transform(self) -> None:
        raise NotImplementedError("BCRA deudores transform not yet implemented")

    def load(self) -> None:
        raise NotImplementedError("BCRA deudores load not yet implemented")
