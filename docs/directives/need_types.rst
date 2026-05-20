Need Types
==========

sphinxcontrib-sysml registers 14 SysML v2 need types with sphinx-needs.
Each type has a unique ID prefix, color, and style.

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
