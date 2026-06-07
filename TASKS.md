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
**Estado:** Done
**Responsable:** Codex
**Prioridad:** Critical
**Dependencias:** T-000

Auditar `manueleco/texture-dataset-curation` y `OriolFreixa/MirChordEstimationAugmentation` y poblar [REUSE_REPORT.md](REUSE_REPORT.md) con análisis real (rutas concretas, no inventadas).

**Criterio de aceptación:**
- Cada item cita ruta real del repo y descripción del archivo/función.
- Tabla resumen al final con prioridades S/M/L.
- Sección explícita de "qué NO reciclar" por dominio bioacústico.

**Cierre:** 2026-06-07 — `REUSE_REPORT.md` poblado con auditoría real de ambos repos; commit `docs(T-001): populate REUSE_REPORT with real repo audit`.

---

## Fase 1 — Estructura del repo

### [T-010]
**Estado:** Done
**Responsable:** Codex
**Prioridad:** Critical
**Dependencias:** T-001

Crear `pyproject.toml` con deps base y estructura `src/frogiso/`.

**Criterio de aceptación:**
- `pip install -e .` funciona en entorno limpio.
- `python -c "import frogiso"` no falla.
- `configs/default.yaml` cargable vía `frogiso.utils.config.load_config`.
- `.gitignore` excluye `data/raw`, `data/interim`, `models/*.ckpt`, `outputs/runs`.

**Cierre:** 2026-06-07 — Paquete instalable `animal-environment-isolator` creado con `pyproject.toml`, `src/frogiso/__init__.py` (`0.1.0`) y configs base; `pip install -e .` OK.

---

### [T-011]
**Estado:** Done
**Responsable:** Codex
**Prioridad:** High
**Dependencias:** T-010

Implementar `src/frogiso/utils/{logging,config,seed}.py`.

**Criterio de aceptación:**
- Logger central escribe a consola + `outputs/logs/<YYYY-MM-DD>.log`.
- `load_config(path, overrides)` soporta `--override key=value`.
- `set_global_seed(seed)` siembra numpy, random y (si torch disponible) torch.

**Cierre:** 2026-06-07 — Implementados `frogiso.utils.logging`, `frogiso.utils.config` y `frogiso.utils.seed`; `load_config("configs/default.yaml")` devuelve dict y soporta overrides CLI-style.

---

### [T-012]
**Estado:** Done
**Responsable:** Codex
**Prioridad:** High
**Dependencias:** T-010

Implementar `src/frogiso/io/manifests.py` con schemas + validación.

**Criterio de aceptación:**
- Schemas declarados según §6 de `ARCHITECTURE.md`.
- `read_manifest(path, schema)` lanza error claro si inválido.
- Tests en `tests/test_manifests.py`.

**Cierre:** 2026-06-07 — Implementados schemas `pandera` estrictos para los 8 CSV de `ARCHITECTURE.md §6`, hashing y tests; `pytest tests/` OK (`24 passed`).

---

### [T-014]
**Estado:** Done
**Responsable:** Codex
**Prioridad:** High
**Dependencias:** T-012

Crear módulo `src/frogiso/web/` con shell Hallmark-styled y landing del proyecto (ADR-010).

**Criterio de aceptación:**
- `outputs/web/index.html` (landing) generado vía hallmark default + Jinja2.
- `outputs/web/tokens.css` con design tokens locked (color + typography + spacing).
- Layout base `web/templates/base.html.j2` con navegación a vistas futuras.
- `scripts/run_web.py --view {landing,all}` regenera el frontend.
- Vista responsive verificada a 320/375/414/768 px.
- Hallmark pre-emit critique stamp presente en cada HTML (`/* Hallmark · pre-emit critique: P? H? E? S? R? V? */`).

**Cierre:** 2026-06-07 — Web shell estático con Jinja2 y landing Hallmark-styled generado en `outputs/web/`; `python scripts/run_web.py --view landing`, `pytest tests/test_web.py` y verificación CDP responsive 320/375/414/768 OK.

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

### [T-022]
**Estado:** Pending
**Responsable:** Codex
**Prioridad:** Medium
**Dependencias:** T-020, T-014

Publicar vista `outputs/web/eda_gallery.html` Hallmark-styled con spectrogramas + estadísticas (lee `metadata/recordings.csv` + figuras).

**Criterio de aceptación:**
- Vista listada en la navegación de la landing.
- Reusa `tokens.css` de T-014 (sin nuevos tokens improvisados).
- Filtros por SR / duración / canales en cliente (JS vanilla, sin frameworks).
- Mobile-responsive verificado en 320/375/414/768 px.

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

### [T-052]
**Estado:** Pending
**Responsable:** Codex
**Prioridad:** Medium
**Dependencias:** T-050, T-014

Publicar `outputs/web/ab_player.html` Hallmark-styled: pares original vs clean con `<audio>` embebido + spectrogramas + métricas SNR/flatness.

**Criterio de aceptación:**
- Lista paginada (≥ 50 clips sin lag).
- Hotkeys teclado: ←/→ navegar, space play/pause.
- Sin chrome fake (sin barras de browser dibujadas).
- Mobile-responsive.

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

### [T-062]
**Estado:** Pending
**Responsable:** Codex
**Prioridad:** Low
**Dependencias:** T-060, T-014

Publicar `outputs/web/curation_browser.html` Hallmark-styled (READ-ONLY): explorador de clips ya curados con filtros por label/confidence/recording. La edición sigue en el notebook (T-060).

**Criterio de aceptación:**
- Lee `metadata/curation.csv`.
- Filtros: label, confidence ≥, recording, duración.
- NO permite editar (sólo navegación + audio + spectrogram).
- Stats agregadas (counts por label, distribución de confidence).

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

### [T-084]
**Estado:** Pending
**Responsable:** Codex
**Prioridad:** High
**Dependencias:** T-083, T-014

Publicar `outputs/web/eval_<run_id>.html` Hallmark-styled: tabla de métricas + confusion matrix + galerías de FP/FN con audio embebido + métricas estratificadas.

**Criterio de aceptación:**
- Confusion matrix visible y legible en móvil.
- N=20 FP y N=20 FN por confidence, no a mano.
- Comparación de runs si hay varios.
- Sin chrome fake; mobile-responsive.

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

---

### [T-101]
**Estado:** Pending
**Responsable:** Codex
**Prioridad:** High
**Dependencias:** T-100, T-014, T-084

Publicar landing final + reporte académico HTML Hallmark-styled.

Sub-pasos:
1. Ejecutar `hallmark audit outputs/web/index.html` y aplicar el punch list.
2. Publicar `outputs/web/report.html` desde `reports/final_report.md` (vía Jinja2 + sección "Ethical considerations on synthetic data" obligatoria).
3. Actualizar landing con enlaces a todas las vistas (eda, ab, curation, eval).

**Criterio de aceptación:**
- Pre-emit critique ≥4 en P/H/E/S/R/V.
- Métricas reales del último run citadas con `<data>` semánticos.
- Mobile-responsive 320/375/414/768 px verificado.
- Cero métricas inventadas (gate 46 de Hallmark).
