"""Tests for the needsysml-act directive (PlantUML + SVG variants)."""

import re
import shutil
from pathlib import Path

import pytest


@pytest.fixture()
def act_app(make_app, tmp_path):
    """Build the act test fixture and return the Sphinx app."""
    srcdir = Path(__file__).parent / "doc_test" / "act"
    tmproot = tmp_path / "act"
    shutil.copytree(srcdir, tmproot)
    app = make_app(srcdir=tmproot)
    app.build()
    return app


class TestActDirective:
    """Smoke tests for the needsysml-act directive family."""

    def test_act_builds_without_error(self, act_app):
        """The fixture builds cleanly."""
        assert act_app is not None

    def test_act_plantuml_renders_without_errors(self, act_app):
        """PlantUML diagram renders without syntax errors.

        Checks the rendered HTML for common PlantUML error indicators:
        - 'Syntax Error' text in plantuml output
        - 'ERROR' text in plantuml output
        - Tiny plantuml images (10x10px indicates failed rendering)
        """
        html = (Path(act_app.outdir) / "index.html").read_text(encoding="utf-8")

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

    def test_act_root_id_in_rendered_html(self, act_app):
        """The root ActionDef ID appears in the rendered HTML output."""
        html = (Path(act_app.outdir) / "index.html").read_text(encoding="utf-8")
        assert "AD-001" in html

    def test_act_controlflows_registered(self, act_app):
        """All seven fixture control flows are registered as needs."""
        needs = act_app.env._needs_all_needs  # noqa: SLF001
        for cf_id in (
            "CTRLFLOW-001",
            "CTRLFLOW-002",
            "CTRLFLOW-003",
            "CTRLFLOW-004",
            "CTRLFLOW-005",
            "CTRLFLOW-006",
            "CTRLFLOW-007",
        ):
            assert cf_id in needs, f"control flow {cf_id} not registered"

    def test_act_partition_field_readable(self, act_app):
        """The partition field is readable on action needs."""
        needs = act_app.env._needs_all_needs  # noqa: SLF001
        a001 = needs.get("A-001")
        assert a001 is not None
        assert a001.get("partition") == "Driver"

    def test_act_fork_action_has_activity_kind(self, act_app):
        """The fork action carries activity_kind='fork'."""
        needs = act_app.env._needs_all_needs  # noqa: SLF001
        fork = needs.get("A-004")
        assert fork is not None
        assert fork.get("activity_kind") == "fork"
