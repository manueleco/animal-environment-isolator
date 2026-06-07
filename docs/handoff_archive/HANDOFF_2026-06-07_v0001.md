# HANDOFF_TO_CODEX.md

> **Documento más importante del proyecto.** Canal principal de comunicación Claude → Codex.
>
> **Antes de cualquier acción, Codex lee este archivo entero.**
> Al cerrar una tarea, Codex archiva la versión anterior en `docs/handoff_archive/HANDOFF_<YYYY-MM-DD>_<short_hash>.md` y reescribe ésta.

**Última actualización:** 2026-06-07
**Actualizado por:** Claude (arquitecto)
**Versión del handoff:** v0001

---

## 1. Estado actual del proyecto

- **Fase activa:** Fase 0 — Auditoría de repos previos + setup de documentación.
- **Hito alcanzado:** Sistema de documentación Markdown completo creado (T-000 Done).
- **Hito inmediato siguiente:** Auditar los dos repos previos y poblar `REUSE_REPORT.md` (T-001).
- **Estructura de carpetas:** ya creada (`data/`, `src/frogiso/`, `scripts/`, `configs/`, `outputs/`, etc.) pero todavía vacía de código.

---

## 2. Última decisión importante

- **ADR-005** (ver `DECISIONS.md`): se adopta el sistema de documentación Markdown como interfaz Claude↔Codex↔Humano.
  Implicación operativa: cualquier cambio de arquitectura o dataset queda registrado en `DECISIONS.md` o `DATASET_NOTES.md` **antes** de implementarse.

---

## 3. Tarea siguiente para Codex

### **[T-001] Auditar repos previos → poblar REUSE_REPORT.md**

Prompt completo en [CODEX_PROMPTS.md §"PROMPT 1"](CODEX_PROMPTS.md). Resumen:

- Clonar en `.cache/external_repos/` (gitignored):
  - `https://github.com/manueleco/texture-dataset-curation`
  - `https://github.com/OriolFreixa/MirChordEstimationAugmentation`
- Por cada repo:
  - Listar archivos relevantes con rutas reales.
  - Clasificar en Reutilizable / Adaptar / Descartar con esfuerzo S/M/L.
  - Documentar riesgos de reciclar sin adaptar.
- Tabla resumen final con prioridades.

**Criterio de aceptación:**
- Cada item cita una ruta real del repo (verificable).
- ≥5 reutilizables, ≥5 a adaptar, ≥3 a descartar **por repo**.
- Sección "Inaccesibilidad" si algún repo no es alcanzable.

**Al cerrar T-001:**
1. Marcar Done en `TASKS.md` con fecha.
2. Reescribir este `HANDOFF_TO_CODEX.md` (archivar el actual).
3. Si surgió decisión técnica → ADR en `DECISIONS.md`.

---

## 4. Archivos relevantes para esta tarea

| Archivo | Por qué importa |
|---|---|
| `PROJECT_CONTEXT.md` | Contexto del proyecto y por qué se reciclan estos repos. |
| `ARCHITECTURE.md` | Hacia dónde tiene que encajar lo reciclado (módulos, manifests, convenciones). |
| `REUSE_REPORT.md` | Archivo destino — Codex lo edita. |
| `CODEX_PROMPTS.md` (Prompt 1) | Instrucciones operativas. |

---

## 5. Riesgos abiertos

| Riesgo | Mitigación inmediata |
|---|---|
| El repo `texture-dataset-curation` puede ser de un dominio (textures) demasiado alejado de bioacústica. | Documentar honestamente en REUSE_REPORT.md qué no se transfiere. |
| Puede haber funciones útiles bajo licencias incompatibles. | Codex verifica licencia de cada repo y la cita. Si es restrictiva → marcar "no reciclable por licencia". |
| Tentación de copiar código en lugar de extraer ideas/patrones. | El prompt prohíbe copiar al proyecto; sólo se citan rutas y se planifica adaptación. |

---

## 6. Preguntas abiertas (a resolver por humano cuando proceda)

- **¿Hay grabaciones reales ya disponibles para subir a `data/raw/`?** Bloquea Fases 2+. Sin audio, sólo podemos seguir hasta T-012 (estructura) en seco.
- **¿Especies objetivo concretas (banda dominante, ritmo silábico)?** Necesario para `configs/species/*.yaml`. Si no se conocen aún, dejar un preset genérico de banda 1500–4000 Hz.
- **¿Hay preferencia por `pandera` vs `pydantic` para validación de manifests (ADR-002b pendiente)?** Si no, Claude propondrá pandera (más natural para CSV tabular).

---

## 7. Qué puede modificar Codex en esta tarea

✅ `REUSE_REPORT.md` (es el output principal).
✅ `.cache/external_repos/` (carpeta local, gitignored).
✅ `.gitignore` para añadir `.cache/`.
✅ `TASKS.md` (marcar T-001 Done al terminar).
✅ `HANDOFF_TO_CODEX.md` (escribir nueva versión al cerrar, archivar la actual).
✅ `DECISIONS.md` si surge alguna decisión.

---

## 8. Qué NO puede modificar Codex en esta tarea

❌ `ARCHITECTURE.md` (cualquier cambio requiere ADR previa aprobada).
❌ `PROJECT_CONTEXT.md` (sólo Claude/humano).
❌ `ROADMAP.md` (sólo Claude/humano).
❌ `CODEX_PROMPTS.md` (sólo Claude).
❌ Código en `src/frogiso/` — esta tarea es de análisis, no de implementación.
❌ Schemas de manifest declarados en ARCHITECTURE.md §6.

---

## 9. Estado de las fases (snapshot)

| Fase | Estado |
|---|---|
| 0 | In Progress (T-000 ✅, T-001 ← siguiente) |
| 1–10 | Planned |

(Fuente autoritativa: `ROADMAP.md`.)

---

## 10. Protocolo de cierre de tarea (recordatorio)

Al terminar **cualquier** tarea, en este orden:

1. `TASKS.md` → estado a Done + fecha.
2. Archivar este handoff: `git mv HANDOFF_TO_CODEX.md docs/handoff_archive/HANDOFF_<fecha>_<hash>.md` (o `cp` si no estamos aún en git).
3. Reescribir `HANDOFF_TO_CODEX.md` con:
   - nuevo estado actual,
   - última decisión,
   - tarea siguiente,
   - qué puede/no puede tocar Codex en la siguiente.
4. Si hubo decisión técnica → `DECISIONS.md`.
5. Si hubo experimento → `EXPERIMENT_LOG.md`.
6. Si cambiaron datos → `DATASET_NOTES.md`.

**No saltarse este protocolo.** El proyecto está diseñado para sobrevivir meses sin contexto vivo.
