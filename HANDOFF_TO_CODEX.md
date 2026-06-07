# HANDOFF_TO_CODEX.md

> **Canal principal Claude → Codex.** Leer ANTES de cualquier acción.
> Al cerrar la tarea actual, archivar esta versión y reescribir.

**Última actualización:** 2026-06-07
**Actualizado por:** Codex
**Versión del handoff:** v0004
**Archivo anterior:** `docs/handoff_archive/HANDOFF_2026-06-07_v0003.md`

---

## 1. Estado actual del proyecto

- **Fase activa:** Fase 2 — exploración y visualización.
- **Hitos alcanzados:**
  - T-000 ✅ Sistema de documentación creado.
  - T-001 ✅ `REUSE_REPORT.md` poblado con auditoría real de:
    - `manueleco/texture-dataset-curation` (`d42655b`).
    - `OriolFreixa/MirChordEstimationAugmentation` (`64df935`, partial clone por tamaño/incidencia del checkout completo).
  - T-010 ✅ Repo instalable con `pyproject.toml` y `src/frogiso/__init__.py` (`0.1.0`).
  - T-011 ✅ Utils base: `logging`, `config`, `seed`.
  - T-012 ✅ IO base: hashing y schemas `pandera` para los 8 CSV de `ARCHITECTURE.md §6`.
  - Fases 0 y 1 marcadas como Done en `ROADMAP.md`.
- **Última decisión técnica:** Se mantiene ADR-002b (`pandera`) y ADR-009 (reuso conceptual sin copiar código/assets). `ARCHITECTURE.md §6` declara 8 manifests CSV; se implementaron los 8 aunque el prompt resumido indicara 7.
- **Verificación:** `pip install -e .`, `python -c "import frogiso; print(frogiso.__version__)"`, `load_config("configs/default.yaml")` con override y `pytest tests/` OK (`24 passed`).
- **Git:** T-010/T-011/T-012 deben quedar cerradas por el commit `feat(T-010..T-012): bootstrap installable package with utils and pandera schemas` y push a `origin main`.

---

## 2. Tarea siguiente (orden estricto)

### **[T-020 + T-021] Espectrogramas batch + notebook EDA**
Prompt: [CODEX_PROMPTS.md §"PROMPT 3"](CODEX_PROMPTS.md).

Implementar:
- `src/frogiso/dsp/spectrograms.py`: `compute_stft`, `compute_mel`, `compute_pcen`, `plot_spectrogram`, `batch_process`.
- `scripts/run_eda.py` CLI: `--input-dir`, `--output-dir`, `--config`, `--format {png,npz,both}`.
- `outputs/figures/spectrograms/<recording_id>.png` (300 dpi, ejes correctos).
- `data/interim/spectrograms/<recording_id>.npz`.
- `notebooks/01_eda_spectrograms.ipynb` con galería + distribuciones de duración/SR/energía.

**Reciclado recomendado desde T-001/T-012:**
- Usar `R-04` y `R-05` como inspiración conceptual para batch I/O y manifests.
- Usar `frogiso.io.hashing.recording_id_from_path` para nombres determinísticos.
- Usar `frogiso.utils.config.load_config` y `configs/default.yaml`.
- No copiar código literal de repos auditados.

---

## 3. Archivos relevantes

| Archivo | Para qué |
|---|---|
| `PROJECT_CONTEXT.md` | Contexto y alcance. |
| `ARCHITECTURE.md` | **Normativo.** Estructura, schemas, dependencias y reglas de splits. |
| `ROADMAP.md` | Fases y estado actual. |
| `TASKS.md` | Tickets y criterios de aceptación. |
| `CODEX_PROMPTS.md` | Usar §"PROMPT 3" para T-020/T-021. |
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
| Audios largos (>10 min) pueden agotar memoria si se cargan de golpe. | Diseñar batch/chunking o carga cuidadosa; validar con varios archivos. |
| Archivos corruptos, estéreo o demasiado cortos pueden romper el batch. | Log warning, continuar; downmix con aviso; skip si `< n_fft`. |
| Generar outputs no determinísticos o no trazables. | Usar config + hashing estable y registrar avisos. |

---

## 5. Preguntas abiertas

- Especies objetivo concretas y bandas dominantes siguen pendientes. Para Fase 3, si no hay datos, usar preset genérico `1500-4000 Hz`.
- T-020/T-021 necesitan audios en `data/raw/` o un directorio de entrada externo indicado por el humano.
- Licencias de futuros IRs/ambients deben documentarse antes de uso en `data/irs/LICENSES.md` y `data/ambient/LICENSES.md`.

---

## 6. Qué puede modificar Codex en la siguiente tarea

✅ `src/frogiso/dsp/` para espectrogramas.
✅ `scripts/run_eda.py`.
✅ `notebooks/01_eda_spectrograms.ipynb`.
✅ `outputs/figures/spectrograms/` y `data/interim/spectrograms/` para artefactos generados.
✅ `tests/` para pruebas nuevas de espectrogramas/batch si aplica.
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
❌ Añadir `torch`, `lightning`, `wandb` o frameworks ML antes de Fase 8.
❌ Detectar eventos o escribir `metadata/events.csv` en PROMPT 3.
❌ `src/frogiso/detect/`, `src/frogiso/models/`, checkpoints o entrenamiento ML.

---

## 8. Estado de fases

| Fase | Estado | Tareas activas |
|---|---|---|
| 0 | Done | — |
| 1 | Done | T-013 pendiente para ingest real |
| 2 | Planned | T-020, T-021 |
| 3–10 | Planned | — |

(Fuente autoritativa: `ARCHITECTURE.md`, `ROADMAP.md` y `TASKS.md`.)
