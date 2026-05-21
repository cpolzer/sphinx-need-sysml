# Research: Use Case Diagram SVG Alignment

## Decision 1: Ellipse border intersection for association lines

**Context**: Actors are at x=80 (stick figures ~20px wide). Use case ellipses are centered at x=460 with rx=120, ry=24. Association lines must connect from the actor's right edge to the ellipse's left border.

**Rationale**: The current template uses `x1=ap[0]+20, x2=up[0]-120` which assumes the ellipse left edge is always at `center_x - rx`. This is correct for horizontal lines but fails when actors and use cases are at different y-positions (diagonal lines). For diagonal lines, the intersection point on the ellipse border must be computed using the ellipse equation.

**Approach**: For a line from point P(px, py) to ellipse center C(cx, cy) with radii (rx, ry), the intersection point on the ellipse border is:
```
dx = cx - px, dy = cy - py
t = 1 / sqrt((dx/rx)^2 + (dy/ry)^2)
ix = cx - dx * t, iy = cy - dy * t
```
This gives the exact border intersection point. For the actor-to-ellipse case, we compute the intersection on the ellipse side (target) and use the actor's rightmost point (x=95, the arm tip) as the source.

**Alternatives considered**:
- Approximate with fixed offsets (current approach) — rejected because it produces floating lines for diagonal connections
- Use SVG `marker-end` with ellipse hit testing — rejected because it requires JavaScript or complex SVG filters

## Decision 2: Actor stick-figure bounding box

**Context**: The current stick figure uses: circle at (80, ay) r=10, body line (80, ay+10)→(80, ay+25), arm line (65, ay+15)→(95, ay+15), legs (80, ay+25)→(68, ay+40) and (80, ay+25)→(92, ay+40).

**Rationale**: The rightmost point of the stick figure is the arm tip at x=95. The vertical span is ay (circle top at ay-10) to ay+40 (leg bottom). For association line purposes, the connection point should be the arm tip (95, ay+15) — this is the natural "handshake" point and matches PlantUML's actor connection semantics.

**Approach**: Store actor connection point as `[95, ay + 15]` (arm tip) instead of `[80, ay + 20]` (body center). This is a single coordinate change — no geometry computation needed since the actor is a fixed shape.

## Decision 3: Extend/include/generalizes line geometry

**Context**: Current extend/include lines use `y1=src[1]-24, y2=dst[1]+24` which assumes ellipses are vertically stacked at fixed 70px intervals. This works for same-column ellipses but produces incorrect angles when use cases are at different vertical positions.

**Rationale**: Use cases are all at the same x=460, so extend/include lines are always vertical (or near-vertical). The current approach of connecting top of source ellipse to bottom of target ellipse is correct for vertical lines. However, the label positioning `x=(src[0]+dst[0])//2+20` places the label 20px to the right of center, which may overlap with the system boundary edge.

**Approach**: Keep the vertical line geometry (top-to-bottom) since all use cases share the same x-coordinate. Adjust label positioning to `x=src[0]+12` (just inside the ellipse right edge) for better readability. For `generalizes`, use the same pattern but with an open triangle arrowhead at the target end (SVG `<polygon>` with `fill="none"`).

**Alternatives considered**:
- Compute exact ellipse-to-ellipse border intersections for all relationship types — rejected as overkill since use cases are vertically aligned; top/bottom points are sufficient
- Use SVG `<marker>` elements for arrowheads — rejected because markers require defs section and add complexity; inline polygons are simpler and match the existing template style

## Decision 4: Dynamic viewBox height calculation

**Context**: Current formula: `(actors | length + use_cases | length) * 40 + 80`. This underestimates for large diagrams.

**Rationale**: Each actor needs ~80px vertical space (stick figure + label). Each use case needs ~70px (ellipse + spacing). The system boundary needs ~40px header. Margins need ~40px top + ~40px bottom.

**Approach**: New formula: `max(actors | length * 80, use_cases | length * 70 + 60) + 80`. This takes the taller of the actor column or use case column, adds boundary header and margins. For the current fixture (2 actors, 4 use cases): `max(160, 340) + 80 = 420`.

**Alternatives considered**:
- Fixed viewBox (current 760x~300) — rejected because it clips large diagrams
- Separate viewBox for actors and use cases — rejected because it complicates the layout

## Decision 5: `generalizes` arrow rendering

**Context**: PlantUML renders `generalizes` as `<|--` (open triangle arrowhead pointing to the generalized use case). The SVG template currently has no `generalizes` support.

**Rationale**: The SVG should match PlantUML's visual output. An open triangle (hollow arrowhead) is the standard UML notation for generalization/inheritance.

**Approach**: Render as a dashed line from child ellipse bottom to parent ellipse top, with an open triangle polygon at the parent end. The triangle points: `(cx, top_y)` (tip), `(cx-6, top_y+10)` (left base), `(cx+6, top_y+10)` (right base), with `fill="none" stroke="#444"`.

**Alternatives considered**:
- Solid line with filled arrowhead — rejected because UML standard uses open/hollow arrowhead for generalization
- Text label `<<generalize>>` — rejected because the arrowhead itself conveys the relationship type; no label needed
