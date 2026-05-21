"""Tests for the needsysml-par directive (PlantUML + SVG variants)."""

import shutil
from pathlib import Path

import pytest


@pytest.fixture()
def par_app(make_app, tmp_path):
    """Build the par test fixture and return the Sphinx app."""
    srcdir = Path(__file__).parent / "doc_test" / "par"
    tmproot = tmp_path / "par"
    shutil.copytree(srcdir, tmproot)
    app = make_app(srcdir=tmproot)
    app.build()
    return app


class TestParDirective:
    """Smoke tests for the needsysml-par directive family."""

    def test_par_builds_without_error(self, par_app):
        """The fixture builds cleanly."""
        assert par_app is not None

    def test_par_root_id_in_rendered_html(self, par_app):
        """The root ConstraintBlock ID appears in the rendered HTML output."""
        html = (Path(par_app.outdir) / "index.html").read_text(encoding="utf-8")
        assert "CONSTRAINT-001" in html

    def test_par_bindings_registered(self, par_app):
        """All three fixture binding connectors are registered."""
        needs = par_app.env._needs_all_needs  # noqa: SLF001
        for bind_id in ("BIND-001", "BIND-002", "BIND-003"):
            assert bind_id in needs, f"binding {bind_id} not registered"

    def test_par_unit_field_readable(self, par_app):
        """The unit field is readable on BIND-001."""
        needs = par_app.env._needs_all_needs  # noqa: SLF001
        bind = needs.get("BIND-001")
        assert bind is not None
        assert bind.get("unit") == "kW"
