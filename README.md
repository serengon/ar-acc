# ar/acc open graph

**Infraestructura open-source de grafos que cruza bases de datos públicas argentinas para generar inteligencia cívica accionable.**

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

> Fork de [br/acc](https://github.com/World-Open-Graph/br-acc) adaptado para Argentina.

---

## Qué es ar/acc?

ar/acc es una infraestructura open-source que ingesta bases de datos públicas argentinas — registros de contribuyentes, contrataciones, resultados electorales, datos judiciales, sanciones, presupuesto, salud, educación — y las normaliza en un único grafo consultable.

Hace accesible en un solo lugar información pública que hoy está dispersa en decenas de portales. No interpreta, no califica, no rankea — muestra conexiones y deja que los usuarios saquen sus propias conclusiones.

---

## Arquitectura

| Componente | Tecnología | Descripción |
|---|---|---|
| **ETL** | Python 3.12+ / uv | 24 pipelines de ingesta de datos públicos |
| **API** | FastAPI | Acceso programático al grafo |
| **Frontend** | React + Vite | UI para buscar y explorar redes |
| **Infra** | Neo4j + Docker + Caddy | Grafo, contenedores, reverse proxy |

---

## Pipelines disponibles

### Tier 0 — Identidad y contrataciones (core)

| Pipeline | Fuente | Dato |
|---|---|---|
| `afip_contribuyentes` | AFIP | Padrón CUIT/CUIL, contribuyentes |
| `igj_sociedades` | IGJ | Registro societario, directores |
| `comprar` | COMPR.AR | Contrataciones del Estado |
| `cne_elecciones` | CNE | Resultados electorales, financiamiento |
| `boletin_oficial` | Boletín Oficial | Decretos, resoluciones, designaciones |

### Tier 1 — Enriquecimiento

| Pipeline | Fuente | Dato |
|---|---|---|
| `bcra_deudores` | BCRA | Central de deudores |
| `cnv` | CNV | Sanciones mercado de valores |
| `agn` | AGN | Informes de auditoría |
| `hcdn_gastos` | HCDN | Gastos de diputados |
| `hsn_gastos` | HSN | Gastos de senadores |
| `oa_sanciones` | Oficina Anticorrupción | Sancionados e inhabilitados |
| `ddjj_funcionarios` | OA | Declaraciones juradas patrimoniales |
| `uif_peps` | UIF | Personas expuestas políticamente |
| `presupuesto_abierto` | Min. Economía | Ejecución presupuestaria |
| `sipa_empleo` | MTEySS | Estadísticas laborales |
| `sisa_salud` | SISA/REFES | Establecimientos de salud |
| `educacion` | Min. Educación | Establecimientos educativos |
| `cij_judicial` | CIJ | Resoluciones judiciales |

### Internacional (compartidas con br/acc)

| Pipeline | Fuente |
|---|---|
| `icij` | ICIJ Offshore Leaks |
| `opensanctions` | OpenSanctions PEP global |
| `ofac` | US Treasury OFAC |
| `eu_sanctions` | EU Consolidated Sanctions |
| `un_sanctions` | UN Security Council |
| `world_bank` | World Bank Debarment |

> Todos los pipelines están en estado **STUB** — la estructura está lista, falta implementar la lógica de extracción para cada fuente.

---

## Quick Start

```bash
cp .env.example .env
docker compose up -d --build
```

Verificar:

- API: http://localhost:9000/health
- API Docs: http://localhost:9000/docs
- Frontend: http://localhost:9100
- Neo4j Browser: http://localhost:9474

---

## Modelo de datos

El grafo usa CUIL (personas, formato `XX-XXXXXXXX-X`) y CUIT (empresas, mismo formato) como claves primarias, equivalentes al CPF/CNPJ brasileño.

### Nodos principales

- `Person` (cuil, dni, name, provincia)
- `Company` (cuit, razon_social, actividad_principal)
- `Contract` (contract_id, value, object, organismo)
- `Election` (year, cargo, provincia, distrito)
- `Sanction` (sanction_id, type, date_start, source)
- `Expense` (expense_id, date, type, value)
- `BoletinAct` (act_id, date, act_type)
- `Health` / `Education` / `LegalCase` / ...

### Relaciones

- `SOCIO_DE` — participación societaria
- `CANDIDATO_EN` — candidatura electoral
- `CONTRATADO_POR` — contrato estatal
- `SANCIONADA` — sanción administrativa
- `GASTOU` — gasto legislativo
- `PARTE_PROCESO` — parte en causa judicial
- Y más...

---

## Desarrollo

```bash
# ETL
cd etl && uv run aracc-etl sources

# API
cd api && uv run uvicorn aracc.main:app --reload

# Frontend
cd frontend && npm run dev

# Tests
make test
```

---

## Contribuir

1. Fork este repo
2. Elegí un pipeline STUB de la lista
3. Implementá `extract()`, `transform()`, `load()`
4. Agregá tests en `etl/tests/`
5. Abrí un PR

Las contribuciones más valiosas son implementaciones de pipelines con fuentes reales de datos argentinos.

---

## Licencia

AGPL-3.0 — mismo que el proyecto original br/acc.

---

## Créditos

Fork de [World-Open-Graph/br-acc](https://github.com/World-Open-Graph/br-acc).
