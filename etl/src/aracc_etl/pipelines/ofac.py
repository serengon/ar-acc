"""OFAC — US Treasury Office of Foreign Assets Control sanctions.

International source, same as br/acc.

Source: https://www.treasury.gov/ofac/downloads/
Status: STUB — reuse br/acc logic
"""

import logging

from aracc_etl.base import Pipeline

logger = logging.getLogger(__name__)


class OfacPipeline(Pipeline):
    name = "ofac"
    source_id = "ofac"

    def extract(self) -> None:
        raise NotImplementedError("OFAC extract not yet implemented")

    def transform(self) -> None:
        raise NotImplementedError("OFAC transform not yet implemented")

    def load(self) -> None:
        raise NotImplementedError("OFAC load not yet implemented")
