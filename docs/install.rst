Installation
============

Requirements
------------

- Python ≥ 3.10
- Sphinx ≥ 4.0
- sphinx-needs ≥ 1.0
- sphinxcontrib-plantuml (optional, required for diagram rendering)
- PlantUML binary (optional, required for diagram rendering)

Install from PyPI
-----------------

.. code-block:: bash

   pip install sphinxcontrib-sysml

For diagram rendering, also install:

.. code-block:: bash

   pip install sphinxcontrib-plantuml

And ensure the ``plantuml`` binary is on your ``PATH``, or set it in ``conf.py``:

.. code-block:: python

   plantuml = "/usr/bin/plantuml"

Enable the Extension
--------------------

Add to your ``conf.py``:

.. code-block:: python

   extensions = [
       "sphinx_needs",
       "sphinxcontrib.plantuml",  # optional but recommended
       "sphinxcontrib.sysml",
   ]

   # Required for clickable diagram links in HTML output
   plantuml_output_format = "svg"

Verify Installation
-------------------

.. code-block:: bash

   python -c "import sphinxcontrib.sysml; print(sphinxcontrib.sysml.VERSION)"

This should print ``0.1.0`` (or your installed version).
