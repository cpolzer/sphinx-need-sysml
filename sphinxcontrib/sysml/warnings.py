"""Warning emission helpers for sphinxcontrib-sysml."""

import sphinx
from packaging.version import Version
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
        log = _get_logger(app)
        log.warning(
            "sphinxcontrib-sysml: PlantUML hyperlinks require "
            "plantuml_output_format = 'svg'. Set this in conf.py for clickable diagrams."
        )


def _get_logger(app: Sphinx):
    sphinx_version = Version(sphinx.__version__)
    if sphinx_version >= Version("1.6"):
        from sphinx.util import logging
        return logging.getLogger(__name__)
    import logging
    return logging.getLogger(__name__)
