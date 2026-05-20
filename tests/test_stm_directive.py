"""Tests for the needsysml-stm directive (PlantUML + SVG variants)."""

import shutil
from pathlib import Path

import pytest


@pytest.fixture()
def stm_app(make_app, tmp_path):
    """Build the stm test fixture and return the Sphinx app."""
    srcdir = Path(__file__).parent / "doc_test" / "stm"
    tmproot = tmp_path / "stm"
    shutil.copytree(srcdir, tmproot)
    app = make_app(srcdir=tmproot)
    app.build()
    return app


class TestStmDirective:
    """Smoke tests for the needsysml-stm directive family."""

    def test_stm_builds_without_error(self, stm_app):
        """The fixture builds cleanly."""
        assert stm_app is not None

    def test_stm_root_id_in_rendered_html(self, stm_app):
        """The root StateDef ID appears in the rendered HTML output."""
        html = (Path(stm_app.outdir) / "index.html").read_text(encoding="utf-8")
        assert "SD-001" in html

    def test_stm_transitions_registered(self, stm_app):
        """All four fixture transitions are registered as needs."""
        needs = stm_app.env._needs_all_needs  # noqa: SLF001
        for trans_id in ("TRANS-001", "TRANS-002", "TRANS-003", "TRANS-004"):
            assert trans_id in needs, f"transition {trans_id} not registered"

    def test_stm_pseudokind_field_readable(self, stm_app):
        """The pseudo_kind field is readable on the initial-state usage."""
        needs = stm_app.env._needs_all_needs  # noqa: SLF001
        off = needs.get("SU-001")
        assert off is not None
        assert off.get("pseudo_kind") == "initial"
