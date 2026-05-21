"""Tests for the needsysml-stm directive (PlantUML + SVG variants)."""

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

    def test_stm_plantuml_renders_without_errors(self, stm_app):
        """PlantUML diagram renders without syntax errors.

        Checks the rendered HTML for common PlantUML error indicators:
        - 'Syntax Error' text in plantuml output
        - 'ERROR' text in plantuml output
        - Tiny plantuml images (10x10px indicates failed rendering)
        """
        html = (Path(stm_app.outdir) / "index.html").read_text(encoding="utf-8")

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

    def test_stm_svg_transition_lines_connect_borders(self, stm_app):
        """Transition line endpoints connect state shape borders.

        Parses the rendered SVG and verifies that each <line> element's
        endpoints fall on or near the bounding shapes of their source and
        target states — not at center points or arbitrary offsets.
        Regression test for the bug where lines floated from center points
        to arbitrary y-coordinates and labels overlapped.
        """
        html = (Path(stm_app.outdir) / "index.html").read_text(encoding="utf-8")

        # Find the needsysml-stm-svg SVG (720x320 viewBox, contains state shapes)
        svg_matches = re.findall(r"<svg[^>]*>.*?</svg>", html, re.DOTALL)
        stm_svg = None
        for svg in svg_matches:
            if 'viewBox="0 0 720 320"' in svg and "SU-001" in svg:
                stm_svg = svg
                break
        assert stm_svg, "No needsysml-stm-svg found in rendered output"

        # Extract state positions from the SVG
        # Regular states: rect elements with rx="8"
        rects = {}
        for m in re.finditer(
            r'<rect\s+x="([^"]+)"\s+y="([^"]+)"\s+width="([^"]+)"\s+height="([^"]+)"[^>]*rx="8"',
            stm_svg,
        ):
            x, y, w, h = (
                float(m.group(1)),
                float(m.group(2)),
                float(m.group(3)),
                float(m.group(4)),
            )
            rects[(x, y, w, h)] = {"x": x, "y": y, "w": w, "h": h}

        # Also capture circles (pseudostates)
        circles = []
        for m in re.finditer(
            r'<circle\s+cx="([^"]+)"\s+cy="([^"]+)"\s+r="([^"]+)"', stm_svg
        ):
            cx, cy, r = float(m.group(1)), float(m.group(2)), float(m.group(3))
            circles.append({"cx": cx, "cy": cy, "r": r})

        # Extract transition lines (exclude tiny decorative lines)
        lines = re.findall(
            r'<line\s+x1="([^"]+)"\s+y1="([^"]+)"\s+x2="([^"]+)"\s+y2="([^"]+)"',
            stm_svg,
        )
        trans_lines = [
            (float(x1), float(y1), float(x2), float(y2))
            for x1, y1, x2, y2 in lines
            if abs(float(x2) - float(x1)) > 10 or abs(float(y2) - float(y1)) > 10
        ]
        assert len(trans_lines) >= 2, (
            f"Expected at least 2 transition lines, found {len(trans_lines)}"
        )

        def on_or_near_shape(px, py, tolerance=30):
            """Check if point is on or near any state shape border."""
            for r in rects.values():
                rx, ry, rw, rh = r["x"], r["y"], r["w"], r["h"]
                on_left = abs(px - rx) <= tolerance and ry <= py <= ry + rh
                on_right = abs(px - (rx + rw)) <= tolerance and ry <= py <= ry + rh
                on_top = abs(py - ry) <= tolerance and rx <= px <= rx + rw
                on_bottom = abs(py - (ry + rh)) <= tolerance and rx <= px <= rx + rw
                if on_left or on_right or on_top or on_bottom:
                    return True
            for c in circles:
                dist = ((px - c["cx"]) ** 2 + (py - c["cy"]) ** 2) ** 0.5
                if abs(dist - c["r"]) <= tolerance:
                    return True
            return False

        for x1, y1, x2, y2 in trans_lines:
            src_on_border = on_or_near_shape(x1, y1)
            dst_on_border = on_or_near_shape(x2, y2)
            assert src_on_border, f"Line start ({x1},{y1}) not on any state border"
            assert dst_on_border, f"Line end ({x2},{y2}) not on any state border"

    def test_stm_svg_state_layout_unchanged(self, stm_app):
        """State rectangle attributes retain original layout values.

        Confirms that the fix to transition line positioning does not
        alter the state rectangle layout (y=90 or y=230, height=40).
        """
        html = (Path(stm_app.outdir) / "index.html").read_text(encoding="utf-8")
        svg_matches = re.findall(r"<svg[^>]*>.*?</svg>", html, re.DOTALL)
        stm_svg = None
        for svg in svg_matches:
            if 'viewBox="0 0 720 320"' in svg and "SU-001" in svg:
                stm_svg = svg
                break
        assert stm_svg, "No needsysml-stm-svg found in rendered output"

        rects = re.findall(
            r'<rect\s+x="([^"]+)"\s+y="([^"]+)"\s+width="([^"]+)"\s+height="([^"]+)"[^>]*rx="8"',
            stm_svg,
        )
        # Filter for state rects (y=90 or y=230, height=40)
        state_rects = [
            (x, y, w, h)
            for x, y, w, h in rects
            if (abs(float(y) - 90) < 1 or abs(float(y) - 230) < 1)
            and abs(float(h) - 40) < 1
        ]
        assert len(state_rects) >= 2, (
            f"Expected at least 2 state rects; found {len(state_rects)}"
        )

    def test_stm_svg_labels_not_overlapping(self, stm_app):
        """Transition labels are positioned with offsets to avoid overlap.

        Verifies that when multiple transitions exist, their labels are
        not rendered at identical positions.
        """
        html = (Path(stm_app.outdir) / "index.html").read_text(encoding="utf-8")
        svg_matches = re.findall(r"<svg[^>]*>.*?</svg>", html, re.DOTALL)
        stm_svg = None
        for svg in svg_matches:
            if 'viewBox="0 0 720 320"' in svg and "SU-001" in svg:
                stm_svg = svg
                break
        assert stm_svg, "No needsysml-stm-svg found in rendered output"

        # Extract text elements that are transition labels (not ID labels)
        # Labels are positioned near the middle of lines, not at state positions
        texts = re.findall(
            r'<text\s+x="([^"]+)"\s+y="([^"]+)"[^>]*>([^<]+)</text>', stm_svg
        )
        # Filter for labels (not monospace ID labels at state positions)
        label_positions = []
        for x, y, content in texts:
            content = content.strip()
            # Skip empty or very short labels
            if len(content) > 2 and "SU-" not in content:
                label_positions.append((float(x), float(y), content))

        # Check that no two labels are at the same position
        positions_seen = set()
        for x, y, content in label_positions:
            pos_key = (round(x), round(y))
            assert pos_key not in positions_seen, (
                f"Duplicate label position ({x}, {y}) for '{content}'"
            )
            positions_seen.add(pos_key)

    @pytest.mark.skipif(not _HAS_PLAYWRIGHT, reason="playwright not installed")
    def test_stm_svg_renders_in_browser(self, stm_app, tmp_path):
        """State Machine Diagram SVG renders visibly in a headless browser.

        Uses Playwright to load the built HTML, find the needsysml-stm-svg
        section, and screenshot it. Verifies:
        - The SVG element is visible and has non-zero dimensions
        - State shapes and transition lines are present in the DOM
        - Screenshot is saved for visual inspection (tests/doc_test/stm/)
        """
        html_path = Path(stm_app.outdir) / "index.html"
        screenshot_path = tmp_path / "stm-svg-rendered.png"

        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            page = browser.new_page()
            page.goto(f"file://{html_path}")
            page.wait_for_load_state("networkidle")

            # Find all SVGs and locate the stm-svg one
            svgs = page.query_selector_all("svg")
            stm_svg = None
            for svg in svgs:
                view_box = svg.get_attribute("viewBox") or ""
                if "720 320" in view_box:
                    inner = svg.inner_html()
                    if "SU-001" in inner:
                        stm_svg = svg
                        break

            assert stm_svg, "No needsysml-stm-svg found in browser render"

            # Verify SVG has non-zero bounding box
            bbox = stm_svg.bounding_box()
            assert bbox is not None, "SVG has no bounding box"
            assert bbox["width"] > 0, "SVG width is 0"
            assert bbox["height"] > 0, "SVG height is 0"

            # Verify expected elements are present
            text_content = stm_svg.text_content()
            assert "SD-001" in text_content or "SU-001" in text_content, (
                "State IDs not visible"
            )
            assert "starting" in text_content or "running" in text_content, (
                "State titles not visible"
            )

            # Screenshot for visual inspection
            stm_svg.screenshot(path=str(screenshot_path))
            assert screenshot_path.exists(), "Screenshot was not saved"

            browser.close()

    @pytest.mark.skipif(not _HAS_PLAYWRIGHT, reason="playwright not installed")
    def test_stm_svg_state_links_navigate_to_anchor(self, stm_app):
        """Clicking a state shape navigates to that need's anchor.

        The user-visible promise of every needsysml-*-svg directive is
        that each drawn element is a live link to the need's definition.
        Find the <a href="#SU-002"> wrapping the ``starting`` state,
        click the inner rect, and assert the URL hash becomes #SU-002.
        """
        html_path = Path(stm_app.outdir) / "index.html"
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            page = browser.new_page()
            page.goto(f"file://{html_path}")
            page.wait_for_load_state("networkidle")

            target_id = "SU-002"
            anchor = page.query_selector(f'a[href="#{target_id}"]')
            assert anchor is not None, (
                f"No <a href='#{target_id}'> found in rendered STM SVG"
            )
            anchor.click()

            # URL fragment should now match the clicked state
            assert page.url.endswith(f"#{target_id}"), (
                f"Expected URL to end with #{target_id}, got {page.url}"
            )
            browser.close()

    @pytest.mark.skipif(not _HAS_PLAYWRIGHT, reason="playwright not installed")
    def test_stm_svg_state_shapes_do_not_overlap(self, stm_app):
        """State shapes must not overlap each other in the rendered DOM.

        Catches a class of layout bug where the per-row alternating
        y-coordinate (90/230) collapses or the per-state x-step is too
        small. Uses Playwright's rendered ``boundingBox`` (browser-truth)
        rather than parsed SVG attributes (template-truth).
        """
        html_path = Path(stm_app.outdir) / "index.html"
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            page = browser.new_page(viewport={"width": 1400, "height": 900})
            page.goto(f"file://{html_path}")
            page.wait_for_load_state("networkidle")

            # Restrict to the STM SVG (viewBox 720x320 + contains SU-001)
            stm_svg = None
            for svg in page.query_selector_all("svg"):
                vb = svg.get_attribute("viewBox") or ""
                if "720 320" in vb and "SU-001" in (svg.inner_html() or ""):
                    stm_svg = svg
                    break
            assert stm_svg, "STM SVG not found in rendered page"

            # Collect bounding boxes of every state shape (rects with rx=8
            # for ordinary states, circles for pseudostates)
            shape_boxes = []
            for sel in ['rect[rx="8"]', "circle"]:
                for shape in stm_svg.query_selector_all(sel):
                    bb = shape.bounding_box()
                    if bb and bb["width"] > 4 and bb["height"] > 4:
                        shape_boxes.append(bb)

            assert len(shape_boxes) >= 4, (
                f"Expected ≥4 state shapes, found {len(shape_boxes)}"
            )

            def overlap(a, b):
                return not (
                    a["x"] + a["width"] <= b["x"]
                    or b["x"] + b["width"] <= a["x"]
                    or a["y"] + a["height"] <= b["y"]
                    or b["y"] + b["height"] <= a["y"]
                )

            for i, a in enumerate(shape_boxes):
                for b in shape_boxes[i + 1 :]:
                    assert not overlap(a, b), (
                        f"State shapes overlap in rendered DOM: {a} vs {b}"
                    )
            browser.close()
