# Git Conventions — ar/acc

## Branching (git-flow)

- `main` — producción. No se commitea ni se force-pushea directo.
- `develop` — branch de integración. Es el default del repo.
- `feature/<nombre>` — funcionalidades nuevas. Se abren desde `develop`, PR a `develop`.
- `fix/<nombre>` — correcciones no urgentes. PR a `develop`.
- `hotfix/<nombre>` — correcciones urgentes en producción. Se abren desde `main`, PR a `main` + backport a `develop`.
- `release/<version>` — preparación de release. Se abre desde `develop`, se mergea a `main` y `develop`.
- `chore/<nombre>`, `docs/<nombre>`, `refactor/<nombre>` — tareas auxiliares. PR a `develop`.

## Commits (Conventional Commits)

Formato: `type(scope): descripción`

### Types

| Type | Uso |
|---|---|
| `feat` | Funcionalidad nueva |
| `fix` | Corrección de bug |
| `docs` | Documentación |
| `style` | Formato, sin cambio de lógica |
| `refactor` | Refactoreo sin cambio de comportamiento |
| `test` | Agregar o corregir tests |
| `chore` | Tareas de mantenimiento |
| `ci` | Cambios en CI/CD |
| `perf` | Mejoras de performance |
| `build` | Cambios en build o dependencias |

### Scopes

| Scope | Componente |
|---|---|
| `etl` | Pipelines de datos (`etl/`) |
| `api` | API FastAPI (`api/`) |
| `frontend` | Frontend React (`frontend/`) |
| `infra` | Docker, Caddy, nginx (`infra/`) |
| `ci` | GitHub Actions, hooks, scripts |

### Ejemplos

```
feat(etl): add AFIP contribuyentes pipeline
fix(api): handle null CUIL in search endpoint
docs(frontend): update component props documentation
refactor(api): extract neo4j connection to dependency
ci: add lint check to PR workflow
```

## Pull Requests

- Feature/fix branches → PR a `develop`
- Hotfix branches → PR a `main`
- Un solo release label por PR
- Los checks de CI y compliance deben pasar antes de mergear
- Idioma del proyecto: español (para UI, docs, y mensajes de commit descriptivos están OK en inglés)
