"""Minimal Sphinx project configuration for testing sphinxcontrib.sysml."""

extensions = [
    "sphinx_needs",
    "sphinxcontrib.sysml",
]

needs_extra_options = [
    "abstract", "owned_by", "multiplicity", "direction", "conjugated",
    "definition", "satisfies", "refines", "allocates", "req_text",
    "source_port", "target_port", "is_initial", "is_final",
]
