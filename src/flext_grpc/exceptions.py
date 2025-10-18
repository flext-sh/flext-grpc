"""FLEXT gRPC Exceptions - gRPC-specific error hierarchy.

Extends FlextExceptions with gRPC-specific error types following
FLEXT structured exception patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_core import FlextExceptions

from flext_grpc.constants import FlextGrpcConstants


class FlextGrpcExceptions(FlextExceptions):
    """gRPC-specific exceptions extending FlextExceptions.

    Provides gRPC-specific error types with structured error handling,
    correlation IDs, and metadata for comprehensive error management
    in gRPC operations.
    """

    class GrpcError(FlextExceptions.BaseError):
        """Base class for gRPC-specific errors."""

        def __init__(self, message: str, **kwargs: object) -> None:
            super().__init__(
                message,
                error_code=FlextGrpcConstants.GrpcErrors.GRPC_BASE_ERROR,
                **kwargs,
            )

    class GrpcConfigurationError(GrpcError):
        """Configuration-related gRPC errors."""

        def __init__(
            self,
            message: str,
            config_key: str | None = None,
            config_value: object = None,
            **kwargs: object,
        ) -> None:
            super().__init__(
                message, error_code=FlextGrpcConstants.GrpcErrors.CONFIG_ERROR, **kwargs
            )
            self.config_key = config_key
            self.config_value = config_value

    class GrpcConnectionError(GrpcError):
        """Connection-related gRPC errors."""

        def __init__(self, message: str, **kwargs: object) -> None:
            super().__init__(
                message,
                error_code=FlextGrpcConstants.GrpcErrors.CONNECTION_ERROR,
                **kwargs,
            )

    class GrpcTimeoutError(GrpcError):
        """Timeout-related gRPC errors."""

        def __init__(self, message: str, **kwargs: object) -> None:
            super().__init__(
                message,
                error_code=FlextGrpcConstants.GrpcErrors.TIMEOUT_ERROR,
                **kwargs,
            )

    class GrpcValidationError(GrpcError):
        """Validation-related gRPC errors."""

        def __init__(
            self,
            message: str,
            field_name: str | None = None,
            value: object = None,
            **kwargs: object,
        ) -> None:
            super().__init__(
                message,
                error_code=FlextGrpcConstants.GrpcErrors.VALIDATION_ERROR,
                **kwargs,
            )
            self.field_name = field_name
            self.value = value

    class GrpcServerError(GrpcError):
        """Server-related gRPC errors."""

        def __init__(self, message: str, **kwargs: object) -> None:
            super().__init__(
                message, error_code=FlextGrpcConstants.GrpcErrors.SERVER_ERROR, **kwargs
            )

    class GrpcClientError(GrpcError):
        """Client-related gRPC errors."""

        def __init__(self, message: str, **kwargs: object) -> None:
            super().__init__(
                message, error_code=FlextGrpcConstants.GrpcErrors.CLIENT_ERROR, **kwargs
            )

    class GrpcStreamError(GrpcError):
        """Stream-related gRPC errors."""

        def __init__(self, message: str, **kwargs: object) -> None:
            super().__init__(
                message, error_code=FlextGrpcConstants.GrpcErrors.STREAM_ERROR, **kwargs
            )

    class GrpcProtocolError(GrpcError):
        """Protocol-related gRPC errors."""

        def __init__(self, message: str, **kwargs: object) -> None:
            super().__init__(
                message,
                error_code=FlextGrpcConstants.GrpcErrors.PROTOCOL_ERROR,
                **kwargs,
            )


# Alias for backward compatibility
FlextGrpcConfigurationError = FlextGrpcExceptions.GrpcConfigurationError
FlextGrpcConnectionError = FlextGrpcExceptions.GrpcConnectionError
FlextGrpcError = FlextGrpcExceptions.GrpcError
FlextGrpcTimeoutError = FlextGrpcExceptions.GrpcTimeoutError
FlextGrpcValidationError = FlextGrpcExceptions.GrpcValidationError

__all__ = [
    "FlextGrpcConfigurationError",
    "FlextGrpcConnectionError",
    "FlextGrpcError",
    "FlextGrpcExceptions",
    "FlextGrpcTimeoutError",
    "FlextGrpcValidationError",
]
