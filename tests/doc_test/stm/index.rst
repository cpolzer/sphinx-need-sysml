stm fixture
===========

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
