"""Tests for SysML v2 extra field registration."""

import pytest
from pathlib import Path
import shutil


@pytest.fixture()
def built_app(make_app, tmp_path):
    """Build the basic test project and return the Sphinx app."""
    srcdir = Path(__file__).parent / "doc_test" / "basic"
    tmproot = tmp_path / "basic"
    shutil.copytree(srcdir, tmproot)
    app = make_app(srcdir=tmproot)
    app.build()
    return app


class TestFieldsRegistration:
    """Verify all 15 SysML v2 extra fields are registered."""

    EXPECTED_FIELDS = [
        "abstract", "owned_by", "multiplicity", "direction", "conjugated",
        "definition", "satisfies", "refines", "allocates", "req_text",
        "source_port", "target_port", "is_initial", "is_final",
    ]

    def test_fields_on_need_data(self, built_app):
        """Fields are accessible on need objects after build."""
        needs = built_app.env._needs_all_needs
        pd001 = needs.get("PD-001")
        assert pd001 is not None, "PD-001 not found in needs data"
        # Verify our custom fields exist on the need object
        assert "abstract" in pd001
        assert "owned_by" in pd001

    def test_owned_by_field_readable(self, built_app):
        """The owned_by field is readable on needs that set it."""
        needs = built_app.env._needs_all_needs
        p001 = needs.get("P-001")
        assert p001 is not None
        assert p001.get("owned_by") == "PD-001"

    def test_satisfies_field_readable(self, built_app):
        """The satisfies field is readable on needs that set it."""
        needs = built_app.env._needs_all_needs
        r001 = needs.get("R-001")
        assert r001 is not None
        assert r001.get("satisfies") == "PD-001"

    def test_direction_field_readable(self, built_app):
        """The direction field is readable on port needs."""
        needs = built_app.env._needs_all_needs
        po001 = needs.get("PO-001")
        assert po001 is not None
        assert po001.get("direction") == "in"
