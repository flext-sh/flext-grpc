# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tools package."""

from __future__ import annotations

from flext_core.lazy import install_lazy_exports

_LAZY_IMPORTS = {
    "ArchitectureValidator": (
        "docs.architecture.tools.validate_docs",
        "ArchitectureValidator",
    ),
    "ValidationResults": ("docs.architecture.tools.validate_docs", "ValidationResults"),
    "ValidationSummary": ("docs.architecture.tools.validate_docs", "ValidationSummary"),
    "save_report": ("docs.architecture.tools.validate_docs", "save_report"),
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
