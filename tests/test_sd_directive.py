"""Tests for the needsysml-sd directive (PlantUML + SVG variants)."""

import re
import shutil
from pathlib import Path

import pytest


@pytest.fixture()
def sd_app(make_app, tmp_path):
    """Build the sd test fixture and return the Sphinx app."""
    srcdir = Path(__file__).parent / "doc_test" / "sd"
    tmproot = tmp_path / "sd"
    shutil.copytree(srcdir, tmproot)
    app = make_app(srcdir=tmproot)
    app.build()
    return app


class TestSdDirective:
    """Smoke tests for the needsysml-sd directive family."""

    def test_sd_builds_without_error(self, sd_app):
        """The fixture builds cleanly."""
        assert sd_app is not None

    def test_sd_plantuml_renders_without_errors(self, sd_app):
        """PlantUML diagram renders without syntax errors.

        Checks the rendered HTML for common PlantUML error indicators:
        - 'Syntax Error' text in plantuml output
        - 'ERROR' text in plantuml output
        - Tiny plantuml images (10x10px indicates failed rendering)
        """
        html = (Path(sd_app.outdir) / "index.html").read_text(encoding="utf-8")

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

    def test_sd_root_id_in_rendered_html(self, sd_app):
        """The interaction-definition ID appears in the rendered HTML."""
        html = (Path(sd_app.outdir) / "index.html").read_text(encoding="utf-8")
        assert "AD-001" in html

    def test_sd_messages_registered(self, sd_app):
        """All four fixture messages are registered as needs."""
        needs = sd_app.env._needs_all_needs  # noqa: SLF001
        for msg_id in ("MSG-001", "MSG-002", "MSG-003", "MSG-004"):
            assert msg_id in needs, f"message {msg_id} not registered"

    def test_sd_message_kinds_readable(self, sd_app):
        """The message_kind field is readable on every message."""
        needs = sd_app.env._needs_all_needs  # noqa: SLF001
        assert needs.get("MSG-001").get("message_kind") == "sync"
        assert needs.get("MSG-002").get("message_kind") == "async"
        assert needs.get("MSG-003").get("message_kind") == "return"

    def test_sd_fragment_group_readable(self, sd_app):
        """Messages carry their fragment_group and fragment_kind."""
        needs = sd_app.env._needs_all_needs  # noqa: SLF001
        m2 = needs.get("MSG-002")
        assert m2.get("fragment_group") == "F1"
        assert m2.get("fragment_kind") == "alt"
        assert "key_position" in m2.get("fragment_guard", "")
