"""Needsyml activity directive (PlantUML + SVG variants)."""

from typing import Any

from docutils.parsers.rst import directives
from docutils.statemachine import StringList
from sphinx.application import Sphinx
from sphinx.util.docutils import SphinxDirective

from sphinxcontrib.sysml.svg_templates import ACT_SVG_TEMPLATE
from sphinxcontrib.sysml.templates import ACT_FULL_TEMPLATE


class NeedsymlActDirective(SphinxDirective):
    """Generate an activity diagram for a given ActionDef.

    Wraps ``.. needuml::`` with ``:config: sysml_act`` and the
    ``ACT_FULL_TEMPLATE`` body. Walks all ``Action`` needs whose
    ``definition`` equals the root, groups by ``partition`` into
    swimlane packages, and emits ``ControlFlow`` and ``ObjectFlow``
    arrows between them.
    """

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        "show-partitions": directives.unchanged,
        "scale": directives.unchanged,
        "align": directives.unchanged,
    }

    def run(self) -> list[Any]:
        root_id = self.arguments[0]
        show_partitions = self.options.get("show-partitions", "true").lower()
        scale = self.options.get("scale")
        align = self.options.get("align", "center")

        content = ACT_FULL_TEMPLATE.replace("{root_id}", root_id).replace(
            "{show_partitions}", "'" + show_partitions + "'"
        )

        from sphinx_needs.directives.needuml import NeedumlDirective

        content_list = StringList(content.splitlines(), source="needsysml-act")
        needuml = NeedumlDirective(
            name="needuml",
            arguments=[root_id],
            options={
                "config": "sysml_act",
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


class NeedsymlActSvgDirective(SphinxDirective):
    """Generate an activity diagram as inline SVG."""

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
        content = _substitute(ACT_SVG_TEMPLATE, root_id)
        return _emit_needsvg_node(self, content, width, align)


def setup(app: Sphinx) -> None:
    """Register the needsysml-act and needsysml-act-svg directives."""
    app.add_directive("needsysml-act", NeedsymlActDirective)
    app.add_directive("needsysml-act-svg", NeedsymlActSvgDirective)
