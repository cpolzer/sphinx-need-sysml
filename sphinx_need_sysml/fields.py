"""SysML v2 extra field definitions for sphinx-needs registration."""

from typing import TypedDict


class _FieldSchema(TypedDict, total=False):
    type: str
    enum: list[str]


class _FieldBase(TypedDict):
    name: str
    description: str


class FieldDef(_FieldBase, total=False):
    schema: _FieldSchema


SYSML_FIELDS: list[FieldDef] = [
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
    # === New in feature 002-full-sysml-diagrams ===
    # State-machine
    {
        "name": "pseudo_kind",
        "description": (
            "Pseudostate kind for a state: initial / final / "
            "shallowHistory / deepHistory / choice / junction. "
            "Absent means an ordinary state."
        ),
        "schema": {
            "type": "string",
            "enum": [
                "initial",
                "final",
                "shallowHistory",
                "deepHistory",
                "choice",
                "junction",
            ],
        },
    },
    {
        "name": "from_state",
        "description": "Source state need ID for a Transition",
        "schema": {"type": "string"},
    },
    {
        "name": "to_state",
        "description": "Target state need ID for a Transition",
        "schema": {"type": "string"},
    },
    {
        "name": "trigger",
        "description": "Trigger event name for a Transition",
        "schema": {"type": "string"},
    },
    {
        "name": "guard",
        "description": "Guard expression for a Transition or Message",
        "schema": {"type": "string"},
    },
    {
        "name": "effect",
        "description": "Effect action name for a Transition",
        "schema": {"type": "string"},
    },
    # Activity
    {
        "name": "from_action",
        "description": "Source action need ID for a ControlFlow / ObjectFlow",
        "schema": {"type": "string"},
    },
    {
        "name": "to_action",
        "description": "Target action need ID for a ControlFlow / ObjectFlow",
        "schema": {"type": "string"},
    },
    {
        "name": "object_type",
        "description": "Type of the object passed by an ObjectFlow (free text)",
        "schema": {"type": "string"},
    },
    {
        "name": "partition",
        "description": "Swimlane partition name for an Action (free text)",
        "schema": {"type": "string"},
    },
    {
        "name": "activity_kind",
        "description": (
            "Special activity node kind: normal / decision / merge / "
            "fork / join (default normal)"
        ),
        "schema": {
            "type": "string",
            "enum": ["normal", "decision", "merge", "fork", "join"],
        },
    },
    # Package
    {
        "name": "parent_package",
        "description": "Parent Package need ID for nesting",
        "schema": {"type": "string"},
    },
    {
        "name": "kind",
        "description": "Dependency kind: use / import / realize",
        "schema": {
            "type": "string",
            "enum": ["use", "import", "realize"],
        },
    },
    {
        "name": "source_ref",
        "description": (
            "Source need ID for a Dependency. Named source_ref (not source) "
            "to avoid collision with sphinx-needs' built-in need.source "
            "attribute which holds the directive's source location."
        ),
        "schema": {"type": "string"},
    },
    {
        "name": "target_ref",
        "description": (
            "Target need ID for a Dependency. Named target_ref (not target) "
            "to mirror source_ref."
        ),
        "schema": {"type": "string"},
    },
    # Use case
    {
        "name": "subject",
        "description": "System boundary label for a UseCase (free text)",
        "schema": {"type": "string"},
    },
    {
        "name": "extends",
        "description": "Comma-list of UseCase IDs this UseCase extends",
        "schema": {"type": "string"},
    },
    {
        "name": "includes",
        "description": "Comma-list of UseCase IDs this UseCase includes",
        "schema": {"type": "string"},
    },
    {
        "name": "generalizes",
        "description": "Comma-list of UseCase IDs this UseCase generalizes",
        "schema": {"type": "string"},
    },
    {
        "name": "interacts_with",
        "description": (
            "Comma-list of UseCase IDs this Actor participates in. "
            "Renderer draws one solid association line per listed UseCase."
        ),
        "schema": {"type": "string"},
    },
    # Sequence
    {
        "name": "represents",
        "description": "Need ID this Lifeline represents (a Part, Actor, or Subsystem)",
        "schema": {"type": "string"},
    },
    {
        "name": "from_lifeline",
        "description": "Source Lifeline need ID for a Message",
        "schema": {"type": "string"},
    },
    {
        "name": "to_lifeline",
        "description": "Target Lifeline need ID for a Message",
        "schema": {"type": "string"},
    },
    {
        "name": "message_kind",
        "description": "Message kind: sync / async / return (default sync)",
        "schema": {
            "type": "string",
            "enum": ["sync", "async", "return"],
        },
    },
    {
        "name": "fragment_group",
        "description": (
            "Identifier of the combined-fragment group this Message belongs "
            "to. Messages sharing a fragment_group render in a single frame."
        ),
        "schema": {"type": "string"},
    },
    {
        "name": "fragment_kind",
        "description": (
            "Combined-fragment kind: alt / opt / loop / par / neg / critical."
            " Honored on the first message in a fragment_group; subsequent "
            "messages inherit."
        ),
        "schema": {
            "type": "string",
            "enum": ["alt", "opt", "loop", "par", "neg", "critical"],
        },
    },
    {
        "name": "fragment_guard",
        "description": "Guard expression printed in a combined-fragment header",
        "schema": {"type": "string"},
    },
    # Parametric
    {
        "name": "expression",
        "description": (
            "Plain-text expression describing a ConstraintBlock relationship "
            "(e.g. 'fuel = output * duration / efficiency')"
        ),
        "schema": {"type": "string"},
    },
    {
        "name": "parameters",
        "description": (
            "Comma-list of ConstraintParameter IDs owned by a ConstraintBlock"
        ),
        "schema": {"type": "string"},
    },
    {
        "name": "value_type",
        "description": "Type/unit label for a ValueProperty (e.g. 'kW')",
        "schema": {"type": "string"},
    },
    {
        "name": "default_value",
        "description": "Default value for a ValueProperty (string form)",
        "schema": {"type": "string"},
    },
    {
        "name": "unit",
        "description": (
            "Unit label printed on a BindingConnector arrow or on a ValueProperty"
        ),
        "schema": {"type": "string"},
    },
    {
        "name": "source_parameter",
        "description": (
            "ConstraintParameter need ID — source end of a BindingConnector"
        ),
        "schema": {"type": "string"},
    },
    {
        "name": "target_value",
        "description": ("ValueProperty need ID — target end of a BindingConnector"),
        "schema": {"type": "string"},
    },
]
