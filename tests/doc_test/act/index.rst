act fixture
===========

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

.. action:: fork_crank
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

.. action:: join_crank
   :id: A-007
   :definition: AD-001
   :partition: ECU
   :activity_kind: join

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

.. controlflow::
   :id: CTRLFLOW-004
   :from_action: A-004
   :to_action: A-005

.. controlflow::
   :id: CTRLFLOW-005
   :from_action: A-004
   :to_action: A-006

.. controlflow::
   :id: CTRLFLOW-006
   :from_action: A-005
   :to_action: A-007

.. controlflow::
   :id: CTRLFLOW-007
   :from_action: A-006
   :to_action: A-007

.. needsysml-act:: AD-001
   :align: center
