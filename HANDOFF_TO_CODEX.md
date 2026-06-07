# HANDOFF_TO_CODEX.md

> **Canal principal Claude → Codex.** Leer ANTES de cualquier acción.

**Última actualización:** 2026-06-07
**Actualizado por:** Codex
**Versión del handoff:** v0006
**Archivo anterior:** `docs/handoff_archive/HANDOFF_2026-06-07_v0005.md`

---

## 1. Estado actual

- **Fase activa:** Fase 2 — ingest/EDA, condicionada por audios reales.
- **Hitos alcanzados:**
  - T-000, T-001, T-010, T-011, T-012 ✅ Done.
  - T-014 ✅ Web shell estático Hallmark-styled con `src/frogiso/web/`, `scripts/run_web.py`, `outputs/web/tokens.css` y landing generada.
  - Repo instalable, 29 tests pasando.
- **Decisión nueva:** **ADR-010** — GUI vía **Hallmark + HTML estático generado**, sin servidor. Frontend coherente en `outputs/web/`, generado por `src/frogiso/web/` con Jinja2.
- **Verificación T-014:** `python scripts/run_web.py --view landing`, `pytest tests/test_web.py`, `pytest tests/` y medición CDP responsive a 320/375/414/768 px OK.
- **Dependencia añadida:** `jinja2` registrada en `pyproject.toml` y `ARCHITECTURE.md §8`.

---

## 2. Tarea siguiente

### **Siguiente paso**

1. **Si hay audios reales en `data/raw/`:** ejecutar T-013 (ingest) para crear `metadata/recordings.csv`.
2. **Si no hay audios:** avanzar a T-020 + T-021 + T-022 (EDA + galería web). En el `CODEX_PROMPTS.md` local de 2026-06-07, T-020/T-021 corresponden a **PROMPT 3**; T-022 está en `TASKS.md` como extensión Hallmark dependiente de T-014.

Nota de consistencia: algunas instrucciones externas llaman "PROMPT 4" a la ruta T-013/T-020/T-022, pero el archivo local verificable usa `PROMPT 3` para espectrogramas y `PROMPT 4` para band-pass. Seguir los tickets y `ARCHITECTURE.md`.

---

## 3. Archivos relevantes

| Archivo | Para qué |
|---|---|
| `ARCHITECTURE.md` (§3, §8, §9 AS-09) | Módulo `web/`, jinja2 como dep base, AS-09. |
| `DECISIONS.md` ADR-010 | Estrategia GUI: Hallmark estático, no servidor. |
| `TASKS.md` | T-014, T-022, T-052, T-062, T-084, T-101 añadidas. |
| `CODEX_PROMPTS.md` PROMPT 3 | T-020/T-021 espectrogramas batch + notebook EDA. |
| `src/frogiso/web/render.py` | Renderizador Jinja2 y tokens Hallmark para vistas estáticas. |
| `outputs/web/tokens.css` | Tokens locked de Hallmark reutilizables por vistas futuras. |
| Skill `hallmark` | `~/.agents/skills/hallmark/SKILL.md` (v1.1.0). Usar default/audit/redesign/study según corresponda. |

---

## 4. Riesgos abiertos

| Riesgo | Mitigación |
|---|---|
| Vistas futuras podrían improvisar tokens fuera de `outputs/web/tokens.css`. | Gate 48: reutilizar tokens locked de T-014; añadir tokens sólo si se centralizan allí. |
| Vistas futuras podrían inventar métricas para rellenar dashboard. | Gate 46: leer manifests/reportes reales o usar `—`/placeholder explícito. |
| Riesgo de añadir deps de UI (React, Tailwind, etc.) | Bloque obligatorio + PROMPT 2.5 lo prohíben explícitamente. |
| Vistas posteriores podrían divergir del design language | Gate "Locked tokens" + reuso obligatorio de `outputs/web/tokens.css`. |
| Audios reales aún no subidos físicamente | T-013 queda condicionado al upload del humano. Si no hay audios, avanzar EDA con la ruta que el humano indique. |

---

## 5. Preguntas abiertas

- **¿Especies objetivo concretas?** Sin esto, `configs/species/generic.yaml` queda en banda 1500–4000 Hz.
- **¿Hay audios en `data/raw/`?** Si sí, T-013; si no, pedir/usar un directorio externo para T-020/T-021.

---

## 6. Qué puede modificar Codex

✅ Todo lo bajo `src/`, `scripts/`, `tests/`, `configs/`, `notebooks/` que corresponda al ticket.
✅ `src/frogiso/web/` y `outputs/web/` para vistas estáticas Hallmark.
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
| 1.5 (web shell) | Done (T-014) |
| 2 | Planned (T-013 condicionado a audios, T-020/T-021/T-022) |
| 3–10 | Planned |

(Fuente autoritativa: `ROADMAP.md` y `TASKS.md`.)
