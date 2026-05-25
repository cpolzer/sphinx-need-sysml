# Contract: Sphinx Extension Public API

**Date**: 2026-05-20
**Type**: Python library (Sphinx extension)

---

## Installation Contract

```
pip install sphinx-need-sysml
```

Installs the `sphinx_need_sysml` package. Requires:
- `sphinx-needs >= 1.0`
- `sphinx >= 4.0`
- `sphinxcontrib-plantuml` (optional — needed for PlantUML diagram rendering)
- `sphinx-need-svg` (optional — needed for SVG-native diagram directives)

---

## conf.py Contract

Minimum configuration to activate the extension:

```python
extensions = [
    "sphinx_needs",
    "sphinxcontrib.plantuml",  # optional but recommended
    "sphinx_need_sysml",
]

# Recommended for clickable diagrams in HTML:
plantuml_output_format = "svg"
```

No required `needs_*` configuration. Extension self-registers all types and fields.

---

## Directive Contract

### SysML v2 Need Type Directives

All 14 types follow the standard sphinx-needs directive pattern:

```rst
.. <directive>:: <title>
   :id: <PREFIX-NNN>
   :status: open | in_review | accepted | rejected
   :tags: tag1, tag2
   :links: <other-need-id>, <other-need-id>
   :<sysml-field>: <value>

   Optional content / description.
```

Directives: `partdef`, `part`, `portdef`, `port`, `interfacedef`, `interface`,
`connectiondef`, `connection`, `requirementdef`, `requirement`,
`actiondef`, `action`, `statedef`, `stateusage`

### Diagram Directives

```rst
.. needsysml-bdd:: PD-001
   :depth: 2
   :scale: 80%
   :align: center
```

```rst
.. needsysml-ibd:: PD-001
   :show-ports: true
   :align: center
```

```rst
.. needsysml-req:: type == 'Requirement' and status == 'open'
   :show-satisfy: true
   :show-refine: true
   :align: center
```

---

## Jinja2 Template Constants Contract

Importable from `sphinx_need_sysml.templates`:

```python
from sphinx_need_sysml.templates import (
    BDD_FULL_TEMPLATE,
    IBD_FULL_TEMPLATE,
    REQ_FULL_TEMPLATE,
    BLOCK_DEF_TEMPLATE,
    BLOCK_INST_TEMPLATE,
    REQ_BOX_TEMPLATE,
)
```

These are strings usable as `.. needuml::` directive bodies for custom diagrams.

---

## needs_flow_configs Contract

The extension registers these keys into `needs_flow_configs`. Users may override any of them in `conf.py` (user entries take precedence):

```python
# These are registered by the extension:
needs_flow_configs = {
    "sysml_bdd": "<skinparam string for BDD>",
    "sysml_ibd": "<skinparam string for IBD>",
    "sysml_req": "<skinparam string for requirements diagrams>",
}
```

---

## setup() Return Contract

```python
{
    "version": "<semver>",
    "parallel_read_safe": True,
    "parallel_write_safe": True,
}
```

---

## Warnings Contract

The extension emits Sphinx warnings (never errors) for:

- Unknown need ID referenced in a diagram template body
- `direction` field value not in `{in, out, inout, ~in}`
- `plantuml_output_format` not set to `"svg"` when diagram directives are used (once per build, not per directive)
