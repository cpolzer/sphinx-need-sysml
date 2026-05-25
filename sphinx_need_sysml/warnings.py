"""Warning emission helpers for sphinx-need-sysml."""

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
            "sphinx-need-sysml: PlantUML hyperlinks require "
            "plantuml_output_format = 'svg'. Set this in conf.py for clickable diagrams."
        )


def _get_logger() -> logging.Logger:
    from sphinx.util import logging as sphinx_logging

    return sphinx_logging.getLogger(__name__)  # type: ignore[return-value]


# === Shared helpers for FR-016 + FR-018 ===
# Every needsysml-* directive uses these so the warning categories and
# placeholder text are uniform across diagrams.


def warn_unknown_ref(
    app: Sphinx,
    docname: str,
    lineno: int,
    diagram: str,
    ref_kind: str,
    ref_id: str,
) -> str:
    """Emit a Sphinx warning for an unknown reference and return a placeholder.

    Use when a diagram element references a need ID that does not exist
    in the live needs registry. Implements FR-016.

    Args:
        app: The Sphinx application.
        docname: The document name where the reference appears.
        lineno: The source line number of the referencing directive.
        diagram: The diagram family (e.g. ``"stm"``, ``"act"``, ``"sd"``).
        ref_kind: The kind of reference (e.g. ``"state"``, ``"action"``,
            ``"lifeline"``, ``"target"``, ``"binding"``).
        ref_id: The unresolved need ID.

    Returns:
        A short placeholder string (``"?? <ref_id>"``) the caller should
        substitute at the element's position in the rendered diagram.
    """
    category = f"needsysml.{diagram}.unknown-{ref_kind}"
    location = f"{docname}:{lineno}"
    _get_logger().warning(
        "%s: unknown %s reference '%s' — rendering placeholder",
        location,
        ref_kind,
        ref_id,
        type=category,  # type: ignore[call-arg]
    )
    return f"?? {ref_id}"


def warn_empty(
    app: Sphinx,
    docname: str,
    lineno: int,
    diagram: str,
) -> str:
    """Emit a Sphinx info-warning for an empty diagram and return a placeholder.

    Use when a diagram's element filter resolves to zero matches.
    Implements FR-018.

    Args:
        app: The Sphinx application.
        docname: The document name where the directive appears.
        lineno: The source line number of the directive.
        diagram: The diagram family (e.g. ``"stm"``, ``"act"``).

    Returns:
        A short placeholder string the caller should display at the
        position the empty content would have occupied.
    """
    category = f"needsysml.{diagram}.empty"
    location = f"{docname}:{lineno}"
    _get_logger().warning(
        "%s: no matching elements for %s diagram — rendering placeholder",
        location,
        diagram,
        type=category,  # type: ignore[call-arg]
    )
    return "No matching elements"
