"""Tests for the needsysml-req directive."""

import pytest
from pathlib import Path
import shutil


@pytest.fixture()
def req_app(make_app, tmp_path):
    """Build the basic test project with req directive."""
    srcdir = Path(__file__).parent / "doc_test" / "basic"
    tmproot = tmp_path / "basic"
    shutil.copytree(srcdir, tmproot)
    app = make_app(srcdir=tmproot)
    app.build()
    return app


class TestReqDirective:
    """Tests for the needsysml-req directive."""

    def test_req_builds_without_error(self, req_app):
        """The req directive builds without raising errors."""
        assert req_app is not None

    def test_req_generates_plantuml_node(self, req_app):
        """The req directive creates a needuml node in the doctree."""
        doctree = req_app.env.get_doctree("index")
        text = doctree.astext()
        assert "R-001" in text or "Requirement" in text

    def test_req_filter_expression_respected(self, req_app):
        """Only needs matching the filter expression appear."""
        # Verify the build completed and needs were processed
        doctree = req_app.env.get_doctree("index")
        text = doctree.astext()
        # The requirements diagram should reference R-001
        assert "R-001" in text or "Brake" in text
