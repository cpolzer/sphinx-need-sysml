"""Needsyml state-machine directive (PlantUML + SVG variants)."""

from typing import Any

from docutils.parsers.rst import directives
from docutils.statemachine import StringList
from sphinx.application import Sphinx
from sphinx.util.docutils import SphinxDirective

from sphinx_need_sysml.svg_templates import STM_SVG_TEMPLATE
from sphinx_need_sysml.templates import STM_FULL_TEMPLATE


class NeedsymlStmDirective(SphinxDirective):
    """Generate a state machine diagram for a given StateDef.

    Wraps ``.. needuml::`` with ``:config: sysml_stm`` and the
    ``STM_FULL_TEMPLATE`` body. Walks all ``StateUsage`` needs whose
    ``definition`` equals the root and emits their ``Transition`` edges
    with PlantUML state-diagram syntax.
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

        content = STM_FULL_TEMPLATE.replace("{root_id}", root_id)

        from sphinx_needs.directives.needuml import NeedumlDirective

        content_list = StringList(content.splitlines(), source="needsysml-stm")
        needuml = NeedumlDirective(
            name="needuml",
            arguments=[],
            options={
                "config": "sysml_stm",
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


class NeedsymlStmSvgDirective(SphinxDirective):
    """Generate a state machine diagram as inline SVG."""

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        "align": directives.unchanged,
        "width": directives.unchanged,
    }

    def run(self) -> list[Any]:
        from sphinx_need_sysml.directives.needsysml_svg import (
            _emit_needsvg_node,
            _substitute,
        )

        root_id = self.arguments[0]
        align = self.options.get("align", "center")
        width = self.options.get("width", "100%")
        content = _substitute(STM_SVG_TEMPLATE, root_id)
        return _emit_needsvg_node(self, content, width, align)


def setup(app: Sphinx) -> None:
    """Register the needsysml-stm and needsysml-stm-svg directives."""
    app.add_directive("needsysml-stm", NeedsymlStmDirective)
    app.add_directive("needsysml-stm-svg", NeedsymlStmSvgDirective)
