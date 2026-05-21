# Feature Specification: Fix Package Diagram UML vs SVG Mismatch

**Feature Branch**: `004-fix-package-uml-svg`

**Created**: 2026-05-21

**Status**: Draft

**Input**: User description: "fix the package diagram: uml vs svg render differently? while svg has pkgs inside the system, in uml the pkgs are not shown?"

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Package Diagram Renders Consistently Across Both Renderers (Priority: P1)

An engineer viewing a package diagram in the rendered documentation sees the same nested package structure whether using the PlantUML directive (`needsysml-pkg`) or the SVG companion directive (`needsysml-pkg-svg`). Currently, the SVG variant correctly shows child packages nested inside the root package, while the PlantUML variant shows only the root package with no children visible.

**Why this priority**: This is a direct rendering bug — users get inconsistent output depending on which renderer they choose, undermining trust in the tool.

**Independent Test**: Build the vehicle_system.rst example and compare the `needsysml-pkg` and `needsysml-pkg-svg` outputs — both must show PKG-002, PKG-003, PKG-004 nested inside PKG-001.

**Acceptance Scenarios**:

1. **Given** a root Package need (PKG-001) with three child packages (PKG-002, PKG-003, PKG-004) linked via `parent_package`, **When** the `needsysml-pkg` directive renders, **Then** all three child packages appear nested inside the root package rectangle.
2. **Given** the same package hierarchy, **When** the `needsysml-pkg-svg` directive renders, **Then** the same three child packages appear inside the root package rectangle (existing behavior, no regression).
3. **Given** a package hierarchy with two levels of nesting (root → child → grandchild), **When** the `needsysml-pkg` directive renders with `:depth: 3`, **Then** all three levels appear in the diagram.

---

### Edge Cases

- What happens when a package has no children? (Root package renders empty — already handled)
- How does the system handle packages with circular `parent_package` references? (Already prevented by sphinx-needs schema)
- What if a Dependency references a non-existent package? (Already handled by `needs.get()` null check)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The `PKG_FULL_TEMPLATE` PlantUML template must filter packages using the lowercase directive name `'package'` in all `filter()` expressions, matching the convention used by `PKG_SVG_TEMPLATE`.
- **FR-002**: The rendered PlantUML package diagram must display all child packages whose `parent_package` field references the root package ID.
- **FR-003**: The rendered PlantUML package diagram must display dependency arrows between packages (existing behavior, no regression).
- **FR-004**: The fix must not affect any other diagram templates (BDD, IBD, STM, ACT, SD, UC, PAR, REQ).

### Key Entities

- **Package need**: A need of type `package` (directive name) with fields `id`, `title`, `parent_package` (optional, references another Package ID).
- **Dependency need**: A need of type `dependency` with fields `source_ref`, `target_ref`, `kind`.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The vehicle_system.rst example renders both `needsysml-pkg` and `needsysml-pkg-svg` showing the same three child packages (PowertrainPkg, ChassisPkg, ControlsPkg) inside VehicleSystem.
- **SC-002**: The `tests/test_pkg_directive.py` smoke test passes with the existing fixture (PKG-001 with two children).
- **SC-003**: The strict docs build (`sphinx-build -W`) completes with zero new warnings.

## Assumptions

- The bug is confined to the `type == 'Package'` filter strings in `PKG_FULL_TEMPLATE` — no other templates are affected.
- sphinx-needs filter expressions are case-sensitive and use the directive name (lowercase), not the type title (TitleCase).
- The SVG template (`PKG_SVG_TEMPLATE`) already uses the correct lowercase filter and does not need changes.
