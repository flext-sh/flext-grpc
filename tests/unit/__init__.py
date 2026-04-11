# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Grpc package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if _t.TYPE_CHECKING:
    from flext_grpc.test_api import TestFlextGrpc
    from flext_grpc.test_config import TestFlextGrpcSettings
    from flext_grpc.test_constants import TestFlextGrpcConstants
    from flext_grpc.test_entities import TestFlextGrpcEntities
    from flext_grpc.test_errors import (
        TestErrorIntegration,
        TestFlextGrpcConfigurationError,
        TestFlextGrpcConnectionError,
        TestFlextGrpcError,
        TestFlextGrpcTimeoutError,
        TestFlextGrpcValidationError,
    )
    from flext_grpc.test_models import TestFlextGrpcModels
    from flext_grpc.test_protocols import Testp
    from flext_grpc.test_services import TestFlextGrpcServiceComponents
    from flext_grpc.test_typings import TestFlextGrpcTypes
    from flext_grpc.test_utilities import Testu
_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".test_api": ("TestFlextGrpc",),
        ".test_config": ("TestFlextGrpcSettings",),
        ".test_constants": ("TestFlextGrpcConstants",),
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
        ".test_protocols": ("Testp",),
        ".test_services": ("TestFlextGrpcServiceComponents",),
        ".test_typings": ("TestFlextGrpcTypes",),
        ".test_utilities": ("Testu",),
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)

__all__ = [
    "TestErrorIntegration",
    "TestFlextGrpc",
    "TestFlextGrpcConfigurationError",
    "TestFlextGrpcConnectionError",
    "TestFlextGrpcConstants",
    "TestFlextGrpcEntities",
    "TestFlextGrpcError",
    "TestFlextGrpcModels",
    "TestFlextGrpcServiceComponents",
    "TestFlextGrpcSettings",
    "TestFlextGrpcTimeoutError",
    "TestFlextGrpcTypes",
    "TestFlextGrpcValidationError",
    "Testp",
    "Testu",
]
