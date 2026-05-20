needsysml-req Directive
=======================

The ``.. needsysml-req::`` directive generates a Requirements Diagram
for all needs matching a filter expression using PlantUML.

Usage
-----

.. code-block:: rst

   .. needsysml-req:: <filter-expr>
      :show-satisfy: true|false
      :show-refine: true|false
      :show-allocate: true|false
      :scale: <N>%
      :align: <left|center|right>

Required Argument
~~~~~~~~~~~~~~~~~

``<filter-expr>``
   A sphinx-needs filter expression selecting which needs to include.
   Example: ``type == 'Requirement' and status == 'open'``

Options
-------

``:show-satisfy: true|false``
   Show ``<<satisfy>>`` dependency arrows (default: true).

``:show-refine: true|false``
   Show ``<<refines>>`` dependency arrows (default: true).

``:show-allocate: true|false``
   Show ``<<allocates>>`` dependency arrows (default: true).

``:scale: <N>%``
   Scale the rendered diagram (e.g., ``80%``).

``:align: <left|center|right>``
   Horizontal alignment of the diagram (default: center).

How It Works
------------

The directive wraps ``.. needuml::`` with:

- ``:config: sysml_req`` — applies SysML requirements skinparam styling
- A pre-baked Jinja2 template that renders each matching need as a
  ``<<requirement>>`` class with id/text compartments, then adds
  dependency arrows for satisfies/refines/allocates links

Example
-------

.. code-block:: rst

   .. requirement:: Braking Distance
      :id: R-001
      :satisfies: PD-001

      The vehicle shall stop within 50m from 100km/h.

   .. requirement:: Engine Power
      :id: R-002
      :satisfies: PD-002

      Engine shall produce at least 150kW.

   .. needsysml-req:: type == 'Requirement'
      :show-satisfy: true
      :show-refine: false
      :align: center

This renders a requirements diagram showing both requirements with
``<<satisfy>>`` arrows pointing to their satisfied parts.

Filter Expressions
------------------

Filter expressions use sphinx-needs' standard filter syntax. Common patterns:

- ``type == 'Requirement'`` — all requirement needs
- ``type == 'Requirement' and status == 'open'`` — open requirements only
- ``satisfies != ""`` — requirements that satisfy something
- ``owned_by == 'RD-001'`` — requirements owned by a specific definition
