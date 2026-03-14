"""World Bank — Debarred firms list.

International source, same as br/acc.

Source: https://www.worldbank.org/en/projects-operations/procurement/debarred-firms
Status: STUB — reuse br/acc logic
"""

import logging

from aracc_etl.base import Pipeline

logger = logging.getLogger(__name__)


class WorldBankPipeline(Pipeline):
    name = "world_bank"
    source_id = "world_bank"

    def extract(self) -> None:
        raise NotImplementedError("World Bank extract not yet implemented")

    def transform(self) -> None:
        raise NotImplementedError("World Bank transform not yet implemented")

    def load(self) -> None:
        raise NotImplementedError("World Bank load not yet implemented")
