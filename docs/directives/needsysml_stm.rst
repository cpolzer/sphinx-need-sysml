needsysml-stm Directive
=======================

The ``.. needsysml-stm::`` directive generates a State Machine Diagram
(stm) for a given ``StateDef`` need using PlantUML. A companion
``.. needsysml-stm-svg::`` directive renders the same diagram as inline
SVG via ``sphinx-need-svg``.

Usage
-----

.. code-block:: rst

   .. needsysml-stm:: <statedef-id>
      :scale: <N>%
      :align: <left|center|right>

   .. needsysml-stm-svg:: <statedef-id>
      :align: <left|center|right>

Required Argument
~~~~~~~~~~~~~~~~~

``<statedef-id>``
   The ID of the ``StateDef`` need whose owned ``StateUsage`` instances
   are drawn. The directive walks the registry for ``StateUsage`` needs
   whose ``definition`` field equals this ID, plus all ``Transition``
   needs whose ``from_state`` and ``to_state`` reference those states.

Options
-------

``:scale: <N>%``
   PlantUML scale factor (e.g. ``80%``). PlantUML variant only.

``:align: <left|center|right>``
   Horizontal alignment of the rendered diagram. Default ``center``.

``:width: <CSS-width>``
   Width passed to the SVG container. SVG variant only. Default ``100%``.

Pseudostate notation
--------------------

Each ``StateUsage`` may carry a ``:pseudo_kind:`` option drawn from the
following enum (validated by sphinx-needs at parse time):

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Value
     - Rendered
   * - ``initial``
     - Filled dot, source of an unlabelled transition from ``[*]`` in PlantUML
   * - ``final``
     - Ringed dot, target of an unlabelled transition to ``[*]``
   * - ``shallowHistory``
     - Circle containing ``H``
   * - ``deepHistory``
     - Circle containing ``H*``
   * - ``choice``
     - Diamond
   * - ``junction``
     - Small filled circle

States without ``:pseudo_kind:`` render as ordinary rounded rectangles.

Transition attributes
---------------------

A ``Transition`` need exposes these fields, all combined into the edge
label:

* ``:trigger:`` — the event name (e.g. ``key_on``)
* ``:guard:`` — a guard expression in brackets (e.g. ``[temperature < 90]``)
* ``:effect:`` — an effect action after a slash (e.g. ``/ start_seq``)

How It Works
------------

The PlantUML directive wraps ``.. needuml::`` with:

* ``:config: sysml_stm`` — applies SysML state-machine skinparam styling
* A pre-baked Jinja2 template (``STM_FULL_TEMPLATE`` in
  ``sphinx_need_sysml.templates``) that emits ``state X``,
  ``state X <<choice>>``, transition arrows, and pseudostate markers.

The SVG companion routes through ``sphinx-need-svg``'s ``Needsvg``
placeholder so the rendering is deferred to ``doctree-resolved`` (this
avoids freezing the needs registry mid-parse). It uses
``STM_SVG_TEMPLATE`` from ``sphinx_need_sysml.svg_templates``.

Example
-------

.. code-block:: rst

   .. statedef:: EngineState
      :id: SD-001

      Lifecycle of the engine.

   .. stateusage:: off
      :id: SU-001
      :definition: SD-001
      :pseudo_kind: initial

   .. stateusage:: starting
      :id: SU-002
      :definition: SD-001

   .. stateusage:: running
      :id: SU-003
      :definition: SD-001

   .. stateusage:: stopping
      :id: SU-004
      :definition: SD-001

   .. transition:: key_on
      :id: TRANS-001
      :from_state: SU-001
      :to_state: SU-002
      :trigger: key_on
      :effect: start_seq

   .. transition:: engine_ok
      :id: TRANS-002
      :from_state: SU-002
      :to_state: SU-003
      :trigger: engine_ok

   .. transition:: key_off
      :id: TRANS-003
      :from_state: SU-003
      :to_state: SU-004
      :trigger: key_off

   .. transition:: spindown
      :id: TRANS-004
      :from_state: SU-004
      :to_state: SU-001
      :trigger: spindown_complete

   .. needsysml-stm:: SD-001
      :align: center

   .. needsysml-stm-svg:: SD-001
      :align: center

Clickable Links
---------------

When ``plantuml_output_format = "svg"`` is set in ``conf.py``, each
state box in the PlantUML diagram is a clickable link to the
corresponding ``StateUsage`` anchor. The SVG variant uses native
``<a href>`` elements and works in every browser and output format that
supports inline SVG.
