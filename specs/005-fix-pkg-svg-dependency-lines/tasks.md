---

description: "Task list for feature 005-fix-pkg-svg-dependency-lines"
---

# Tasks: Fix Package SVG Dependency Line Positioning

**Input**: Design documents from `/specs/005-fix-pkg-svg-dependency-lines/`

**Prerequisites**: plan.md ✓, spec.md ✓

**Tests**: Existing `tests/test_pkg_directive.py` smoke test validates the fix; `tests/doc_test/pkg/` fixture provides test data.

**Organization**: Single user story (US1) — fix dependency line positioning in `PKG_SVG_TEMPLATE`.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Task may run in parallel with other [P] tasks at the same phase boundary
- **[Story]**: US1 — maps to the single user story in spec.md
- All paths are repository-relative

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Pre-implementation housekeeping

- [ ] T001 Confirm working tree clean on branch `005-fix-pkg-svg-dependency-lines`; verify no uncommitted changes from prior work

---

## Phase 2: Implementation (US1 — Dependency Line Positioning)

**Goal**: Dependency lines in `PKG_SVG_TEMPLATE` connect package box borders instead of floating from center points.

### Tests for User Story 1

- [ ] T002 [P] [US1] Extend `tests/test_pkg_directive.py` with a visual assertion: parse the rendered SVG from the pkg fixture and verify that dependency line endpoints (`x1`, `y1`, `x2`, `y2`) fall within the bounding rectangles of their source and target packages (not at center points or arbitrary offsets)

### Implementation for User Story 1

- [ ] T003 [US1] In `sphinxcontrib/sysml/svg_templates.py`, change `child_pos` storage from `{id: [cx, 200]}` to `{id: {x, y, w, h}}` where `x=cx`, `y=80`, `w=cw-20`, `h=220` — matching the actual `<rect>` element attributes in the template
- [ ] T004 [US1] Update the dependency line `<line>` element coordinates: compute source endpoint at the right edge of the source rect (`x+w, y+h/2`) and target endpoint at the left edge of the target rect (`x, y+h/2`). For right-to-left dependencies (source index > target index), swap edges: source left edge → target right edge
- [ ] T005 [US1] Update the stereotype label `<text>` position to align with the new line midpoint. Apply a small vertical offset per dependency (`loop.index0 * 12`) to prevent overlapping labels when multiple dependencies exist between the same pair of packages
- [ ] T006 [P] [US1] Run `git diff -- sphinxcontrib/sysml/templates.py` — produces no output, confirming `PKG_FULL_TEMPLATE` is unchanged (FR-006)

---

## Phase 3: Verification

**Purpose**: Confirm fix works and no regressions

- [ ] T007 [P] [US1] Run `pytest tests/test_pkg_directive.py -v` — all tests pass including the new visual assertion from T002; additionally assert that the rendered SVG `<rect>` elements for child packages retain their original attributes (`y="80"`, `height="220"`, `width` matching `cw-20`) — confirming FR-005 (no layout regression)
- [ ] T008 [P] [US1] Run `sphinx-build -W docs docs/_build/html` — zero warnings, `needsysml-pkg-svg` renders with border-connected dependency lines
- [ ] T009 [US1] Run full test suite `pytest tests/ -q` — all existing tests pass (no regression)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies — start immediately
- **Phase 2 (Implementation)**: Depends on Phase 1. T002 can run in parallel with T003-T006 (different files). T003 must complete before T004 and T005 (data structure change gates coordinate computation). T006 is parallel with T003-T005 (different file, verification only).
- **Phase 3 (Verification)**: Depends on Phase 2 completion. T007 and T008 can run in parallel; T009 runs after both pass.

### Parallel Opportunities

- T002 (new test) is parallel with T003-T006 (implementation) — different files
- T007 (pkg test) and T008 (docs build) are parallel — independent validation
- T006 (PlantUML unchanged check) is parallel with all other implementation tasks — different file

---

## Implementation Strategy

### Single-Pass (Recommended)

1. Phase 1: Confirm clean working tree
2. Phase 2: Change `child_pos` storage → update line coordinates → update label positions → verify PlantUML unchanged
3. Phase 3: Run pkg test → run docs build → run full suite

Total: 9 tasks, estimated ~30 minutes.

---

## Validation

- ✅ Single user story with clear independent test
- ✅ All tasks identify file paths explicitly
- ✅ No task duplicates a file in a [P] group
- ✅ Existing smoke test validates the fix; new visual assertion adds regression safety
- ✅ PlantUML template explicitly verified unchanged (FR-006)

## Summary

- **Total tasks**: 9
- **Parallel-marked tasks**: 4
- **Files touched**: 2 (`sphinxcontrib/sysml/svg_templates.py`, `tests/test_pkg_directive.py`)
- **New files**: 0
- **Regression risk**: Low — only dependency line coordinates change; rectangle layout unchanged
