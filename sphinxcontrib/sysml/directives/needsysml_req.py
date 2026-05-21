"""Needsyml requirements diagram directive — wraps needuml with pre-baked REQ template."""

from typing import Any

from docutils.parsers.rst import directives
from docutils.statemachine import StringList
from sphinx.application import Sphinx
from sphinx.util.docutils import SphinxDirective

from sphinxcontrib.sysml.templates import REQ_FULL_TEMPLATE


class NeedsymlReqDirective(SphinxDirective):
    """Generate a requirements diagram for needs matching a filter expression.

    Wraps ``.. needuml::`` with ``:config: sysml_req`` and the
    ``REQ_FULL_TEMPLATE`` body.
    """

    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = True
    option_spec = {
        "filter": directives.unchanged,
        "show-satisfy": directives.unchanged,
        "show-refine": directives.unchanged,
        "show-allocate": directives.unchanged,
        "scale": directives.unchanged,
        "align": directives.unchanged,
    }

    def run(self) -> list[Any]:
        # Resolution order: positional argument (legacy) → :filter: option →
        # default 'type == "Requirement"'.
        if self.arguments:
            filter_expr = self.arguments[0]
        else:
            filter_expr = self.options.get("filter", "type == 'Requirement'")
        show_satisfy = self.options.get("show-satisfy", "true").lower() == "true"
        show_refine = self.options.get("show-refine", "true").lower() == "true"
        show_allocate = self.options.get("show-allocate", "true").lower() == "true"
        scale = self.options.get("scale")
        align = self.options.get("align", "center")

        # Render the REQ template with context variables
        content = (
            REQ_FULL_TEMPLATE.replace("{filter_expr}", filter_expr)
            .replace("{show_satisfy}", str(show_satisfy).lower())
            .replace("{show_refine}", str(show_refine).lower())
            .replace("{show_allocate}", str(show_allocate).lower())
        )

        from sphinx_needs.directives.needuml import NeedumlDirective

        content_list = StringList(content.splitlines(), source="needsysml-req")
        needuml = NeedumlDirective(
            name="needuml",
            arguments=[filter_expr],
            options={
                "config": "sysml_req",
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
    """Register the needsysml-req directive."""
    app.add_directive("needsysml-req", NeedsymlReqDirective)
