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
    "c": ("flext_core.constants", "FlextConstants"),
    "d": ("flext_core.decorators", "FlextDecorators"),
    "e": ("flext_core.exceptions", "FlextExceptions"),
    "h": ("flext_core.handlers", "FlextHandlers"),
    "m": ("flext_core.models", "FlextModels"),
    "p": ("flext_core.protocols", "FlextProtocols"),
    "r": ("flext_core.result", "FlextResult"),
    "s": ("flext_core.service", "FlextService"),
    "save_report": ("docs.architecture.tools.validate_docs", "save_report"),
    "t": ("flext_core.typings", "FlextTypes"),
    "u": ("flext_core.utilities", "FlextUtilities"),
    "validate_docs": "docs.architecture.tools.validate_docs",
    "x": ("flext_core.mixins", "FlextMixins"),
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
