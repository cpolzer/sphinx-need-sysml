Test Project
============

Basic test project for sphinxcontrib-sysml with all 14 need types.

Structural Types
----------------

.. partdef:: Engine
   :id: PD-001
   :abstract: false
   :owned_by:

   A PartDef representing an engine block.

.. part:: V8 Engine
   :id: P-001
   :owned_by: PD-001
   :definition: PD-001
   :multiplicity: 1

   A V8 engine instance.

.. portdef:: FuelPort
   :id: POD-001
   :direction: in
   :conjugated: false

   A fuel input port definition.

.. port:: Fuel Input
   :id: PO-001
   :owned_by: P-001
   :definition: POD-001
   :direction: in

   Fuel input port on the engine.

.. interfacedef:: DataBus
   :id: IFD-001

   A data bus interface definition.

.. interface:: CAN Bus
   :id: IF-001
   :definition: IFD-001

   CAN bus interface usage.

.. connectiondef:: FuelLine
   :id: CD-001
   :source_port: PO-001
   :target_port: PO-002

   A fuel line connector definition.

.. connection:: Fuel Connection
   :id: C-001
   :definition: CD-001
   :source_port: PO-001
   :target_port: PO-002
   :multiplicity: 1

   Actual fuel line connection.

Behavioral Types
----------------

.. actiondef:: StartEngine
   :id: AD-001
   :abstract: false

   Action definition for starting the engine.

.. action:: Ignition
   :id: A-001
   :owned_by: AD-001
   :definition: AD-001

   Ignition action usage.

.. statedef:: Running
   :id: SD-001
   :is_initial: false
   :is_final: false

   State definition for running state.

.. stateusage:: Engine Running
   :id: SU-001
   :owned_by: SD-001
   :definition: SD-001
   :is_initial: true

   Engine running state usage.

Requirement Types
-----------------

.. requirementdef:: SafetyReq
   :id: RD-001

   Safety requirement definition.

.. requirement:: Brake Distance
   :id: R-001
   :owned_by: RD-001
   :definition: RD-001
   :satisfies: PD-001
   :refines:
   :allocates:

   Decelerate >= 8 m/s2

Diagrams
--------

.. needsysml-bdd:: PD-001
   :depth: 2
   :scale: 80%
   :align: center

.. needsysml-req:: type == 'requirement'
   :show-satisfy: true
   :show-refine: true
   :align: center

.. needsysml-ibd:: PD-001
   :show-ports: true
   :align: center
