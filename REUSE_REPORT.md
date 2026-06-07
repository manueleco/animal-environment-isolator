# REUSE_REPORT.md

> Auditoría de repos previos. **Documento a poblar por Codex en la tarea T-001.**
>
> Claude deja aquí el esqueleto y la guía. Codex sustituye los `TODO` con análisis real (rutas concretas verificables).

**Última actualización:** 2026-06-07 (esqueleto inicial)
**Estado:** Pending T-001

---

## 0. Cómo usar este documento

- **No editar las secciones de framework.** Editar sólo los placeholders `TODO`.
- Cada item debe citar **ruta real** del repo original: `path/to/file.py:func_name` o `path/to/module/`.
- Esfuerzo: **S** (≤1 día), **M** (2–4 días), **L** (≥5 días o riesgo alto).
- Si una ruta deja de existir o el repo es inaccesible, registrarlo en §4.

---

## 1. Repo A — `manueleco/texture-dataset-curation`

**URL:** https://github.com/manueleco/texture-dataset-curation
**Dominio original:** dataset curation para textures / generative.
**Encaje conceptual con bioacústica:** moderado — los patrones de I/O y curación se traducen bien; el dominio sonoro no.

### 1.1 Reutilizable (alta confianza)

| Ruta | Qué hace | Cómo encaja aquí | Esfuerzo |
|---|---|---|---|
| TODO | TODO | TODO | S/M/L |
| TODO | TODO | TODO | S/M/L |
| TODO | TODO | TODO | S/M/L |
| TODO | TODO | TODO | S/M/L |
| TODO | TODO | TODO | S/M/L |

**Mínimo:** 5 items. Foco esperado en: batch I/O, hashing/IDs, manifests CSV, estructura de notebooks, logging.

### 1.2 Adaptar (parcial; requiere cambios)

| Ruta | Qué hace originalmente | Qué cambiar para bioacústica | Esfuerzo |
|---|---|---|---|
| TODO | TODO | TODO | S/M/L |
| TODO | TODO | TODO | S/M/L |
| TODO | TODO | TODO | S/M/L |
| TODO | TODO | TODO | S/M/L |
| TODO | TODO | TODO | S/M/L |

**Foco esperado en:** schemas de metadata (añadir campos bioacústicos: `species_guess`, `dominant_band_hz`, `call_rate_hz`, `SNR_db`), pipelines de transformación.

### 1.3 Descartar (no aplicable)

| Ruta | Por qué no aplica |
|---|---|
| TODO | TODO |
| TODO | TODO |
| TODO | TODO |

**Foco esperado:** generación de texturas sonoras, priors estadísticos del dominio texture, métricas perceptuales de textura.

### 1.4 Riesgos de reciclar sin adaptar

- TODO — riesgo específico (ej.: tratar cada clip como textura homogénea → pierde estructura temporal del canto).
- TODO
- TODO

---

## 2. Repo B — `OriolFreixa/MirChordEstimationAugmentation`

**URL:** https://github.com/OriolFreixa/MirChordEstimationAugmentation
**Dominio original:** robust automatic chord estimation through realistic audio augmentation (UPF/MTG).
**Encaje conceptual con bioacústica:** **alto** para el pipeline de augmentación y splits; **bajo** para los front-ends musicales.

### 2.1 Reutilizable (alta confianza)

| Ruta | Qué hace | Cómo encaja aquí | Esfuerzo |
|---|---|---|---|
| TODO (script de convolutional reverb) | Aplica reverb con IRs | Usar con IRs de exteriores en `src/frogiso/augment/reverb.py` | S |
| TODO (script de ambient noise mix de Freesound) | Mezcla con noise externo a SNR target | Adaptar a ambient bioacústico (viento/agua/insectos) | S |
| TODO (random EQ) | EQ aleatorio suave | Usar tal cual con rangos más conservadores | S |
| TODO (compresión dinámica) | Compresión suave | Usar tal cual con ratios bajos | S |
| TODO (split por track) | Evita leakage | Renombrar a `recording_id` | S |

**Mínimo:** 5 items.

### 2.2 Adaptar (parcial)

| Ruta | Qué hace originalmente | Qué cambiar para bioacústica | Esfuerzo |
|---|---|---|---|
| TODO (front-end CQT con tuning 440) | Representación para chord estimation | Sustituir por mel/PCEN | M |
| TODO (configs YAML de augmentación) | Parametrización de chord aug | Reusar estructura YAML, cambiar rangos | S |
| TODO (training loop) | Loop genérico | Adaptar a clasificación binaria frog/no-frog | M |
| TODO (manifests de tracks) | Manejo de tracks musicales | Renombrar a recordings; añadir campos bio | S |
| TODO (evaluación chord) | Métricas armónicas | Sustituir por precision/recall/F1 binaria | S |

### 2.3 Descartar

| Ruta | Por qué no aplica |
|---|---|
| TODO (chord templates / krumhansl) | Supuestos tonales de música occidental — irrelevantes. |
| TODO (croma features) | No discrimina cantos biológicos. |
| TODO (IRs de salas/iglesias si las hay) | Alargan sílabas y distorsionan cantos; sólo IRs de exteriores. |

### 2.4 Riesgos de reciclar sin adaptar

- **Reverb agresivo** alarga sílabas y rompe la detección por energía. Limitar a IRs cortas (RT60 ≤ 1.5 s).
- **Compresión agresiva** sube el ruido al nivel del canto: degrada SNR justo al revés del objetivo. Mantener ratios ≤4, threshold ≥ -20 dBFS.
- **EQ aleatorio amplio** puede mover el centroide fuera de la banda biológica. Limitar gains a ±3 dB.
- **Mezclar ambients de Freesound sin auditar** puede meter ranas en los "negativos" → label noise. Auditoría manual obligatoria (ver `DATASET_NOTES.md §1.4`).

---

## 3. Tabla resumen — prioridades de reuso

| ID | Origen | Concepto/Archivo | Prioridad | Esfuerzo | Encaje en proyecto |
|---|---|---|---|---|---|
| R-01 | Repo B | Convolutional reverb pipeline | Alta | S | `augment/reverb.py` (Fase 7) |
| R-02 | Repo B | Ambient noise mix a SNR target | Alta | S | `augment/mix_noise.py` (Fase 7) |
| R-03 | Repo B | Split a nivel de track → recording_id | Alta | S | `datasets/splits.py` (Fase 8) |
| R-04 | Repo B | YAML configs para augmentación | Alta | S | `configs/augmentation.yaml` |
| R-05 | Repo A | Manifests CSV + hashing | Alta | S | `io/manifests.py` (Fase 1) |
| R-06 | Repo A | Estructura de notebooks EDA | Media | S | `notebooks/01_eda_*` |
| R-07 | Repo B | Random EQ + compresión suave | Media | S | `augment/eq.py`, `augment/compression.py` |
| R-08 | Repo B | Training loop con Lightning | Media | M | `models/cnn_small.py` (Fase 8) |
| R-09 | Repo A | Patrón batch I/O sobre directorios | Media | S | `io/batch.py` |
| R-10 | Repo B | Estructura `outputs/runs/<run_id>/` | Media | S | Convención global |

> Codex completa esta tabla con los items reales encontrados, manteniendo IDs estables (R-NN) para referenciarlos desde TASKS.md y DECISIONS.md.

---

## 4. Inaccesibilidad

(Vacío en el esqueleto inicial. Codex registra aquí cualquier repo/archivo no alcanzable y propone alternativa.)

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

---

## 7. Licencias de los repos originales

| Repo | Licencia detectada | Compatible con uso académico aquí | Notas |
|---|---|---|---|
| texture-dataset-curation | TODO | TODO | TODO |
| MirChordEstimationAugmentation | TODO | TODO | TODO |

(Codex completa en T-001 leyendo el LICENSE de cada repo.)
