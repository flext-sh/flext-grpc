"""FLEXT gRPC Constants - Enterprise configuration constants and validation rules.

This module provides comprehensive constants for the FLEXT gRPC platform,
extending the flext-core constant foundation with domain-specific values,
validation rules, and configuration defaults. Designed for consistent
configuration management and enterprise deployment standards.

Constant Categories:
    The FLEXT gRPC constants are organized into functional categories:
    - Network Constants: Host, port, and network configuration defaults
    - Service Constants: Worker, timeout, and service configuration limits
    - Validation Constants: String length limits and validation rules
    - Operation Constants: Service operation and argument requirements
    - Pattern Constants: Regular expressions for validation
    - Default Configurations: Complete configuration templates

Enterprise Standards:
    All constants follow enterprise deployment standards:
    - Security-compliant defaults (non-privileged ports, reasonable timeouts)
    - Performance-optimized values (appropriate worker counts, timeouts)
    - Validation rules that prevent common configuration errors
    - Backward compatibility through legacy constant aliases
    - Consistent naming conventions across the FLEXT ecosystem

Configuration Philosophy:
    Constants provide sensible defaults while enabling customization:
    - Development-friendly defaults (localhost, standard ports)
    - Production-ready limits (worker counts, timeout ranges)
    - Validation boundaries that prevent resource exhaustion
    - Extensible patterns that support enterprise requirements

Example:
    Using FLEXT gRPC constants for configuration:

    >>> from flext_grpc.constants import FlextGrpcConstants
    >>>
    >>> # Use constants for validation
    >>> def validate_port(port: int) -> bool:
    ...     return FlextGrpcConstants.MIN_PORT <= port <= FlextGrpcConstants.MAX_PORT
    >>>
    >>> # Use default configuration template
    >>> config_template = FlextGrpcConstants.DEFAULT_CONFIG
    >>> print(f"Default: {config_template['host']}:{config_template['port']}")
    Default: localhost:50051
    >>>
    >>> # Validate service names
    >>> def validate_service_name(name: str) -> bool:
    ...     return len(name) <= FlextGrpcConstants.MAX_SERVICE_NAME_LENGTH

Integration:
    - Extends flext-core constants for ecosystem consistency
    - Used throughout platform for validation and defaults
    - Supports enterprise configuration management systems
    - Enables consistent behavior across all gRPC operations

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import ClassVar

from flext_core.constants import FlextConstants

# =============================================================================
# GRPC-SPECIFIC SEMANTIC CONSTANTS - Modern Python 3.13 Structure
# =============================================================================


class FlextGrpcSemanticConstants(FlextConstants):
    """gRPC-specific semantic constants extending FlextConstants.

    Modern Python 3.13 constants following semantic grouping patterns.
    Extends the FLEXT ecosystem constants with gRPC communication specific
    values while maintaining full backward compatibility.
    """

    class Network:
        """Network configuration constants."""

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

    class Validation:
        """Validation limits and patterns."""

        MAX_SERVICE_NAME_LENGTH = 255
        MAX_METHOD_NAME_LENGTH = 200
        MIN_TIMEOUT_SECONDS = 0.1
        MAX_TIMEOUT_SECONDS = 600.0

    class Config:
        """Default configuration templates."""

        DEFAULT_CONFIG: ClassVar[dict[str, object]] = {
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
    Network = FlextGrpcSemanticConstants.Network
    Service = FlextGrpcSemanticConstants.Service
    Validation = FlextGrpcSemanticConstants.Validation
    Config = FlextGrpcSemanticConstants.Config

    # Legacy compatibility - flat access patterns (DEPRECATED - use semantic access)
    DEFAULT_HOST = FlextGrpcSemanticConstants.Network.DEFAULT_HOST
    DEFAULT_PORT = FlextGrpcSemanticConstants.Network.DEFAULT_PORT
    MIN_PORT = FlextGrpcSemanticConstants.Network.MIN_PORT
    MAX_PORT = FlextGrpcSemanticConstants.Network.MAX_PORT
    HOST_NAME_PATTERN = FlextGrpcSemanticConstants.Network.HOST_NAME_PATTERN

    DEFAULT_TIMEOUT = FlextGrpcSemanticConstants.Service.DEFAULT_TIMEOUT
    DEFAULT_MAX_WORKERS = FlextGrpcSemanticConstants.Service.DEFAULT_MAX_WORKERS
    MIN_WORKERS = FlextGrpcSemanticConstants.Service.MIN_WORKERS
    MAX_WORKERS = FlextGrpcSemanticConstants.Service.MAX_WORKERS
    MIN_REQUIRED_ARGS = FlextGrpcSemanticConstants.Service.MIN_REQUIRED_ARGS

    MAX_SERVICE_NAME_LENGTH = (
        FlextGrpcSemanticConstants.Validation.MAX_SERVICE_NAME_LENGTH
    )
    MAX_METHOD_NAME_LENGTH = (
        FlextGrpcSemanticConstants.Validation.MAX_METHOD_NAME_LENGTH
    )
    MIN_TIMEOUT_SECONDS = FlextGrpcSemanticConstants.Validation.MIN_TIMEOUT_SECONDS
    MAX_TIMEOUT_SECONDS = FlextGrpcSemanticConstants.Validation.MAX_TIMEOUT_SECONDS

    DEFAULT_CONFIG = FlextGrpcSemanticConstants.Config.DEFAULT_CONFIG


# =============================================================================
# LEGACY CONSTANTS - Backward compatibility module-level aliases
# =============================================================================

# Network configuration constants (DEPRECATED - use FlextGrpcConstants.Network.*)
FLEXT_GRPC_DEFAULT_HOST = FlextGrpcSemanticConstants.Network.DEFAULT_HOST
FLEXT_GRPC_DEFAULT_PORT = FlextGrpcSemanticConstants.Network.DEFAULT_PORT
FLEXT_GRPC_MIN_PORT = FlextGrpcSemanticConstants.Network.MIN_PORT
FLEXT_GRPC_MAX_PORT = FlextGrpcSemanticConstants.Network.MAX_PORT
FLEXT_GRPC_HOST_NAME_PATTERN = FlextGrpcSemanticConstants.Network.HOST_NAME_PATTERN

# Service configuration constants (DEPRECATED - use FlextGrpcConstants.Service.*)
FLEXT_GRPC_DEFAULT_TIMEOUT = FlextGrpcSemanticConstants.Service.DEFAULT_TIMEOUT
FLEXT_GRPC_DEFAULT_MAX_WORKERS = FlextGrpcSemanticConstants.Service.DEFAULT_MAX_WORKERS
FLEXT_GRPC_MIN_WORKERS = FlextGrpcSemanticConstants.Service.MIN_WORKERS
FLEXT_GRPC_MAX_WORKERS = FlextGrpcSemanticConstants.Service.MAX_WORKERS

# Validation rule constants (DEPRECATED - use FlextGrpcConstants.Validation.*)
FLEXT_GRPC_MAX_SERVICE_NAME_LENGTH = (
    FlextGrpcSemanticConstants.Validation.MAX_SERVICE_NAME_LENGTH
)
FLEXT_GRPC_MAX_METHOD_NAME_LENGTH = (
    FlextGrpcSemanticConstants.Validation.MAX_METHOD_NAME_LENGTH
)
FLEXT_GRPC_MIN_TIMEOUT_SECONDS = (
    FlextGrpcSemanticConstants.Validation.MIN_TIMEOUT_SECONDS
)
FLEXT_GRPC_MAX_TIMEOUT_SECONDS = (
    FlextGrpcSemanticConstants.Validation.MAX_TIMEOUT_SECONDS
)

# Configuration constants (DEPRECATED - use FlextGrpcConstants.Config.*)
FLEXT_GRPC_DEFAULT_CONFIG = FlextGrpcSemanticConstants.Config.DEFAULT_CONFIG

# =============================================================================
# EXPORTS
# =============================================================================

__all__: list[str] = [
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
