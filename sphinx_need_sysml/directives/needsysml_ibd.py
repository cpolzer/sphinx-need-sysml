"""Needsyml IBD directive — wraps needuml with pre-baked IBD template."""

from typing import Any

from docutils.parsers.rst import directives
from docutils.statemachine import StringList
from sphinx.application import Sphinx
from sphinx.util.docutils import SphinxDirective

from sphinx_need_sysml.templates import IBD_FULL_TEMPLATE


class NeedsymlIbdDirective(SphinxDirective):
    """Generate an Internal Block Diagram for a given PartDef need.

    Wraps ``.. needuml::`` with ``:config: sysml_ibd`` and the
    ``IBD_FULL_TEMPLATE`` body.

    Note: IBD diagrams are approximations using PlantUML component diagram
    syntax. Port placement is not locked to specific block edges.
    """

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        "show-ports": directives.unchanged,
        "scale": directives.unchanged,
        "align": directives.unchanged,
    }

    def run(self) -> list[Any]:
        root_id = self.arguments[0]
        scale = self.options.get("scale")
        align = self.options.get("align", "center")

        # Render the IBD template with context variables
        content = IBD_FULL_TEMPLATE.replace("{root_id}", root_id)

        from sphinx_needs.directives.needuml import NeedumlDirective

        content_list = StringList(content.splitlines(), source="needsysml-ibd")
        needuml = NeedumlDirective(
            name="needuml",
            arguments=[],
            options={
                "config": "sysml_ibd",
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


def setup(app: Sphinx) -> None:
    """Register the needsysml-ibd directive."""
    app.add_directive("needsysml-ibd", NeedsymlIbdDirective)
