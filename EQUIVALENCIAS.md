# Equivalencias Brasil (br/acc) → Argentina (ar/acc)

Mapeo de fuentes de datos públicas entre el proyecto original brasileño y la adaptación argentina.

---

## Identificadores

| Concepto | Brasil | Argentina |
|---|---|---|
| ID persona física | CPF (11 dígitos, `XXX.XXX.XXX-XX`) | CUIL (11 dígitos, `XX-XXXXXXXX-X`) |
| ID persona jurídica | CNPJ (14 dígitos, `XX.XXX.XXX/XXXX-XX`) | CUIT (11 dígitos, `XX-XXXXXXXX-X`) |
| Documento de identidad | RG (varía por estado) | DNI (7-8 dígitos) |
| Registro de contribuyente | Receita Federal | AFIP |
| División geográfica | UF (estado) | Provincia |

---

## Fuentes de datos — Tier 0 (Core)

| Categoría | Brasil (br/acc) | Pipeline BR | Argentina (ar/acc) | Pipeline AR | Acceso AR |
|---|---|---|---|---|---|
| Registro empresarial | Receita Federal CNPJ | `cnpj` | AFIP Padrón de Contribuyentes | `afip_contribuyentes` | Parcial — consulta web AFIP |
| Socios / Directores | CNPJ (tabla Sócios) | `cnpj` | IGJ — Inspección General de Justicia | `igj_sociedades` | Limitado — no hay API pública |
| Contrataciones públicas | ComprasNet / PNCP | `comprasnet`, `pncp` | COMPR.AR | `comprar` | API pública en datos.gob.ar |
| Elecciones y donaciones | TSE | `tse` | CNE — Cámara Nacional Electoral | `cne_elecciones` | datos.gob.ar + electoral.gob.ar |
| Boletín oficial | DOU — Diário Oficial da União | `dou` | Boletín Oficial de la República Argentina | `boletin_oficial` | boletinoficial.gob.ar |

---

## Fuentes de datos — Tier 1 (Enriquecimiento)

| Categoría | Brasil (br/acc) | Pipeline BR | Argentina (ar/acc) | Pipeline AR | Acceso AR |
|---|---|---|---|---|---|
| Deuda / morosidad | PGFN — Dívida Ativa | `pgfn` | BCRA — Central de Deudores | `bcra_deudores` | Consulta pública bcra.gob.ar |
| Mercado de valores | CVM — Comissão de Valores Mobiliários | `cvm`, `cvm_funds` | CNV — Comisión Nacional de Valores | `cnv` | cnv.gov.ar |
| Auditoría estatal | TCU — Tribunal de Contas da União | `tcu` | AGN — Auditoría General de la Nación | `agn` | agn.gob.ar (informes PDF) |
| Gastos diputados | Câmara — CEAP | `camara` | HCDN — Cámara de Diputados | `hcdn_gastos` | datos.hcdn.gob.ar |
| Gastos senadores | Senado — CEAPS | `senado` | HSN — Senado de la Nación | `hsn_gastos` | senado.gob.ar |
| Sanciones / inhabilitados | CEIS / CNEP | `sanctions` | OA — Oficina Anticorrupción | `oa_sanciones` | argentina.gob.ar/anticorrupcion |
| Personas expuestas (PEP) | CGU — Lista PEP | `pep_cgu` | UIF — Unidad de Información Financiera | `uif_peps` | argentina.gob.ar/uif |
| Declaraciones patrimoniales | TSE — Bens de candidatos | `tse_bens` | DDJJ de funcionarios | `ddjj_funcionarios` | OA (parcial) |
| Presupuesto | SICONFI / SIOP | `siconfi`, `siop` | Presupuesto Abierto | `presupuesto_abierto` | presupuestoabierto.gob.ar |
| Empleo / trabajo | RAIS / CAGED | `rais`, `caged` | SIPA / MTEySS | `sipa_empleo` | datos.gob.ar |
| Salud — establecimientos | DataSUS — CNES | `datasus` | SISA / REFES | `sisa_salud` | sisa.msal.gov.ar |
| Educación — establecimientos | INEP — Censo Escolar | `inep` | DINIECE / Min. Educación | `educacion` | datos.gob.ar |
| Justicia | DataJud — CNJ | `datajud` | CIJ — Centro de Información Judicial | `cij_judicial` | cij.gov.ar |
| Banco de desarrollo | BNDES — Operações | `bndes` | — (no hay equivalente directo) | — | — |
| Medio ambiente | IBAMA — Embargos | `ibama` | — (Min. Ambiente, datos dispersos) | — | Pendiente |
| Servidores expulsados | CEAF | `ceaf` | — (no hay registro centralizado) | — | — |
| ONGs impedidas | CEPIM | `cepim` | — | — | — |
| Tarjeta gobierno | CPGF | `cpgf` | — | — | — |
| Viajes oficiales | Viagens a Serviço | `viagens` | — | — | Pendiente |
| Acuerdos de leniencia | Acordos de Leniência | `leniency` | — | — | — |
| Renuncias fiscales | Renúncias Fiscais | `renuncias` | — | — | — |
| Banco Central penalidades | BCB Penalidades | `bcb` | — (BCRA sanciones) | — | Pendiente |
| Holdings | Brasil.IO Holdings | `holdings` | — | — | — |
| Partidos — afiliados | TSE Filiados | `tse_filiados` | — (CNE, no disponible masivo) | — | — |
| CPIs / Comisiones investig. | Senado CPIs | `senado_cpis` | — (Comisiones parlamentarias) | — | Pendiente |
| Licitaciones municipales | MiDES | `mides` | — (municipios dispersos) | — | Pendiente |
| Diarios municipales | Querido Diário | `querido_diario` | — | — | — |
| Supremo Tribunal | STF | `stf` | CSJN — Corte Suprema | — | Pendiente |
| Transferencias federales | TransfereGov / Emendas | `transferegov`, `tesouro_emendas` | — (transferencias a provincias) | — | Pendiente |

---

## Fuentes internacionales (compartidas)

Estas fuentes son idénticas en ambos proyectos, solo cambia el filtro por país.

| Fuente | Pipeline | Descripción |
|---|---|---|
| ICIJ Offshore Leaks | `icij` | Panama Papers, Pandora Papers, etc. |
| OpenSanctions | `opensanctions` | PEPs y sanciones globales |
| OFAC | `ofac` | Sanciones del Tesoro de EE.UU. |
| EU Consolidated Sanctions | `eu_sanctions` | Lista consolidada de sanciones UE |
| UN Security Council | `un_sanctions` | Sanciones del Consejo de Seguridad ONU |
| World Bank Debarment | `world_bank` | Empresas inhabilitadas por el Banco Mundial |

---

## Diferencias clave

| Aspecto | Brasil | Argentina |
|---|---|---|
| **Madurez de datos abiertos** | Muy alta — Portal da Transparência, dados.gov.br, APIs REST | Media — datos.gob.ar existe pero cobertura desigual |
| **Registro societario** | CNPJ incluye socios en datos abiertos | IGJ no publica datos abiertos masivos |
| **Financiamiento electoral** | TSE publica donaciones con CPF | CNE publica menos detalle |
| **Identificador unificado** | CPF (persona) ≠ CNPJ (empresa), formatos distintos | CUIL y CUIT comparten formato, se distinguen por prefijo |
| **Estructura federal** | 26 estados + DF, datos centralizados por órgano federal | 23 provincias + CABA, datos más fragmentados por jurisdicción |
| **Ley de protección de datos** | LGPD | Ley 25.326 de Protección de Datos Personales |

---

## Fuentes argentinas adicionales (sin equivalente en br/acc)

| Fuente | URL | Dato potencial |
|---|---|---|
| Registro de la Propiedad Inmueble (CABA) | — | Titularidad de inmuebles |
| ANSES | anses.gob.ar | Beneficios previsionales (no público) |
| Registro Automotor (DNRPA) | dnrpa.gov.ar | Titularidad vehicular (no público masivo) |
| Procrear / programas sociales | datos.gob.ar | Beneficiarios de programas |
| INDEC | indec.gob.ar | Estadísticas económicas y sociales |
