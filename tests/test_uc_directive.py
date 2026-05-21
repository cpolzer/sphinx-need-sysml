"""Tests for the needsysml-uc directive (PlantUML + SVG variants)."""

import re
import shutil
from pathlib import Path

import pytest


@pytest.fixture()
def uc_app(make_app, tmp_path):
    """Build the uc test fixture and return the Sphinx app."""
    srcdir = Path(__file__).parent / "doc_test" / "uc"
    tmproot = tmp_path / "uc"
    shutil.copytree(srcdir, tmproot)
    app = make_app(srcdir=tmproot)
    app.build()
    return app


class TestUcDirective:
    """Smoke tests for the needsysml-uc directive family."""

    def test_uc_builds_without_error(self, uc_app):
        """The fixture builds cleanly."""
        assert uc_app is not None

    def test_uc_plantuml_renders_without_errors(self, uc_app):
        """PlantUML diagram renders without syntax errors.

        Checks the rendered HTML for common PlantUML error indicators:
        - 'Syntax Error' text in plantuml output
        - 'ERROR' text in plantuml output
        - Tiny plantuml images (10x10px indicates failed rendering)
        """
        html = (Path(uc_app.outdir) / "index.html").read_text(encoding="utf-8")

        # Check for error text in plantuml sections
        error_patterns = [
            r'class="plantuml"[^>]*>.*?Syntax Error',
            r'class="plantuml"[^>]*>.*?ERROR',
        ]
        for pattern in error_patterns:
            match = re.search(pattern, html, re.DOTALL | re.IGNORECASE)
            assert not match, f"PlantUML error found in HTML: {match.group(0)[:200]}"

        # Check for tiny plantuml images (failed renders are often 10x10px)
        tiny_img = re.search(
            r'<img[^>]*plantuml[^>]*style="width:\s*10px[^>]*>', html, re.IGNORECASE
        )
        assert not tiny_img, "Found 10px PlantUML image (indicates render failure)"

    def test_uc_ids_in_rendered_html(self, uc_app):
        """Use case and actor IDs appear in the rendered HTML."""
        html = (Path(uc_app.outdir) / "index.html").read_text(encoding="utf-8")
        assert "USECASE-001" in html
        assert "ACTOR-001" in html

    def test_uc_extends_and_includes_registered(self, uc_app):
        """The extends and includes fields are readable on UseCases."""
        needs = uc_app.env._needs_all_needs  # noqa: SLF001
        uc2 = needs.get("USECASE-002")
        assert uc2 is not None
        assert uc2.get("extends") == "USECASE-001"
        uc4 = needs.get("USECASE-004")
        assert uc4 is not None
        assert uc4.get("includes") == "USECASE-003"

    def test_uc_actor_interacts_with(self, uc_app):
        """Actors carry their interacts_with field per finding U1."""
        needs = uc_app.env._needs_all_needs  # noqa: SLF001
        driver = needs.get("ACTOR-001")
        assert driver is not None
        assert driver.get("interacts_with") == "USECASE-001"
        mechanic = needs.get("ACTOR-002")
        assert mechanic is not None
        assert "USECASE-002" in mechanic.get("interacts_with", "")
        assert "USECASE-003" in mechanic.get("interacts_with", "")

    def test_uc_subject_field(self, uc_app):
        """All use cases share subject='Vehicle'."""
        needs = uc_app.env._needs_all_needs  # noqa: SLF001
        for uc_id in ("USECASE-001", "USECASE-002", "USECASE-003", "USECASE-004"):
            uc = needs.get(uc_id)
            assert uc.get("subject") == "Vehicle"
