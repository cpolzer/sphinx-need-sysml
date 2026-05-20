uc fixture
==========

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

.. needsysml-uc::
   :align: center
