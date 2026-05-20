"""Warning emission helpers for sphinxcontrib-sysml."""

import logging

from sphinx.application import Sphinx

_PLANTUML_WARNING_EMITTED = False


def warn_plantuml_format(app: Sphinx) -> None:
    """Emit a Sphinx warning if plantuml_output_format is not 'svg'.

    Only emits once per build to avoid noise.
    """
    global _PLANTUML_WARNING_EMITTED
    if _PLANTUML_WARNING_EMITTED:
        return

    fmt = getattr(app.config, "plantuml_output_format", None)
    if fmt != "svg":
        _PLANTUML_WARNING_EMITTED = True
        _get_logger().warning(
            "sphinxcontrib-sysml: PlantUML hyperlinks require "
            "plantuml_output_format = 'svg'. Set this in conf.py for clickable diagrams."
        )


def _get_logger() -> logging.Logger:
    from sphinx.util import logging as sphinx_logging

    return sphinx_logging.getLogger(__name__)  # type: ignore[return-value]
