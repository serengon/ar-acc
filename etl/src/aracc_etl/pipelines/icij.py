"""ICIJ — International Consortium of Investigative Journalists.

Ingests offshore entity data from ICIJ leaks (Panama Papers, Pandora Papers, etc.).
Same source as br/acc — international, filtered for Argentine connections.

Source: https://offshoreleaks.icij.org/
Status: STUB — reuse br/acc logic, filter by Argentina
"""

import logging

from aracc_etl.base import Pipeline

logger = logging.getLogger(__name__)


class ICIJPipeline(Pipeline):
    name = "icij"
    source_id = "icij"

    def extract(self) -> None:
        raise NotImplementedError("ICIJ extract not yet implemented")

    def transform(self) -> None:
        raise NotImplementedError("ICIJ transform not yet implemented")

    def load(self) -> None:
        raise NotImplementedError("ICIJ load not yet implemented")
