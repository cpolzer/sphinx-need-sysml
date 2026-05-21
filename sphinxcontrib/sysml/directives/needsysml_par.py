"""Needsyml parametric diagram directive — wraps needuml with pre-baked PAR template."""

from typing import Any

from docutils.parsers.rst import directives
from docutils.statemachine import StringList
from sphinx.application import Sphinx
from sphinx.util.docutils import SphinxDirective

from sphinxcontrib.sysml.svg_templates import PAR_SVG_TEMPLATE
from sphinxcontrib.sysml.templates import PAR_FULL_TEMPLATE


class NeedsymlParDirective(SphinxDirective):
    """Generate a parametric diagram for a given ConstraintBlock need.

    Wraps ``.. needuml::`` with ``:config: sysml_par`` and the
    ``PAR_FULL_TEMPLATE`` body. Uses a class-diagram approximation
    since PlantUML has no native parametric mode.
    """

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        "scale": directives.unchanged,
        "align": directives.unchanged,
    }

    def run(self) -> list[Any]:
        root_id = self.arguments[0]
        scale = self.options.get("scale")
        align = self.options.get("align", "center")

        content = PAR_FULL_TEMPLATE.replace("{root_id}", root_id)

        from sphinx_needs.directives.needuml import NeedumlDirective

        content_list = StringList(content.splitlines(), source="needsysml-par")
        needuml = NeedumlDirective(
            name="needuml",
            arguments=[],
            options={
                "config": "sysml_par",
                "scale": scale or "",
                "align": align,
            },
            content=content_list,
            lineno=self.lineno,
            content_offset=self.content_offset,
            block_text=self.block_text,
            state=self.state,
            state_machine=self.state_machine,
        )

        return needuml.run()  # type: ignore[no-any-return]


class NeedsymlParSvgDirective(SphinxDirective):
    """Generate a parametric diagram as inline SVG."""

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        "align": directives.unchanged,
        "width": directives.unchanged,
    }

    def run(self) -> list[Any]:
        from sphinxcontrib.sysml.directives.needsysml_svg import (
            _emit_needsvg_node,
            _substitute,
        )

        root_id = self.arguments[0]
        align = self.options.get("align", "center")
        width = self.options.get("width", "100%")
        content = _substitute(PAR_SVG_TEMPLATE, root_id)
        return _emit_needsvg_node(self, content, width, align)


def setup(app: Sphinx) -> None:
    """Register the needsysml-par directives."""
    app.add_directive("needsysml-par", NeedsymlParDirective)
    app.add_directive("needsysml-par-svg", NeedsymlParSvgDirective)
