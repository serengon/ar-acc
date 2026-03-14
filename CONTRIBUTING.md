# Contribuir a ar/acc

Gracias por querer mejorar ar/acc.

## Reglas base

- Mantené los cambios alineados con el objetivo de transparencia cívica.
- No agregues secretos, credenciales ni datos de infraestructura privada.
- Respetá los defaults de privacidad y las restricciones legales (Ley 25.326).

## Setup

```bash
# 1. Cloná y configurá hooks
git clone https://github.com/serengon/ar-acc.git
cd ar-acc
make setup-hooks

# 2. Instalá dependencias
cd api && uv sync --dev
cd ../etl && uv sync --dev
cd ../frontend && npm install
```

## Git Flow

**Leé [GIT_FLOW.md](GIT_FLOW.md) para el flujo completo.**

Resumen rápido:

```bash
# Partí de develop
git checkout develop && git pull
git checkout -b feature/pipeline-comprar

# Trabajá con conventional commits
git commit -m "feat(etl): implement comprar extract"

# PR a develop
git push -u origin feature/pipeline-comprar
```

Los hooks locales validan:
- No commits directos a `main`
- Formato Conventional Commits
- No force push a branches protegidos

## Seguridad y entorno

- **Frontend env:** Solo variables `VITE_*` se exponen al cliente. No pongas secretos ahí.
- **Auth:** Tokens en memoria o HttpOnly cookies. No uses `localStorage`.
- **Releases:** Corré `npm audit` en `frontend/` antes de releases.

## Checks de calidad

Corré antes de abrir un PR:

```bash
make check
```

## Cómo implementar un pipeline

1. Elegí un pipeline STUB de `etl/src/aracc_etl/pipelines/`
2. Implementá `extract()`, `transform()`, `load()` siguiendo el patrón de `base.py`
3. Agregá tests en `etl/tests/test_{pipeline}_pipeline.py`
4. Agregá fixtures de ejemplo en `etl/tests/fixtures/`
5. Abrí PR a `develop` con conventional commits

## Pull Requests

- Scope acotado, explicá el impacto.
- Incluí tests para cambios de comportamiento.
- Actualizá docs si cambian interfaces o workflows.
- CI en verde antes de pedir review.

## Contribuciones con IA

Las contribuciones asistidas por IA son bienvenidas.
El contribuyente humano es responsable de:
- Corrección técnica
- Compliance de seguridad/privacidad
- Review final antes del merge
