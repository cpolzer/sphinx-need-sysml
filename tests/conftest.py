"""Pytest configuration for sphinxcontrib-sysml tests."""

import shutil
from pathlib import Path
from tempfile import mkdtemp

import pytest
from packaging.version import Version
from sphinx import __version__ as sphinx_version

if Version(sphinx_version) < Version("7.2"):
    from sphinx.testing.path import path

pytest_plugins = "sphinx.testing.fixtures"


@pytest.fixture(scope="session")
def rootdir():
    return Path(__file__).parent.absolute() / "doc_test"


def copy_srcdir_to_tmpdir(srcdir, tmp):
    srcdir = Path(srcdir)
    tmproot = tmp / srcdir.name
    shutil.copytree(srcdir, tmproot)
    if Version(sphinx_version) >= Version("7.2"):
        return tmproot
    return path(tmproot)


@pytest.fixture(scope="function")
def basic_app(make_app, tmp_path):
    """Sphinx app fixture for basic test project."""
    rd = Path(__file__).parent.absolute() / "doc_test"
    srcdir = copy_srcdir_to_tmpdir(rd / "basic", tmp_path)
    app = make_app(srcdir=srcdir)
    app.build()
    return app
