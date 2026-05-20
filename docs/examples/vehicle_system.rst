Vehicle System Example
======================

A complete worked example demonstrating all three SysML v2 diagram types
for a vehicle system.

Setup
-----

First, ensure ``sphinxcontrib.sysml`` is in your ``conf.py`` extensions:

.. code-block:: python

   extensions = [
       "sphinx_needs",
       "sphinxcontrib.plantuml",
       "sphinxcontrib.sysml",
   ]

   plantuml_output_format = "svg"

Structural Definitions
----------------------

Define the top-level system and its components:

.. code-block:: rst

   .. partdef:: Vehicle
      :id: PD-001
      :status: accepted

      Top-level vehicle system.

   .. partdef:: Engine
      :id: PD-002
      :owned_by: PD-001
      :status: accepted

      Combustion engine.

   .. partdef:: Transmission
      :id: PD-003
      :owned_by: PD-001
      :status: accepted

      Transmission system.

   .. partdef:: Chassis
      :id: PD-004
      :owned_by: PD-001
      :status: accepted

      Vehicle chassis.

   .. part:: engine
      :id: P-001
      :definition: PD-002
      :owned_by: PD-001
      :multiplicity: 1

      The engine instance.

   .. part:: transmission
      :id: P-002
      :definition: PD-003
      :owned_by: PD-001
      :multiplicity: 1

      The transmission instance.

   .. part:: chassis
      :id: P-003
      :definition: PD-004
      :owned_by: PD-001
      :multiplicity: 1

      The chassis instance.

Live needs:

.. partdef:: Vehicle
   :id: PD-001
   :status: accepted

   Top-level vehicle system.

.. partdef:: Engine
   :id: PD-002
   :owned_by: PD-001
   :status: accepted

   Combustion engine.

.. partdef:: Transmission
   :id: PD-003
   :owned_by: PD-001
   :status: accepted

   Transmission system.

.. partdef:: Chassis
   :id: PD-004
   :owned_by: PD-001
   :status: accepted

   Vehicle chassis.

.. part:: engine
   :id: P-001
   :definition: PD-002
   :owned_by: PD-001
   :multiplicity: 1

   The engine instance.

.. part:: transmission
   :id: P-002
   :definition: PD-003
   :owned_by: PD-001
   :multiplicity: 1

   The transmission instance.

.. part:: chassis
   :id: P-003
   :definition: PD-004
   :owned_by: PD-001
   :multiplicity: 1

   The chassis instance.

Ports and Connections
---------------------

Define interfaces between components:

.. code-block:: rst

   .. portdef:: FuelPort
      :id: POD-001
      :direction: in

   .. portdef:: DriveShaftPort
      :id: POD-002
      :direction: out

   .. port:: fuel_in
      :id: PO-001
      :definition: POD-001
      :owned_by: P-001
      :direction: in

   .. port:: drive_out
      :id: PO-002
      :definition: POD-002
      :owned_by: P-002
      :direction: out

   .. connectiondef:: DriveConnection
      :id: CD-001
      :source_port: PO-002
      :target_port: PO-003

   .. connection:: drive_link
      :id: C-001
      :definition: CD-001
      :source_port: PO-002
      :target_port: PO-003

Live needs:

.. portdef:: FuelPort
   :id: POD-001
   :direction: in

.. portdef:: DriveShaftPort
   :id: POD-002
   :direction: out

.. port:: fuel_in
   :id: PO-001
   :definition: POD-001
   :owned_by: P-001
   :direction: in

.. port:: drive_out
   :id: PO-002
   :definition: POD-002
   :owned_by: P-002
   :direction: out

.. connectiondef:: DriveConnection
   :id: CD-001
   :source_port: PO-002
   :target_port: PO-003

.. connection:: drive_link
   :id: C-001
   :definition: CD-001
   :source_port: PO-002
   :target_port: PO-003

Requirements
------------

Define requirements and link them to structural elements:

.. code-block:: rst

   .. requirement:: Braking Distance
      :id: R-001
      :req_text: The vehicle shall stop within 50m from 100km/h.
      :satisfies: PD-001

   .. requirement:: Engine Power
      :id: R-002
      :req_text: Engine shall produce at least 150kW.
      :satisfies: PD-002

   .. requirement:: Fuel Efficiency
      :id: R-003
      :req_text: Vehicle shall achieve 6L/100km combined cycle.
      :satisfies: PD-001, PD-002

Live needs:

.. requirement:: Braking Distance
   :id: R-001
   :req_text: The vehicle shall stop within 50m from 100km/h.
   :satisfies: PD-001

.. requirement:: Engine Power
   :id: R-002
   :req_text: Engine shall produce at least 150kW.
   :satisfies: PD-002

.. requirement:: Fuel Efficiency
   :id: R-003
   :req_text: Vehicle shall achieve 6L/100km combined cycle.
   :satisfies: PD-001, PD-002

Block Definition Diagram
------------------------

Generate a BDD showing the vehicle hierarchy:

.. code-block:: rst

   .. needsysml-bdd:: PD-001
      :depth: 2
      :scale: 80%
      :align: center

Rendered result:

.. needsysml-bdd:: PD-001
   :depth: 2
   :scale: 80%
   :align: center

SVG Block Definition Diagram
----------------------------

The same diagram rendered as inline SVG using ``sphinx-need-svg``.
This produces native SVG with reliable clickable links in all browsers:

.. code-block:: rst

   .. needsvg::
      :align: center

      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 400">
        {% set root_id = "PD-001" %}
        {% set root = needs.get(root_id) %}
        {% if root %}
        {{ flow(root_id) }}
        {% set children = filter("type == 'PartDef' and owned_by == '" + root_id + "'") %}
        {% for child in children %}
        {{ flow(child.id) }}
        {% endfor %}
        {% endif %}
      </svg>

Rendered result:

.. needsvg::
   :align: center

   <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 400">
     {% set root_id = "PD-001" %}
     {% set root = needs.get(root_id) %}
     {% if root %}
     {{ flow(root_id) }}
     {% set children = filter("type == 'PartDef' and owned_by == '" + root_id + "'") %}
     {% for child in children %}
     {{ flow(child.id) }}
     {% endfor %}
     {% endif %}
   </svg>

Requirements Diagram
--------------------

Show requirements and their satisfaction links:

.. code-block:: rst

   .. needsysml-req:: type == 'Requirement'
      :show-satisfy: true
      :show-refine: true
      :align: center

Rendered result:

.. needsysml-req:: type == 'Requirement'
   :show-satisfy: true
   :show-refine: true
   :align: center

Internal Block Diagram
----------------------

Show internal component structure with ports:

.. code-block:: rst

   .. needsysml-ibd:: PD-001
      :show-ports: true
      :align: center

Rendered result:

.. needsysml-ibd:: PD-001
   :show-ports: true
   :align: center

Query Results
-------------

Use sphinx-needs' ``needtable`` to query requirements:

.. code-block:: rst

   .. needtable::
      :filter: type == 'Requirement' and satisfies != ""
      :columns: id, title, satisfies, status

Live query:

.. needtable::
   :filter: type == 'Requirement' and satisfies != ""
   :columns: id, title, satisfies, status
