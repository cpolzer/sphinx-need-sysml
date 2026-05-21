# Data Model: Use Case Diagram Elements

## Entities

### Actor

Represents a system user or external entity that interacts with use cases.

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique need ID (e.g., `ACTOR-001`) |
| `title` | string | Display name (e.g., "Driver", "Mechanic") |
| `interacts_with` | string | Comma-separated list of UseCase IDs this actor participates in |

**Rendering geometry**:
- Stick figure centered at `(80, ay)` where `ay = 60 + index * 80`
- Circle head: `cx=80, cy=ay, r=10`
- Body: vertical line `(80, ay+10) → (80, ay+25)`
- Arms: horizontal line `(65, ay+15) → (95, ay+15)`
- Legs: two lines from `(80, ay+25)` to `(68, ay+40)` and `(92, ay+40)`
- Connection point for association lines: `(95, ay+15)` (right arm tip)
- Label: `(80, ay+55)` centered below figure

### UseCase

Represents a system capability or goal.

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique need ID (e.g., `USECASE-001`) |
| `title` | string | Display name (e.g., "Start engine", "Diagnose fault") |
| `subject` | string | System boundary label; use cases with same subject share a boundary rectangle |
| `extends` | string | Comma-separated list of UseCase IDs this use case extends |
| `includes` | string | Comma-separated list of UseCase IDs this use case includes |
| `generalizes` | string | Comma-separated list of UseCase IDs this use case generalizes (inherits from) |

**Rendering geometry**:
- Ellipse centered at `(460, uy)` where `uy = 90 + index * 70`
- Dimensions: `rx=120, ry=24`
- Border points for line connections:
  - Top: `(460, uy - 24)`
  - Bottom: `(460, uy + 24)`
  - Left: `(340, uy)`
  - Right: `(580, uy)`
- Label: `(460, uy + 4)` centered inside ellipse

### System Boundary

A rectangle enclosing use cases that share the same `subject` value.

| Field | Type | Description |
|-------|------|-------------|
| `label` | string | The `subject` field value, or "System" if not specified |
| `x` | int | Fixed at 200 |
| `y` | int | Fixed at 40 |
| `width` | int | Fixed at 520 |
| `height` | int | Dynamic: `use_cases.length * 70 + 20` |

### Relationship

Derived from field values on Actor and UseCase entities. Not a standalone entity.

| Type | Source | Target | Visual |
|------|--------|--------|--------|
| Association | Actor `interacts_with` | UseCase | Solid line from actor arm tip to ellipse left border |
| Extend | UseCase `extends` | UseCase | Dashed line, source bottom → target top, `<<extend>>` label |
| Include | UseCase `includes` | UseCase | Dashed line, source bottom → target top, `<<include>>` label |
| Generalize | UseCase `generalizes` | UseCase | Dashed line, source bottom → target top, open triangle arrowhead |

## Validation Rules

- `interacts_with`, `extends`, `includes`, `generalizes` are comma-separated ID lists; each ID must reference an existing need or be silently skipped
- `subject` is free text; empty or null subjects default to "System" boundary label
- Circular references in `extends`/`includes`/`generalizes` are tolerated (rendered as-is, no infinite loop since template iterates once)

## State Transitions

N/A — entities are static data rendered at build time.
