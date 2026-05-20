"""Needsyml use case directive (PlantUML + SVG variants)."""

from typing import Any

from docutils.parsers.rst import directives
from docutils.statemachine import StringList
from sphinx.application import Sphinx
from sphinx.util.docutils import SphinxDirective

from sphinxcontrib.sysml.svg_templates import UC_SVG_TEMPLATE
from sphinxcontrib.sysml.templates import UC_FULL_TEMPLATE


class NeedsymlUcDirective(SphinxDirective):
    """Generate a use case diagram.

    Walks ``UseCase`` needs matching the filter argument (default
    ``type == 'UseCase'``) and groups them by ``subject`` into system
    boundaries. Actors render outside the boundary; their
    ``interacts_with`` field drives solid association lines.
    extends / includes / generalizes render between use cases as
    dashed labelled arrows.
    """

    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = True
    option_spec = {
        "filter": directives.unchanged,
        "subject": directives.unchanged,
        "scale": directives.unchanged,
        "align": directives.unchanged,
    }

    def run(self) -> list[Any]:
        if self.arguments:
            filter_expr = self.arguments[0]
        else:
            filter_expr = self.options.get("filter", "type == 'UseCase'")
        subject_filter = self.options.get("subject", "")
        scale = self.options.get("scale")
        align = self.options.get("align", "center")

        content = UC_FULL_TEMPLATE.replace("{filter_expr}", filter_expr).replace(
            "{subject_filter}", subject_filter
        )

        from sphinx_needs.directives.needuml import NeedumlDirective

        content_list = StringList(content.splitlines(), source="needsysml-uc")
        needuml = NeedumlDirective(
            name="needuml",
            arguments=[filter_expr],
            options={
                "config": "sysml_uc",
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


class NeedsymlUcSvgDirective(SphinxDirective):
    """Generate a use case diagram as inline SVG."""

    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = True
    option_spec = {
        "filter": directives.unchanged,
        "subject": directives.unchanged,
        "align": directives.unchanged,
        "width": directives.unchanged,
    }

    def run(self) -> list[Any]:
        from sphinxcontrib.sysml.directives.needsysml_svg import (
            _emit_needsvg_node,
            _substitute,
        )

        if self.arguments:
            filter_expr = self.arguments[0]
        else:
            filter_expr = self.options.get("filter", "type == 'UseCase'")
        align = self.options.get("align", "center")
        width = self.options.get("width", "100%")
        content = _substitute(UC_SVG_TEMPLATE, "", filter_expr)
        return _emit_needsvg_node(self, content, width, align)


def setup(app: Sphinx) -> None:
    """Register the needsysml-uc and needsysml-uc-svg directives."""
    app.add_directive("needsysml-uc", NeedsymlUcDirective)
    app.add_directive("needsysml-uc-svg", NeedsymlUcSvgDirective)
