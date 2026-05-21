pkg fixture
===========

.. package:: VehicleSystem
   :id: PKG-001

   Top-level package.

.. package:: Powertrain
   :id: PKG-002
   :parent_package: PKG-001

.. package:: Chassis
   :id: PKG-003
   :parent_package: PKG-001

.. dependency:: pt_uses_chassis
   :id: DEP-001
   :source_ref: PKG-002
   :target_ref: PKG-003
   :kind: use

.. dependency:: pt_imports_chassis
   :id: DEP-002
   :source_ref: PKG-002
   :target_ref: PKG-003
   :kind: import

.. needsysml-pkg:: PKG-001
   :align: center
