needsysml-sd Directive
======================

The ``.. needsysml-sd::`` directive generates a Sequence Diagram for a
given interaction definition (conventionally an ``ActionDef`` that
represents the interaction). A companion ``.. needsysml-sd-svg::``
renders the same diagram as inline SVG.

Usage
-----

.. code-block:: rst

   .. needsysml-sd:: <interaction-id>
      :scale: <N>%
      :align: <left|center|right>

   .. needsysml-sd-svg:: <interaction-id>
      :align: <left|center|right>

Lifelines
---------

Each participant is declared as a ``lifeline`` need:

.. code-block:: rst

   .. lifeline:: driver_ll
      :id: LIFELINE-001
      :definition: AD-001
      :represents: ACTOR-001

The ``:represents:`` field optionally points at the Part, Actor, or
Subsystem the lifeline represents.

Messages
--------

Messages connect two lifelines:

.. code-block:: rst

   .. message:: turn_key
      :id: MSG-001
      :from_lifeline: LIFELINE-001
      :to_lifeline: LIFELINE-002
      :message_kind: sync

The ``:message_kind:`` enum:

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Value
     - Rendered
   * - ``sync`` (default)
     - Solid arrow with filled arrowhead (``->``)
   * - ``async``
     - Solid arrow with open arrowhead (``->>``)
   * - ``return``
     - Dashed arrow (``-->``)

Combined fragments
------------------

Messages sharing a ``:fragment_group:`` value render inside a single
combined-fragment frame. The first message's ``:fragment_kind:`` and
``:fragment_guard:`` are used as the frame header.

.. code-block:: rst

   .. message:: crank
      :id: MSG-002
      :from_lifeline: LIFELINE-002
      :to_lifeline: LIFELINE-003
      :message_kind: async
      :fragment_group: F1
      :fragment_kind: alt
      :fragment_guard: key_position == 'start'

Supported ``:fragment_kind:`` values: ``alt``, ``opt``, ``loop``,
``par``, ``neg``, ``critical`` (enum-validated by sphinx-needs).

How It Works
------------

The PlantUML directive wraps ``.. needuml::`` with ``:config: sysml_sd``
and emits native PlantUML sequence syntax (``participant``, message
arrows, ``alt``/``opt``/``loop`` blocks). The SVG companion lays out
lifelines as vertical columns with dashed timelines and stacks message
arrows by row, wrapping each ``fragment_group`` in a labelled
rectangle.

Clickable Links
---------------

PlantUML variant: each participant carries a ``[[<docname>.html#<id>]]``
link active when ``plantuml_output_format = "svg"``. SVG variant: each
lifeline and each message label is wrapped in a native ``<a href>``.
