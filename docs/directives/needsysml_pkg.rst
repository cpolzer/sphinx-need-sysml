needsysml-pkg Directive
=======================

The ``.. needsysml-pkg::`` directive generates a Package Diagram from a
root ``Package`` need. A companion ``.. needsysml-pkg-svg::`` renders the
same diagram as inline SVG.

Usage
-----

.. code-block:: rst

   .. needsysml-pkg:: <root-package-id>
      :depth: <N>
      :scale: <N>%
      :align: <left|center|right>

   .. needsysml-pkg-svg:: <root-package-id>
      :align: <left|center|right>

Required Argument
~~~~~~~~~~~~~~~~~

``<root-package-id>``
   The ID of the root ``Package`` need. The directive walks
   ``parent_package`` relationships to build the nested tree.

Options
-------

``:depth: <N>``
   Maximum nesting depth (default 3 — root + 2 levels of children).
   PlantUML variant only.

``:scale: <N>%``
   PlantUML variant only.

``:align: <left|center|right>``
   Horizontal alignment. Default ``center``.

Nesting
-------

A ``Package`` need with a ``:parent_package: <id>`` field renders inside
its parent's rectangle in the diagram.

Dependencies
------------

A ``Dependency`` need wires two packages together:

.. code-block:: rst

   .. dependency:: pt_uses_chassis
      :id: DEP-001
      :source_ref: PKG-002
      :target_ref: PKG-003
      :kind: use

The ``:kind:`` enum values:

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Value
     - Stereotype label
   * - ``use``
     - ``<<use>>`` (default)
   * - ``import``
     - ``<<import>>``
   * - ``realize``
     - ``<<realize>>``

How It Works
------------

The PlantUML directive wraps ``.. needuml::`` with ``:config:
sysml_pkg`` and the ``PKG_FULL_TEMPLATE`` body. The template renders
the root package plus two levels of nested children (``depth=3``
covers most system organizations) and then emits one dashed arrow per
``Dependency`` with its kind stereotype label.

The SVG companion (``PKG_SVG_TEMPLATE``) lays out the root rectangle
with its direct children inside as smaller rectangles arranged
horizontally, and draws labelled dashed arrows for each dependency.

.. note::

   The template is unrolled rather than recursive because the
   minijinja engine that ``needuml`` uses does not support
   ``list.append()`` — needed for recursive macros. For deeper nesting
   you can compose multiple ``needsysml-pkg`` invocations, each rooted
   at a different parent.

Clickable Links
---------------

PlantUML variant: each ``package`` carries a ``[[<docname>.html#<id>]]``
link active when ``plantuml_output_format = "svg"``. SVG variant: each
package rectangle is wrapped in a native ``<a href>``.
