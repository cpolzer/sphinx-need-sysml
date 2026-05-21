"""Needsyml allocation matrix directive — renders a requirement-to-part traceability table."""

from typing import Any

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.addnodes import pending_xref
from sphinx.application import Sphinx
from sphinx.util.docutils import SphinxDirective
from sphinx_needs.config import NeedsSphinxConfig
from sphinx_needs.data import SphinxNeedsData
from sphinx_needs.filter_common import filter_needs


class NeedsymlAllocDirective(SphinxDirective):
    """Generate an allocation matrix table.

    Rows are needs matching the ``:rows:`` filter (default: needs with
    non-empty ``allocates``). Columns are the unique part IDs referenced
    by those rows' ``allocates`` fields, optionally filtered by
    ``:columns:``. A marker (default ``✓``) is placed at each allocated
    intersection.
    """

    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        "rows": directives.unchanged,
        "columns": directives.unchanged,
        "marker": directives.unchanged,
    }

    def run(self) -> list[Any]:
        env = self.env
        needs_data = SphinxNeedsData(env)
        all_needs = needs_data._env_needs  # noqa: SLF001
        config = NeedsSphinxConfig(self.config)

        rows_filter = self.options.get("rows", 'allocates != ""')
        columns_filter = self.options.get("columns", None)
        marker = self.options.get("marker", "✓")

        # Evaluate rows filter against all needs
        row_needs = filter_needs(all_needs.values(), config, rows_filter, location=self)

        # Collect column IDs from allocates fields of row needs
        col_ids: set[str] = set()
        for need in row_needs:
            allocates = need.get("allocates", "")
            if allocates:
                for aid in allocates.split(","):
                    aid = aid.strip()
                    if aid:
                        col_ids.add(aid)

        # Filter columns if a columns_filter is provided
        if columns_filter:
            col_needs = filter_needs(
                [all_needs[cid] for cid in col_ids if cid in all_needs],
                config,
                columns_filter,
                location=self,
            )
            col_ids = {n["id"] for n in col_needs}

        # Sort for deterministic output
        sorted_col_ids = sorted(col_ids)
        sorted_row_needs = sorted(row_needs, key=lambda n: n["id"])

        # Handle empty result
        if not sorted_row_needs or not sorted_col_ids:
            from sphinxcontrib.sysml.warnings import warn_empty

            placeholder = warn_empty(self.env.app, env.docname, self.lineno, "alloc")
            return [nodes.paragraph("", placeholder)]

        # Build the table
        table = nodes.table(classes=["needsysml-alloc-matrix"])
        tgroup = nodes.tgroup(cols=1 + len(sorted_col_ids))

        # Column specs: first column (row headers) wider, rest equal
        tgroup += nodes.colspec(colwidth=3)
        for _ in sorted_col_ids:
            tgroup += nodes.colspec(colwidth=1)

        # Header row
        header_row = nodes.row()
        header_row += nodes.entry("", nodes.paragraph("", ""))
        for col_id in sorted_col_ids:
            col_need = all_needs.get(col_id)
            if col_need:
                cell = nodes.entry()
                cell += _make_need_ref(col_need, env.docname)
                header_row += cell
            else:
                header_row += nodes.entry("", nodes.paragraph("", col_id))
        tgroup += nodes.thead("", header_row)

        # Body rows
        tbody = nodes.tbody()
        for row_need in sorted_row_needs:
            row = nodes.row()

            # Row header: link to the need
            row += nodes.entry("", _make_need_ref(row_need, env.docname))

            # Marker cells
            row_allocates = set()
            allocates = row_need.get("allocates", "")
            if allocates:
                for aid in allocates.split(","):
                    aid = aid.strip()
                    if aid:
                        row_allocates.add(aid)

            for col_id in sorted_col_ids:
                cell = nodes.entry()
                if col_id in row_allocates:
                    cell += nodes.paragraph("", marker)
                else:
                    cell += nodes.paragraph("", "")
                row += cell

            tbody += row

        tgroup += tbody
        table += tgroup
        table.line = self.lineno

        return [table]


def _make_need_ref(need_info: dict[str, Any], docname: str) -> nodes.paragraph:
    """Create a paragraph with a pending cross-reference to the given need."""
    para = nodes.paragraph()
    ref = pending_xref(
        "",
        nodes.Text(need_info["id"]),
        refdomain="need",
        reftype="need",
        reftarget=need_info["id"],
        refexplicit=False,
        refdoc=docname,
    )
    para += ref
    return para


def setup(app: Sphinx) -> None:
    """Register the needsysml-alloc directive."""
    app.add_directive("needsysml-alloc", NeedsymlAllocDirective)
