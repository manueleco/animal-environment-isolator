# Animal Environment Isolator

Plataforma reproducible de bioacústica para detección, segmentación y aislamiento (enhancement) de cantos de ranas en grabaciones ambientales.

Diseñada para evolucionar desde **DSP clásico** hasta **machine learning** y **source separation** específica de dominio, manteniendo toda la arquitectura documentada para colaboración continua entre Claude (arquitecto), Codex (implementador) e investigador humano (UPF — Sound and Music Computing).

---

## Filosofía

Prioridades, en orden estricto:

1. **Reproducibilidad** — todo configurable por YAML, seeds explícitas, manifests CSV.
2. **Trazabilidad** — cada artefacto (clip, spectrograma, modelo) tiene origen registrado.
3. **Interpretabilidad** — la heurística DSP es la baseline auditable; ML viene después.
4. **Robustez experimental** — splits sin leakage, augmentación etiquetada, evaluación honesta.
5. **Calidad de dataset** — curación manual asistida antes que volumen ciego.

Por encima de complejidad innecesaria, modelos grandes y optimización prematura.

---

## Sistema de documentación

Toda la información crítica del proyecto vive en estos archivos Markdown. **Si algún archivo entra en conflicto con otro, [ARCHITECTURE.md](ARCHITECTURE.md) tiene prioridad.**

| Archivo | Propósito |
|---|---|
| [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md) | Objetivos, motivación, alcance, riesgos. |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Arquitectura, pipeline, convenciones, decisiones estructurales. |
| [ROADMAP.md](ROADMAP.md) | Fases, dependencias, MVP, estado. |
| [TASKS.md](TASKS.md) | Checklist operativa con IDs y criterios de aceptación. |
| [DECISIONS.md](DECISIONS.md) | Registro arquitectónico estilo ADR. |
| [EXPERIMENT_LOG.md](EXPERIMENT_LOG.md) | Hipótesis, parámetros y resultados de cada experimento. |
| [DATASET_NOTES.md](DATASET_NOTES.md) | Fuentes, versionado, leakage, convenciones de nombres. |
| [EVALUATION_PLAN.md](EVALUATION_PLAN.md) | Métricas, baselines, evaluación auditiva y visual. |
| [CODEX_PROMPTS.md](CODEX_PROMPTS.md) | Prompts oficiales por fase para Codex. |
| [HANDOFF_TO_CODEX.md](HANDOFF_TO_CODEX.md) | Canal principal Claude → Codex. Leer SIEMPRE primero. |
| [REUSE_REPORT.md](REUSE_REPORT.md) | Auditoría de los dos repos previos: qué reciclar, qué descartar. |

---

## Roles

- **Claude** — Arquitecto, Technical Lead, Research Supervisor, Documentation Manager. Mantiene la coherencia y escribe los prompts. **No implementa.**
- **Codex** — Implementador. Lee la documentación, ejecuta los prompts oficiales, actualiza `TASKS.md` y `HANDOFF_TO_CODEX.md` al cerrar cada tarea.
- **Humano (Manuel)** — Investigador / Revisor / Product Owner. Aprueba decisiones de alcance, curación final, dirección académica.

---

## Cómo retomar el proyecto (en una semana o en 6 meses)

1. Abrir [HANDOFF_TO_CODEX.md](HANDOFF_TO_CODEX.md) — dice exactamente dónde quedó el proyecto.
2. Leer [ROADMAP.md](ROADMAP.md) para ver la fase activa.
3. Leer [TASKS.md](TASKS.md) para ver la tarea siguiente.
4. Si hay dudas estructurales, consultar [ARCHITECTURE.md](ARCHITECTURE.md).

---

## Stack

Python ≥3.10 · librosa · scipy · soundfile · numpy · pandas · matplotlib · noisereduce · scikit-maad · scikit-learn · pyyaml · tqdm · click · (opcional) PyTorch + Lightning, wandb.
