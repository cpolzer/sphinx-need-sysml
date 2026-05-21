"""Tests for the needsysml-pkg directive (PlantUML + SVG variants)."""

import re
import shutil
from pathlib import Path

import pytest

try:
    from playwright.sync_api import sync_playwright

    _HAS_PLAYWRIGHT = True
except ImportError:
    _HAS_PLAYWRIGHT = False


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

    def test_pkg_svg_dependency_lines_connect_borders(self, pkg_app):
        """Dependency line endpoints connect package rectangle borders.

        Parses the rendered SVG and verifies that each <line> element's
        endpoints (x1,y1) and (x2,y2) fall within the bounding rectangles
        of their source and target packages — not at center points or
        arbitrary offsets. Regression test for the bug where lines
        floated from center points to arbitrary y-coordinates.
        """
        html = (Path(pkg_app.outdir) / "index.html").read_text(encoding="utf-8")

        # Find the needsysml-pkg-svg SVG (contains stroke-dasharray dependency lines)
        svg_matches = re.findall(r"<svg[^>]*>.*?</svg>", html, re.DOTALL)
        pkg_svg = None
        for svg in svg_matches:
            if "stroke-dasharray" in svg and "dependency" not in svg.lower():
                # The SVG template uses stroke-dasharray for dependency lines
                pkg_svg = svg
                break
        assert pkg_svg, "No needsysml-pkg-svg found in rendered output"

        # Extract package rect positions: x, y, width, height
        rects = {}
        for m in re.finditer(
            r'<rect\s+x="(\d+)"\s+y="(\d+)"\s+width="(\d+)"\s+height="(\d+)"', pkg_svg
        ):
            x, y, w, h = (
                int(m.group(1)),
                int(m.group(2)),
                int(m.group(3)),
                int(m.group(4)),
            )
            # Skip the root package rect (y=20, h=340)
            if y == 20 and h == 340:
                continue
            rects[(x, y, w, h)] = {"x": x, "y": y, "w": w, "h": h}

        # Extract dependency lines (exclude tiny decorative lines)
        lines = re.findall(
            r'<line\s+x1="(\d+)"\s+y1="(\d+)"\s+x2="(\d+)"\s+y2="(\d+)"', pkg_svg
        )
        dep_lines = [
            (int(x1), int(y1), int(x2), int(y2))
            for x1, y1, x2, y2 in lines
            if abs(int(x2) - int(x1)) > 10  # Filter out tiny decorative lines
        ]
        assert len(dep_lines) >= 2, (
            f"Expected at least 2 dependency lines, found {len(dep_lines)}"
        )

        for x1, y1, x2, y2 in dep_lines:

            def on_border(px, py, rect):
                rx, ry, rw, rh = rect["x"], rect["y"], rect["w"], rect["h"]
                tolerance = 5
                on_left = abs(px - rx) <= tolerance and ry <= py <= ry + rh
                on_right = abs(px - (rx + rw)) <= tolerance and ry <= py <= ry + rh
                on_top = abs(py - ry) <= tolerance and rx <= px <= rx + rw
                on_bottom = abs(py - (ry + rh)) <= tolerance and rx <= px <= rx + rw
                return on_left or on_right or on_top or on_bottom

            src_on_border = any(on_border(x1, y1, r) for r in rects.values())
            dst_on_border = any(on_border(x2, y2, r) for r in rects.values())
            assert src_on_border, f"Line start ({x1},{y1}) not on any package border"
            assert dst_on_border, f"Line end ({x2},{y2}) not on any package border"

    def test_pkg_svg_rect_layout_unchanged(self, pkg_app):
        """Package rectangle attributes retain original layout values.

        Confirms FR-005: the fix to dependency line positioning does not
        alter the rectangle layout (y="80", height="220").
        """
        html = (Path(pkg_app.outdir) / "index.html").read_text(encoding="utf-8")
        svg_matches = re.findall(r"<svg[^>]*>.*?</svg>", html, re.DOTALL)
        pkg_svg = None
        for svg in svg_matches:
            if "stroke-dasharray" in svg:
                pkg_svg = svg
                break
        assert pkg_svg, "No needsysml-pkg-svg found in rendered output"

        rects = re.findall(
            r'<rect\s+x="(\d+)"\s+y="(\d+)"\s+width="(\d+)"\s+height="(\d+)"', pkg_svg
        )
        # Filter out the root package rect (y="20", height="340")
        child_rects = [
            (x, y, w, h) for x, y, w, h in rects if int(y) == 80 and int(h) == 220
        ]
        assert len(child_rects) >= 2, (
            f"Expected at least 2 child rects with y=80, h=220; found {len(child_rects)}"
        )

    @pytest.mark.skipif(not _HAS_PLAYWRIGHT, reason="playwright not installed")
    def test_pkg_svg_renders_in_browser(self, pkg_app, tmp_path):
        """Package Diagram SVG renders visibly in a headless browser.

        Uses Playwright to load the built HTML, find the needsysml-pkg-svg
        section, and screenshot it. Verifies:
        - The SVG element is visible and has non-zero dimensions
        - Package rects and dependency lines are present in the DOM
        - Screenshot is saved for visual inspection (tests/doc_test/pkg/)
        """
        html_path = Path(pkg_app.outdir) / "index.html"
        screenshot_path = tmp_path / "pkg-svg-rendered.png"

        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            page = browser.new_page()
            page.goto(f"file://{html_path}")
            page.wait_for_load_state("networkidle")

            # Find all SVGs and locate the pkg-svg one
            svgs = page.query_selector_all("svg")
            pkg_svg = None
            for svg in svgs:
                inner = svg.inner_html()
                if "stroke-dasharray" in inner and "PKG-001" in inner:
                    pkg_svg = svg
                    break

            assert pkg_svg, "No needsysml-pkg-svg found in browser render"

            # Verify SVG has non-zero bounding box
            bbox = pkg_svg.bounding_box()
            assert bbox is not None, "SVG has no bounding box"
            assert bbox["width"] > 0, "SVG width is 0"
            assert bbox["height"] > 0, "SVG height is 0"

            # Verify expected elements are present
            text_content = pkg_svg.text_content()
            assert "PKG-001" in text_content, "Root package ID not visible"
            assert "PKG-002" in text_content or "Powertrain" in text_content, (
                "Child package not visible"
            )

            # Screenshot for visual inspection
            pkg_svg.screenshot(path=str(screenshot_path))
            assert screenshot_path.exists(), "Screenshot was not saved"

            browser.close()
