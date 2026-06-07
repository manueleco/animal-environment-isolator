# ROADMAP.md

> Estados permitidos: **Planned**, **In Progress**, **Done**, **Blocked**.

**Última actualización:** 2026-06-07
**Mantenedor:** Claude (arquitecto). Codex actualiza estado al cerrar tarea.

---

## MVP

**Definición de MVP** (mínimo entregable defendible):
Fases 0 → 6 completas + un baseline DSP (sin ML) capaz de detectar eventos y exportar clips revisados manualmente, con manifests y A/B de denoising. Esto ya es defendible como proyecto.

**MVP académico ampliado** (recomendado entregar): MVP + Fase 7 (augmentación) + Fase 8 (baseline ML) + Fase 10 (reporte).

---

## Fases

### Fase 0 — Auditoría de repos previos + setup de documentación
**Estado:** Done
**Depende de:** —
**Entregables:**
- Sistema de docs Markdown (este archivo y compañeros). ✅
- [REUSE_REPORT.md](REUSE_REPORT.md) con análisis real de los dos repos.

**Criterio de salida:** REUSE_REPORT.md completo con rutas reales citadas.

---

### Fase 1 — Estructura del nuevo repo
**Estado:** Planned
**Depende de:** Fase 0.
**Entregables:**
- Árbol de carpetas (§3 de [ARCHITECTURE.md](ARCHITECTURE.md)).
- `pyproject.toml` con deps base.
- `src/frogiso/utils/{logging,config,seed}.py`.
- `configs/default.yaml`.
- `.gitignore`.

**Criterio de salida:** `pip install -e .` en clean env + `import frogiso` OK.

---

### Fase 2 — Exploración y visualización (espectrogramas)
**Estado:** Planned
**Depende de:** Fase 1.
**Entregables:**
- `src/frogiso/dsp/spectrograms.py` (STFT, mel, PCEN).
- `scripts/run_eda.py`.
- Notebook `01_eda_spectrograms.ipynb`.
- Galería en `outputs/figures/spectrograms/`.

**Criterio de salida:** ≥1 grabación real procesada con mel + PCEN comparados visualmente.

---

### Fase 3 — Filtrado band-pass + detección heurística
**Estado:** Planned
**Depende de:** Fase 2.
**Entregables:**
- `src/frogiso/dsp/bandpass.py`.
- `src/frogiso/detect/energy_detector.py`.
- `scripts/run_bandpass.py`, `scripts/run_detect.py`.
- Configs por especie en `configs/species/`.
- `metadata/events.csv` poblado.

**Criterio de salida:** Sobre una grabación de prueba, eventos detectados coinciden visualmente con el espectrograma (validación manual).

---

### Fase 4 — Extracción automática de clips
**Estado:** Planned
**Depende de:** Fase 3.
**Entregables:**
- `src/frogiso/clips/extractor.py`.
- `scripts/run_extract_clips.py`.
- `data/processed/clips/` + `metadata/clips.csv`.

**Criterio de salida:** Clips WAV con padding correcto, naming colisión-free, sha256 verificable.

---

### Fase 5 — Denoising + comparación A/B
**Estado:** Planned
**Depende de:** Fase 4.
**Entregables:**
- `src/frogiso/denoise/spectral.py`.
- `scripts/run_denoise.py`.
- `data/processed/clips_clean/`.
- HTML A/B player en `outputs/ab/`.

**Criterio de salida:** Comparación A/B documentada en `EXPERIMENT_LOG.md` con al menos 10 clips.

---

### Fase 6 — Curación manual / semi-automática
**Estado:** Planned
**Depende de:** Fase 5.
**Entregables:**
- Notebook `05_manual_curation.ipynb` con ipywidgets.
- `metadata/curation.csv`.
- `data/curated/{positive,negative,ambiguous}/` (vía manifest, no copia física obligatoria).

**Criterio de salida:** ≥200 clips etiquetados manualmente (positive + negative razonable).

**[Aquí está el MVP mínimo.]**

---

### Fase 7 — Augmentación realista
**Estado:** Planned
**Depende de:** Fase 6.
**Entregables:**
- `src/frogiso/augment/{reverb,mix_noise,eq,compression}.py`.
- `scripts/run_augment.py`.
- `data/augmented/train/` + `metadata/augmentation_log.csv`.
- `data/irs/LICENSES.md` y `data/ambient/LICENSES.md` poblados.

**Criterio de salida:** Augmentación aplicada SÓLO a train, log completo, validación auditiva de N=10 pares.

---

### Fase 8 — Baseline ML frog/no-frog
**Estado:** Planned
**Depende de:** Fases 6 y 7.
**Entregables:**
- `src/frogiso/datasets/splits.py` (split por recording_id).
- `src/frogiso/models/{cnn_small,sklearn_baseline}.py`.
- `scripts/run_split.py`, `scripts/run_train.py`.
- Checkpoint en `models/<run_id>/`.
- Métricas en `outputs/runs/<run_id>/`.

**Criterio de salida:** F1 ≥ baseline a definir en `EVALUATION_PLAN.md`; sin leakage verificable.

---

### Fase 9 — Avanzado (opcional)
**Estado:** Planned
**Depende de:** Fase 8.
**Entregables candidatos:**
- Embeddings de modelo pre-entrenado (BirdNET / Perch) + clustering (UMAP + HDBSCAN).
- Enhancement con masking espectral guiado por detección.
- Comparación frente a baseline.

**Criterio de salida:** Informe técnico con ganancia (o no) sobre baseline.

---

### Fase 10 — Documentación + reporte académico
**Estado:** Planned
**Depende de:** Fase 8 (mínimo).
**Entregables:**
- README completo y reproducible.
- `reports/final_report.md` estilo paper.
- Sección explícita sobre limitaciones y datos sintéticos.

**Criterio de salida:** Un tercero clona el repo y reproduce las métricas con sólo el README.

---

## Tabla resumen

| Fase | Estado | Owner principal | Bloqueada por |
|---|---|---|---|
| 0  | Done        | Claude → Codex (REUSE_REPORT) | — |
| 1  | Planned     | Codex                          | 0 |
| 2  | Planned     | Codex                          | 1 |
| 3  | Planned     | Codex                          | 2 |
| 4  | Planned     | Codex                          | 3 |
| 5  | Planned     | Codex                          | 4 |
| 6  | Planned     | Humano + Codex (notebook)      | 5 |
| 7  | Planned     | Codex                          | 6 |
| 8  | Planned     | Codex                          | 6, 7 |
| 9  | Planned     | Codex (opcional)               | 8 |
| 10 | Planned     | Claude + Humano                | 8 |
