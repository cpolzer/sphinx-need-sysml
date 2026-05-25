# Implementation Plan: Fix Package Diagram UML vs SVG Mismatch

**Branch**: `004-fix-package-uml-svg` | **Date**: 2026-05-21 | **Spec**: [spec.md](spec.md)

## Summary

Fix a case-sensitivity bug in `PKG_FULL_TEMPLATE` where `filter()` expressions use `type == 'Package'` (capital P) instead of `type == 'package'` (lowercase), causing the PlantUML package diagram to render zero child packages while the SVG companion renders them correctly. The fix is a two-line change in `sphinx_need_sysml/templates.py`.

## Technical Context

**Language/Version**: Python ≥ 3.10

**Primary Dependencies**: sphinx-needs (filter expressions use directive name, lowercase), PlantUML (rendering)

**Storage**: N/A — Sphinx extension; no persistent state

**Testing**: pytest — existing `tests/test_pkg_directive.py` smoke test + `tests/doc_test/pkg/` fixture

**Target Platform**: Linux / macOS / Windows (pure Python)

**Project Type**: Python library — Sphinx extension under `sphinxcontrib.*` namespace

**Performance Goals**: No change — fix does not affect rendering performance

**Constraints**: Must remain backward-compatible; no other templates affected

**Scale/Scope**: Single template file (`sphinx_need_sysml/templates.py`), two filter expression strings

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

`.specify/memory/constitution.md` contains only the unfilled template (no project-specific principles ratified). No constitutional gates to enforce. The fix follows existing conventions:

- Single-line bug fix in the established template module
- Existing smoke test validates the fix
- No new types, fields, or directives introduced
- Backward-compatible (only fixes broken behavior)

Gate: **PASS**

## Project Structure

### Documentation (this feature)

```text
specs/004-fix-package-uml-svg/
├── spec.md              # Feature specification
├── plan.md              # This file
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
sphinx_need_sysml/
└── templates.py         # Single file change: PKG_FULL_TEMPLATE filter expressions

tests/
├── doc_test/pkg/        # Existing fixture — validates fix
└── test_pkg_directive.py # Existing smoke test — validates fix
```

**Structure Decision**: No new files. The fix is confined to two `filter()` expressions inside `PKG_FULL_TEMPLATE` in `sphinx_need_sysml/templates.py`, changing `'Package'` → `'package'` on lines 114 and 117.

## Complexity Tracking

No constitution violations to justify. This is a straightforward case-sensitivity bug fix with zero architectural impact.

## Phase 0 Artifacts

No research needed — the root cause is identified: sphinx-needs `filter()` expressions use the lowercase directive name (`package`), not the type title (`Package`). The SVG template already uses the correct form.

## Phase 1 Artifacts

No new data model, contracts, or quickstart docs needed. The fix is a single-template change with existing test coverage.

## Key Design Decisions

1. **Scope limited to `PKG_FULL_TEMPLATE` only**: No other templates are affected — verified by grep across all template files. The SVG template (`PKG_SVG_TEMPLATE`) already uses lowercase `'package'`.
2. **No new tests needed**: The existing `tests/test_pkg_directive.py` smoke test already asserts that child packages appear in the rendered output. Once the filter is fixed, the test will pass with the correct behavior.
3. **No version bump needed**: This is a bug fix on the current branch; versioning is handled by `cz bump` on merge to main.
