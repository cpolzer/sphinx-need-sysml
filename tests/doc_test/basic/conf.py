"""Minimal Sphinx project configuration for testing sphinxcontrib.sysml."""

extensions = [
    "sphinx_needs",
    "sphinxcontrib.sysml",
]

# Allow hyphenated IDs like PD-001, R-001, etc.
needs_id_regex = "^[A-Z0-9_-]+"
