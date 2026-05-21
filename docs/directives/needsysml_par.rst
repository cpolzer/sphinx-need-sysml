needsysml-par Directive
=======================

The ``.. needsysml-par::`` directive generates a Parametric Diagram
from a root ``ConstraintBlock`` need. A companion
``.. needsysml-par-svg::`` renders the same diagram as inline SVG.

.. note::

   PlantUML has no native parametric diagram mode. This directive uses
   a class-diagram approximation: the constraint block is rendered as a
   ``<<constraint>>``-stereotyped class with a parameter compartment,
   and binding connectors as labelled arrows to value-property boxes.

Usage
-----

.. code-block:: rst

   .. needsysml-par:: <constraintblock-id>
      :scale: <N>%
      :align: <left|center|right>

   .. needsysml-par-svg:: <constraintblock-id>
      :align: <left|center|right>

Required Argument
~~~~~~~~~~~~~~~~~

``<constraintblock-id>``
   The ID of the root ``ConstraintBlock`` need. The directive renders
   the block, its parameters, and the value properties bound to those
   parameters by ``BindingConnector`` edges.

Options
-------

``:scale: <N>%``
   PlantUML variant only.

``:align: <left|center|right>``
   Horizontal alignment. Default ``center``.

How It Works
------------

The PlantUML directive wraps ``.. needuml::`` with ``:config:
sysml_par`` and the ``PAR_FULL_TEMPLATE`` body. The template:

1. Renders the ``ConstraintBlock`` as a ``<<constraint>>``-stereotyped
   class with its ``expression`` and parameter compartment.
2. Iterates ``BindingConnector`` needs, drawing labelled arrows from
   constraint parameters to value properties.
3. The ``unit`` field on each ``BindingConnector`` appears as the arrow
   label.

The SVG companion (``PAR_SVG_TEMPLATE``) lays out the constraint block
rectangle with parameter port circles and value-property boxes,
connected by dashed lines with unit labels.

Example
-------

.. code-block:: rst

   .. constraintparameter:: output_param
      :id: PARAM-001

   .. constraintblock:: FuelConsumption
      :id: CONSTRAINT-001
      :parameters: PARAM-001
      :expression: fuel = output * duration / efficiency

   .. valueproperty:: engine_output
      :id: VALUE-001
      :value_type: kW

   .. bindingconnector::
      :id: BIND-001
      :source_parameter: PARAM-001
      :target_value: VALUE-001
      :unit: kW

   .. needsysml-par:: CONSTRAINT-001
      :align: center

Clickable Links
---------------

PlantUML variant: each element carries a ``[[<docname>.html#<id>]]``
link active when ``plantuml_output_format = "svg"``. SVG variant: each
element is wrapped in a native ``<a href>``.
