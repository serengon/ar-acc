"""IGJ — Inspección General de Justicia / Registro Societario.

Ingests corporate registry data: company directors, shareholders, legal form.
Complements AFIP CUIT data with ownership structure.

Source: https://www.argentina.gob.ar/justicia/igj
Status: STUB — IGJ data is not openly available; may require FOIA or scraping
"""

import logging

from aracc_etl.base import Pipeline

logger = logging.getLogger(__name__)


class IgjSociedadesPipeline(Pipeline):
    name = "igj_sociedades"
    source_id = "igj_sociedades"

    def extract(self) -> None:
        raise NotImplementedError("IGJ sociedades extract not yet implemented")

    def transform(self) -> None:
        raise NotImplementedError("IGJ sociedades transform not yet implemented")

    def load(self) -> None:
        raise NotImplementedError("IGJ sociedades load not yet implemented")
