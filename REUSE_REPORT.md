# REUSE_REPORT.md

> Auditoría de repos previos. **Documento a poblar por Codex en la tarea T-001.**
>
> Claude deja aquí el esqueleto y la guía. Codex sustituye los `TODO` con análisis real (rutas concretas verificables).

**Última actualización:** 2026-06-07
**Estado:** Done T-001

---

## 0. Cómo usar este documento

> **ADR-009: reuso por replicación de patrón, no por copia de código.**
> No clonamos ni importamos archivos. Documentamos *ideas* y proponemos cómo replicarlas
> idiomáticamente en `src/frogiso/`. Las URLs son referencia, no fuente de import.

- **No editar las secciones de framework.** Editar sólo los placeholders `TODO`.
- Cada item incluye:
  - **ID R-NN** estable (lo citamos en docstrings y commits futuros).
  - **Patrón/idea** (1–3 frases).
  - **URL de referencia** (permalink GitHub al archivo o función concreta).
  - **Qué hace allí** (1–2 frases).
  - **Cómo replicarlo aquí**: módulo/función destino propuesto en `src/frogiso/`.
  - **Esfuerzo**: S (≤1 día), M (2–4 días), L (≥5 días o riesgo alto).
- Si una URL deja de existir o el repo es inaccesible, registrarlo en §4.

---

## 1. Repo A — `manueleco/texture-dataset-curation`

**URL:** https://github.com/manueleco/texture-dataset-curation
**Dominio original:** dataset curation para textures / generative.
**Encaje conceptual con bioacústica:** moderado — los patrones de I/O y curación se traducen bien; el dominio sonoro no.
**Checkout auditado:** `.cache/external_repos/texture-dataset-curation` (`d42655b`, rama `main`).

### 1.1 Reutilizable (alta confianza)

| Ruta | Qué hace | Cómo encaja aquí | Esfuerzo |
|---|---|---|---|
| `scripts/01_build_manifest.py:main` | Recorre `data/raw/piano/fur_elise/*.wav`, lee `soundfile.sf.info`, calcula duración a partir de frames/samplerate y escribe `data/processed/manifest.csv`. | Base directa para `scripts/run_ingest.py`: patrón de escaneo batch, extracción de metadatos de audio y escritura CSV. | S |
| `data/processed/manifest.csv` | Manifest tabular con `path,filename,samplerate,channels,frames,duration_sec` para 62 WAV. | Semilla conceptual para `metadata/recordings.csv`: conserva la idea de manifest versionable e inspeccionable, aunque el schema debe ampliarse según `ARCHITECTURE.md §6`. | S |
| `notebooks/datasetOverview.ipynb` (`## 1. Load manifest`) | Carga el manifest y crea carpetas `results/figures` y `results/logs` antes de analizar. | Patrón útil para notebooks de EDA retomables que leen manifests y guardan figuras/logs sin estado implícito. | S |
| `notebooks/datasetOverview.ipynb` (`## 2. Basic stats`, `## 3. Histograms`) | Resume columnas, estadísticos de duración y genera `results/figures/duration_hist.png`. | Reutilizable como estructura de `notebooks/01_eda_spectrograms.ipynb`: estadísticas de duración/SR/canales antes de DSP. | S |
| `notebooks/datasetOverview.ipynb` (celdas QC con `peak`, `rms`, `silence_ratio`, `clipped`) | Lee audio con `soundfile`, calcula métricas simples de nivel/silencio/clipping y crea una muestra QC. | Encaja en ingest/curación como checks baratos antes de espectrogramas: clipping, silencio y RMS por recording/clip. | S |
| `data/processed/qc_sample.csv` | CSV de revisión con `filename,peak,rms,silence_ratio,clipped`, ordenado para inspección. | Buen patrón para `metadata/*_qc.csv` o reportes de curación manual asistida. | S |
| `results/logs/dataset_summary.json` | Resumen persistido con número de archivos, SR, canales, duración y rutas de artefactos. | Encaja con `outputs/logs/` y `outputs/figures/`: cada fase debe dejar un resumen reproducible y pequeño. | S |

**Mínimo:** 5 items. Foco esperado en: batch I/O, hashing/IDs, manifests CSV, estructura de notebooks, logging.

### 1.2 Adaptar (parcial; requiere cambios)

| Ruta | Qué hace originalmente | Qué cambiar para bioacústica | Esfuerzo |
|---|---|---|---|
| `scripts/01_build_manifest.py` | Tiene rutas hardcodeadas (`AUDIO_DIR`, `OUT_CSV`) y solo busca `*.wav` en una carpeta fija. | Convertir a CLI con `--config`, leer `configs/default.yaml`, recorrer `data/raw/` de forma recursiva y aceptar WAV/FLAC/MP3 si el stack lo soporta. | S |
| `scripts/01_build_manifest.py` | Usa `p.name` como identidad principal. | Añadir `recording_id = sha256(absolute_path)[:12]`, `sha256` de contenido y detección de duplicados, como exige `ARCHITECTURE.md §4.1` y §6. | M |
| `data/processed/manifest.csv` | Schema mínimo para clips musicales homogéneos. | Sustituir por `metadata/recordings.csv` con `recording_id,path,sha256,duration_s,sample_rate,channels,source,license,recorded_at,notes`. | S |
| `notebooks/datasetOverview.ipynb` | EDA centrada en duración, audio player y métricas generales. | Añadir espectrogramas STFT/mel/PCEN, energía por bandas candidatas, percentiles de ruido y ejemplos de eventos rana/no-rana. | M |
| `notebooks/datasetOverview.ipynb` (QC `silence_ratio`) | Define silencio como `abs(y) < 1e-3`, independiente de SR/banda/ruido de campo. | Reemplazar por métricas robustas: `peak_dbfs`, RMS por banda, ruido de fondo, SNR estimado y flags por clipping/saturación/viento. | M |
| `results/logs/dataset_summary.json` | Guarda resumen sin hash de config ni versión de detector/ingest. | Añadir `run_id`, hash de config, fecha, commit del proyecto y rutas relativas bajo `outputs/logs/`. | S |
| `requirements.txt` | Lista dependencias útiles (`numpy`, `pandas`, `librosa`, `soundfile`, `matplotlib`, `tqdm`, `jupyter`). | Llevar solo las deps base que ya permite `ARCHITECTURE.md §8`; `jupyter/ipykernel` deben quedar en extra de notebooks, no en core. | S |

**Foco esperado en:** schemas de metadata (añadir campos bioacústicos: `species_guess`, `dominant_band_hz`, `call_rate_hz`, `SNR_db`), pipelines de transformación.

### 1.3 Descartar (no aplicable)

| Ruta | Por qué no aplica |
|---|---|
| `README.md` | Es demasiado breve y solo declara "Generative Algorithms - Texture Dataset curation"; no aporta protocolo reproducible ni diseño transferible. |
| `data/processed/manifest.csv` (filas `data/raw/piano/fur_elise/*`) | Los datos auditados son clips de piano de Fur Elise, no bioacústica; no se reciclan datos ni etiquetas. |
| `results/figures/duration_hist.png` | Figura estática generada para ese dataset; debe regenerarse desde manifests reales del proyecto. |
| `notebooks/datasetOverview.ipynb` (`## 4. Play sounds`) | Audio player con ejemplos de piano y salida embebida; no aporta curación de cantos ni conviene versionar audio embebido. |
| `.DS_Store` y `data/.DS_Store` | Metadatos locales de macOS; deben ignorarse siempre. |

**Foco esperado:** generación de texturas sonoras, priors estadísticos del dominio texture, métricas perceptuales de textura.

### 1.4 Riesgos de reciclar sin adaptar

- Tratar cada archivo como textura homogénea puede ocultar la estructura temporal del canto: onset, offset, trenes de pulsos y pausas son parte central del problema.
- Mantener rutas hardcodeadas rompería el principio de configuración por YAML y haría el pipeline difícil de reproducir en otro equipo.
- Usar `filename` como ID provocaría colisiones al mezclar sesiones/cámaras/grabadoras; el proyecto exige `recording_id` y hashes.
- El QC de silencio/clipping no distingue ruido ambiental de baja energía frente a ausencia real de canto.
- No hay LICENSE detectable; no se debe copiar código del repo A sin permiso/licencia clara.
- El repo A no implementa splits ni control de leakage; reciclarlo como dataset pipeline completo dejaría un hueco crítico.

---

## 2. Repo B — `OriolFreixa/MirChordEstimationAugmentation`

**URL:** https://github.com/OriolFreixa/MirChordEstimationAugmentation
**Dominio original:** robust automatic chord estimation through realistic audio augmentation (UPF/MTG).
**Encaje conceptual con bioacústica:** **alto** para el pipeline de augmentación y splits; **bajo** para los front-ends musicales.
**Checkout auditado:** `.cache/external_repos/MirChordEstimationAugmentation_partial` (`64df935`, rama `main`). Ver §4 para la incidencia del clone completo.

### 2.1 Reutilizable (alta confianza)

| Ruta | Qué hace | Cómo encaja aquí | Esfuerzo |
|---|---|---|---|
| `data_augmentation_merged.py:apply_reverb` / `apply_reverb_arr` | Convoluciona audio con una IR, recorta a la longitud original y mezcla wet/dry. | Base conceptual para `src/frogiso/augment/reverb.py` usando IRs exteriores auditadas y logueadas. | S |
| `data_augmentation_merged.py:add_real_noise` / `add_real_noise_arr` | Tila/recorta un ruido real, normaliza RMS y lo mezcla con la señal. | Base para `src/frogiso/augment/mix_noise.py`, con ambients de viento/agua/insectos y SNR objetivo medido. | M |
| `data_augmentation_merged.py:randomly_eq` / `randomly_eq_arr` | Aplica filtros por bandas con ganancia aleatoria y evita bandas fuera de Nyquist. | Útil para EQ suave en train, con bandas y gains controlados por `configs/augmentation.yaml`. | S |
| `data_augmentation_merged.py:apply_compression` / `apply_compression_arr` | Implementa compresor feed-forward con threshold, ratio, attack, release y makeup gain. | Útil para simular grabadoras/procesado de campo, con límites conservadores y log por clip. | S |
| `previous_sanity_check/generate_reverb_augments.py:generate_reverb_augments` | Itera audio x IR, excluye subcarpetas `examples/images`, slugifica nombres y genera variantes. | Patrón para batch augmentation reproducible y nombres de salida; debe adaptarse a `augmentation_log.csv`. | S |
| `ace_safe_trainer.py:_canonical_track_id`, `_split_dataset`, `LeakageSafeChocoAudioDataset` | Agrupa variantes aumentadas con su track fuente y evita que entren en val/test limpios. | Patrón de oro para `src/frogiso/datasets/splits.py`: renombrar track/source a `recording_id`. | M |
| `previous_sanity_check/jams_extra.py:build_augmented_jams` | Copia anotaciones JAMS originales a audios aumentados derivando el stem base. | Reutilizable como idea para propagar `clip_id/source_clip_id` a `augmentation_log.csv`, no como JAMS. | M |
| `preprocess/audio_processor.py:AudioProcessor` y `AudioChunkProcessor` | Carga audio, resamplea, pasa a mono, corta/pad, normaliza y procesa chunks. | Patrón parcial para loaders/clip extraction y preprocesado determinístico. | M |
| `preprocess/dataset.gin` | Centraliza sample rate, hop length, duración, paths, extensiones y jobs. | Aunque el proyecto usa YAML, la lista de parámetros ayuda a diseñar `configs/default.yaml` y `configs/augmentation.yaml`. | S |

**Mínimo:** 5 items.

### 2.2 Adaptar (parcial)

| Ruta | Qué hace originalmente | Qué cambiar para bioacústica | Esfuerzo |
|---|---|---|---|
| `data_augmentation_merged.py:add_real_noise` | Mezcla por `wet_dry_mix` relativo al RMS, no por SNR explícito ni con manifest de licencia. | Convertir a `snr_target_db` y medir `snr_measured_db`; exigir `ambient_used` con licencia en `metadata/augmentation_log.csv`. | M |
| `data_augmentation_merged.py:apply_reverb` | Usa IRs de salas/iglesias/estudios y normaliza salida. | Restringir a IRs exteriores o espacios plausibles; medir/filtrar RT60; evitar normalización que destruya niveles relativos. | M |
| `data_augmentation_merged.py:randomly_eq` | Bandas musicales por defecto `(100,500)`, `(500,2000)`, `(2000,8000)` y gain `[-6,+6] dB`. | Usar bandas por especie/preset y gains más conservadores (p. ej. ±3 dB) para no mover el canto fuera de su banda dominante. | S |
| `data_augmentation_merged.py:apply_compression` | Defaults musicales: threshold -20 dBFS, ratio 4:1 y normalización final. | Reducir agresividad, loguear parámetros y comparar A/B porque la compresión puede subir insectos/agua tanto como la rana. | S |
| `previous_sanity_check/data_augmentation.py:add_noise` | Genera ruido blanco/rosa/marrón con SNR sintético. | Mantener solo para stress tests o `data/synthetic/`; no usar como negativo real ni como augment principal. | S |
| `preprocess/audio_processor.py:AudioProcessor._pitch_shift` | Pitch-shift en semitonos para transposición musical. | Quitar de la ruta base; si se usa pitch/time perturbation, definir rangos bioacústicamente plausibles por especie y registrarlos. | M |
| `preprocess/transforms.py:CQTransform` | CQT orientada a notas (`bins_per_octave`, `start_note="C1"`). | Sustituir por STFT/mel/PCEN del módulo `src/frogiso/dsp/spectrograms.py`; no usar afinación musical. | M |
| `preprocess/preprocess_data.py:ChoCoProcessor` | Procesa canciones y JAMS a `.pt`, limpia cache con `file.unlink()` y genera chunks por canción. | Cambiar a manifests CSV y clips/eventos; nunca borrar cache de forma implícita; outputs regenerables bajo `data/interim/` o `data/processed/`. | L |
| `ace_safe_trainer.py:ChocoAudioDataModule` | Asume datasets Billboard/Isophonics/MARL, `.pt` preprocesados y vocabularios de acordes. | Reescribir para `clip_id,label,recording_id,source,split`, clasificación frog/no-frog y validación anti-leakage por `recording_id`. | M |
| `preprocess/dataset.gin` | Config Gin con rutas del experimento y `augmentation_range` musical. | Traducir a YAML, separar `default.yaml` de `augmentation.yaml`, y eliminar parámetros musicales. | S |
| `previous_sanity_check/jams_extra.py:build_augmented_jams` | Copia JAMS al audio aumentado usando `original_stem = augmented_stem.split("_")[0]`. | Cambiar a mapping explícito por `clip_id` para evitar errores si el ID contiene `_`; registrar `source_clip_id`. | M |

### 2.3 Descartar

| Ruta | Por qué no aplica |
|---|---|
| `preprocess/chord_utils.py` | Codifica raíces, bajos y modos de acordes Harte con `music21`; supuestos tonales occidentales irrelevantes para ranas. |
| `preprocess/chord_processor.py` | Convierte anotaciones JAMS de acordes a vocabularios `root`, `bass`, `majmin`, `complete`; no hay transferencia directa a eventos bioacústicos. |
| `previous_sanity_check/utils.py:compute_chroma_features` y `previous_sanity_check/auxiliary.py:plot_chroma_features` | Chroma STFT/CENS descarta información espectral absoluta que sí importa en bioacústica. |
| `preprocess/transforms.py:CQTransform` | La CQT con `start_note` y octavas está diseñada para armonía musical; para rana convienen mel/PCEN o STFT parametrizados por banda. |
| `irs/1st-baptist-nashville/`, `irs/heslington-church-vaa-group-2/`, `irs/lady-chapel-st-albans-cathedral/`, `irs/genesis-6-studio-live-room-drum-set/` | IRs de iglesias/estudios/salas; pueden alargar sílabas y no representan campo exterior salvo experimento controlado. |
| `training_jams_data/Checkpoints/` y `training_plus_augmentaiton/Checkpoints/` | Checkpoints ACE pesados, específicos de acordes y sin utilidad para baseline frog/no-frog. |
| `training_jams_data/preprocessed_data/` y `training_plus_augmentaiton/preprocessed_data_backup_before_rename/` | Miles de `.pt` preprocesados de música; no se copian datos ni formatos binarios como fuente de verdad. |
| `augmentations_test_outputs/` | MP3 generados para sanity checks musicales; no usar como datos ni como referencia de calidad. |
| `wandb/` | Runs locales versionados; deben permanecer fuera de este proyecto salvo métricas resumidas manualmente. |

### 2.4 Riesgos de reciclar sin adaptar

- **Reverb agresivo** alarga sílabas y rompe la detección por energía. Limitar a IRs cortas (RT60 ≤ 1.5 s).
- **Compresión agresiva** sube el ruido al nivel del canto: degrada SNR justo al revés del objetivo. Mantener ratios ≤4, threshold ≥ -20 dBFS.
- **EQ aleatorio amplio** puede mover el centroide fuera de la banda biológica. Limitar gains a ±3 dB.
- **Mezclar ambients de Freesound sin auditar** puede meter ranas en los "negativos" → label noise. Auditoría manual obligatoria (ver `DATASET_NOTES.md §1.4`).
- `data_augmentation_merged.py` escribe MP3 por defecto; este proyecto debe preferir WAV/FLAC lossless para clips y A/B.
- La normalización final en reverb/EQ/compresión puede destruir relaciones de nivel y SNR que luego se evalúan.
- `ace_safe_trainer.py` resuelve leakage por suffix de filename; si se porta literalmente a `clip_id`, IDs con `_` o sufijos inesperados pueden romper el grouping.
- `preprocess/preprocess_data.py:_clean_cache` borra archivos del cache al iniciar; no encaja con el principio de pipeline retomable.
- El repo B versiona checkpoints, audios, `.pt` y `wandb/`; copiar su estructura de repo traería deuda de almacenamiento y riesgo de licencias.
- No hay LICENSE de repo detectable; usar solo como referencia conceptual hasta tener permiso/licencia clara.

---

## 3. Tabla resumen — prioridades de reuso

| ID | Origen | Concepto/Archivo | Prioridad | Esfuerzo | Encaje en proyecto |
|---|---|---|---|---|---|
| R-01 | Repo B | `data_augmentation_merged.py:apply_reverb` | Alta | S | `src/frogiso/augment/reverb.py` (Fase 7), reimplementado con IRs exteriores. |
| R-02 | Repo B | `data_augmentation_merged.py:add_real_noise` | Alta | M | `src/frogiso/augment/mix_noise.py`, con SNR objetivo y licencias de ambients. |
| R-03 | Repo B | `ace_safe_trainer.py:_split_dataset` + grouping por fuente | Alta | M | `src/frogiso/datasets/splits.py`, split por `recording_id` sin leakage. |
| R-04 | Repo A | `scripts/01_build_manifest.py:main` | Alta | S | `scripts/run_ingest.py`, patrón de batch I/O + `soundfile` metadata. |
| R-05 | Repo A | `data/processed/manifest.csv` | Alta | S | Diseño inicial de `metadata/recordings.csv`, ampliado a schema normativo. |
| R-06 | Repo A | `notebooks/datasetOverview.ipynb` QC (`peak`, `rms`, `silence_ratio`, `clipped`) | Alta | S | Checks de ingest/curación antes de entrenar. |
| R-07 | Repo B | `previous_sanity_check/generate_reverb_augments.py` | Media | S | Batch augmentation con nombres slugificados y exclusión de subdirectorios no-IR. |
| R-08 | Repo B | `data_augmentation_merged.py:randomly_eq` | Media | S | `src/frogiso/augment/eq.py`, gains y bandas conservadoras. |
| R-09 | Repo B | `data_augmentation_merged.py:apply_compression` | Media | S | `src/frogiso/augment/compression.py`, ratio/threshold auditables. |
| R-10 | Repo B | `preprocess/audio_processor.py:AudioProcessor` | Media | M | Preprocesado deterministicamente configurable: resample, mono, crop/pad, normalize. |
| R-11 | Repo B | `previous_sanity_check/jams_extra.py:build_augmented_jams` | Media | M | Propagación explícita de anotaciones a aumentados vía `source_clip_id`. |
| R-12 | Repo B | `preprocess/dataset.gin` | Media | S | Lista de parámetros para trasladar a YAML (`default.yaml`, `augmentation.yaml`). |
| R-13 | Repo A | `results/logs/dataset_summary.json` | Media | S | Resúmenes por fase bajo `outputs/logs/` con rutas de artefactos. |
| R-14 | Repo B | `data_augmentation_merged.py:add_noise` | Baja | S | Solo stress tests/synthetic; nunca val/test ni negativos reales. |
| R-15 | Repo B | `requirements.txt` / `pyproject.toml` | Baja | M | Auditoría de dependencias; no instalar en venv principal ni copiar pinning CUDA. |
| R-16 | Repo A | `requirements.txt` | Baja | S | Confirmar solapamiento con deps base (`librosa`, `soundfile`, `pandas`, etc.). |
| R-17 | Repo B | `separate_billboard.py` | Baja | M | Idea de filtrado por corpus, pero evitar `shutil.move` destructivo; usar manifests. |
| R-18 | Repo B | `data_augmentation_real.ipynb` | Baja | L | Referencia narrativa de experimento; no convertir en pipeline principal. |

IDs estables para futuras tareas: `R-01` a `R-18`.

---

## 4. Inaccesibilidad

- `texture-dataset-curation` fue clonado y auditado normalmente en `.cache/external_repos/texture-dataset-curation` (`d42655b`).
- El primer `git clone https://github.com/OriolFreixa/MirChordEstimationAugmentation.git .cache/external_repos/MirChordEstimationAugmentation` descargó ~1.2 GB de `.git` pero quedó sin `HEAD` ni worktree (`git rev-parse HEAD` falló con `Needed a single revision`).
- Un segundo clone superficial en `.cache/external_repos/MirChordEstimationAugmentation_shallow` también quedó sin `HEAD`.
- La alternativa válida fue `git clone --filter=blob:none --no-checkout --depth 1 ... .cache/external_repos/MirChordEstimationAugmentation_partial`, auditado con `git ls-tree` y `git show` de blobs concretos de texto (`64df935`).
- No se descargaron intencionalmente blobs pesados de audio, checkpoints, `.pt` ni runs `wandb/`; sus rutas sí fueron verificadas por `git ls-tree`.
- No hay archivos fuente relevantes inaccesibles para T-001; las limitaciones afectan solo al checkout completo y a assets/binarios que no deben copiarse.

---

## 5. Ganancias esperadas

- **Tiempo ahorrado en augmentación realista** (Fase 7): semanas → días.
- **Tiempo ahorrado en infraestructura de manifests/splits** (Fase 1, 8): días.
- **Patrones de evaluación baseline vs augmented** (Fase 8): ahorro de diseño.

---

## 6. Riesgos sistémicos del reuso

| Riesgo | Mitigación |
|---|---|
| Trasladar supuestos musicales (tonalidad, armonía) al dominio bioacústico | Auditoría explícita en §2.3; rechazar componentes que dependan de esos supuestos. |
| Heredar bugs no detectados de los repos originales | Tests propios sobre lo reciclado, especialmente en splits y augmentación. |
| Incompatibilidad de licencias | Codex verifica licencia de ambos repos en T-001 y la registra aquí. |
| Dependencias obsoletas en los repos originales | Reescribir contra versiones actuales del stack (librosa, scipy, torch). |
| Heredar formatos binarios como fuente de verdad (`.pt`, checkpoints, MP3) | Mantener CSV manifests como fuente de verdad y regenerar artefactos pesados. |
| Reutilizar notebooks con salidas embebidas como pipeline | Convertir solo las ideas a scripts CLI + notebooks ligeros de revisión. |
| Copiar assets externos sin licencia trazable | Usar manifests de licencia en `data/irs/LICENSES.md` y `data/ambient/LICENSES.md`; no copiar assets auditados aquí. |

---

## 7. Licencias de los repos originales

| Repo | Licencia detectada | Compatible con uso académico aquí | Notas |
|---|---|---|---|
| texture-dataset-curation | **No detectada**. No hay `LICENSE`, `LICENSE.md`, `COPYING` ni `NOTICE` en el checkout; `README.md` no declara licencia. | Compatible solo como referencia conceptual. **No copiar código ni datos** sin permiso/licencia explícita. | Verificado con `find .cache/external_repos/texture-dataset-curation -maxdepth 3 ...`; datos auditados son rutas de piano/Fur Elise y no se reutilizan. |
| MirChordEstimationAugmentation | **No detectada para el repo**. No hay `LICENSE`, `LICENSE.md`, `COPYING` ni `NOTICE` en el árbol root (`git ls-tree`); `README.md` cita OpenAIR/Freesound pero no declara licencia del código. | Compatible solo como referencia conceptual y reimplementación propia. **No copiar código, IRs, MP3, checkpoints ni `.pt`** sin permiso/licencia explícita. | IRs bajo `irs/*/Read Me.txt` incluyen metadatos técnicos, no términos de licencia suficientes. Requiere auditoría externa antes de usar cualquier asset. |
