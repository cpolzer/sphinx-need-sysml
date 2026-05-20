needsysml-bdd-svg Directive
============================

The ``.. needsysml-bdd-svg::`` directive generates a Block Definition
Diagram as **inline SVG** using ``sphinx-need-svg``. Unlike the PlantUML
path, this produces native SVG with reliable clickable links in all
browsers.

Requirements
------------

This directive requires ``sphinx-need-svg`` to be installed:

.. code-block:: bash

   pip install sphinx-need-svg

If ``sphinx-need-svg`` is not installed, the directive is not registered
and will cause an "unknown directive" error.

Usage
-----

.. code-block:: rst

   .. needsysml-bdd-svg:: <need-id>
      :depth: N
      :filter: <expression>
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
   Override the default child filter expression.

``:align: <left|center|right>``
   Horizontal alignment of the diagram (default: center).

When to Use SVG vs PlantUML
----------------------------

**Use SVG (``needsysml-bdd-svg``) when:**

- You need reliable clickable links in all browsers
- You don't have PlantUML installed
- You want precision control over element placement
- Your diagrams are relatively simple

**Use PlantUML (``needsysml-bdd``) when:**

- You want auto-layout for complex diagrams
- You already have PlantUML set up
- You need the full PlantUML styling ecosystem
- Your diagrams have many interconnected elements

Example
-------

.. code-block:: rst

   .. partdef:: Vehicle
      :id: PD-001

   .. partdef:: Engine
      :id: PD-002
      :owned_by: PD-001

   .. needsysml-bdd-svg:: PD-001
      :depth: 2
      :align: center

This renders an inline SVG showing Vehicle with its child Engine,
each as a clickable block linking to its HTML anchor.
