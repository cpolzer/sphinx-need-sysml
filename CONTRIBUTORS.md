# Contributors

sphinxcontrib-sysml is developed by the following contributors:

| Name | Role |
|------|------|
| Chris | Author & Maintainer |

## Local Development

### Prerequisites

- Python ≥ 3.10
- `pip` or `uv`

### Setup

```bash
# Clone the repository
git clone https://github.com/user/sphinxcontrib-sysml.git
cd sphinxcontrib-sysml

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate

# Install the package in editable mode with dev dependencies
pip install -e ".[test,docs]"
pip install pre-commit ruff mypy nox

# (Optional) Install PlantUML for diagram rendering
# sudo apt install plantuml  # Debian/Ubuntu
# brew install plantuml      # macOS

# Install pre-commit hooks
pre-commit install
```

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run a specific test file
pytest tests/test_need_types.py -v

# Run tests with coverage
pytest tests/ --cov=sphinxcontrib.sysml --cov-report=html
```

### Running Nox Sessions

```bash
# Run tests across Python/Sphinx version matrix
nox -s tests

# Run linting
nox -s lint

# Build documentation
nox -s docs
```

### Building Documentation

```bash
source .venv/bin/activate
cd docs
sphinx-build -b html . _build/html
# Open _build/html/index.html in a browser
```

### Code Style

This project uses **ruff** for linting and formatting:

```bash
# Check for lint issues
ruff check sphinxcontrib/ tests/

# Auto-fix fixable issues
ruff check --fix sphinxcontrib/ tests/

# Check formatting
ruff format --check sphinxcontrib/ tests/

# Apply formatting
ruff format sphinxcontrib/ tests/
```

### Type Checking

```bash
mypy sphinxcontrib/sysml/
```

## CI Flow

The project uses **GitHub Actions** for continuous integration. The CI pipeline
runs on every push to `main` and on all pull requests.

### Pipeline Stages

1. **Lint** — `ruff check` and `ruff format --check` on all Python files
2. **Type Check** — `mypy sphinxcontrib/sysml/` with strict mode
3. **Test** — `nox -s tests` runs the test matrix:
   - Python 3.10, 3.12
   - Sphinx 5.0, 7.2.5, 8.1.3
   - sphinx-needs 2.1, 4.2, 5.1, 6.0.0, 6.3.0, 8.0.0
4. **Docs Build** — `nox -s docs` verifies documentation builds without errors

### Passing CI

- All lint checks must pass (no ruff violations)
- All type checks must pass (no mypy errors)
- All test combinations must pass (48+ tests)
- Documentation must build without errors

### Pre-commit

Install `pre-commit` hooks locally to catch issues before pushing:

```bash
pre-commit install
pre-commit run --all-files
```

## Pull Request Process

1. Create a feature branch from `main`
2. Make your changes and add/update tests
3. Run `pytest tests/ -v` and `ruff check sphinxcontrib/ tests/` locally
4. Push your branch and open a pull request
5. Ensure all CI checks pass
6. Request review from a maintainer

## Release Process

1. Update `VERSION` in `sphinxcontrib/sysml/__init__.py`
2. Update `CHANGELOG.md` with release notes
3. Create a git tag: `git tag v0.1.0`
4. Push the tag: `git push origin v0.1.0`
5. GitHub Actions publishes to PyPI on tag push

## License

By contributing to this project, you agree that your contributions will be
licensed under the MIT License.
