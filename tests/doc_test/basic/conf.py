"""Minimal Sphinx project configuration for testing sphinx_need_sysml."""

extensions = [
    "sphinx_needs",
    "sphinxcontrib.plantuml",
    "sphinx_need_sysml",
]

# Allow hyphenated IDs like PD-001, R-001, etc.
needs_id_regex = "^[A-Z0-9_-]+"

# Required for clickable diagrams in HTML
plantuml_output_format = "svg"
