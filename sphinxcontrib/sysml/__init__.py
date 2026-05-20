"""Sphinx extension for SysML v2 need types and diagrams."""

VERSION = "0.1.0"


def setup(app):
    """Sphinx extension entry point."""
    return {
        "version": VERSION,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
