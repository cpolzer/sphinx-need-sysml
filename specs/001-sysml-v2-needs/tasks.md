# Tasks: sphinxcontrib-sysml

**Input**: Design documents from `specs/001-sysml-v2-needs/`

**Tech stack**: Python ≥ 3.10, flit, pytest + nox, sphinx-needs ≥ 1.0, sphinxcontrib-plantuml (optional), sphinx-need-svg (optional)

**Package layout**: `sphinxcontrib/sysml/` at repo root — single-package extension following `sphinx-test-reports` conventions.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[US#]**: Which user story this task belongs to (from spec.md)

---

## Phase 1: Setup

**Purpose**: Project skeleton — nothing works yet, but the package is installable.

- [ ] T001 Create `pyproject.toml` with flit build backend, project metadata, dependencies (`sphinx-needs>=1.0`, `sphinx>=4.0`), optional deps (`sphinxcontrib-plantuml`, `sphinx-need-svg`), and dev/test extras
- [ ] T002 Create `sphinxcontrib/__init__.py` (namespace package — empty, with namespace declaration)
- [ ] T003 Create `sphinxcontrib/sysml/__init__.py` with stub `setup(app)` returning `{"version": "0.1.0", "parallel_read_safe": True}`
- [ ] T004 [P] Create `noxfile.py` with `tests`, `lint`, and `docs` sessions following `sphinx-test-reports` nox conventions
- [ ] T005 [P] Add ruff and mypy config sections to `pyproject.toml` mirroring `sphinx-test-reports` settings
- [ ] T006 [P] Create `.gitignore` for Python project (dist/, __pycache__, .venv/, *.egg-info, docs/_build/)

**Checkpoint**: `pip install -e .` succeeds and `python -c "import sphinxcontrib.sysml"` works.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core registration infrastructure that all user stories depend on.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

- [ ] T007 Create `sphinxcontrib/sysml/config.py` — define `SYSML_NEED_TYPES` list of dicts (directive, title, prefix, color, style) for all 14 types from data-model.md
- [ ] T008 Create `sphinxcontrib/sysml/fields.py` — define `SYSML_FIELDS` list of dicts (name, description, schema) for all 15 fields from data-model.md
- [ ] T009 Add `add_field` / `add_extra_option` compatibility shim to `sphinxcontrib/sysml/__init__.py` matching the exact pattern from `sphinx-test-reports/sphinxcontrib/test_reports/test_reports.py`
- [ ] T010 Implement `_register_types_and_fields(app, config)` in `sphinxcontrib/sysml/__init__.py` — calls `add_need_type` for each entry in `SYSML_NEED_TYPES` and the shim for each entry in `SYSML_FIELDS`; connect to `config-inited` event in `setup()`
- [ ] T011 Create `sphinxcontrib/sysml/warnings.py` — implement `warn_plantuml_format(app)` that emits a Sphinx warning if `plantuml_output_format != "svg"` (checks via `getattr(app.config, "plantuml_output_format", None)`)
- [ ] T012 Create `tests/conftest.py` — Sphinx app fixture using `sphinx.testing.app` that loads a minimal doc_test project with `sphinxcontrib.sysml` in extensions
- [ ] T013 Create `tests/doc_test/basic/conf.py` and `tests/doc_test/basic/index.rst` — minimal Sphinx project with `sphinx_needs` + `sphinxcontrib.sysml` in extensions (no plantuml required)

**Checkpoint**: `pytest tests/` passes with zero tests collected (fixtures work, no errors on import).

---

## Phase 3: US1 — Define SysML v2 Structural Elements (Priority: P1) 🎯 MVP

**Goal**: Users can write `.. partdef::`, `.. part::`, `.. portdef::`, `.. requirement::` etc. directives in RST, build with Sphinx, and see rendered needs with correct types and fields.

**Independent Test**: Build `tests/doc_test/basic/` with a `.. partdef:: Engine` and `.. requirement:: Brake Distance` — both appear in the HTML output as needs with correct IDs, types, and fields visible.

### Implementation for US1

- [ ] T014 [US1] Add all 14 need type directives to `tests/doc_test/basic/index.rst` — one example each of `partdef`, `part`, `portdef`, `port`, `interfacedef`, `interface`, `connectiondef`, `connection`, `requirementdef`, `requirement`, `actiondef`, `action`, `statedef`, `stateusage` with minimal required fields
- [ ] T015 [P] [US1] Write `tests/test_need_types.py` — pytest tests verifying: (a) each of the 14 directives is registered in app after build, (b) each generates a need with the correct type name and ID prefix in the built needs data
- [ ] T016 [P] [US1] Write `tests/test_fields.py` — pytest tests verifying: (a) each of the 15 extra fields is registered, (b) `owned_by`, `satisfies`, `direction`, `multiplicity` fields are readable on built needs that set them, (c) `abstract` field accepts boolean values
- [ ] T017 [US1] Verify `tests/doc_test/basic/` builds without errors or warnings using `sphinx-build -b html` in nox tests session; fix any registration issues

**Checkpoint**: All 14 need types usable in RST; `needtable` and `:need:` role work against them; pytest tests pass.

---

## Phase 4: US2 + US5 — Block Definition Diagram + Clickable Links (Priority: P1)

**Goal**: Users can write `.. needsysml-bdd:: PD-001` and get a rendered PlantUML BDD diagram where each block is a clickable link to the corresponding need's HTML anchor.

**Independent Test**: Build `tests/doc_test/basic/` with a `.. needsysml-bdd::` directive referencing a `partdef` need — the HTML output contains a `<object>` SVG element with block elements visible; `plantuml_output_format = "svg"` is set in the test conf.py.

### Implementation for US2 + US5

- [ ] T018 [US2] Create `sphinxcontrib/sysml/flow_configs.py` — define `SYSML_FLOW_CONFIGS` dict with `sysml_bdd` skinparam string (class `<<PartDef>>` background/border colors, `hide empty members` default off, `left to right direction` as optional)
- [ ] T019 [US2] Implement `_register_flow_configs(app)` in `sphinxcontrib/sysml/__init__.py` — merges `SYSML_FLOW_CONFIGS` into `app.config.needs_flow_configs` at `builder-inited`, user keys take precedence; connect event in `setup()`
- [ ] T020 [P] [US2] Create `sphinxcontrib/sysml/templates.py` — implement `BLOCK_DEF_TEMPLATE` string: Jinja2 snippet that renders a single `PartDef` need as a PlantUML class with `<<PartDef>>` stereotype, compartments for owned Ports and attribute values, and `[[{docname}.html#{id}{{{title}}}]]` hyperlink syntax using `ref()`
- [ ] T021 [P] [US2] Add `BDD_FULL_TEMPLATE` to `sphinxcontrib/sysml/templates.py` — complete Jinja2 `@startuml/@enduml` body that: renders the root PartDef via `BLOCK_DEF_TEMPLATE`, uses `filter("type == 'Part' and owned_by == '{root_id}'")`to find child Parts, renders each child with a composition arrow `root_id *-- child_id`, supports `:depth:` parameter
- [ ] T022 [US2] Create `sphinxcontrib/sysml/directives/__init__.py` (empty)
- [ ] T023 [US2] Create `sphinxcontrib/sysml/directives/needsysml_bdd.py` — implement `NeedsymlBddDirective(SphinxDirective)` with `required_arguments=1`, `option_spec` for `:depth:`, `:filter:`, `:scale:`, `:align:`; `run()` method that creates a `Needuml` node with content set to `BDD_FULL_TEMPLATE` rendered with the given need ID and depth
- [ ] T024 [US2] Register `needsysml-bdd` directive and connect `plantuml_output_format` warning check in `setup()` in `sphinxcontrib/sysml/__init__.py`
- [ ] T025 [US2] Add `plantuml_output_format = "svg"` to `tests/doc_test/basic/conf.py` and add a `.. needsysml-bdd::` example to `tests/doc_test/basic/index.rst` using the `PD-` need defined in T014
- [ ] T026 [P] [US2] Write `tests/test_bdd_directive.py` — tests verifying: (a) directive builds without error, (b) HTML output contains `<object` element (SVG rendered), (c) a warning is emitted if `plantuml_output_format` is not `svg`
- [ ] T027 [P] [US2] Write `tests/test_flow_configs.py` — test that `sysml_bdd` key exists in `app.config.needs_flow_configs` after build, and that user-defined key is not overwritten

**Checkpoint**: `.. needsysml-bdd:: PD-001` renders a clickable SVG BDD in HTML. US2 and US5 complete.

---

## Phase 5: US3 — Requirements Diagram (Priority: P2)

**Goal**: Users can write `.. needsysml-req:: type == 'Requirement'` and get a PlantUML requirements diagram showing requirement boxes with `<<satisfy>>` and `<<deriveReqt>>` dependency arrows.

**Independent Test**: Build with requirements having `satisfies` links to `partdef` needs — the diagram shows both types connected by labelled arrows.

### Implementation for US3

- [ ] T028 [US3] Add `sysml_req` skinparam string to `sphinxcontrib/sysml/flow_configs.py` — style `<<requirement>>` class elements with yellow background/gold border
- [ ] T029 [P] [US3] Add `REQ_BOX_TEMPLATE` and `REQ_FULL_TEMPLATE` to `sphinxcontrib/sysml/templates.py` — `REQ_BOX_TEMPLATE` renders one requirement as `<<requirement>>` class with `id`/`text` compartments and hyperlink; `REQ_FULL_TEMPLATE` iterates needs matching a filter expression, renders each box, then adds `..>` arrows for `satisfies`, `refines`, and `allocates` links
- [ ] T030 [US3] Create `sphinxcontrib/sysml/directives/needsysml_req.py` — `NeedsymlReqDirective` with `required_arguments=1` (filter expression), `option_spec` for `:show-satisfy:`, `:show-refine:`, `:show-allocate:`, `:scale:`, `:align:`; `run()` renders `REQ_FULL_TEMPLATE` with the filter and show-* flags
- [ ] T031 [US3] Register `needsysml-req` directive in `setup()` in `sphinxcontrib/sysml/__init__.py`
- [ ] T032 [US3] Add `.. needsysml-req::` example to `tests/doc_test/basic/index.rst` using requirements with `satisfies` links defined in T014
- [ ] T033 [P] [US3] Write `tests/test_req_directive.py` — tests: (a) builds without error, (b) `<<satisfy>>` arrow text present in generated PlantUML source (via `:save:` option), (c) filter expression respected (only matching needs appear)

**Checkpoint**: Requirements diagram with traceability arrows renders. US3 complete.

---

## Phase 6: US4 — Internal Block Diagram (Priority: P2)

**Goal**: Users can write `.. needsysml-ibd:: PD-001` and get a component-diagram-style IBD showing internal Part instances with port connections.

**Independent Test**: Build with a `partdef` owning two `part` instances each with `port` usages — the diagram shows both parts inside a context boundary with port-to-port connections.

### Implementation for US4

- [ ] T034 [US4] Add `sysml_ibd` skinparam string to `sphinxcontrib/sysml/flow_configs.py` — style component `<<Part>>` elements, `<<ibd>>` rectangle boundary
- [ ] T035 [P] [US4] Add `BLOCK_INST_TEMPLATE` and `IBD_FULL_TEMPLATE` to `sphinxcontrib/sysml/templates.py` — `IBD_FULL_TEMPLATE` uses component diagram syntax: renders root PartDef as `rectangle` boundary, child Parts as `component` elements with `portin`/`portout` for owned Ports, then Connection needs as connector lines between ports; includes clear comment noting IBD is an approximation (no locked port placement)
- [ ] T036 [US4] Create `sphinxcontrib/sysml/directives/needsysml_ibd.py` — `NeedsymlIbdDirective` with `required_arguments=1`, `option_spec` for `:show-ports:` (default true), `:scale:`, `:align:`; `run()` renders `IBD_FULL_TEMPLATE`
- [ ] T037 [US4] Register `needsysml-ibd` directive in `setup()` in `sphinxcontrib/sysml/__init__.py`
- [ ] T038 [US4] Add `.. needsysml-ibd::` example and `connection` needs to `tests/doc_test/basic/index.rst`
- [ ] T039 [P] [US4] Write `tests/test_ibd_directive.py` — tests: (a) builds without error, (b) IBD diagram contains expected part names

**Checkpoint**: IBD renders as component diagram approximation. All 5 user stories complete.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Documentation, full example, and integration test.

- [ ] T040 [P] Create `tests/doc_test/full_example/conf.py` and `tests/doc_test/full_example/index.rst` — complete vehicle system example from `quickstart.md` using all three diagram types
- [ ] T041 Create `docs/conf.py` and `docs/index.rst` — Sphinx docs project with sphinx-needs + sphinxcontrib.plantuml + sphinxcontrib.sysml in extensions; uses sphinx-immaterial theme
- [ ] T042 [P] Create `docs/install.rst` — installation instructions mirroring `quickstart.md`
- [ ] T043 [P] Create `docs/directives/need_types.rst` — documents all 14 need types with their fields, ID prefixes, and usage examples
- [ ] T044 [P] Create `docs/directives/needsysml_bdd.rst` — documents `.. needsysml-bdd::` directive options and rendered output
- [ ] T045 [P] Create `docs/directives/needsysml_ibd.rst` — documents `.. needsysml-ibd::` with IBD approximation caveat
- [ ] T046 [P] Create `docs/directives/needsysml_req.rst` — documents `.. needsysml-req::` with filter expression examples
- [ ] T047 [P] Create `docs/examples/vehicle_system.rst` — full worked example (vehicle system BDD + IBD + requirements)
- [ ] T048 Build and validate `docs/` with `sphinx-build -b html` — fix any broken refs or missing content
- [ ] T049 [P] Add `SKILL.md` to repo root — agent-readable contract for the extension (directive options, Jinja helpers, config keys), following the `sphinx-need-svg/SKILL.md` pattern
- [ ] T050 Run `quickstart.md` steps manually in a clean venv; fix any discrepancies between docs and implementation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately
- **Foundational (Phase 2)**: Depends on Phase 1 completion — **blocks all user stories**
- **US1 (Phase 3)**: Depends on Phase 2 only
- **US2+US5 (Phase 4)**: Depends on Phase 2 + Phase 3 (need types must exist for BDD to render anything)
- **US3 (Phase 5)**: Depends on Phase 2 + Phase 3 (requirement types must exist)
- **US4 (Phase 6)**: Depends on Phase 2 + Phase 3 (part/port types must exist)
- **Polish (Phase 7)**: Depends on all story phases complete

### User Story Dependencies

- **US1 (P1)**: First — foundational types enable all diagrams
- **US2+US5 (P1)**: After US1 — BDD needs PartDef/Part types
- **US3 (P2)**: After US1 — Requirements diagram needs Requirement types; can run in parallel with US2+US5
- **US4 (P2)**: After US1 — IBD needs Part/Port/Connection types; can run in parallel with US3

### Parallel Opportunities

Within Phase 3 (US1): T015 and T016 can run in parallel (different test files).
Within Phase 4 (US2+US5): T020 and T021 (templates) can run in parallel with T022 (directive skeleton).
Within Phase 5 (US3): T029 (templates) can run in parallel with T030 (directive).
Within Phase 7 (Polish): All docs tasks (T042–T047) can run in parallel.
Phases 5 and 6 can run in parallel with each other once Phase 3 is complete.

---

## Parallel Example: US2+US5

```
# These can run simultaneously:
Task T020: Implement BLOCK_DEF_TEMPLATE in sphinxcontrib/sysml/templates.py
Task T021: Implement BDD_FULL_TEMPLATE in sphinxcontrib/sysml/templates.py

# Then, these can run simultaneously:
Task T026: Write tests/test_bdd_directive.py
Task T027: Write tests/test_flow_configs.py
```

---

## Implementation Strategy

### MVP (User Stories 1 + 2 + 5 only — Phases 1–4)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: US1 (need types work)
4. Complete Phase 4: US2+US5 (BDD with clickable links)
5. **STOP and VALIDATE**: `sphinx-build` a doc with `.. partdef::`, `.. part::`, and `.. needsysml-bdd::` — all work, links are clickable in HTML
6. This is a shippable v0.1.0

### Incremental Delivery

1. v0.1.0 — Phases 1–4: need types + BDD + links
2. v0.2.0 — Phase 5: requirements diagram
3. v0.3.0 — Phase 6: IBD
4. v1.0.0 — Phase 7: full docs + full example

---

## Notes

- Total tasks: **50**
- US1: 4 tasks | US2+US5: 10 tasks | US3: 6 tasks | US4: 6 tasks | Setup: 6 | Foundational: 7 | Polish: 11
- [P] tasks = different files, safe to run in parallel
- Commit after each phase checkpoint
- `add_field` compatibility shim (T009) is critical — test against both sphinx-needs < 6 and ≥ 6 if possible
- IBD fidelity is intentionally limited; document this in `needsysml_ibd.rst` (T045)
