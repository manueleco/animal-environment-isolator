# HANDOFF_TO_CODEX.md

> **Canal principal Claude → Codex.** Leer ANTES de cualquier acción.
> Al cerrar la tarea actual, archivar esta versión y reescribir.

**Última actualización:** 2026-06-07
**Actualizado por:** Claude (arquitecto)
**Versión del handoff:** v0002
**Archivo anterior:** `docs/handoff_archive/HANDOFF_2026-06-07_v0001.md`

---

## 1. Estado actual del proyecto

- **Fase activa:** Fase 0 (auditoría) y Fase 1 (estructura) — listas para arrancar en paralelo conceptual.
- **Hitos alcanzados:**
  - T-000 ✅ Sistema de documentación creado y commiteado.
  - Repo git inicializado, remote `origin` configurado a `https://github.com/manueleco/animal-environment-isolator.git`, rama `main`.
- **Decisiones recientes:**
  - **ADR-002b** — Validación de manifests con **`pandera`**.
  - **ADR-008** — Codex gestiona git (commit + push por tarea cerrada). Protocolo completo en [CODEX_PROMPTS.md §"Bloque obligatorio"](CODEX_PROMPTS.md).
- **Confirmación del humano:**
  - Hay **grabaciones reales disponibles** para subir a `data/raw/` (pendiente upload físico por el humano).

---

## 2. Tareas siguientes (orden estricto)

### **[T-001] Auditar repos previos → poblar REUSE_REPORT.md**
Prompt: [CODEX_PROMPTS.md §"PROMPT 1"](CODEX_PROMPTS.md).
**Bloquea:** T-010 (porque el reuse report condiciona qué módulos arrancar primero).

### **[T-010 + T-011 + T-012] Estructura instalable del proyecto**
Prompt: [CODEX_PROMPTS.md §"PROMPT 2"](CODEX_PROMPTS.md).
**Bloquea:** T-013 y todas las fases siguientes.

### **[T-013] Ingest de grabaciones reales**
Tarea nueva añadida hoy. Cuando el humano suba audios a `data/raw/`, Codex implementa `scripts/run_ingest.py` que calcula sha256, lee duración/SR/channels y puebla `metadata/recordings.csv`.
**Bloquea:** Fase 2+.

---

## 3. Archivos relevantes

| Archivo | Para qué |
|---|---|
| `PROJECT_CONTEXT.md` | Contexto y alcance. |
| `ARCHITECTURE.md` | **Normativo.** Schemas, convenciones, IDs. |
| `ROADMAP.md` | Fases y estados. |
| `TASKS.md` | Tickets con criterios de aceptación. |
| `CODEX_PROMPTS.md` | Prompts oficiales por tarea. |
| `DECISIONS.md` | ADRs vigentes (revisar ADR-002b, ADR-007, ADR-008 antes de codificar). |
| `REUSE_REPORT.md` | Esqueleto a poblar en T-001. |
| `DATASET_NOTES.md` | Convenciones de naming + advertencia sobre synthetic. |

---

## 4. Riesgos abiertos

| Riesgo | Mitigación |
|---|---|
| Codex podría hacer `git add .` ciego y subir binarios/secretos. | Bloque obligatorio exige `git add` selectivo y respeto al `.gitignore`. |
| Codex podría hacer commits que mezclen tareas. | Bloque obligatorio: un commit por tarea (intermedios permitidos, último cierra ticket). |
| Codex podría hacer `--force` o `--no-verify`. | Prohibido explícitamente. |
| Audios reales aún no subidos físicamente. | T-013 queda en Pending hasta que el humano los suba; el resto del trabajo no se bloquea. |
| Licencias de repos previos sin verificar. | T-001 incluye verificación de licencia. |

---

## 5. Preguntas abiertas

- **¿Especies objetivo concretas (banda dominante, ritmo silábico)?**
  Necesario para `configs/species/*.yaml` en Fase 3. Si no se conocen aún, Codex deja un preset genérico `species/generic.yaml` con banda 1500–4000 Hz.

---

## 6. Qué puede modificar Codex

✅ Cualquier archivo bajo `src/`, `scripts/`, `tests/`, `configs/`, `notebooks/`.
✅ `REUSE_REPORT.md`, `EXPERIMENT_LOG.md`, `DATASET_NOTES.md`, `TASKS.md`.
✅ `HANDOFF_TO_CODEX.md` (siempre archivando la versión previa primero).
✅ `DECISIONS.md` añadiendo nuevas ADR (no editando las existentes).
✅ `pyproject.toml`, `.gitignore`.
✅ Git: `add` selectivo, `commit`, `push origin main`.

## 7. Qué NO puede modificar Codex

❌ `ARCHITECTURE.md` sin ADR previa aprobada.
❌ `PROJECT_CONTEXT.md` salvo correcciones tipográficas.
❌ `ROADMAP.md` (fases): sólo Claude/humano cambian la estructura; Codex sólo actualiza estados.
❌ `CODEX_PROMPTS.md`: sólo Claude.
❌ Schemas de manifest declarados en ARCHITECTURE.md §6 sin ADR.
❌ `data/raw/` (los audios los sube el humano).
❌ Historial git: nunca `--force`, nunca `--amend` sobre commits ya pusheados, nunca `--no-verify`.

---

## 8. Estado de fases

| Fase | Estado | Tareas activas |
|---|---|---|
| 0 | In Progress | T-001 |
| 1 | Planned | T-010, T-011, T-012, T-013 |
| 2–10 | Planned | — |

(Fuente autoritativa: `ROADMAP.md` y `TASKS.md`.)
