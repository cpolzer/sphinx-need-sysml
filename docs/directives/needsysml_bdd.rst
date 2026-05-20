needsysml-bdd Directive
=======================

The ``.. needsysml-bdd::`` directive generates a Block Definition Diagram
(BDD) for a given PartDef need using PlantUML.

Usage
-----

.. code-block:: rst

   .. needsysml-bdd:: <need-id>
      :depth: N
      :filter: <expression>
      :scale: <N>%
      :align: <left|center|right>

Required Argument
~~~~~~~~~~~~~~~~~

``<need-id>``
   The ID of the PartDef need to use as the root of the diagram.

Options
-------

``:depth: N``
   Maximum depth of child parts to include (default: 2).

``:filter: <expression>``
   Override the default child filter expression. By default, the directive
   selects needs matching ``type == 'Part' and owned_by == '<root-id>'``.

``:scale: <N>%``
   Scale the rendered diagram (e.g., ``80%``).

``:align: <left|center|right>``
   Horizontal alignment of the diagram (default: center).

How It Works
------------

The directive wraps sphinx-needs' ``.. needuml::`` directive with:

- ``:config: sysml_bdd`` — applies SysML BDD skinparam styling
- A pre-baked Jinja2 template that renders the root PartDef and its
  owned child Parts with composition arrows (``*--``)

The generated PlantUML uses class diagram syntax with ``<<PartDef>>`` and
``<<Part>>`` stereotypes, styled via the ``sysml_bdd`` flow config.

Example
-------

.. code-block:: rst

   .. partdef:: Vehicle
      :id: PD-001

      Vehicle system definition.

   .. partdef:: Engine
      :id: PD-002
      :owned_by: PD-001

      Engine definition.

   .. needsysml-bdd:: PD-001
      :depth: 2
      :scale: 80%
      :align: center

This renders a BDD showing Vehicle with its child Engine connected by a
composition arrow.

Clickable Links
---------------

When ``plantuml_output_format = "svg"`` is set in ``conf.py``, each block
in the diagram is a clickable link to the corresponding need's HTML anchor.

If the output format is not SVG, the extension emits a build warning.

Custom Templates
----------------

For full control, use ``.. needuml::`` directly with the ``sysml_bdd`` config:

.. code-block:: rst

   .. needuml::
      :config: sysml_bdd

      @startuml
      {{ uml("PD-001") }}
      {% for part in filter("type == 'Part' and owned_by == 'PD-001'") %}
      {{ uml(part.id) }}
      PD-001 *-- {{ part.id }}
      {% endfor %}
      @enduml
