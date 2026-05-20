"""Needsyml package diagram directive (PlantUML + SVG variants)."""

from typing import Any

from docutils.parsers.rst import directives
from docutils.statemachine import StringList
from sphinx.application import Sphinx
from sphinx.util.docutils import SphinxDirective

from sphinxcontrib.sysml.svg_templates import PKG_SVG_TEMPLATE
from sphinxcontrib.sysml.templates import PKG_FULL_TEMPLATE


class NeedsymlPkgDirective(SphinxDirective):
    """Generate a package diagram from a root Package need.

    Walks the package tree under the root via the ``parent_package``
    field, emits nested PlantUML ``package`` blocks, and draws
    ``Dependency`` arrows between any two packages in the rendered tree.
    """

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        "depth": directives.unchanged,
        "scale": directives.unchanged,
        "align": directives.unchanged,
    }

    def run(self) -> list[Any]:
        root_id = self.arguments[0]
        depth = self.options.get("depth", "3")
        scale = self.options.get("scale")
        align = self.options.get("align", "center")

        content = PKG_FULL_TEMPLATE.replace("{root_id}", root_id).replace(
            "{depth}", depth
        )

        from sphinx_needs.directives.needuml import NeedumlDirective

        content_list = StringList(content.splitlines(), source="needsysml-pkg")
        needuml = NeedumlDirective(
            name="needuml",
            arguments=[root_id],
            options={
                "config": "sysml_pkg",
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


class NeedsymlPkgSvgDirective(SphinxDirective):
    """Generate a package diagram as inline SVG."""

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
        content = _substitute(PKG_SVG_TEMPLATE, root_id)
        return _emit_needsvg_node(self, content, width, align)


def setup(app: Sphinx) -> None:
    """Register the needsysml-pkg and needsysml-pkg-svg directives."""
    app.add_directive("needsysml-pkg", NeedsymlPkgDirective)
    app.add_directive("needsysml-pkg-svg", NeedsymlPkgSvgDirective)
