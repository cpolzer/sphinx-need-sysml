"""Sphinx extension for SysML v2 need types and diagrams."""

import importlib.util
import inspect
import logging
from collections.abc import Mapping

from sphinx.application import Sphinx
from sphinx.config import Config
from sphinx_needs.api import add_need_type

from sphinxcontrib.sysml.config import SYSML_NEED_TYPES
from sphinxcontrib.sysml.fields import SYSML_FIELDS

VERSION = "0.3.0"

# Detect sphinx-need-svg availability
_HAS_NEED_SVG = importlib.util.find_spec("sphinx_need_svg") is not None

# Compatibility shim for add_field vs add_extra_option (mirrors sphinx-test-reports)
try:
    from sphinx_needs.api import add_field as _add_field

    def _register_field(
        name: str, description: str, schema: Mapping[str, object] | None = None
    ) -> None:
        try:
            _add_field(name, description, schema=schema)
        except Exception:
            _get_logger().debug(f"Field '{name}' already registered, skipping")

except ImportError:
    from sphinx_needs.api import add_extra_option as _add_extra_option

    _add_extra_option_supports_description = (
        "description" in inspect.signature(_add_extra_option).parameters
    )

    def _register_field(
        name: str, description: str, schema: Mapping[str, object] | None = None
    ) -> None:
        kwargs: dict[str, object] = {}
        if _add_extra_option_supports_description:
            kwargs["description"] = description
        if schema is not None:
            kwargs["schema"] = schema
        try:
            _add_extra_option(None, name, **kwargs)
        except Exception:
            _get_logger().debug(f"Field '{name}' already registered, skipping")


def _get_logger() -> logging.Logger:
    from sphinx.util import logging as sphinx_logging

    return sphinx_logging.getLogger(__name__)  # type: ignore[return-value]


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


def _warn_plantuml_format(app: Sphinx) -> None:
    """Emit warning if plantuml_output_format is not svg when diagram directives are used."""
    from sphinxcontrib.sysml.warnings import warn_plantuml_format

    warn_plantuml_format(app)


def setup(app: Sphinx) -> dict[str, object]:
    """Sphinx extension entry point."""
    app.setup_extension("sphinx_needs")

    app.connect("config-inited", _register_types_and_fields)
    app.connect("builder-inited", _register_flow_configs)
    app.connect("builder-inited", _warn_plantuml_format)

    # Register diagram directives
    from sphinxcontrib.sysml.directives.needsysml_bdd import NeedsymlBddDirective
    from sphinxcontrib.sysml.directives.needsysml_ibd import NeedsymlIbdDirective
    from sphinxcontrib.sysml.directives.needsysml_req import NeedsymlReqDirective
    from sphinxcontrib.sysml.directives.needsysml_act import (
        NeedsymlActDirective,
        NeedsymlActSvgDirective,
    )
    from sphinxcontrib.sysml.directives.needsysml_pkg import (
        NeedsymlPkgDirective,
        NeedsymlPkgSvgDirective,
    )
    from sphinxcontrib.sysml.directives.needsysml_sd import (
        NeedsymlSdDirective,
        NeedsymlSdSvgDirective,
    )
    from sphinxcontrib.sysml.directives.needsysml_stm import (
        NeedsymlStmDirective,
        NeedsymlStmSvgDirective,
    )
    from sphinxcontrib.sysml.directives.needsysml_uc import (
        NeedsymlUcDirective,
        NeedsymlUcSvgDirective,
    )

    app.add_directive("needsysml-bdd", NeedsymlBddDirective)
    app.add_directive("needsysml-ibd", NeedsymlIbdDirective)
    app.add_directive("needsysml-req", NeedsymlReqDirective)
    app.add_directive("needsysml-stm", NeedsymlStmDirective)
    app.add_directive("needsysml-act", NeedsymlActDirective)
    app.add_directive("needsysml-sd", NeedsymlSdDirective)
    app.add_directive("needsysml-uc", NeedsymlUcDirective)
    app.add_directive("needsysml-pkg", NeedsymlPkgDirective)

    # Register SVG directives only when sphinx-need-svg is available
    if _HAS_NEED_SVG:
        from sphinxcontrib.sysml.directives.needsysml_svg import (
            NeedsymlBddSvgDirective,
            NeedsymlIbdSvgDirective,
        )

        app.add_directive("needsysml-bdd-svg", NeedsymlBddSvgDirective)
        app.add_directive("needsysml-ibd-svg", NeedsymlIbdSvgDirective)
        app.add_directive("needsysml-stm-svg", NeedsymlStmSvgDirective)
        app.add_directive("needsysml-act-svg", NeedsymlActSvgDirective)
        app.add_directive("needsysml-sd-svg", NeedsymlSdSvgDirective)
        app.add_directive("needsysml-uc-svg", NeedsymlUcSvgDirective)
        app.add_directive("needsysml-pkg-svg", NeedsymlPkgSvgDirective)

    return {
        "version": VERSION,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
