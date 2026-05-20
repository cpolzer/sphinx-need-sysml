"""Tests for the needsysml-pkg directive (PlantUML + SVG variants)."""

import shutil
from pathlib import Path

import pytest


@pytest.fixture()
def pkg_app(make_app, tmp_path):
    """Build the pkg test fixture and return the Sphinx app."""
    srcdir = Path(__file__).parent / "doc_test" / "pkg"
    tmproot = tmp_path / "pkg"
    shutil.copytree(srcdir, tmproot)
    app = make_app(srcdir=tmproot)
    app.build()
    return app


class TestPkgDirective:
    """Smoke tests for the needsysml-pkg directive family."""

    def test_pkg_builds_without_error(self, pkg_app):
        """The fixture builds cleanly."""
        assert pkg_app is not None

    def test_pkg_root_id_in_rendered_html(self, pkg_app):
        """The root Package ID appears in the rendered HTML output."""
        html = (Path(pkg_app.outdir) / "index.html").read_text(encoding="utf-8")
        assert "PKG-001" in html

    def test_pkg_nested_packages_registered(self, pkg_app):
        """Child packages and dependencies are registered as needs."""
        needs = pkg_app.env._needs_all_needs  # noqa: SLF001
        for need_id in ("PKG-001", "PKG-002", "PKG-003", "DEP-001", "DEP-002"):
            assert need_id in needs, f"need {need_id} not registered"

    def test_pkg_parent_package_field(self, pkg_app):
        """Child packages reference their parent via parent_package."""
        needs = pkg_app.env._needs_all_needs  # noqa: SLF001
        pkg2 = needs.get("PKG-002")
        assert pkg2.get("parent_package") == "PKG-001"
        pkg3 = needs.get("PKG-003")
        assert pkg3.get("parent_package") == "PKG-001"

    def test_pkg_dependency_kind_field(self, pkg_app):
        """Dependency.kind enum values are honored."""
        needs = pkg_app.env._needs_all_needs  # noqa: SLF001
        d1 = needs.get("DEP-001")
        d2 = needs.get("DEP-002")
        assert d1.get("kind") == "use"
        assert d2.get("kind") == "import"
