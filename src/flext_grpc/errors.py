"""FLEXT gRPC Errors - Minimal domain-specific errors using flext-core.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import (
    FlextConfigurationError,
    FlextConnectionError,
    FlextError,
    FlextTimeoutError,
    FlextValidationError,
)

# =============================================================================
# MINIMAL GRPC-SPECIFIC ERRORS - NO DUPLICATION
# =============================================================================


class FlextGrpcError(FlextError):
    """Base gRPC error - only for gRPC-specific functionality."""


class FlextGrpcValidationError(FlextValidationError):
    """gRPC validation error with field context."""

    def __init__(self, message: str, field_name: str | None = None) -> None:
        super().__init__(message)
        self.field_name = field_name


class FlextGrpcConnectionError(FlextConnectionError):
    """gRPC connection error with channel context."""


class FlextGrpcTimeoutError(FlextTimeoutError):
    """gRPC timeout error with deadline context."""


class FlextGrpcConfigurationError(FlextConfigurationError):
    """gRPC configuration error with config context."""

    def __init__(
        self,
        message: str,
        config_key: str | None = None,
        config_value: object = None,
    ) -> None:
        super().__init__(message)
        self.config_key = config_key
        self.config_value = config_value

# =============================================================================
# EXPORTS - Only minimal gRPC-specific errors
# =============================================================================


__all__ = [
    "FlextGrpcConfigurationError",
    "FlextGrpcConnectionError",
    "FlextGrpcError",
    "FlextGrpcTimeoutError",
    "FlextGrpcValidationError",
]
