needsysml-uc Directive
======================

The ``.. needsysml-uc::`` directive generates a Use Case Diagram with
actors outside one or more system-boundary rectangles and use cases
inside. A companion ``.. needsysml-uc-svg::`` renders the same diagram
as inline SVG.

Usage
-----

.. code-block:: rst

   .. needsysml-uc::
      :filter: type == 'UseCase'
      :subject: Vehicle
      :align: center

   .. needsysml-uc-svg::
      :align: center

Optional Argument
-----------------

You may pass the filter expression positionally for parity with the
``needsysml-req`` directive, or via the ``:filter:`` option. When
neither is supplied, the default is ``type == 'UseCase'``.

Options
-------

``:filter: <expression>``
   Filter expression selecting which use cases to draw. Default
   ``type == 'UseCase'``.

``:subject: <name>``
   Limit the diagram to use cases whose ``subject`` equals this value.
   When omitted, all subjects render as separate system-boundary
   rectangles.

``:scale: <N>%``
   PlantUML variant only.

``:align: <left|center|right>``
   Horizontal alignment. Default ``center``.

Actor associations (finding U1)
-------------------------------

Each ``Actor`` need carries an ``:interacts_with:`` field — a
comma-separated list of ``USECASE-`` IDs the actor participates in. The
renderer draws one solid association line per listed use case.

.. code-block:: rst

   .. actor:: Driver
      :id: ACTOR-001
      :interacts_with: USECASE-001

UseCase-to-UseCase relationships
--------------------------------

* ``:extends: USECASE-XXX[, USECASE-YYY]`` — dashed arrow labelled ``<<extend>>``
* ``:includes: USECASE-XXX[, USECASE-YYY]`` — dashed arrow labelled ``<<include>>``
* ``:generalizes: USECASE-XXX[, USECASE-YYY]`` — solid arrow with hollow triangle head (PlantUML ``<|--``)

System boundary
---------------

Each ``UseCase`` has a ``:subject:`` (free text) field. Use cases
sharing a subject render together inside a single rectangle labelled
with the subject name. Multiple subjects render as separate rectangles
on the same diagram.

How It Works
------------

The PlantUML directive wraps ``.. needuml::`` with ``:config: sysml_uc``
and ``UC_FULL_TEMPLATE`` — `left to right direction`, ``actor`` and
``usecase`` declarations grouped by subject in ``rectangle "<subject>"
{}`` blocks, then association/extend/include/generalize arrows.

The SVG companion (``UC_SVG_TEMPLATE``) draws stick-figure actors on
the left, use case ellipses inside a labelled boundary rectangle on the
right, and association/extend/include lines connecting them.

Clickable Links
---------------

PlantUML variant: each ``actor`` and ``usecase`` carries a
``[[<docname>.html#<id>]]`` link active when
``plantuml_output_format = "svg"``. SVG variant: each element is
wrapped in a native ``<a href>``.
