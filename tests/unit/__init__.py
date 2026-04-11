# AUTO-GENERATED FILE — Regenerate with: make gen
"""Unit package."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".test_api": ("test_api",),
        ".test_config": ("test_config",),
        ".test_constants": ("test_constants",),
        ".test_entities": ("test_entities",),
        ".test_errors": ("test_errors",),
        ".test_models": ("test_models",),
        ".test_protocols": ("test_protocols",),
        ".test_services": ("test_services",),
        ".test_typings": ("test_typings",),
        ".test_utilities": ("test_utilities",),
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
