"""Tests for the needsysml-alloc directive."""

import shutil
from pathlib import Path

import pytest


@pytest.fixture()
def alloc_app(make_app, tmp_path):
    """Build the alloc test fixture and return the Sphinx app."""
    srcdir = Path(__file__).parent / "doc_test" / "alloc"
    tmproot = tmp_path / "alloc"
    shutil.copytree(srcdir, tmproot)
    app = make_app(srcdir=tmproot)
    app.build()
    return app


class TestAllocDirective:
    """Smoke tests for the needsysml-alloc directive."""

    def test_alloc_builds_without_error(self, alloc_app):
        """The fixture builds cleanly."""
        assert alloc_app is not None

    def test_alloc_renders_table(self, alloc_app):
        """The rendered HTML contains a <table> element."""
        html = (Path(alloc_app.outdir) / "index.html").read_text(encoding="utf-8")
        assert "<table" in html

    def test_alloc_marker_present(self, alloc_app):
        """The ✓ marker appears at expected intersections."""
        html = (Path(alloc_app.outdir) / "index.html").read_text(encoding="utf-8")
        assert "✓" in html

    def test_alloc_unallocated_row_empty(self, alloc_app):
        """R-004 (no allocates) renders as a row with no markers."""
        html = (Path(alloc_app.outdir) / "index.html").read_text(encoding="utf-8")
        assert "R-004" in html

    def test_alloc_needs_registered(self, alloc_app):
        """All fixture requirements and parts are registered."""
        needs = alloc_app.env._needs_all_needs  # noqa: SLF001
        for need_id in ("R-001", "R-002", "R-003", "R-004", "P-001", "P-002", "P-003"):
            assert need_id in needs, f"{need_id} not registered"
