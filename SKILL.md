# SKILL: sphinxcontrib-sysml

Sphinx extension for SysML v2 need types and diagrams.

## Extension Setup

```python
# conf.py
extensions = [
    "sphinx_needs",
    "sphinxcontrib.plantuml",  # optional
    "sphinxcontrib.sysml",
]
plantuml_output_format = "svg"  # required for clickable diagrams
```

## Directive Options

### Need Type Directives (14 types)

All follow standard sphinx-needs pattern:

```rst
.. <directive>:: <title>
   :id: <PREFIX-NNN>
   :status: open|in_review|accepted|rejected
   :<sysml-field>: <value>
```

Types: `partdef`, `part`, `portdef`, `port`, `interfacedef`, `interface`,
`connectiondef`, `connection`, `requirementdef`, `requirement`,
`actiondef`, `action`, `statedef`, `stateusage`

ID prefixes: `PD-`, `P-`, `POD-`, `PO-`, `IFD-`, `IF-`, `CD-`, `C-`,
`AD-`, `A-`, `SD-`, `SU-`, `RD-`, `R-`

### Diagram Directives

#### `.. needsysml-bdd:: <need-id>`

Options: `:depth: N` (default 2), `:filter: <expr>`, `:scale:`, `:align:`

Wraps `.. needuml::` with `:config: sysml_bdd` and BDD_FULL_TEMPLATE.
Renders root PartDef + child Parts with composition arrows.

#### `.. needsysml-ibd:: <need-id>`

Options: `:show-ports: true|false` (default true), `:scale:`, `:align:`

Wraps `.. needuml::` with `:config: sysml_ibd` and IBD_FULL_TEMPLATE.
**Approximation only** — no locked port placement.

#### `.. needsysml-req:: <filter-expr>`

Options: `:show-satisfy:`, `:show-refine:`, `:show-allocate:`, `:scale:`, `:align:`

Wraps `.. needuml::` with `:config: sysml_req` and REQ_FULL_TEMPLATE.
Renders requirements with dependency arrows.

## Config Keys

### needs_flow_configs (registered by extension)

- `sysml_bdd` — skinparam for PartDef/Part class elements
- `sysml_ibd` — skinparam for component/ibd elements
- `sysml_req` — skinparam for requirement class elements

User entries take precedence (merge at builder-inited).

### needs_id_regex

Configure to allow hyphenated IDs:

```python
needs_id_regex = "^[A-Z0-9_-]+"
```

## Jinja Helpers

Available in `.. needuml::` bodies:

| Name | Description |
|------|-------------|
| `needs` | dict[str, NeedItem] — all needs keyed by ID |
| `uml(id)` | Render one need as PlantUML |
| `filter(expr)` | Return needs matching filter expression |
| `ref(id)` | Generate `[[url text]]` PlantUML hyperlink string |

## Template Constants

Importable from `sphinxcontrib.sysml.templates`:

```python
from sphinxcontrib.sysml.templates import (
    BDD_FULL_TEMPLATE, IBD_FULL_TEMPLATE, REQ_FULL_TEMPLATE,
    BLOCK_DEF_TEMPLATE, BLOCK_INST_TEMPLATE, REQ_BOX_TEMPLATE,
)
```

## Warnings

- `plantuml_output_format != "svg"` → warning about non-clickable diagrams
- Unknown need ID in diagram → Sphinx warning (not error)
- Invalid `direction` value → Sphinx warning

## Compatibility

- `add_field` shim: tries new API, falls back to `add_extra_option`
- Works without sphinxcontrib-plantuml (degrades gracefully)
- sphinx-need-svg: optional secondary rendering path (future)
