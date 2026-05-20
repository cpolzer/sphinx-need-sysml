## v0.3.0 (2026-05-21)

### Feat

- **diagrams**: full SysML v2 diagram coverage (v1, stories 1–5)
  - new `needsysml-stm` / `needsysml-stm-svg` — state machine with composite states, pseudostates (initial / final / shallow / deep history / choice / junction), and transitions with trigger/guard/effect
  - new `needsysml-act` / `needsysml-act-svg` — activity with swimlane partitions, fork/join, decision/merge, control flow and object flow
  - new `needsysml-sd` / `needsysml-sd-svg` — sequence with sync / async / return messages and combined fragments (alt / opt / loop / par / neg / critical)
  - new `needsysml-uc` / `needsysml-uc-svg` — use case with system-boundary subjects, actor↔use-case associations via `interacts_with`, and extends / includes / generalizes relationships
  - new `needsysml-pkg` / `needsysml-pkg-svg` — package with up to 3 levels of nesting and use / import / realize dependency kinds
  - promoted `needsysml-ibd-svg` to a first-class directive (was an inline `.. needsvg::` workaround)
  - added `:filter:` option (default `type == 'Requirement'`) to `needsysml-req` — positional argument still works
- **types**: 13 new SysML need types — Transition, ControlFlow, ObjectFlow, Package, Dependency, UseCase, Actor, ConstraintBlock, ConstraintParameter, ValueProperty, BindingConnector, Lifeline, Message (total: 27 types)
- **fields**: 34 new extra fields covering state-machine, activity, package, use case, sequence, and parametric attributes; enum-validated where applicable (e.g. `pseudo_kind`, `message_kind`, `fragment_kind`, `kind`, `activity_kind`)
- **error handling**: shared `warn_unknown_ref` / `warn_empty` helpers in `warnings.py` provide uniform categorized warnings (`[needsysml.<diagram>.unknown-<ref_kind>]`) and placeholders across every new diagram directive
- **demo**: extended `docs/examples/vehicle_system.rst` to demonstrate every v1 diagram (10 views) with PlantUML and SVG variants side by side; full strict build is clean in under 11 seconds

### Notes

- v1.1 element types (ConstraintBlock, ConstraintParameter, ValueProperty, BindingConnector) are registered now so users' models stay stable when the parametric and allocation-matrix diagrams ship in v0.4.

## v0.2.4 (2026-05-20)

### Fix

- add Pillow dependency for PlantUML scaling support

## v0.2.3 (2026-05-20)

### Fix

- fail docs build on warnings and fix missing toctree entry

## v0.2.2 (2026-05-20)

### Fix

- correct PyPI project URLs to cpolzer/sphinx-need-sysml

## v0.2.1 (2026-05-20)

### Fix

- **ci**: update actions to v5 to resolve Node.js 20 deprecation warnings

## v0.2.0 (2026-05-20)

### Fix

- **ci**: use PAT_TOKEN for version bump to bypass branch protection
- **types**: replace broken mypy exclude with overrides and fix type errors
- resolve all ruff lint errors in CI
