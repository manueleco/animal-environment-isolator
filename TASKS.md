# TASKS.md

> Checklist operativa. **Codex actualiza el estado de cada tarea al cerrarla** y refleja el cambio también en `HANDOFF_TO_CODEX.md`.

**Estados:** Pending · In Progress · Blocked · Done
**Prioridades:** Critical · High · Medium · Low

---

## Fase 0 — Auditoría + setup

### [T-000]
**Estado:** Done
**Responsable:** Claude
**Prioridad:** Critical
**Dependencias:** —

Crear sistema de documentación Markdown base (este archivo + compañeros).

**Criterio de aceptación:**
- Todos los archivos listados en README.md existen y tienen contenido inicial.
- Estructura de carpetas creada.

---

### [T-001]
**Estado:** Pending
**Responsable:** Codex
**Prioridad:** Critical
**Dependencias:** T-000

Auditar `manueleco/texture-dataset-curation` y `OriolFreixa/MirChordEstimationAugmentation` y poblar [REUSE_REPORT.md](REUSE_REPORT.md) con análisis real (rutas concretas, no inventadas).

**Criterio de aceptación:**
- Cada item cita ruta real del repo y descripción del archivo/función.
- Tabla resumen al final con prioridades S/M/L.
- Sección explícita de "qué NO reciclar" por dominio bioacústico.

---

## Fase 1 — Estructura del repo

### [T-010]
**Estado:** Pending
**Responsable:** Codex
**Prioridad:** Critical
**Dependencias:** T-001

Crear `pyproject.toml` con deps base y estructura `src/frogiso/`.

**Criterio de aceptación:**
- `pip install -e .` funciona en entorno limpio.
- `python -c "import frogiso"` no falla.
- `configs/default.yaml` cargable vía `frogiso.utils.config.load_config`.
- `.gitignore` excluye `data/raw`, `data/interim`, `models/*.ckpt`, `outputs/runs`.

---

### [T-011]
**Estado:** Pending
**Responsable:** Codex
**Prioridad:** High
**Dependencias:** T-010

Implementar `src/frogiso/utils/{logging,config,seed}.py`.

**Criterio de aceptación:**
- Logger central escribe a consola + `outputs/logs/<YYYY-MM-DD>.log`.
- `load_config(path, overrides)` soporta `--override key=value`.
- `set_global_seed(seed)` siembra numpy, random y (si torch disponible) torch.

---

### [T-012]
**Estado:** Pending
**Responsable:** Codex
**Prioridad:** High
**Dependencias:** T-010

Implementar `src/frogiso/io/manifests.py` con schemas + validación.

**Criterio de aceptación:**
- Schemas declarados según §6 de `ARCHITECTURE.md`.
- `read_manifest(path, schema)` lanza error claro si inválido.
- Tests en `tests/test_manifests.py`.

---

### [T-013]
**Estado:** Pending
**Responsable:** Humano (subir audios) + Codex (script)
**Prioridad:** High
**Dependencias:** T-012

Implementar script de ingest `scripts/run_ingest.py` que escanea `data/raw/`, calcula sha256, extrae duración/SR/channels y puebla `metadata/recordings.csv`.

**Criterio de aceptación:**
- `metadata/recordings.csv` válido contra schema.
- Idempotente: re-ejecución no duplica filas.
- Detecta duplicados por sha256 y avisa.
- Skip de archivos corruptos con log.

---

## Fase 2 — Exploración

### [T-020]
**Estado:** Pending
**Responsable:** Codex
**Prioridad:** High
**Dependencias:** T-012

Implementar `src/frogiso/dsp/spectrograms.py` (STFT, mel, PCEN) + CLI `scripts/run_eda.py`.

**Criterio de aceptación:**
- Procesa ≥100 archivos sin OOM.
- PNG a 300 dpi con ejes correctos.
- NPZ determinístico (misma config → mismo hash de salida).

---

### [T-021]
**Estado:** Pending
**Responsable:** Codex + Humano (revisión)
**Prioridad:** Medium
**Dependencias:** T-020

Notebook `01_eda_spectrograms.ipynb` con galería + estadísticas por archivo.

**Criterio de aceptación:**
- Muestra distribución de duraciones, SR, energía por banda.
- Documenta ≥5 observaciones sobre las grabaciones reales.

---

## Fase 3 — Band-pass + detección

### [T-030]
**Estado:** Pending
**Responsable:** Codex
**Prioridad:** High
**Dependencias:** T-020

Implementar `src/frogiso/dsp/bandpass.py` + `scripts/run_bandpass.py`.

**Criterio de aceptación:**
- Filtro Butterworth con `filtfilt` opcional (zero-phase).
- Plot de respuesta del filtro guardado.
- Detección y warning de clipping.

---

### [T-031]
**Estado:** Pending
**Responsable:** Codex
**Prioridad:** Critical
**Dependencias:** T-030, T-012

Implementar `src/frogiso/detect/energy_detector.py` + `scripts/run_detect.py`.

**Criterio de aceptación:**
- Threshold adaptativo `mediana + k·MAD`.
- Genera `metadata/events.csv` válido contra schema.
- Plot waveform + eventos resaltados.
- Sobre grabación de prueba, ≥80% de eventos detectados validados manualmente.

---

## Fase 4 — Clips

### [T-040]
**Estado:** Pending
**Responsable:** Codex
**Prioridad:** High
**Dependencias:** T-031

Implementar `src/frogiso/clips/extractor.py` + `scripts/run_extract_clips.py`.

**Criterio de aceptación:**
- Naming colisión-free según §4.1 de `ARCHITECTURE.md`.
- sha256 verificado al exportar.
- `metadata/clips.csv` válido.
- Spectrogram por clip exportado.

---

## Fase 5 — Denoising

### [T-050]
**Estado:** Pending
**Responsable:** Codex
**Prioridad:** Medium
**Dependencias:** T-040

Implementar `src/frogiso/denoise/spectral.py` + `scripts/run_denoise.py`.

**Criterio de aceptación:**
- Wrapper noisereduce + opción Wiener.
- A/B plot por clip.
- `metadata/denoise_log.csv` poblado.
- HTML A/B player generado.

---

### [T-051]
**Estado:** Pending
**Responsable:** Humano
**Prioridad:** Medium
**Dependencias:** T-050

Revisar 10 pares A/B y documentar en `EXPERIMENT_LOG.md`.

**Criterio de aceptación:** Entrada EXP-005 (o equivalente) con conclusión clara: ¿denoising activado por defecto sí/no?

---

## Fase 6 — Curación

### [T-060]
**Estado:** Pending
**Responsable:** Codex
**Prioridad:** High
**Dependencias:** T-040 (T-050 opcional)

Notebook `05_manual_curation.ipynb` con ipywidgets.

**Criterio de aceptación:**
- Audio player + waveform + spectrogram + metadata.
- Etiquetado: positive / negative / ambiguous / discard.
- Save incremental a `metadata/curation.csv`.

---

### [T-061]
**Estado:** Pending
**Responsable:** Humano
**Prioridad:** Critical
**Dependencias:** T-060

Curar ≥200 clips manualmente.

**Criterio de aceptación:** `metadata/curation.csv` con ≥200 filas etiquetadas y distribución documentada en `DATASET_NOTES.md`.

---

## Fase 7 — Augmentación

### [T-070]
**Estado:** Pending
**Responsable:** Humano
**Prioridad:** High
**Dependencias:** —

Recolectar IRs de exteriores y ambient noise. Documentar licencias en `data/irs/LICENSES.md` y `data/ambient/LICENSES.md`.

**Criterio de aceptación:** ≥5 IRs de exteriores + ≥10 clips de ambient diversos con licencia explícita.

---

### [T-071]
**Estado:** Pending
**Responsable:** Codex
**Prioridad:** High
**Dependencias:** T-061, T-070

Implementar `src/frogiso/augment/` (reverb, mix_noise, eq, compression) + `scripts/run_augment.py`.

**Criterio de aceptación:**
- Reverb no alarga clip más del margen configurable.
- SNR target medido ±1 dB.
- `metadata/augmentation_log.csv` con todos los parámetros.
- Aplicado SÓLO a recordings de train.

---

### [T-072]
**Estado:** Pending
**Responsable:** Codex
**Prioridad:** Low
**Dependencias:** T-010

Implementar generación de ejemplos sintéticos (`src/frogiso/synthetic/`) etiquetados `is_synthetic=true`.

**Criterio de aceptación:**
- Manifest separado.
- Loader excluye synthetic por defecto.
- Advertencia en docstring del módulo.

---

## Fase 8 — Baseline ML

### [T-080]
**Estado:** Pending
**Responsable:** Codex
**Prioridad:** Critical
**Dependencias:** T-061

Implementar `src/frogiso/datasets/splits.py` + `scripts/run_split.py`.

**Criterio de aceptación:**
- Split por `recording_id`.
- Assertion automática de intersección vacía.
- Ratios respetados ±2%.
- Reportar `reports/split_stats.md`.

---

### [T-081]
**Estado:** Pending
**Responsable:** Codex
**Prioridad:** High
**Dependencias:** T-080, T-071

Implementar baseline sklearn (`src/frogiso/models/sklearn_baseline.py`).

**Criterio de aceptación:**
- Features: MFCC stats + spectral centroid + rolloff + ZCR + scikit-maad indices.
- Entrenamiento determinístico.
- Métricas en `outputs/runs/<run_id>/`.

---

### [T-082]
**Estado:** Pending
**Responsable:** Codex
**Prioridad:** High
**Dependencias:** T-080, T-071

Implementar CNN pequeño (`src/frogiso/models/cnn_small.py`) con PyTorch Lightning.

**Criterio de aceptación:**
- 3 bloques conv + GAP + linear.
- Augmentación sólo en train.
- Checkpoint guardado.
- wandb opcional, fallback CSV+matplotlib.

---

### [T-083]
**Estado:** Pending
**Responsable:** Codex
**Prioridad:** Critical
**Dependencias:** T-081 o T-082

Implementar evaluación (`src/frogiso/eval/metrics.py` + `scripts/run_eval.py`).

**Criterio de aceptación:**
- precision/recall/F1, ROC-AUC, PR-AUC, confusion matrix.
- Export FP/FN con audio + spectrogram + HTML index.
- `reports/eval_<run_id>.md` generado.

---

## Fase 9 — Avanzado (opcional)

### [T-090]
**Estado:** Pending
**Responsable:** Codex
**Prioridad:** Low
**Dependencias:** T-083

Embeddings pre-entrenados + clustering UMAP/HDBSCAN.

**Criterio de aceptación:** Informe técnico con comparación frente a baseline.

---

## Fase 10 — Documentación + reporte

### [T-100]
**Estado:** Pending
**Responsable:** Claude + Humano
**Prioridad:** High
**Dependencias:** T-083

README completo + `reports/final_report.md` paper-style.

**Criterio de aceptación:**
- Reproducible siguiendo sólo README.
- Sección explícita sobre limitaciones y datos sintéticos.
- Métricas reales (no placeholders).
