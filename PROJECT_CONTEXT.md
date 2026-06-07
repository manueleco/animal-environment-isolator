# PROJECT_CONTEXT.md

> Contexto vivo del proyecto. Si algo cambia aquí, debe reflejarse en `ARCHITECTURE.md` y `ROADMAP.md` cuando aplique.

**Última actualización:** 2026-06-07
**Mantenedor:** Claude (arquitecto)
**Project Owner:** Manuel (UPF — Sound and Music Computing)

---

## 1. Objetivos del proyecto

### Objetivo primario
Detectar, segmentar y mejorar perceptualmente cantos de ranas en grabaciones ambientales de campo, reduciendo lo máximo posible la presencia audible de viento, agua, insectos, aves y ruido humano.

### Objetivos secundarios
- Construir un dataset curado y reutilizable de cantos de rana con metadatos.
- Aplicar conceptos del máster (DSP, análisis tiempo-frecuencia, event detection, segmentation, denoising, augmentation, ML/source separation) a un dominio biológico real.
- Producir un pipeline reproducible que terceros puedan correr con el mismo audio y obtener los mismos resultados.
- Entregar un reporte académico defendible.

### Objetivo NO declarado (rechazo explícito)
- **No** se promete separación de fuentes perfecta. El objetivo medible es mejora de SNR perceptual (~6–12 dB) y detección robusta, no fuente limpia.

---

## 2. Motivación académica

- Máster en **Sound and Music Computing (SMC)** en la **UPF / MTG**.
- Aplicación de competencias del máster a un dominio (bioacústica) distinto del clásico MIR, demostrando transferibilidad.
- Conexión con líneas de investigación del MTG en augmentación realista, robustez de modelos y trabajo con audio de campo.
- Producto académicamente defendible: dataset curado + pipeline + baseline + reporte.

---

## 3. Contexto UPF / SMC

- El alumno tiene formación en DSP, análisis tiempo-frecuencia, MIR y experiencia con Python científico.
- Existen dos repos previos del propio autor / entorno UPF que pueden aportar componentes:
  - `manueleco/texture-dataset-curation` (dataset curation, generative).
  - `OriolFreixa/MirChordEstimationAugmentation` (augmentación realista para chord estimation, UPF/MTG).
- Auditoría detallada en [REUSE_REPORT.md](REUSE_REPORT.md).

---

## 4. Alcance actual (in-scope)

- Procesamiento batch de múltiples grabaciones ambientales.
- Generación de espectrogramas (STFT / mel / PCEN).
- Filtrado band-pass configurable por especie/preset.
- Detección heurística de eventos por energía en banda con threshold adaptativo.
- Segmentación temporal y extracción de clips con timestamps.
- Denoising clásico (noisereduce / spectral gating) con comparación A/B.
- Curación manual asistida en notebook.
- Splits train/val/test sin leakage a nivel de sesión de grabación.
- Augmentación realista (reverb con IRs de exteriores, mezcla con ambient noise, EQ suave, compresión suave).
- Generación opcional de ejemplos sintéticos controlados, etiquetados como `is_synthetic`.
- Baseline binario frog/no-frog (CNN pequeño + sklearn con features clásicas + scikit-maad).
- Evaluación cuantitativa (precision/recall/F1, confusion matrix, PR-AUC) y cualitativa (escucha A/B de FP/FN).
- Reporte académico y README reproducible.

---

## 5. Fuera de alcance (out-of-scope)

- Clasificación a nivel de especie (requiere etiquetado experto a escala).
- Separación de fuentes pretendidamente perfecta.
- Uso de modelos generativos para sintetizar cantos "convincentes" como datos de entrenamiento (ver [DATASET_NOTES.md §riesgos](DATASET_NOTES.md)).
- Despliegue en tiempo real / edge.
- App móvil o frontend web.
- Inferencia masiva sobre datasets públicos (Xeno-canto, etc.) sin auditoría previa.
- Fine-tuning de modelos pre-entrenados pesados (BirdNET/Perch) — sólo se contempla uso de embeddings en fase avanzada opcional.

---

## 6. Definiciones importantes

| Término | Definición operativa en este proyecto |
|---|---|
| **Recording** | Archivo de audio crudo de una sesión de grabación. ID = sha256(path)[:12]. |
| **Event** | Intervalo temporal `[start_s, end_s]` detectado por la heurística como candidato a canto. Vive en `metadata/events.csv`. |
| **Clip** | Archivo WAV exportado a partir de un event con padding. Unidad de curación y entrenamiento. |
| **Detección** | Localizar **cuándo** ocurre algo que parece canto. No implica clasificación. |
| **Segmentación** | Delimitar onset/offset preciso del evento. Refinamiento de la detección. |
| **Band-pass filtering** | Filtro lineal sobre la señal cruda; no es denoising. |
| **Denoising** | Reducción de ruido espectralmente informada (gating, Wiener). Puede introducir artefactos. |
| **Source separation** | Separar señales mezcladas en componentes. **Aspiracional**, no garantizado. |
| **Augmentation realista** | Aplicar transformaciones acústicas plausibles (reverb, ambient mix, EQ, compresión) a datos reales etiquetados, sólo en train. |
| **Synthetic** | Audio generado proceduralmente (osciladores, AM/FM, trenes de pulsos). Etiqueta obligatoria. **Nunca** sustituye datos reales en train final. |
| **Leakage** | Que clips del mismo recording acaben en distintos splits. **Prohibido**. |

---

## 7. Riesgos técnicos

| Riesgo | Mitigación |
|---|---|
| Solapamiento espectral rana–insecto–ave | Band-pass por especie + validación auditiva + ML como fallback. |
| Ruido de banda ancha (agua, viento) inmune a band-pass | Spectral gating + reportar honestamente los límites. |
| Falsos positivos altos en heurística | Curación manual obligatoria antes de entrenar. |
| Dataset pequeño | Augmentación realista + reportar IC de métricas. |
| Sesgo de fondo en augmentación | Diversidad de IRs y ambients + reportar manifest de qué se mezcló. |
| Leakage entre splits | Split estricto por `recording_id` + assertion automática. |
| Domain shift de datos sintéticos | Synthetic sólo para validación de pipeline / SNR sweeps, jamás como única fuente. |
| Pérdida de contexto entre sesiones | Sistema de docs Markdown + `HANDOFF_TO_CODEX.md`. |

Ver detalle en [DECISIONS.md](DECISIONS.md) y [DATASET_NOTES.md](DATASET_NOTES.md).

---

## 8. Riesgos no técnicos

- **Licencias** de IRs y ambient noise (Freesound, etc.) — manifest obligatorio en `data/irs/LICENSES.md` y `data/ambient/LICENSES.md` antes de usarlos.
- **Ética científica** — si se publicara el dataset, declarar explícitamente proporciones real/aumentado/sintético.

---

## 9. Estado general

**Fase activa:** Fase 0 — Auditoría de repos previos + setup de documentación.
**Próximo hito:** REUSE_REPORT.md completo + Fase 1 (estructura del repo) implementada.
**Bloqueos actuales:** Ninguno.

Detalle en [ROADMAP.md](ROADMAP.md) y [HANDOFF_TO_CODEX.md](HANDOFF_TO_CODEX.md).
