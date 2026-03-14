# Git Flow — ar/acc

## Branches

```
main            ← producción, siempre deployable, protegida
develop         ← integración, rama default, acá se mergean PRs
feature/*       ← una feature o pipeline nuevo
hotfix/*        ← fix urgente que va directo a main
release/*       ← preparación de release (opcional)
```

### Reglas

| Branch | Push directo | Force push | Quién mergea |
|---|---|---|---|
| `main` | Prohibido | Prohibido | Solo desde `develop` o `hotfix/*` via PR |
| `develop` | Permitido para maintainers | Prohibido | Feature PRs aprobados |
| `feature/*` | Libre | Libre (tu branch) | Autor via PR a `develop` |
| `hotfix/*` | Libre | Libre | Autor via PR a `main` + backport a `develop` |

---

## Flujo diario

### Nueva feature / pipeline

```bash
# 1. Partí de develop actualizado
git checkout develop
git pull origin develop

# 2. Creá tu branch
git checkout -b feature/pipeline-comprar

# 3. Trabajá, commiteá (conventional commits)
git add .
git commit -m "feat(etl): implement comprar pipeline extract"

# 4. Pushea y abrí PR a develop
git push -u origin feature/pipeline-comprar
# → PR a develop en GitHub
```

### Hotfix (fix urgente en producción)

```bash
# 1. Partí de main
git checkout main
git pull origin main
git checkout -b hotfix/fix-cuit-validation

# 2. Fix + commit
git commit -m "fix(etl): correct CUIT check digit for prefix 34"

# 3. PR a main, después backport a develop
git push -u origin hotfix/fix-cuit-validation
# → PR a main
# → Después de merge, cherry-pick o merge a develop
```

### Release

```bash
# 1. Desde develop
git checkout develop
git checkout -b release/1.0.0

# 2. Bumps de versión, changelog, últimos ajustes
git commit -m "chore: prepare release 1.0.0"

# 3. PR a main + tag
# → Merge a main
# → git tag v1.0.0
# → Merge back a develop
```

---

## Convención de nombres

### Branches

```
feature/pipeline-{nombre}     ← pipeline nuevo (ej: feature/pipeline-comprar)
feature/api-{descripcion}     ← cambio en API
feature/frontend-{descripcion} ← cambio en frontend
feature/{descripcion}         ← otros cambios
hotfix/{descripcion}          ← fix urgente
release/{version}             ← preparación de release
```

### Commits — Conventional Commits

```
tipo(alcance): descripción corta
```

**Tipos:**

| Tipo | Cuándo usar |
|---|---|
| `feat` | Nueva funcionalidad |
| `fix` | Corrección de bug |
| `docs` | Solo documentación |
| `style` | Formato, sin cambio de lógica |
| `refactor` | Refactoreo sin cambio funcional |
| `test` | Tests nuevos o modificados |
| `chore` | Mantenimiento, deps, configs |
| `ci` | Cambios en CI/CD |
| `perf` | Mejoras de performance |
| `build` | Build system, dependencias |

**Alcances comunes:** `etl`, `api`, `frontend`, `infra`, `ci`

**Ejemplos:**
```
feat(etl): implement comprar pipeline extract and transform
fix(api): handle null CUIT in entity lookup
docs: add EQUIVALENCIAS with new judicial sources
test(etl): add unit tests for CUIL validation
ci: add branch protection workflow
chore(deps): bump neo4j driver to 5.28
```

---

## Hooks automáticos

El repo incluye hooks en `.githooks/` que se activan con:

```bash
make setup-hooks
```

### Qué hacen:

| Hook | Validación |
|---|---|
| `pre-commit` | Bloquea commits directos a `main` |
| `commit-msg` | Exige formato Conventional Commits |
| `pre-push` | Bloquea force push a `main` y `develop`; avisa si el branch name no sigue la convención |

### Instalación

```bash
# Opción 1: make
make setup-hooks

# Opción 2: manual
git config core.hooksPath .githooks
```

> Los hooks son locales. Cada colaborador los instala una vez al clonar.
> Para enforcement server-side, usamos GitHub branch protection rules.

---

## Protección de branches en GitHub

### `main`
- Require PR con al menos 1 aprobación
- Require status checks (CI) en verde
- No force push
- No delete

### `develop`
- Require status checks (CI) en verde
- No force push
- No delete

---

## Diagrama

```
feature/pipeline-comprar ──→ PR ──→ develop ──→ PR ──→ main ──→ tag v1.0.0
feature/pipeline-bcra    ──→ PR ──↗                        ↑
                                                           │
hotfix/fix-cuit ─────────────────────────── PR ────────────┘
                                              └──→ backport a develop
```
