"""Full example Sphinx project configuration."""

extensions = [
    "sphinx_needs",
    "sphinxcontrib.plantuml",
    "sphinx_need_sysml",
]

needs_id_regex = "^[A-Z0-9_-]+"
plantuml_output_format = "svg"
