# AUTO-GENERATED FILE — Regenerate with: make gen
"""Unit package."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".test_api": ("TestsFlextGrpcApi",),
        ".test_config": ("TestsFlextGrpcConfig",),
        ".test_constants": ("TestsFlextGrpcConstantsUnit",),
        ".test_entities": ("TestFlextGrpcEntities",),
        ".test_errors": (
            "TestErrorIntegration",
            "TestFlextGrpcConfigurationError",
            "TestFlextGrpcConnectionError",
            "TestFlextGrpcError",
            "TestFlextGrpcTimeoutError",
            "TestFlextGrpcValidationError",
        ),
        ".test_models": ("TestFlextGrpcModels",),
        ".test_protocols": ("TestsFlextGrpcProtocolsUnit",),
        ".test_services": ("TestFlextGrpcServiceComponents",),
        ".test_typings": ("TestsFlextGrpcTypesUnit",),
        ".test_utilities": ("Testu",),
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
