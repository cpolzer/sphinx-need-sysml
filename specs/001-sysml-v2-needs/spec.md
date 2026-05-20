# Feature Specification: SysML v2 sphinx-needs Extension

**Feature Branch**: `001-sysml-v2-needs`

**Created**: 2026-05-20

**Status**: Draft

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Define SysML v2 structural elements (Priority: P1)

A systems engineer writing Sphinx documentation wants to define structural elements of their system — parts, blocks, ports, interfaces — using sphinx-needs directives that carry SysML v2 semantics. They want the elements to be cross-referenced like any other need, appear in need tables and filters, and serve as input to diagram generation.

**Why this priority**: This is the foundational capability. Without typed SysML v2 need types registered in sphinx-needs, no other feature (diagrams, requirement traceability) works.

**Independent Test**: A user can add `.. partdef::`, `.. part::`, `.. portdef::`, `.. interface::`, and `.. connection::` directives to an RST file, run `sphinx-build`, and see the elements rendered with their fields and IDs — without any diagram directives present.

**Acceptance Scenarios**:

1. **Given** a Sphinx project with the extension enabled, **When** the user writes a `.. partdef:: Engine` directive with fields `abstract: false` and a linked `port`, **Then** the built HTML shows it as a need with type `PartDef`, the correct fields, and a working cross-reference link.
2. **Given** multiple `.. part::` directives referencing a `.. partdef::`, **When** the user runs a `.. needtable::` filter on type `Part`, **Then** all part instances appear with their `definition` link resolved.
3. **Given** an invalid field value (e.g., unsupported multiplicity format), **When** Sphinx builds, **Then** a clear warning is emitted identifying the directive and field.

---

### User Story 2 - Generate a Block Definition Diagram (BDD) (Priority: P1)

A systems engineer wants to visualize the hierarchy and composition of `PartDef` elements in a Block Definition Diagram style, using a `.. needuml::` directive with a named SysML config. The diagram should show parts, their attributes, ports, and composition relationships — rendered via PlantUML.

**Why this priority**: Diagrams are the primary deliverable of SysML modeling. BDD is the most fundamental SysML v2 structure diagram.

**Independent Test**: A user can write `.. needuml:: :config: sysml_bdd` followed by Jinja calls like `{{ uml("ENGINE-001") }}`, run `sphinx-build`, and see a PlantUML-rendered BDD diagram showing the part definition with its ports and attributes.

**Acceptance Scenarios**:

1. **Given** a `PartDef` need with child `Part` usages and `PortDef` elements, **When** the user includes `{{ uml("PART-001") }}` inside a `.. needuml:: :config: sysml_bdd` directive, **Then** the rendered diagram shows the part as a SysML block with compartments for attributes and ports.
2. **Given** a composition relationship between two `PartDef` needs, **When** the BDD template processes them, **Then** the diagram renders a composition arrow with correct multiplicity notation.
3. **Given** a `.. needuml::` with `sysml_bdd` config referencing a non-existent need ID, **When** Sphinx builds, **Then** a warning is emitted and the diagram renders with a placeholder noting the missing element.

---

### User Story 3 - Generate a Requirements Diagram (Priority: P2)

A systems engineer wants to visualize requirements and their traceability to structural elements using a Requirements Diagram. `Requirement` needs carry `satisfies` and `refines` links to other needs, and the diagram shows containment and dependency arrows.

**Why this priority**: Requirements traceability is a core SysML use case and directly leverages sphinx-needs' existing link infrastructure.

**Independent Test**: A user can define `.. requirementdef::` and `.. requirement::` directives with `satisfies` links pointing to `PartDef` IDs, then render them with `.. needuml:: :config: sysml_req`, and see a diagram showing requirement boxes with satisfaction arrows.

**Acceptance Scenarios**:

1. **Given** a `Requirement` need with `satisfies: PART-001`, **When** rendered in a requirements diagram, **Then** a satisfaction arrow is drawn from the requirement to the target element.
2. **Given** a `Requirement` with `refines: REQ-001`, **When** rendered, **Then** a refinement dependency arrow is shown.
3. **Given** a filter expression in the diagram (e.g., `{{ filter("type == 'Requirement' and status == 'open'") }}`), **When** rendered, **Then** only matching requirements appear in the diagram.

---

### User Story 4 - Generate an Internal Block Diagram (IBD) (Priority: P2)

A systems engineer wants to visualize how `Part` instances inside a parent `PartDef` connect to each other via their ports using an Internal Block Diagram style. The diagram shows the internal structure of one composite part.

**Why this priority**: IBD complements BDD by showing runtime/deployment structure (instances and connections vs. type definitions).

**Independent Test**: A user can write `{{ uml("VEHICLE-001", diagram="ibd") }}` inside a `.. needuml:: :config: sysml_ibd` directive and see a diagram showing the internal `Part` instances with port connections rendered as lines.

**Acceptance Scenarios**:

1. **Given** a composite `PartDef` with two internal `Part` usages connected via matching port types, **When** rendered as IBD, **Then** the diagram shows both parts with their ports connected by a line.
2. **Given** a `Part` with no connections defined, **When** rendered in IBD context, **Then** the part appears as an isolated block with its ports shown but unconnected.

---

### User Story 5 - Link sphinx-needs entities inside SysML diagrams (Priority: P1)

A documentation author wants clickable hyperlinks from SysML diagram elements back to the sphinx-needs entries they represent, so readers can navigate from a diagram node to the full need definition.

**Why this priority**: This is the explicit linkability requirement from the project brief and what differentiates this extension from a plain PlantUML helper.

**Independent Test**: A user renders a BDD diagram and clicks a block in the HTML output — the browser navigates to the corresponding `.. partdef::` directive anchor in the documentation.

**Acceptance Scenarios**:

1. **Given** a BDD diagram rendered in HTML output, **When** the user clicks a block representing `ENGINE-001`, **Then** the browser navigates to the anchor for the `ENGINE-001` need.
2. **Given** a diagram rendered in PDF output, **When** the PDF is viewed, **Then** element labels include the need ID so the reader can locate the definition manually.
3. **Given** a need that has been moved to a different RST page, **When** Sphinx rebuilds, **Then** the diagram link still resolves to the correct page and anchor.

---

### Edge Cases

- What happens when a `Part` references a `PartDef` that hasn't been defined yet in the build order?
- How does the diagram template handle circular composition (part A contains part B which contains part A)?
- What if a user uses `.. needuml::` with a `sysml_bdd` config but mixes in non-SysML need types via a filter?
- What happens when PlantUML is not installed or `sphinxcontrib-plantuml` is not configured?
- How are very large part hierarchies (50+ elements) handled in a single diagram — is there a depth or count limit?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The extension MUST register the following sphinx-needs types when loaded: `PartDef`, `Part`, `PortDef`, `Port`, `InterfaceDef`, `Interface`, `ConnectionDef`, `Connection`, `RequirementDef`, `Requirement`, `ActionDef`, `Action`, `StateDef`, `StateUsage`.
- **FR-002**: Each SysML v2 need type MUST expose a defined set of extra options/fields appropriate to its SysML v2 semantics (e.g., `abstract`, `multiplicity`, `direction`, `satisfies`, `refines`, `allocates`, `owned_by`).
- **FR-003**: The extension MUST register named `flow_configs` in sphinx-needs for at least: `sysml_bdd` (Block Definition Diagram), `sysml_ibd` (Internal Block Diagram), and `sysml_req` (Requirements Diagram).
- **FR-004**: Each `flow_config` MUST be a Jinja2 template that, when used inside `.. needuml::`, renders syntactically valid PlantUML output representing the appropriate SysML v2 diagram type.
- **FR-005**: Diagram elements rendered from sphinx-needs entities MUST include PlantUML URL links that resolve to the HTML anchor of the corresponding need in the built documentation.
- **FR-006**: The extension MUST emit a Sphinx warning (not a build error) when a diagram template references a need ID that does not exist in the current build.
- **FR-007**: The extension MUST be usable without any configuration beyond adding it to `extensions` in `conf.py` and having `sphinxcontrib-plantuml` available.
- **FR-008**: All registered need types and fields MUST be compatible with standard sphinx-needs features: `needtable`, `needflow`, `needfilter`, cross-references via `:need:` role, and dynamic functions.
- **FR-009**: The extension MUST provide at least one `needuml` Jinja helper function (e.g., `sysml_block()`) that encapsulates the PlantUML notation for a SysML v2 block, so users can use it in custom diagrams without knowing PlantUML SysML syntax.
- **FR-010**: The extension package MUST follow the `sphinxcontrib.*` namespace convention and be installable via `pip`.

### Key Entities

- **PartDef**: A SysML v2 block/part type definition. Attributes: `abstract` (bool), `owned_by` (need ID). Can own `PortDef` and `AttributeDef` children.
- **Part**: An instance/usage of a `PartDef` within a composite. Attributes: `definition` (PartDef ID), `multiplicity`, `owned_by` (parent PartDef ID).
- **PortDef**: A typed port definition. Attributes: `direction` (in/out/inout), `conjugated` (bool), `owned_by` (PartDef ID).
- **Port**: A port usage on a Part. Attributes: `definition` (PortDef ID), `owned_by` (Part ID).
- **RequirementDef / Requirement**: A requirement type and its usage. Attributes: `satisfies` (need IDs), `refines` (need IDs), `allocates` (need IDs), `text` (requirement statement).
- **ActionDef / Action**: A behavioral action type and usage. Attributes: `owned_by`, `performs` (ActionDef ID).
- **ConnectionDef / Connection**: A typed connection between ports. Attributes: `source_port`, `target_port`, `owned_by`.
- **StateDef / StateUsage**: A state type and its usage in a state machine. Attributes: `owned_by`, `is_initial` (bool), `is_final` (bool).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A user with an existing sphinx-needs project can enable the extension and define a 5-element part hierarchy with requirements traceability in under 30 minutes, following only the extension's documentation.
- **SC-002**: A Sphinx build with 50 SysML v2 needs and 3 diagrams completes without errors on a system with PlantUML installed.
- **SC-003**: All registered SysML v2 need types and their fields are discoverable via standard sphinx-needs `needtable` and `needfilter` directives without any additional configuration.
- **SC-004**: Clicking a block in an HTML BDD or IBD diagram navigates to the corresponding need definition within the same Sphinx build output.
- **SC-005**: The extension passes its own test suite (unit + integration) with at least 80% coverage of the registered types and diagram templates.
- **SC-006**: A new user can install the extension with a single `pip install` command and has no required dependencies beyond `sphinx-needs` and `sphinxcontrib-plantuml`.

## Assumptions

- The target rendering engine is PlantUML via `sphinxcontrib-plantuml`; no alternative renderers (Mermaid, Graphviz) are in scope for v1.
- The extension targets sphinx-needs ≥ 1.0 and Python ≥ 3.10, matching the conventions of `sphinx-test-reports`.
- SysML v2 tool interop (import/export of `.sysml` textual files or REST API integration) is explicitly out of scope for v1.
- Activity diagrams and state machine diagrams are lower-priority and may ship as `sysml_act` / `sysml_stm` configs in a follow-up; only `sysml_bdd`, `sysml_ibd`, and `sysml_req` are v1 commitments.
- Users are expected to have basic familiarity with sphinx-needs directives and PlantUML configuration.
- The extension will use `flit` as the build backend, consistent with other useblocks-ecosystem extensions.
- Need type short tags (used in IDs) will follow the pattern: `PD` (PartDef), `P` (Part), `POD` (PortDef), `PO` (Port), `RD` (RequirementDef), `R` (Requirement), `AD` (ActionDef), `A` (Action), `CD` (ConnectionDef), `C` (Connection), `SD` (StateDef), `SU` (StateUsage).
