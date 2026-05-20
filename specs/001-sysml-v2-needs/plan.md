# Implementation Plan: SysML v2 sphinx-needs Extension

**Branch**: `001-sysml-v2-needs` | **Date**: 2026-05-20 | **Spec**: [spec.md](spec.md)

## Summary

Build `sphinxcontrib-sysml` — a sphinx-needs extension that registers 14 SysML v2 need types (PartDef, Part, PortDef, Port, InterfaceDef, Interface, ConnectionDef, Connection, RequirementDef, Requirement, ActionDef, Action, StateDef, StateUsage), associated extra fields, PlantUML skinparam flow configs, and three high-level diagram directives (`needsysml-bdd`, `needsysml-ibd`, `needsysml-req`) that generate auto-layout PlantUML diagrams via needuml. Optional `sphinx-need-svg` integration provides SVG-native clickable diagrams as an alternative rendering path.

## Technical Context

**Language/Version**: Python ≥ 3.10

**Primary Dependencies**:
- `sphinx-needs >= 1.0` — need type registration, `add_field`, `add_need_type`, `flow_configs`, Jinja context
- `sphinx >= 4.0`
- `sphinxcontrib-plantuml` — optional, for PlantUML rendering
- `sphinx-need-svg` — optional, for SVG-native diagram rendering (local: `/home/chris/develop/open_source/sphinx-need-svg`)

**Storage**: N/A

**Testing**: pytest + nox, following `sphinx-test-reports` conventions

**Target Platform**: Linux / macOS / Windows (pure Python, no native dependencies)

**Project Type**: Python library (Sphinx extension), `sphinxcontrib.*` namespace, `flit` build backend

**Performance Goals**: A Sphinx build with 50 SysML v2 needs and 3 diagrams completes without errors in standard build time.

**Constraints**:
- Must not break existing sphinx-needs config in user's project
- `needs_flow_configs` merge must prefer user-defined keys over extension defaults
- Extension must work without `sphinxcontrib-plantuml` installed (degrade gracefully with warning)
- `add_field` compatibility shim required for sphinx-needs < 6.0

**Scale/Scope**: 14 need types, ~15 extra fields, 3 flow configs, 3 diagram directives, ~6 Jinja2 template constants, ~1500 LOC

## Constitution Check

Constitution not yet ratified (blank template). No gates to enforce. Re-check after constitution is written.

## Project Structure

### Documentation (this feature)

```text
specs/001-sysml-v2-needs/
├── spec.md
├── plan.md              ← this file
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── sphinx-extension-api.md
├── checklists/
│   └── requirements.md
└── tasks.md             ← /speckit-tasks output (not yet created)
```

### Source Code (repository root)

```text
sphinxcontrib/
└── sysml/
    ├── __init__.py          # setup(), VERSION, public re-exports
    ├── config.py            # SysmlConfig dataclass, need type definitions, field definitions
    ├── templates.py         # Jinja2 template string constants (BDD_FULL_TEMPLATE etc.)
    ├── flow_configs.py      # PlantUML skinparam strings for sysml_bdd/ibd/req
    ├── directives/
    │   ├── __init__.py
    │   ├── needsysml_bdd.py  # NeedsymlBddDirective wrapping needuml
    │   ├── needsysml_ibd.py  # NeedsymlIbdDirective wrapping needuml
    │   └── needsysml_req.py  # NeedsymlReqDirective wrapping needuml
    └── warnings.py          # Warning emission helpers

docs/
├── conf.py
├── index.rst
├── install.rst
├── directives/
│   ├── need_types.rst
│   ├── needsysml_bdd.rst
│   ├── needsysml_ibd.rst
│   └── needsysml_req.rst
└── examples/
    └── vehicle_system.rst

tests/
├── conftest.py
├── doc_test/
│   ├── basic/
│   │   ├── conf.py
│   │   └── index.rst
│   └── full_example/
│       ├── conf.py
│       └── index.rst
├── test_need_types.py
├── test_fields.py
├── test_flow_configs.py
├── test_bdd_directive.py
├── test_ibd_directive.py
└── test_req_directive.py

pyproject.toml
noxfile.py
```

**Structure Decision**: Single-package extension in `sphinxcontrib/sysml/`, mirroring `sphinx-test-reports` layout. Directives split into individual files for clarity. No backend/frontend split — pure Sphinx extension.

## Complexity Tracking

No constitution violations to justify.

---

## Phase 0 Artifacts

- [research.md](research.md) — PlantUML SysML notation, sphinx-needs API, hyperlink strategy, needuml Jinja context. All NEEDS CLARIFICATION resolved.

## Phase 1 Artifacts

- [data-model.md](data-model.md) — All 14 need types, 15 extra fields, flow config keys, directive contracts
- [contracts/sphinx-extension-api.md](contracts/sphinx-extension-api.md) — Installation, conf.py, directive, and warning contracts
- [quickstart.md](quickstart.md) — End-to-end usage example

## Key Design Decisions (from research)

1. **`needs_flow_configs` = skinparam only**: Jinja2 templates live in directive bodies, not in flow configs. The extension ships Jinja2 template string constants in `templates.py` that users can reference in custom `.. needuml::` directives.

2. **Dual rendering path**: PlantUML (needuml) is primary; sphinx-need-svg is optional secondary. Detection via `importlib.util.find_spec("sphinx_need_svg")`.

3. **PlantUML hyperlinks**: Use `[[{docname}.html#{id}{title}]]` syntax in class definitions. Extension emits a build warning if `plantuml_output_format != "svg"`.

4. **`add_field` compatibility shim**: Match the pattern from `sphinx-test-reports` — try `add_field` (new API), fall back to `add_extra_option` (deprecated).

5. **High-level directives**: `needsysml-bdd`, `needsysml-ibd`, `needsysml-req` wrap `.. needuml::` internally by programmatically creating a `NeedumlDirective` node with pre-baked content. This avoids duplicating the PlantUML rendering logic.

6. **IBD fidelity acknowledgement**: IBD diagrams are clearly labelled as approximations (component diagram without locked port placement). Documentation will note this limitation.
