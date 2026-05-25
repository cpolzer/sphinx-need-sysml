# AGENTS.md — sphinx-need-sysml

## Project

Sphinx extension registering 14 SysML v2 need types, 15 extra fields, and 4 diagram directives that wrap `.. needuml::` with pre-baked Jinja2 templates.

## Commands

```bash
# Setup
python -m venv .venv && source .venv/bin/activate
pip install -e ".[test,docs]"

# Test (fast)
pytest tests/ -v

# Lint + format check
ruff check sphinx_need_sysml/ tests/
ruff format --check sphinx_need_sysml/ tests/

# Auto-fix
ruff check --fix sphinx_need_sysml/ tests/
ruff format sphinx_need_sysml/ tests/

# Type check
mypy sphinx_need_sysml/

# Build docs
sphinx-build -b html -W docs docs/_build/html
```

CI order: **lint → test → docs-build**. All must pass on PRs.

## Architecture

- **Package**: `sphinx_need_sysml/` — top-level Python package
- **Build**: flit (`[tool.flit.module] name = "sphinx_need_sysml"`)
- **Entry point**: `sphinx_need_sysml/__init__.py` → `setup(app)`
- **Registration flow**: `config-inited` event registers need types + fields via `add_need_type` / `add_field` with `add_extra_option` fallback shim
- **Flow configs**: merged into `needs_flow_configs` at `builder-inited`; user keys take precedence
- **Diagram directives**: each wraps `NeedumlDirective` with a config key + Jinja2 template from `templates.py`
- **SVG path**: `needsysml-bdd-svg` uses `sphinx_need_svg.jinja_context.render_jinja_svg`, registered only when `sphinx_need_svg` is importable (`_HAS_NEED_SVG` flag)

## Key Gotchas

- **`needs_id_regex`** — default sphinx-needs regex rejects hyphenated IDs like `PD-001`. Test projects need `needs_id_regex = "^[A-Z0-9_-]+"`.
- **`needs_fields`** (sphinx-needs ≥ 6) expects a dict, not a list. Don't set it in test conf.py unless needed.
- **`_needs_all_needs`** — sphinx-needs stores needs on `env._needs_all_needs` (private attr). Tests use `# noqa: SLF001`.
- **PlantUML not required** — extension works without it; diagrams emit warnings but don't break the build.
- **Template `{root_id}` replacement** — `BDD_FULL_TEMPLATE` and `IBD_FULL_TEMPLATE` use `{root_id}` as a literal string placeholder (not Jinja), replaced via `.replace()` before passing to needuml.

## Test Structure

- `tests/doc_test/basic/` — minimal project with all 14 need types + 3 diagram directives
- `tests/doc_test/full_example/` — vehicle system example with all diagram types + SVG directive
- Fixtures use `sphinx.testing.fixtures` plugin; `make_app` + `app.build()` is the standard pattern
- Test matrix: Python 3.10–3.12 × Sphinx 5.0/7.2.5/8.1.3 × sphinx-needs 2.1–8.0.0 (via nox)

## Release

- Version in `pyproject.toml` and `sphinx_need_sysml/__init__.py:VERSION`
- `cz bump` (commitizen) auto-bumps on push to main if conventional commits warrant it
- Push `v*` tag → GitHub Actions builds and publishes to PyPI

## Branch Protection

`main` requires: lint, test (3.10/3.11/3.12), docs-build to pass. 1 review required (admin can bypass).
