# EVALUATION_PLAN.md

> Plan de evaluación cuantitativa y cualitativa. **Antes** de entrenar nada, el criterio de éxito debe estar fijado aquí.

**Última actualización:** 2026-06-07

---

## 1. Niveles de evaluación

| Nivel | Qué evalúa | Cuándo |
|---|---|---|
| **DSP heurística** | ¿La detección por energía encuentra los cantos? | Fase 3–4 |
| **Denoising A/B** | ¿La versión limpia se oye mejor sin degradar la rana? | Fase 5 |
| **Curación** | Distribución, balance, ambigüedad | Fase 6 |
| **Augmentación** | ¿SNR target real coincide con el pedido? ¿Audible? | Fase 7 |
| **Clasificación ML** | Métricas estándar de clasificación binaria | Fase 8 |
| **Robustez** | Métricas estratificadas por SNR / fondo / augmentación | Fase 8/9 |
| **Cualitativa** | Escucha humana de FP/FN | Continua |

---

## 2. Métricas cuantitativas

### 2.1 Detección heurística (Fase 3–4)
- **Precision** = TP / (TP + FP), donde TP = evento que coincide en >50% con un canto real confirmado por escucha.
- **Recall** = TP / (TP + FN), sobre una grabación con anotaciones manuales de referencia.
- **Cobertura temporal**: ∑duración(TP) / ∑duración(cantos reales).
- **Coste por hora**: FP/h, útil para tunear threshold.

### 2.2 Denoising (Fase 5)
- **ΔSNR estimado** (pre vs post).
- **Spectral flatness** pre/post (proxy de musical noise).
- **PESQ / STOI** — opcional, vienen de voz pero útiles como proxy.
- **Preferencia auditiva A/B** (ver §3).

### 2.3 Clasificación ML (Fase 8)
- **Precision, Recall, F1** por clase y macro/micro.
- **Accuracy** (reportado pero **no usado como métrica principal** por desbalance).
- **ROC-AUC** y **PR-AUC**.
- **Confusion matrix** (PNG en `outputs/eval/<run_id>/`).
- **Threshold sweep** para curva PR completa.

### 2.4 Robustez (Fase 8/9)
- Métricas estratificadas por:
  - SNR estimado del clip.
  - Fondo dominante (viento, agua, insectos…).
  - Augmentación aplicada (sí/no, cuál).
  - Banda dominante.

---

## 3. Evaluación cualitativa / auditiva

### 3.1 Revisión de FP/FN
- Para cada modelo evaluado, exportar los N=20 FP y N=20 FN con mayor confianza (peores errores).
- HTML index con audio embebido + spectrogram + metadata.
- Escucha por el investigador → anotación en `EXPERIMENT_LOG.md`.

### 3.2 A/B de denoising y augmentación
- Generar HTML con pares `<audio>` aleatorizados.
- Investigador anota preferencia y notas.

### 3.3 Sanity check de augmentación
- Para N=10 clips augmentados, verificar:
  - El canto sigue siendo audible.
  - El fondo no domina absurdamente.
  - El SNR medido coincide con el target (±1 dB).

---

## 4. Criterios de éxito

### 4.1 MVP (Fase 0–6)
- ≥1 grabación procesada de extremo a extremo.
- ≥200 clips curados.
- Pipeline reproducible documentado.
- Sin métricas ML aún — éxito = funciona y se puede demostrar.

### 4.2 MVP ampliado (Fase 7–8)
- Baseline ML con **F1 macro ≥ 0.70** en test (recordings nunca vistos).
- **Sin leakage** verificable.
- Robustez mostrada en al menos 2 estratificaciones (ej. por SNR y por fondo).

### 4.3 Objetivo aspiracional (Fase 9)
- Mejora ≥3 puntos de F1 sobre baseline con técnica avanzada (embeddings/enhancement).
- O bien: demostración honesta de que no mejora y discusión de por qué.

---

## 5. Baselines

### 5.1 Baseline trivial (siempre reportar)
- **Always-positive**: predice positive siempre. F1 = 2P/(P+1) con P=precision class balance.
- **Random stratified**.
- **Majority class**.

### 5.2 Baseline heurístico
- Detector de energía en banda (sin ML) → se reporta como baseline en Fase 8.

### 5.3 Baseline sklearn
- Random Forest sobre features clásicas (MFCC stats + scikit-maad indices).

### 5.4 Baseline DL pequeño
- CNN pequeño sobre mel-spectrogram.

**Comparar todos en la misma tabla.** Sin baseline, las métricas no significan nada.

---

## 6. Experimentos comparativos planificados

| ID | Comparación | Métrica clave | Fase |
|---|---|---|---|
| CMP-01 | Threshold absoluto vs adaptativo (MAD) | Precision, Recall heurístico | 3 |
| CMP-02 | Sin denoise vs noisereduce vs Wiener | ΔSNR + preferencia A/B | 5 |
| CMP-03 | sklearn RF vs CNN pequeño | F1 macro | 8 |
| CMP-04 | Sin augmentación vs con augmentación | F1 macro + robustez por fondo | 8 |
| CMP-05 | Mel-spectrogram vs PCEN como input | F1 macro | 8 |
| CMP-06 (opcional) | Baseline vs embeddings + linear probe | F1 macro | 9 |

Cada CMP-XX genera entrada en `EXPERIMENT_LOG.md`.

---

## 7. Reproducibilidad

- Cada experimento exporta:
  - `outputs/runs/<run_id>/config.yaml` (snapshot completo).
  - `outputs/runs/<run_id>/git_sha.txt` (commit usado).
  - `outputs/runs/<run_id>/dataset_hashes.txt` (hashes de manifests usados).
  - `outputs/runs/<run_id>/metrics.csv`.
- Una persona externa con sólo `run_id` debe poder reproducir el experimento.

---

## 8. Antipatrones de evaluación (prohibidos)

- Reportar sólo accuracy en problema desbalanceado.
- Reportar métricas en train.
- Optimizar threshold sobre test.
- Augmentar val/test.
- Cherry-picking de FP/FN: el script los selecciona por confidence, no a mano.
- Comparar modelos entrenados con seeds distintas sin reportarlo.
