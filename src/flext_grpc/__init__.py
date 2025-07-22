"""FLEXT GRPC - Enterprise gRPC Services with simplified imports.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

Version 0.7.0 - Clean Architecture with simplified public API:
- All common imports available from root: from flext_grpc import GRPCService
- Zero tolerance for mock/fake implementations - REAL gRPC only
- Deprecation warnings for internal imports
"""

from __future__ import annotations

import warnings

# Import from flext-core for foundational patterns
from flext_core import (
    BaseConfig,
    # Foundation patterns - ALWAYS from flext-core
    BaseConfig as GRPCBaseConfig,  # Configuration base
    DomainBaseModel,
    DomainBaseModel as BaseModel,  # Base for gRPC models
    DomainError as GRPCError,  # gRPC-specific errors
    ServiceResult,
    ValidationError as ValidationError,  # Validation errors
)

# Application layer exports - simplified imports
from flext_grpc.application.commands import (
    ExecuteRPCCallCommand,
    HealthCheckCommand,
    RegisterRPCMethodCommand,
    StartGRPCServiceCommand,
    StopGRPCServiceCommand,
)

# Domain layer exports - simplified imports
from flext_grpc.domain.entities import (
    GRPCService,
    RPCCall,
    RPCMethod,
    RPCMethodType,
    ServiceStatus,
)

# Infrastructure exports - simplified imports
from flext_grpc.infrastructure.grpc_base import BaseGrpcService

__version__ = "0.7.0"


class FlextGRPCDeprecationWarning(DeprecationWarning):
    """Custom deprecation warning for FLEXT gRPC import changes."""


def _show_deprecation_warning(old_import: str, new_import: str) -> None:
    """Show deprecation warning for import paths."""
    message_parts = [
        f"⚠️  DEPRECATED IMPORT: {old_import}",
        f"✅ USE INSTEAD: {new_import}",
        "🔗 This will be removed in version 1.0.0",
        "📖 See FLEXT gRPC docs for migration guide",
    ]
    warnings.warn(
        "\n".join(message_parts),
        FlextGRPCDeprecationWarning,
        stacklevel=3,
    )


# ================================
# SIMPLIFIED PUBLIC API EXPORTS
# ================================

# ================================
# PUBLIC API EXPORTS
# ================================

__all__ = [
    # Infrastructure (simplified access)
    "BaseGrpcService",  # from flext_grpc import BaseGrpcService
    "BaseModel",  # from flext_grpc import BaseModel
    # Application Commands (simplified access)
    "ExecuteRPCCallCommand",  # from flext_grpc import ExecuteRPCCallCommand
    # Deprecation utilities
    "FlextGRPCDeprecationWarning",
    "GRPCBaseConfig",  # from flext_grpc import GRPCBaseConfig
    "GRPCError",  # from flext_grpc import GRPCError
    # Domain Entities (simplified access)
    "GRPCService",  # from flext_grpc import GRPCService
    "HealthCheckCommand",  # from flext_grpc import HealthCheckCommand
    "RPCCall",  # from flext_grpc import RPCCall
    "RPCMethod",  # from flext_grpc import RPCMethod
    "RPCMethodType",  # from flext_grpc import RPCMethodType
    "RegisterRPCMethodCommand",  # from flext_grpc import RegisterRPCMethodCommand
    # Core Patterns (from flext-core)
    "ServiceResult",  # from flext_grpc import ServiceResult
    "ServiceStatus",  # from flext_grpc import ServiceStatus
    "StartGRPCServiceCommand",  # from flext_grpc import StartGRPCServiceCommand
    "StopGRPCServiceCommand",  # from flext_grpc import StopGRPCServiceCommand
    "ValidationError",  # from flext_grpc import ValidationError
    # Version
    "__version__",
]
