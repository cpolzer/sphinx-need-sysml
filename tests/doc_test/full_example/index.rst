Vehicle System Example
======================

A complete vehicle system example demonstrating all three SysML v2 diagram types.

Structural Definitions
----------------------

.. partdef:: Vehicle
   :id: PD-001
   :status: accepted
   :abstract: false

   Top-level vehicle system definition.

.. partdef:: Engine
   :id: PD-002
   :status: accepted
   :owned_by: PD-001
   :abstract: false

   Combustion engine block definition.

.. partdef:: Transmission
   :id: PD-003
   :status: accepted
   :owned_by: PD-001
   :abstract: false

   Transmission system definition.

.. partdef:: Wheel
   :id: PD-004
   :status: accepted
   :owned_by: PD-001
   :abstract: false

   Wheel assembly definition.

.. part:: engine
   :id: P-001
   :definition: PD-002
   :owned_by: PD-001
   :multiplicity: 1

   The single engine instance inside the Vehicle.

.. part:: transmission
   :id: P-002
   :definition: PD-003
   :owned_by: PD-001
   :multiplicity: 1

   The transmission instance.

.. part:: front_wheel
   :id: P-003
   :definition: PD-004
   :owned_by: PD-001
   :multiplicity: 2

   Front wheel assembly.

.. part:: rear_wheel
   :id: P-004
   :definition: PD-004
   :owned_by: PD-001
   :multiplicity: 2

   Rear wheel assembly.

Port Definitions
----------------

.. portdef:: FuelPort
   :id: POD-001
   :direction: in

   Fuel input port.

.. portdef:: DriveShaftPort
   :id: POD-002
   :direction: out

   Drive shaft output port.

.. port:: fuel_in
   :id: PO-001
   :definition: POD-001
   :owned_by: P-001
   :direction: in

   Fuel input on engine.

.. port:: drive_out
   :id: PO-002
   :definition: POD-002
   :owned_by: P-002
   :direction: out

   Drive output from transmission.

Connection Definitions
----------------------

.. connectiondef:: DriveConnection
   :id: CD-001
   :source_port: PO-002
   :target_port: PO-003

   Drive shaft connection.

.. connection:: drive_link
   :id: C-001
   :definition: CD-001
   :source_port: PO-002
   :target_port: PO-003

   Actual drive connection.

Requirements
------------

.. requirementdef:: PerformanceReq
   :id: RD-001

   Vehicle performance requirements definition.

.. requirement:: Braking Distance
   :id: R-001
   :owned_by: RD-001
   :definition: RD-001
   :satisfies: PD-001
   :status: open

   The vehicle shall stop within 50m from 100km/h.

.. requirement:: Engine Power
   :id: R-002
   :owned_by: RD-001
   :definition: RD-001
   :satisfies: PD-002
   :status: accepted

   Engine shall produce at least 150kW.

.. requirement:: Fuel Efficiency
   :id: R-003
   :owned_by: RD-001
   :definition: RD-001
   :satisfies: PD-001, PD-002
   :status: open

   Vehicle shall achieve 6L/100km combined cycle.

Actions
-------

.. actiondef:: StartVehicle
   :id: AD-001
   :abstract: false

   Action definition for starting the vehicle.

.. action:: Ignition Sequence
   :id: A-001
   :owned_by: AD-001
   :definition: AD-001

   Ignition sequence action.

State Definitions
-----------------

.. statedef:: VehicleState
   :id: SD-001
   :is_initial: false
   :is_final: false

   Vehicle operational states.

.. stateusage:: Off
   :id: SU-001
   :owned_by: SD-001
   :definition: SD-001
   :is_initial: true

   Vehicle off state.

.. stateusage:: Running
   :id: SU-002
   :owned_by: SD-001
   :definition: SD-001
   :is_initial: false

   Vehicle running state.

Diagrams
--------

Block Definition Diagram
~~~~~~~~~~~~~~~~~~~~~~~~

.. needsysml-bdd:: PD-001
   :depth: 2
   :scale: 80%
   :align: center

Requirements Diagram
~~~~~~~~~~~~~~~~~~~~

.. needsysml-req:: type == 'requirement'
   :show-satisfy: true
   :show-refine: true
   :align: center

Internal Block Diagram
~~~~~~~~~~~~~~~~~~~~~~

.. needsysml-ibd:: PD-001
   :show-ports: true
   :align: center

SVG Block Definition Diagram (requires sphinx-need-svg)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. needsysml-bdd-svg:: PD-001
   :depth: 2
   :align: center

Need Table
~~~~~~~~~~

.. needtable::
   :filter: type == 'requirement' and satisfies != ""
   :columns: id, title, satisfies, status
