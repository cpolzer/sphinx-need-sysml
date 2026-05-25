sphinx-need-sysml
===================

Sphinx extension for SysML v2 need types and diagrams via sphinx-needs and PlantUML.

.. toctree::
   :maxdepth: 2
   :caption: Contents

   install
   directives/need_types
   directives/needsysml_bdd
   directives/needsysml_ibd
   directives/needsysml_req
   directives/needsysml_svg
   directives/needsysml_stm
   directives/needsysml_act
   directives/needsysml_sd
   directives/needsysml_uc
   directives/needsysml_pkg
   directives/needsysml_par
   directives/needsysml_alloc
   examples/vehicle_system

Overview
--------

``sphinx-need-sysml`` registers 14 SysML v2 need types and 15 extra fields
with sphinx-needs, enabling you to write SysML v2 structural and behavioral
elements directly in reStructuredText. It also provides three high-level
diagram directives that generate PlantUML diagrams:

- ``.. needsysml-bdd::`` — Block Definition Diagrams
- ``.. needsysml-ibd::`` — Internal Block Diagrams
- ``.. needsysml-req::`` — Requirements Diagrams

Quick Example
-------------

.. code-block:: rst

   .. partdef:: Engine
      :id: PD-001

      Engine block definition.

   .. needsysml-bdd:: PD-001
      :depth: 2

See :doc:`install` for setup instructions and :doc:`examples/vehicle_system`
for a complete worked example.

References
----------

- `SysML v2 Diagram Tutorial <https://sysml.org/tutorials/sysml-diagram-tutorial/>`_ — Official OMG tutorial covering all SysML v2 diagram types.
