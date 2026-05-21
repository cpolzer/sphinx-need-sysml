"""Test fixture for the needsysml-sd directive."""

extensions = [
    "sphinx_needs",
    "sphinxcontrib.plantuml",
    "sphinx_need_sysml",
]

needs_id_regex = "^[A-Z0-9_-]+"
plantuml_output_format = "svg"
master_doc = "index"
exclude_patterns = ["_build"]
