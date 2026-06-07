# CODEX_PROMPTS.md

> Prompts oficiales por fase. **Copiar/pegar tal cual a Codex.** Cada prompt es autosuficiente y empieza con el bloque obligatorio de lectura.

**Última actualización:** 2026-06-07
**Mantenedor:** Claude (arquitecto).

---

## BLOQUE OBLIGATORIO (prepender a TODOS los prompts)

```
ANTES DE HACER CAMBIOS:
1. Leer PROJECT_CONTEXT.md
2. Leer ARCHITECTURE.md
3. Leer ROADMAP.md
4. Leer TASKS.md
5. Leer HANDOFF_TO_CODEX.md
6. Verificar `git status` está limpio y que la rama es `main`.

Si existe contradicción entre archivos, ARCHITECTURE.md tiene prioridad.

REGLAS DURAS:
- No cambies la arquitectura sin pedir autorización explícita (requiere ADR en DECISIONS.md).
- No introduzcas dependencias nuevas sin documentarlas en pyproject.toml + ARCHITECTURE.md §8.
- No elimines documentación.
- No cambies formatos de manifest sin ADR.
- No crees estructuras paralelas al roadmap.
- Splits SIEMPRE por `recording_id`. Augmentación SOLO en train. Synthetic NUNCA en val/test.
- Validación de manifests con `pandera` (ADR-002b).
- Stack ML: PyTorch + Lightning (ADR-007). Sólo se instala a partir de Fase 8.

AL CERRAR LA TAREA, EN ESTE ORDEN:
1. TASKS.md → mover el ticket a Done con fecha y commit corto.
2. Si hubo decisión técnica → nueva ADR en DECISIONS.md.
3. Si hubo experimento → entrada en EXPERIMENT_LOG.md.
4. Si tocaste datos → actualizar DATASET_NOTES.md.
5. Archivar el handoff actual:
   cp HANDOFF_TO_CODEX.md docs/handoff_archive/HANDOFF_$(date +%Y-%m-%d)_<short_hash>.md
6. Reescribir HANDOFF_TO_CODEX.md con: estado actual, última decisión, tarea siguiente,
   archivos relevantes, riesgos, qué puede / no puede tocar Codex en la siguiente.

PROTOCOLO GIT (ADR-008):
- Un commit por tarea cerrada (commits intermedios permitidos, el final cierra el ticket).
- Mensaje: `<tipo>(T-NNN): <título corto>` + cuerpo con cambios + `Closes T-NNN`.
- Tipos: feat, fix, docs, refactor, test, chore, exp, data.
- `git add` SELECTIVO (no `git add .` ciego — revisar `git status` antes).
- Excluir SIEMPRE: data/raw, data/interim, data/processed, data/augmented, data/synthetic,
  outputs/runs, models/*.ckpt, .claude/, .cache/, wandb/.
- `git push origin main` tras el commit final del ticket.
- NUNCA `--force`, NUNCA `--no-verify`, NUNCA mezclar tareas distintas en un commit.
- Si el hook pre-commit falla, arreglar el problema y crear un NUEVO commit (no `--amend`).
```

---

## PROMPT 1 — Auditoría de repos previos (T-001) — **REVISADO según ADR-009**

```
[Bloque obligatorio arriba]

Tarea: T-001 — Estudiar los repos previos como referencia conceptual y poblar REUSE_REPORT.md.

Objetivo:
Extraer PATRONES, ideas y lógica reutilizables de:
- https://github.com/manueleco/texture-dataset-curation
- https://github.com/OriolFreixa/MirChordEstimationAugmentation

NO se clona código al proyecto. NO se importan ni se copian archivos.
Lo que entra al repo se reescribe de cero en `src/frogiso/` siguiendo nuestras convenciones,
referenciando el patrón origen vía ID R-NN en docstring.

Contexto:
- ADR-009: reuso por replicación, no por copia.
- Stack frogiso: librosa, scipy, soundfile, numpy, pandas, noisereduce, scikit-maad, sklearn,
  pandera, opcional torch+lightning en Fase 8.

Método de inspección permitido:
- GitHub web (lectura directa de archivos).
- `gh api repos/<owner>/<repo>/contents/<path>`.
- WebFetch sobre URLs concretas.
- NO clonar a .cache/ ni a ningún sitio.

Outputs:
REUSE_REPORT.md poblado con foco en PATRONES, no en código:
- Por cada repo, secciones "Reutilizable" / "Adaptar" / "Descartar" / "Riesgos".
- Cada item incluye:
  · ID estable R-NN (para referenciarlo desde docstrings y commits futuros).
  · Patrón / idea (descripción 1–3 frases).
  · URL del archivo fuente (https://github.com/... permalink) como referencia.
  · Qué hace allí (en 1–2 frases).
  · Cómo replicarlo idiomáticamente en frogiso: módulo/función destino propuesto.
  · Esfuerzo S/M/L.
- Tabla resumen final con prioridades.
- §7 con licencias verificadas (leer LICENSE de cada repo vía GitHub).

Criterios de aceptación:
- Cada URL apunta a un archivo verificable en GitHub (no inventada).
- Mínimo 5 reutilizables + 5 a adaptar + 3 a descartar por repo.
- Cada item de "Reutilizable" propone módulo destino concreto en frogiso.
- Tabla resumen con IDs R-NN estables.

Edge cases:
- Repo movido / renombrado / privado → registrar en §4 "Inaccesibilidad" y proponer alternativa.
- Archivo sin equivalente conceptual en bioacústica → va a "Descartar" con justificación.

NO hacer:
- No clonar repos al disco.
- No copiar bloques de código al repo frogiso (excepción: snippets ≤20 líneas de
  utilidad pura, citando autoría + licencia en docstring — ADR-009).
- No instalar deps de esos repos en el venv del proyecto.
- No crear ningún archivo bajo src/frogiso/ en esta tarea (la implementación viene en T-010+).
- No copiar al proyecto IRs, audios o assets de los repos.

Reciclado/referencia esperada (no exhaustiva):
- texture-dataset-curation: patrones de batch I/O, hashing/IDs, manifests CSV,
  estructura de notebooks EDA, logging.
- MirChordEstimationAugmentation: pipeline de convolutional reverb, mix con ambient
  a SNR target, random EQ suave, compresión suave, split por track sin leakage,
  configs YAML, estructura de runs.

Cierre:
1. TASKS.md: T-001 → Done con fecha.
2. HANDOFF_TO_CODEX.md: archivar v0002, escribir v0003 apuntando a PROMPT 2.
3. Commit: docs(T-001): document reusable patterns from previous repos (no code copy)
   Closes T-001
4. git push origin main.
```

---

## PROMPT 2 — Estructura del proyecto (T-010, T-011, T-012)

```
[Bloque obligatorio arriba]

Tarea: T-010 + T-011 + T-012 — Crear estructura del proyecto.

Objetivo:
Dejar el repo en estado "instalable y testeable" con utils básicos y schemas de manifest.

Inputs:
- ARCHITECTURE.md §3 (estructura), §4 (convenciones), §6 (schemas).

Outputs:
- pyproject.toml con deps base: librosa, soundfile, scipy, numpy, pandas, matplotlib, noisereduce, scikit-maad, scikit-learn, pyyaml, tqdm, click + (validación: pandera o pydantic — registrar ADR-002b con la decisión).
- src/frogiso/__init__.py con __version__ = "0.1.0".
- src/frogiso/utils/{logging,config,seed}.py.
- src/frogiso/io/{__init__,manifests,hashing}.py.
- configs/default.yaml con sample_rate, hop_length, n_fft, win_length, n_mels, fmin, fmax, paths.
- .gitignore.
- tests/test_manifests.py y tests/test_hashing.py.

Criterios de aceptación:
- `pip install -e .` en clean env funciona.
- `python -c "import frogiso; print(frogiso.__version__)"` imprime 0.1.0.
- `pytest tests/` pasa.
- `frogiso.utils.config.load_config("configs/default.yaml")` devuelve dict.
- Schemas de manifest validan los CSV declarados en ARCHITECTURE.md §6.

Qué NO debe hacer Codex:
- No añadir torch a deps base.
- No crear módulos DSP/ML aún.
- No tocar data/.

Reciclado:
- Patrón de batch I/O y hashing del repo texture-dataset-curation (si REUSE_REPORT.md lo confirma).
```

---

## PROMPT 3 — Espectrogramas batch (T-020, T-021)

```
[Bloque obligatorio arriba]

Tarea: T-020 + T-021 — Espectrogramas batch + notebook EDA.

Objetivo:
Generar STFT/mel/PCEN para todos los audios en un directorio y crear el notebook de exploración.

Contexto técnico:
- PCEN es estándar en bioacústica (Lostanlen et al.) — preferible cuando hay ruido de fondo variable.
- Las grabaciones pueden ser largas (>10 min). Stream/chunk si hace falta.

Inputs:
- Directorio de WAV/FLAC.
- YAML config con sr, n_fft, hop_length, n_mels, fmin, fmax, pcen {true/false}.

Outputs:
- src/frogiso/dsp/spectrograms.py: compute_stft, compute_mel, compute_pcen, plot_spectrogram, batch_process.
- scripts/run_eda.py CLI: --input-dir, --output-dir, --config, --format {png,npz,both}.
- outputs/figures/spectrograms/<recording_id>.png (300 dpi, ejes correctos).
- data/interim/spectrograms/<recording_id>.npz.
- notebooks/01_eda_spectrograms.ipynb con galería + distribuciones de duración/SR/energía.

Criterios de aceptación:
- Procesa ≥100 archivos sin OOM.
- NPZ determinístico (misma config → mismo hash).
- Resample automático si SR distinto del configurado; log de aviso.

Edge cases:
- Archivos corruptos → log warning, continuar.
- Audios estéreo → down-mix con aviso.
- Audios < n_fft samples → skip con log.

Qué NO debe hacer Codex:
- No detectar eventos.
- No escribir en data/raw/.
```

---

## PROMPT 4 — Band-pass configurable (T-030)

```
[Bloque obligatorio arriba]

Tarea: T-030 — Band-pass por especie.

Objetivo:
Implementar filtrado band-pass configurable por preset (configs/species/*.yaml).

Inputs:
- WAV o directorio.
- Config con lowcut, highcut, order, filter_type {butter, cheby1}, zero_phase {true/false}.

Outputs:
- src/frogiso/dsp/bandpass.py: design_filter, apply_filter, batch_apply.
- scripts/run_bandpass.py CLI.
- data/interim/bandpassed/<recording_id>.wav.
- outputs/figures/filters/<preset>.png con respuesta del filtro.

Criterios de aceptación:
- scipy.signal con filtfilt si zero_phase=true.
- Detección y warning de clipping en la salida.
- Test unitario del diseño del filtro (frecuencias de corte verificadas).

Edge cases:
- lowcut ≤ 0 o highcut ≥ nyquist → error claro.
- SR distinto → resample previo + log.

Qué NO debe hacer Codex:
- No aplicar denoising.
- No detectar eventos.
```

---

## PROMPT 5 — Detección por energía en banda (T-031)

```
[Bloque obligatorio arriba]

Tarea: T-031 — Detector heurístico de eventos.

Objetivo:
Detectar eventos por energía RMS en banda con threshold adaptativo.

Contexto:
Estrategia: energía RMS por frame → smoothing → threshold = mediana + k·MAD → eventos donde energía > threshold por > min_duration_ms. Merge de eventos separados por < merge_gap_ms.

Inputs:
- WAV (o directorio).
- Config: frame_ms, hop_ms, smoothing_ms, k_mad, min_duration_ms, max_duration_ms, merge_gap_ms, band {lowcut, highcut}.

Outputs:
- src/frogiso/detect/energy_detector.py.
- scripts/run_detect.py CLI.
- metadata/events.csv válido contra schema (ARCHITECTURE.md §6).
- outputs/figures/detections/<recording_id>.png con waveform + eventos resaltados.
- Si --debug: exportar array de energía por frame a outputs/debug/.

Criterios de aceptación:
- Reproducible (seed cuando aplique).
- Threshold se adapta y no satura en ruido constante.
- CSV con boundary_flag si el evento toca inicio/fin del archivo.
- Validación manual sobre 1 grabación: ≥80% de eventos coinciden con cantos audibles.

Edge cases:
- Cero eventos → CSV vacío con header.

Qué NO debe hacer Codex:
- No clasificar especies.
- No asumir que todo evento detectado es rana.
```

---

## PROMPT 6 — Extracción de clips (T-040)

```
[Bloque obligatorio arriba]

Tarea: T-040 — Extraer clips con padding.

Inputs:
- metadata/events.csv.
- Audios originales (no band-passed — queremos el clip "natural").
- Config: pad_pre_ms, pad_post_ms, normalize {none,peak,rms}, target_sr.

Outputs:
- data/processed/clips/<clip_id>.wav.
- data/processed/spectrograms/<clip_id>.png.
- metadata/clips.csv válido (schema en ARCHITECTURE.md §6).

Criterios de aceptación:
- Naming colisión-free; sha256 verificable.
- pad respetando límites del archivo.
- Test unitario del naming/IDs.

Edge cases:
- Eventos < 50 ms: flag short=true, exportar igual.
- Solapamientos: opción --merge-overlaps.

Qué NO debe hacer Codex:
- No descartar clips por "calidad" (eso lo hace curación manual).
```

---

## PROMPT 7 — Denoising y A/B (T-050)

```
[Bloque obligatorio arriba]

Tarea: T-050 — Denoising con A/B.

Inputs:
- Clip WAV o batch.
- Config: method {noisereduce, wiener}, stationary, prop_decrease, noise_profile_path (opcional).

Outputs:
- data/processed/clips_clean/<clip_id>.wav.
- outputs/figures/ab/<clip_id>.png: waveform/spectrogram original vs clean.
- metadata/denoise_log.csv con métricas SNR_pre/post y spectral flatness pre/post.
- HTML A/B en outputs/ab/index.html con audios embebidos.

Criterios de aceptación:
- Reproducible.
- Si métrica empeora → log warning.
- No sobrescribir el original.

Edge cases:
- Clips muy cortos → skip con log.

Qué NO debe hacer Codex:
- No prometer remoción de ruido específico (ej. insectos).
- No usar modelos generativos para "limpiar".
```

---

## PROMPT 8 — Notebook de curación (T-060)

```
[Bloque obligatorio arriba]

Tarea: T-060 — Notebook de revisión manual.

Outputs:
- notebooks/05_manual_curation.ipynb con ipywidgets.
- metadata/curation.csv (save incremental).

Funcionalidad:
- Muestra: waveform + spectrogram + reproductor de audio + metadata del clip.
- Etiqueta: positive / negative / ambiguous / discard.
- Confianza 1–5, notas libres.
- Filtros: sólo no-etiquetados, por recording, por duración.
- Botones / atajos para etiquetado rápido.

Criterios de aceptación:
- Guardado incremental (no perder progreso al cerrar).
- No mueve archivos físicamente; sólo etiqueta.
- Idempotente: re-abrir el notebook recupera el progreso.

Qué NO debe hacer Codex:
- No sobrescribir labels existentes sin confirmación.
```

---

## PROMPT 9 — Splits sin leakage (T-080)

```
[Bloque obligatorio arriba]

Tarea: T-080 — Split train/val/test por recording_id.

Inputs:
- metadata/clips.csv + metadata/curation.csv.
- Config: ratios (default 70/15/15), stratify_by {label}, seed.

Outputs:
- data/splits/{train,val,test}_manifest.csv.
- reports/split_stats.md con conteos por label y recording.

Criterios de aceptación:
- Assertion: ningún recording_id en >1 split.
- Test unitario que verifica intersección vacía.
- Ratios ±2%.

Edge cases:
- Recording con 1 clip → train por defecto, configurable.
- Clases muy desbalanceadas → warning + sugerir oversampling en augmentación.

Qué NO debe hacer Codex:
- No duplicar clips entre splits "por balance".

Reciclado:
- Lógica de split a nivel de track de MirChordEstimationAugmentation.
```

---

## PROMPT 10 — Augmentación realista (T-071)

```
[Bloque obligatorio arriba]

Tarea: T-071 — Augmentación realista para bioacústica.

Contexto:
SÓLO se aplica a clips cuyo recording_id esté en train_manifest.csv (ADR-006). Augmentar val/test = fail del job.

Augmentaciones:
1. Convolutional reverb con IRs de exteriores (data/irs/).
2. Mix con ambient noise (data/ambient/) a SNR target muestreado de [3, 20] dB.
3. Random EQ suave (±3 dB en 2–3 bandas).
4. Compresión suave (ratio 2–4, threshold -20..-10 dBFS).
5. Time/pitch shift moderado → off por defecto.

Inputs:
- train_manifest.csv.
- configs/augmentation.yaml con rangos y probabilidades.
- data/irs/, data/ambient/ con manifests de licencia.

Outputs:
- data/augmented/train/<clip_id>__aug<idx>.wav.
- metadata/augmentation_log.csv con todos los parámetros + seed.
- Plot de N=10 pares original vs augmentado para sanity.

Criterios de aceptación:
- Reproducible por seed por clip.
- Reverb no alarga clip más del margen configurable.
- SNR final medido coincide con target ±1 dB.
- Verificar que el ambient mezclado NO contiene ranas (consultar data/ambient/LICENSES.md).
- Falla si recording_id no está en train.

Edge cases:
- IRs/ambient ausentes → skip esa augmentación con warning.

Qué NO debe hacer Codex:
- No aplicar a val/test.
- No descargar de Freesound automáticamente.
- No usar IRs de salas/iglesias (sólo exteriores).
```

---

## PROMPT 11 — Synthetic controlado (T-072)

```
[Bloque obligatorio arriba]

Tarea: T-072 — Generación sintética controlada.

Objetivo:
Generar ejemplos sintéticos CONTROLADOS para validar el pipeline. NO para entrenar el modelo final.

Tipos:
a) Tonos AM/FM modulados.
b) Trenes de pulsos con envelope.
c) Mezclas controladas: clip_real_positivo + ruido a SNR target.

Inputs:
- Config: type, freq_range, syllable_rate, duration, snr_target, n_examples.

Outputs:
- data/synthetic/<type>/<synth_id>.wav.
- metadata/synthetic_manifest.csv con is_synthetic=true.
- README en data/synthetic/ con advertencia.

Criterios de aceptación:
- Manifest separado del dataset real.
- Loader excluye synthetic por defecto.
- Docstring del módulo con advertencia obligatoria:
  "Synthetic samples are for pipeline validation and SNR robustness studies only. Training bioacoustic classifiers exclusively on synthetic data leads to severe domain shift and is not scientifically valid."

Qué NO debe hacer Codex:
- No mezclar synthetic con curated/.
- No marcar synthetic como label positivo "rana".
```

---

## PROMPT 12 — Baseline sklearn + CNN (T-081, T-082)

```
[Bloque obligatorio arriba]

Tarea: T-081 + T-082 — Baselines ML.

Stack:
- sklearn baseline: RandomForest sobre MFCC stats + spectral centroid + rolloff + ZCR + scikit-maad indices.
- CNN small (PyTorch + Lightning): 3 conv blocks + GAP + linear.

Inputs:
- Splits manifests.
- Config: model {sklearn_rf, cnn_small}, batch_size, epochs, lr, mel params.

Outputs:
- src/frogiso/models/sklearn_baseline.py.
- src/frogiso/models/cnn_small.py.
- scripts/run_train.py CLI con --model.
- models/<run_id>/{checkpoint.ckpt, config.yaml, git_sha.txt, dataset_hashes.txt}.
- outputs/runs/<run_id>/{loss_curves.png, metrics.csv}.

Criterios de aceptación:
- Determinístico con seed global.
- wandb opcional (si WANDB_API_KEY), fallback CSV+matplotlib.
- Augmentación leída desde data/augmented/, SÓLO en train.
- Class weighting si imbalance > 2:1.

Edge cases:
- Dataset pequeño (<100/clase) → warning sugiriendo más curación.

Qué NO debe hacer Codex:
- No mezclar splits.
- No evaluar en train.
- No usar modelos pre-entrenados pesados (eso es Fase 9).
```

---

## PROMPT 13 — Evaluación (T-083)

```
[Bloque obligatorio arriba]

Tarea: T-083 — Evaluación cuantitativa + cualitativa.

Outputs:
- src/frogiso/eval/metrics.py.
- scripts/run_eval.py.
- reports/eval_<run_id>.md con: precision/recall/F1 (por clase, macro, micro), ROC-AUC, PR-AUC, confusion matrix PNG.
- outputs/eval/<run_id>/{false_positives,false_negatives}/ con clips + spectrograms.
- outputs/eval/<run_id>/index.html con audios embebidos para escucha.
- Métricas estratificadas por SNR y por fondo dominante.

Criterios de aceptación:
- Threshold sweep para curva PR.
- Sección "qualitative findings" con conteos por recording y banda dominante.

Edge cases:
- Test sin ejemplos de una clase → skip métrica afectada con log.

Qué NO debe hacer Codex:
- No ajustar threshold sobre test.
- No reportar sólo accuracy.
```

---

## PROMPT 14 — README + reporte académico (T-100)

```
[Bloque obligatorio arriba]

Tarea: T-100 — README final + final_report.md.

Outputs:
- README.md actualizado con: descripción, arquitectura (link a figura/diagrama), instalación, reproducción de cada fase con comandos exactos, estructura del repo, limitaciones, licencia, citaciones.
- reports/final_report.md paper-style: Abstract, Background, Datos, Métodos, Resultados (tablas + figuras), Discusión, Limitaciones (incl. advertencia sobre datos sintéticos), Trabajo futuro, Referencias.

Criterios de aceptación:
- Cita métricas reales del último run.
- Sección explícita "Ethical and scientific considerations on synthetic data".
- Reproducible siguiendo sólo el README en un entorno limpio.

Qué NO debe hacer Codex:
- No inventar métricas.
- No sobreestimar la calidad de separación.
```

---

## PROMPT 15 — Embeddings + clustering (T-090, opcional)

```
[Bloque obligatorio arriba]

Tarea: T-090 — Embeddings pre-entrenados (BirdNET/Perch) + clustering.

Objetivo:
Extraer embeddings, hacer UMAP + HDBSCAN, comparar con baseline.

Outputs:
- src/frogiso/embeddings/<modelo>.py.
- scripts/run_embed.py + run_cluster.py.
- outputs/embeddings/<run_id>/.
- reports/phase_9_report.md con comparación honesta vs baseline.

Criterios de aceptación:
- Si embeddings + linear probe NO mejora baseline → reportarlo claramente, no esconderlo.

Qué NO debe hacer Codex:
- No fine-tunear el modelo pre-entrenado (sólo embeddings/linear probe).
- No usar modelos cuya licencia prohíba uso académico.
```

---

## Notas para Claude (mantenedor de este archivo)

- Si una tarea cambia de scope, **nueva versión del prompt** abajo, no se edita la anterior.
- Numerar prompts coherentemente con TASKS.md.
- Cada vez que se cierra un ticket, comprobar si el prompt necesita actualización para el siguiente.
