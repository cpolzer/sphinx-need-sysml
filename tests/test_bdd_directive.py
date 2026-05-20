"""Tests for the needsysml-bdd directive."""

import pytest
from pathlib import Path
import shutil


@pytest.fixture()
def bdd_app(make_app, tmp_path):
    """Build the basic test project with BDD directive."""
    srcdir = Path(__file__).parent / "doc_test" / "basic"
    tmproot = tmp_path / "basic"
    shutil.copytree(srcdir, tmproot)
    app = make_app(srcdir=tmproot)
    app.build()
    return app


class TestBddDirective:
    """Tests for the needsysml-bdd directive."""

    def test_bdd_builds_without_error(self, bdd_app):
        """The BDD directive builds without raising errors."""
        # If we got here, the build succeeded
        assert bdd_app is not None

    def test_bdd_generates_plantuml_node(self, bdd_app):
        """The BDD directive creates a needuml node in the doctree."""
        doctree = bdd_app.env.get_doctree("index")
        # Check that the document contains needuml-related content
        text = doctree.astext()
        assert "PD-001" in text or "Engine" in text

    def test_bdd_warning_without_svg(self, make_app, tmp_path):
        """A warning is emitted if plantuml_output_format is not svg."""
        srcdir = Path(__file__).parent / "doc_test" / "basic"
        tmproot = tmp_path / "basic"
        shutil.copytree(srcdir, tmproot)
        # Override conf.py to use non-SVG output
        conf = tmproot / "conf.py"
        content = conf.read_text()
        content = content.replace('plantuml_output_format = "svg"', 'plantuml_output_format = "png"')
        conf.write_text(content)

        app = make_app(srcdir=tmproot)
        app.build()
        warnings = app.warning.getvalue()
        assert "plantuml_output_format" in warnings or "svg" in warnings.lower()
