"""FLEXT gRPC Errors - Custom exception hierarchy for gRPC operations.

Error classes follow flext-core FlextExceptions patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_core import FlextExceptions


class FlextGrpcError(FlextExceptions.BaseError):
    """Base error for all gRPC-related errors."""


class FlextGrpcValidationError(FlextExceptions.BaseError):
    """Validation error for gRPC request/response validation."""

    def __init__(self, message: str, *, field: str | None = None) -> None:
        """Initialize with optional field name."""
        super().__init__(message)
        self.field = field


class FlextGrpcConnectionError(FlextExceptions.BaseError):
    """Connection error for gRPC channel failures."""


class FlextGrpcTimeoutError(FlextExceptions.BaseError):
    """Timeout error for gRPC operations that exceed time limits."""


class FlextGrpcSettingsurationError(FlextExceptions.BaseError):
    """Configuration error for gRPC settings issues."""

    def __init__(self, message: str, *, config_key: str | None = None) -> None:
        """Initialize with optional config key."""
        super().__init__(message)
        self.config_key = config_key


__all__ = [
    "FlextGrpcConnectionError",
    "FlextGrpcError",
    "FlextGrpcSettingsurationError",
    "FlextGrpcTimeoutError",
    "FlextGrpcValidationError",
]
