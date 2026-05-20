"""Tests for SysML flow config registration."""

import pytest
from pathlib import Path
import shutil


@pytest.fixture()
def flow_app(make_app, tmp_path):
    """Build the basic test project."""
    srcdir = Path(__file__).parent / "doc_test" / "basic"
    tmproot = tmp_path / "basic"
    shutil.copytree(srcdir, tmproot)
    app = make_app(srcdir=tmproot)
    app.build()
    return app


class TestFlowConfigs:
    """Tests for needs_flow_configs registration."""

    def test_sysml_bdd_key_exists(self, flow_app):
        """The sysml_bdd key exists in needs_flow_configs after build."""
        flow_configs = flow_app.config.needs_flow_configs
        assert "sysml_bdd" in flow_configs

    def test_sysml_ibd_key_exists(self, flow_app):
        """The sysml_ibd key exists in needs_flow_configs after build."""
        flow_configs = flow_app.config.needs_flow_configs
        assert "sysml_ibd" in flow_configs

    def test_sysml_req_key_exists(self, flow_app):
        """The sysml_req key exists in needs_flow_configs after build."""
        flow_configs = flow_app.config.needs_flow_configs
        assert "sysml_req" in flow_configs

    def test_user_override_preserved(self, make_app, tmp_path):
        """User-defined flow config keys are not overwritten."""
        srcdir = Path(__file__).parent / "doc_test" / "basic"
        tmproot = tmp_path / "basic"
        shutil.copytree(srcdir, tmproot)
        # Add a custom flow config
        conf = tmproot / "conf.py"
        content = conf.read_text()
        content += '\nneeds_flow_configs = {"custom_key": "custom_value"}\n'
        conf.write_text(content)

        app = make_app(srcdir=tmproot)
        app.build()
        flow_configs = app.config.needs_flow_configs
        assert "custom_key" in flow_configs
        assert flow_configs["custom_key"] == "custom_value"
        # Extension keys should still be present
        assert "sysml_bdd" in flow_configs
