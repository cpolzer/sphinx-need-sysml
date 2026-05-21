# Implementation Plan: Fix Package SVG Dependency Line Positioning

**Branch**: `005-fix-pkg-svg-dependency-lines` | **Date**: 2026-05-21 | **Spec**: [spec.md](spec.md)

## Summary

Fix the dependency line positioning in `PKG_SVG_TEMPLATE` so that dashed arrows connect the border edges of child package rectangles instead of floating from center points to arbitrary y-coordinates. The fix replaces the current `[center_x, 200]` point storage with full rectangle geometry and computes border-to-border line endpoints.

## Technical Context

**Language/Version**: Python ≥ 3.10

**Primary Dependencies**: sphinx-needs (needs registry), Jinja2 (SVG template rendering)

**Storage**: N/A — template-only change

**Testing**: pytest — existing `tests/test_pkg_directive.py` smoke test + `tests/doc_test/pkg/` fixture

**Target Platform**: Linux / macOS / Windows (pure Python, SVG output)

**Project Type**: Python library — Sphinx extension under `sphinxcontrib.*` namespace

**Performance Goals**: No change — SVG rendering is already fast

**Constraints**: Must not change rectangle layout; only dependency line coordinates change. Template must remain valid Jinja2 for sphinx-need-svg's `SvgJinjaContext`.

**Scale/Scope**: Single template section (`PKG_SVG_TEMPLATE`, lines 250-259) in `sphinxcontrib/sysml/svg_templates.py`

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

`.specify/memory/constitution.md` contains only the unfilled template (no project-specific principles ratified). No constitutional gates to enforce. The fix follows existing conventions:

- Single-template change in the established SVG template module
- Existing smoke test validates the fix
- No new types, fields, or directives introduced
- Backward-compatible (only fixes broken visual behavior)

Gate: **PASS**

## Project Structure

### Documentation (this feature)

```text
specs/005-fix-pkg-svg-dependency-lines/
├── spec.md              # Feature specification
├── plan.md              # This file
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
sphinxcontrib/sysml/
└── svg_templates.py     # Single file change: PKG_SVG_TEMPLATE dependency line section (lines 250-259)

tests/
├── doc_test/pkg/        # Existing fixture — validates fix
└── test_pkg_directive.py # Existing smoke test — validates fix
```

**Structure Decision**: No new files. The fix is confined to the dependency line rendering block inside `PKG_SVG_TEMPLATE` in `sphinxcontrib/sysml/svg_templates.py`.

## Complexity Tracking

No constitution violations to justify. This is a visual layout bug fix with zero architectural impact.

## Phase 0 Artifacts

No research needed — the root cause is identified: `child_pos` stores `[center_x, 200]` (a center point) and lines are drawn from center to arbitrary y-offsets. The fix stores full rectangle geometry and computes border intersection points.

## Phase 1 Artifacts

No new data model, contracts, or quickstart docs needed. The fix is a single-template change with existing test coverage.

## Key Design Decisions

1. **Store rectangle geometry in `child_pos`**: Change from `{id: [cx, 200]}` to `{id: {x, y, w, h}}` so dependency lines can compute exact border coordinates.
2. **Border-to-border line computation**: For horizontally-arranged boxes, the source line endpoint is the right edge (`x + w, y + h/2`) and the target endpoint is the left edge (`x, y + h/2`). This works for left-to-right dependencies; for right-to-left, the edges swap.
3. **Multiple lines between same pair**: Use a small vertical offset per dependency (e.g., `+ loop.index0 * 12`) applied to the midpoint y-coordinate so lines don't overlap.
4. **No layout changes**: Rectangle positions and dimensions remain identical — only the `<line>` element coordinates change.
5. **Stereotype label positioning**: The `<<kind>>` label text is positioned at the line midpoint with the same vertical offset as the line, keeping it readable.
