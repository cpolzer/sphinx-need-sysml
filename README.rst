sphinx-need-sysml
===================

Sphinx extension that registers **14 SysML v2 need types**, **15 extra fields**, and **4 diagram directives** on top of `sphinx-needs <https://sphinx-needs.readthedocs.io/>`_ and `PlantUML <https://plantuml.com/>`_.

.. image:: https://img.shields.io/pypi/v/sphinx-need-sysml.svg
   :target: https://pypi.org/project/sphinx-need-sysml/
   :alt: PyPI

.. image:: https://github.com/cpolzer/sphinx-need-sysml/actions/workflows/ci.yml/badge.svg
   :target: https://github.com/cpolzer/sphinx-need-sysml/actions/workflows/ci.yml
   :alt: CI

Installation
------------

.. code-block:: bash

   pip install sphinx-need-sysml

Requires ``sphinx-needs >= 1.0`` and Python >= 3.10.

Quick Start
-----------

1. Add to your ``conf.py``:

.. code-block:: python

   extensions = [
       "sphinx_needs",
       "sphinx_need_sysml",
   ]

2. Document SysML elements using the registered directives:

.. code-block:: rst

   .. partdef:: PD-001
      :title: WheelAssembly

      A wheel assembly consisting of a tire, rim, and hub.

   .. part:: P-001
      :title: FrontLeftWheel
      :definition: PD-001

      The front-left wheel of the vehicle.

3. Generate diagrams with the diagram directives:

.. code-block:: rst

   .. needsysml-bdd:: PD-001
      :depth: 2

Need Types
----------

14 SysML v2 need types are registered automatically. Each type has a directive, a title, an ID prefix, a color, and a PlantUML style.

Structural
~~~~~~~~~~

.. list-table::
   :header-rows: 1

   * - Directive
     - Title
     - Prefix
     - Description
   * - ``partdef``
     - PartDef
     - ``PD-``
     - Definition of a part (structural building block)
   * - ``part``
     - Part
     - ``P-``
     - Usage/instance of a PartDef
   * - ``portdef``
     - PortDef
     - ``POD-``
     - Definition of a port (interaction point)
   * - ``port``
     - Port
     - ``PO-``
     - Usage/instance of a PortDef
   * - ``interfacedef``
     - InterfaceDef
     - ``IFD-``
     - Definition of an interface
   * - ``interface``
     - Interface
     - ``IF-``
     - Usage/instance of an InterfaceDef
   * - ``connectiondef``
     - ConnectionDef
     - ``CD-``
     - Definition of a connection between ports
   * - ``connection``
     - Connection
     - ``C-``
     - Usage/instance of a ConnectionDef

Behavioral
~~~~~~~~~~

.. list-table::
   :header-rows: 1

   * - Directive
     - Title
     - Prefix
     - Description
   * - ``actiondef``
     - ActionDef
     - ``AD-``
     - Definition of an action/behavior
   * - ``action``
     - Action
     - ``A-``
     - Usage/instance of an ActionDef
   * - ``statedef``
     - StateDef
     - ``SD-``
     - Definition of a state
   * - ``stateusage``
     - StateUsage
     - ``SU-``
     - Usage/instance of a StateDef

Requirements
~~~~~~~~~~~~

.. list-table::
   :header-rows: 1

   * - Directive
     - Title
     - Prefix
     - Description
   * - ``requirementdef``
     - RequirementDef
     - ``RD-``
     - Definition of a requirement
   * - ``requirement``
     - Requirement
     - ``R-``
     - Usage/instance of a RequirementDef

Extra Fields
------------

These fields can be used on any need type. They carry SysML-specific semantics:

.. list-table::
   :header-rows: 1

   * - Field
     - Type
     - Description
   * - ``abstract``
     - boolean
     - Whether this element is abstract (no direct instantiation)
   * - ``owned_by``
     - string
     - Parent element ID (enables hierarchy traversal in templates)
   * - ``multiplicity``
     - string
     - UML multiplicity notation, e.g. ``0..1``, ``1..*``, ``*``
   * - ``direction``
     - string
     - Port direction: ``in``, ``out``, ``inout``, ``~in`` (conjugated in)
   * - ``conjugated``
     - boolean
     - Whether this port type is conjugated
   * - ``definition``
     - string
     - ID of the Def type this usage instantiates
   * - ``satisfies``
     - string
     - Comma-separated need IDs this element satisfies (requirements)
   * - ``refines``
     - string
     - Comma-separated need IDs this requirement refines
   * - ``allocates``
     - string
     - Comma-separated need IDs allocated to this element
   * - ``req_text``
     - string
     - Formal requirement statement text
   * - ``source_port``
     - string
     - Need ID of the source Port for a connection
   * - ``target_port``
     - string
     - Need ID of the target Port for a connection
   * - ``is_initial``
     - boolean
     - Whether this is the initial state
   * - ``is_final``
     - boolean
     - Whether this is the final state

Diagram Directives
------------------

Four diagram directives wrap ``needuml::`` with pre-baked Jinja2 templates and PlantUML skinparam configs.

.. code-block:: rst

   .. needsysml-bdd:: ROOT_ID
      :depth: 2
      :scale: 0.8
      :align: center

Generates a **Block Definition Diagram** for the given PartDef. Traverses owned parts up to ``depth`` levels.

.. code-block:: rst

   .. needsysml-ibd:: ROOT_ID
      :scale: 0.8
      :align: center

Generates an **Internal Block Diagram** showing parts, ports, and connections within a PartDef.

.. code-block:: rst

   .. needsysml-req:: ROOT_ID

Generates a **Requirements Diagram** showing the requirement and its traceability links (satisfies, refines, derives, verifies).

.. code-block:: rst

   .. needsysml-bdd-svg:: ROOT_ID

Generates a BDD as an inline SVG (requires ``sphinx-need-svg`` to be installed).

Options common to all diagram directives:

- ``scale`` — PlantUML scale factor (e.g. ``0.8``)
- ``align`` — Diagram alignment (``left``, ``center``, ``right``; default ``center``)
- ``depth`` — BDD traversal depth (default ``2``)

Flow Configs
------------

Three PlantUML flow configs are registered at ``builder-inited``:

- ``sysml_bdd`` — BDD skinparams (class stereotypes for PartDef/Part, left-to-right layout)
- ``sysml_ibd`` — IBD skinparams (component stereotype for Part, rectangle for IBD boundary)
- ``sysml_req`` — Requirements skinparams (class stereotype for requirement)

User-defined keys in ``needs_flow_configs`` take precedence.

Configuration Tips
------------------

Hyphenated IDs
~~~~~~~~~~~~~~

The default sphinx-needs ID regex rejects hyphens. If you use IDs like ``PD-001``, add this to ``conf.py``:

.. code-block:: python

   needs_id_regex = "^[A-Z0-9_-]+"

PlantUML output
~~~~~~~~~~~~~~~

Set SVG output for crisp diagrams:

.. code-block:: python

   plantuml_output_format = "svg"

Optional: sphinx-need-svg
~~~~~~~~~~~~~~~~~~~~~~~~~

Install ``sphinx-need-svg`` to enable the ``needsysml-bdd-svg`` directive for inline SVG diagrams.

Compatibility
-------------

- Python 3.10–3.12
- Sphinx 5.0–8.x
- sphinx-needs 2.1–8.0
- PlantUML (optional; diagrams emit warnings but don't break the build if absent)

Links
-----

- `PyPI <https://pypi.org/project/sphinx-need-sysml/>`_
- `GitHub <https://github.com/cpolzer/sphinx-need-sysml>`_
- `Documentation <https://cpolzer.github.io/sphinx-need-sysml/>`_
- `sphinx-needs <https://sphinx-needs.readthedocs.io/>`_
