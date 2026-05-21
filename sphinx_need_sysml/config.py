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
    # === New in feature 002-full-sysml-diagrams ===
    # State-machine
    {
        "directive": "transition",
        "title": "Transition",
        "prefix": "TRANS-",
        "color": "#EEDDDD",
        "style": "node",
    },
    # Activity
    {
        "directive": "controlflow",
        "title": "ControlFlow",
        "prefix": "CTRLFLOW-",
        "color": "#DDEEEE",
        "style": "node",
    },
    {
        "directive": "objectflow",
        "title": "ObjectFlow",
        "prefix": "OBJFLOW-",
        "color": "#CCEEDD",
        "style": "node",
    },
    # Package
    {
        "directive": "package",
        "title": "Package",
        "prefix": "PKG-",
        "color": "#EEEEFF",
        "style": "folder",
    },
    {
        "directive": "dependency",
        "title": "Dependency",
        "prefix": "DEP-",
        "color": "#DDDDDD",
        "style": "node",
    },
    # Use case
    {
        "directive": "usecase",
        "title": "UseCase",
        "prefix": "USECASE-",
        "color": "#FFEEDD",
        "style": "node",
    },
    {
        "directive": "actor",
        "title": "Actor",
        "prefix": "ACTOR-",
        "color": "#EEEECC",
        "style": "actor",
    },
    # Parametric
    {
        "directive": "constraintblock",
        "title": "ConstraintBlock",
        "prefix": "CONSTRAINT-",
        "color": "#FFF0DC",
        "style": "node",
    },
    {
        "directive": "constraintparameter",
        "title": "ConstraintParameter",
        "prefix": "PARAM-",
        "color": "#FFE8C8",
        "style": "node",
    },
    {
        "directive": "valueproperty",
        "title": "ValueProperty",
        "prefix": "VALUE-",
        "color": "#E8F4FF",
        "style": "node",
    },
    {
        "directive": "bindingconnector",
        "title": "BindingConnector",
        "prefix": "BIND-",
        "color": "#D8E8FF",
        "style": "node",
    },
    # Sequence
    {
        "directive": "lifeline",
        "title": "Lifeline",
        "prefix": "LIFELINE-",
        "color": "#E0E8F0",
        "style": "node",
    },
    {
        "directive": "message",
        "title": "Message",
        "prefix": "MSG-",
        "color": "#D0E0F0",
        "style": "node",
    },
]
