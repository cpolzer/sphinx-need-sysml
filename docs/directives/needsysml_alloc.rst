needsysml-alloc Directive
=========================

The ``.. needsysml-alloc::`` directive generates an allocation matrix
table showing which requirements allocate to which parts. Unlike other
diagram directives, it renders a docutils ``<table>`` (not PlantUML or
SVG), so it works in HTML, PDF, and ePub outputs.

Usage
-----

.. code-block:: rst

   .. needsysml-alloc::
      :rows: <filter-expression>
      :columns: <filter-expression>
      :marker: <character>

No required argument — the defaults work for the common case.

Options
-------

``:rows: <filter-expression>``
   Filter expression for the row axis. Default: needs with non-empty
   ``allocates`` field (``allocates != ""``).

``:columns: <filter-expression>``
   Filter expression for the column axis. Default: all unique part IDs
   referenced by the row needs' ``allocates`` fields.

``:marker: <character>``
   Character placed at allocated intersections. Default ``✓``.

How It Works
------------

The directive evaluates the ``:rows:`` filter against all registered
needs, then collects the unique IDs referenced by each row need's
``allocates`` field to form the columns. If ``:columns:`` is provided,
those column IDs are further filtered.

Row and column headers are cross-references to the corresponding need
anchors. Interior cells contain the marker character at allocated
intersections and are empty otherwise (no links in interior cells per
FR-013).

Example
-------

.. code-block:: rst

   .. requirement:: Engine Control
      :id: R-001
      :allocates: P-001, P-002

      The engine control system shall manage fuel delivery.

   .. part:: ECU
      :id: P-001

   .. part:: Fuel Injector
      :id: P-002

   .. needsysml-alloc::

Custom filters:

.. code-block:: rst

   .. needsysml-alloc::
      :rows: type == 'Action'
      :columns: type == 'Part'

Empty Result
------------

When no needs match the rows filter, the directive emits an
informational warning (``[needsysml.alloc.empty]``) and renders a
"No matching elements" placeholder.
