# HANDOFF_TO_CODEX.md

> **Canal principal Claude → Codex.** Leer ANTES de cualquier acción.
> Al cerrar la tarea actual, archivar esta versión y reescribir.

**Última actualización:** 2026-06-07
**Actualizado por:** Codex
**Versión del handoff:** v0003
**Archivo anterior:** `docs/handoff_archive/HANDOFF_2026-06-07_v0002.md`

---

## 1. Estado actual del proyecto

- **Fase activa:** Fase 1 — estructura instalable del repo.
- **Hitos alcanzados:**
  - T-000 ✅ Sistema de documentación creado.
  - T-001 ✅ `REUSE_REPORT.md` poblado con auditoría real de:
    - `manueleco/texture-dataset-curation` (`d42655b`).
    - `OriolFreixa/MirChordEstimationAugmentation` (`64df935`, partial clone por tamaño/incidencia del checkout completo).
  - Fase 0 marcada como Done en `ROADMAP.md`.
- **Última decisión técnica:** No se añadió ADR nueva. La auditoría confirma reuso conceptual, no copia de código/assets, por ausencia de LICENSE en ambos repos.
- **Git:** T-001 queda cerrado por el commit `docs(T-001): populate REUSE_REPORT with real repo audit` y push a `origin main`.

---

## 2. Tarea siguiente (orden estricto)

### **[T-010 + T-011 + T-012] Estructura instalable del proyecto**
Prompt: [CODEX_PROMPTS.md §"PROMPT 2"](CODEX_PROMPTS.md).

Implementar:
- `pyproject.toml` con deps base permitidas por `ARCHITECTURE.md §8`.
- Estructura `src/frogiso/`.
- `src/frogiso/utils/{logging,config,seed}.py`.
- `src/frogiso/io/{__init__,manifests,hashing}.py`.
- `configs/default.yaml`.
- `.gitignore` si falta algo normativo.
- Tests de manifests/hashing.

**Reciclado recomendado desde T-001:**
- `R-04` y `R-05` de `REUSE_REPORT.md`: patrón batch manifest del repo A.
- `R-10` y `R-12`: parámetros de preprocesado/config del repo B, traducidos a YAML.
- No copiar código literal de los repos auditados.

---

## 3. Archivos relevantes

| Archivo | Para qué |
|---|---|
| `PROJECT_CONTEXT.md` | Contexto y alcance. |
| `ARCHITECTURE.md` | **Normativo.** Estructura, schemas, dependencias y reglas de splits. |
| `ROADMAP.md` | Fases y estado actual. |
| `TASKS.md` | Tickets y criterios de aceptación. |
| `CODEX_PROMPTS.md` | Usar §"PROMPT 2" para T-010/T-011/T-012. |
| `DECISIONS.md` | ADR-002b (`pandera`), ADR-007 (PyTorch/Lightning solo Fase 8), ADR-008 (git). |
| `REUSE_REPORT.md` | IDs R-01..R-18; fuente de patrones reutilizables/adaptables/descartados. |
| `DATASET_NOTES.md` | Reglas de synthetic y advertencias de datos/licencias. |

---

## 4. Riesgos abiertos

| Riesgo | Mitigación |
|---|---|
| Copiar código de repos sin licencia detectable. | Reimplementar conceptos; no copiar código/assets. |
| Arrastrar supuestos musicales de repo B (CQT, chroma, acordes, JAMS). | Usar mel/PCEN/STFT y manifests CSV de `ARCHITECTURE.md`; descartar componentes musicales. |
| Introducir deps pesadas antes de tiempo (`torch`, `lightning`, `wandb`). | Respetar `ARCHITECTURE.md §8`: ML solo a partir de Fase 8. |
| Romper la fuente de verdad CSV con `.pt` o notebooks. | Manifests CSV versionados, artefactos pesados gitignored. |
| Fase 1 puede tentar a crear DSP/detectores aún. | No crear módulos DSP/ML en PROMPT 2; solo estructura, utils, IO y tests. |

---

## 5. Preguntas abiertas

- Especies objetivo concretas y bandas dominantes siguen pendientes. Para Fase 3, si no hay datos, usar preset genérico `1500-4000 Hz` como indicaba v0002.
- Licencias de futuros IRs/ambients deben documentarse antes de uso en `data/irs/LICENSES.md` y `data/ambient/LICENSES.md`.

---

## 6. Qué puede modificar Codex en la siguiente tarea

✅ `pyproject.toml`, `.gitignore`, `configs/`.
✅ `src/frogiso/` solo para estructura Fase 1 (`utils`, `io`, `__init__`).
✅ `scripts/` si hace falta CLI mínima de validación/config, pero no DSP.
✅ `tests/`.
✅ `TASKS.md`, `HANDOFF_TO_CODEX.md`, `ROADMAP.md` estados al cerrar.
✅ `DECISIONS.md` solo si surge una decisión nueva no cubierta por ADR vigente.
✅ Git: `add` selectivo, commit y `git push origin main`.

## 7. Qué NO puede modificar Codex en la siguiente tarea

❌ `ARCHITECTURE.md` sin ADR previa aprobada.
❌ `PROJECT_CONTEXT.md` salvo erratas.
❌ `CODEX_PROMPTS.md`.
❌ Schemas de manifests distintos a `ARCHITECTURE.md §6`.
❌ `data/raw/` y datos reales.
❌ Copiar código, IRs, audio, checkpoints, `.pt` o notebooks de `.cache/external_repos/`.
❌ Añadir `torch`, `lightning`, `wandb` o frameworks ML en Fase 1.
❌ `src/frogiso/dsp/`, `detect/`, `models/` salvo crear carpetas vacías si el prompt/arquitectura lo exige.

---

## 8. Estado de fases

| Fase | Estado | Tareas activas |
|---|---|---|
| 0 | Done | — |
| 1 | Planned | T-010, T-011, T-012, T-013 |
| 2–10 | Planned | — |

(Fuente autoritativa: `ARCHITECTURE.md`, `ROADMAP.md` y `TASKS.md`.)
