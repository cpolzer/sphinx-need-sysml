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
    "PAR_SVG_TEMPLATE",
    "PKG_SVG_TEMPLATE",
    "SD_SVG_TEMPLATE",
    "STM_SVG_TEMPLATE",
    "UC_SVG_TEMPLATE",
]


BDD_SVG_TEMPLATE = """\
{% set root_id = "__ROOT_ID__" %}
{% set root = needs.get(root_id) %}
{% set l1 = filter("__FILTER_EXPR__") | list %}
{# Bottom-up tree layout: leaves get columns, parents center above kids. #}
{% set ns = namespace(l2_map={}, l2_total=0) %}
{% for c1 in l1 %}
{% set kids = filter("type == 'partdef' and owned_by == '" + c1.id + "'") | list %}
{% set _ = ns.l2_map.update({c1.id: kids}) %}
{% set ns.l2_total = ns.l2_total + (kids | length) %}
{% endfor %}
{% set cols = ns.l2_total if ns.l2_total > (l1 | length) else (l1 | length) %}
{% if cols < 1 %}{% set cols = 1 %}{% endif %}
{% set col_w = 150 %}
{% set width = (cols * col_w) + 40 %}
{% set y_root = 20 %}
{% set y_l1 = 130 %}
{% set y_l2 = 240 %}
{% set height = (y_l2 + 60) if ns.l2_total > 0 else (y_l1 + 60) %}
{% set positions = {} %}
{% set col_idx = namespace(val=0) %}
{% for c1 in l1 %}
{% set kids = ns.l2_map[c1.id] %}
{% if (kids | length) > 0 %}
{% set first_col = col_idx.val %}
{% for c2 in kids %}
{% set _ = positions.update({c2.id: [20 + col_idx.val * col_w + col_w // 2, y_l2]}) %}
{% set col_idx.val = col_idx.val + 1 %}
{% endfor %}
{% set last_col = col_idx.val - 1 %}
{% set _ = positions.update({c1.id: [20 + ((first_col + last_col) * col_w) // 2 + col_w // 2, y_l1]}) %}
{% else %}
{% set _ = positions.update({c1.id: [20 + col_idx.val * col_w + col_w // 2, y_l1]}) %}
{% set col_idx.val = col_idx.val + 1 %}
{% endif %}
{% endfor %}
{% set root_xs = namespace(sum=0) %}
{% for c1 in l1 %}{% set root_xs.sum = root_xs.sum + positions[c1.id][0] %}{% endfor %}
{% set root_x = (root_xs.sum // (l1 | length)) if (l1 | length) > 0 else (width // 2) %}
{% if root %}{% set _ = positions.update({root.id: [root_x, y_root]}) %}{% endif %}
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {{ width }} {{ height }}" width="100%">
  {% if root %}
  <g transform="translate({{ positions[root.id][0] - 60 }}, {{ positions[root.id][1] }})">{{ flow(root.id) }}</g>
  {% for c1 in l1 %}
  {% set rx = positions[root.id][0] %}
  {% set ry = positions[root.id][1] + 40 %}
  {% set cx1 = positions[c1.id][0] %}
  {% set cy1 = positions[c1.id][1] %}
  <line x1="{{ rx }}" y1="{{ ry + 16 }}" x2="{{ cx1 }}" y2="{{ cy1 }}"
        stroke="#336699" stroke-width="1.5"/>
  <polygon points="{{ rx }},{{ ry }} {{ rx + 6 }},{{ ry + 8 }} {{ rx }},{{ ry + 16 }} {{ rx - 6 }},{{ ry + 8 }}"
           fill="#336699" stroke="#336699"/>
  <g transform="translate({{ cx1 - 60 }}, {{ cy1 }})">{{ flow(c1.id) }}</g>
  {% for c2 in ns.l2_map[c1.id] %}
  {% set px = positions[c1.id][0] %}
  {% set py = positions[c1.id][1] + 40 %}
  {% set cx2 = positions[c2.id][0] %}
  {% set cy2 = positions[c2.id][1] %}
  <line x1="{{ px }}" y1="{{ py + 16 }}" x2="{{ cx2 }}" y2="{{ cy2 }}"
        stroke="#336699" stroke-width="1.5"/>
  <polygon points="{{ px }},{{ py }} {{ px + 6 }},{{ py + 8 }} {{ px }},{{ py + 16 }} {{ px - 6 }},{{ py + 8 }}"
           fill="#336699" stroke="#336699"/>
  <g transform="translate({{ cx2 - 60 }}, {{ cy2 }})">{{ flow(c2.id) }}</g>
  {% endfor %}
  {% endfor %}
  {% if (l1 | length) == 0 %}
  <text x="{{ width // 2 }}" y="{{ y_l1 + 30 }}" text-anchor="middle"
        font-family="sans-serif" font-size="12" fill="#999">
    No matching elements
  </text>
  {% endif %}
  {% else %}
  <text x="{{ width // 2 }}" y="{{ height // 2 }}" text-anchor="middle"
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
  <a href="{{ ref(a.id) }}">
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
  <a href="{{ ref(a.id) }}">
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
  <a href="{{ ref(uc.id) }}">
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
  <a href="{{ ref(root.id) }}">
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
  {% set rx = cx %}
  {% set ry = 80 %}
  {% set rw = cw - 20 %}
  {% set rh = 220 %}
  {% set _ = child_pos.update({c.id: {"x": rx, "y": ry, "w": rw, "h": rh}}) %}
  <a href="{{ ref(c.id) }}">
    <rect x="{{ rx }}" y="{{ ry }}" width="{{ rw }}" height="{{ rh }}"
          fill="#FFFFFF" stroke="#336699"/>
    <text x="{{ rx + 12 }}" y="100" font-family="sans-serif" font-size="11"
          font-weight="bold" fill="#336699">{{ c.title }}</text>
    <text x="{{ rx + 12 }}" y="118" font-family="monospace" font-size="9"
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
  {% set src_right = src.x + src.w %}
  {% set dst_left = dst.x %}
  {% set src_left = src.x %}
  {% set dst_right = dst.x + dst.w %}
  {% set mid_y = src.y + src.h // 2 %}
  {% set offset = loop.index0 * 12 %}
  {% if src_right <= dst_left %}
  {% set x1 = src_right %}
  {% set y1 = mid_y + offset %}
  {% set x2 = dst_left %}
  {% set y2 = mid_y + offset %}
  {% elif src_left >= dst_right %}
  {% set x1 = src_left %}
  {% set y1 = mid_y + offset %}
  {% set x2 = dst_right %}
  {% set y2 = mid_y + offset %}
  {% else %}
  {% set x1 = src_right %}
  {% set y1 = mid_y + offset %}
  {% set x2 = dst_left %}
  {% set y2 = mid_y + offset %}
  {% endif %}
  <line x1="{{ x1 }}" y1="{{ y1 }}" x2="{{ x2 }}" y2="{{ y2 }}"
        stroke="#444" stroke-dasharray="4 3" stroke-width="1.2"/>
  <text x="{{ (x1 + x2) // 2 }}" y="{{ mid_y + offset - 6 }}" text-anchor="middle"
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
  <a href="{{ ref(ll.id) }}">
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
    <a href="{{ ref(m.id) }}">{{ m.title }}</a>
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
  {% set state_pos = {} %}
  {% for s in states %}
  {% set cx = step * loop.index %}
  {% set cy = 90 if loop.index0 % 2 == 0 else 230 %}
  {% if s.pseudo_kind == 'initial' %}
  {% set _ = state_pos.update({s.id: {"x": cx - 9, "y": cy + 11, "w": 18, "h": 18}}) %}
  <circle cx="{{ cx }}" cy="{{ cy + 20 }}" r="9" fill="#222" stroke="#222"/>
  <text x="{{ cx }}" y="{{ cy + 50 }}" text-anchor="middle"
        font-family="monospace" font-size="9" fill="#666">{{ s.id }}</text>
  {% elif s.pseudo_kind == 'final' %}
  {% set _ = state_pos.update({s.id: {"x": cx - 11, "y": cy + 9, "w": 22, "h": 22}}) %}
  <circle cx="{{ cx }}" cy="{{ cy + 20 }}" r="11" fill="white" stroke="#222"/>
  <circle cx="{{ cx }}" cy="{{ cy + 20 }}" r="6" fill="#222"/>
  <text x="{{ cx }}" y="{{ cy + 50 }}" text-anchor="middle"
        font-family="monospace" font-size="9" fill="#666">{{ s.id }}</text>
  {% elif s.pseudo_kind in ('shallowHistory', 'deepHistory') %}
  {% set _ = state_pos.update({s.id: {"x": cx - 13, "y": cy + 7, "w": 26, "h": 26}}) %}
  <circle cx="{{ cx }}" cy="{{ cy + 20 }}" r="13"
          fill="#EEEEDD" stroke="#888866"/>
  <text x="{{ cx }}" y="{{ cy + 24 }}" text-anchor="middle"
        font-family="serif" font-style="italic" font-size="13">{{
        'H*' if s.pseudo_kind == 'deepHistory' else 'H' }}</text>
  {% elif s.pseudo_kind == 'choice' %}
  {% set _ = state_pos.update({s.id: {"x": cx - 18, "y": cy + 5, "w": 36, "h": 30}}) %}
  <polygon points="{{ cx }},{{ cy + 5 }} {{ cx + 18 }},{{ cy + 20 }} {{ cx }},{{ cy + 35 }} {{ cx - 18 }},{{ cy + 20 }}"
           fill="#FFEEBB" stroke="#CC9900"/>
  {% elif s.pseudo_kind == 'junction' %}
  {% set _ = state_pos.update({s.id: {"x": cx - 6, "y": cy + 14, "w": 12, "h": 12}}) %}
  <circle cx="{{ cx }}" cy="{{ cy + 20 }}" r="6" fill="#888888" stroke="#444"/>
  {% else %}
  {% set _ = state_pos.update({s.id: {"x": cx - 55, "y": cy, "w": 110, "h": 40}}) %}
  <a href="{{ ref(s.id) }}">
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
   {% if src and dst and src.definition == root_id and dst.definition == root_id and t.from_state in state_pos and t.to_state in state_pos %}
   {% set label = (t.trigger or '') %}
   {% if t.guard %}{% set label = label + ' [' + t.guard + ']' %}{% endif %}
   {% if t.effect %}{% set label = label + ' / ' + t.effect %}{% endif %}
   {% set src_rect = state_pos[t.from_state] %}
   {% set dst_rect = state_pos[t.to_state] %}
   {% set src_cx = src_rect.x + src_rect.w // 2 %}
   {% set src_cy = src_rect.y + src_rect.h // 2 %}
   {% set dst_cx = dst_rect.x + dst_rect.w // 2 %}
   {% set dst_cy = dst_rect.y + dst_rect.h // 2 %}
   {% set dx = dst_cx - src_cx %}
   {% set dy = dst_cy - src_cy %}
   {% set dist = (dx * dx + dy * dy) ** 0.5 %}
   {% if dist > 0 %}
   {% set nx = dx / dist %}
   {% set ny = dy / dist %}
   {% else %}
   {% set nx = 0 %}
   {% set ny = 0 %}
   {% endif %}
   {% set src_px = src_cx + nx * (src_rect.w // 2) %}
   {% set src_py = src_cy + ny * (src_rect.h // 2) %}
   {% set dst_px = dst_cx - nx * (dst_rect.w // 2) %}
   {% set dst_py = dst_cy - ny * (dst_rect.h // 2) %}
   <line x1="{{ src_px | round(1) }}" y1="{{ src_py | round(1) }}" x2="{{ dst_px | round(1) }}" y2="{{ dst_py | round(1) }}"
         stroke="#666" stroke-width="1.5"/>
   {% set mx = (src_px + dst_px) // 2 %}
   {% set my = (src_py + dst_py) // 2 %}
   {% set lx = mx + ny * 10 %}
   {% set ly = my - nx * 10 - 6 %}
   <text x="{{ lx | round(1) }}" y="{{ ly | round(1) }}"
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
{% set root = needs.get(root_id) %}
{% set parts = filter("type == 'part' and owned_by == '" + root_id + "'") | list %}
{% set part_ids = parts | map(attribute='id') | list %}
{# Group ports by direction per part so we can place in-ports on the left
   edge, out-ports on the right edge, others on the top. #}
{% set part_ports = {} %}
{% for p in parts %}
{% set ins = [] %}
{% set outs = [] %}
{% set others = [] %}
{% for port in filter("type == 'port' and owned_by == '" + p.id + "'") %}
{% if port.direction == 'in' %}{% set _ = ins.append(port) %}
{% elif port.direction == 'out' %}{% set _ = outs.append(port) %}
{% else %}{% set _ = others.append(port) %}
{% endif %}
{% endfor %}
{% set _ = part_ports.update({p.id: {'in': ins, 'out': outs, 'other': others}}) %}
{% endfor %}
{% set part_w = 170 %}
{% set part_h = 110 %}
{% set part_gap = 120 %}
{% set pad = 70 %}
{% set part_y = 70 %}
{% set count = parts | length %}
{% set width = (pad * 2) + (count * part_w) + ((count - 1) * part_gap) if count > 0 else 720 %}
{% set height = part_y + part_h + 60 %}
{% set ns = namespace(port_pos={}) %}
{% for p in parts %}
{% set p_x = pad + loop.index0 * (part_w + part_gap) %}
{% set ports = part_ports[p.id] %}
{% for port in ports['in'] %}
{% set py_offset = part_h * loop.index // ((ports['in'] | length) + 1) %}
{% set _ = ns.port_pos.update({port.id: [p_x, part_y + py_offset, 'left']}) %}
{% endfor %}
{% for port in ports['out'] %}
{% set py_offset = part_h * loop.index // ((ports['out'] | length) + 1) %}
{% set _ = ns.port_pos.update({port.id: [p_x + part_w, part_y + py_offset, 'right']}) %}
{% endfor %}
{% for port in ports['other'] %}
{% set px_offset = part_w * loop.index // ((ports['other'] | length) + 1) %}
{% set _ = ns.port_pos.update({port.id: [p_x + px_offset, part_y, 'top']}) %}
{% endfor %}
{% endfor %}
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {{ width }} {{ height }}" width="100%">
  {% if root %}
  <rect x="10" y="10" width="{{ width - 20 }}" height="{{ height - 20 }}"
        fill="none" stroke="#336699" stroke-dasharray="4 3"/>
  <text x="24" y="32" font-family="sans-serif" font-size="13" font-style="italic"
        fill="#336699">«ibd» {{ root.title }}</text>
  <text x="24" y="48" font-family="monospace" font-size="9" fill="#666">{{ root_id }}</text>
  {% if count > 0 %}
  {% for p in parts %}
  {% set p_x = pad + loop.index0 * (part_w + part_gap) %}
  <a href="#{{ p.id }}">
    <rect x="{{ p_x }}" y="{{ part_y }}" width="{{ part_w }}" height="{{ part_h }}"
          rx="6" fill="#E8F0FA" stroke="#336699" stroke-width="1.5"/>
    <text x="{{ p_x + part_w // 2 }}" y="{{ part_y + 18 }}" text-anchor="middle"
          font-family="sans-serif" font-size="10" font-style="italic" fill="#666">«Part»</text>
    <text x="{{ p_x + part_w // 2 }}" y="{{ part_y + 38 }}" text-anchor="middle"
          font-family="monospace" font-size="10" fill="#666">{{ p.id }}</text>
    <text x="{{ p_x + part_w // 2 }}" y="{{ part_y + 58 }}" text-anchor="middle"
          font-family="sans-serif" font-size="12" font-weight="bold">{{ p.title }}</text>
  </a>
  {% set ports = part_ports[p.id] %}
  {% for port in ports['in'] + ports['out'] + ports['other'] %}
  {% set pos = ns.port_pos[port.id] %}
  <a href="#{{ port.id }}">
    <rect x="{{ pos[0] - 6 }}" y="{{ pos[1] - 6 }}" width="12" height="12"
          fill="#FFFFFF" stroke="#336699" stroke-width="1.2"/>
    {% if pos[2] == 'left' %}
    <text x="{{ pos[0] - 8 }}" y="{{ pos[1] - 10 }}" text-anchor="end"
          font-family="monospace" font-size="9" fill="#444">{{ port.id }}</text>
    {% elif pos[2] == 'right' %}
    <text x="{{ pos[0] + 8 }}" y="{{ pos[1] - 10 }}"
          font-family="monospace" font-size="9" fill="#444">{{ port.id }}</text>
    {% else %}
    <text x="{{ pos[0] }}" y="{{ pos[1] - 10 }}" text-anchor="middle"
          font-family="monospace" font-size="9" fill="#444">{{ port.id }}</text>
    {% endif %}
  </a>
  {% endfor %}
  {% endfor %}
  {# Connectors: Connection needs whose both ports are inside this IBD #}
  {% for c in filter("type == 'connection'") %}
  {% if c.source_port in ns.port_pos and c.target_port in ns.port_pos %}
  {% set s = ns.port_pos[c.source_port] %}
  {% set t = ns.port_pos[c.target_port] %}
  <line x1="{{ s[0] }}" y1="{{ s[1] }}" x2="{{ t[0] }}" y2="{{ t[1] }}"
        stroke="#444" stroke-width="1.5"/>
  {% set mx = (s[0] + t[0]) // 2 %}
  {% set my = (s[1] + t[1]) // 2 %}
  <text x="{{ mx }}" y="{{ my + 18 }}" text-anchor="middle"
        font-family="sans-serif" font-size="10" font-style="italic" fill="#222">{{ c.title }}</text>
  {% endif %}
  {% endfor %}
  {% else %}
  <text x="{{ width // 2 }}" y="{{ part_y + 50 }}" text-anchor="middle"
        font-family="sans-serif" font-size="12" fill="#999">
    No internal parts
  </text>
  {% endif %}
  {% else %}
  <text x="{{ width // 2 }}" y="{{ height // 2 }}" text-anchor="middle"
        font-family="sans-serif" font-size="12" fill="red">
    Unknown root need: {{ root_id }}
  </text>
  {% endif %}
</svg>
"""


PAR_SVG_TEMPLATE = """\
{% set root_id = "__ROOT_ID__" %}
{% set root = needs.get(root_id) %}
{% set bindings = filter("type == 'bindingconnector'") | list %}
{% set value_props = filter("type == 'valueproperty'") | list %}
{% set param_count = (root.parameters or '').split(',') | reject('equalto', '') | list | length %}
{% set vp_count = value_props | length %}
{% set box_w = 160 %}
{% set box_h = 60 %}
{% set svg_w = (param_count + vp_count + 2) * box_w + 40 %}
{% set svg_h = 280 %}
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {{ svg_w }} {{ svg_h }}" width="100%">
  {% if root %}
  <a href="{{ ref(root.id) }}">
    <rect x="20" y="20" width="{{ box_w }}" height="{{ box_h }}"
          rx="8" fill="#FFF0DC" stroke="#CC8800"/>
    <text x="{{ 20 + box_w // 2 }}" y="44" text-anchor="middle"
          font-family="sans-serif" font-size="11" font-weight="bold">{{ root.title }}</text>
    <text x="{{ 20 + box_w // 2 }}" y="62" text-anchor="middle"
          font-family="monospace" font-size="9" fill="#666">&lt;&lt;constraint&gt;&gt;</text>
  </a>
  {% set param_ids = (root.parameters or '').split(',') | map('trim') | reject('equalto', '') | list %}
  {% for pid in param_ids %}
  {% set param = needs.get(pid) %}
  {% if param %}
  {% set px = 20 + loop.index * box_w %}
  <circle cx="{{ px + box_w // 2 }}" cy="50" r="8"
          fill="#FFE8C8" stroke="#CC8800"/>
  <text x="{{ px + box_w // 2 }}" y="80" text-anchor="middle"
        font-family="monospace" font-size="8" fill="#666">{{ param.id }}</text>
  {% endif %}
  {% endfor %}
  {% for vp in value_props %}
  {% set vx = 20 + (param_count + 1 + loop.index0) * box_w %}
  <a href="{{ ref(vp.id) }}">
    <rect x="{{ vx }}" y="140" width="{{ box_w - 10 }}" height="{{ box_h }}"
          rx="4" fill="#E8F4FF" stroke="#336699"/>
    <text x="{{ vx + (box_w - 10) // 2 }}" y="164" text-anchor="middle"
          font-family="sans-serif" font-size="11">{{ vp.title }}</text>
    <text x="{{ vx + (box_w - 10) // 2 }}" y="182" text-anchor="middle"
          font-family="monospace" font-size="9" fill="#666">{{ vp.value_type or '' }}{% if vp.default_value %} = {{ vp.default_value }}{% endif %}</text>
  </a>
  {% endfor %}
  {% for b in bindings %}
  {% set src_param = needs.get(b.source_parameter) %}
  {% set dst_value = needs.get(b.target_value) %}
  {% if src_param and dst_value %}
  {% set src_idx = param_ids.index(src_param.id) + 1 if src_param.id in param_ids else -1 %}
  {% set dst_idx = -1 %}
  {% for i, vp in enumerate(value_props) %}
  {% if vp.id == dst_value.id %}{% set dst_idx = i %}{% endif %}
  {% endfor %}
  {% if src_idx > 0 and dst_idx >= 0 %}
  {% set sx = 20 + src_idx * box_w + box_w // 2 %}
  {% set dx = 20 + (param_count + 1 + dst_idx) * box_w + (box_w - 10) // 2 %}
  <line x1="{{ sx }}" y1="58" x2="{{ dx }}" y2="140"
        stroke="#444" stroke-dasharray="4 3" stroke-width="1.2"/>
  {% if b.unit %}
  <text x="{{ (sx + dx) // 2 }}" y="{{ (58 + 140) // 2 - 4 }}"
        text-anchor="middle" font-family="sans-serif" font-size="10"
        fill="#444" font-style="italic">{{ b.unit }}</text>
  {% endif %}
  {% endif %}
  {% endif %}
  {% endfor %}
  {% else %}
  <text x="360" y="140" text-anchor="middle"
        font-family="sans-serif" font-size="12" fill="red">
    Unknown root constraint: {{ root_id }}
  </text>
  {% endif %}
</svg>
"""
