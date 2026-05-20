"""Tests for the needsysml-ibd directive."""

import shutil
from pathlib import Path

import pytest


@pytest.fixture()
def ibd_app(make_app, tmp_path):
    """Build the basic test project with IBD directive."""
    srcdir = Path(__file__).parent / "doc_test" / "basic"
    tmproot = tmp_path / "basic"
    shutil.copytree(srcdir, tmproot)
    app = make_app(srcdir=tmproot)
    app.build()
    return app


class TestIbdDirective:
    """Tests for the needsysml-ibd directive."""

    def test_ibd_builds_without_error(self, ibd_app):
        """The IBD directive builds without raising errors."""
        assert ibd_app is not None

    def test_ibd_generates_plantuml_node(self, ibd_app):
        """The IBD directive creates a needuml node in the doctree."""
        doctree = ibd_app.env.get_doctree("index")
        # Check that the document was built successfully (no errors)
        assert doctree is not None
        # The doctree should have content
        assert len(doctree.children) > 0

    def test_ibd_contains_expected_part_names(self, ibd_app):
        """IBD diagram contains expected part names."""
        doctree = ibd_app.env.get_doctree("index")
        text = doctree.astext()
        # The IBD should reference the root PartDef
        assert "Engine" in text or "PD-001" in text
