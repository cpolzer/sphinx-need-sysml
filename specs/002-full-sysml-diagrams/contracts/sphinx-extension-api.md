# Contract: Sphinx Extension API (Feature 002)

**Date**: 2026-05-20

This contract is additive to [`../../001-sysml-v2-needs/contracts/sphinx-extension-api.md`](../../001-sysml-v2-needs/contracts/sphinx-extension-api.md). Existing contracts continue to hold; this document covers only the new directives and behaviors introduced in feature `002-full-sysml-diagrams`.

---

## 1. Conf.py setup (unchanged)

Engineers using this feature need no new entries in `conf.py` beyond what 001 already requires:

```python
extensions = [
    "sphinx_needs",
    "sphinxcontrib.plantuml",
    "sphinx_need_sysml",
    "sphinx_need_svg",   # optional — only needed for *-svg directives
]
plantuml_output_format = "svg"
```

When `sphinx_need_svg` is absent from `extensions`, the SVG companion directives (`needsysml-stm-svg`, `needsysml-act-svg`, …) are not registered. The corresponding PlantUML directives still work.

---

## 2. New directives (PlantUML path)

All new PlantUML directives follow the same surface as the existing `needsysml-bdd` / `needsysml-ibd` / `needsysml-req` directives: they wrap `.. needuml::` with a pre-baked Jinja template + a per-diagram `:config: sysml_<x>` flow config.

### 2.1 `needsysml-stm` — State Machine Diagram

```rst
.. needsysml-stm:: <statedef-id>
   :scale: <N>%
   :align: <left|center|right>
```

**Required argument**: A `StateDef` need ID. The renderer walks all `StateUsage` needs whose `definition` equals this `StateDef`, plus all `Transition` needs whose `from_state` or `to_state` lies in that set.

**Optional options**:
- `:scale:` — PlantUML scale (e.g. `80%`).
- `:align:` — diagram horizontal alignment.

**Output**: PlantUML state diagram with composite states, history pseudostates, choice/junction, transitions labelled `trigger [guard] / effect`. Need links activate when `plantuml_output_format = "svg"`.

### 2.2 `needsysml-act` — Activity Diagram

```rst
.. needsysml-act:: <actiondef-id>
   :show-partitions: true|false
   :scale: <N>%
   :align: <left|center|right>
```

**Required argument**: An `ActionDef` need ID. The renderer walks all `Action` needs whose `definition` equals this `ActionDef`, groups by `partition`, then walks `ControlFlow` and `ObjectFlow` edges among those actions.

**Optional options**:
- `:show-partitions:` — when `true` (default), emit swimlane blocks per distinct `partition` value. When `false`, all actions render at the top level.
- `:scale:`, `:align:` — as above.

**Output**: PlantUML activity-beta diagram with swimlanes, fork/join, decision/merge, and object-flow nodes.

### 2.3 `needsysml-sd` — Sequence Diagram

```rst
.. needsysml-sd:: <interaction-id>
   :scale: <N>%
   :align: <left|center|right>
```

**Required argument**: An ID identifying the interaction. Conventionally an `ActionDef` representing the interaction; the renderer walks `Lifeline` needs whose `definition` equals this ID, plus `Message` needs whose `from_lifeline` or `to_lifeline` lies in that set.

**Output**: PlantUML sequence diagram with lifelines, sync/async/return messages, combined fragments grouped by `fragment_group`.

### 2.4 `needsysml-uc` — Use Case Diagram

```rst
.. needsysml-uc:: <filter-expression>
   :subject: <name>
   :scale: <N>%
   :align: <left|center|right>
```

**Required argument**: A sphinx-needs filter expression selecting which use cases to draw. Default in the absence of an argument is `type == 'UseCase'`.

**Optional options**:
- `:subject:` — restrict to use cases with this `subject` value. Default: all subjects, rendered in separate boundary rectangles.
- `:scale:`, `:align:` — as above.

**Output**: PlantUML use case diagram with actor figures outside one or more system-boundary rectangles, solid association lines from each actor to the use cases listed in its `interacts_with` field, and dashed labelled arrows for the `extends` / `includes` / `generalizes` use-case-to-use-case relationships.

### 2.5 `needsysml-pkg` — Package Diagram

```rst
.. needsysml-pkg:: <root-package-id>
   :depth: <N>
   :scale: <N>%
   :align: <left|center|right>
```

**Required argument**: A `Package` need ID — the root of the rendered tree.

**Optional options**:
- `:depth:` — max nesting depth (default 3).
- `:scale:`, `:align:` — as above.

**Output**: PlantUML package diagram with nested packages and labelled dependency arrows.

### 2.6 `needsysml-par` (v1.1) — Parametric Diagram

```rst
.. needsysml-par:: <constraintblock-id>
   :scale: <N>%
   :align: <left|center|right>
```

**Required argument**: A `ConstraintBlock` need ID. The renderer draws the constraint block, its parameters, and the value properties bound to those parameters by `BindingConnector` edges.

**Output**: PlantUML class-diagram approximation (per `research.md § 1`) with a `<<constraint>>`-stereotyped class and labelled binding arrows.

### 2.7 `needsysml-alloc` (v1.1) — Allocation Matrix

```rst
.. needsysml-alloc::
   :rows: <filter-expression>
   :columns: <filter-expression>
   :marker: <character>
```

**No required argument** (per spec Q3 — defaults work for the common case).

**Optional options**:
- `:rows:` — filter expression for the row axis. Default: `allocates != ""`.
- `:columns:` — filter expression for the column axis. Default: needs referenced by any `allocates` value (computed from the row set).
- `:marker:` — character placed at allocated intersections. Default `✓`.

**Output**: A docutils `<table>` with row-need links as row headers, column-need links as column headers, and the marker character at intersections.

---

## 3. New directives (SVG companion path)

For each of `stm`, `act`, `sd`, `uc`, `pkg`, `par`, plus the previously-existing `ibd` and `bdd`, register a `-svg` companion directive: `needsysml-stm-svg`, `needsysml-act-svg`, `needsysml-sd-svg`, `needsysml-uc-svg`, `needsysml-pkg-svg`, `needsysml-par-svg`, `needsysml-ibd-svg` (promotion), `needsysml-bdd-svg` (already present).

All companions follow the identical surface as the PlantUML directive (same required argument, same options) but route through the `sphinx_need_svg.directives.needsvg.Needsvg` placeholder:

```python
def run(self) -> list[Any]:
    content = self._render_svg_template()
    targetid = f"needsvg-{self.env.docname}-{self.env.new_serialno('needsvg')}"
    self.env.needsvg_all_data.setdefault(targetid, {
        "docname": self.env.docname,
        "lineno": self.lineno,
        "content": content,
        "options": {"width": "100%", "height": "auto", "align": ..., "debug": False},
    })
    return [nodes.target("", "", ids=[targetid]),
            self._make_needsvg_node(targetid)]
```

Each `-svg` directive's `_render_svg_template()` returns an SVG string with placeholder tokens (`__ROOT_ID__`, `__FILTER_EXPR__`) substituted into the Jinja-bearing template in `svg_templates.py`. Sphinx-need-svg's `process_needsvg` handler then runs the Jinja template against the live needs registry at `doctree-resolved`.

**Registration gate**: SVG companions are registered only when `importlib.util.find_spec("sphinx_need_svg")` succeeds. The PlantUML directives are always registered.

---

## 4. `needsysml-req` enhancement (additive)

`needsysml-req` already accepts a positional filter argument. This feature adds an optional `:filter:` option with default `type == 'Requirement'`. The positional form continues to work for backward compatibility:

```rst
.. needsysml-req::
   :filter: type == 'Requirement' and status == 'accepted'
   :show-satisfy: true
   :align: center
```

When neither the positional argument nor `:filter:` is supplied, the directive defaults to `type == 'Requirement'`.

---

## 5. Behavior contracts

### 5.1 Unknown-reference handling (FR-016)

When a directive's input arguments or options reference a need ID that does not exist in the needs registry, the directive MUST:
1. Emit one Sphinx warning, categorized under `[needsysml.<diagram>.unknown-*]` (see `data-model.md § Validation Rules`).
2. Render output that contains an explicit `??` or `Unknown: <id>` placeholder at the position the element would have occupied.
3. NOT abort the build. The build's overall return code remains 0 unless the user has enabled `-W` (warnings-as-errors).

### 5.2 Renderer-not-installed handling (FR-017)

When `sphinx_need_svg` is not installed:
- `-svg` companion directives MUST NOT be registered (no `app.add_directive` call).
- The PlantUML directives MUST continue to register and function.
- Documents that include `-svg` directives produce Sphinx's standard `unknown directive` warning, not an extension crash. This is the same degradation engineers see for `sphinxcontrib-plantuml` already.

When `sphinxcontrib.plantuml` is not installed:
- The PlantUML directives ARE registered but emit a warning (existing 001 behavior).
- `-svg` companions, if registered, continue to work — they don't depend on PlantUML.

### 5.3 Empty-result handling (FR-018)

When a directive's filter resolves to an empty set (no states, no actions, no packages, …):
- The directive MUST render an SVG/PlantUML output containing an explicit "No matching elements" placeholder.
- The directive MUST emit one informational warning (`[needsysml.<diagram>.empty]`) so engineers learn about the empty result without a hard failure.

### 5.4 Clickable links (FR-013, FR-014)

- PlantUML directives: each rendered need is wrapped in PlantUML's `[[<docname>.html#<need-id> <title>]]` link syntax. Requires `plantuml_output_format = "svg"`. The existing warning in `warnings.py` continues to fire when this is not set.
- SVG companions: each rendered need is wrapped in an SVG `<a href="<docname>.html#<need-id>">` element produced by `sphinx_need_svg.jinja_context.SvgJinjaContext.flow()`. Works in every output format that supports inline SVG.

### 5.5 Allocation matrix non-link cells (FR-013)

Row and column headers in the matrix link to the corresponding need anchors. Interior marker cells do NOT link.

---

## 6. Extension setup function

`sphinx_need_sysml.setup(app)` is extended:

```python
def setup(app: Sphinx) -> dict[str, object]:
    app.setup_extension("sphinx_needs")
    app.connect("config-inited", _register_types_and_fields)
    app.connect("builder-inited", _register_flow_configs)
    app.connect("builder-inited", _warn_plantuml_format)

    # Existing 001 directives
    app.add_directive("needsysml-bdd", NeedsymlBddDirective)
    app.add_directive("needsysml-ibd", NeedsymlIbdDirective)
    app.add_directive("needsysml-req", NeedsymlReqDirective)

    # v1 new directives
    app.add_directive("needsysml-stm", NeedsymlStmDirective)
    app.add_directive("needsysml-act", NeedsymlActDirective)
    app.add_directive("needsysml-sd",  NeedsymlSdDirective)
    app.add_directive("needsysml-uc",  NeedsymlUcDirective)
    app.add_directive("needsysml-pkg", NeedsymlPkgDirective)

    # v1.1 new directives
    app.add_directive("needsysml-par",   NeedsymlParDirective)
    app.add_directive("needsysml-alloc", NeedsymlAllocDirective)

    if _HAS_NEED_SVG:
        # v0.2 svg
        app.add_directive("needsysml-bdd-svg", NeedsymlBddSvgDirective)
        # v1 svg
        app.add_directive("needsysml-ibd-svg", NeedsymlIbdSvgDirective)
        app.add_directive("needsysml-stm-svg", NeedsymlStmSvgDirective)
        app.add_directive("needsysml-act-svg", NeedsymlActSvgDirective)
        app.add_directive("needsysml-sd-svg",  NeedsymlSdSvgDirective)
        app.add_directive("needsysml-uc-svg",  NeedsymlUcSvgDirective)
        app.add_directive("needsysml-pkg-svg", NeedsymlPkgSvgDirective)
        # v1.1 svg
        app.add_directive("needsysml-par-svg", NeedsymlParSvgDirective)

    return {
        "version": VERSION,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
```

---

## 7. Versioning

| Release | Version | Contents |
|---|---|---|
| v1 | `sphinx-need-sysml 0.3.0` | All 13 new need types, ~25 new fields, 6 new flow configs, all six v1 PlantUML directives, all six v1 SVG companions, `needsysml-req` `:filter:` option, `needsysml-ibd-svg` promotion. v1.1 element types (ConstraintBlock, ConstraintParameter, ValueProperty, BindingConnector) registered but their directives NOT yet added. |
| v1.1 | `sphinx-need-sysml 0.4.0` | `needsysml-alloc` matrix, `needsysml-par` + `needsysml-par-svg` directives. Their templates added. No new types/fields beyond v1. |

Bump `sphinx_need_sysml/__init__.py:VERSION` and `pyproject.toml:[project] version` in lockstep; `tool.commitizen.version_files` already lists both. Commit message style: `feat: full SysML diagram coverage (v1)` etc., per the project's existing commitizen config.
