"""Jinja2 template string constants for SysML v2 PlantUML diagrams.

These constants are usable as ``.. needuml::`` directive bodies for custom
diagrams. They are also used internally by the ``needsysml-*`` directives.

Note: skinparam styling is applied via the ``:config:`` option on the
``.. needuml::`` directive (e.g. ``:config: sysml_bdd``), not in the
template body itself.
"""

BLOCK_DEF_TEMPLATE = """\
class "{{ need.id }}\\n{{ need.title }}" <<PartDef>> [[{{ ref(need.id) }|{{ need.title }}]] {
{% if need.owned_by %}
    == owned_by ==
    {{ need.owned_by }}
{% endif %}
{% if need.abstract %}
    == abstract ==
    {{ need.abstract }}
{% endif %}
}
"""

BLOCK_INST_TEMPLATE = """\
class "{{ need.id }}\\n{{ need.title }}" <<Part>> [[{{ ref(need.id) }|{{ need.title }}]] {
{% if need.definition %}
    == definition ==
    {{ need.definition }}
{% endif %}
{% if need.multiplicity %}
    == multiplicity ==
    {{ need.multiplicity }}
{% endif %}
}
"""

REQ_BOX_TEMPLATE = """\
class "{{ need.id }}\\n{{ need.title }}" <<requirement>> [[{{ ref(need.id) }|{{ need.title }}]] {
    == id ==
    {{ need.id }}
{% if need.req_text %}
    == text ==
    {{ need.req_text }}
{% endif %}
}
"""

BDD_FULL_TEMPLATE = """\
@startuml
{% set root = needs.get(root_id) %}
{% if root %}
{{ uml(root_id) }}
{% for child in filter("type == 'Part' and owned_by == '" + root_id + "'") %}
{{ uml(child.id) }}
{{ root_id }} *-- {{ child.id }}
{% endfor %}
{% endif %}
@enduml
"""

IBD_FULL_TEMPLATE = """\
@startuml
{% set root = needs.get(root_id) %}
{% if root %}
rectangle "{{ root.title }}" <<ibd>> {
{% for child in filter("type == 'Part' and owned_by == '" + root_id + "'") %}
    component "{{ child.id }}\\n{{ child.title }}" <<Part>> as {{ child.id }} {
{% for port in filter("type == 'Port' and owned_by == '" + child.id + "'") %}
        portin {{ port.id }}
{% endfor %}
    }
{% endfor %}
}
{% endif %}
@enduml
"""

REQ_FULL_TEMPLATE = """\
@startuml
{% for need in filter(filter_expr) %}
{{ uml(need.id) }}
{% if show_satisfy and need.satisfies %}
{% for target in need.satisfies.split(",") %}
{{ need.id }} ..> {{ target | trim }} : <<satisfy>>
{% endfor %}
{% endif %}
{% if show_refine and need.refines %}
{% for target in need.refines.split(",") %}
{{ need.id }} ..> {{ target | trim }} : <<refines>>
{% endfor %}
{% endif %}
{% if show_allocate and need.allocates %}
{% for target in need.allocates.split(",") %}
{{ need.id }} ..> {{ target | trim }} : <<allocates>>
{% endfor %}
{% endif %}
{% endfor %}
@enduml
"""
