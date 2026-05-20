"""Needsyml SVG BDD directive — renders inline SVG using sphinx-need-svg."""

from typing import Any

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.application import Sphinx
from sphinx.util.docutils import SphinxDirective


class NeedsymlBddSvgDirective(SphinxDirective):
    """Generate a Block Definition Diagram as inline SVG.

    Uses ``sphinx-need-svg``'s ``SvgJinjaContext`` to render a BDD
    with native SVG hyperlinks — works without PlantUML.
    """

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        "depth": directives.unchanged,
        "filter": directives.unchanged,
        "align": directives.unchanged,
    }

    def run(self) -> list[Any]:
        root_id = self.arguments[0]
        align = self.options.get("align", "center")

        # Build SVG content using sphinx-need-svg's Jinja context
        from sphinx_need_svg.jinja_context import render_jinja_svg

        # SVG BDD template — uses needsvg's flow() for blocks
        svg_template = """\
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 400">
  <style>
    .partdef { fill: #DDEEFF; stroke: #336699; stroke-width: 2; }
    .part { fill: #BBDDFF; stroke: #336699; stroke-width: 1; }
    .label { font-family: sans-serif; font-size: 12px; }
    .id-label { font-family: monospace; font-size: 10px; fill: #666; }
    .composition { stroke: #333; stroke-width: 2; }
  </style>
  {% set root = needs.get(root_id) %}
  {% if root %}
  {{ flow(root_id) }}
  {% set children = filter("type == 'Part' and owned_by == '" + root_id + "'") %}
  {% for child in children %}
  {{ flow(child.id) }}
  {% endfor %}
  {% endif %}
</svg>"""

        content = svg_template.replace("{root_id}", root_id)
        svg_markup, _ = render_jinja_svg(content, self.env.app)

        # Wrap in a container for alignment
        wrapper_attrs = {"style": f"text-align: {align}; margin: 1em 0;"}
        wrapper = nodes.container("", **wrapper_attrs)
        wrapper += nodes.raw("", svg_markup, format="html")

        return [wrapper]


def setup(app: Sphinx) -> None:
    """Register the needsysml-bdd-svg directive."""
    app.add_directive("needsysml-bdd-svg", NeedsymlBddSvgDirective)
