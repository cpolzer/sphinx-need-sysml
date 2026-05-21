# Quickstart: sphinx-need-sysml

**Date**: 2026-05-20

---

## Install

```bash
pip install sphinx-need-sysml sphinxcontrib-plantuml
```

## conf.py

```python
extensions = [
    "sphinx_needs",
    "sphinxcontrib.plantuml",
    "sphinx_need_sysml",
]

# Required for clickable diagram links in HTML output
plantuml_output_format = "svg"

# PlantUML binary path (if not on PATH)
# plantuml = "/usr/bin/plantuml"
```

## Define structural elements

```rst
.. partdef:: Vehicle
   :id: PD-001
   :status: accepted
   :abstract: false

   Top-level vehicle system definition.

.. partdef:: Engine
   :id: PD-002
   :status: accepted
   :owned_by: PD-001
   :abstract: false

   Combustion engine block definition.

.. part:: engine
   :id: P-001
   :definition: PD-002
   :owned_by: PD-001
   :multiplicity: 1

   The single engine instance inside the Vehicle.
```

## Define a requirement and link it

```rst
.. requirement:: Braking Distance
   :id: R-001
   :status: open
   :req_text: The vehicle shall stop within 50m from 100km/h.
   :satisfies: PD-001
```

## Generate a Block Definition Diagram

```rst
.. needsysml-bdd:: PD-001
   :depth: 2
   :align: center
```

## Generate a Requirements Diagram

```rst
.. needsysml-req:: type == 'Requirement'
   :show-satisfy: true
   :align: center
```

## Use raw needuml with SysML config (advanced)

```rst
.. needuml::
   :config: sysml_bdd

   @startuml
   {{ uml("PD-001") }}
   {% for part in filter("type == 'Part' and owned_by == 'PD-001'") %}
   {{ uml(part.id) }}
   PD-001 *-- {{ part.id }}
   {% endfor %}
   @enduml
```

## Query in needtable

```rst
.. needtable::
   :filter: type == 'Requirement' and satisfies != ""
   :columns: id, title, satisfies, status
```
