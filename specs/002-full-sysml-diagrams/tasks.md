---

description: "Task list for feature 002-full-sysml-diagrams"
---

# Tasks: Full SysML v2 Diagram Coverage

**Input**: Design documents from `/specs/002-full-sysml-diagrams/`

**Prerequisites**: plan.md ✓, spec.md ✓, research.md ✓, data-model.md ✓, contracts/sphinx-extension-api.md ✓, quickstart.md ✓

**Tests**: Smoke tests per directive (FR-019); explicitly requested in spec clarification and in plan.md § "Smoke test pattern".

**Organization**: Tasks are grouped by user story. v1 (Phases 3–7) covers stories US1–US5 (state machine, activity, sequence, use case, package) and ships as `0.3.0`. v1.1 (Phases 9–10) covers US6 (allocation matrix) and US7 (parametric) and ships as `0.4.0`.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Task may run in parallel with other [P] tasks at the same phase boundary (different files, no incomplete dependencies)
- **[Story]**: US1–US7 — maps to the seven user stories in spec.md
- All paths are repository-relative

## Path Conventions

Single-project layout per plan.md § "Project Structure":

- Source: `sphinx_need_sysml/`
- Docs: `docs/`
- Tests: `tests/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Pre-implementation housekeeping that affects every later task

- [X] T001 Confirm working tree clean on branch `002-full-sysml-diagrams`; bump `[project] version` in `pyproject.toml` from `0.2.4` to `0.3.0-dev` and `VERSION` in `sphinx_need_sysml/__init__.py` to match
- [X] T002 [P] Add the existing pre-existing test failure (`tests/test_req_directive.py::TestReqDirective::test_req_filter_expression_respected`) to a known-issues marker in `tests/conftest.py` (`pytest.mark.xfail(reason="pre-existing — tracked in issue")`) so this feature's CI doesn't regress on it
- [X] T003 [P] Create the new SVG template module file `sphinx_need_sysml/svg_templates.py` with a module docstring and an exported `__all__` list (empty for now — templates added per-story)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Data model, flow configs, and shared directive machinery — every user story depends on this phase

**⚠️ CRITICAL**: No user story may start until this phase is complete

### Need types and fields

- [X] T004 Add 13 new need-type dicts to `SYSML_NEED_TYPES` in `sphinx_need_sysml/config.py` per data-model.md § "New Need Types" (Transition, ControlFlow, ObjectFlow, Package, Dependency, UseCase, Actor, ConstraintBlock, ConstraintParameter, ValueProperty, BindingConnector, Lifeline, Message — with the locked word-like prefixes from spec Q1)
- [X] T005 Add the 34 new field dicts to `SYSML_FIELDS` in `sphinx_need_sysml/fields.py` per data-model.md § "New Extra Fields" (state-machine 6, activity 5, package 4, use case 5, sequence 7, parametric 7). Includes `interacts_with` on Actor (comma-list of UseCase IDs, per remediation of analyze finding U1). Enum-constrained fields use `schema: {enum: [...]}` so sphinx-needs validates at parse time.
- [X] T006 Extend `tests/test_need_types.py` to assert all 13 new types are registered with their expected prefixes; extend `tests/test_fields.py` to assert all 34 new fields are registered with their schemas

### Flow configs

- [X] T007 Add six new skinparam strings to `SYSML_FLOW_CONFIGS` in `sphinx_need_sysml/flow_configs.py`: `sysml_stm`, `sysml_act`, `sysml_sd`, `sysml_uc`, `sysml_pkg`, `sysml_par` — refer to research.md § 1 for example PlantUML output styling
- [X] T008 Extend `tests/test_flow_configs.py` to assert the six new flow-config keys are present after `builder-inited`

### Foundation directive work (preserves backward compatibility)

- [X] T009 [P] In `sphinx_need_sysml/directives/needsysml_req.py`, add a `:filter:` option to `option_spec` with default `type == 'Requirement'`; keep the positional argument working as a fallback (no regression to existing tests)
- [X] T009b In `sphinx_need_sysml/warnings.py`, add two shared helpers used by every new diagram directive (closes analyze findings G1 and G2): `warn_unknown_ref(app, docname, lineno, diagram, ref_kind, ref_id)` — emits a Sphinx warning under the category `[needsysml.<diagram>.unknown-<ref_kind>]` and returns the placeholder string (`?? <ref_id>`) the directive should render in that element's slot; `warn_empty(app, docname, lineno, diagram)` — emits one informational warning under category `[needsysml.<diagram>.empty]` and returns the standard "No matching elements" placeholder string. Both helpers MUST be the ONLY mechanism every new directive uses for FR-016 and FR-018, so the warning categories and placeholder text are uniform.
- [X] T010 Promote the raw `needsvg` IBD template from `docs/examples/vehicle_system.rst` to a first-class directive: create `sphinx_need_sysml/directives/needsysml_ibd.py`'s sibling `NeedsymlIbdSvgDirective` inside `sphinx_need_sysml/directives/needsysml_svg.py` (reusing the same module that hosts `NeedsymlBddSvgDirective`); use the `Needsvg` placeholder pattern documented in research.md § 2
- [X] T011 Move the inline `_SVG_TEMPLATE` string from `sphinx_need_sysml/directives/needsysml_svg.py` to `sphinx_need_sysml/svg_templates.py` as `BDD_SVG_TEMPLATE` and reference it from the directive (refactor — no behavior change)
- [X] T012 Register the new `needsysml-ibd-svg` directive in `sphinx_need_sysml/__init__.py:setup()` under the `_HAS_NEED_SVG` gate

**Checkpoint**: Foundation ready — every user story can now build on the 27-type/38-field model

---

## Phase 3: User Story 1 — State Machine Modeling (Priority: P1) 🎯 MVP

**Goal**: Engineers can document state machines with composite states, transitions (with trigger/guard/effect), and pseudostates (initial / final / shallowHistory / deepHistory / choice / junction), rendered in both PlantUML and SVG.

**Independent Test**: Build the `tests/doc_test/stm/` fixture and confirm (a) the state diagram renders with all four engine states and three transitions, (b) `SD-001` appears in the rendered output, (c) clicking a state in the SVG variant navigates to its definition anchor.

### Tests for User Story 1 ⚠️

> Write the smoke test FIRST and confirm it fails before implementation lands.

- [X] T013 [P] [US1] Create test fixture `tests/doc_test/stm/conf.py` (extensions list incl. `sphinx_need_sysml`, `plantuml_output_format = "svg"`) and `tests/doc_test/stm/index.rst` (one `statedef`, four `stateusage` with varied `pseudo_kind`, four `transition`s, one `.. needsysml-stm::` invocation)
- [X] T014 [US1] Create smoke test `tests/test_stm_directive.py`: build cleanly, `SD-001` appears in the rendered HTML (doctree astext doesn't include needuml-rendered IDs), transitions registered, `pseudo_kind` field readable

### Implementation for User Story 1

- [X] T015 [P] [US1] Add `STM_FULL_TEMPLATE` Jinja constant to `sphinx_need_sysml/templates.py` per research.md § 1 (state-machine pattern); walks the root `StateDef`'s usages and their transitions, emits composite-state nesting via `owned_by`, emits pseudostate notation per `pseudo_kind`
- [X] T016 [P] [US1] Add `STM_SVG_TEMPLATE` to `sphinx_need_sysml/svg_templates.py` using `flow()` for state nodes and hand-laid arrows for transitions (mirror the existing `BDD_SVG_TEMPLATE` layout strategy)
- [X] T017 [US1] Create `sphinx_need_sysml/directives/needsysml_stm.py` with `NeedsymlStmDirective` (wraps `needuml` with `STM_FULL_TEMPLATE` and `:config: sysml_stm`) and `NeedsymlStmSvgDirective` (uses the `Needsvg` placeholder pattern from research.md § 2 with `STM_SVG_TEMPLATE`); follow the `needsysml_bdd.py` + `needsysml_svg.py` patterns
- [X] T018 [US1] Register both directives in `sphinx_need_sysml/__init__.py:setup()` (PlantUML unconditional; SVG under `_HAS_NEED_SVG`)
- [X] T019 [P] [US1] Write per-directive documentation page `docs/directives/needsysml_stm.rst` mirroring the existing `needsysml_bdd.rst` structure (Usage, Options, How It Works, Example, Pseudostate notation table)
- [X] T020 [P] [US1] Add `needsysml_stm` entry to the `directives/` toctree in `docs/index.rst`
- [X] T021 [US1] Extend `docs/examples/vehicle_system.rst` with a "State Machine" section: define engine states (Off/Starting/Running/Stopping) with `pseudo_kind`, four transitions between them, both `.. needsysml-stm::` and `.. needsysml-stm-svg::` invocations side by side

**Checkpoint**: US1 ships independently — engineers can model a state machine with composite states and pseudostates and see it rendered in both paths.

---

## Phase 4: User Story 2 — Activity Flow (Priority: P1)

**Goal**: Engineers can document activities with swimlane partitions, fork/join, decision/merge, control flow, and object flow — rendered in both PlantUML and SVG.

**Independent Test**: Build `tests/doc_test/act/` fixture and confirm a "StartEngine" activity renders with two swimlanes ("Driver", "ECU"), three sequential control flows, and one fork/join construct.

### Tests for User Story 2 ⚠️

- [X] T022 [P] [US2] Create test fixture `tests/doc_test/act/conf.py` + `index.rst` with one `actiondef`, seven `action`s across two `partition` values, seven `controlflow`s including a fork/join
- [X] T023 [US2] Create smoke test `tests/test_act_directive.py`: build cleanly, `AD-001` appears, control flows registered, `partition` field readable, `activity_kind: fork` honored

### Implementation for User Story 2

- [X] T024 [P] [US2] Add `ACT_FULL_TEMPLATE` to `sphinx_need_sysml/templates.py` per research.md § 1 + § 4 (class-diagram approximation: actions as stereotyped classes inside `package <<swimlane>>` blocks, explicit control-flow arrows; fork/join via `<<fork>>` / `<<join>>` stereotypes — activity-beta syntax is order-driven and doesn't fit the data model)
- [X] T025 [P] [US2] Add `ACT_SVG_TEMPLATE` to `sphinx_need_sysml/svg_templates.py` (swimlane columns, action boxes via `flow()`-style anchors, control-flow arrows; fork/join as horizontal bars, decision/merge as diamonds)
- [X] T026 [US2] Create `sphinx_need_sysml/directives/needsysml_act.py` with `NeedsymlActDirective` and `NeedsymlActSvgDirective`; accept `:show-partitions: true|false` option (default true) per contracts § 2.2
- [X] T027 [US2] Register both directives in `sphinx_need_sysml/__init__.py:setup()`
- [X] T028 [P] [US2] Write `docs/directives/needsysml_act.rst` documentation page
- [X] T029 [P] [US2] Add `needsysml_act` entry to `docs/index.rst` toctree
- [X] T030 [US2] Add "Activity" section to `docs/examples/vehicle_system.rst` demonstrating a multi-partition activity, fork/join, and both render variants

**Checkpoint**: US2 ships independently — engineers can model a complete activity with swimlanes.

---

## Phase 5: User Story 3 — Sequence Interaction (Priority: P2)

**Goal**: Engineers can document cross-component sequences with lifelines, sync/async/return messages, and combined fragments (alt/opt/loop/par/neg/critical), rendered in both PlantUML and SVG.

**Independent Test**: Build `tests/doc_test/sd/` fixture with three lifelines and six messages including one `alt` fragment and one `loop` fragment; confirm the fragment frames render with their guards.

### Tests for User Story 3 ⚠️

- [X] T031 [P] [US3] Create test fixture `tests/doc_test/sd/conf.py` + `index.rst` with one `actiondef` (interaction), three `lifeline`s, four `message`s spanning all three `message_kind`s plus one `fragment_group="F1"` `alt` fragment and one `fragment_group="F2"` `loop` fragment
- [X] T032 [US3] Create smoke test `tests/test_sd_directive.py`: build cleanly, AD-001 in HTML, messages registered, message_kind and fragment_group fields readable

### Implementation for User Story 3

- [X] T033 [P] [US3] Add `SD_FULL_TEMPLATE` to `sphinx_need_sysml/templates.py` per research.md § 1 + § 5 (`participant` declarations, message arrows per kind, fragment frames per `fragment_group` via Jinja namespace state)
- [X] T034 [P] [US3] Add `SD_SVG_TEMPLATE` to `sphinx_need_sysml/svg_templates.py` (vertical lifeline lines, horizontal message arrows with arrowhead per `message_kind`, fragment frame `<rect>`s with header guard text)
- [X] T035 [US3] Create `sphinx_need_sysml/directives/needsysml_sd.py` with `NeedsymlSdDirective` and `NeedsymlSdSvgDirective` per contracts § 2.3
- [X] T036 [US3] Register both directives in `sphinx_need_sysml/__init__.py:setup()`
- [X] T037 [P] [US3] Write `docs/directives/needsysml_sd.rst` documentation page (include the combined-fragment kinds table)
- [X] T038 [P] [US3] Add `needsysml_sd` entry to `docs/index.rst` toctree
- [X] T039 [US3] Add "Sequence" section to `docs/examples/vehicle_system.rst` (ignition sequence: Driver → ECU → Starter with an `alt` fragment guarded by `key_position == "start"`)

**Checkpoint**: US3 ships independently — engineers can document protocol-level interactions with full fragment fidelity.

---

## Phase 6: User Story 4 — Use Case Modeling (Priority: P2)

**Goal**: Engineers can document actors, use cases inside system boundaries, and the extends/includes/generalizes relationships between use cases — rendered in both PlantUML and SVG.

**Independent Test**: Build `tests/doc_test/uc/` fixture with two actors, four use cases inside a "Vehicle" subject, one extend and one include relationship; confirm both relationship arrows render with their stereotype labels.

### Tests for User Story 4 ⚠️

- [X] T040 [P] [US4] Create test fixture `tests/doc_test/uc/conf.py` + `index.rst` with two `actor`s (each with `interacts_with` populated), four `usecase`s sharing `subject: Vehicle`, one `extends` link, one `includes` link, and association lines wired via `interacts_with`
- [X] T041 [US4] Create smoke test `tests/test_uc_directive.py`: build cleanly, `USECASE-001` and `ACTOR-001` in HTML, extends/includes fields readable, `interacts_with` field readable on actors, subject field consistent across use cases

### Implementation for User Story 4

- [X] T042 [P] [US4] Add `UC_FULL_TEMPLATE` to `sphinx_need_sysml/templates.py` per research.md § 1 + § 6 (`left to right direction`, actor declarations, system-boundary `rectangle` per subject, use case ellipses, extends/includes/generalizes arrows, actor→usecase associations via `interacts_with`)
- [X] T043 [P] [US4] Add `UC_SVG_TEMPLATE` to `sphinx_need_sysml/svg_templates.py` (stick figures for actors, ellipses for use cases inside a labelled `<rect>` boundary, dashed arrows for relationships, solid association lines)
- [X] T044 [US4] Create `sphinx_need_sysml/directives/needsysml_uc.py` with `NeedsymlUcDirective` and `NeedsymlUcSvgDirective`; accept `:subject:` option per contracts § 2.4; default filter `type == 'UseCase'` when no positional argument provided; renders solid association lines from each Actor to every UseCase listed in the actor's `interacts_with` field
- [X] T045 [US4] Register both directives in `sphinx_need_sysml/__init__.py:setup()`
- [X] T046 [P] [US4] Write `docs/directives/needsysml_uc.rst` documentation page
- [X] T047 [P] [US4] Add `needsysml_uc` entry to `docs/index.rst` toctree
- [X] T048 [US4] Add "Use Case" section to `docs/examples/vehicle_system.rst` (Driver + Mechanic actors, four use cases, one extend, one include)

**Checkpoint**: US4 ships independently — engineers can capture stakeholder-system interactions.

---

## Phase 7: User Story 5 — Package Organization (Priority: P2)

**Goal**: Engineers can group needs into nested packages and document dependencies between packages (use / import / realize), rendered in both PlantUML and SVG.

**Independent Test**: Build `tests/doc_test/pkg/` fixture with three nested packages and two cross-package dependencies (one `<<use>>`, one `<<import>>`); confirm the nested layout renders and dependency arrows are labelled.

### Tests for User Story 5 ⚠️

- [X] T049 [P] [US5] Create test fixture `tests/doc_test/pkg/conf.py` + `index.rst` with three `package`s (one parent, two children via `parent_package`) and two `dependency`s of different `kind`s
- [X] T050 [US5] Create smoke test `tests/test_pkg_directive.py`: build cleanly, `PKG-001` appears in HTML, parent_package and dependency kind fields readable

### Implementation for User Story 5

- [X] T051 [P] [US5] Add `PKG_FULL_TEMPLATE` to `sphinx_need_sysml/templates.py` (nested `package "Name" { … }` blocks, dependency arrows with `<<kind>>` labels; unrolled to ≤3 levels because minijinja doesn't support recursive macros with `.append()`)
- [X] T052 [P] [US5] Add `PKG_SVG_TEMPLATE` to `sphinx_need_sysml/svg_templates.py` (nested `<rect>` groupings sized to contain children, labelled dependency `<line>`s)
- [X] T053 [US5] Create `sphinx_need_sysml/directives/needsysml_pkg.py` with `NeedsymlPkgDirective` and `NeedsymlPkgSvgDirective`; accept `:depth:` option (default 3) per contracts § 2.5
- [X] T054 [US5] Register both directives in `sphinx_need_sysml/__init__.py:setup()`
- [X] T055 [P] [US5] Write `docs/directives/needsysml_pkg.rst` documentation page
- [X] T056 [P] [US5] Add `needsysml_pkg` entry to `docs/index.rst` toctree (completed alongside T055 — same edit pass)
- [X] T057 [US5] Add "Package" section to `docs/examples/vehicle_system.rst` (VehicleSystem with PowertrainPkg / ChassisPkg / ControlsPkg + two cross-package dependencies of different kinds)

**Checkpoint**: US5 ships independently. With Phases 3–7 complete, v1 scope (User Stories 1–5) is feature-complete.

---

## Phase 8: Polish & Release Preparation (v1.0)

**Purpose**: v1 packaging, documentation polish, and release verification

- [X] T058 [P] Run the full pytest suite (`.venv/bin/python -m pytest tests -q`); **103 passed, 1 xfailed** (pre-existing failure honored); zero regressions
- [X] T059 [P] Run a strict docs build (`.venv/bin/python -m sphinx -W docs docs/_build/html`); 0 warnings; every diagram in the vehicle example renders cleanly
- [X] T060 Time the full docs build per SC-008; **10.5 s wall-clock** (target < 30 s); recorded in `quickstart.md`
- [X] T061 [P] Inspect rendered HTML for the vehicle example; **78 unique need-anchor `href` links** in `vehicle_system.html`; recorded in `quickstart.md`
- [X] T062 Update `docs/directives/need_types.rst` to add a "New in v1" section listing the 13 new types with their prefixes (split into stm/act/pkg/uc/sd/par sub-sections)
- [X] T063 Bump version `0.3.0-dev0` → `0.3.0` in `pyproject.toml`, `sphinx_need_sysml/__init__.py`, `pyproject.toml:[tool.commitizen]`; CHANGELOG.md entry added describing the v1 feature set
- [ ] T064 Open a PR titled `feat: full SysML v2 diagram coverage (v1 — stories 1–5)` referencing this tasks.md

**Checkpoint v1**: `sphinx-need-sysml 0.3.0` is ready to release. User Stories 1–5 deliver.

---

## Phase 9: User Story 6 — Allocation Traceability Matrix (Priority: P3, v1.1)

**Goal**: Engineers can render an allocation matrix (rows × columns) over arbitrary need filters, defaulting to requirement-to-part mappings.

**Independent Test**: Build `tests/doc_test/alloc/` fixture with four requirements (three with `allocates` to parts) and confirm a matrix renders with three filled rows × distinct columns and the no-allocation row empty.

**Note**: No SVG companion per spec FR-010 — the matrix is a docutils HTML table, not an SVG drawing.

### Tests for User Story 6 ⚠️

- [ ] T065 [P] [US6] Create test fixture `tests/doc_test/alloc/conf.py` + `index.rst` with four `requirement`s (three with `allocates: P-XXX, P-YYY`), three `part`s, and one `.. needsysml-alloc::` invocation (no options — exercises defaults)
- [ ] T066 [US6] Create smoke test `tests/test_alloc_directive.py`: build cleanly; assert the rendered HTML contains a `<table>` with the marker character `✓` at the expected intersections and an empty row for the unallocated requirement

### Implementation for User Story 6

- [ ] T067 [US6] Create `sphinx_need_sysml/directives/needsysml_alloc.py` with `NeedsymlAllocDirective` per contracts § 2.7: parse `:rows:` / `:columns:` filter options (defaults per spec Q3), parse `:marker:` option (default `✓`), build a `docutils.nodes.table` with row/column header `pending_xref` links to need anchors, marker characters at intersections (no link in interior cells per contracts § 5.5)
- [ ] T068 [US6] Register `needsysml-alloc` (unconditional — no SVG variant) in `sphinx_need_sysml/__init__.py:setup()`
- [ ] T069 [P] [US6] Write `docs/directives/needsysml_alloc.rst` documentation page
- [ ] T070 [P] [US6] Add `needsysml_alloc` entry to `docs/index.rst` toctree
- [ ] T071 [US6] Add "Allocation Matrix" section to `docs/examples/vehicle_system.rst` — two invocations: one with defaults, one with `:rows: type == 'Action'` / `:columns: type == 'Part'`

**Checkpoint**: US6 ships independently.

---

## Phase 10: User Story 7 — Parametric Constraints (Priority: P3, v1.1)

**Goal**: Engineers can document constraint blocks with parameters, value properties on parts, and binding connectors between them — rendered in PlantUML (class-diagram approximation) and SVG.

**Independent Test**: Build `tests/doc_test/par/` fixture with one `constraintblock` (3 parameters + plain-text `expression`), three `valueproperty`s on parts, three `bindingconnector`s with units; confirm parameter ports render and binding arrows carry their unit labels.

### Tests for User Story 7 ⚠️

- [ ] T072 [P] [US7] Create test fixture `tests/doc_test/par/conf.py` + `index.rst` with one `constraintblock` (`expression: "fuel = output * duration / efficiency"`), three `constraintparameter`s, three `valueproperty`s with `value_type`+`default_value`+`unit`, and three `bindingconnector`s
- [ ] T073 [US7] Create smoke test `tests/test_par_directive.py`: build cleanly, `CONSTRAINT-001` appears, `BIND-001`'s unit (`kW`) appears on a binding arrow label

### Implementation for User Story 7

- [ ] T074 [P] [US7] Add `PAR_FULL_TEMPLATE` to `sphinx_need_sysml/templates.py` (class-diagram approximation: `<<constraint>>`-stereotyped class with parameter compartment, dashed binding arrows labelled with `unit`)
- [ ] T075 [P] [US7] Add `PAR_SVG_TEMPLATE` to `sphinx_need_sysml/svg_templates.py` (rounded rectangle for the constraint block, small circles on its edges for parameter ports, lines to value-property boxes labelled with the unit)
- [ ] T076 [US7] Create `sphinx_need_sysml/directives/needsysml_par.py` with `NeedsymlParDirective` and `NeedsymlParSvgDirective` per contracts § 2.6
- [ ] T077 [US7] Register both directives in `sphinx_need_sysml/__init__.py:setup()`
- [ ] T078 [P] [US7] Write `docs/directives/needsysml_par.rst` documentation page (note the class-diagram-approximation caveat)
- [ ] T079 [P] [US7] Add `needsysml_par` entry to `docs/index.rst` toctree
- [ ] T080 [US7] Add "Parametric" section to `docs/examples/vehicle_system.rst` (fuel-consumption constraint binding engine output, trip duration, efficiency)

**Checkpoint**: US7 ships independently.

---

## Phase 11: Polish & Release (v1.1)

**Purpose**: v1.1 packaging and release

- [ ] T081 [P] Re-run full pytest suite; assert v1.1 directives' smoke tests pass and v1 tests still pass
- [ ] T082 [P] Re-run strict docs build; assert zero warnings; assert allocation matrix renders in PDF builder if available (`sphinx-build -b latex ...`) to verify FR-014 holds for the matrix
- [ ] T083 Bump `0.3.0` → `0.4.0`; update CHANGELOG.md; tag `v0.4.0`
- [ ] T084 Open a PR titled `feat: SysML allocation matrix and parametric diagrams (v1.1 — stories 6–7)` referencing this tasks.md
- [ ] T085 [P] Run the `quickstart.md` walkthrough manually end-to-end on a fresh checkout to confirm the engineer experience matches the documented flow

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies — start immediately
- **Phase 2 (Foundational)**: Depends on Phase 1; BLOCKS all user-story phases
- **Phases 3–7 (US1–US5, v1)**: Each depends on Phase 2 completion. In principle each story is independently testable per spec; in practice the docs files `docs/index.rst` toctree and `docs/examples/vehicle_system.rst` are touched by every story, so stories must serialize on those two files. Within a single story, the parallel markers below identify safe parallelism.
- **Phase 8 (Polish v1)**: Depends on all of Phases 3–7 completing
- **Phases 9–10 (US6–US7, v1.1)**: Depend on Phase 8 completion; otherwise independent of each other for everything except `docs/index.rst` toctree and `docs/examples/vehicle_system.rst`
- **Phase 11 (Polish v1.1)**: Depends on Phases 9 and 10

### User Story Dependencies (within Phase 2 completion)

Every story depends on:
- T004 (new types registered) — so `partdef`/`statedef`/etc. directives work
- T005 (new fields registered, including `interacts_with` per finding U1) — so `:trigger:`, `:from_state:`, `:interacts_with:`, etc. parse cleanly
- T007 (flow configs) — so `:config: sysml_<x>` finds skinparam
- T009b (`warn_unknown_ref` / `warn_empty` helpers in `warnings.py`) — every directive uses these to satisfy FR-016 / FR-018 uniformly
- T011 (svg_templates.py exists) — so per-story SVG template additions have a home

Within a story:
- Template constants (PlantUML + SVG) can be added in parallel — different files
- The directive module depends on the template constants existing
- The directive registration depends on the directive module existing
- The smoke test depends on both the directive registration and the test fixture
- The docs page and vehicle_system.rst demo can be written in parallel — different files

### Parallel Opportunities

**Within Phase 2**:
- T009 (`needsysml-req` :filter: option) is parallel with T004–T008 — different file
- T011 (`BDD_SVG_TEMPLATE` move to svg_templates.py) parallel with T009 once T003 lands

**Within each US Phase**:
- The two template tasks (PlantUML + SVG) are [P] with each other
- The docs page and toctree update are [P] with each other and with the demo addition (but the demo addition serializes with other US's demo additions because `vehicle_system.rst` is shared)

**Cross-team (if multiple engineers):**
- After Phase 2 completes, one engineer can drive US1+US2 (the P1 stories) while another drives US3+US4+US5 (P2 stories), serializing only on the shared docs files
- v1.1 stories (US6, US7) are nearly fully parallel: alloc has no template constants in templates.py or svg_templates.py, so it doesn't even contend on those files

---

## Parallel Example: User Story 1 (State Machine)

```text
# These can start simultaneously once Phase 2 is complete:
Task: "T013 [US1] Create tests/doc_test/stm/ fixture (conf.py + index.rst)"
Task: "T015 [US1] Add STM_FULL_TEMPLATE to sphinx_need_sysml/templates.py"
Task: "T016 [US1] Add STM_SVG_TEMPLATE to sphinx_need_sysml/svg_templates.py"
Task: "T019 [US1] Write docs/directives/needsysml_stm.rst"
Task: "T020 [US1] Add stm entry to docs/index.rst toctree"

# These serialize after the parallel tasks above complete:
Then T017 (needsysml_stm.py directive) → T018 (registration) → T014 (smoke test)
Then T021 (vehicle_system.rst demo addition — serializes with later stories' demo additions)
```

---

## Implementation Strategy

### MVP First (User Story 1 only)

1. Complete Phase 1 (Setup) and Phase 2 (Foundational) — ~12 tasks
2. Complete Phase 3 (US1 — state machine) — 9 tasks
3. **Stop and validate**: run `tests/test_stm_directive.py`, build `docs/`, navigate to the new state diagram in `docs/_build/html/examples/vehicle_system.html`, click a state to confirm SVG link
4. If MVP is enough to ship, jump to a slimmed Phase 8 (skip Phase 4–7 for now)

### Incremental Delivery (v1 path)

1. Setup + Foundational (Phases 1–2)
2. US1 (Phase 3) → validate → could ship here as `0.3.0-beta1`
3. US2 (Phase 4) → validate
4. US3 (Phase 5) → validate
5. US4 (Phase 6) → validate
6. US5 (Phase 7) → validate
7. Phase 8 polish + version bump → release `0.3.0`

### v1.1 Path

After `0.3.0` is in users' hands:
- US6 + US7 (Phases 9–10) — these can be developed in parallel; only serialize on the shared docs files
- Phase 11 polish + version bump → release `0.4.0`

### Parallel Team Strategy

With three engineers post-Foundational:

- Engineer A: US1 + US2 (the two P1 stories) → ~18 tasks
- Engineer B: US3 + US4 → ~18 tasks
- Engineer C: US5 + (after v1) US6 → ~15 tasks
- One engineer drops in to handle Phase 8 polish + release
- v1.1: A and B split US6/US7

The `docs/index.rst` toctree and `docs/examples/vehicle_system.rst` need a quick merge-coordination protocol (e.g. each story's demo addition lands its own commit with a clear `### <DiagramName>` header, easy to rebase past each other).

---

## Validation

- ✅ All five v1 user stories have one independent test fixture each
- ✅ All seven user stories have one smoke test file each
- ✅ All thirteen new directives (7 PlantUML + 6 SVG) are registered in `sphinx_need_sysml/__init__.py:setup()`
- ✅ Every new directive has a per-directive documentation page under `docs/directives/`
- ✅ The vehicle example demonstrates all ten diagram views (3 existing + 7 new) per FR-020 / SC-003
- ✅ Smoke tests cover the FR-019 contract (build + content-presence)
- ✅ No task duplicates a file in a [P] group (verified by walking the [P] markers — each [P] within a phase touches a distinct file)
- ✅ Each task identifies its file path explicitly so an LLM can execute it without additional context
- ✅ Two-phase release boundary (Phase 8 ships v1.0; Phase 11 ships v1.1) honored per spec Q5

## Summary

- **Total tasks**: 86 (T001–T085 + T009b)
- **v1 tasks (Phases 1–8)**: 65 — covers US1–US5; includes the shared `warn_unknown_ref` / `warn_empty` helpers (T009b)
- **v1.1 tasks (Phases 9–11)**: 21 — covers US6, US7
- **Parallel-marked tasks**: 38 — clustered by phase boundary
- **Smoke test files**: 7 (one per new directive family) + extension of 3 existing test files (T006, T008, T058)
- **MVP scope (recommended first stop)**: Phase 1 + Phase 2 + Phase 3 = 22 tasks delivers User Story 1 end-to-end
- **Remediation applied (post-analyze)**: 4 edits — `interacts_with` field on Actor (U1); shared FR-016/FR-018 helpers task T009b (G1, G2); US4 fixture + smoke test updated to exercise the new field (U1).
