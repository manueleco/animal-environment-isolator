# EXPERIMENT_LOG.md

> Bitácora experimental. Cada experimento es una entrada inmutable: si se repite con otros parámetros, **nueva entrada**.

**Formato:**

```
## EXP-NNN — <título corto>
- Fecha: YYYY-MM-DD
- Autor: Humano / Codex
- Fase: 0–10
- Hipótesis: una frase
- Parámetros: bloque YAML o lista
- Dataset: split, número de clips, fuente
- Resultado: tabla / métricas / observaciones
- Observaciones cualitativas: qué se oye/se ve
- Próximo paso: acción concreta
- Run artifacts: rutas a `outputs/runs/<run_id>/`, checkpoints, figuras
```

---

<!--
## EXP-000 — Ejemplo (NO usar como real)
- Fecha: 2026-06-07
- Autor: Claude (ejemplo)
- Fase: 3
- Hipótesis: El threshold adaptativo mediana+3·MAD reduce falsos positivos vs threshold absoluto en grabaciones con ruido variable.
- Parámetros:
  ```yaml
  band: [1500, 4000]
  frame_ms: 30
  hop_ms: 10
  smoothing_ms: 50
  k_mad: 3
  min_duration_ms: 80
  ```
- Dataset: 1 grabación (recording_id=abc123def456, 12 min, charca nocturna).
- Resultado: 142 eventos detectados; 118 validados manualmente como positivos → precision ≈ 0.83.
- Observaciones cualitativas: FP concentrados en insectos sostenidos en banda alta; ningún FN evidente al revisar el espectrograma.
- Próximo paso: probar k_mad=4 sobre la misma grabación para reducir FP de insectos.
- Run artifacts: outputs/runs/20260607_153000_abc/
-->

---

## EXP-001 — (a poblar al ejecutar el primer experimento)

(vacío; será la primera entrada real)
