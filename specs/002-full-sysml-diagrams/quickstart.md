# Quickstart: Full SysML v2 Diagram Coverage

**Date**: 2026-05-20

This quickstart shows an engineer the shortest path from a fresh Sphinx project to a working SysML model with every diagram type rendered. Assumes feature `002-full-sysml-diagrams` has shipped (v1 ≥ 0.3.0; v1.1 features marked).

---

## Install

```bash
pip install "sphinxcontrib-sysml>=0.3.0" sphinxcontrib-plantuml sphinx-need-svg
```

`sphinx-need-svg` is optional but unlocks the `-svg` companion directives.

## conf.py

```python
extensions = [
    "sphinx_needs",
    "sphinxcontrib.plantuml",
    "sphinxcontrib.sysml",
    "sphinx_need_svg",      # optional
]
plantuml_output_format = "svg"
```

No additional configuration is required — the extension auto-registers all 27 need types and all flow configs at setup time.

---

## Five-minute model walkthrough

The vehicle example in `docs/examples/vehicle_system.rst` exercises every diagram. The snippets below show one section per diagram — enough to render a working model.

### 1. State machine (v1)

```rst
.. statedef:: EngineState
   :id: SD-001

   Lifecycle of the engine.

.. stateusage:: off
   :id: SU-001
   :definition: SD-001
   :pseudo_kind: initial

.. stateusage:: starting
   :id: SU-002
   :definition: SD-001

.. stateusage:: running
   :id: SU-003
   :definition: SD-001

.. stateusage:: stopping
   :id: SU-004
   :definition: SD-001

.. transition:: key_on
   :id: TRANS-001
   :from_state: SU-001
   :to_state: SU-002
   :trigger: key_on
   :effect: start_seq

.. transition:: engine_ok
   :id: TRANS-002
   :from_state: SU-002
   :to_state: SU-003
   :trigger: engine_ok

.. transition:: key_off
   :id: TRANS-003
   :from_state: SU-003
   :to_state: SU-004
   :trigger: key_off

.. transition:: spindown
   :id: TRANS-004
   :from_state: SU-004
   :to_state: SU-001
   :trigger: spindown_complete

.. needsysml-stm:: SD-001
   :align: center

.. needsysml-stm-svg:: SD-001
   :align: center
```

### 2. Activity (v1)

```rst
.. actiondef:: StartEngine
   :id: AD-001

   Cold-start procedure.

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

.. action:: crank_starter
   :id: A-004
   :definition: AD-001
   :partition: ECU

.. controlflow::
   :id: CTRLFLOW-001
   :from_action: A-001
   :to_action: A-002

.. controlflow::
   :id: CTRLFLOW-002
   :from_action: A-002
   :to_action: A-003

.. controlflow::
   :id: CTRLFLOW-003
   :from_action: A-003
   :to_action: A-004

.. needsysml-act:: AD-001
   :align: center

.. needsysml-act-svg:: AD-001
   :align: center
```

### 3. Sequence (v1)

```rst
.. actiondef:: IgnitionSequence
   :id: AD-010

   Driver → ECU → Starter interaction at key-on.

.. lifeline:: driver_ll
   :id: LIFELINE-001
   :definition: AD-010
   :represents: ACTOR-001

.. lifeline:: ecu_ll
   :id: LIFELINE-002
   :definition: AD-010
   :represents: PD-010

.. lifeline:: starter_ll
   :id: LIFELINE-003
   :definition: AD-010
   :represents: PD-011

.. message:: turn_key
   :id: MSG-001
   :from_lifeline: LIFELINE-001
   :to_lifeline: LIFELINE-002
   :message_kind: sync

.. message:: crank
   :id: MSG-002
   :from_lifeline: LIFELINE-002
   :to_lifeline: LIFELINE-003
   :message_kind: async
   :fragment_group: F1
   :fragment_kind: alt
   :fragment_guard: key_position == "start"

.. message:: ok
   :id: MSG-003
   :from_lifeline: LIFELINE-003
   :to_lifeline: LIFELINE-002
   :message_kind: return
   :fragment_group: F1

.. needsysml-sd:: AD-010
   :align: center

.. needsysml-sd-svg:: AD-010
   :align: center
```

### 4. Use case (v1)

```rst
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

.. needsysml-uc:: type == 'UseCase'
   :subject: Vehicle
   :align: center

.. needsysml-uc-svg:: type == 'UseCase'
   :subject: Vehicle
   :align: center
```

### 5. Package (v1)

```rst
.. package:: VehicleSystem
   :id: PKG-001

.. package:: Powertrain
   :id: PKG-002
   :parent_package: PKG-001

.. package:: Chassis
   :id: PKG-003
   :parent_package: PKG-001

.. dependency::
   :id: DEP-001
   :source: PKG-002
   :target: PKG-003
   :kind: use

.. needsysml-pkg:: PKG-001
   :depth: 3
   :align: center

.. needsysml-pkg-svg:: PKG-001
   :align: center
```

### 6. Allocation matrix (v1.1)

```rst
.. needsysml-alloc::

.. needsysml-alloc::
   :rows: type == 'Action'
   :columns: type == 'Part'
```

The first invocation uses the defaults from spec Q3 (rows = needs with non-empty `allocates`, columns = needs referenced by those allocations). The second invocation explicitly maps actions to parts.

### 7. Parametric (v1.1)

```rst
.. constraintparameter:: output_param
   :id: PARAM-001

.. constraintparameter:: duration_param
   :id: PARAM-002

.. constraintparameter:: efficiency_param
   :id: PARAM-003

.. constraintparameter:: fuel_param
   :id: PARAM-004

.. constraintblock:: FuelConsumption
   :id: CONSTRAINT-001
   :parameters: PARAM-001, PARAM-002, PARAM-003, PARAM-004
   :expression: fuel = output * duration / efficiency

.. valueproperty:: engine_output
   :id: VALUE-001
   :owned_by: P-002
   :value_type: kW
   :default_value: "150"

.. valueproperty:: trip_duration
   :id: VALUE-002
   :owned_by: P-001
   :value_type: s

.. bindingconnector::
   :id: BIND-001
   :source_parameter: PARAM-001
   :target_value: VALUE-001
   :unit: kW

.. bindingconnector::
   :id: BIND-002
   :source_parameter: PARAM-002
   :target_value: VALUE-002
   :unit: s

.. needsysml-par:: CONSTRAINT-001
   :align: center

.. needsysml-par-svg:: CONSTRAINT-001
   :align: center
```

---

## Build and verify

```bash
sphinx-build -W docs docs/_build/html
```

The `-W` strict mode catches missing references and empty diagrams. Per spec edge cases, an unknown `from_state` reference produces one categorized warning and a `??` placeholder on the diagram rather than a build failure under default settings; with `-W` the warning becomes an error.

Browse `docs/_build/html/examples/vehicle_system.html` and click any state, action, lifeline, package, or actor box — it navigates to the need's definition anchor on the page.

---

## Troubleshooting

- **"Unknown directive `needsysml-stm-svg`"** — `sphinx-need-svg` is not installed or not in `extensions`. The PlantUML `needsysml-stm` still works without it.
- **PlantUML diagram links don't navigate** — `plantuml_output_format` is not `svg`. Set it in `conf.py`.
- **Build hangs at `pickling environment...`** — large activity diagrams with many partitions and flows may take seconds to render. SC-008 budgets the full vehicle example at < 30 s.
- **State diagram shows ordinary boxes instead of pseudostates** — your `StateUsage` is missing `:pseudo_kind:`. If you supplied an unrecognized value, sphinx-needs rejects it at parse time with a schema-validation error (the `pseudo_kind` field is enum-constrained); fix the value to one of `initial`, `final`, `shallowHistory`, `deepHistory`, `choice`, `junction`.
- **`needsysml-act` skips a swimlane** — verify each `Action`'s `:partition:` is spelled consistently across the activity. `partition: "Driver"` and `partition: "driver"` group into different lanes.

---

## v1 verification results (measured 2026-05-21)

Recorded against the full vehicle example with all v1 diagrams (bdd, ibd, req, stm, act, sd, uc, pkg) rendered side-by-side in PlantUML and SVG.

| Success criterion | Target | Measured |
|---|---|---|
| SC-003 Strict docs build is clean | 0 warnings | ✅ 0 warnings |
| SC-004 Drawn nodes link to need anchors | 100% | ✅ 78 unique need-anchor `href` links in `vehicle_system.html` |
| SC-008 Vehicle example build wall-clock | < 30 s | ✅ 10.5 s on dev workstation |

