sd fixture
==========

.. actiondef:: IgnitionSequence
   :id: AD-001

   Key-on interaction.

.. lifeline:: driver_ll
   :id: LIFELINE-001
   :definition: AD-001

.. lifeline:: ecu_ll
   :id: LIFELINE-002
   :definition: AD-001

.. lifeline:: starter_ll
   :id: LIFELINE-003
   :definition: AD-001

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
   :fragment_guard: key_position == 'start'

.. message:: ok
   :id: MSG-003
   :from_lifeline: LIFELINE-003
   :to_lifeline: LIFELINE-002
   :message_kind: return
   :fragment_group: F1

.. message:: heartbeat
   :id: MSG-004
   :from_lifeline: LIFELINE-002
   :to_lifeline: LIFELINE-002
   :message_kind: async
   :fragment_group: F2
   :fragment_kind: loop
   :fragment_guard: engine_warming

.. needsysml-sd:: AD-001
   :align: center
