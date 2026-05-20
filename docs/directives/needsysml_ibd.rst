needsysml-ibd Directive
=======================

The ``.. needsysml-ibd::`` directive generates an Internal Block Diagram
(IBD) for a given PartDef need using PlantUML.

.. warning::

   IBD diagrams are **approximations** using PlantUML component diagram
   syntax. Port placement is not locked to specific block edges. For
   precision IBD diagrams, consider using ``sphinx-need-svg`` as an
   alternative rendering path.

Usage
-----

.. code-block:: rst

   .. needsysml-ibd:: <need-id>
      :show-ports: true|false
      :scale: <N>%
      :align: <left|center|right>

Required Argument
~~~~~~~~~~~~~~~~~

``<need-id>``
   The ID of the PartDef need to use as the root of the diagram.

Options
-------

``:show-ports: true|false``
   Whether to show port elements inside parts (default: true).

``:scale: <N>%``
   Scale the rendered diagram (e.g., ``80%``).

``:align: <left|center|right>``
   Horizontal alignment of the diagram (default: center).

How It Works
------------

The directive wraps ``.. needuml::`` with:

- ``:config: sysml_ibd`` — applies SysML IBD skinparam styling
- A pre-baked Jinja2 template that renders the root PartDef as a
  rectangle boundary, child Parts as component elements with ports,
  and connections between ports

The generated PlantUML uses component diagram syntax with ``<<Part>>``
stereotypes and ``portin``/``portout`` elements.

Example
-------

.. code-block:: rst

   .. partdef:: Vehicle
      :id: PD-001

   .. partdef:: Engine
      :id: PD-002
      :owned_by: PD-001

   .. portdef:: FuelPort
      :id: POD-001
      :direction: in

   .. part:: engine
      :id: P-001
      :owned_by: PD-001
      :definition: PD-002

   .. port:: fuel_in
      :id: PO-001
      :owned_by: P-001
      :definition: POD-001
      :direction: in

   .. needsysml-ibd:: PD-001
      :show-ports: true
      :align: center

This renders an IBD showing the Vehicle boundary with internal parts
and their ports.
