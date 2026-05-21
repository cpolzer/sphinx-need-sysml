# Quickstart: Use Case Diagram SVG

## What this feature does

Fixes the `needsysml-uc-svg` directive so its output visually matches the PlantUML `needsysml-uc` directive. Specifically:

1. **Association lines** now connect from actor stick-figure arm tips to use case ellipse borders (not center points)
2. **Extend/include labels** are repositioned for better readability
3. **Generalize relationships** are now rendered (previously missing)
4. **ViewBox height** dynamically scales for large diagrams

## How to use

No API changes. Existing `.. needsysml-uc-svg::` directives will automatically render with the improved layout after upgrading.

```rst
.. actor:: Driver
   :id: ACTOR-001
   :interacts_with: USECASE-001

.. usecase:: Start engine
   :id: USECASE-001
   :subject: Vehicle
   :extends: USECASE-002

.. usecase:: Stop engine
   :id: USECASE-002
   :subject: Vehicle
   :generalizes: USECASE-003

.. usecase:: Idle engine
   :id: USECASE-003
   :subject: Vehicle

.. needsysml-uc-svg::
   :align: center
```

## Testing

```bash
# Run existing uc tests (should all pass)
pytest tests/test_uc_directive.py -v

# Run all tests to verify no regressions
pytest tests/ -v

# Lint
ruff check sphinxcontrib/sysml/svg_templates.py tests/test_uc_directive.py
ruff format --check sphinxcontrib/sysml/svg_templates.py tests/test_uc_directive.py
```

## Files changed

- `sphinxcontrib/sysml/svg_templates.py` — `UC_SVG_TEMPLATE` (~85 lines)
- `tests/test_uc_directive.py` — 3 new tests
- `tests/doc_test/uc/conf.py` — add `sphinx_need_svg` extension
- `tests/doc_test/uc/index.rst` — add `needsysml-uc-svg` directive
