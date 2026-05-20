# Data Model: Full SysML v2 Diagram Coverage

**Date**: 2026-05-20

This document specifies the new need types, fields, and flow configs added in feature `002-full-sysml-diagrams`. It is additive to the data model from [`001-sysml-v2-needs/data-model.md`](../001-sysml-v2-needs/data-model.md); existing types and fields are not changed.

---

## New Need Types

Registered via `add_need_type()` at `config-inited`. Directive names are lowercase. Prefixes follow the word-like convention chosen in spec clarification Q1.

| Directive | Title | ID Prefix | Color | Style | SysML / UML concept | Ships in |
|-----------|-------|-----------|-------|-------|---------------------|----------|
| `transition` | Transition | `TRANS-` | `#EEDDDD` | `node` | State machine transition | v1 |
| `controlflow` | ControlFlow | `CTRLFLOW-` | `#DDEEEE` | `node` | Activity control flow edge | v1 |
| `objectflow` | ObjectFlow | `OBJFLOW-` | `#CCEEDD` | `node` | Activity object/data flow edge | v1 |
| `package` | Package | `PKG-` | `#EEEEFF` | `folder` | Package container | v1 |
| `dependency` | Dependency | `DEP-` | `#DDDDDD` | `node` | Package dependency edge | v1 |
| `usecase` | UseCase | `USECASE-` | `#FFEEDD` | `node` | Use case | v1 |
| `actor` | Actor | `ACTOR-` | `#EEEECC` | `actor` | Actor (external user) | v1 |
| `constraintblock` | ConstraintBlock | `CONSTRAINT-` | `#FFF0DC` | `node` | Constraint block definition | v1 (type only) / v1.1 (rendered) |
| `constraintparameter` | ConstraintParameter | `PARAM-` | `#FFE8C8` | `node` | Constraint parameter | v1 (type only) / v1.1 (rendered) |
| `valueproperty` | ValueProperty | `VALUE-` | `#E8F4FF` | `node` | Quantitative attribute of a part | v1 (type only) / v1.1 (rendered) |
| `bindingconnector` | BindingConnector | `BIND-` | `#D8E8FF` | `node` | Binding between a parameter and a value property | v1 (type only) / v1.1 (rendered) |
| `lifeline` | Lifeline | `LIFELINE-` | `#E0E8F0` | `node` | Sequence diagram participant lifeline | v1 |
| `message` | Message | `MSG-` | `#D0E0F0` | `node` | Sequence diagram message | v1 |

**Total new types**: 13. **Existing types in 001**: 14. **Final type count**: 27.

---

## New Extra Fields

Registered via `add_field()` at `config-inited`. All fields are optional unless noted.

### State-machine fields

| Field | Type | Applicable types | Description |
|---|---|---|---|
| `pseudo_kind` | string enum: `initial`, `final`, `shallowHistory`, `deepHistory`, `choice`, `junction` | StateDef, StateUsage | Pseudostate kind. Absent ⇒ ordinary state. |
| `from_state` | string (need ID) | Transition | Source state of the transition. **Required.** |
| `to_state` | string (need ID) | Transition | Target state of the transition. **Required.** |
| `trigger` | string | Transition | Trigger event name (e.g. `key_on`). |
| `guard` | string | Transition | Guard expression (e.g. `temperature < 90`). |
| `effect` | string | Transition | Effect action name. |

### Activity fields

| Field | Type | Applicable types | Description |
|---|---|---|---|
| `from_action` | string (need ID) | ControlFlow, ObjectFlow | Source action. **Required.** |
| `to_action` | string (need ID) | ControlFlow, ObjectFlow | Target action. **Required.** |
| `object_type` | string | ObjectFlow | Type of the object passed (free text or a need title). |
| `partition` | string | Action, ActionDef | Swimlane name (free text). Actions with the same `partition` group together. |
| `activity_kind` | string enum: `normal`, `decision`, `merge`, `fork`, `join` | Action | Special activity node kind. Default `normal`. |

### Package fields

| Field | Type | Applicable types | Description |
|---|---|---|---|
| `parent_package` | string (need ID) | Package | Parent package for nesting. |
| `kind` | string enum: `use`, `import`, `realize` | Dependency | Kind of dependency. **Required.** |
| `source` | string (need ID) | Dependency | Source of the dependency arrow. **Required.** |
| `target` | string (need ID) | Dependency | Target of the dependency arrow. **Required.** |

### Use case fields

| Field | Type | Applicable types | Description |
|---|---|---|---|
| `subject` | string | UseCase | System boundary label (free text). Use cases sharing a subject group in the diagram. |
| `extends` | string (comma-list of need IDs) | UseCase | Use cases this one extends. |
| `includes` | string (comma-list of need IDs) | UseCase | Use cases this one includes. |
| `generalizes` | string (comma-list of need IDs) | UseCase | Use cases this one generalizes (child → parent). |
| `interacts_with` | string (comma-list of need IDs) | Actor | Use cases the actor participates in. Renderer draws one association line per listed UseCase. **Outgoing from the actor**, matching the source-owns-the-link convention used by `extends`/`includes`/`generalizes`. |

### Sequence fields

| Field | Type | Applicable types | Description |
|---|---|---|---|
| `represents` | string (need ID) | Lifeline | The Part / Actor / Subsystem this lifeline represents. |
| `from_lifeline` | string (need ID) | Message | Source lifeline. **Required.** |
| `to_lifeline` | string (need ID) | Message | Target lifeline. **Required.** |
| `message_kind` | string enum: `sync`, `async`, `return` | Message | Message kind. Default `sync`. |
| `fragment_group` | string | Message | Identifier of the combined-fragment group this message belongs to. Messages sharing a `fragment_group` are wrapped in a single fragment frame. |
| `fragment_kind` | string enum: `alt`, `opt`, `loop`, `par`, `neg`, `critical` | Message | Combined-fragment kind. Honored only on the first message in a `fragment_group`; subsequent messages inherit. |
| `fragment_guard` | string | Message | Guard expression printed in the fragment header. |

### Parametric fields

| Field | Type | Applicable types | Description |
|---|---|---|---|
| `expression` | string | ConstraintBlock | Plain-text expression describing the constraint (e.g. `fuel = output * duration / efficiency`). Per spec Q4, plain text only — no math typesetting. |
| `parameters` | string (comma-list of need IDs) | ConstraintBlock | The `ConstraintParameter` IDs owned by this block. |
| `value_type` | string | ValueProperty | Type name (e.g. `kW`, `s`, `L`). |
| `default_value` | string | ValueProperty | Default value as a string. |
| `unit` | string | ValueProperty, BindingConnector | Unit label printed on binding arrows in the parametric diagram. |
| `source_parameter` | string (need ID) | BindingConnector | The constraint parameter end of the binding. **Required.** |
| `target_value` | string (need ID) | BindingConnector | The value property end of the binding. **Required.** |

**Total new fields**: 34. Tally per category: state-machine 6, activity 5, package 4, use-case 5, sequence 7, parametric 7. (An earlier draft tallied 26 by undercounting the activity, sequence, and parametric groups; `interacts_with` on Actor was added separately per remediation of analyze finding U1.)

---

## Field Reuse Across Existing Types

The new fields above are additive — existing fields (`abstract`, `owned_by`, `multiplicity`, `direction`, `conjugated`, `definition`, `satisfies`, `refines`, `allocates`, `source_port`, `target_port`, `is_initial`, `is_final`) remain unchanged in semantics and applicability.

Note that `is_initial` / `is_final` continue to work for backwards compatibility but are now subsumed by `pseudo_kind`: a state with `is_initial: true` is rendered identically to one with `pseudo_kind: initial`. The renderer recognizes both forms. Documentation will recommend `pseudo_kind` for new models.

---

## New `needs_flow_configs` Entries

Mutated into `app.config.needs_flow_configs` at `builder-inited`, preserving any user overrides.

| Config Key | Applies To | Content |
|---|---|---|
| `sysml_stm` | State machine diagrams | skinparam for `state` and pseudostate nodes |
| `sysml_act` | Activity diagrams | skinparam for `activity` mode (partition styling, decision diamonds) |
| `sysml_sd` | Sequence diagrams | skinparam for `participant`, message arrows, combined-fragment frames |
| `sysml_uc` | Use case diagrams | skinparam for `actor`, `usecase`, system-boundary rectangle |
| `sysml_pkg` | Package diagrams | skinparam for `package` nesting and dependency arrows |
| `sysml_par` | Parametric diagrams | skinparam for `class<<constraint>>` and binding arrows |

The placeholder keys `sysml_act` and `sysml_stm` reserved in feature 001 are now filled with real content.

---

## New Jinja2 Template Constants

Added to `sphinxcontrib/sysml/templates.py`:

- `STM_FULL_TEMPLATE` — root state defining element → all owned states + pseudostates + transitions.
- `ACT_FULL_TEMPLATE` — root action defining element → all owned actions (grouped by `partition`) + control/object flows + decision/fork nodes.
- `SD_FULL_TEMPLATE` — root sequence (typically an ActionDef or InteractionDef) → all lifelines + messages + combined fragments.
- `UC_FULL_TEMPLATE` — filter over `type == 'UseCase'` → use cases grouped by `subject` + actors + extends/includes/generalizes.
- `PKG_FULL_TEMPLATE` — root package → nested packages + dependency arrows.
- `PAR_FULL_TEMPLATE` (v1.1) — constraint block + parameters + bound value properties.

Added to a new `sphinxcontrib/sysml/svg_templates.py`:

- `STM_SVG_TEMPLATE`, `ACT_SVG_TEMPLATE`, `SD_SVG_TEMPLATE`, `UC_SVG_TEMPLATE`, `PKG_SVG_TEMPLATE`, `IBD_SVG_TEMPLATE` (promotion), `PAR_SVG_TEMPLATE` (v1.1) — each rendered through the `Needsvg` placeholder pipeline as documented in `research.md § 2`.

The `BDD_SVG_TEMPLATE` already inlined in `needsysml_svg.py` is moved to `svg_templates.py` for consistency, leaving `needsysml_svg.py` as a thin directive shell.

---

## Relationships Summary

```text
ActionDef "activity"
   └── Action (partition="Driver" | "ECU" | …)
         ←── ControlFlow.from_action / .to_action
         ←── ObjectFlow.from_action / .to_action (typed by object_type)

StateDef "state machine"
   ├── StateUsage (pseudo_kind=initial|final|…|None)
   └── Transition.from_state / .to_state (+ trigger, guard, effect)

Package
   └── Package (parent_package = parent's ID)
       └── (any need can be owned_by this package via existing owned_by field)
   ←── Dependency.source / .target / .kind ∈ {use, import, realize}

UseCase (subject="Vehicle")
   ←── Actor.interacts_with (comma-list of UseCase IDs) — solid association line per listed UC
   ←── UseCase.extends / .includes / .generalizes — UC-to-UC relationships (dashed labelled arrows)

Lifeline (represents = a Part/Actor ID)
   ←── Message.from_lifeline / .to_lifeline
            (message_kind ∈ {sync, async, return})
            (fragment_group + fragment_kind ∈ {alt, opt, loop, par, neg, critical})

ConstraintBlock
   └── ConstraintParameter (linked via parameters comma-list on the block)
   ←── BindingConnector.source_parameter → .target_value
         (unit labels the arrow in the parametric diagram)
ValueProperty (value_type, default_value, unit; owned_by a Part)
```

---

## Validation Rules

Validation is split across two layers:

1. **Shape and enum validation** — handled automatically by sphinx-needs at need-parse time, driven by the `schema` argument passed to `add_field()`. Fields declared with `schema: {"type": "string", "enum": [...]}` (e.g. `pseudo_kind`, `message_kind`, `fragment_kind`, `activity_kind`, `kind`) reject out-of-enum values before the directive renderers ever see them. No extra code in the directives is needed.
2. **Reference resolution** — handled by the directive renderers using the shared `warn_unknown_ref()` helper (per tasks.md T009b). Each diagram emits a categorized warning + placeholder when a need-ID field references a missing target:

| Check | Warning category | Trigger |
|---|---|---|
| `Transition.from_state` / `.to_state` references unknown need | `[needsysml.stm.unknown-state]` | Build emits warning; diagram renders the transition with `??` placeholder at the unknown end. |
| `ControlFlow` / `ObjectFlow` references unknown action | `[needsysml.act.unknown-action]` | Same |
| `Message.from_lifeline` / `.to_lifeline` references unknown lifeline | `[needsysml.sd.unknown-lifeline]` | Same |
| `Dependency.source` / `.target` references unknown package | `[needsysml.pkg.unknown-target]` | Same |
| `UseCase.extends` / `.includes` / `.generalizes` / `Actor.interacts_with` references unknown use case | `[needsysml.uc.unknown-target]` | Same |
| `BindingConnector.source_parameter` references unknown parameter, or `.target_value` references unknown value property | `[needsysml.par.unknown-binding]` | Same |

This implements FR-016 (visible warning + placeholder, not build failure).

---

## Backwards Compatibility

- Existing 14 need types and 13 existing fields are unchanged.
- `is_initial` / `is_final` continue to work; new code may use `pseudo_kind` interchangeably.
- `needsysml-req`'s positional filter argument continues to work; the new `:filter:` option is additive.
- All new directives are net-new — no existing directive is renamed or removed.
- Engineers upgrading from 0.2.4 → 0.3.0 → 0.4.0 do not need to edit existing models. They only need to add the new conf.py entry (none — the extension auto-registers the new types) and start using the new directives if desired.
