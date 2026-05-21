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
{% if need.content %}
    == text ==
    {{ need.content }}
{% endif %}
}
"""

BDD_FULL_TEMPLATE = """\
@startuml
{% set root = needs.get(root_id) %}
{% if root %}
{{ uml(root_id) }}
{% for child in filter("type == 'part' and owned_by == '" + root_id + "'") %}
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
{% for child in filter("type == 'part' and owned_by == '" + root_id + "'") %}
    component "{{ child.id }}\\n{{ child.title }}" <<Part>> as {{ child.id }} {
{% for port in filter("type == 'port' and owned_by == '" + child.id + "'") %}
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


# === New in feature 002-full-sysml-diagrams ===

# Package — nested packages with dependency arrows. Renders the root
# package plus up to two levels of children (depth=3 covers the typical
# system → subsystem → component organization). minijinja (the engine
# behind needuml templates) does not support list.append(), so the
# template is unrolled rather than recursive.
PKG_FULL_TEMPLATE = """\
@startuml
{% set root_id = "{root_id}" %}
{% set root = needs.get(root_id) %}
{% if root %}
{% set level1 = filter("type == 'package' and parent_package == '" + root_id + "'") | list %}
package "{{ root.title }}" as {{ root.id }} [[{{ ref(root.id) }}]] {
{% for c1 in level1 %}
{% set level2 = filter("type == 'package' and parent_package == '" + c1.id + "'") | list %}
{% if (level2 | length) > 0 %}
package "{{ c1.title }}" as {{ c1.id }} [[{{ ref(c1.id) }}]] {
{% for c2 in level2 %}
package "{{ c2.title }}" as {{ c2.id }} [[{{ ref(c2.id) }}]]
{% endfor %}
}
{% else %}
package "{{ c1.title }}" as {{ c1.id }} [[{{ ref(c1.id) }}]]
{% endif %}
{% endfor %}
}
{% set deps = filter("type == 'dependency'") | list %}
{% for d in deps %}
{% if needs.get(d.source) and needs.get(d.target) %}
{{ d.source }} ..> {{ d.target }} : <<{{ d.kind or 'use' }}>>
{% endif %}
{% endfor %}
{% endif %}
@enduml
"""


# Use case — actors outside system boundaries, use cases inside. Walks
# UseCase needs matching `filter_expr` (default `type == 'usecase'`).
# Groups by `subject` for boundaries. Actors with `interacts_with` get
# solid association lines per listed UseCase. extends/includes/
# generalizes between UseCases render as dashed labelled arrows.
UC_FULL_TEMPLATE = """\
@startuml
{% set filter_expr = "{filter_expr}" %}
{% set subject_filter = "{subject_filter}" %}
{% set use_cases = filter(filter_expr) | list %}
{% if subject_filter %}
{% set use_cases = use_cases | selectattr('subject', 'equalto', subject_filter) | list %}
{% endif %}
{% set uc_ids = use_cases | map(attribute='id') | list %}
{% set actors = filter("type == 'actor'") | list %}
{% set non_default_subjects = use_cases | map(attribute='subject') | reject('equalto', None) | reject('equalto', '') | unique | list %}
{% set has_default_subject = (use_cases | rejectattr('subject') | list | length) > 0 or (use_cases | selectattr('subject', 'equalto', '') | list | length) > 0 %}
{% set subjects = non_default_subjects + (['_default'] if has_default_subject else []) %}
{% for a in actors %}
actor "{{ a.title }}" as {{ a.id }} [[{{ ref(a.id) }}]]
{% endfor %}
{% for s in subjects %}
{% if s == '_default' %}
{% for uc in use_cases if (uc.subject or '_default') == '_default' %}
usecase "{{ uc.title }}" as {{ uc.id }} [[{{ ref(uc.id) }}]]
{% endfor %}
{% else %}
rectangle "{{ s }}" {
{% for uc in use_cases if uc.subject == s %}
    usecase "{{ uc.title }}" as {{ uc.id }} [[{{ ref(uc.id) }}]]
{% endfor %}
}
{% endif %}
{% endfor %}
{% for a in actors %}
{% if a.interacts_with %}
{% for uc_id in a.interacts_with.split(",") %}
{% set uc_id_stripped = uc_id | trim %}
{% if uc_id_stripped in uc_ids %}
{{ a.id }} --> {{ uc_id_stripped }}
{% endif %}
{% endfor %}
{% endif %}
{% endfor %}
{% for uc in use_cases %}
{% if uc.extends %}
{% for target in uc.extends.split(",") %}
{{ uc.id }} ..> {{ target | trim }} : <<extend>>
{% endfor %}
{% endif %}
{% if uc.includes %}
{% for target in uc.includes.split(",") %}
{{ uc.id }} ..> {{ target | trim }} : <<include>>
{% endfor %}
{% endif %}
{% if uc.generalizes %}
{% for target in uc.generalizes.split(",") %}
{{ uc.id }} <|-- {{ target | trim }}
{% endfor %}
{% endif %}
{% endfor %}
@enduml
"""


# Sequence — walks Lifelines whose `definition` equals the root, emits
# PlantUML sequence diagram. Messages render with arrowhead per
# `message_kind` (sync → ->, async → ->>, return → -->). Messages sharing
# a `fragment_group` wrap in a single combined-fragment frame whose kind
# comes from the first message's `fragment_kind`.
SD_FULL_TEMPLATE = """\
@startuml
{% set root_id = "{root_id}" %}
{% set lifelines = filter("type == 'lifeline' and definition == '" + root_id + "'") | list %}
{% set messages = filter("type == 'message'") | list %}
{% set lifeline_ids = lifelines | map(attribute='id') | list %}
{% set state = namespace(group=None) %}
{% for ll in lifelines %}
participant "{{ ll.title }}" as {{ ll.id }} [[{{ ref(ll.id) }}]]
{% endfor %}
{% for m in messages %}
{% if m.from_lifeline in lifeline_ids and m.to_lifeline in lifeline_ids %}
{% if (m.fragment_group or '') != (state.group or '') %}
{% if state.group %}end
{% endif %}
{% if m.fragment_group %}{{ m.fragment_kind or 'opt' }}{% if m.fragment_guard %} {{ m.fragment_guard }}{% endif %}
{% endif %}
{% set state.group = m.fragment_group %}
{% endif %}
{% set arrow = '->' if (m.message_kind or 'sync') == 'sync' else ('->>' if m.message_kind == 'async' else '-->') %}
{{ m.from_lifeline }} {{ arrow }} {{ m.to_lifeline }} : {{ m.title }}
{% endif %}
{% endfor %}
{% if state.group %}end{% endif %}
@enduml
"""


# Activity — class-diagram approximation. PlantUML's activity-beta syntax
# is order-driven and node IDs aren't reusable, so we render actions as
# stereotyped classes inside swimlane packages, with explicit control-flow
# arrows. Fork/join nodes are shown with their UML <<fork>> / <<join>>
# stereotypes; decision/merge as <<decision>> / <<merge>>.
ACT_FULL_TEMPLATE = """\
@startuml
{% set root_id = "{root_id}" %}
{% set show_partitions = ({show_partitions} == 'true') %}
{% set actions = filter("type == 'action' and definition == '" + root_id + "'") | list %}
{% set ctrl_flows = filter("type == 'controlflow'") | list %}
{% set obj_flows = filter("type == 'objectflow'") | list %}
{% set action_ids = actions | map(attribute='id') | list %}
{% if show_partitions %}
{% set partition_names = actions | map(attribute='partition') | reject('equalto', None) | reject('equalto', '') | unique | list %}
{% set has_default = (actions | rejectattr('partition') | list | length) > 0 or (actions | selectattr('partition', 'equalto', '') | list | length) > 0 %}
{% set partition_names = partition_names + (['_default'] if has_default else []) %}
{% for part in partition_names %}
{% if part == '_default' %}
{% for a in actions if (a.partition or '_default') == '_default' %}
class "{{ a.id }}\\n{{ a.title }}" <<{{ a.activity_kind or 'action' }}>> [[{{ ref(a.id) }}]]

{% endfor %}
{% else %}
package "{{ part }}" <<swimlane>> {
{% for a in actions if a.partition == part %}
class "{{ a.id }}\\n{{ a.title }}" <<{{ a.activity_kind or 'action' }}>> [[{{ ref(a.id) }}]]
{% endfor %}
}
{% endif %}
{% endfor %}
{% else %}
{% for a in actions %}
class "{{ a.id }}\\n{{ a.title }}" <<{{ a.activity_kind or 'action' }}>> [[{{ ref(a.id) }}]]

{% endfor %}
{% endif %}
{% for f in ctrl_flows %}
{% if f.from_action in action_ids and f.to_action in action_ids %}
"{{ f.from_action }}\\n{{ needs.get(f.from_action).title }}" --> "{{ f.to_action }}\\n{{ needs.get(f.to_action).title }}"
{% endif %}
{% endfor %}
{% for f in obj_flows %}
{% if f.from_action in action_ids and f.to_action in action_ids %}
"{{ f.from_action }}\\n{{ needs.get(f.from_action).title }}" --> "{{ f.to_action }}\\n{{ needs.get(f.to_action).title }}" : {{ f.object_type or 'object' }}
{% endif %}
{% endfor %}
@enduml
"""


# State Machine — walks all StateUsage instances of the root StateDef plus
# their Transitions, emits PlantUML state-diagram syntax. Pseudostates are
# rendered with their UML notation (initial/final via [*], history via
# <<history>>, choice via <<choice>>, junction via <<junction>>).
STM_FULL_TEMPLATE = """\
@startuml
{% set root_id = "{root_id}" %}
{% set states = filter("type == 'stateusage' and definition == '" + root_id + "'") | list %}
{% set transitions = filter("type == 'transition'") | list %}
{% set state_ids = states | map(attribute='id') | list %}
{% for s in states %}
{% if s.pseudo_kind == 'choice' %}
state {{ s.id }} <<choice>>
{% elif s.pseudo_kind == 'junction' %}
state {{ s.id }} <<junction>>
{% elif s.pseudo_kind == 'shallowHistory' %}
state {{ s.id }} <<history>>
{% elif s.pseudo_kind == 'deepHistory' %}
state {{ s.id }} <<history*>>
{% elif s.pseudo_kind not in ('initial', 'final') %}
state "{{ s.title }}" as {{ s.id }} [[{{ ref(s.id) }}]]
{% endif %}
{% endfor %}
{% for t in transitions %}
{% if t.from_state in state_ids and t.to_state in state_ids %}
{% set src = needs.get(t.from_state) %}
{% set dst = needs.get(t.to_state) %}
{% set src_render = '[*]' if (src and src.pseudo_kind == 'initial') else t.from_state %}
{% set dst_render = '[*]' if (dst and dst.pseudo_kind == 'final') else t.to_state %}
{% set label = t.trigger or '' %}
{% if t.guard %}{% set label = label + ' [' + t.guard + ']' %}{% endif %}
{% if t.effect %}{% set label = label + ' / ' + t.effect %}{% endif %}
{{ src_render }} --> {{ dst_render }}{% if label %} : {{ label }}{% endif %}

{% endif %}
{% endfor %}
@enduml
"""
