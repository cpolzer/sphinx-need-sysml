"""Sphinx extension for SysML v2 need types and diagrams."""

import inspect

import sphinx
import sphinx_needs
from packaging.version import Version
from sphinx.application import Sphinx
from sphinx.config import Config
from sphinx_needs.api import add_need_type

from sphinxcontrib.sysml.config import SYSML_NEED_TYPES
from sphinxcontrib.sysml.fields import SYSML_FIELDS

VERSION = "0.1.0"

# Compatibility shim for add_field vs add_extra_option (mirrors sphinx-test-reports)
try:
    from sphinx_needs.api import add_field as _add_field

    def _register_field(name: str, description: str, schema: dict | None = None) -> None:
        try:
            _add_field(name, description, schema=schema)
        except Exception:
            log = _get_logger()
            log.debug(f"Field '{name}' already registered, skipping")

except ImportError:
    from sphinx_needs.api import add_extra_option as _add_extra_option

    _add_extra_option_supports_description = (
        "description" in inspect.signature(_add_extra_option).parameters
    )

    def _register_field(name: str, description: str, schema: dict | None = None) -> None:
        kwargs = {}
        if _add_extra_option_supports_description:
            kwargs["description"] = description
        if schema is not None:
            kwargs["schema"] = schema
        try:
            _add_extra_option(None, name, **kwargs)
        except Exception:
            log = _get_logger()
            log.debug(f"Field '{name}' already registered, skipping")


def _get_logger():
    sphinx_version = Version(sphinx.__version__)
    if sphinx_version >= Version("1.6"):
        from sphinx.util import logging
        return logging.getLogger(__name__)
    import logging
    return logging.getLogger(__name__)


def _register_types_and_fields(app: Sphinx, config: Config) -> None:
    """Register all SysML v2 need types and extra fields with sphinx-needs."""
    for need_type in SYSML_NEED_TYPES:
        add_need_type(
            app,
            need_type["directive"],
            need_type["title"],
            need_type["prefix"],
            need_type["color"],
            need_type["style"],
        )

    for field in SYSML_FIELDS:
        _register_field(
            field["name"],
            field["description"],
            field.get("schema"),
        )


def _register_flow_configs(app: Sphinx) -> None:
    """Merge SysML flow configs into needs_flow_configs, preserving user overrides."""
    from sphinxcontrib.sysml.flow_configs import SYSML_FLOW_CONFIGS

    existing = getattr(app.config, "needs_flow_configs", None) or {}
    app.config.needs_flow_configs = {**SYSML_FLOW_CONFIGS, **existing}


def setup(app: Sphinx) -> dict:
    """Sphinx extension entry point."""
    app.setup_extension("sphinx_needs")

    app.connect("config-inited", _register_types_and_fields)
    app.connect("builder-inited", _register_flow_configs)

    return {
        "version": VERSION,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
