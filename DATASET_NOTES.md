# DATASET_NOTES.md

> Documentación viva de los datos. **Cada vez que entren nuevos audios, IRs o ambient noise, actualizar este archivo y el manifest correspondiente.**

**Última actualización:** 2026-06-07

---

## 1. Fuentes de datos

### 1.1 Grabaciones de campo (datos reales — `data/raw/`)
- **Origen:** grabaciones propias del investigador (pendiente de añadir físicamente).
- **Formato esperado:** WAV/FLAC, mono o estéreo, SR ≥22050 Hz.
- **Metadatos mínimos por grabación** (en `metadata/recordings.csv`):
  - `recording_id`, `path`, `sha256`, `duration_s`, `sample_rate`, `channels`, `recorded_at`, `location` (opcional, anonimizable), `device`, `notes`.

### 1.2 Datasets externos (referencia / consulta)
- **Xeno-canto** (https://xeno-canto.org) — uso bajo licencia CC, descarga manual o vía API con auditoría previa de licencias. **No** se descargan masivamente.
- **iNaturalist sounds** — mismo régimen.
- Cualquier dataset externo entra con su propio manifest separado: `metadata/external_<source>.csv`.

### 1.3 IRs (impulse responses) — `data/irs/`
- Necesarios para Fase 7 (reverb).
- **Solo IRs de exteriores**: bosques, vegetación densa, espacios abiertos al aire libre.
- Fuente preferida: Freesound (con filtro de licencia CC).
- Archivo obligatorio: `data/irs/LICENSES.md` con tabla `nombre | url | autor | licencia | notas`.

### 1.4 Ambient noise — `data/ambient/`
- Fondos para mezcla en augmentación: viento, agua corriente, lluvia, insectos sostenidos, ambiente nocturno.
- **Auditar manualmente** cada clip antes de añadirlo — no puede contener cantos de rana (label noise grave).
- Fuente preferida: Freesound (CC).
- Archivo obligatorio: `data/ambient/LICENSES.md`.

---

## 2. Datos reales vs sintéticos vs augmentados

| Categoría | Carpeta | Manifest | Flag | Permitido en train | Permitido en val/test |
|---|---|---|---|---|---|
| Real crudo | `data/raw/` | `recordings.csv` | — | sí (vía clips) | sí (vía clips) |
| Clip extraído | `data/processed/clips/` | `clips.csv` | — | sí | sí |
| Clip denoised | `data/processed/clips_clean/` | `denoise_log.csv` | — | sí (si se decide) | sí (si se decide) |
| Curado | `data/curated/` | `curation.csv` | `label` | sí | sí |
| Augmentado | `data/augmented/train/` | `augmentation_log.csv` | `source=augmented` | **sí, sólo train** | **no** |
| Sintético | `data/synthetic/` | `synthetic_manifest.csv` | `is_synthetic=true` | **opcional, marcado** | **no, nunca** |

---

## 3. Versionado

- **Los binarios de audio NO se versionan en git** (gitignored).
- **Los manifests CSV SÍ se versionan**. Son la fuente de verdad reproducible.
- Cada release/snapshot importante etiqueta el repo y registra:
  - hashes sha256 de los recordings usados,
  - hashes de las configs aplicadas,
  - en `reports/release_<vYYYYMMDD>.md`.

---

## 4. Riesgos de leakage

| Riesgo | Mitigación |
|---|---|
| Mismo `recording_id` en train y test | Assertion automática en `datasets/splits.py`. Falla el job. |
| Mezcla de cantos de rana dentro de "ambient noise" | Auditoría manual de cada ambient antes de añadirlo + nota en `data/ambient/LICENSES.md`. |
| Mismas IRs en train y test | Para enhancement (Fase 9), separar IRs por split. Para clasificación, todas las IRs van a train. |
| Synthetic colándose a val/test | Loader excluye por defecto, test unitario que lo verifica. |
| Augmentado colándose a val/test | Augmentación lee `train_manifest.csv` y rechaza otros; assertion adicional en eval. |
| Duplicados de audio con distinto nombre | sha256 calculado al ingest; warning si colisión. |

---

## 5. Convenciones de nombres

### 5.1 Recordings
`<YYYYMMDD>_<HHMM>_<location_short>_<device>_<seq>.wav`
Ejemplo: `20260605_2210_lago_zoom_h6_01.wav`

### 5.2 IDs derivados
- `recording_id` = `sha256(absolute_path)[:12]`
- `event_id` = `<recording_id>__e<NNNN>`
- `clip_id` = `<recording_id>__e<NNNN>__<start_ms>_<end_ms>`
- `aug_id` = `<clip_id>__aug<idx>`
- `synth_id` = `synth_<type>_<NNNNNN>`

### 5.3 Artefactos
- Spectrograma: `<clip_id>.png` / `<recording_id>.npz`
- Modelo: `models/<run_id>/checkpoint.ckpt`
- Reporte de eval: `reports/eval_<run_id>.md`

---

## 6. Estado actual

| Categoría | Cantidad | Notas |
|---|---|---|
| Grabaciones reales (raw) | 0 | Pendientes de subir físicamente. |
| Clips extraídos | 0 | — |
| Clips curados | 0 | — |
| IRs disponibles | 0 | Pendiente recolección Fase 7. |
| Ambient noise | 0 | Pendiente recolección Fase 7. |
| Synthetic | 0 | Generación opcional. |

(Actualizar al cerrar T-021, T-040, T-061, T-070).

---

## 7. Advertencia científica sobre datos generados por IA

**No se entrenará el modelo final con datos sintéticos como única fuente.** Los sintéticos sirven exclusivamente para:

1. Validación del pipeline (sanity checks deterministas).
2. SNR sweeps controlados para medir robustez.
3. Ablations de componentes (¿el detector funciona en señales de prueba?).

Entrenar clasificadores bioacústicos con cantos sintetizados procedural o generativamente introduce:

- **Domain shift severo**: el modelo aprende características que no existen en cantos reales.
- **Label noise sistemático**: la "verdad" la inventa el generador.
- **Sesgo taxonómico**: imposible asignar identidad de especie a generados.
- **Pérdida de validez ecológica**: el modelo no es utilizable para monitoreo real.

Cualquier reporte derivado debe declarar proporción real/aumentado/sintético y discutir el sesgo.
