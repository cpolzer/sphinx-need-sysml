# Feature Specification: Use Case Diagram UML and SVG Alignment

**Feature Branch**: `006-usecase-diagram-uml-svg`

**Created**: 2026-05-21

**Status**: Draft

**Input**: User description: "lets work on the usecase diagram uml and svg-> uml renders [screenshot showing a use case diagram with actors, use cases in ellipses, system boundary rectangle, and association/extend/include arrows]"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - SVG renders use case diagram matching PlantUML output (Priority: P1)

A documentation author writes `.. needsysml-uc::` and `.. needsysml-uc-svg::` directives in their Sphinx docs. The SVG output should visually match the PlantUML-rendered diagram — actors as stick figures on the left, use cases as ellipses inside a system boundary rectangle, with association, extend, and include relationships drawn as connected lines with proper labels.

**Why this priority**: The SVG directive exists as an alternative to PlantUML rendering. If it produces incorrect or misleading diagrams, users cannot trust it and will avoid it entirely.

**Independent Test**: Build the uc test fixture with both directives present. Visually compare the SVG output against the PlantUML output — actors, ellipses, boundary, and all relationship lines should be present and correctly positioned.

**Acceptance Scenarios**:

1. **Given** a project with actors, use cases, and relationships defined, **When** both `needsysml-uc` and `needsysml-uc-svg` are rendered, **Then** the SVG shows the same elements in equivalent positions
2. **Given** an actor with `interacts_with` pointing to a use case, **When** the SVG renders, **Then** a solid line connects the actor to the use case ellipse border
3. **Given** a use case with `extends` pointing to another, **When** the SVG renders, **Then** a dashed line with `<<extend>>` label connects the two ellipses
4. **Given** a use case with `includes` pointing to another, **When** the SVG renders, **Then** a dashed line with `<<include>>` label connects the two ellipses

---

### User Story 2 - SVG handles multiple actors and use cases without overlap (Priority: P2)

When a use case diagram has many actors (stacked vertically on the left) and many use cases (stacked vertically inside the system boundary), the SVG layout should space them evenly without overlapping elements or clipped content.

**Why this priority**: Real-world use case diagrams often have 5+ actors and 10+ use cases. A layout that only works for 2 actors and 4 use cases is not useful.

**Independent Test**: Create a fixture with 4 actors and 8 use cases. Verify the SVG viewBox height accommodates all elements and no text or shapes overlap.

**Acceptance Scenarios**:

1. **Given** N actors and M use cases, **When** the SVG renders, **Then** the viewBox height is at least `(N + M) * minimum_spacing + margins`
2. **Given** use cases with long titles, **When** the SVG renders, **Then** ellipse width accommodates the text without clipping

---

### User Story 3 - SVG supports `generalizes` relationships (Priority: P3)

The PlantUML template already supports `generalizes` between use cases (rendered as `<|--` inheritance arrows). The SVG template should also render these as dashed arrows with appropriate labeling.

**Why this priority**: Feature parity with the PlantUML output. Currently the SVG template only handles `extends` and `includes`.

**Independent Test**: Add a use case with `generalizes` field to the fixture. Verify the SVG renders an inheritance-style arrow between the two use cases.

**Acceptance Scenarios**:

1. **Given** a use case with `generalizes: USECASE-001`, **When** the SVG renders, **Then** a dashed arrow points from the child to the parent use case

---

### Edge Cases

- What happens when an actor's `interacts_with` references a non-existent use case ID? (Should skip silently, not break)
- How does the SVG handle use cases with no `subject` field? (Should default to a generic system boundary or no boundary)
- What if `extends`/`includes`/`generalizes` contains circular references? (Should render without infinite loops)
- How does the layout behave with zero actors or zero use cases? (Should show a "no elements" placeholder)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Actors MUST render as recognizable human-figure icons positioned on the left side of the diagram
- **FR-002**: Use cases MUST render as oval/elliptical shapes positioned inside a system boundary rectangle
- **FR-003**: A system boundary rectangle MUST enclose use cases, labeled with the `subject` field value (or "System" if not specified)
- **FR-004**: Association lines (from actor `interacts_with`) MUST connect from the actor icon to the target use case shape border — not to center points
- **FR-005**: Extend relationships (from use case `extends`) MUST render as dashed lines with `<<extend>>` label positioned near the line midpoint
- **FR-006**: Include relationships (from use case `includes`) MUST render as dashed lines with `<<include>>` label positioned near the line midpoint
- **FR-007**: Generalize relationships (from use case `generalizes`) MUST render as dashed lines with inheritance-style arrow pointing to the generalized use case
- **FR-008**: The diagram canvas dimensions MUST dynamically scale based on the number of actors and use cases to prevent clipping
- **FR-009**: Multiple association lines from the same actor to different use cases MUST be vertically offset to avoid overlap
- **FR-010**: The directive MUST use the same filter expression logic as the PlantUML variant (`type == 'UseCase'` by default)
- **FR-011**: Invalid or missing relationship targets MUST be silently skipped without breaking the render

### Key Entities

- **Actor**: A stick-figure representation of a system user, with `id`, `title`, and `interacts_with` (comma-separated use case IDs)
- **UseCase**: An ellipse representing a system capability, with `id`, `title`, `subject` (system boundary label), `extends`, `includes`, and `generalizes` fields
- **System Boundary**: A rectangle enclosing use cases that share the same `subject` value

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All relationship lines (association, extend, include, generalize) connect to element borders — not floating from center points — verified by inspecting rendered output coordinates
- **SC-002**: The diagram canvas height is within 10% of the minimum required to display all elements without overlap, for diagrams with up to 10 actors and 20 use cases
- **SC-003**: Visual comparison of SVG vs PlantUML output shows equivalent element positioning (actors left, use cases right, boundary enclosing use cases)
- **SC-004**: All 5 existing uc fixture tests pass, plus 3 new SVG-specific regression tests
- **SC-005**: The rendered diagram loads without requiring JavaScript or external network requests

## Assumptions

- The PlantUML output is considered the "source of truth" for visual layout — the SVG should match it as closely as possible
- Actors are always positioned on the left side of the diagram, use cases on the right (inside the system boundary)
- The `subject` field on use cases is used to group them into system boundaries; use cases without `subject` go into a default boundary
- The existing directive structure (filter expressions, position dictionaries) is preserved; only coordinate calculations and line endpoints are modified
- Playwright is available for visual regression testing
