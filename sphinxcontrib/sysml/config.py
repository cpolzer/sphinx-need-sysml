"""SysML v2 need type definitions for sphinx-needs registration."""

SYSML_NEED_TYPES = [
    # Structural types
    {
        "directive": "partdef",
        "title": "PartDef",
        "prefix": "PD-",
        "color": "#DDEEFF",
        "style": "node",
    },
    {
        "directive": "part",
        "title": "Part",
        "prefix": "P-",
        "color": "#BBDDFF",
        "style": "node",
    },
    {
        "directive": "portdef",
        "title": "PortDef",
        "prefix": "POD-",
        "color": "#FFEECC",
        "style": "node",
    },
    {
        "directive": "port",
        "title": "Port",
        "prefix": "PO-",
        "color": "#FFE0AA",
        "style": "node",
    },
    {
        "directive": "interfacedef",
        "title": "InterfaceDef",
        "prefix": "IFD-",
        "color": "#DDEEDD",
        "style": "node",
    },
    {
        "directive": "interface",
        "title": "Interface",
        "prefix": "IF-",
        "color": "#BBDDBB",
        "style": "node",
    },
    {
        "directive": "connectiondef",
        "title": "ConnectionDef",
        "prefix": "CD-",
        "color": "#EEDDFF",
        "style": "node",
    },
    {
        "directive": "connection",
        "title": "Connection",
        "prefix": "C-",
        "color": "#DDCCFF",
        "style": "node",
    },
    # Behavioral types
    {
        "directive": "actiondef",
        "title": "ActionDef",
        "prefix": "AD-",
        "color": "#FFEEDD",
        "style": "node",
    },
    {
        "directive": "action",
        "title": "Action",
        "prefix": "A-",
        "color": "#FFE0CC",
        "style": "node",
    },
    {
        "directive": "statedef",
        "title": "StateDef",
        "prefix": "SD-",
        "color": "#EEEEDD",
        "style": "node",
    },
    {
        "directive": "stateusage",
        "title": "StateUsage",
        "prefix": "SU-",
        "color": "#DDDDCC",
        "style": "node",
    },
    # Requirement types
    {
        "directive": "requirementdef",
        "title": "RequirementDef",
        "prefix": "RD-",
        "color": "#FFF0CC",
        "style": "node",
    },
    {
        "directive": "requirement",
        "title": "Requirement",
        "prefix": "R-",
        "color": "#FFEEAA",
        "style": "node",
    },
]
