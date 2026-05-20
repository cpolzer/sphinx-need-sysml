"""Tests for SysML v2 need type registration."""

import pytest
from sphinx.application import Sphinx


@pytest.fixture()
def built_app(make_app, tmp_path):
    """Build the basic test project and return the Sphinx app."""
    from pathlib import Path
    import shutil

    srcdir = Path(__file__).parent / "doc_test" / "basic"
    tmproot = tmp_path / "basic"
    shutil.copytree(srcdir, tmproot)
    app = make_app(srcdir=tmproot)
    app.build()
    return app


class TestNeedTypesRegistration:
    """Verify all 14 SysML v2 need types are registered."""

    EXPECTED_TYPES = [
        ("partdef", "PartDef", "PD-"),
        ("part", "Part", "P-"),
        ("portdef", "PortDef", "POD-"),
        ("port", "Port", "PO-"),
        ("interfacedef", "InterfaceDef", "IFD-"),
        ("interface", "Interface", "IF-"),
        ("connectiondef", "ConnectionDef", "CD-"),
        ("connection", "Connection", "C-"),
        ("actiondef", "ActionDef", "AD-"),
        ("action", "Action", "A-"),
        ("statedef", "StateDef", "SD-"),
        ("stateusage", "StateUsage", "SU-"),
        ("requirementdef", "RequirementDef", "RD-"),
        ("requirement", "Requirement", "R-"),
    ]

    @pytest.mark.parametrize("directive,title,prefix", EXPECTED_TYPES)
    def test_type_registered(self, built_app, directive, title, prefix):
        """Each need type is registered in the app after build."""
        needs_config = built_app.config
        need_types = needs_config.needs_types
        type_names = [t["directive"] for t in need_types]
        assert directive in type_names, f"Type '{directive}' not registered"

    @pytest.mark.parametrize("directive,title,prefix", EXPECTED_TYPES)
    def test_type_has_correct_prefix(self, built_app, directive, title, prefix):
        """Each need type has the correct ID prefix."""
        need_types = built_app.config.needs_types
        for t in need_types:
            if t["directive"] == directive:
                assert t["prefix"] == prefix, (
                    f"Type '{directive}' has prefix '{t['prefix']}', expected '{prefix}'"
                )
                break
