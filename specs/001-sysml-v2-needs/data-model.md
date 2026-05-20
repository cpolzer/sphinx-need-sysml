# Data Model: SysML v2 sphinx-needs Extension

**Date**: 2026-05-20

---

## Need Types

All types registered via `add_need_type()` at `config-inited`. Directive names are lowercase with no underscores to match sphinx-needs convention.

### Structural Types

| Directive | Title | ID Prefix | Color | Style | SysML v2 Concept |
|-----------|-------|-----------|-------|-------|-----------------|
| `partdef` | PartDef | `PD-` | `#DDEEFF` | `node` | `part def` — a block/part type definition |
| `part` | Part | `P-` | `#BBDDFF` | `node` | `part` — an instance/usage of a PartDef |
| `portdef` | PortDef | `POD-` | `#FFEECC` | `node` | `port def` — a typed port definition |
| `port` | Port | `PO-` | `#FFE0AA` | `node` | `port` — a port usage on a Part |
| `interfacedef` | InterfaceDef | `IFD-` | `#DDEEDD` | `node` | `interface def` — a connection interface type |
| `interface` | Interface | `IF-` | `#BBDDBB` | `node` | `interface` — an interface usage |
| `connectiondef` | ConnectionDef | `CD-` | `#EEDDFF` | `node` | `connection def` — a typed connector |
| `connection` | Connection | `C-` | `#DDCCFF` | `node` | `connection` — a connector instance |

### Behavioral Types

| Directive | Title | ID Prefix | Color | Style | SysML v2 Concept |
|-----------|-------|-----------|-------|-------|-----------------|
| `actiondef` | ActionDef | `AD-` | `#FFEEDD` | `node` | `action def` — a behavioral action type |
| `action` | Action | `A-` | `#FFE0CC` | `node` | `action` — an action usage |
| `statedef` | StateDef | `SD-` | `#EEEEDD` | `node` | `state def` — a state type |
| `stateusage` | StateUsage | `SU-` | `#DDDDCC` | `node` | `state` — a state usage |

### Requirement Types

| Directive | Title | ID Prefix | Color | Style | SysML v2 Concept |
|-----------|-------|-----------|-------|-------|-----------------|
| `requirementdef` | RequirementDef | `RD-` | `#FFF0CC` | `node` | `requirement def` — a requirement type |
| `requirement` | Requirement | `R-` | `#FFEEAA` | `node` | `requirement` — a requirement usage/instance |

---

## Extra Fields

All fields registered via `add_field()` at `config-inited`. Fields are shared across types where semantically applicable — sphinx-needs registers them globally.

| Field Name | Type | Description | Applicable Types |
|------------|------|-------------|-----------------|
| `abstract` | boolean | Whether this element is abstract (no direct instantiation) | PartDef, ActionDef, StateDef, RequirementDef |
| `owned_by` | string | Parent element ID (enables hierarchy traversal in templates) | All |
| `multiplicity` | string | UML multiplicity notation, e.g. `0..1`, `1..*`, `*` | Part, Port, Connection |
| `direction` | string | Port direction: `in`, `out`, `inout`, `~in` (conjugated in) | PortDef, Port |
| `conjugated` | boolean | Whether this port type is conjugated | PortDef |
| `definition` | string | ID of the Def type this usage instantiates | Part, Port, Interface, Connection, Action, StateUsage |
| `satisfies` | string | Comma-separated need IDs this element satisfies (requirements) | PartDef, Part, ActionDef |
| `refines` | string | Comma-separated need IDs this requirement refines | RequirementDef, Requirement |
| `allocates` | string | Comma-separated need IDs allocated to this element | PartDef, Part, ActionDef |
| `req_text` | string | Formal requirement statement text | RequirementDef, Requirement |
| `source_port` | string | Need ID of the source Port for a connection | ConnectionDef, Connection |
| `target_port` | string | Need ID of the target Port for a connection | ConnectionDef, Connection |
| `is_initial` | boolean | Whether this is the initial state | StateDef, StateUsage |
| `is_final` | boolean | Whether this is the final state | StateDef, StateUsage |

---

## Flow Config Strings (skinparam only)

Registered by mutating `app.config.needs_flow_configs` at `builder-inited`.

| Config Key | Applies To | Content |
|------------|-----------|---------|
| `sysml_bdd` | Block Definition Diagrams | skinparam for `<<block>>` / `<<PartDef>>` class elements |
| `sysml_ibd` | Internal Block Diagrams | skinparam for component elements with `<<Part>>` stereotype |
| `sysml_req` | Requirements Diagrams | skinparam for `<<requirement>>` class elements |
| `sysml_act` | Activity Diagrams (future) | Reserved for v2 |
| `sysml_stm` | State Machine Diagrams (future) | Reserved for v2 |

---

## Jinja2 Template Constants

Python string constants exported from `sphinxcontrib.sysml.templates` for use inside `.. needuml::` bodies. Not rendered automatically — users include them as building blocks.

| Constant | Description |
|----------|-------------|
| `BLOCK_DEF_TEMPLATE` | Renders a single `PartDef` as a PlantUML class with attribute/port compartments and a hyperlink |
| `BLOCK_INST_TEMPLATE` | Renders a `Part` instance (simpler — no compartments, just type reference) |
| `REQ_BOX_TEMPLATE` | Renders a `Requirement` as a `<<requirement>>` class with `id`/`text` compartments |
| `BDD_FULL_TEMPLATE` | Complete BDD Jinja2 body: renders a PartDef and all its owned Parts/Ports with composition arrows |
| `IBD_FULL_TEMPLATE` | Complete IBD Jinja2 body: renders internal Part instances with their ports and connections |
| `REQ_FULL_TEMPLATE` | Complete requirements diagram body: renders requirements matching a filter with satisfy/refine arrows |

---

## Custom Directives (wrapping needuml)

Higher-level directives that auto-fill the Jinja2 body so users don't need to write it manually.

### `.. needsysml-bdd:: <need-id>`
Generates a BDD for the given PartDef. Wraps `.. needuml::` with `:config: sysml_bdd` and the `BDD_FULL_TEMPLATE` body.

Options: `:depth: N` (default: 2), `:filter: <expr>` (override child filter), `:scale: <N>%`, `:align: <left|center|right>`

### `.. needsysml-ibd:: <need-id>`
Generates an IBD for the given PartDef. Wraps `.. needuml::` with `:config: sysml_ibd` and `IBD_FULL_TEMPLATE`.

Options: `:show-ports: true/false` (default: true), `:scale:`, `:align:`

### `.. needsysml-req:: <filter-expr>`
Generates a requirements diagram for all needs matching the filter. Wraps `.. needuml::` with `:config: sysml_req` and `REQ_FULL_TEMPLATE`.

Options: `:show-satisfy:`, `:show-refine:`, `:show-allocate:`, `:scale:`, `:align:`

---

## State Transitions

No state machine in the extension itself. sphinx-needs handles need state via the standard `status` field. SysML state machines are modeled as `StateDef`/`StateUsage` needs linked via `owned_by`.

---

## Validation Rules (from FR-006)

- Referencing a non-existent need ID in a diagram template → Sphinx warning (not error), placeholder node in diagram.
- `direction` field value not in `{in, out, inout, ~in}` → Sphinx warning.
- `multiplicity` field is free-text (no structural validation in v1).
