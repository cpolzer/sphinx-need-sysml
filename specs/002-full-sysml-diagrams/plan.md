# Implementation Plan: Full SysML v2 Diagram Coverage

**Branch**: `002-full-sysml-diagrams` | **Date**: 2026-05-20 | **Spec**: [spec.md](spec.md)

## Summary

Extend `sphinxcontrib-sysml` from three diagram views (bdd, ibd, req) to full SysML v2 coverage: six additional diagram directives — `needsysml-stm` (state machine), `needsysml-act` (activity), `needsysml-sd` (sequence), `needsysml-uc` (use case), `needsysml-pkg` (package), `needsysml-par` (parametric) — plus an `needsysml-alloc` allocation-matrix directive, each with a matching SVG-rendered companion (`-svg` suffix) built on the existing `sphinx-need-svg` `Needsvg` placeholder pattern. Register thirteen new SysML need types (`Transition`, `ControlFlow`, `ObjectFlow`, `Package`, `Dependency`, `UseCase`, `Actor`, `ConstraintBlock`, `ConstraintParameter`, `ValueProperty`, `BindingConnector`, `Lifeline`, `Message`) with word-like ID prefixes (`TRANS-`, `PKG-`, `USECASE-`, …) and the supporting attribute fields. Extend the existing `StateDef` / `StateUsage` types with a `pseudo_kind` field (initial / final / shallowHistory / deepHistory / choice / junction). Ship as a **two-phase release**: v1 = state machine + activity + sequence + use case + package (User Stories 1–5); v1.1 = allocation matrix + parametric (User Stories 6–7). The vehicle example is extended to demonstrate every diagram with PlantUML and SVG variants side by side, and each new directive gets a smoke test matching the existing `test_bdd_directive.py` pattern.

## Technical Context

**Language/Version**: Python ≥ 3.10 (matches existing extension; see `pyproject.toml`)

**Primary Dependencies**:
- `sphinx-needs >= 1.0` — need type / field registration, needuml Jinja context
- `sphinx >= 4.0`
- `sphinxcontrib-plantuml` — auto-layout renderer (still optional; warning emitted if absent)
- `sphinx-need-svg >= 0.3` — precise-layout renderer; optional, registers SVG variants only when present (same gating pattern as `_HAS_NEED_SVG` in `sphinxcontrib/sysml/__init__.py`)

**Storage**: N/A — Sphinx extension; all model state lives in `sphinx_needs.data.SphinxNeedsData`.

**Testing**: pytest + nox, one new `test_<directive>_directive.py` per new directive, mirroring the existing pattern (`tests/test_bdd_directive.py`, `tests/test_ibd_directive.py`, `tests/test_req_directive.py`).

**Target Platform**: Linux / macOS / Windows (pure Python; no native dependencies beyond the optional `plantuml.jar` and `Pillow` for PlantUML SVG scaling).

**Project Type**: Python library — Sphinx extension under the `sphinxcontrib.*` namespace, `flit` build backend, single package layout.

**Performance Goals**: SC-008 — full vehicle example (all ten diagram views) builds in under 30 seconds wall-clock on a developer workstation. Per-directive cost ≤ existing `needsysml-bdd` cost.

**Constraints**:
- Must remain backward-compatible with existing `001-sysml-v2-needs` feature: no rename or removal of existing types/fields/directives.
- `add_field` registration must keep the compatibility shim that already handles `add_field` vs deprecated `add_extra_option`.
- New SVG directives MUST defer rendering to `doctree-resolved` (reusing `sphinx_need_svg.directives.needsvg.Needsvg`) — calling `SphinxNeedsData.get_needs_view()` during a directive's `run()` freezes the needs registry and breaks every later directive (already fixed for `needsysml-bdd-svg` in `needsysml_svg.py`).
- SVG variants MUST gracefully degrade when `sphinx-need-svg` is not installed (don't register; the corresponding PlantUML directive still works).
- All new types follow SysML v2 naming where v2 defines them; v1-only concepts (UseCase, Actor, Lifeline, Message) keep their v1 names.

**Scale/Scope**:
- 13 new need types, ~22 new extra fields
- 7 new diagram directives + 6 SVG companions = 13 new directives
- 6 new PlantUML Jinja2 template constants in `templates.py`
- 6 new SVG Jinja2 template constants in `svg_templates.py` (new module)
- 5 new `needs_flow_configs` entries (sysml_stm, sysml_act, sysml_sd, sysml_uc, sysml_pkg, sysml_par)
- 7 new smoke-test files + 1 expanded fixture page
- ~1500 LOC new Python, ~600 LOC new docs

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

`.specify/memory/constitution.md` contains only the unfilled template (no project-specific principles ratified). No constitutional gates to enforce. The plan follows the conventions already established by feature `001-sysml-v2-needs` and by the existing codebase:

- Single-package layout (`sphinxcontrib/sysml/`) with sub-packages per concern.
- One directive per file under `sphinxcontrib/sysml/directives/`.
- Template constants colocated in `templates.py` (PlantUML) and a new `svg_templates.py` (SVG).
- One pytest file per directive.
- Backward-compatible API surface; deprecation only when explicitly approved.

Re-check after Phase 1 design: still PASS.

## Project Structure

### Documentation (this feature)

```text
specs/002-full-sysml-diagrams/
├── spec.md
├── plan.md              ← this file
├── research.md          ← Phase 0 output
├── data-model.md        ← Phase 1 output
├── quickstart.md        ← Phase 1 output
├── contracts/
│   └── sphinx-extension-api.md  ← Phase 1 output
├── checklists/
│   └── requirements.md  ← already validated
└── tasks.md             ← /speckit-tasks output (not yet created)
```

### Source Code (repository root)

```text
sphinxcontrib/
└── sysml/
    ├── __init__.py              # extended: register new types, fields, directives
    ├── config.py                # extended: SYSML_NEED_TYPES adds 13 entries
    ├── fields.py                # extended: SYSML_FIELDS adds ~22 entries
    ├── flow_configs.py          # extended: 6 new sysml_* skinparam strings
    ├── templates.py             # extended: 6 new PlantUML Jinja2 constants
    ├── svg_templates.py         # NEW: 6 SVG Jinja2 constants for SVG variants
    ├── warnings.py              # extended: per-directive warning helpers
    └── directives/
        ├── __init__.py
        ├── needsysml_bdd.py     # existing
        ├── needsysml_ibd.py     # existing
        ├── needsysml_req.py     # existing + :filter: default option
        ├── needsysml_svg.py     # existing (ibd-svg promotion lives here)
        ├── needsysml_stm.py     # NEW (PlantUML state machine)
        ├── needsysml_act.py     # NEW (PlantUML activity)
        ├── needsysml_sd.py      # NEW (PlantUML sequence)
        ├── needsysml_uc.py      # NEW (PlantUML use case)
        ├── needsysml_pkg.py     # NEW (PlantUML package)
        ├── needsysml_par.py     # NEW (PlantUML parametric, v1.1)
        ├── needsysml_alloc.py   # NEW (allocation matrix, v1.1)
        └── needsysml_svg_extra.py  # NEW: helpers shared by all -svg directives

docs/
├── conf.py
├── index.rst                    # extended: add new directive pages to toctree
├── install.rst
├── directives/
│   ├── need_types.rst           # extended: document new types
│   ├── needsysml_bdd.rst        # existing
│   ├── needsysml_ibd.rst        # existing
│   ├── needsysml_req.rst        # existing
│   ├── needsysml_svg.rst        # existing
│   ├── needsysml_stm.rst        # NEW
│   ├── needsysml_act.rst        # NEW
│   ├── needsysml_sd.rst         # NEW
│   ├── needsysml_uc.rst         # NEW
│   ├── needsysml_pkg.rst        # NEW
│   ├── needsysml_par.rst        # NEW (v1.1)
│   └── needsysml_alloc.rst      # NEW (v1.1)
└── examples/
    └── vehicle_system.rst       # extended: one section per new diagram

tests/
├── conftest.py
├── doc_test/
│   └── full_example/            # existing fixture; extended for new types
├── test_need_types.py           # extended: assert new types registered
├── test_fields.py               # extended: assert new fields registered
├── test_flow_configs.py         # extended: assert new flow configs registered
├── test_bdd_directive.py        # existing
├── test_ibd_directive.py        # existing
├── test_req_directive.py        # existing (failing test pre-dates this feature; out of scope)
├── test_stm_directive.py        # NEW
├── test_act_directive.py        # NEW
├── test_sd_directive.py         # NEW
├── test_uc_directive.py         # NEW
├── test_pkg_directive.py        # NEW
├── test_par_directive.py        # NEW (v1.1)
└── test_alloc_directive.py      # NEW (v1.1)

pyproject.toml                   # extended: version bump 0.2.4 → 0.3.0 (v1), → 0.4.0 (v1.1)
```

**Structure Decision**: Continue the established single-package extension layout. New diagram directives go one-per-file under `directives/`. Template constants stay colocated by render path (`templates.py` for PlantUML, new `svg_templates.py` for SVG) to keep imports clean and to match the existing `templates.py` convention. Tests follow the existing one-file-per-directive convention so each test can be run independently for triage.

## Complexity Tracking

No constitution violations to justify. The design follows existing patterns established in feature `001-sysml-v2-needs`; no new architecture is introduced. The thirteen new need types are a quantitative expansion, not a qualitative architectural shift.

| Decision | Why Needed | Simpler Alternative Rejected Because |
|----------|------------|-------------------------------------|
| Separate `svg_templates.py` module instead of merging into `templates.py` | Keep PlantUML and SVG concerns linearly separate; ease grep-ability when debugging one render path | Merging into `templates.py` would create one 600+ line module with two concerns |
| One directive file per new diagram (vs one mega-file) | Match the existing convention; each test imports a single small module; keeps blast radius of bugs small | A single `extra_directives.py` would couple unrelated diagrams' lifetimes and complicate testing |
| Two-phase release (v1 = stories 1–5, v1.1 = stories 6–7) | User choice (clarification Q5); ships the high-value diagrams sooner; v1.1 elements can still be registered in v1 to keep data model stable | Single big-bang release was rejected by user during clarification |

---

## Phase 0 Artifacts

- [research.md](research.md) — PlantUML syntax for stm/act/sd/uc/pkg/par, sphinx-need-svg deferred-rendering pattern, allocation matrix table-vs-grid decision, pseudostate notation, swimlane partition syntax, combined fragment syntax. All NEEDS CLARIFICATION resolved at clarify stage.

## Phase 1 Artifacts

- [data-model.md](data-model.md) — 13 new need types with locked prefixes; ~22 new fields; 6 new flow_configs entries; extension of StateDef/StateUsage with `pseudo_kind`; relationships between new types.
- [contracts/sphinx-extension-api.md](contracts/sphinx-extension-api.md) — Directive option surface for each of the 7 new diagrams + 6 SVG companions; conf.py expectations; behavior contracts for FR-016 / FR-017 / FR-018 (error handling); warning categories.
- [quickstart.md](quickstart.md) — End-to-end engineer workflow: write a state machine + activity + sequence + use case + package model, build, get rendered diagrams with clickable links in under five minutes.

## Key Design Decisions (from research)

1. **PlantUML native diagram modes for every diagram type**: PlantUML has native syntax for state machines (`@startuml … state X { } … X --> Y : trigger [guard] / effect`), activity (`@startuml :Action;`), sequence (`@startuml participant A`), use case (`@startuml actor :A: usecase (UC)`), and package (`@startuml package "X" { }`). No custom rendering needed — wrap `.. needuml::` with the appropriate body and a fresh `:config: sysml_<diagram>` skinparam, mirroring `needsysml-bdd`'s pattern.

2. **Parametric diagram is the weakest PlantUML fit**: PlantUML has no native parametric diagram mode. Use the class diagram with `<<constraint>>` stereotype + binding connectors as `..>` arrows labelled with units, similar to how `needsysml-bdd` reuses class diagrams. Acknowledge in docs that parametric fidelity is approximation-level, as IBD already is.

3. **All new SVG variants use the same `Needsvg` placeholder pattern as `needsysml-bdd-svg`**: register a `Needsvg` node + populate `env.needsvg_all_data` during `run()`, then let `process_needsvg` render at `doctree-resolved`. This avoids the "needs frozen mid-parse" failure mode that `needsysml-bdd-svg` already had to fix.

4. **`pseudo_kind` as an enum string field, not new need types**: pseudostates are kinds of states, not separate entities. Add a `pseudo_kind` string field (constrained to `initial`/`final`/`shallowHistory`/`deepHistory`/`choice`/`junction`) to StateDef/StateUsage rather than registering six new pseudostate types. Keeps the type registry small and matches how SysML v2 itself models pseudostates as a kind on State.

5. **Allocation matrix as an `<table>` not an SVG**: per FR-010 + Q3, render as a sphinx-needs-style HTML table with axis filter options. The renderer emits a `nodes.table` (docutils) so it picks up the active theme's table styling and remains queryable in PDF/ePub builds — unlike the SVG diagrams.

6. **Smoke test pattern**: every new directive gets one pytest module that builds a minimal doc fixture (`tests/doc_test/<directive>/conf.py` + `index.rst`) and asserts (a) `app.build()` returns without warnings (or with only the warnings declared by FR-016/FR-017/FR-018), (b) a fixture-defined need ID appears in the rendered doctree's astext. This mirrors `test_bdd_directive.py:test_bdd_builds_without_error`.

7. **Two-phase release packaging**: bump to `0.3.0` when v1 stories 1–5 ship. v1.1 stories 6–7 ship as `0.4.0`. Element types required by v1.1 (ConstraintBlock, ConstraintParameter, ValueProperty, BindingConnector) are still registered in v1 so users' models don't need a follow-up data-model migration when v1.1 lands — only the diagram directives appear later.

8. **`needsysml-req` gets a default filter and a `:filter:` option**: today the directive requires a positional filter argument. Phase A foundation work (see [tasks.md] when written) adds `:filter:` as an option with default `type == 'Requirement'`. Backward compatible — the positional form still works.

9. **`needsysml-ibd-svg` becomes first-class**: the inline `.. needsvg::` IBD workaround currently demonstrated in `vehicle_system.rst` is promoted to a real directive in this feature so engineers have parity between PlantUML and SVG IBD rendering.

10. **CLAUDE.md plan reference**: the `<!-- SPECKIT START -->` … `<!-- SPECKIT END -->` block in the root CLAUDE.md will be updated to reference `specs/002-full-sysml-diagrams/plan.md` so future Claude sessions discover the active plan.
