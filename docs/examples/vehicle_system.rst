Vehicle System: Full SysML v2 Demo
==================================

A complete worked example showing every major SysML v2 element type and
every diagram path provided by ``sphinxcontrib-sysml`` — both the
PlantUML directives (``needsysml-bdd``, ``needsysml-ibd``,
``needsysml-req``) and the inline-SVG variants powered by
``sphinx-need-svg`` (``needsysml-bdd-svg`` and raw ``needsvg``
templates).

.. contents::
   :local:
   :depth: 2

Setup
-----

Enable the extensions in ``docs/conf.py``:

.. code-block:: python

   extensions = [
       "sphinx_needs",
       "sphinxcontrib.plantuml",
       "sphinxcontrib.sysml",
       "sphinx_need_svg",  # optional, enables SVG diagrams
   ]

   plantuml_output_format = "svg"  # required for clickable PlantUML links

Structural Model
----------------

The vehicle decomposes into a powertrain (engine + transmission) and a
chassis with four wheels.

PartDefs (definitions)
~~~~~~~~~~~~~~~~~~~~~~

.. partdef:: Vehicle
   :id: PD-001
   :status: accepted

   Top-level vehicle system.

.. partdef:: Powertrain
   :id: PD-002
   :owned_by: PD-001
   :status: accepted

   Powertrain subsystem: engine plus transmission.

.. partdef:: Engine
   :id: PD-003
   :owned_by: PD-002
   :status: accepted

   Internal combustion engine.

.. partdef:: Transmission
   :id: PD-004
   :owned_by: PD-002
   :status: accepted

   Multi-speed gearbox.

.. partdef:: Chassis
   :id: PD-005
   :owned_by: PD-001
   :status: accepted

   Vehicle chassis carrying the wheels.

.. partdef:: Wheel
   :id: PD-006
   :owned_by: PD-005
   :status: accepted

   Wheel and tyre assembly.

Parts (usages)
~~~~~~~~~~~~~~

.. part:: powertrain
   :id: P-001
   :definition: PD-002
   :owned_by: PD-001
   :multiplicity: 1

   The vehicle's powertrain instance.

.. part:: engine
   :id: P-002
   :definition: PD-003
   :owned_by: PD-002
   :multiplicity: 1

   The engine instance.

.. part:: transmission
   :id: P-003
   :definition: PD-004
   :owned_by: PD-002
   :multiplicity: 1

   The transmission instance.

.. part:: chassis
   :id: P-004
   :definition: PD-005
   :owned_by: PD-001
   :multiplicity: 1

   The chassis instance.

.. part:: front_left_wheel
   :id: P-005
   :definition: PD-006
   :owned_by: PD-005
   :multiplicity: 1

.. part:: front_right_wheel
   :id: P-006
   :definition: PD-006
   :owned_by: PD-005
   :multiplicity: 1

.. part:: rear_left_wheel
   :id: P-007
   :definition: PD-006
   :owned_by: PD-005
   :multiplicity: 1

.. part:: rear_right_wheel
   :id: P-008
   :definition: PD-006
   :owned_by: PD-005
   :multiplicity: 1

Ports and Connections
---------------------

Ports specify how parts interface; connections wire compatible ports
together.

.. portdef:: FuelPort
   :id: POD-001
   :direction: in

   Fuel inlet port type.

.. portdef:: PowerOutPort
   :id: POD-002
   :direction: out

   Rotational power output port type.

.. portdef:: PowerInPort
   :id: POD-003
   :direction: in

   Rotational power input port type (conjugate of POD-002).

.. port:: fuel_in
   :id: PO-001
   :definition: POD-001
   :owned_by: P-002
   :direction: in

.. port:: power_out
   :id: PO-002
   :definition: POD-002
   :owned_by: P-002
   :direction: out

.. port:: power_in
   :id: PO-003
   :definition: POD-003
   :owned_by: P-003
   :direction: in

.. port:: drive_out
   :id: PO-004
   :definition: POD-002
   :owned_by: P-003
   :direction: out

.. port:: drive_in
   :id: PO-005
   :definition: POD-003
   :owned_by: P-004
   :direction: in

.. connectiondef:: EngineToTransLink
   :id: CD-001
   :source_port: POD-002
   :target_port: POD-003

   Connector type carrying rotational power.

.. connection:: engine_to_trans
   :id: C-001
   :definition: CD-001
   :source_port: PO-002
   :target_port: PO-003

   Wires engine ``power_out`` into transmission ``power_in``.

.. connection:: trans_to_chassis
   :id: C-002
   :definition: CD-001
   :source_port: PO-004
   :target_port: PO-005

   Wires transmission ``drive_out`` into chassis ``drive_in``.

Behavioral Elements
-------------------

Actions describe what the system does; states describe modes it can be in.

.. actiondef:: StartEngine
   :id: AD-001

   Cold-start sequence for the engine.

.. action:: insert_key
   :id: A-001
   :definition: AD-001
   :partition: Driver

.. action:: turn_key
   :id: A-002
   :definition: AD-001
   :partition: Driver

.. action:: power_rails
   :id: A-003
   :definition: AD-001
   :partition: ECU

.. action:: fork_node
   :id: A-004
   :definition: AD-001
   :partition: ECU
   :activity_kind: fork

.. action:: crank_starter
   :id: A-005
   :definition: AD-001
   :partition: ECU

.. action:: fuel_pump_prime
   :id: A-006
   :definition: AD-001
   :partition: ECU

.. action:: join_node
   :id: A-007
   :definition: AD-001
   :partition: ECU
   :activity_kind: join

.. controlflow:: insert→turn
   :id: CTRLFLOW-001
   :from_action: A-001
   :to_action: A-002

.. controlflow:: turn→power
   :id: CTRLFLOW-002
   :from_action: A-002
   :to_action: A-003

.. controlflow:: power→fork
   :id: CTRLFLOW-003
   :from_action: A-003
   :to_action: A-004

.. controlflow:: fork→crank
   :id: CTRLFLOW-004
   :from_action: A-004
   :to_action: A-005

.. controlflow:: fork→fuel
   :id: CTRLFLOW-005
   :from_action: A-004
   :to_action: A-006

.. controlflow:: crank→join
   :id: CTRLFLOW-006
   :from_action: A-005
   :to_action: A-007

.. controlflow:: fuel→join
   :id: CTRLFLOW-007
   :from_action: A-006
   :to_action: A-007

.. statedef:: EngineState
   :id: SD-001

   Lifecycle states of the engine.

.. stateusage:: off
   :id: SU-001
   :definition: SD-001
   :owned_by: P-002
   :pseudo_kind: initial

.. stateusage:: starting
   :id: SU-002
   :definition: SD-001
   :owned_by: P-002

.. stateusage:: running
   :id: SU-003
   :definition: SD-001
   :owned_by: P-002

.. stateusage:: stopping
   :id: SU-004
   :definition: SD-001
   :owned_by: P-002

.. transition:: key_on_transition
   :id: TRANS-001
   :from_state: SU-001
   :to_state: SU-002
   :trigger: key_on
   :effect: start_seq

.. transition:: engine_ok_transition
   :id: TRANS-002
   :from_state: SU-002
   :to_state: SU-003
   :trigger: engine_ok

.. transition:: key_off_transition
   :id: TRANS-003
   :from_state: SU-003
   :to_state: SU-004
   :trigger: key_off

.. transition:: spindown_transition
   :id: TRANS-004
   :from_state: SU-004
   :to_state: SU-001
   :trigger: spindown_complete

.. transition:: critical_fault_transition
   :id: TRANS-005
   :from_state: SU-003
   :to_state: SU-001
   :trigger: fault
   :guard: severity == 'critical'

Package Organization
--------------------

Packages organize the model into nested groupings, with cross-package
dependencies labelled by kind.

.. package:: VehicleSystem
   :id: PKG-001

   Top-level package for the whole vehicle system.

.. package:: PowertrainPkg
   :id: PKG-002
   :parent_package: PKG-001

.. package:: ChassisPkg
   :id: PKG-003
   :parent_package: PKG-001

.. package:: ControlsPkg
   :id: PKG-004
   :parent_package: PKG-001

.. dependency:: pt_uses_controls
   :id: DEP-001
   :source_ref: PKG-002
   :target_ref: PKG-004
   :kind: use

.. dependency:: chassis_imports_controls
   :id: DEP-002
   :source_ref: PKG-003
   :target_ref: PKG-004
   :kind: import

Package Diagram (PlantUML)
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: rst

   .. needsysml-pkg:: PKG-001
      :align: center

.. needsysml-pkg:: PKG-001
   :align: center

Package Diagram (SVG)
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: rst

   .. needsysml-pkg-svg:: PKG-001
      :align: center

.. needsysml-pkg-svg:: PKG-001
   :align: center

Use Cases
---------

Use cases capture stakeholder-system interactions inside a system
boundary. ``Actor.interacts_with`` wires actors to use cases;
``UseCase.extends`` / ``.includes`` / ``.generalizes`` wire use cases
to each other.

.. actor:: Driver
   :id: ACTOR-001
   :interacts_with: USECASE-001

.. actor:: Mechanic
   :id: ACTOR-002
   :interacts_with: USECASE-002, USECASE-003

.. usecase:: Start engine
   :id: USECASE-001
   :subject: Vehicle

.. usecase:: Diagnose fault
   :id: USECASE-002
   :subject: Vehicle
   :extends: USECASE-001

.. usecase:: Authenticate key
   :id: USECASE-003
   :subject: Vehicle

.. usecase:: Perform service
   :id: USECASE-004
   :subject: Vehicle
   :includes: USECASE-003

Use Case Diagram (PlantUML)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: rst

   .. needsysml-uc::
      :align: center

.. needsysml-uc::
   :align: center

Use Case Diagram (SVG)
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: rst

   .. needsysml-uc-svg::
      :align: center

.. needsysml-uc-svg::
   :align: center

Sequence
--------

A sequence diagram captures the cross-component interaction during
key-on ignition: ``Driver`` → ``ECU`` → ``Starter``. The two combined
fragments illustrate an ``alt`` (sync vs. accessory mode) and a ``loop``
(warm-up).

.. actiondef:: IgnitionSequence
   :id: AD-010

   Key-on ignition interaction across Driver, ECU, and Starter.

.. lifeline:: driver_ll
   :id: LIFELINE-001
   :definition: AD-010

.. lifeline:: ecu_ll
   :id: LIFELINE-002
   :definition: AD-010

.. lifeline:: starter_ll
   :id: LIFELINE-003
   :definition: AD-010

.. message:: turn_key_msg
   :id: MSG-001
   :from_lifeline: LIFELINE-001
   :to_lifeline: LIFELINE-002
   :message_kind: sync

.. message:: crank_msg
   :id: MSG-002
   :from_lifeline: LIFELINE-002
   :to_lifeline: LIFELINE-003
   :message_kind: async
   :fragment_group: F1
   :fragment_kind: alt
   :fragment_guard: key_position == 'start'

.. message:: ok_msg
   :id: MSG-003
   :from_lifeline: LIFELINE-003
   :to_lifeline: LIFELINE-002
   :message_kind: return
   :fragment_group: F1

.. message:: heartbeat_msg
   :id: MSG-004
   :from_lifeline: LIFELINE-002
   :to_lifeline: LIFELINE-002
   :message_kind: async
   :fragment_group: F2
   :fragment_kind: loop
   :fragment_guard: engine_warming

Sequence Diagram (PlantUML)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: rst

   .. needsysml-sd:: AD-010
      :align: center

.. needsysml-sd:: AD-010
   :align: center

Sequence Diagram (SVG)
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: rst

   .. needsysml-sd-svg:: AD-010
      :align: center

.. needsysml-sd-svg:: AD-010
   :align: center

Requirements
------------

Requirements link to the structural elements they govern via
``satisfies``, ``refines``, and ``allocates``.

.. requirementdef:: SafetyRequirement
   :id: RD-001
   :abstract: true

   Abstract base for vehicle safety requirements.

.. requirement:: Braking Distance
   :id: R-001
   :satisfies: PD-001
   :refines: RD-001

   The vehicle shall stop within 50 m from 100 km/h.

.. requirement:: Engine Power
   :id: R-002
   :satisfies: PD-003

   The engine shall produce at least 150 kW at 5000 rpm.

.. requirement:: Fuel Efficiency
   :id: R-003
   :satisfies: PD-001
   :allocates: P-002

   The vehicle shall achieve 6 L / 100 km combined cycle.

.. requirement:: Acceleration
   :id: R-004
   :satisfies: PD-001
   :refines: RD-001

   The vehicle shall accelerate 0 to 100 km/h in under 8 s.

Activity Diagram (PlantUML)
---------------------------

``needsysml-act`` walks the ``ActionDef``'s owned actions, groups them
into swimlanes by ``:partition:``, and connects them via the
``controlflow`` (and optional ``objectflow``) edges.

.. code-block:: rst

   .. needsysml-act:: AD-001
      :show-partitions: true
      :align: center

.. needsysml-act:: AD-001
   :show-partitions: true
   :align: center

Activity Diagram (SVG)
----------------------

.. code-block:: rst

   .. needsysml-act-svg:: AD-001
      :align: center

.. needsysml-act-svg:: AD-001
   :align: center

State Machine Diagram (PlantUML)
--------------------------------

``needsysml-stm`` walks the ``StateDef``'s usages and renders them with
their transitions. Pseudostates (initial / final / history / choice /
junction) appear with their UML notation.

.. code-block:: rst

   .. needsysml-stm:: SD-001
      :align: center

.. needsysml-stm:: SD-001
   :align: center

State Machine Diagram (SVG)
---------------------------

``needsysml-stm-svg`` renders the same state machine as inline SVG with
clickable links on every state.

.. code-block:: rst

   .. needsysml-stm-svg:: SD-001
      :align: center

.. needsysml-stm-svg:: SD-001
   :align: center

Block Definition Diagram (PlantUML)
-----------------------------------

``needsysml-bdd`` renders a class-diagram BDD with composition arrows
via PlantUML.

.. code-block:: rst

   .. needsysml-bdd:: PD-001
      :depth: 2
      :scale: 80%
      :align: center

.. needsysml-bdd:: PD-001
   :depth: 2
   :scale: 80%
   :align: center

Block Definition Diagram (SVG)
------------------------------

``needsysml-bdd-svg`` renders the same diagram as native inline SVG via
``sphinx-need-svg``. Every block is a real ``<a>`` link with reliable
cross-browser navigation.

.. code-block:: rst

   .. needsysml-bdd-svg:: PD-001
      :align: center

.. needsysml-bdd-svg:: PD-001
   :align: center

Custom SVG with ``needsvg``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

For full control, drop into a raw ``needsvg`` directive and use the
Jinja helpers (``needs``, ``filter``, ``flow``, ``ref``) directly.

.. code-block:: rst

   .. needsvg::
      :align: center

      {% set root_id = "PD-002" %}
      {% set root = needs.get(root_id) %}
      {% set children = filter("type == 'partdef' and owned_by == '" + root_id + "'") %}
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 240">
        <g transform="translate(240, 20)">{{ flow(root_id) }}</g>
        {% for child in children %}
        {% set cx = 150 * loop.index %}
        <line x1="300" y1="60" x2="{{ cx }}" y2="180"
              stroke="#336699" stroke-width="1.5"/>
        <g transform="translate({{ cx - 60 }}, 180)">{{ flow(child.id) }}</g>
        {% endfor %}
      </svg>

.. needsvg::
   :align: center

   {% set root_id = "PD-002" %}
   {% set root = needs.get(root_id) %}
   {% set children = filter("type == 'partdef' and owned_by == '" + root_id + "'") %}
   <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 240">
     <g transform="translate(240, 20)">{{ flow(root_id) }}</g>
     {% for child in children %}
     {% set cx = 150 * loop.index %}
     <line x1="300" y1="60" x2="{{ cx }}" y2="180"
           stroke="#336699" stroke-width="1.5"/>
     <g transform="translate({{ cx - 60 }}, 180)">{{ flow(child.id) }}</g>
     {% endfor %}
   </svg>

Internal Block Diagram (PlantUML)
---------------------------------

``needsysml-ibd`` renders an IBD showing parts and their ports inside a
boundary rectangle.

.. code-block:: rst

   .. needsysml-ibd:: PD-002
      :show-ports: true
      :align: center

.. needsysml-ibd:: PD-002
   :show-ports: true
   :align: center

Internal Block Diagram (SVG)
----------------------------

There is no high-level ``needsysml-ibd-svg`` directive yet, but the same
result is achievable today by composing ``needsvg`` with the Jinja
helpers:

.. code-block:: rst

   .. needsvg::
      :align: center

      {% set parent = "PD-002" %}
      {% set parts = filter("type == 'part' and owned_by == '" + parent + "'") %}
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 220">
        <rect x="10" y="10" width="620" height="200"
              fill="none" stroke="#336699" stroke-dasharray="4 3"/>
        <text x="20" y="28" font-family="sans-serif" font-size="12"
              fill="#336699">{{ parent }} (IBD)</text>
        {% for part in parts %}
        {% set px = 40 + (loop.index0 * 280) %}
        <g transform="translate({{ px }}, 60)">{{ flow(part.id) }}</g>
        {% set ports = filter("type == 'port' and owned_by == '" + part.id + "'") %}
        {% for port in ports %}
        <circle cx="{{ px + (loop.index0 * 30) + 10 }}" cy="110"
                r="6" fill="#FFE0AA" stroke="#cc8800"/>
        <text x="{{ px + (loop.index0 * 30) + 10 }}" y="135"
              text-anchor="middle" font-family="monospace"
              font-size="9" fill="#666">{{ port.id }}</text>
        {% endfor %}
        {% endfor %}
      </svg>

.. needsvg::
   :align: center

   {% set parent = "PD-002" %}
   {% set parts = filter("type == 'part' and owned_by == '" + parent + "'") %}
   <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 220">
     <rect x="10" y="10" width="620" height="200"
           fill="none" stroke="#336699" stroke-dasharray="4 3"/>
     <text x="20" y="28" font-family="sans-serif" font-size="12"
           fill="#336699">{{ parent }} (IBD)</text>
     {% for part in parts %}
     {% set px = 40 + (loop.index0 * 280) %}
     <g transform="translate({{ px }}, 60)">{{ flow(part.id) }}</g>
     {% set ports = filter("type == 'port' and owned_by == '" + part.id + "'") %}
     {% for port in ports %}
     <circle cx="{{ px + (loop.index0 * 30) + 10 }}" cy="110"
             r="6" fill="#FFE0AA" stroke="#cc8800"/>
     <text x="{{ px + (loop.index0 * 30) + 10 }}" y="135"
           text-anchor="middle" font-family="monospace"
           font-size="9" fill="#666">{{ port.id }}</text>
     {% endfor %}
     {% endfor %}
   </svg>

Requirements Diagram (PlantUML)
-------------------------------

``needsysml-req`` renders a requirements diagram with satisfy / refine /
allocate links.

.. code-block:: rst

   .. needsysml-req:: type == 'requirement'
      :show-satisfy: true
      :show-refine: true
      :show-allocate: true
      :align: center

.. needsysml-req:: type == 'requirement'
   :show-satisfy: true
   :show-refine: true
   :show-allocate: true
   :align: center

Requirements Diagram (SVG)
--------------------------

A simple SVG list of requirements with their satisfy links, built using
``needsvg``:

.. code-block:: rst

   .. needsvg::
      :align: center

      {% set reqs = filter("type == 'requirement'") | list %}
      <svg xmlns="http://www.w3.org/2000/svg"
           viewBox="0 0 640 {{ 40 + (reqs | length) * 60 }}">
        {% for r in reqs %}
        <g transform="translate(20, {{ 20 + loop.index0 * 60 }})">
          <a href="{{ ref(r.id) }}">
            <rect width="120" height="40" rx="4" fill="#ddeeff" stroke="#336699"/>
            <text x="60" y="16" text-anchor="middle" font-size="10" fill="#666">{{ r.id }}</text>
            <text x="60" y="30" text-anchor="middle" font-size="11">{{ r.title }}</text>
          </a>
        </g>
        {% if r.satisfies %}
        <text x="160" y="{{ 45 + loop.index0 * 60 }}"
              font-family="sans-serif" font-size="11" fill="#444">
          satisfies → {{ r.satisfies }}
        </text>
        {% endif %}
        {% endfor %}
      </svg>

.. needsvg::
   :align: center

   {% set reqs = filter("type == 'requirement'") | list %}
   <svg xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 640 {{ 40 + (reqs | length) * 60 }}">
     {% for r in reqs %}
     <g transform="translate(20, {{ 20 + loop.index0 * 60 }})">
       <a href="{{ ref(r.id) }}">
         <rect width="120" height="40" rx="4" fill="#ddeeff" stroke="#336699"/>
         <text x="60" y="16" text-anchor="middle" font-size="10" fill="#666">{{ r.id }}</text>
         <text x="60" y="30" text-anchor="middle" font-size="11">{{ r.title }}</text>
       </a>
     </g>
     {% if r.satisfies %}
     <text x="160" y="{{ 45 + loop.index0 * 60 }}"
           font-family="sans-serif" font-size="11" fill="#444">
       satisfies → {{ r.satisfies }}
     </text>
     {% endif %}
     {% endfor %}
   </svg>

Query Tables
------------

Once the model is in place, ``sphinx-needs`` queries work across every
SysML element:

.. code-block:: rst

   .. needtable::
      :filter: type == 'requirement' and satisfies != ""
      :columns: id, title, satisfies, refines, status

.. needtable::
   :filter: type == 'requirement' and satisfies != ""
   :columns: id, title, satisfies, refines, status

.. code-block:: rst

   .. needtable::
      :filter: type == 'part'
      :columns: id, title, definition, owned_by

.. needtable::
   :filter: type == 'part'
   :columns: id, title, definition, owned_by

Allocation Matrix (v1.1)
------------------------

The ``needsysml-alloc`` directive renders a traceability table showing
which requirements allocate to which parts. Rows are needs with
non-empty ``allocates``; columns are the unique part IDs referenced.

.. needsysml-alloc::

You can also filter explicitly:

.. code-block:: rst

   .. needsysml-alloc::
      :rows: type == 'requirement'
      :columns: type == 'part'

Parametric Diagram (v1.1)
-------------------------

Parametric diagrams show constraint blocks with their parameters and
binding connectors to value properties. PlantUML uses a class-diagram
approximation.

First, define the constraint parameters and block:

.. constraintparameter:: fuel_output_param
   :id: PARAM-010

.. constraintparameter:: fuel_duration_param
   :id: PARAM-011

.. constraintparameter:: fuel_efficiency_param
   :id: PARAM-012

.. constraintblock:: FuelConsumptionEquation
   :id: CONSTRAINT-010
   :parameters: PARAM-010, PARAM-011, PARAM-012
   :expression: fuel_used = output * duration / efficiency

Then define value properties on parts and bind them:

.. valueproperty:: engine_power
   :id: VALUE-010
   :owned_by: P-002
   :value_type: kW
   :default_value: "150"

.. valueproperty:: trip_time
   :id: VALUE-011
   :owned_by: P-001
   :value_type: h

.. valueproperty:: engine_efficiency
   :id: VALUE-012
   :owned_by: P-002
   :value_type: ""

.. bindingconnector:: bind_output
   :id: BIND-010
   :source_parameter: PARAM-010
   :target_value: VALUE-010
   :unit: kW

.. bindingconnector:: bind_duration
   :id: BIND-011
   :source_parameter: PARAM-011
   :target_value: VALUE-011
   :unit: h

.. bindingconnector:: bind_efficiency
   :id: BIND-012
   :source_parameter: PARAM-012
   :target_value: VALUE-012

Render the parametric diagram:

.. needsysml-par:: CONSTRAINT-010
   :align: center
