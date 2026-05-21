"""Sphinx documentation project configuration for sphinx-need-sysml."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

extensions = [
    "sphinx_needs",
    "sphinxcontrib.plantuml",
    "sphinx_need_sysml",
    "sphinx_need_svg",
    "sphinx_immaterial",
]

needs_id_regex = "^[A-Z0-9_-]+"
plantuml_output_format = "svg"

# Theme
html_theme = "sphinx_immaterial"
html_theme_options = {
    "repo_url": "https://github.com/user/sphinx-need-sysml",
    "repo_name": "sphinx-need-sysml",
}

project = "sphinx-need-sysml"
copyright = "2026, sphinx-need-sysml contributors"
master_doc = "index"
