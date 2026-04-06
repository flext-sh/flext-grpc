# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tools package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports

if _t.TYPE_CHECKING:
    import docs.architecture.tools.validate_docs as _docs_architecture_tools_validate_docs

    validate_docs = _docs_architecture_tools_validate_docs
    from docs.architecture.tools.validate_docs import (
        ArchitectureValidator,
        ValidationResults,
        ValidationSummary,
        main,
        save_report,
    )

    from flext_core.constants import FlextConstants as c
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.models import FlextModels as m
    from flext_core.protocols import FlextProtocols as p
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
    from flext_core.typings import FlextTypes as t
    from flext_core.utilities import FlextUtilities as u
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
    "main": ("docs.architecture.tools.validate_docs", "main"),
    "p": ("flext_core.protocols", "FlextProtocols"),
    "r": ("flext_core.result", "FlextResult"),
    "s": ("flext_core.service", "FlextService"),
    "save_report": ("docs.architecture.tools.validate_docs", "save_report"),
    "t": ("flext_core.typings", "FlextTypes"),
    "u": ("flext_core.utilities", "FlextUtilities"),
    "validate_docs": "docs.architecture.tools.validate_docs",
    "x": ("flext_core.mixins", "FlextMixins"),
}

__all__ = [
    "ArchitectureValidator",
    "ValidationResults",
    "ValidationSummary",
    "c",
    "d",
    "e",
    "h",
    "m",
    "main",
    "p",
    "r",
    "s",
    "save_report",
    "t",
    "u",
    "validate_docs",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
