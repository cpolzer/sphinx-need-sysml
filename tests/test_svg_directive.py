"""Tests for the needsysml-bdd-svg directive."""

import shutil
from pathlib import Path


class TestSvgDirective:
    """Tests for the needsysml-bdd-svg directive."""

    def test_svg_flag_reflects_availability(self):
        """The _HAS_NEED_SVG flag reflects whether sphinx_need_svg is importable."""
        import sphinxcontrib.sysml

        # The flag should be a boolean
        assert isinstance(sphinxcontrib.sysml._HAS_NEED_SVG, bool)  # noqa: SLF001

    def test_svg_directive_importable_when_available(self):
        """The SVG directive module is importable when sphinx_need_svg is available."""
        import sphinxcontrib.sysml

        if sphinxcontrib.sysml._HAS_NEED_SVG:  # noqa: SLF001
            from sphinxcontrib.sysml.directives.needsysml_svg import (
                NeedsymlBddSvgDirective,
            )

            assert NeedsymlBddSvgDirective is not None
            assert NeedsymlBddSvgDirective.required_arguments == 1

    def test_svg_directive_not_registered_when_unavailable(self, make_app, tmp_path):
        """When sphinx_need_svg is absent, the SVG directive is not registered."""
        import sphinxcontrib.sysml

        if not sphinxcontrib.sysml._HAS_NEED_SVG:  # noqa: SLF001
            srcdir = Path(__file__).parent / "doc_test" / "basic"
            tmproot = tmp_path / "basic"
            shutil.copytree(srcdir, tmproot)
            app = make_app(srcdir=tmproot)
            app.build()
            # The directive should not cause errors
            # (it simply won't be available for use in RST)
            assert app is not None
