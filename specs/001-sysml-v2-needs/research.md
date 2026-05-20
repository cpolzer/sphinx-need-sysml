# Research: SysML v2 sphinx-needs Extension

**Date**: 2026-05-20
**Feature**: specs/001-sysml-v2-needs

---

## 1. PlantUML and SysML v2 Support

### Decision
Use PlantUML class diagrams with `<<stereotype>>` annotations as the primary rendering backend. There is no native SysML support in PlantUML — no `@startsysml`, no `!include <SysML>` standard library, no SysML-specific diagram modes.

### Rationale
PlantUML's class diagram syntax is the most faithful approximation available:
- `*--` composition arrow maps to SysML composition (filled diamond)
- `..>` dashed dependency + `: <<satisfy>>` label maps to SysML satisfaction/derivation
- `<<block>>`, `<<requirement>>`, `<<port>>` stereotypes render as display labels
- Named compartments (`== Attributes ==`, `-- Ports --`) approximate SysML block compartments

Requirements diagrams are the highest-fidelity result. BDD is achievable. IBD is the weakest — PlantUML's `portin`/`portout` in component diagrams cannot reliably lock ports to block edges.

### Alternatives Considered
- **Native SysML v2 textual notation**: Out of scope for v1 per spec.
- **Mermaid**: No SysML support at all.
- **Custom SVG renderer**: Covered by sphinx-need-svg (see section 3).

### PlantUML Code Patterns

**BDD (Block Definition Diagram)** — use `@startuml` class diagram:
```plantuml
skinparam class<<block>> {
    BackgroundColor #DDEEFF
    BorderColor #336699
}
class "PD-001\nEngine" <<block>> [[../parts.html#PD-001{Engine}]] {
    == Attributes ==
    + power : kW
    + displacement : cm3
    -- Ports --
    + fuelIn : FuelPort
}
class "PD-002\nVehicle" <<block>> [[../system.html#PD-002{Vehicle}]] {
}
PD-002 *--> "1" PD-001 : engine
```

**Requirements Diagram** — use class diagram with `..>` arrows:
```plantuml
skinparam class<<requirement>> {
    BackgroundColor #FFF0CC
    BorderColor #CC9900
}
class "R-001\nBrake Performance" <<requirement>> [[../req.html#R-001]] {
    text = "Decelerate >= 8 m/s2"
}
PD-001 ..> R-001 : <<satisfy>>
R-001 ..> R-002 : <<deriveReqt>>
```

**IBD (Internal Block Diagram)** — use component diagram (limited fidelity):
```plantuml
rectangle "vehicle : Vehicle" <<ibd>> {
    component "engine : Engine" <<block>> as engine {
        portin fuelIn
        portout drive
    }
    component "wheel : Wheel" <<block>> as wheel {
        portin driveIn
    }
}
engine::drive --> wheel::driveIn
```

### Key Limitation: No `!include <SysML>`
There is no official PlantUML SysML library. All skinparam styling must be defined inline or in a custom include file. The extension will ship a default skinparam config via `needs_flow_configs`.

---

## 2. sphinx-needs API for Extension Registration

### Decision
Use `add_need_type()` + `add_field()` (new API, no `app` param) called from a `config-inited` event handler. Provide a compatibility shim identical to `sphinx-test-reports` for `add_field` vs `add_extra_option`.

### Exact Signatures (sphinx-needs ≥ 1.0)

```python
add_need_type(
    app: Sphinx,
    directive: str,    # RST directive name, e.g. "partdef"
    title: str,        # Human-readable name, e.g. "PartDef"
    prefix: str,       # ID prefix, e.g. "PD-"
    color: str = "#ffffff",
    style: str = "node",
) -> None

add_field(
    name: str,              # positional-only
    /,
    description: str,       # positional
    *,
    schema: dict | None = None,   # {"type": "string"}, {"type": "boolean"}, etc.
    nullable: bool | None = None,
    default: Any = None,
) -> None
```

`add_field` has no `app` parameter (unlike the deprecated `add_extra_option`). Both must be called at `config-inited`.

### Registration Pattern

```python
def setup(app: Sphinx) -> dict:
    app.setup_extension("sphinx_needs")
    app.connect("config-inited", _register_types_and_fields)
    app.connect("builder-inited", _register_flow_configs)
    return {"version": VERSION, "parallel_read_safe": True}
```

`needs_flow_configs` must be mutated at `builder-inited` (not `config-inited`) — merge with any user-defined entries to avoid clobbering:
```python
def _register_flow_configs(app: Sphinx) -> None:
    existing = app.config.needs_flow_configs or {}
    app.config.needs_flow_configs = {**_SYSML_CONFIGS, **existing}
```

### Alternatives Considered
- No `add_flow_config()` API exists in `sphinx_needs.api` — direct config mutation is the only path.

---

## 3. Hyperlink Strategy: PlantUML vs sphinx-need-svg

### Decision
**Dual-path approach**: PlantUML/needuml as primary (auto-layout), sphinx-need-svg as secondary (precision + reliable links).

### PlantUML Links (Primary Path)
PlantUML supports `[[url{tooltip}label]]` syntax on class/component elements. In HTML output:
- Works when `plantuml_output_format = "svg"` → sphinxcontrib-plantuml renders `<object>` tag → inline SVG `<a>` links are clickable.
- Fails when `plantuml_output_format = "svg_img"` → `<img>` tag → browser sandboxes SVG navigation.
- Same-page anchors require `skinparam topurl <base_url>` — the extension will emit a warning if `plantuml_output_format` is not `svg`.

The `ref()` function in needuml context generates `[[{docname}.html#{need_id}{title}]]` strings. PlantUML URL syntax:
```
class "PD-001" [[parts.html#PD-001{Engine block definition}]]
```

### sphinx-need-svg (Secondary Path — Precision Diagrams)
`sphinx-need-svg` renders inline SVG directly into the HTML DOM via `nodes.raw()`. Hyperlinks are native SVG `<a href>` — work in all browsers without any configuration.

`SvgJinjaContext.ref(need_id)` returns `{docname}.html#{need_id}` — a relative URL from any page in the same Sphinx build.

**Use cases for sphinx-need-svg path:**
- Precision IBD diagrams where port placement matters
- Users without PlantUML installed
- Custom architecture diagrams with fixed layouts

**Dependency**: `sphinx-need-svg` is an optional dependency. The extension detects its presence and enables the `.. needsysml::` SVG-based directive when available.

### Alternatives Considered
- PNG + `.cmapx` image maps: not supported by sphinxcontrib-plantuml automatically; rejected.
- Requiring SVG output format: too prescriptive; instead emit a warning.

---

## 4. needuml Jinja Template Context

### Key Findings
`needs_flow_configs` values are **raw PlantUML skinparam strings**, NOT Jinja2 templates. The Jinja2 template is in the `.. needuml::` directive body.

Available in `.. needuml::` body:

| Name | Signature | Description |
|------|-----------|-------------|
| `needs` | `dict[str, NeedItem]` | All needs keyed by ID |
| `uml(id)` | `uml(need_id, key="diagram", **kwargs) -> str` | Render one need as PlantUML; expands stored arch snippet if present |
| `flow(id)` | `flow(need_id) -> str` | Render need as standard needflow node |
| `filter(expr)` | `filter(filter_string) -> list[NeedItem]` | Return needs matching sphinx-needs filter expression |
| `ref(id)` | `ref(need_id, option=None, text=None) -> str` | Generate `[[url text]]` PlantUML hyperlink string |
| `import(...)` | needarch-only | Not available in standalone `.. needuml::` |

`uml()` is **not auto-recursive** — it renders one element and expands any stored `arch` snippet. To expand children:
```jinja2
{{ uml("PD-001") }}
{% for part in filter("type == 'Part' and owned_by == 'PD-001'") %}
{{ uml(part.id) }}
PD-001 *-- {{ part.id }}
{% endfor %}
```

### Implication for Extension Design
The extension cannot ship Jinja2 templates as `flow_config` values. Instead it must:
1. Ship `flow_config` skinparam strings (styling only)
2. Ship Jinja2 template snippets as documentation examples and as Python string constants users can `{% include %}` or copy

For fully automated diagram generation, the extension should provide a custom `.. needsysml-bdd::` directive that wraps `.. needuml::` with a pre-filled Jinja2 body, so users don't write the Jinja2 manually.
