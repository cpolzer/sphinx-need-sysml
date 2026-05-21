# Feature Specification: Fix Package SVG Dependency Line Positioning

**Feature Branch**: `005-fix-pkg-svg-dependency-lines`

**Created**: 2026-05-21

**Status**: Draft

**Input**: User description: "now lets work on the package svg diagram: the connecting lines for the dependency links are not really connecting the inner pkgs diagram boxes' borders, rather look weirdly placed. can we ansure svg opositioning for linked boxed?"

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Dependency Lines Connect Package Box Borders Correctly (Priority: P1)

An engineer viewing a package diagram in SVG sees dependency arrows that originate from the border of the source package box and terminate at the border of the target package box. Currently, the lines originate from the center of the source box and terminate at arbitrary y-coordinates above the destination box, making them look disconnected and misaligned.

**Why this priority**: Visual correctness is essential for documentation — misaligned arrows confuse readers about which packages are connected.

**Independent Test**: Build the vehicle_system.rst example and inspect the `needsysml-pkg-svg` output — dependency arrows (DEP-001, DEP-002) must visibly connect the edges of the child package rectangles (PKG-002, PKG-003, PKG-004).

**Acceptance Scenarios**:

1. **Given** three child packages (PKG-002, PKG-003, PKG-004) arranged horizontally inside a root package, **When** two dependencies exist between them (PKG-002→PKG-004, PKG-003→PKG-004), **Then** each dependency line starts at the right edge of the source box and ends at the left edge of the target box.
2. **Given** multiple dependency lines between the same pair of packages, **When** rendered, **Then** lines are spaced so they don't overlap and remain readable.
3. **Given** a single child package with no dependencies, **When** rendered, **Then** no dependency lines appear (existing behavior, no regression).

---

### Edge Cases

- What happens when source and target are adjacent boxes? (Line should be short, connecting adjacent borders)
- How does the system handle dependencies where source is to the right of target? (Line should go leftward, connecting appropriate borders)
- What if a dependency references a non-child package? (Already handled — line not drawn since package not in `child_pos`)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Dependency lines in `PKG_SVG_TEMPLATE` must originate from the border edge of the source package rectangle, not from its center point.
- **FR-002**: Dependency lines must terminate at the border edge of the target package rectangle, not at an arbitrary offset above it.
- **FR-003**: Line endpoints must be computed from the actual rectangle geometry (x, y, width, height) stored during layout, not from hardcoded y-coordinates.
- **FR-004**: Multiple dependency lines between the same pair of packages must be visually distinct (not overlapping).
- **FR-005**: The fix must not affect the layout of package rectangles themselves — only the dependency line positioning changes.
- **FR-006**: The PlantUML package diagram (`PKG_FULL_TEMPLATE`) must remain unchanged (no regression).

### Key Entities

- **Package rectangle**: Positioned at `(cx, 80)` with dimensions `(cw - 20) × 220` in the SVG layout.
- **Dependency line**: A dashed `<line>` element with a stereotype label (`<<use>>`, `<<import>>`, `<<realize>>`) positioned at its midpoint.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: In the vehicle_system.rst `needsysml-pkg-svg` output, dependency lines DEP-001 and DEP-002 visibly connect the edges of their respective source and target package rectangles.
- **SC-002**: The `tests/test_pkg_directive.py` smoke test passes with no regression.
- **SC-003**: The strict docs build (`sphinx-build -W`) completes with zero new warnings.

## Assumptions

- The bug is confined to the dependency line coordinate computation in `PKG_SVG_TEMPLATE` — the rectangle layout logic is correct.
- Package boxes are always arranged horizontally (left to right) within the root package boundary.
- The fix uses the existing `child_pos` dictionary but stores full rectangle geometry (x, y, width, height) instead of just a center point.
