"""DDJJ — Declaraciones Juradas Patrimoniales de Funcionarios.

Ingests asset declarations from public officials.
Analogous to Brazil's TSE candidate asset declarations.

Source: https://www.argentina.gob.ar/anticorrupcion/declaraciones-juradas
Status: STUB
"""

import logging

from aracc_etl.base import Pipeline

logger = logging.getLogger(__name__)


class DdjjFuncionariosPipeline(Pipeline):
    name = "ddjj_funcionarios"
    source_id = "ddjj_funcionarios"

    def extract(self) -> None:
        raise NotImplementedError("DDJJ funcionarios extract not yet implemented")

    def transform(self) -> None:
        raise NotImplementedError("DDJJ funcionarios transform not yet implemented")

    def load(self) -> None:
        raise NotImplementedError("DDJJ funcionarios load not yet implemented")
