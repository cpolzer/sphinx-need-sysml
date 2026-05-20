needsysml-act Directive
=======================

The ``.. needsysml-act::`` directive generates an Activity Diagram
(act) for a given ``ActionDef`` need using PlantUML. A companion
``.. needsysml-act-svg::`` directive renders the same diagram as inline
SVG via ``sphinx-need-svg``.

Usage
-----

.. code-block:: rst

   .. needsysml-act:: <actiondef-id>
      :show-partitions: true|false
      :scale: <N>%
      :align: <left|center|right>

   .. needsysml-act-svg:: <actiondef-id>
      :align: <left|center|right>

Required Argument
~~~~~~~~~~~~~~~~~

``<actiondef-id>``
   The ID of the ``ActionDef`` need whose owned ``Action`` instances are
   drawn. The directive walks the registry for ``Action`` needs whose
   ``definition`` field equals this ID, plus all ``ControlFlow`` and
   ``ObjectFlow`` needs that connect them.

Options
-------

``:show-partitions: true|false``
   Whether to render swimlanes per ``partition`` value. Default
   ``true``. PlantUML variant only.

``:scale: <N>%``
   PlantUML scale factor. PlantUML variant only.

``:align: <left|center|right>``
   Horizontal alignment. Default ``center``.

``:width: <CSS-width>``
   Width passed to the SVG container. SVG variant only. Default
   ``100%``.

Action attributes
-----------------

* ``:partition:`` — swimlane name (free text). Actions sharing the same
  value group together.
* ``:activity_kind:`` — one of ``normal`` (default), ``decision``,
  ``merge``, ``fork``, ``join``. Fork/join render as horizontal bars;
  decision/merge as diamonds.

ControlFlow / ObjectFlow
------------------------

A ``controlflow`` need wires ``:from_action: <id>`` to ``:to_action:
<id>``. An ``objectflow`` adds ``:object_type:`` for a labelled data
flow.

How It Works
------------

The PlantUML directive wraps ``.. needuml::`` with ``:config:
sysml_act`` and a class-diagram approximation: actions render as
stereotyped classes (``<<action>>``, ``<<fork>>``, ``<<decision>>``,
…), grouped by ``partition`` into ``package <<swimlane>>`` blocks, and
control flows render as solid arrows. This is faithful to SysML even
though PlantUML's native activity-beta syntax is order-driven and would
not let us cleanly reference the existing need IDs as nodes.

The SVG companion (``ACT_SVG_TEMPLATE``) lays out swimlanes as vertical
columns and stacks actions inside them, with explicit arrow segments
for every ``ControlFlow``.

Clickable Links
---------------

PlantUML variant: each action class carries a ``[[<docname>.html#<id>]]``
link that activates when ``plantuml_output_format = "svg"``. SVG
variant: each action is wrapped in a native ``<a href>`` element.
