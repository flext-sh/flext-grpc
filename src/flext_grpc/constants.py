"""FLEXT gRPC Constants - Enterprise configuration constants and validation rules.

This module provides comprehensive constants for the FLEXT gRPC platform,
extending the flext-core constant foundation with domain-specific values,
validation rules, and configuration defaults. Designed for consistent
configuration management and enterprise deployment standards.
Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import ClassVar

from flext_core import FlextConstants, FlextTypes

# =============================================================================
# GRPC-SPECIFIC SEMANTIC CONSTANTS - Modern Python 3.13 Structure
# =============================================================================


class FlextGrpcSemanticConstants(FlextConstants):
    """gRPC-specific semantic constants extending FlextConstants.

    Modern Python 3.13 constants following semantic grouping patterns.
    Extends the FLEXT ecosystem constants with gRPC communication specific
    values while maintaining full backward compatibility.
    """

    class GrpcNetwork:
        """gRPC network configuration constants."""

        # CONSUME from single source - NO DUPLICATION
        DEFAULT_HOST = FlextConstants.Infrastructure.DEFAULT_HOST
        DEFAULT_PORT = 50051  # gRPC-specific port
        MIN_PORT = FlextConstants.Platform.MIN_PORT_NUMBER
        MAX_PORT = FlextConstants.Platform.MAX_PORT_NUMBER
        HOST_NAME_PATTERN = r"^[a-zA-Z0-9.-]+$"

    class Service:
        """Service configuration constants."""

        # CONSUME from single source - NO DUPLICATION
        DEFAULT_TIMEOUT = FlextConstants.Defaults.TIMEOUT
        DEFAULT_MAX_WORKERS = 10
        MIN_WORKERS = 1
        MAX_WORKERS = 100
        MIN_REQUIRED_ARGS = 2

    class GrpcValidation:
        """gRPC validation limits and patterns."""

        MAX_SERVICE_NAME_LENGTH = 255
        MAX_METHOD_NAME_LENGTH = 200
        MIN_TIMEOUT_SECONDS = 0.1
        MAX_TIMEOUT_SECONDS = 600.0

    class Config:
        """Default configuration templates."""

        DEFAULT_CONFIG: ClassVar[FlextTypes.Core.Dict] = {
            "host": FlextConstants.Infrastructure.DEFAULT_HOST,
            "port": 50051,
            "timeout": FlextConstants.Defaults.TIMEOUT,
            "max_workers": 10,
        }


class FlextGrpcConstants(FlextGrpcSemanticConstants):
    """gRPC constants with backward compatibility.

    Legacy compatibility layer providing both modern semantic access
    and traditional flat constant access patterns for smooth migration.
    """

    # Modern semantic access (Primary API) - direct references
    GrpcNetwork = FlextGrpcSemanticConstants.GrpcNetwork
    Service = FlextGrpcSemanticConstants.Service
    GrpcValidation = FlextGrpcSemanticConstants.GrpcValidation
    Config = FlextGrpcSemanticConstants.Config

    # Legacy compatibility - flat access patterns (DEPRECATED - use semantic access)
    DEFAULT_HOST = FlextGrpcSemanticConstants.GrpcNetwork.DEFAULT_HOST
    DEFAULT_PORT = FlextGrpcSemanticConstants.GrpcNetwork.DEFAULT_PORT
    MIN_PORT = FlextGrpcSemanticConstants.GrpcNetwork.MIN_PORT
    MAX_PORT = FlextGrpcSemanticConstants.GrpcNetwork.MAX_PORT
    HOST_NAME_PATTERN = FlextGrpcSemanticConstants.GrpcNetwork.HOST_NAME_PATTERN

    DEFAULT_TIMEOUT = FlextGrpcSemanticConstants.Service.DEFAULT_TIMEOUT
    DEFAULT_MAX_WORKERS = FlextGrpcSemanticConstants.Service.DEFAULT_MAX_WORKERS
    MIN_WORKERS = FlextGrpcSemanticConstants.Service.MIN_WORKERS
    MAX_WORKERS = FlextGrpcSemanticConstants.Service.MAX_WORKERS
    MIN_REQUIRED_ARGS = FlextGrpcSemanticConstants.Service.MIN_REQUIRED_ARGS

    MAX_SERVICE_NAME_LENGTH = (
        FlextGrpcSemanticConstants.GrpcValidation.MAX_SERVICE_NAME_LENGTH
    )
    MAX_METHOD_NAME_LENGTH = (
        FlextGrpcSemanticConstants.GrpcValidation.MAX_METHOD_NAME_LENGTH
    )
    MIN_TIMEOUT_SECONDS = FlextGrpcSemanticConstants.GrpcValidation.MIN_TIMEOUT_SECONDS
    MAX_TIMEOUT_SECONDS = FlextGrpcSemanticConstants.GrpcValidation.MAX_TIMEOUT_SECONDS

    DEFAULT_CONFIG = FlextGrpcSemanticConstants.Config.DEFAULT_CONFIG


# =============================================================================
# LEGACY CONSTANTS - Backward compatibility module-level aliases
# =============================================================================

# Network configuration constants (DEPRECATED - use FlextGrpcConstants.GrpcNetwork.*)
FLEXT_GRPC_DEFAULT_HOST = FlextGrpcSemanticConstants.GrpcNetwork.DEFAULT_HOST
FLEXT_GRPC_DEFAULT_PORT = FlextGrpcSemanticConstants.GrpcNetwork.DEFAULT_PORT
FLEXT_GRPC_MIN_PORT = FlextGrpcSemanticConstants.GrpcNetwork.MIN_PORT
FLEXT_GRPC_MAX_PORT = FlextGrpcSemanticConstants.GrpcNetwork.MAX_PORT
FLEXT_GRPC_HOST_NAME_PATTERN = FlextGrpcSemanticConstants.GrpcNetwork.HOST_NAME_PATTERN

# Service configuration constants (DEPRECATED - use FlextGrpcConstants.Service.*)
FLEXT_GRPC_DEFAULT_TIMEOUT = FlextGrpcSemanticConstants.Service.DEFAULT_TIMEOUT
FLEXT_GRPC_DEFAULT_MAX_WORKERS = FlextGrpcSemanticConstants.Service.DEFAULT_MAX_WORKERS
FLEXT_GRPC_MIN_WORKERS = FlextGrpcSemanticConstants.Service.MIN_WORKERS
FLEXT_GRPC_MAX_WORKERS = FlextGrpcSemanticConstants.Service.MAX_WORKERS

# Validation rule constants (DEPRECATED - use FlextGrpcConstants.GrpcValidation.*)
FLEXT_GRPC_MAX_SERVICE_NAME_LENGTH = (
    FlextGrpcSemanticConstants.GrpcValidation.MAX_SERVICE_NAME_LENGTH
)
FLEXT_GRPC_MAX_METHOD_NAME_LENGTH = (
    FlextGrpcSemanticConstants.GrpcValidation.MAX_METHOD_NAME_LENGTH
)
FLEXT_GRPC_MIN_TIMEOUT_SECONDS = (
    FlextGrpcSemanticConstants.GrpcValidation.MIN_TIMEOUT_SECONDS
)
FLEXT_GRPC_MAX_TIMEOUT_SECONDS = (
    FlextGrpcSemanticConstants.GrpcValidation.MAX_TIMEOUT_SECONDS
)

# Configuration constants (DEPRECATED - use FlextGrpcConstants.Config.*)
FLEXT_GRPC_DEFAULT_CONFIG = FlextGrpcSemanticConstants.Config.DEFAULT_CONFIG

# =============================================================================
# EXPORTS
# =============================================================================

__all__: FlextTypes.Core.StringList = [
    "FLEXT_GRPC_DEFAULT_CONFIG",
    "FLEXT_GRPC_DEFAULT_HOST",
    "FLEXT_GRPC_DEFAULT_MAX_WORKERS",
    "FLEXT_GRPC_DEFAULT_PORT",
    "FLEXT_GRPC_DEFAULT_TIMEOUT",
    "FLEXT_GRPC_HOST_NAME_PATTERN",
    "FLEXT_GRPC_MAX_METHOD_NAME_LENGTH",
    "FLEXT_GRPC_MAX_PORT",
    "FLEXT_GRPC_MAX_SERVICE_NAME_LENGTH",
    "FLEXT_GRPC_MAX_TIMEOUT_SECONDS",
    "FLEXT_GRPC_MAX_WORKERS",
    "FLEXT_GRPC_MIN_PORT",
    "FLEXT_GRPC_MIN_TIMEOUT_SECONDS",
    "FLEXT_GRPC_MIN_WORKERS",
    "FlextGrpcConstants",
    "FlextGrpcSemanticConstants",
]
