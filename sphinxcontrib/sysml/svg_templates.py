"""SVG Jinja templates for the `needsysml-*-svg` directives.

Each constant is a Jinja2 template string rendered by sphinx-need-svg's
``SvgJinjaContext`` (which exposes ``needs``, ``filter``, ``flow``, and
``ref`` to the template). Directives substitute placeholder tokens like
``__ROOT_ID__`` or ``__FILTER_EXPR__`` into the template before handing
it off to the ``Needsvg`` placeholder pipeline for deferred rendering at
``doctree-resolved``.
"""

__all__ = [
    "ACT_SVG_TEMPLATE",
    "BDD_SVG_TEMPLATE",
    "IBD_SVG_TEMPLATE",
    "PKG_SVG_TEMPLATE",
    "SD_SVG_TEMPLATE",
    "STM_SVG_TEMPLATE",
    "UC_SVG_TEMPLATE",
]


BDD_SVG_TEMPLATE = """\
{% set root_id = "__ROOT_ID__" %}
{% set children = filter("__FILTER_EXPR__") | list %}
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 260" width="100%">
  {% set root = needs.get(root_id) %}
  {% if root %}
  <g transform="translate(300, 20)">
    <a href="#{{ root_id }}">
      <rect width="120" height="40" rx="4" fill="#ddeeff" stroke="#336699"/>
      <text x="60" y="16" text-anchor="middle" font-size="10" fill="#666">{{ root_id }}</text>
      <text x="60" y="30" text-anchor="middle" font-size="11">{{ root.title }}</text>
    </a>
  </g>
  {% set count = children | length %}
  {% if count > 0 %}
  {% set step = (720 // (count + 1)) %}
  {% for child in children %}
  {% set cx = step * loop.index %}
  <line x1="360" y1="60" x2="{{ cx }}" y2="180"
        stroke="#336699" stroke-width="1.5"/>
  <polygon points="358,55 366,55 362,65" fill="#336699"/>
  <g transform="translate({{ cx - 60 }}, 180)">
    <a href="#{{ child.id }}">
      <rect width="120" height="40" rx="4" fill="#ddeeff" stroke="#336699"/>
      <text x="60" y="16" text-anchor="middle" font-size="10" fill="#666">{{ child.id }}</text>
      <text x="60" y="30" text-anchor="middle" font-size="11">{{ child.title }}</text>
    </a>
  </g>
  {% endfor %}
  {% else %}
  <text x="360" y="150" text-anchor="middle"
        font-family="sans-serif" font-size="12" fill="#999">
    No matching elements
  </text>
  {% endif %}
  {% else %}
  <text x="360" y="130" text-anchor="middle"
        font-family="sans-serif" font-size="12" fill="red">
    Unknown root need: {{ root_id }}
  </text>
  {% endif %}
</svg>
"""


ACT_SVG_TEMPLATE = """\
{% set root_id = "__ROOT_ID__" %}
{% set actions = filter("type == 'action' and definition == '" + root_id + "'") | list %}
{% set ctrl_flows = filter("type == 'controlflow'") | list %}
{% set action_ids = actions | map(attribute='id') | list %}
{% set partition_names = [] %}
{% for a in actions %}
{% set part = a.partition or '_default' %}
{% if part not in partition_names %}{% set _ = partition_names.append(part) %}{% endif %}
{% endfor %}
{% set lane_w = 200 %}
{% set lane_h = 80 %}
<svg xmlns="http://www.w3.org/2000/svg"
     viewBox="0 0 {{ partition_names | length * lane_w + 40 }} {{ actions | length * lane_h + 80 }}"
     width="100%">
  {% set count = actions | length %}
  {% if count > 0 %}
  {% for part in partition_names %}
  {% set lx = 20 + loop.index0 * lane_w %}
  <rect x="{{ lx }}" y="20" width="{{ lane_w - 10 }}"
        height="{{ count * lane_h + 50 }}"
        fill="#FAF6EE" stroke="#CC9966" stroke-width="1"/>
  <text x="{{ lx + (lane_w - 10) // 2 }}" y="40"
        text-anchor="middle" font-family="sans-serif" font-size="12"
        font-weight="bold" fill="#CC9966">{{ part if part != '_default' else '(no swimlane)' }}</text>
  {% endfor %}
  {% set action_pos = {} %}
  {% for a in actions %}
  {% set part = a.partition or '_default' %}
  {% set col = partition_names.index(part) %}
  {% set cx = 20 + col * lane_w + (lane_w - 10) // 2 %}
  {% set cy = 70 + loop.index0 * lane_h %}
  {% set _ = action_pos.update({a.id: [cx, cy]}) %}
  {% if a.activity_kind == 'fork' or a.activity_kind == 'join' %}
  <rect x="{{ cx - 40 }}" y="{{ cy + 18 }}" width="80" height="6" fill="#222"/>
  <text x="{{ cx }}" y="{{ cy + 14 }}" text-anchor="middle"
        font-family="monospace" font-size="9" fill="#666">{{ a.id }} ({{ a.activity_kind }})</text>
  {% elif a.activity_kind == 'decision' or a.activity_kind == 'merge' %}
  <polygon points="{{ cx }},{{ cy + 8 }} {{ cx + 26 }},{{ cy + 22 }} {{ cx }},{{ cy + 36 }} {{ cx - 26 }},{{ cy + 22 }}"
           fill="#FFE0AA" stroke="#CC8800"/>
  <text x="{{ cx }}" y="{{ cy + 26 }}" text-anchor="middle"
        font-family="monospace" font-size="9" fill="#666">{{ a.id }}</text>
  {% else %}
  <a href="#{{ a.id }}">
    <rect x="{{ cx - 70 }}" y="{{ cy }}" width="140" height="44"
          rx="20" fill="#FFEEDD" stroke="#CC9966"/>
    <text x="{{ cx }}" y="{{ cy + 18 }}" text-anchor="middle"
          font-family="monospace" font-size="9" fill="#666">{{ a.id }}</text>
    <text x="{{ cx }}" y="{{ cy + 32 }}" text-anchor="middle"
          font-family="sans-serif" font-size="11">{{ a.title }}</text>
  </a>
  {% endif %}
  {% endfor %}
  {% for f in ctrl_flows %}
  {% if f.from_action in action_ids and f.to_action in action_ids %}
  {% set src = action_pos[f.from_action] %}
  {% set dst = action_pos[f.to_action] %}
  <line x1="{{ src[0] }}" y1="{{ src[1] + 44 }}" x2="{{ dst[0] }}" y2="{{ dst[1] }}"
        stroke="#666" stroke-width="1.5"/>
  {% endif %}
  {% endfor %}
  {% else %}
  <text x="360" y="120" text-anchor="middle"
        font-family="sans-serif" font-size="12" fill="#999">
    No matching elements
  </text>
  {% endif %}
</svg>
"""


UC_SVG_TEMPLATE = """\
{% set use_cases = filter("__FILTER_EXPR__") | list %}
{% set actors = filter("type == 'actor'") | list %}
{% set uc_ids = use_cases | map(attribute='id') | list %}
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 {{ (actors | length + use_cases | length) * 40 + 80 }}" width="100%">
  {% if (use_cases | length) > 0 or (actors | length) > 0 %}
  {% set actor_pos = {} %}
  {% for a in actors %}
  {% set ay = 60 + loop.index0 * 80 %}
  {% set _ = actor_pos.update({a.id: [80, ay + 20]}) %}
  <a href="#{{ a.id }}">
    <circle cx="80" cy="{{ ay }}" r="10" fill="#EEEECC" stroke="#886600"/>
    <line x1="80" y1="{{ ay + 10 }}" x2="80" y2="{{ ay + 25 }}" stroke="#886600"/>
    <line x1="65" y1="{{ ay + 15 }}" x2="95" y2="{{ ay + 15 }}" stroke="#886600"/>
    <line x1="80" y1="{{ ay + 25 }}" x2="68" y2="{{ ay + 40 }}" stroke="#886600"/>
    <line x1="80" y1="{{ ay + 25 }}" x2="92" y2="{{ ay + 40 }}" stroke="#886600"/>
    <text x="80" y="{{ ay + 55 }}" text-anchor="middle"
          font-family="sans-serif" font-size="11">{{ a.title }}</text>
  </a>
  {% endfor %}
  {% set uc_pos = {} %}
  <rect x="200" y="40" width="520" height="{{ (use_cases | length) * 70 + 20 }}"
        fill="none" stroke="#336699" stroke-width="1.5"/>
  {% set subjects = use_cases | map(attribute='subject') | reject('equalto', None) | unique | list %}
  <text x="220" y="60" font-family="sans-serif" font-size="12" font-weight="bold"
        fill="#336699">{{ subjects[0] if subjects else 'System' }}</text>
  {% for uc in use_cases %}
  {% set uy = 90 + loop.index0 * 70 %}
  {% set _ = uc_pos.update({uc.id: [460, uy]}) %}
  <a href="#{{ uc.id }}">
    <ellipse cx="460" cy="{{ uy }}" rx="120" ry="24"
             fill="#FFEEDD" stroke="#CC8800"/>
    <text x="460" y="{{ uy + 4 }}" text-anchor="middle"
          font-family="sans-serif" font-size="11">{{ uc.title }}</text>
  </a>
  {% endfor %}
  {% for a in actors if a.interacts_with %}
  {% for uc_id in a.interacts_with.split(",") %}
  {% set uc_id_stripped = uc_id | trim %}
  {% if uc_id_stripped in uc_pos %}
  {% set ap = actor_pos[a.id] %}
  {% set up = uc_pos[uc_id_stripped] %}
  <line x1="{{ ap[0] + 20 }}" y1="{{ ap[1] }}" x2="{{ up[0] - 120 }}" y2="{{ up[1] }}"
        stroke="#666" stroke-width="1.5"/>
  {% endif %}
  {% endfor %}
  {% endfor %}
  {% for uc in use_cases %}
  {% if uc.extends %}
  {% for target in uc.extends.split(",") %}
  {% set target_id = target | trim %}
  {% if target_id in uc_pos %}
  {% set src = uc_pos[uc.id] %}
  {% set dst = uc_pos[target_id] %}
  <line x1="{{ src[0] }}" y1="{{ src[1] - 24 }}" x2="{{ dst[0] }}" y2="{{ dst[1] + 24 }}"
        stroke="#444" stroke-dasharray="4 3" stroke-width="1"/>
  <text x="{{ (src[0] + dst[0]) // 2 + 20 }}" y="{{ (src[1] + dst[1]) // 2 }}"
        font-family="sans-serif" font-size="9" fill="#444"
        font-style="italic">&lt;&lt;extend&gt;&gt;</text>
  {% endif %}
  {% endfor %}
  {% endif %}
  {% if uc.includes %}
  {% for target in uc.includes.split(",") %}
  {% set target_id = target | trim %}
  {% if target_id in uc_pos %}
  {% set src = uc_pos[uc.id] %}
  {% set dst = uc_pos[target_id] %}
  <line x1="{{ src[0] }}" y1="{{ src[1] - 24 }}" x2="{{ dst[0] }}" y2="{{ dst[1] + 24 }}"
        stroke="#444" stroke-dasharray="4 3" stroke-width="1"/>
  <text x="{{ (src[0] + dst[0]) // 2 + 20 }}" y="{{ (src[1] + dst[1]) // 2 }}"
        font-family="sans-serif" font-size="9" fill="#444"
        font-style="italic">&lt;&lt;include&gt;&gt;</text>
  {% endif %}
  {% endfor %}
  {% endif %}
  {% endfor %}
  {% else %}
  <text x="360" y="120" text-anchor="middle"
        font-family="sans-serif" font-size="12" fill="#999">
    No matching elements
  </text>
  {% endif %}
</svg>
"""


PKG_SVG_TEMPLATE = """\
{% set root_id = "__ROOT_ID__" %}
{% set all_packages = filter("type == 'package'") | list %}
{% set deps = filter("type == 'dependency'") | list %}
{% set root = needs.get(root_id) %}
{% set children = all_packages | selectattr('parent_package', 'equalto', root_id) | list %}
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 380" width="100%">
  {% if root %}
  <a href="#{{ root.id }}">
    <rect x="20" y="20" width="720" height="340"
          fill="#EEEEFF" stroke="#336699" stroke-width="2"/>
    <text x="36" y="42" font-family="sans-serif" font-size="13"
          font-weight="bold" fill="#336699">{{ root.title }} ({{ root.id }})</text>
  </a>
  {% set count = children | length %}
  {% set child_pos = {} %}
  {% if count > 0 %}
  {% set cw = (720 - 60) // count %}
  {% for c in children %}
  {% set cx = 40 + loop.index0 * cw %}
  {% set _ = child_pos.update({c.id: [cx + cw // 2, 200]}) %}
  <a href="#{{ c.id }}">
    <rect x="{{ cx }}" y="80" width="{{ cw - 20 }}" height="220"
          fill="#FFFFFF" stroke="#336699"/>
    <text x="{{ cx + 12 }}" y="100" font-family="sans-serif" font-size="11"
          font-weight="bold" fill="#336699">{{ c.title }}</text>
    <text x="{{ cx + 12 }}" y="118" font-family="monospace" font-size="9"
          fill="#666">{{ c.id }}</text>
  </a>
  {% endfor %}
  {% else %}
  <text x="380" y="200" text-anchor="middle"
        font-family="sans-serif" font-size="12" fill="#999">
    No nested packages
  </text>
  {% endif %}
  {% for d in deps %}
  {% if d.source_ref in child_pos and d.target_ref in child_pos %}
  {% set src = child_pos[d.source_ref] %}
  {% set dst = child_pos[d.target_ref] %}
  <line x1="{{ src[0] }}" y1="{{ src[1] }}" x2="{{ dst[0] }}" y2="{{ dst[1] - 20 - loop.index0 * 16 }}"
        stroke="#444" stroke-dasharray="4 3" stroke-width="1.2"/>
  <text x="{{ (src[0] + dst[0]) // 2 }}" y="{{ src[1] - 14 - loop.index0 * 16 }}" text-anchor="middle"
        font-family="sans-serif" font-size="10" fill="#444"
        font-style="italic">&lt;&lt;{{ d.kind or 'use' }}&gt;&gt;</text>
  {% endif %}
  {% endfor %}
  {% else %}
  <text x="360" y="180" text-anchor="middle"
        font-family="sans-serif" font-size="12" fill="red">
    Unknown root package: {{ root_id }}
  </text>
  {% endif %}
</svg>
"""


SD_SVG_TEMPLATE = """\
{% set root_id = "__ROOT_ID__" %}
{% set lifelines = filter("type == 'lifeline' and definition == '" + root_id + "'") | list %}
{% set messages = filter("type == 'message'") | list %}
{% set lifeline_ids = lifelines | map(attribute='id') | list %}
{% set msg_count = messages | length %}
{% set col_w = 180 %}
{% set row_h = 50 %}
{% set width = (lifelines | length) * col_w + 80 %}
{% set height = msg_count * row_h + 140 %}
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {{ width }} {{ height }}" width="100%">
  {% if lifelines | length > 0 %}
  {% for ll in lifelines %}
  {% set lx = 60 + loop.index0 * col_w %}
  <a href="#{{ ll.id }}">
    <rect x="{{ lx - 60 }}" y="20" width="120" height="40"
          rx="4" fill="#E0E8F0" stroke="#336699"/>
    <text x="{{ lx }}" y="36" text-anchor="middle"
          font-family="monospace" font-size="9" fill="#666">{{ ll.id }}</text>
    <text x="{{ lx }}" y="50" text-anchor="middle"
          font-family="sans-serif" font-size="11">{{ ll.title }}</text>
  </a>
  <line x1="{{ lx }}" y1="60" x2="{{ lx }}" y2="{{ height - 20 }}"
        stroke="#888888" stroke-dasharray="3 4"/>
  {% endfor %}
  {% set msg_y = namespace(val=90) %}
  {% set last_group = namespace(val=None) %}
  {% set fragment_y = namespace(val=None) %}
  {% for m in messages %}
  {% if m.from_lifeline in lifeline_ids and m.to_lifeline in lifeline_ids %}
  {% set src_index = lifeline_ids.index(m.from_lifeline) %}
  {% set dst_index = lifeline_ids.index(m.to_lifeline) %}
  {% set sx = 60 + src_index * col_w %}
  {% set dx = 60 + dst_index * col_w %}
  {% if (m.fragment_group or '') != (last_group.val or '') %}
  {% if last_group.val %}
  <rect x="20" y="{{ fragment_y.val }}" width="{{ width - 40 }}" height="{{ msg_y.val - fragment_y.val - 8 }}"
        fill="none" stroke="#336699" stroke-width="1"/>
  {% endif %}
  {% if m.fragment_group %}
  {% set fragment_y.val = msg_y.val - 8 %}
  <text x="32" y="{{ msg_y.val - 12 }}" font-family="sans-serif"
        font-size="10" font-weight="bold" fill="#336699">{{ m.fragment_kind or 'opt' }}{% if m.fragment_guard %} [{{ m.fragment_guard }}]{% endif %}</text>
  {% set msg_y.val = msg_y.val + 12 %}
  {% endif %}
  {% set last_group.val = m.fragment_group %}
  {% endif %}
  {% set dash = '5 4' if m.message_kind == 'return' else 'none' %}
  {% set marker_id = 'open' if m.message_kind == 'async' else 'filled' %}
  <line x1="{{ sx }}" y1="{{ msg_y.val }}" x2="{{ dx }}" y2="{{ msg_y.val }}"
        stroke="#444" stroke-width="1.5"
        stroke-dasharray="{{ dash }}"/>
  <polygon points="{{ dx }},{{ msg_y.val }} {{ dx - 8 if dx > sx else dx + 8 }},{{ msg_y.val - 4 }} {{ dx - 8 if dx > sx else dx + 8 }},{{ msg_y.val + 4 }}"
           fill="{{ '#444' if marker_id == 'filled' else 'none' }}" stroke="#444"/>
  <text x="{{ (sx + dx) // 2 }}" y="{{ msg_y.val - 4 }}" text-anchor="middle"
        font-family="sans-serif" font-size="10" fill="#222">
    <a href="#{{ m.id }}">{{ m.title }}</a>
  </text>
  {% set msg_y.val = msg_y.val + row_h %}
  {% endif %}
  {% endfor %}
  {% if last_group.val %}
  <rect x="20" y="{{ fragment_y.val }}" width="{{ width - 40 }}" height="{{ msg_y.val - fragment_y.val - 8 }}"
        fill="none" stroke="#336699" stroke-width="1"/>
  {% endif %}
  {% else %}
  <text x="360" y="120" text-anchor="middle"
        font-family="sans-serif" font-size="12" fill="#999">
    No matching elements
  </text>
  {% endif %}
</svg>
"""


STM_SVG_TEMPLATE = """\
{% set root_id = "__ROOT_ID__" %}
{% set states = filter("type == 'stateusage' and definition == '" + root_id + "'") | list %}
{% set transitions = filter("type == 'transition'") | list %}
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 320" width="100%">
  {% set count = states | length %}
  {% if count > 0 %}
  {% set step = (720 // (count + 1)) %}
  {% set rendered = {} %}
  {% for s in states %}
  {% set cx = step * loop.index %}
  {% set cy = 90 if loop.index0 % 2 == 0 else 230 %}
  {% if s.pseudo_kind == 'initial' %}
  <circle cx="{{ cx }}" cy="{{ cy + 20 }}" r="9" fill="#222" stroke="#222"/>
  <text x="{{ cx }}" y="{{ cy + 50 }}" text-anchor="middle"
        font-family="monospace" font-size="9" fill="#666">{{ s.id }}</text>
  {% elif s.pseudo_kind == 'final' %}
  <circle cx="{{ cx }}" cy="{{ cy + 20 }}" r="11" fill="white" stroke="#222"/>
  <circle cx="{{ cx }}" cy="{{ cy + 20 }}" r="6" fill="#222"/>
  <text x="{{ cx }}" y="{{ cy + 50 }}" text-anchor="middle"
        font-family="monospace" font-size="9" fill="#666">{{ s.id }}</text>
  {% elif s.pseudo_kind in ('shallowHistory', 'deepHistory') %}
  <circle cx="{{ cx }}" cy="{{ cy + 20 }}" r="13"
          fill="#EEEEDD" stroke="#888866"/>
  <text x="{{ cx }}" y="{{ cy + 24 }}" text-anchor="middle"
        font-family="serif" font-style="italic" font-size="13">{{
        'H*' if s.pseudo_kind == 'deepHistory' else 'H' }}</text>
  {% elif s.pseudo_kind == 'choice' %}
  <polygon points="{{ cx }},{{ cy + 5 }} {{ cx + 18 }},{{ cy + 20 }} {{ cx }},{{ cy + 35 }} {{ cx - 18 }},{{ cy + 20 }}"
           fill="#FFEEBB" stroke="#CC9900"/>
  {% elif s.pseudo_kind == 'junction' %}
  <circle cx="{{ cx }}" cy="{{ cy + 20 }}" r="6" fill="#888888" stroke="#444"/>
  {% else %}
  <a href="#{{ s.id }}">
    <rect x="{{ cx - 55 }}" y="{{ cy }}" width="110" height="40"
          rx="8" fill="#EEEEDD" stroke="#888866"/>
    <text x="{{ cx }}" y="{{ cy + 16 }}" text-anchor="middle"
          font-family="monospace" font-size="9" fill="#666">{{ s.id }}</text>
    <text x="{{ cx }}" y="{{ cy + 30 }}" text-anchor="middle"
          font-family="sans-serif" font-size="11">{{ s.title }}</text>
  </a>
  {% endif %}
  {% endfor %}
  {% for t in transitions %}
  {% set src = needs.get(t.from_state) %}
  {% set dst = needs.get(t.to_state) %}
  {% if src and dst and src.definition == root_id and dst.definition == root_id %}
  {% set label = (t.trigger or '') %}
  {% if t.guard %}{% set label = label + ' [' + t.guard + ']' %}{% endif %}
  {% if t.effect %}{% set label = label + ' / ' + t.effect %}{% endif %}
  {% set src_index = (states | map(attribute='id') | list).index(t.from_state) + 1 %}
  {% set dst_index = (states | map(attribute='id') | list).index(t.to_state) + 1 %}
  {% set sx = step * src_index %}
  {% set dx = step * dst_index %}
  {% set sy = (90 if (src_index - 1) % 2 == 0 else 230) + 40 %}
  {% set dy = 90 if (dst_index - 1) % 2 == 0 else 230 %}
  <line x1="{{ sx }}" y1="{{ sy }}" x2="{{ dx }}" y2="{{ dy }}"
        stroke="#666" stroke-width="1.5"/>
  <text x="{{ (sx + dx) // 2 }}" y="{{ (sy + dy) // 2 - 4 }}"
        text-anchor="middle" font-family="sans-serif" font-size="10"
        fill="#444">{{ label }}</text>
  {% endif %}
  {% endfor %}
  {% else %}
  <text x="360" y="160" text-anchor="middle"
        font-family="sans-serif" font-size="12" fill="#999">
    No matching elements
  </text>
  {% endif %}
</svg>
"""


IBD_SVG_TEMPLATE = """\
{% set root_id = "__ROOT_ID__" %}
{% set parts = filter("type == 'part' and owned_by == '" + root_id + "'") | list %}
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 260" width="100%">
  {% set root = needs.get(root_id) %}
  {% if root %}
  <rect x="20" y="10" width="680" height="240"
        fill="none" stroke="#336699" stroke-dasharray="4 3"/>
  <text x="32" y="32" font-family="sans-serif" font-size="13"
        fill="#336699">{{ root.title }} ({{ root_id }}) — IBD</text>
  {% set count = parts | length %}
  {% if count > 0 %}
  {% for part in parts %}
  {% set px = 60 + ((680 - 120) // (count + 1)) * loop.index - 60 %}
  <g transform="translate({{ px }}, 90)">
    <a href="#{{ part.id }}">
      <rect width="120" height="40" rx="4" fill="#ddeeff" stroke="#336699"/>
      <text x="60" y="16" text-anchor="middle" font-size="10" fill="#666">{{ part.id }}</text>
      <text x="60" y="30" text-anchor="middle" font-size="11">{{ part.title }}</text>
    </a>
  </g>
  {% set ports = filter("type == 'port' and owned_by == '" + part.id + "'") | list %}
  {% for port in ports %}
  <circle cx="{{ px + (loop.index0 * 28) + 10 }}" cy="150"
          r="6" fill="#FFE0AA" stroke="#cc8800"/>
  <text x="{{ px + (loop.index0 * 28) + 10 }}" y="175"
        text-anchor="middle" font-family="monospace"
        font-size="9" fill="#666">{{ port.id }}</text>
  {% endfor %}
  {% endfor %}
  {% else %}
  <text x="360" y="135" text-anchor="middle"
        font-family="sans-serif" font-size="12" fill="#999">
    No matching elements
  </text>
  {% endif %}
  {% else %}
  <text x="360" y="135" text-anchor="middle"
        font-family="sans-serif" font-size="12" fill="red">
    Unknown root need: {{ root_id }}
  </text>
  {% endif %}
</svg>
"""
