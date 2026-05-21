"""Needsyml SVG directives — render diagrams as inline SVG via sphinx-need-svg.

We build a pre-baked Jinja template (root, children-from-filter, layout)
and hand it off to sphinx-need-svg's ``Needsvg`` placeholder node so that
rendering happens at ``doctree-resolved`` time. Doing the render in our
own ``run()`` would call ``SphinxNeedsData.get_needs_view()`` mid-parse,
which freezes the needs registry and breaks every later directive.

Hosts the BDD-svg directive (existing) and the IBD-svg directive
(promotion of the raw-needsvg workaround that used to live in
``docs/examples/vehicle_system.rst``).
"""

from typing import Any

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.application import Sphinx
from sphinx.util.docutils import SphinxDirective

from sphinxcontrib.sysml.svg_templates import (
    BDD_SVG_TEMPLATE,
    IBD_SVG_TEMPLATE,
)


def _emit_needsvg_node(
    directive: SphinxDirective,
    content: str,
    width: str,
    align: str,
) -> list[Any]:
    """Stash the template into env.needsvg_all_data and return placeholder nodes.

    Shared by every ``needsysml-*-svg`` directive — keeps the deferred
    rendering plumbing in one place.
    """
    from sphinx_need_svg.directives.needsvg import Needsvg

    env = directive.env
    serial = env.new_serialno("needsvg")
    targetid = f"needsvg-{env.docname}-{serial}"

    if not hasattr(env, "needsvg_all_data"):
        env.needsvg_all_data = {}  # type: ignore[attr-defined]

    env.needsvg_all_data[targetid] = {  # type: ignore[attr-defined]
        "docname": env.docname,
        "lineno": directive.lineno,
        "content": content,
        "options": {
            "width": width,
            "height": "auto",
            "align": align,
            "debug": False,
        },
    }

    targetnode = nodes.target("", "", ids=[targetid])
    node = Needsvg("")
    node["targetid"] = targetid
    return [targetnode, node]


def _substitute(template: str, root_id: str, filter_expr: str | None = None) -> str:
    """Substitute the two placeholder tokens into an SVG Jinja template."""
    out = template.replace("__ROOT_ID__", root_id)
    if filter_expr is not None:
        out = out.replace("__FILTER_EXPR__", filter_expr.replace('"', '\\"'))
    return out


class NeedsymlBddSvgDirective(SphinxDirective):
    """Generate a Block Definition Diagram as inline SVG."""

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        "depth": directives.unchanged,
        "filter": directives.unchanged,
        "align": directives.unchanged,
        "width": directives.unchanged,
    }

    def run(self) -> list[Any]:
        root_id = self.arguments[0]
        align = self.options.get("align", "center")
        width = self.options.get("width", "100%")
        filter_expr = self.options.get(
            "filter", f"type == 'PartDef' and owned_by == '{root_id}'"
        )
        content = _substitute(BDD_SVG_TEMPLATE, root_id, filter_expr)
        return _emit_needsvg_node(self, content, width, align)


class NeedsymlIbdSvgDirective(SphinxDirective):
    """Generate an Internal Block Diagram as inline SVG.

    Promotion of the raw-needsvg IBD template that previously lived in
    ``docs/examples/vehicle_system.rst``. Renders the root PartDef's owned
    Parts with their owned Ports inside a dashed system-boundary rectangle.
    """

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        "show-ports": directives.unchanged,
        "align": directives.unchanged,
        "width": directives.unchanged,
    }

    def run(self) -> list[Any]:
        root_id = self.arguments[0]
        align = self.options.get("align", "center")
        width = self.options.get("width", "100%")
        content = _substitute(IBD_SVG_TEMPLATE, root_id)
        return _emit_needsvg_node(self, content, width, align)


def setup(app: Sphinx) -> None:
    """Register the SVG directives (BDD + IBD)."""
    app.add_directive("needsysml-bdd-svg", NeedsymlBddSvgDirective)
    app.add_directive("needsysml-ibd-svg", NeedsymlIbdSvgDirective)
