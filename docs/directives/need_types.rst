Need Types
==========

sphinx-need-sysml registers 27 SysML need types with sphinx-needs: 14
structural / behavioral / requirement types from the initial release,
plus 13 additional types added in feature 002 to support state-machine,
activity, sequence, use case, package, parametric, and allocation
diagrams. Each type has a unique ID prefix, color, and style.

Structural Types
----------------

.. list-table::
   :header-rows: 1

   * - Directive
     - Title
     - ID Prefix
     - Description
   * - ``partdef``
     - PartDef
     - ``PD-``
     - A block/part type definition (e.g., Engine, Vehicle)
   * - ``part``
     - Part
     - ``P-``
     - An instance/usage of a PartDef
   * - ``portdef``
     - PortDef
     - ``POD-``
     - A typed port definition
   * - ``port``
     - Port
     - ``PO-``
     - A port usage on a Part
   * - ``interfacedef``
     - InterfaceDef
     - ``IFD-``
     - A connection interface type
   * - ``interface``
     - Interface
     - ``IF-``
     - An interface usage
   * - ``connectiondef``
     - ConnectionDef
     - ``CD-``
     - A typed connector definition
   * - ``connection``
     - Connection
     - ``C-``
     - A connector instance

Behavioral Types
----------------

.. list-table::
   :header-rows: 1

   * - Directive
     - Title
     - ID Prefix
     - Description
   * - ``actiondef``
     - ActionDef
     - ``AD-``
     - A behavioral action type
   * - ``action``
     - Action
     - ``A-``
     - An action usage
   * - ``statedef``
     - StateDef
     - ``SD-``
     - A state type
   * - ``stateusage``
     - StateUsage
     - ``SU-``
     - A state usage

Requirement Types
-----------------

.. list-table::
   :header-rows: 1

   * - Directive
     - Title
     - ID Prefix
     - Description
   * - ``requirementdef``
     - RequirementDef
     - ``RD-``
     - A requirement type definition
   * - ``requirement``
     - Requirement
     - ``R-``
     - A requirement usage/instance

New in v0.3 — State-Machine
---------------------------

.. list-table::
   :header-rows: 1

   * - Directive
     - Title
     - ID Prefix
     - Description
   * - ``transition``
     - Transition
     - ``TRANS-``
     - A directed transition between two states

New in v0.3 — Activity
----------------------

.. list-table::
   :header-rows: 1

   * - Directive
     - Title
     - ID Prefix
     - Description
   * - ``controlflow``
     - ControlFlow
     - ``CTRLFLOW-``
     - A control-flow edge between two actions
   * - ``objectflow``
     - ObjectFlow
     - ``OBJFLOW-``
     - A data-flow edge between two actions

New in v0.3 — Package
---------------------

.. list-table::
   :header-rows: 1

   * - Directive
     - Title
     - ID Prefix
     - Description
   * - ``package``
     - Package
     - ``PKG-``
     - A package container
   * - ``dependency``
     - Dependency
     - ``DEP-``
     - A directed package dependency

New in v0.3 — Use Case
----------------------

.. list-table::
   :header-rows: 1

   * - Directive
     - Title
     - ID Prefix
     - Description
   * - ``usecase``
     - UseCase
     - ``USECASE-``
     - A user-facing use case
   * - ``actor``
     - Actor
     - ``ACTOR-``
     - An external actor

New in v0.3 — Sequence
----------------------

.. list-table::
   :header-rows: 1

   * - Directive
     - Title
     - ID Prefix
     - Description
   * - ``lifeline``
     - Lifeline
     - ``LIFELINE-``
     - A sequence-diagram lifeline
   * - ``message``
     - Message
     - ``MSG-``
     - A message between two lifelines

New in v0.3 — Parametric (v1.1 diagrams pending)
------------------------------------------------

The element types below register in v0.3 so models can declare them,
but the rendered parametric diagram ships with v0.4.

.. list-table::
   :header-rows: 1

   * - Directive
     - Title
     - ID Prefix
     - Description
   * - ``constraintblock``
     - ConstraintBlock
     - ``CONSTRAINT-``
     - A mathematical constraint definition
   * - ``constraintparameter``
     - ConstraintParameter
     - ``PARAM-``
     - A typed slot on a ConstraintBlock
   * - ``valueproperty``
     - ValueProperty
     - ``VALUE-``
     - A quantitative attribute of a part
   * - ``bindingconnector``
     - BindingConnector
     - ``BIND-``
     - A binding between a parameter and a value property

Extra Fields
------------

All need types share the following extra fields:

.. list-table::
   :header-rows: 1

   * - Field
     - Type
     - Description
   * - ``abstract``
     - boolean
     - Whether this element is abstract
   * - ``owned_by``
     - string
     - Parent element ID (enables hierarchy traversal)
   * - ``multiplicity``
     - string
     - UML multiplicity notation (e.g., ``0..1``, ``1..*``)
   * - ``direction``
     - string
     - Port direction: ``in``, ``out``, ``inout``, ``~in``
   * - ``conjugated``
     - boolean
     - Whether this port type is conjugated
   * - ``definition``
     - string
     - ID of the Def type this usage instantiates
   * - ``satisfies``
     - string
     - Comma-separated need IDs this element satisfies
   * - ``refines``
     - string
     - Comma-separated need IDs this requirement refines
   * - ``allocates``
     - string
     - Comma-separated need IDs allocated to this element
   * - ``source_port``
     - string
     - Need ID of the source Port for a connection
   * - ``target_port``
     - string
     - Need ID of the target Port for a connection
   * - ``is_initial``
     - boolean
     - Whether this is the initial state
   * - ``is_final``
     - boolean
     - Whether this is the final state

Usage Example
-------------

.. code-block:: rst

   .. partdef:: Engine
      :id: PD-001
      :abstract: false

      Engine block definition.

   .. part:: V8 Engine
      :id: P-001
      :owned_by: PD-001
      :definition: PD-001
      :multiplicity: 1

      A V8 engine instance.
