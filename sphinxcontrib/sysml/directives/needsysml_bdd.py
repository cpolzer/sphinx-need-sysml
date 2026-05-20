"""Needsyml BDD directive — wraps needuml with pre-baked BDD template."""

from docutils.parsers.rst import directives
from docutils.statemachine import StringList
from sphinx.application import Sphinx
from sphinx.util.docutils import SphinxDirective

from sphinxcontrib.sysml.templates import BDD_FULL_TEMPLATE


class NeedsymlBddDirective(SphinxDirective):
    """Generate a Block Definition Diagram for a given PartDef need.

    Wraps ``.. needuml::`` with ``:config: sysml_bdd`` and the
    ``BDD_FULL_TEMPLATE`` body.
    """

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        "depth": directives.unchanged,
        "filter": directives.unchanged,
        "scale": directives.unchanged,
        "align": directives.unchanged,
    }

    def run(self):
        root_id = self.arguments[0]
        depth = self.options.get("depth", "2")
        custom_filter = self.options.get("filter")
        scale = self.options.get("scale")
        align = self.options.get("align", "center")

        # Build the filter expression for child parts
        if custom_filter:
            child_filter = custom_filter
        else:
            child_filter = f"type == 'Part' and owned_by == '{root_id}'"

        # Render the BDD template with context variables
        content = BDD_FULL_TEMPLATE.replace("{root_id}", root_id).replace(
            "{depth}", depth
        )

        # Create needuml directive options
        from sphinx_needs.directives.needuml import NeedumlDirective

        # Create and configure a NeedumlDirective instance
        content_list = StringList(content.splitlines(), source="needsysml-bdd")
        needuml = NeedumlDirective(
            name="needuml",
            arguments=[root_id],
            options={
                "config": "sysml_bdd",
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

        return needuml.run()


def setup(app: Sphinx) -> None:
    """Register the needsysml-bdd directive."""
    app.add_directive("needsysml-bdd", NeedsymlBddDirective)
