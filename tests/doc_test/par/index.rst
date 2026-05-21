par fixture
===========

.. constraintparameter:: output_param
   :id: PARAM-001

.. constraintparameter:: duration_param
   :id: PARAM-002

.. constraintparameter:: efficiency_param
   :id: PARAM-003

.. constraintblock:: FuelConsumption
   :id: CONSTRAINT-001
   :parameters: PARAM-001, PARAM-002, PARAM-003
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

.. valueproperty:: efficiency_val
   :id: VALUE-003
   :owned_by: P-002
   :value_type: ""

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

.. bindingconnector::
   :id: BIND-003
   :source_parameter: PARAM-003
   :target_value: VALUE-003

.. needsysml-par:: CONSTRAINT-001
   :align: center
