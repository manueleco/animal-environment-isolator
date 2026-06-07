# ARCHITECTURE.md

> **Documento normativo.** Si otro archivo entra en conflicto con éste, **este gana**. Cualquier cambio arquitectónico requiere una entrada en [DECISIONS.md](DECISIONS.md) antes de implementarse.

**Última actualización:** 2026-06-07
**Mantenedor:** Claude (arquitecto)

---

## 1. Visión arquitectónica

Pipeline **incremental y modular**, con cada fase produciendo artefactos que el siguiente paso consume vía manifests CSV. Ninguna fase asume estado en memoria de la anterior — todo es retomable desde manifests.

**Principios:**
1. DSP determinístico **antes** que ML.
2. Heurística auditable **antes** que modelo opaco.
3. Curación manual **antes** que volumen.
4. Augmentación etiquetada **antes** que augmentación oculta.
5. Configuración por YAML **antes** que parámetros en código.

---

## 2. Pipeline (diagrama textual)

```
                ┌──────────────────────────────┐
                │  data/raw/  (audios crudos)  │
                └──────────────┬───────────────┘
                               │  (1) Preprocesamiento
                               ▼   resample → mono → normalize
                ┌──────────────────────────────┐
                │       data/interim/          │
                └──────────────┬───────────────┘
                               │  (2) Exploración
                               ▼   STFT / mel / PCEN
                  outputs/figures/spectrograms/  + data/interim/spectrograms/*.npz
                               │
                               │  (3) Band-pass configurable por especie
                               ▼   configs/species/*.yaml
                  data/interim/bandpassed/
                               │
                               │  (4) Detección heurística por energía en banda
                               ▼   threshold = mediana + k·MAD
                  metadata/events.csv  +  outputs/figures/detections/
                               │
                               │  (5) Extracción de clips con padding
                               ▼
                  data/processed/clips/  +  metadata/clips.csv
                               │
                               │  (6) Denoising opcional con A/B
                               ▼
                  data/processed/clips_clean/  +  outputs/figures/ab/
                               │
                               │  (7) Curación manual (notebook ipywidgets)
                               ▼
                  metadata/curation.csv  →  data/curated/{positive,negative,ambiguous}/
                               │
                               │  (8) Split por recording_id (sin leakage)
                               ▼
                  data/splits/{train,val,test}_manifest.csv
                               │
                               │  (9) Augmentación realista — SÓLO train
                               ▼   reverb (IRs exteriores) + ambient mix + EQ + compresión
                  data/augmented/train/  +  metadata/augmentation_log.csv
                               │
                               │  (10) Baseline ML frog/no-frog
                               ▼   mel-spectrogram + CNN pequeño  /  sklearn + scikit-maad
                  models/<run_id>/  +  outputs/runs/<run_id>/
                               │
                               │  (11) Evaluación
                               ▼
                  reports/eval_<run_id>.md  +  outputs/eval/<run_id>/{FP,FN}/
                               │
                               │  (12) Avanzado opcional: embeddings, clustering, enhancement
                               ▼
                  reports/phase_9_report.md
```

Cada flecha es un script CLI en `scripts/` que llama a `src/frogiso/`.

---

## 3. Estructura del repositorio (normativa)

```
animal-environment-isolator/
├── README.md
├── PROJECT_CONTEXT.md
├── ARCHITECTURE.md          ← este archivo
├── ROADMAP.md
├── TASKS.md
├── DECISIONS.md
├── EXPERIMENT_LOG.md
├── DATASET_NOTES.md
├── EVALUATION_PLAN.md
├── CODEX_PROMPTS.md
├── HANDOFF_TO_CODEX.md
├── REUSE_REPORT.md
├── pyproject.toml
├── configs/
│   ├── default.yaml
│   ├── species/
│   │   └── *.yaml
│   └── augmentation.yaml
├── data/
│   ├── raw/             (gitignored)
│   ├── interim/         (gitignored, regenerable)
│   ├── processed/       (gitignored, regenerable)
│   ├── curated/         (versionado vía manifest, no binarios)
│   ├── augmented/       (gitignored)
│   ├── synthetic/       (gitignored, marcado is_synthetic=true)
│   ├── irs/             (con LICENSES.md)
│   └── ambient/         (con LICENSES.md)
├── metadata/            (CSV manifests, VERSIONADOS)
├── notebooks/
├── src/frogiso/
│   ├── io/        manifests, hashing, batch I/O
│   ├── dsp/       spectrograms, bandpass, PCEN
│   ├── detect/    energy detector, threshold adaptativo
│   ├── clips/     extracción, naming, export
│   ├── denoise/   noisereduce wrappers
│   ├── augment/   reverb, mix_noise, eq, comp
│   ├── datasets/  splits, manifests, loaders
│   ├── models/    cnn_small, sklearn_baseline
│   ├── eval/      métricas, FP/FN export
│   ├── web/       templates Jinja2 + renderers (Hallmark-styled, ADR-010)
│   └── utils/     logging, seed, config loader
├── scripts/             CLIs delgadas; no contienen lógica
├── outputs/
│   ├── figures/
│   ├── logs/
│   ├── runs/
│   └── web/             (gitignored, regenerable; landing + vistas por fase, tokens.css)
├── models/              checkpoints (pesados gitignored)
├── reports/
├── tests/
└── docs/
    ├── adr/             (decisiones largas referenciadas desde DECISIONS.md)
    └── handoff_archive/ (handoffs antiguos, ver §12)
```

---

## 4. Convenciones

### 4.1 Identificadores
- `recording_id` = `sha256(absolute_path)[:12]`. Estable mientras no se renombre el archivo.
- `event_id` = `<recording_id>__e<NNN>` con NNN zero-padded a 4 dígitos.
- `clip_id` = `<recording_id>__e<NNN>__<start_ms>_<end_ms>`.
- `run_id` = `<YYYYMMDD>_<HHMMSS>_<short_hash_config>`.

### 4.2 Naming de archivos
- WAV de clips: `<clip_id>.wav`.
- Spectrogramas: `<clip_id>.png` (legibles a 300 dpi) y `<recording_id>.npz` para arrays.
- Augmentados: `<clip_id>__aug<idx>.wav`.

### 4.3 Configuración
- **Todos** los parámetros relevantes viven en YAML bajo `configs/`.
- Nunca hardcodear sample_rate, n_fft, hop_length, bandas, thresholds.
- Cada script CLI acepta `--config path/to.yaml` y `--override key=value`.

### 4.4 Logging
- Logger central en `src/frogiso/utils/logging.py`.
- Salida a consola + `outputs/logs/<YYYY-MM-DD>.log` rotativo.
- Nivel por defecto INFO, configurable.

### 4.5 Seeds
- `seed` declarada en config raíz.
- `src/frogiso/utils/seed.py:set_global_seed(seed)` siembra numpy, random, torch.

### 4.6 Tests
- Sólo donde el output sea determinístico: hashing, splits, validación de manifests, design del filtro band-pass.
- No exigimos cobertura amplia — exigimos cobertura **donde el silencio de un bug sería caro** (leakage, naming colisión, configuración mal cargada).

---

## 5. Entradas y salidas por módulo

| Módulo | Input | Output |
|---|---|---|
| `dsp.spectrograms` | WAV + config | `.npz` + `.png` |
| `dsp.bandpass` | WAV + (lowcut, highcut, order) | WAV filtrado |
| `detect.energy_detector` | WAV (idealmente band-passed) + config | `events.csv` |
| `clips.extractor` | WAV original + `events.csv` + padding config | WAV clips + `clips.csv` |
| `denoise.spectral` | clip WAV + (opcional) noise profile | WAV clean + métricas pre/post |
| `augment.realistic` | clip curado + IRs + ambient + config | WAV aug + entrada en `augmentation_log.csv` |
| `datasets.splits` | `clips.csv` + `curation.csv` + ratios | 3 manifests de split |
| `models.cnn_small` | mel-spectrograms desde split | checkpoint + métricas |
| `eval.metrics` | predicciones + test manifest | `eval_<run_id>.md` + FP/FN export |
| `web.render` | manifests + figuras + métricas | HTML estático Hallmark-styled en `outputs/web/` |

---

## 6. Manifests CSV (schemas normativos)

### `metadata/recordings.csv`
`recording_id, path, sha256, duration_s, sample_rate, channels, source, license, recorded_at, notes`

### `metadata/events.csv`
`event_id, recording_id, start_s, end_s, duration_s, peak_db, mean_band_energy_db, band_lowcut, band_highcut, threshold_used, boundary_flag, detector_version`

### `metadata/clips.csv`
`clip_id, event_id, recording_id, path, start_s, end_s, duration_s, sample_rate, peak_dbfs, sha256, pad_pre_ms, pad_post_ms`

### `metadata/curation.csv`
`clip_id, label {positive,negative,ambiguous,discard}, confidence_1_5, notes, reviewer, timestamp`

### `metadata/denoise_log.csv`
`clip_id, method, params_json, snr_estimate_pre_db, snr_estimate_post_db, spectral_flatness_pre, spectral_flatness_post, output_path`

### `metadata/augmentation_log.csv`
`aug_id, source_clip_id, ir_used, ambient_used, snr_target_db, snr_measured_db, eq_params_json, comp_params_json, seed, output_path`

### `metadata/synthetic_manifest.csv`
`synth_id, type, params_json, duration_s, is_synthetic, source, output_path`

### `data/splits/{train,val,test}_manifest.csv`
`clip_id, label, recording_id, source {real,augmented}, split`

**Validación obligatoria** con pandera o pydantic en `src/frogiso/io/manifests.py`.

---

## 7. Reglas de splits (no negociables)

1. Split a nivel de `recording_id`. Nunca a nivel de clip.
2. Augmentación se aplica **sólo** sobre clips cuyo `recording_id` pertenezca a `train`.
3. Synthetic **nunca** entra a val/test.
4. Una assertion automática verifica intersección vacía de `recording_id` entre splits — falla el job si se rompe.

---

## 8. Dependencias

### Base
`librosa`, `soundfile`, `scipy`, `numpy`, `pandas`, `matplotlib`, `pyyaml`, `click`, `tqdm`, `noisereduce`, `scikit-maad`, `scikit-learn`.

### Validación
`pandera` o `pydantic` (decisión pendiente — ver ADR-002).

### Notebooks
`jupyter`, `ipywidgets`.

### ML (a partir de Fase 8)
`torch`, `lightning`, opcional `wandb`.

### Prohibidas sin ADR
- Cualquier framework de DL distinto de PyTorch.
- Cualquier base de datos (SQLite, etc.) en lugar de CSV.
- Cualquier dependencia con licencia incompatible con el uso académico.

---

## 9. Decisiones estructurales fijas

| ID | Decisión | Por qué |
|---|---|---|
| AS-01 | Pipeline incremental DSP → ML, no al revés. | Auditable y honesto; ML como mejora, no como caja negra inicial. |
| AS-02 | Manifests CSV como fuente de verdad. | Diffeables, inspeccionables, reproducibles. |
| AS-03 | Split por `recording_id` siempre. | Evitar leakage; estándar en bioacústica/MIR. |
| AS-04 | Augmentación etiquetada y logueada por clip. | Permite ablations y debugging de bias. |
| AS-05 | Synthetic separado del dataset real, flag obligatorio. | Evita contaminar entrenamiento de ML bioacústico. |
| AS-06 | Configs YAML, no parámetros en código. | Reproducibilidad. |
| AS-07 | CLIs en `scripts/`, lógica en `src/frogiso/`. | Separación responsabilidad. |
| AS-08 | Documentación Markdown versionada como interfaz Claude↔Codex. | Persistencia de contexto. |
| AS-09 | GUI = HTML estático Hallmark-styled, sin servidor. | Reproducibilidad + design coherente sin runtime extra (ADR-010). |

Cualquier alteración requiere ADR en [DECISIONS.md](DECISIONS.md).

---

## 10. Qué cuenta como "cambio arquitectónico" (requiere ADR)

- Cambiar formato de manifest.
- Introducir/eliminar una fase del pipeline.
- Cambiar la unidad de split (ej. de recording a clip — **prohibido**).
- Cambiar stack base (ej. de PyTorch a otro).
- Cambiar representación primaria (ej. de mel a CQT).
- Introducir DB en lugar de CSV.
- Cambiar el sistema de IDs.

## 11. Qué NO requiere ADR

- Añadir un script nuevo bajo `scripts/`.
- Añadir un módulo nuevo dentro de un paquete existente respetando interfaces.
- Tuneo de hiperparámetros documentado en `EXPERIMENT_LOG.md`.
- Añadir tests.
- Añadir notebooks de análisis.

---

## 12. Política de handoff

`HANDOFF_TO_CODEX.md` es el documento **vivo** en root. Antes de sobrescribirlo, archivar la versión anterior en `docs/handoff_archive/HANDOFF_<YYYY-MM-DD>_<short_hash>.md` para mantener historial sin saturar el archivo principal.
