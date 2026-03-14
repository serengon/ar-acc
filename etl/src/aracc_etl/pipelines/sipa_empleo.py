"""SIPA / MTEySS — Sistema Integrado Previsional Argentino.

Ingests labor and employment statistics.
Analogous to Brazil's RAIS / CAGED.

Source: https://datos.gob.ar/ (MTEySS datasets)
Status: STUB
"""

import logging

from aracc_etl.base import Pipeline

logger = logging.getLogger(__name__)


class SipaEmpleoPipeline(Pipeline):
    name = "sipa_empleo"
    source_id = "sipa_empleo"

    def extract(self) -> None:
        raise NotImplementedError("SIPA empleo extract not yet implemented")

    def transform(self) -> None:
        raise NotImplementedError("SIPA empleo transform not yet implemented")

    def load(self) -> None:
        raise NotImplementedError("SIPA empleo load not yet implemented")
