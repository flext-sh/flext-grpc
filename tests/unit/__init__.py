# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Unit package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_core import FlextTypes
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
    from flext_grpc import (
        test_api,
        test_config,
        test_constants,
        test_entities,
        test_errors,
        test_models,
        test_protocols,
        test_services,
        test_typings,
        test_utilities,
    )
    from flext_grpc.test_api import TestFlextGrpc
    from flext_grpc.test_config import TestFlextGrpcSettings
    from flext_grpc.test_constants import TestFlextGrpcConstants
    from flext_grpc.test_entities import TestFlextGrpcEntities
    from flext_grpc.test_errors import TestFlextGrpcError
    from flext_grpc.test_models import TestFlextGrpcModels
    from flext_grpc.test_protocols import Testp
    from flext_grpc.test_services import TestFlextGrpcServices
    from flext_grpc.test_typings import TestFlextGrpcTypes
    from flext_grpc.test_utilities import Testu

_LAZY_IMPORTS: FlextTypes.LazyImportIndex = {
    "TestFlextGrpc": "flext_grpc.test_api",
    "TestFlextGrpcConstants": "flext_grpc.test_constants",
    "TestFlextGrpcEntities": "flext_grpc.test_entities",
    "TestFlextGrpcError": "flext_grpc.test_errors",
    "TestFlextGrpcModels": "flext_grpc.test_models",
    "TestFlextGrpcServices": "flext_grpc.test_services",
    "TestFlextGrpcSettings": "flext_grpc.test_config",
    "TestFlextGrpcTypes": "flext_grpc.test_typings",
    "Testp": "flext_grpc.test_protocols",
    "Testu": "flext_grpc.test_utilities",
    "c": ("flext_core.constants", "FlextConstants"),
    "d": ("flext_core.decorators", "FlextDecorators"),
    "e": ("flext_core.exceptions", "FlextExceptions"),
    "h": ("flext_core.handlers", "FlextHandlers"),
    "m": ("flext_core.models", "FlextModels"),
    "p": ("flext_core.protocols", "FlextProtocols"),
    "r": ("flext_core.result", "FlextResult"),
    "s": ("flext_core.service", "FlextService"),
    "t": ("flext_core.typings", "FlextTypes"),
    "test_api": "flext_grpc.test_api",
    "test_config": "flext_grpc.test_config",
    "test_constants": "flext_grpc.test_constants",
    "test_entities": "flext_grpc.test_entities",
    "test_errors": "flext_grpc.test_errors",
    "test_models": "flext_grpc.test_models",
    "test_protocols": "flext_grpc.test_protocols",
    "test_services": "flext_grpc.test_services",
    "test_typings": "flext_grpc.test_typings",
    "test_utilities": "flext_grpc.test_utilities",
    "u": ("flext_core.utilities", "FlextUtilities"),
    "x": ("flext_core.mixins", "FlextMixins"),
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
