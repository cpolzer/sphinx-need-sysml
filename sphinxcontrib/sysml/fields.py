"""SysML v2 extra field definitions for sphinx-needs registration."""

SYSML_FIELDS = [
    {
        "name": "abstract",
        "description": "Whether this element is abstract (no direct instantiation)",
        "schema": {"type": "boolean"},
    },
    {
        "name": "owned_by",
        "description": "Parent element ID (enables hierarchy traversal in templates)",
        "schema": {"type": "string"},
    },
    {
        "name": "multiplicity",
        "description": "UML multiplicity notation, e.g. 0..1, 1..*, *",
        "schema": {"type": "string"},
    },
    {
        "name": "direction",
        "description": "Port direction: in, out, inout, ~in (conjugated in)",
        "schema": {"type": "string"},
    },
    {
        "name": "conjugated",
        "description": "Whether this port type is conjugated",
        "schema": {"type": "boolean"},
    },
    {
        "name": "definition",
        "description": "ID of the Def type this usage instantiates",
        "schema": {"type": "string"},
    },
    {
        "name": "satisfies",
        "description": "Comma-separated need IDs this element satisfies (requirements)",
        "schema": {"type": "string"},
    },
    {
        "name": "refines",
        "description": "Comma-separated need IDs this requirement refines",
        "schema": {"type": "string"},
    },
    {
        "name": "allocates",
        "description": "Comma-separated need IDs allocated to this element",
        "schema": {"type": "string"},
    },
    {
        "name": "req_text",
        "description": "Formal requirement statement text",
        "schema": {"type": "string"},
    },
    {
        "name": "source_port",
        "description": "Need ID of the source Port for a connection",
        "schema": {"type": "string"},
    },
    {
        "name": "target_port",
        "description": "Need ID of the target Port for a connection",
        "schema": {"type": "string"},
    },
    {
        "name": "is_initial",
        "description": "Whether this is the initial state",
        "schema": {"type": "boolean"},
    },
    {
        "name": "is_final",
        "description": "Whether this is the final state",
        "schema": {"type": "boolean"},
    },
]
