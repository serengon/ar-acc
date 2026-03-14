"""EU Consolidated Sanctions List.

International source, same as br/acc.

Source: https://data.europa.eu/data/datasets/consolidated-list-of-persons-groups-and-entities-subject-to-eu-financial-sanctions
Status: STUB — reuse br/acc logic
"""

import logging

from aracc_etl.base import Pipeline

logger = logging.getLogger(__name__)


class EuSanctionsPipeline(Pipeline):
    name = "eu_sanctions"
    source_id = "eu_sanctions"

    def extract(self) -> None:
        raise NotImplementedError("EU sanctions extract not yet implemented")

    def transform(self) -> None:
        raise NotImplementedError("EU sanctions transform not yet implemented")

    def load(self) -> None:
        raise NotImplementedError("EU sanctions load not yet implemented")
