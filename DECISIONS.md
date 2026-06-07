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

## ADR-009 — Reuso por replicación de patrón, no por copia de código
- **Fecha:** 2026-06-07
- **Estado:** Accepted
- **Decidido por:** Humano
- **Contexto:** Los dos repos previos (`texture-dataset-curation`, `MirChordEstimationAugmentation`) son fuentes de inspiración arquitectónica. Copiar código arrastra deps, supuestos de dominio y bugs latentes. Lo valioso son **las ideas y la lógica**, no las implementaciones literales.
- **Decisión:**
  - **No** se clonan los repos al working tree del proyecto. Inspección remota vía GitHub web / `gh api` / WebFetch.
  - El `REUSE_REPORT.md` documenta **patrones e ideas** con: descripción, URL del archivo fuente como referencia, propuesta de cómo replicarlo idiomáticamente en `frogiso`, esfuerzo.
  - El código que entra al repo se escribe **de cero**, siguiendo nuestras convenciones (manifests pandera, ARCHITECTURE.md §4), y referencia el patrón origen vía ID `R-NN` en docstring.
  - Excepción: snippets ≤20 líneas de utilidad pura (ej. fórmula concreta) pueden copiarse citando autoría + licencia en el docstring.
- **Alternativas descartadas:**
  - Clonar y copiar archivos → arrastra deps obsoletas, supuestos de dominio musical y bugs no auditados.
  - Sub-módulo git de los repos → fricción operativa innecesaria.
- **Consecuencias (+):** Código limpio, sin deuda heredada, deps mínimas, supuestos de dominio bioacústico desde el inicio.
- **Consecuencias (−):** Reimplementar lleva algo más de tiempo. Aceptado.
- **Referencias:** [REUSE_REPORT.md](REUSE_REPORT.md), [CODEX_PROMPTS.md "PROMPT 1"](CODEX_PROMPTS.md).

---

## ADR-010 — GUI vía Hallmark + HTML estático generado, no app interactiva
- **Fecha:** 2026-06-07
- **Estado:** Accepted
- **Decidido por:** Humano + Claude
- **Contexto:** El usuario instaló la skill `hallmark` (~/.agents/skills/hallmark, v1.1.0) y quiere una interfaz gráfica. Hallmark genera HTML+CSS estático con disciplina de diseño (anti-AI-slop, tokens, accesibilidad, responsive). NO es un framework de runtime. Lo que sí encaja perfectamente con el proyecto: dashboards, A/B players, FP/FN review, landing y reporte académico.
- **Decisión:**
  - **Frontend estático Hallmark-styled** generado por Python + Jinja2 a partir de los manifests CSV.
  - Módulo nuevo `src/frogiso/web/` (templates + renderers).
  - Destino: `outputs/web/` (gitignored como salida regenerable; sólo se versionan los templates y los CSS tokens).
  - Cada fase que produce artefactos también publica su vista al frontend:
    - Fase 2 → `eda_gallery.html`
    - Fase 3 → `detections.html`
    - Fase 5 → `ab_player.html`
    - Fase 6 → `curation_browser.html` (read-only; la edición sigue en notebook).
    - Fase 8 → `eval_<run_id>.html` con FP/FN embebidos.
    - Fase 10 → `index.html` (landing) + `report.html` (reporte académico).
  - **Tokens de diseño** (`outputs/web/tokens.css`) se generan UNA VEZ vía hallmark default en T-014 y se reutilizan en todas las vistas (disciplina "Locked tokens" de Hallmark).
  - Curación interactiva permanece en notebook (ipywidgets) — no se reemplaza por una app web.
  - **NO se introduce servidor** (Streamlit/Gradio/FastAPI). Si en el futuro se quiere interactividad real, requerirá una ADR nueva.
- **Cómo invoca Codex a Hallmark:**
  - Verbo `default` para construir nuevas vistas (T-014 landing, vistas por fase).
  - Verbo `audit` para revisar vistas existentes antes del reporte final (T-101).
  - Verbo `redesign` si el humano pide cambiar estructura sin cambiar contenido.
  - Las disciplinas de Hallmark (pre-emit critique, locked tokens, mobile-responsive 320/375/414/768 px, sin chrome fake, sin métricas inventadas) son OBLIGATORIAS y aplican a todas las vistas.
- **Alternativas descartadas:**
  - Streamlit/Gradio → introduce servidor, complica reproducibilidad, no aporta sobre el caso de uso real (revisar artefactos producidos por el pipeline).
  - Notebook puro como GUI → menos pulido, no comparte design language entre vistas.
  - Static site generator de terceros (Hugo, MkDocs) → fricción de stack adicional; Jinja2 ya viene con el ecosistema Python.
- **Consecuencias (+):** Vistas coherentes y profesionales; reproducible (regenerar tras cada run); commit-friendly (templates en git, salida en outputs/); cero servidor.
- **Consecuencias (−):** No hay interactividad live (retunear thresholds desde el browser). Aceptado por ahora.
- **Referencias:** [ARCHITECTURE.md §3 (módulo web)](ARCHITECTURE.md), CODEX_PROMPTS.md "PROMPT 3 (T-014)".

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
