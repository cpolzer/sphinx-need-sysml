# Feature Specification: Full SysML v2 Diagram Coverage

**Feature Branch**: `002-full-sysml-diagrams`

**Created**: 2026-05-20

**Status**: Draft

**Input**: User description: "Cover all SysML v2 diagram types in the sphinxcontrib-sysml extension. Today the extension supports Block Definition (bdd), Internal Block (ibd), and Requirements (req) diagrams, but engineers writing SysML models also need State Machine (stm), Activity (act), Sequence (sd), Use Case (uc), Package (pkg), Parametric (par), and an Allocation matrix view. Engineers should be able to declare every SysML v2 modeling element as a sphinx-needs item — so it is queryable and traceable from sphinx-needs tables and roles — and render every standard SysML diagram type from that model. Each diagram should be available in two rendering paths: an auto-laid-out PlantUML rendering and a precise inline-SVG rendering with clickable need links. Fidelity should be production-grade: state machines must support nested/composite states, history pseudostates, and transitions with trigger/guard/effect; activity diagrams must support swimlane partitions, fork/join, decision/merge, and object flow; sequence diagrams must support all combined fragments (alt, opt, loop, par, neg, critical) and sync/async/return messages; use cases must support extends/includes/generalization and a system-boundary subject; package diagrams must distinguish dependency kinds (use, import, realize) and support nested packages; parametric diagrams must support constraint blocks with parameters, value properties, and binding connectors with units. The example documentation should demonstrate every new diagram in one coherent model, with auto-layout and precise variants side by side."

## Clarifications

### Session 2026-05-20

- Q: ID prefixes for the 13 new element types? → A: Word-like prefixes (Option B): `TRANS-` Transition, `CTRLFLOW-` ControlFlow, `OBJFLOW-` ObjectFlow, `PKG-` Package, `DEP-` Dependency, `USECASE-` UseCase, `ACTOR-` Actor, `CONSTRAINT-` ConstraintBlock, `PARAM-` ConstraintParameter, `VALUE-` ValueProperty, `BIND-` BindingConnector, `LIFELINE-` Lifeline, `MSG-` Message.
- Q: Which state pseudostate kinds must the state machine support? → A: Common production set (Option B): initial, final, shallow history (`H`), deep history (`H*`), choice (`◆`), junction (`•`). Fork, join, terminate, entry-point and exit-point pseudostates are out of scope for this feature.
- Q: Allocation matrix axes — fixed or flexible? → A: Flexible with defaults (Option B): the matrix directive exposes `:rows:` and `:columns:` options accepting filter expressions; defaults are "needs that have `allocates`" (rows) and "needs referenced by `allocates`" (columns). One directive covers requirement-to-part, action-to-part, and any other allocation view.
- Q: Constraint expression representation in parametric diagrams? → A: Single plain-text `expression` field (Option A). Engineers needing rendered math notation use Sphinx's existing `:math:` role or a math admonition in surrounding prose; the constraint block element itself stores only the plain-text expression, keeping the data model queryable.
- Q: MVP scope for the initial release? → A: Two-phase release (Option C). v1 ships P1 + P2 (state machine, activity, sequence, use case, package = five stories). v1.1 ships P3 (allocation matrix, parametric = two stories). Internal task ordering still follows P1 → P2 → P3.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - State Machine Modeling for Safety-Critical Behavior (Priority: P1)

A systems engineer documenting an embedded controller needs to capture lifecycle states of a component (e.g. an engine: `Off`, `Starting`, `Running`, `Stopping`) and the transitions between them, including the events that trigger transitions, guard conditions, and entry/exit/do effects. The engineer wants every state and transition to be a first-class, queryable item in the documentation so reviewers can trace requirements directly to state behaviors, and they want a rendered state diagram embedded next to the textual description.

**Why this priority**: State machines are the highest-value behavioral artifact in safety-critical and embedded SysML modeling. The extension already registers state types but cannot draw transitions or composite states today, which blocks the most common SysML behavioral analysis workflow.

**Independent Test**: The engineer writes a state machine for the engine in the vehicle example (states + transitions), runs the documentation build, and confirms (a) a rendered state diagram appears, (b) every state and transition is listed in a needs table, (c) clicking a state in the diagram navigates to its definition in the page.

**Acceptance Scenarios**:

1. **Given** an engine with four lifecycle states and transitions between them, **When** the engineer declares them as needs and adds a state machine diagram directive referencing the state-defining element, **Then** the rendered output shows all four states connected by transitions labelled with their triggers, guards, and effects.
2. **Given** a composite state ("Running") that contains sub-states ("Idle", "Loaded"), **When** the engineer declares the parent–child relationship in needs, **Then** the rendered diagram shows the sub-states nested visually inside the parent state.
3. **Given** a transition with a guard condition, **When** the diagram is rendered, **Then** the guard is displayed in brackets next to the trigger.
4. **Given** a composite state with a shallow-history pseudostate, **When** the diagram is rendered, **Then** the history pseudostate is drawn with an `H` marker inside the composite state.
5. **Given** two outgoing transitions from a choice pseudostate with different guard expressions, **When** the diagram is rendered, **Then** the choice is drawn as a diamond and each outgoing transition is labelled with its guard.

---

### User Story 2 - Activity Flow for Operational Behavior (Priority: P1)

A systems engineer documenting how the system performs an operation (e.g. "Start Engine" or "Process Order") needs to capture the sequence of actions, the control flow between them, decision points, parallel branches (fork/join), and which actor or subsystem owns each action (swimlane partitions). The engineer wants both control flow and object flow (data passed between actions), and wants the resulting activity diagram embedded in the documentation.

**Why this priority**: Activity diagrams are the second pillar of behavioral modeling and are required for operational and functional analysis. The extension already registers action types but cannot draw flows or swimlanes today.

**Independent Test**: The engineer writes an activity ("Start Engine") with five actions across two swimlanes, runs the build, and confirms the rendered activity diagram shows the actions in their swimlanes connected by control-flow arrows, including a decision diamond.

**Acceptance Scenarios**:

1. **Given** four actions in sequence, **When** the engineer declares control flows between them, **Then** the diagram renders them in order with directional arrows.
2. **Given** an activity with two parallel branches joined later, **When** the engineer declares fork and join nodes, **Then** the diagram shows the parallel branches with a fork bar and a join bar.
3. **Given** actions assigned to different swimlanes (e.g. "Driver" vs "ECU"), **When** the diagram is rendered, **Then** the actions appear under the correct vertical or horizontal partition.
4. **Given** an action that produces an output consumed by another action, **When** the engineer declares an object flow between them, **Then** the diagram shows a labelled object node on the flow.

---

### User Story 3 - Sequence Interaction for Cross-Component Scenarios (Priority: P2)

A systems engineer documenting an interaction between components (e.g. "key-on ignition sequence") needs to show participants as lifelines, the messages exchanged between them (synchronous calls, asynchronous signals, returns), and the structured fragments that govern message flow (alternative paths, optional sequences, loops, parallel sections). The engineer wants a rendered sequence diagram that captures the protocol precisely.

**Why this priority**: Sequence diagrams are the primary tool for documenting cross-component scenarios and protocols, especially during integration and acceptance. Less universally needed than state and activity but still essential for many real systems.

**Independent Test**: The engineer writes a sequence with three lifelines and six messages including one alt fragment and one loop fragment, runs the build, and confirms the rendered diagram shows the lifelines as parallel vertical lines with the messages as labelled arrows, the alt fragment as a labelled frame with a divider for the else branch, and the loop fragment as a labelled frame.

**Acceptance Scenarios**:

1. **Given** three lifelines and a synchronous message from one to another, **When** rendered, **Then** the message appears as a solid-arrowed labelled arrow between the lifelines.
2. **Given** an asynchronous message and a return message, **When** rendered, **Then** the async appears with an open arrowhead and the return appears as a dashed arrow.
3. **Given** an alt fragment containing two message blocks with a guard, **When** rendered, **Then** the fragment shows the keyword "alt", the guard expression, and a horizontal divider between branches.
4. **Given** a loop fragment with a guard, **When** rendered, **Then** the fragment shows the keyword "loop" and the guard expression.

---

### User Story 4 - Use Case Modeling for Stakeholder Analysis (Priority: P2)

A systems engineer kicking off a project needs to document the actors who interact with the system and the use cases each actor participates in, including relationships between use cases (one extends another, one includes another, one generalizes another), all within a clearly drawn system boundary. The engineer wants the use case diagram embedded next to the actor descriptions.

**Why this priority**: Use case diagrams establish system scope and stakeholder relationships. Widely taught and expected in SysML toolchains, but conceptually simpler than the behavioral diagrams above.

**Independent Test**: The engineer declares two actors ("Driver", "Mechanic"), four use cases inside a "Vehicle" system boundary, plus one extend and one include relationship, runs the build, and confirms the rendered diagram shows the actors as stick figures outside the boundary connected by lines to the use case ellipses inside the boundary.

**Acceptance Scenarios**:

1. **Given** an actor and a use case, **When** the engineer declares an association between them, **Then** the diagram shows a solid line between the actor stick figure and the use case ellipse.
2. **Given** a use case A that extends a use case B, **When** rendered, **Then** the diagram shows a dashed arrow from A to B labelled `<<extend>>`.
3. **Given** a use case A that includes a use case B, **When** rendered, **Then** the diagram shows a dashed arrow from A to B labelled `<<include>>`.
4. **Given** a system boundary with a name, **When** rendered, **Then** all the use cases appear inside a labelled rectangle representing the boundary.

---

### User Story 5 - Package Organization for Large Models (Priority: P2)

A systems engineer working on a large model needs to group related elements into packages, nest packages within packages, and document dependencies between packages (which packages use, import, or realize others). The engineer wants the package structure to be queryable like any other need and rendered as a package diagram.

**Why this priority**: Package organization becomes essential once a model grows past a few dozen elements. Lower priority than behavioral diagrams because today's users can work around it with section headings, but increasingly painful as models scale.

**Independent Test**: The engineer declares three packages with parent–child nesting and two cross-package dependencies (one `<<use>>`, one `<<import>>`), runs the build, and confirms the rendered diagram shows nested package rectangles with labelled dependency arrows.

**Acceptance Scenarios**:

1. **Given** two top-level packages, **When** declared as needs, **Then** the rendered diagram shows them as labelled rectangles.
2. **Given** a child package owned by a parent package, **When** rendered, **Then** the child is drawn nested inside the parent's rectangle.
3. **Given** a dependency declared from package A to package B with kind "import", **When** rendered, **Then** a dashed arrow appears from A to B labelled `<<import>>`.

---

### User Story 6 - Allocation Traceability Matrix (Priority: P3, deferred to v1.1)

A systems engineer reviewing how requirements are allocated to structural elements (and how behaviors are allocated to structure) needs a tabular matrix view rather than a node-link diagram. The engineer wants to see, at a glance, which requirements/behaviors are allocated to which parts, and to query that mapping.

**Why this priority**: A nice-to-have once requirements and structural elements exist. Lower priority because the underlying `allocates` field already lets engineers query the data via needs tables — this story is about a dedicated matrix view.

**Independent Test**: The engineer declares four requirements, three of which use `allocates` to point at structural parts, runs the build, and confirms a matrix renders with requirements as rows, parts as columns, and check marks at the intersections.

**Acceptance Scenarios**:

1. **Given** four requirements with allocation links to three parts, **When** the engineer adds an allocation matrix directive with no axis options, **Then** the rendered matrix shows requirements as rows and parts as columns with markers at allocated intersections.
2. **Given** a requirement without any allocations, **When** the matrix is rendered, **Then** the requirement's row contains no markers.
3. **Given** an engineer wants to view action-to-part allocations instead of requirement-to-part, **When** they invoke the directive with `:rows: type == 'Action'` and `:columns: type == 'Part'`, **Then** the rendered matrix shows actions as rows and parts as columns with markers at allocated intersections.

---

### User Story 7 - Parametric Constraints for Quantitative Analysis (Priority: P3, deferred to v1.1)

A systems engineer modeling a quantitative constraint (e.g. "fuel consumption = engine output × duration ÷ efficiency") needs to capture the mathematical relationship as a constraint block, its parameters, and the value properties on parts that bind to those parameters. The engineer wants a parametric diagram that shows the constraint block surrounded by the value properties bound to its parameters.

**Why this priority**: Parametric modeling is powerful for quantitative analysis but used by a smaller audience than the other diagram types. It also requires the largest set of new element types, making it the highest-cost story. Implementing it last lets earlier stories validate the underlying infrastructure first.

**Independent Test**: The engineer declares one constraint block with three parameters, three value properties on parts, and binding connectors between them. The engineer runs the build and confirms the rendered diagram shows the constraint block as a rounded rectangle with parameter ports around its edge, connected by lines to value-property nodes.

**Acceptance Scenarios**:

1. **Given** a constraint block with three parameters and a plain-text expression, **When** rendered, **Then** the diagram shows the constraint as a rounded rectangle with three labelled parameter ports and the expression text inside the rectangle.
2. **Given** a binding connector from a parameter to a value property with a stated unit, **When** rendered, **Then** the connection line is labelled with the unit.

---

### Edge Cases

- A diagram directive references a need ID that does not exist → the diagram renders with a clearly marked "unknown reference" placeholder rather than failing the build.
- A diagram has no matching child elements (empty BDD, empty package, etc.) → the diagram renders with an explicit "no children" placeholder rather than producing an empty area.
- An engineer mixes auto-layout and precise-layout variants of the same diagram on the same page → both render independently without interfering with each other.
- The precise-layout renderer is not installed → directives that have only an auto-layout path continue to work; the precise variants emit a clear "renderer not installed" message rather than an extension error.
- A composite state contains another composite state (nested 3+ levels deep) → the rendered diagram preserves nesting; if depth exceeds what is visually reasonable, the diagram is still legible.
- Two diagrams on the same page reference overlapping subsets of needs → both render correctly and clickable links from either diagram navigate to the same anchor.
- An activity has actions outside any swimlane → those actions render outside the partitions.

## Requirements *(mandatory)*

### Functional Requirements

**Element type declarations**

- **FR-001**: Engineers MUST be able to declare every SysML v2 modeling element listed below as a sphinx-needs item, with each element receiving the following unique ID prefix (word-like, distinct from the existing 1–3 letter prefixes used by the 14 already-registered types):
  - Transition → `TRANS-`
  - ControlFlow → `CTRLFLOW-`
  - ObjectFlow → `OBJFLOW-`
  - Package → `PKG-`
  - Dependency → `DEP-`
  - UseCase → `USECASE-`
  - Actor → `ACTOR-`
  - ConstraintBlock → `CONSTRAINT-`
  - ConstraintParameter → `PARAM-`
  - ValueProperty → `VALUE-`
  - BindingConnector → `BIND-`
  - Lifeline → `LIFELINE-`
  - Message → `MSG-`
- **FR-002**: Engineers MUST be able to attach the following attributes to elements:
  - States: optional pseudostate kind, drawn from `initial`, `final`, `shallowHistory`, `deepHistory`, `choice`, `junction`. A state without a pseudostate kind is a normal state.
  - Transitions: source state, target state, trigger event, guard expression, effect action.
  - Control and object flows: source action, target action; for object flows additionally a passed-object type.
  - Packages: parent package (for nesting); dependencies: source, target, kind ("use" / "import" / "realize").
  - Use cases: subject (system boundary), extends, includes, generalizes.
  - Actors: `interacts_with` — a comma-separated list of `USECASE-` IDs the actor participates in. The renderer draws one solid line per listed use case.
  - Constraint blocks: parameter list, plain-text `expression` (e.g. `fuel = output * duration / efficiency`); binding connectors: source parameter, target value property, unit; value properties: type, default value.
  - Lifelines: represented element; messages: source lifeline, target lifeline, kind ("sync" / "async" / "return"), guard, fragment.
- **FR-003**: All new element types MUST be queryable via the same filter expressions and table directives that work for existing element types, so engineers can list, filter, or count them like any other need.

**Diagram rendering — auto-layout path**

- **FR-004**: System MUST provide an auto-layout state machine diagram directive that takes a state-defining element as the root and renders all owned states and the transitions between them, with composite states shown as nested rectangles and pseudostates rendered with their UML notation (filled dot for `initial`, ringed dot for `final`, `H` for `shallowHistory`, `H*` for `deepHistory`, diamond for `choice`, small filled circle for `junction`).
- **FR-005**: System MUST provide an auto-layout activity diagram directive that renders actions, control flows, decision/merge nodes, fork/join nodes, and object flows, with optional swimlane partitions per actor or subsystem.
- **FR-006**: System MUST provide an auto-layout sequence diagram directive that renders lifelines as vertical lines, messages as horizontal arrows between them, and combined fragments (alt, opt, loop, par, neg, critical) as labelled boxes around the contained messages.
- **FR-007**: System MUST provide an auto-layout use case diagram directive that renders actors outside a system boundary, use cases inside the boundary, and the extends / includes / generalization relationships between use cases.
- **FR-008**: System MUST provide an auto-layout package diagram directive that renders packages as nested rectangles and labelled dependency arrows between them.
- **FR-009**: System MUST provide an auto-layout parametric diagram directive that renders a constraint block with its parameters and the bound value properties.
- **FR-010**: System MUST provide an allocation matrix directive that renders a tabular matrix with allocators on one axis, allocation targets on the other, and markers at allocated intersections. The directive MUST accept two filter-expression options (`:rows:` and `:columns:`) that select which needs occupy each axis. When the options are omitted, the directive MUST default to "needs that have a non-empty `allocates` field" on the row axis and "needs referenced by any `allocates` value" on the column axis, so the common requirement→part view requires no options.

**Diagram rendering — precise-layout path**

- **FR-011**: For every diagram type defined in FR-004 through FR-009, system MUST additionally provide a precise-layout variant that produces inline content with clickable links from every diagram element to the corresponding need definition's anchor in the same document.
- **FR-012**: Both rendering paths MUST be invokable from the same documentation source without conflict, and MUST be selectable independently per diagram instance.

**Traceability and integration**

- **FR-013**: Every node drawn in any auto-layout diagram MUST be a clickable link to the corresponding need anchor when the documentation output supports hyperlinked images.
- **FR-014**: Every node drawn in any precise-layout diagram MUST be a clickable link to the corresponding need anchor regardless of output format.
- **FR-015**: All new diagram directives MUST be discoverable from the existing documentation index (the same place engineers look up bdd / ibd / req today).

**Error handling**

- **FR-016**: When a diagram directive references a need ID that does not exist, the build MUST complete with a visible warning (categorized so users can suppress per diagram via `suppress_warnings`) and the rendered output MUST show an explicit "unknown reference" marker at the position the element would have occupied. Every diagram directive MUST use the same shared warning + placeholder helpers so the behavior is uniform across diagrams (see data-model.md § "Validation Rules" for the category names).
- **FR-017**: When the precise-layout renderer is not installed, the auto-layout variants MUST continue to work, and the precise variants MUST emit a clear "renderer not installed" message at the directive's location rather than aborting the build.
- **FR-018**: When a diagram has no matching child elements, the rendered output MUST show an explicit "no children" placeholder rather than an empty area and MUST emit one informational warning (category `[needsysml.<diagram>.empty]`). Every diagram directive MUST use the same shared empty-result helper so the placeholder text and warning category are consistent across diagrams.

**Verification**

- **FR-019**: Each new diagram directive MUST have an automated build-and-assert test confirming that the directive builds without error and that an expected need ID from the test fixture appears in the rendered output.

**Demonstration**

- **FR-020**: The repository's existing worked example (the vehicle system) MUST be extended to demonstrate every new diagram type using a single coherent model, with the auto-layout and precise-layout variants of each diagram shown side by side.

### Key Entities

- **Transition**: A directed move from one state to another, owned by the source state, carrying optional trigger, guard, and effect attributes.
- **ControlFlow**: A directed sequencing relationship between two actions inside an activity.
- **ObjectFlow**: A directed data-passing relationship between two actions, optionally typed by the object being passed.
- **Package**: A grouping container for other needs; may nest. Has no own behavior beyond organization.
- **Dependency**: A directed relationship between two packages (or other elements) with a kind discriminator (`use` / `import` / `realize`).
- **UseCase**: A user-facing scenario the system performs, owned by a system boundary, with optional `extends` / `includes` / `generalizes` links to other use cases.
- **Actor**: An external entity that interacts with a system to perform use cases. Carries an `interacts_with` field listing the use cases the actor participates in.
- **ConstraintBlock**: A definition of a mathematical or logical constraint, with a list of typed parameters and a plain-text expression describing the relationship.
- **ConstraintParameter**: A typed input/output slot of a constraint block.
- **ValueProperty**: A quantitative attribute of a part with a type and unit.
- **BindingConnector**: A directed binding from a constraint parameter to a value property, carrying a unit.
- **Lifeline**: A vertical line in a sequence diagram representing one participating element over time.
- **Message**: A communication between two lifelines, with a kind (`sync` / `async` / `return`), optional guard, and optional enclosing fragment.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All nine SysML v2 diagram categories (bdd, ibd, req, stm, act, sd, uc, pkg, par) plus the allocation matrix are renderable from a sphinx-needs model — no diagram category is missing.
- **SC-002**: Every new diagram type can be rendered in two modes (auto-layout and precise-layout) — engineers have a consistent choice across all diagrams.
- **SC-003**: At least one worked example (the vehicle system) demonstrates all ten diagram views (nine SysML + allocation) in a single page, building cleanly with no warnings under the strict documentation build.
- **SC-004**: Every drawn node in every diagram links to its source need definition — measured by counting clickable anchors in the rendered output for the vehicle example (target: 100% of element drawings).
- **SC-005**: An engineer unfamiliar with the extension can add a new state machine (one defining element + three states + three transitions) and see it rendered with no boilerplate other than the directive call — measured by counting lines of source needed (target: under 25 lines including state and transition declarations).
- **SC-006**: Each new diagram directive has at least one automated smoke test that asserts both successful build and content correctness, matching the existing test pattern for bdd / ibd / req — measured at 100% coverage of new directives.
- **SC-007**: Adding the new element types and diagrams does not regress any existing diagram, table, or filter — measured by the existing test suite continuing to pass at its prior pass rate.
- **SC-008**: The full vehicle example renders in under 30 seconds on a developer workstation — measured as the wall-clock time of a clean documentation build.

## Assumptions

- Engineers using the extension are already familiar with the existing sphinxcontrib-sysml conventions (Def vs Usage naming, ID prefix conventions, owned_by composition, satisfies/refines/allocates traceability links).
- The existing auto-layout renderer (PlantUML via sphinx-needs' needuml) and the existing precise-layout renderer (sphinx-need-svg) are the canonical implementations for the two rendering paths. Adding additional renderers is out of scope for this feature.
- All new diagram types follow the same wrapping pattern as the existing bdd / ibd / req directives: a directive wrapping a Jinja template that targets the underlying renderer.
- The new element types follow SysML v2 naming where appropriate; element kinds that exist only in SysML v1 (e.g. `UseCase`, `Lifeline`, `Message`) keep their v1 names since SysML v2 does not redefine them.
- The vehicle example continues to use a single source file (no split into per-diagram example files) so engineers see the entire SysML coverage demonstrated as one coherent model.
- Smoke tests follow the existing pytest layout (one test file per directive, build a minimal fixture page, assert no error and content presence).
- Output formats other than HTML (e.g. PDF, ePub) are best-effort: clickable links and SVG behavior may degrade. Full multi-format parity is out of scope.
- Internationalization and right-to-left language support for diagram labels is out of scope; labels render in the source language of the needs.
- Performance optimization for very large models (thousands of elements) is out of scope; the target is documentation-scale models (hundreds of elements).
- The constitution and existing extension architecture (single Sphinx extension, sphinx-needs as the data model, optional sphinx-need-svg for precise rendering) are preserved.
- Release is two-phase: v1 includes User Stories 1–5 (P1 + P2: state machine, activity, sequence, use case, package). v1.1 includes User Stories 6–7 (P3: allocation matrix, parametric). The new element types and fields required by v1.1 (ConstraintBlock, ConstraintParameter, ValueProperty, BindingConnector) may still be registered in v1 to keep the data model stable, even though their diagram directives ship in v1.1.
