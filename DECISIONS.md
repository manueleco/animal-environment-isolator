# DECISIONS.md

> Registro arquitectónico estilo ADR (Architecture Decision Record). Inmutable: las decisiones no se editan, se **superceden** con una nueva entrada que referencia la anterior.

**Formato por entrada:**

```
## ADR-NNN — <título corto>
- Fecha: YYYY-MM-DD
- Estado: Proposed | Accepted | Superseded by ADR-XXX | Deprecated
- Decidido por: Claude / Humano / Codex (con aprobación humana)
- Contexto: por qué surge esta decisión
- Decisión: qué se decide, con la precisión necesaria
- Alternativas descartadas: lista con razón corta
- Consecuencias: positivas y negativas
- Referencias: tickets, archivos, PRs
```

---

## ADR-001 — Pipeline incremental DSP → ML, no al revés
- **Fecha:** 2026-06-07
- **Estado:** Accepted
- **Decidido por:** Humano + Claude
- **Contexto:** Es tentador empezar con un modelo grande pre-entrenado. Necesitamos un baseline auditable y un dataset curado antes de meter ML.
- **Decisión:** Las fases 2–6 son íntegramente DSP/heurística + curación manual. ML entra a partir de la fase 8 sobre un dataset ya curado.
- **Alternativas descartadas:**
  - Empezar con BirdNET zero-shot → opaco, no transferible al ejercicio académico.
  - Pipeline end-to-end con un único notebook → sin trazabilidad.
- **Consecuencias (+):** Auditable, defendible académicamente, trazable.
- **Consecuencias (−):** Más lento de llegar a métricas finales.
- **Referencias:** [ARCHITECTURE.md §1](ARCHITECTURE.md), [ROADMAP.md](ROADMAP.md).

---

## ADR-002 — Manifests CSV con validación por schema
- **Fecha:** 2026-06-07
- **Estado:** Proposed (validar entre `pandera` y `pydantic`)
- **Decidido por:** Claude (pendiente confirmación humana)
- **Contexto:** Necesitamos manifests diffeables, inspeccionables y versionables. SQLite/Parquet son potentes pero opacos para revisión humana.
- **Decisión:** CSV como formato fuente de verdad para todos los manifests, con validación por schema en `src/frogiso/io/manifests.py`.
- **Alternativas descartadas:**
  - SQLite → no diffeable.
  - Parquet → binario, no inspeccionable a ojo.
  - JSON → más verboso para tabular.
- **Consecuencias (+):** Inspeccionables, versionables en git si caben.
- **Consecuencias (−):** No escala a millones de filas — aceptado, no estamos en ese régimen.
- **Pendiente:** elegir librería de validación (ADR-002b).

---

## ADR-003 — Split por `recording_id`, nunca por `clip_id`
- **Fecha:** 2026-06-07
- **Estado:** Accepted
- **Decidido por:** Claude + Humano
- **Contexto:** Estándar en bioacústica/MIR. Clips del mismo recording comparten condiciones acústicas; permitirlos en distintos splits infla métricas.
- **Decisión:** Todos los splits son a nivel de `recording_id`. Assertion automática verifica intersección vacía y falla el job si se rompe.
- **Alternativas descartadas:**
  - Split estratificado por clip → leakage garantizado.
  - Split temporal dentro del mismo recording → mismo problema.
- **Consecuencias (+):** Métricas honestas, transferibles.
- **Consecuencias (−):** Con pocos recordings, splits muy desbalanceados — se asume y se mitiga con augmentación.
- **Referencias:** Reciclado del concepto en `MirChordEstimationAugmentation`.

---

## ADR-004 — Synthetic data marcado y separado del dataset real
- **Fecha:** 2026-06-07
- **Estado:** Accepted
- **Decidido por:** Claude + Humano
- **Contexto:** Entrenar modelos bioacústicos con audio generado proceduralmente o por IA introduce domain shift y label noise no auditables.
- **Decisión:**
  - Synthetic vive en `data/synthetic/` con manifest separado.
  - Flag obligatorio `is_synthetic=true`.
  - Loader del dataset excluye synthetic por defecto.
  - Synthetic **prohibido** en val/test.
  - Synthetic permitido sólo para: validación del pipeline, SNR sweeps, ablations.
- **Alternativas descartadas:**
  - Mezclar synthetic con real para "ampliar dataset" → contaminación científica.
- **Consecuencias (+):** Reportes científicamente honestos.
- **Consecuencias (−):** Menos volumen de entrenamiento — aceptado.
- **Referencias:** [DATASET_NOTES.md §riesgos](DATASET_NOTES.md).

---

## ADR-005 — Documentación Markdown versionada como interfaz Claude↔Codex↔Humano
- **Fecha:** 2026-06-07
- **Estado:** Accepted
- **Decidido por:** Humano
- **Contexto:** El contexto entre sesiones de Claude/Codex no es persistente. Necesitamos una memoria externa retomable.
- **Decisión:** Sistema de docs Markdown obligatorio en root, con `HANDOFF_TO_CODEX.md` como canal principal y `ARCHITECTURE.md` con prioridad sobre el resto en caso de conflicto.
- **Alternativas descartadas:**
  - Memoria de Claude integrada → no compartida con Codex ni humano.
  - Issue tracker externo → fricción adicional.
- **Consecuencias (+):** Proyecto retomable a meses vista.
- **Consecuencias (−):** Disciplina obligatoria de actualizar docs en cada cierre de tarea.

---

## ADR-006 — Augmentación se aplica sólo a recordings de train
- **Fecha:** 2026-06-07
- **Estado:** Accepted
- **Decidido por:** Claude
- **Contexto:** Augmentar val/test infla métricas y oculta debilidades reales del modelo.
- **Decisión:** El pipeline de augmentación lee el `train_manifest.csv` y rechaza explícitamente clips cuyo `recording_id` no esté allí.
- **Alternativas descartadas:**
  - Augmentar val "para más estabilidad" → métricas no comparables con literatura.
- **Consecuencias (+):** Métricas comparables; evaluación honesta de robustez.
- **Consecuencias (−):** Val/test pueden ser pequeños — aceptado, se reporta IC.

---

## ADR-002b — Validación de manifests con `pandera`
- **Fecha:** 2026-06-07
- **Estado:** Accepted
- **Decidido por:** Claude (con luz verde implícita del humano: "si no opinas, voy con pandera").
- **Contexto:** ADR-002 dejó pendiente la elección entre `pandera` y `pydantic` para validar CSV.
- **Decisión:** `pandera` para schemas tabulares (lee directo del DataFrame, valida tipos + constraints + uniqueness + foreign keys lógicas con `Check`). `pydantic` queda reservado a configs YAML si hace falta.
- **Alternativas descartadas:** `pydantic` puro (más verboso para tabular), `cerberus` (menos mantenido), validación manual con asserts (no auditable).
- **Consecuencias (+):** Schemas declarativos legibles, integración natural con pandas.
- **Consecuencias (−):** Dependencia adicional. Aceptado.

---

## ADR-007 — PyTorch + Lightning como stack ML (no TF/JAX)
- **Fecha:** 2026-06-07
- **Estado:** Accepted
- **Decidido por:** Claude
- **Contexto:** El alumno tiene experiencia con PyTorch; ecosistema bioacústica está mayoritariamente en PyTorch; Lightning ordena training loops y logging.
- **Decisión:** Cuando se llegue a ML (Fase 8), stack = PyTorch + Lightning, con wandb opcional.
- **Alternativas descartadas:** TensorFlow, JAX, Keras puro.
- **Consecuencias:** Dependencia opcional, no instalada hasta Fase 8.

---

## ADR-008 — Codex gestiona git (commit + push directo a `main`)
- **Fecha:** 2026-06-07
- **Estado:** Accepted
- **Decidido por:** Humano
- **Contexto:** El usuario indicó explícitamente que Codex puede manejar git. El proyecto es académico de un único autor — overhead de PRs no aporta.
- **Decisión:**
  - Codex hace `git add` selectivo, `git commit` y `git push origin main` al cerrar **cada** tarea.
  - **Un commit por tarea cerrada.** Mensaje estructurado: `<tipo>(T-NNN): <título corto>` + cuerpo con cambios + referencia al ticket.
  - Tipos permitidos: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `exp` (experimento), `data` (cambio de manifests/datos).
  - **Nunca** `--force` ni `--no-verify`.
  - **Nunca** commits que mezclen tareas distintas.
  - Si una tarea es muy grande, varios commits intermedios permitidos, pero el último debe cerrar el ticket explícitamente (`Closes T-NNN`).
- **Alternativas descartadas:** PRs por tarea (overhead), commits manuales del humano (fricción).
- **Consecuencias (+):** Trazabilidad clara ticket↔commit, historial auditable.
- **Consecuencias (−):** Si Codex se equivoca, queda en historial. Mitigación: revisión humana periódica del log; nunca destructivo.
- **Referencias:** Protocolo git completo en [CODEX_PROMPTS.md §"Bloque obligatorio"](CODEX_PROMPTS.md).

---

<!-- Plantilla para próximas ADR -->
<!--
## ADR-NNN — <título>
- Fecha:
- Estado:
- Decidido por:
- Contexto:
- Decisión:
- Alternativas descartadas:
- Consecuencias:
- Referencias:
-->
