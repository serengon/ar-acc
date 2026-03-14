"""OpenSanctions — Global PEP and sanctions database.

International source, same as br/acc.

Source: https://www.opensanctions.org/
Status: STUB — reuse br/acc logic
"""

import logging

from aracc_etl.base import Pipeline

logger = logging.getLogger(__name__)


class OpenSanctionsPipeline(Pipeline):
    name = "opensanctions"
    source_id = "opensanctions"

    def extract(self) -> None:
        raise NotImplementedError("OpenSanctions extract not yet implemented")

    def transform(self) -> None:
        raise NotImplementedError("OpenSanctions transform not yet implemented")

    def load(self) -> None:
        raise NotImplementedError("OpenSanctions load not yet implemented")
