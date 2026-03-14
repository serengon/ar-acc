"""UN Consolidated Sanctions List.

International source, same as br/acc.

Source: https://www.un.org/securitycouncil/content/un-sc-consolidated-list
Status: STUB — reuse br/acc logic
"""

import logging

from aracc_etl.base import Pipeline

logger = logging.getLogger(__name__)


class UnSanctionsPipeline(Pipeline):
    name = "un_sanctions"
    source_id = "un_sanctions"

    def extract(self) -> None:
        raise NotImplementedError("UN sanctions extract not yet implemented")

    def transform(self) -> None:
        raise NotImplementedError("UN sanctions transform not yet implemented")

    def load(self) -> None:
        raise NotImplementedError("UN sanctions load not yet implemented")
