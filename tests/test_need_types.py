"""Tests for SysML v2 need type registration."""

import pytest


@pytest.fixture()
def built_app(make_app, tmp_path):
    """Build the basic test project and return the Sphinx app."""
    import shutil
    from pathlib import Path

    srcdir = Path(__file__).parent / "doc_test" / "basic"
    tmproot = tmp_path / "basic"
    shutil.copytree(srcdir, tmproot)
    app = make_app(srcdir=tmproot)
    app.build()
    return app


class TestNeedTypesRegistration:
    """Verify all 27 SysML v2 need types are registered (14 from feature 001 + 13 from 002)."""

    EXPECTED_TYPES = [
        # Feature 001
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
        # Feature 002 — state-machine
        ("transition", "Transition", "TRANS-"),
        # Feature 002 — activity
        ("controlflow", "ControlFlow", "CTRLFLOW-"),
        ("objectflow", "ObjectFlow", "OBJFLOW-"),
        # Feature 002 — package
        ("package", "Package", "PKG-"),
        ("dependency", "Dependency", "DEP-"),
        # Feature 002 — use case
        ("usecase", "UseCase", "USECASE-"),
        ("actor", "Actor", "ACTOR-"),
        # Feature 002 — parametric (registered in v1; rendered in v1.1)
        ("constraintblock", "ConstraintBlock", "CONSTRAINT-"),
        ("constraintparameter", "ConstraintParameter", "PARAM-"),
        ("valueproperty", "ValueProperty", "VALUE-"),
        ("bindingconnector", "BindingConnector", "BIND-"),
        # Feature 002 — sequence
        ("lifeline", "Lifeline", "LIFELINE-"),
        ("message", "Message", "MSG-"),
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
