# Implementation Plan: Use Case Diagram UML and SVG Alignment

**Branch**: `006-usecase-diagram-uml-svg` | **Date**: 2026-05-21 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/006-usecase-diagram-uml-svg/spec.md`

## Summary

Align the `needsysml-uc-svg` directive output with the PlantUML `needsysml-uc` rendering. The SVG template currently has three gaps: (1) association lines from actors connect to ellipse center points instead of borders, (2) extend/include lines use hardcoded offsets that don't account for ellipse geometry, and (3) `generalizes` relationships are not rendered at all. The fix follows the same border-to-border pattern established in the pkg-svg fix (feature 005): store full ellipse geometry, compute border intersection points for line endpoints, and add `generalizes` rendering.

## Technical Context

**Language/Version**: Python 3.10+ (project minimum)

**Primary Dependencies**: sphinx-needs (filter API), sphinx-need-svg (SVG rendering pipeline), Jinja2 (template engine)

**Storage**: N/A — in-memory rendering only

**Testing**: pytest + sphinx.testing.fixtures, Playwright for visual regression

**Target Platform**: Sphinx HTML builder output (inline SVG in HTML pages)

**Project Type**: Sphinx extension (library)

**Performance Goals**: SVG renders at build time — no runtime performance concern. Template must handle up to 10 actors and 20 use cases without viewBox clipping.

**Constraints**: Pure Jinja2 template — no Python code in the template. Must use the same `actor_pos` / `uc_pos` dictionary pattern as the existing template. SVG must be self-contained (no external CSS/JS).

**Scale/Scope**: Single file change (`sphinxcontrib/sysml/svg_templates.py`, ~85 lines for UC_SVG_TEMPLATE) plus test fixture updates and 3 new tests.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Based on AGENTS.md conventions:

- **TDD**: Tests written before implementation. 3 new SVG regression tests will be added to `tests/test_uc_directive.py` before modifying the template.
- **Lint + format**: `ruff check` and `ruff format` must pass on changed files.
- **Test suite**: All existing tests must continue to pass. New tests added for SVG-specific behavior.
- **No `sphinxcontrib/__init__.py`**: Not applicable to this change.
- **CI order**: lint → test → docs-build. All must pass.

**Gate status**: PASS — no constitution violations. This is a single-file template change following established patterns from the pkg-svg fix.

### Post-Design Re-evaluation

After Phase 1 design (research.md, data-model.md, quickstart.md):

- **TDD**: Confirmed — 3 new tests planned (border connection, layout scaling, generalizes rendering)
- **Lint + format**: Single file change (`svg_templates.py`) — straightforward to lint
- **Test suite**: Existing 5 uc tests unchanged; 3 new tests added
- **No new modules**: Only template string modification, no new Python files
- **CI**: No new dependencies, no breaking changes

**Post-design gate status**: PASS — design confirms no constitution violations.

## Project Structure

### Documentation (this feature)

```text
specs/006-usecase-diagram-uml-svg/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (N/A — no external interfaces)
└── tasks.md             # Phase 2 output (NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
sphinxcontrib/sysml/
├── svg_templates.py     # UC_SVG_TEMPLATE modified (lines 127-211)

tests/
├── test_uc_directive.py # 3 new SVG regression tests added
└── doc_test/uc/
    ├── conf.py          # Add sphinx_need_svg extension
    └── index.rst        # Add needsysml-uc-svg directive
```

**Structure Decision**: Single-project layout. Only `svg_templates.py` is modified for the template fix. Test fixture and test file are updated for coverage. No new modules or directories created.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| (none) | | |
