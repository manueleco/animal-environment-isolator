# HANDOFF_TO_CODEX.md

> **Canal principal Claude → Codex.** Leer ANTES de cualquier acción.

**Última actualización:** 2026-06-07
**Actualizado por:** Claude
**Versión del handoff:** v0005
**Archivo anterior:** `docs/handoff_archive/HANDOFF_2026-06-07_v0004.md`

---

## 1. Estado actual

- **Fase activa:** Fase 1.5 nueva — **Web shell + landing Hallmark** (cross-cutting con Fase 2).
- **Hitos alcanzados:**
  - T-000, T-001, T-010, T-011, T-012 ✅ Done.
  - Repo instalable, 24 tests pasando.
- **Decisión nueva:** **ADR-010** — GUI vía **Hallmark + HTML estático generado**, sin servidor. Frontend coherente en `outputs/web/`, generado por `src/frogiso/web/` con Jinja2.
- **Reordenamiento:** se inserta **T-014 (web shell)** ANTES de T-013 (ingest) y T-020 (EDA) para que toda vista posterior publique al frontend desde el inicio.

---

## 2. Tarea siguiente

### **[T-014] Web shell + landing Hallmark-styled**
Prompt: [CODEX_PROMPTS.md §"PROMPT 2.5"](CODEX_PROMPTS.md) (nuevo).

Resumen:
- Crear `src/frogiso/web/` (render.py, templates/).
- Invocar la skill `hallmark` (default) con brief de landing académica.
- Trasladar el output Hallmark a Jinja2 templates + tokens.css separados.
- `scripts/run_web.py --view landing` produce `outputs/web/index.html`.
- Verificar disciplinas Hallmark: pre-emit critique stamp, locked tokens, mobile-responsive, sin chrome fake, sin métricas inventadas.

Después de T-014: PROMPT 3 (T-013 ingest, sólo si hay audios en `data/raw/`) → PROMPT 4 (T-020+T-021+T-022 EDA + galería web) → resto.

---

## 3. Archivos relevantes

| Archivo | Para qué |
|---|---|
| `ARCHITECTURE.md` (§3, §8, §9 AS-09) | Módulo `web/` añadido, jinja2 como dep, AS-09. |
| `DECISIONS.md` ADR-010 | Estrategia GUI: Hallmark estático, no servidor. |
| `TASKS.md` | T-014, T-022, T-052, T-062, T-084, T-101 añadidas. |
| `CODEX_PROMPTS.md` PROMPT 2.5 | Instrucciones operativas T-014. |
| Skill `hallmark` | `~/.agents/skills/hallmark/SKILL.md` (v1.1.0). Invocable por verbos default/audit/redesign/study. |

---

## 4. Riesgos abiertos

| Riesgo | Mitigación |
|---|---|
| Hallmark podría "improvisar" tokens dentro del HTML. | Gate 48 (locked tokens) lo prohíbe. Codex verifica antes de cerrar. |
| Hallmark podría inventar métricas placeholder. | Gate 46. La landing inicial muestra el estado real de fases desde ROADMAP.md o usa `—` marcado como "metric to confirm". |
| Riesgo de añadir deps de UI (React, Tailwind, etc.) | Bloque obligatorio + PROMPT 2.5 lo prohíben explícitamente. |
| Vistas posteriores podrían divergir del design language | Gate "Locked tokens" + reuso obligatorio de `outputs/web/tokens.css`. |
| Audios reales aún no subidos físicamente | T-013 sigue Blocked hasta upload del humano. Resto del trabajo no se bloquea. |

---

## 5. Preguntas abiertas

- **¿Especies objetivo concretas?** Sin esto, `configs/species/generic.yaml` queda en banda 1500–4000 Hz.
- **¿Tienes una preferencia de "vibe" para la landing?** (sobrio académico / editorial / atmosférico / minimal). Si no opinas, Hallmark elegirá del catálogo por sí solo.

---

## 6. Qué puede modificar Codex

✅ Todo lo bajo `src/`, `scripts/`, `tests/`, `configs/`, `notebooks/`.
✅ `src/frogiso/web/` (nuevo).
✅ `outputs/web/` (regenerable).
✅ `REUSE_REPORT.md`, `EXPERIMENT_LOG.md`, `DATASET_NOTES.md`, `TASKS.md`.
✅ `HANDOFF_TO_CODEX.md` (archivando primero la versión vigente).
✅ `DECISIONS.md` añadiendo ADRs nuevas (no editar las existentes).
✅ `pyproject.toml`, `.gitignore`.
✅ Git: add selectivo, commit, push origin main.

## 7. Qué NO puede modificar Codex

❌ `ARCHITECTURE.md` sin ADR previa.
❌ `PROJECT_CONTEXT.md`, `ROADMAP.md`, `CODEX_PROMPTS.md` (sólo Claude).
❌ Schemas de manifest declarados en ARCHITECTURE.md §6 sin ADR.
❌ `data/raw/` (los audios los sube el humano).
❌ Introducir Streamlit / Gradio / FastAPI / React / Tailwind / Bootstrap sin ADR nueva (ADR-010 lo prohíbe).
❌ Historial git: nunca `--force`, nunca `--no-verify`, nunca `--amend` sobre commits ya pusheados.

---

## 8. Estado de fases (snapshot)

| Fase | Estado |
|---|---|
| 0 | Done |
| 1 | Done |
| 1.5 (nueva: web shell) | In Progress (T-014) |
| 2 | Planned (T-013 condicionado a audios, T-020/T-021/T-022) |
| 3–10 | Planned |

(Fuente autoritativa: `ROADMAP.md` y `TASKS.md`.)
