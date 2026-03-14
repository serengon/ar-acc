"""UIF — Unidad de Información Financiera / PEPs.

Ingests the list of Politically Exposed Persons from UIF.
Analogous to Brazil's CGU PEP list.

Source: https://www.argentina.gob.ar/uif
Status: STUB
"""

import logging

from aracc_etl.base import Pipeline

logger = logging.getLogger(__name__)


class UifPepsPipeline(Pipeline):
    name = "uif_peps"
    source_id = "uif_peps"

    def extract(self) -> None:
        raise NotImplementedError("UIF PEPs extract not yet implemented")

    def transform(self) -> None:
        raise NotImplementedError("UIF PEPs transform not yet implemented")

    def load(self) -> None:
        raise NotImplementedError("UIF PEPs load not yet implemented")
