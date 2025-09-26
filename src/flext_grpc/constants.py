"""FLEXT gRPC Constants.

gRPC-specific constants including network settings, service configuration,
validation rules, and configuration defaults. Designed for consistent
configuration management and enterprise deployment standards.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Final

from flext_core import FlextConstants, FlextTypes


class FlextGrpcConstants(FlextConstants):
    """gRPC-specific constants following FLEXT unified single-class pattern.

    Inherits from FlextConstants for universal constants, defines only
    gRPC-specific constants using nested namespace classes.

    Layer N Foundation: gRPC domain-specific constants building on flext-core Layer 0.

    Usage:
        ```python
        from flext_grpc import FlextGrpcConstants

        timeout = FlextGrpcConstants.Service.DEFAULT_TIMEOUT
        port = FlextGrpcConstants.Network.DEFAULT_PORT
        ```
    """

    # Project metadata (Final attributes inherited from FlextConstants)
    # CONSTANTS_VERSION, PROJECT_PREFIX, PROJECT_NAME inherited from FlextConstants

    class Network:
        """gRPC network configuration constants."""

        # Use FlextConstants for common network patterns
        DEFAULT_HOST: Final[str] = FlextConstants.Platform.DEFAULT_HOST
        MIN_PORT: Final[int] = FlextConstants.Network.MIN_PORT
        MAX_PORT: Final[int] = FlextConstants.Network.MAX_PORT

        # gRPC-specific network constants
        DEFAULT_PORT: Final[int] = 50051  # Standard gRPC port
        HOST_NAME_PATTERN: Final[str] = r"^[a-zA-Z0-9.-]+$"

    class Service:
        """gRPC service configuration constants."""

        # Use FlextConstants for common service patterns
        DEFAULT_TIMEOUT: Final[int] = FlextConstants.Network.DEFAULT_TIMEOUT

        # gRPC-specific service constants
        DEFAULT_MAX_WORKERS: Final[int] = FlextConstants.Container.MAX_WORKERS
        MIN_WORKERS: Final[int] = FlextConstants.Container.MIN_WORKERS
        MAX_WORKERS: Final[int] = 100
        MIN_REQUIRED_ARGS: Final[int] = 2

    class Validation:
        """gRPC validation constants."""

        # Use FlextConstants for common validation patterns
        MIN_TIMEOUT_SECONDS: Final[float] = 0.1
        MAX_TIMEOUT_SECONDS: Final[float] = (
            FlextConstants.Performance.MAX_TIMEOUT_SECONDS
        )

        # gRPC-specific validation constants
        MAX_SERVICE_NAME_LENGTH: Final[int] = 255
        MAX_METHOD_NAME_LENGTH: Final[int] = 200

    class Messages:
        """gRPC-specific error and status messages."""

        SERVICE_START_FAILED: Final[str] = "gRPC service failed to start: {error}"
        SERVICE_STARTED: Final[str] = "gRPC service started on {host}:{port}"
        CONNECTION_FAILED: Final[str] = "gRPC connection failed: {error}"
        TIMEOUT_ERROR: Final[str] = "gRPC operation timed out after {timeout}s"

    class Errors:
        """gRPC-specific error codes extending FlextConstants.Errors."""

        # Compose with FlextConstants base errors
        BASE_ERROR: Final[str] = f"GRPC_{FlextConstants.Errors.VALIDATION_ERROR}"

        # gRPC-specific errors
        GRPC_SERVICE_ERROR: Final[str] = "GRPC_SERVICE_ERROR"
        GRPC_CONNECTION_ERROR: Final[str] = "GRPC_CONNECTION_ERROR"
        GRPC_TIMEOUT_ERROR: Final[str] = "GRPC_TIMEOUT_ERROR"


__all__: FlextTypes.Core.StringList = [
    "FlextGrpcConstants",
]
