"""Pydantic models for DDJJ (Declaraciones Juradas) CSV validation."""

from pydantic import BaseModel


class DeclaracionRow(BaseModel):
    """Row from the principal declaraciones-juradas CSV (57 columns)."""

    tipo_declaracion_jurada_id: int | None = None
    desde: str | None = None
    hasta: str | None = None
    periodo_inicio_cierre: str | None = None
    organismo: str | None = None
    cargo: str | None = None
    cuit: str | None = None
    nombres: str | None = None
    apellido: str | None = None
    # Monetary fields — dash-separated decimals (e.g. 35278884-41)
    total_bienes_del_pais_inicio: str | None = None
    total_bienes_del_exterior_inicio: str | None = None
    total_bienes_inicio: str | None = None
    total_deudas_del_pais_inicio: str | None = None
    total_deudas_del_exterior_inicio: str | None = None
    total_deudas_inicio: str | None = None
    total_bienes_del_pais_cierre: str | None = None
    total_bienes_del_exterior_cierre: str | None = None
    total_bienes_cierre: str | None = None
    total_deudas_del_pais_cierre: str | None = None
    total_deudas_del_exterior_cierre: str | None = None
    total_deudas_cierre: str | None = None
    ingreso_neto_anual: str | None = None
    ingreso_neto_anual_del_cargo: str | None = None
    ingreso_bruto_anual: str | None = None
    ingreso_bruto_anual_del_cargo: str | None = None
    gastos_del_pais: str | None = None
    gastos_del_exterior: str | None = None
    total_gastos: str | None = None
    total_ingresos_otros_neto: str | None = None
    total_ingresos_otros_bruto: str | None = None


class BienRow(BaseModel):
    """Row from the bienes CSV."""

    cuit: str | None = None
    nombres: str | None = None
    apellido: str | None = None
    tipo_bien: str | None = None
    sub_tipo_bien: str | None = None
    lugar_radicacion_pais: str | None = None
    lugar_radicacion_provincia: str | None = None
    descripcion: str | None = None
    valor_moneda: str | None = None
    valor: float | None = None
    porcentaje_titularidad: float | None = None
    periodo_inicio_cierre: str | None = None
    desde: str | None = None


class DeudaRow(BaseModel):
    """Row from the deudas CSV."""

    cuit: str | None = None
    nombres: str | None = None
    apellido: str | None = None
    tipo_deuda: str | None = None
    sub_tipo_deuda: str | None = None
    lugar_radicacion_pais: str | None = None
    lugar_radicacion_provincia: str | None = None
    descripcion: str | None = None
    valor_moneda: str | None = None
    monto: float | None = None
    porcentaje_titularidad: float | None = None
    periodo_inicio_cierre: str | None = None
    desde: str | None = None


class FamiliarRow(BaseModel):
    """Row from the grupo-familiar CSV."""

    cuit: str | None = None
    nombres: str | None = None
    apellido: str | None = None
    familiar_nombres: str | None = None
    familiar_apellido: str | None = None
    familiar_tipo_documento: str | None = None
    familiar_documento: str | None = None
    vinculo_familiar_tipo: str | None = None
    actividad_familiar: str | None = None
    desde: str | None = None
    hasta: str | None = None
    periodo_inicio_cierre: str | None = None
