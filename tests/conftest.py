"""Pytest configuration for sphinx-need-sysml tests."""

import shutil
from pathlib import Path

import pytest

pytest_plugins = "sphinx.testing.fixtures"

TEST_ROOT = Path(__file__).parent / "doc_test"


@pytest.fixture(scope="session")
def rootdir():
    return TEST_ROOT


def copy_test_app(srcdir, tmp_path):
    """Copy a test app source to a temp directory."""
    tmproot = tmp_path / srcdir.name
    shutil.copytree(srcdir, tmproot)
    return tmproot


@pytest.fixture(scope="function")
def basic_app(make_app, tmp_path):
    """Sphinx app fixture for basic test project."""
    srcdir = copy_test_app(TEST_ROOT / "basic", tmp_path)
    app = make_app(srcdir=srcdir)
    app.build()
    return app
