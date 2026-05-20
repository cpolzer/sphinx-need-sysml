"""Sphinx documentation project configuration for sphinxcontrib-sysml."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

extensions = [
    "sphinx_needs",
    "sphinxcontrib.plantuml",
    "sphinxcontrib.sysml",
    "sphinx_need_svg",
    "sphinx_immaterial",
]

needs_id_regex = "^[A-Z0-9_-]+"
plantuml_output_format = "svg"

# Theme
html_theme = "sphinx_immaterial"
html_theme_options = {
    "repo_url": "https://github.com/user/sphinxcontrib-sysml",
    "repo_name": "sphinxcontrib-sysml",
}

project = "sphinxcontrib-sysml"
copyright = "2026, sphinxcontrib-sysml contributors"
master_doc = "index"
