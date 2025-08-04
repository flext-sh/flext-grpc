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


class FlextGrpcConstants(FlextConstants):
    """Enterprise gRPC constants extending flext-core platform foundation.

    Comprehensive constant definitions for the FLEXT gRPC platform providing
    configuration defaults, validation rules, and operational limits.
    Extends flext-core constants while adding gRPC-specific values for
    consistent platform behavior and enterprise deployment standards.

    This class serves as the single source of truth for all gRPC-related
    constants, ensuring consistency across entities, services, configuration,
    and validation throughout the platform.

    Constant Categories:
        - Network: Host and port configuration defaults and limits
        - Service: Worker counts, timeouts, and service operational limits
        - Validation: String length limits and format validation rules
        - Operation: Service operation requirements and argument validation
        - Pattern: Regular expressions for format validation
        - Configuration: Complete default configuration templates

    Enterprise Compliance:
        All constants follow enterprise security and performance standards:
        - Non-privileged port defaults (>= 1024) for security compliance
        - Reasonable resource limits to prevent system exhaustion
        - Performance-optimized defaults based on enterprise best practices
        - Validation boundaries that prevent common configuration errors

    Example:
        Using constants for validation and configuration:

        >>> # Port validation
        >>> def is_valid_port(port: int) -> bool:
        ...     return (
        ...         FlextGrpcConstants.MIN_PORT <= port <= FlextGrpcConstants.MAX_PORT
        ...     )
        >>>
        >>> # Worker count validation
        >>> def is_valid_workers(count: int) -> bool:
        ...     return (
        ...         FlextGrpcConstants.MIN_WORKERS
        ...         <= count
        ...         <= FlextGrpcConstants.MAX_WORKERS
        ...     )
        >>>
        >>> # Use default configuration
        >>> default_host = FlextGrpcConstants.DEFAULT_HOST
        >>> default_port = FlextGrpcConstants.DEFAULT_PORT
        >>> config = f"{default_host}:{default_port}"

    Integration:
        Constants are used throughout the platform for:
        - Entity validation and configuration
        - Service operation parameter validation
        - Configuration object initialization
        - Error message generation with consistent limits
        - Enterprise deployment configuration templates

    """

    # Network Constants - Host and port configuration standards
    DEFAULT_HOST = "localhost"  # Development-friendly default host
    DEFAULT_PORT = 50051  # Standard gRPC port (non-privileged)
    MIN_PORT = 1  # Minimum valid port number (system minimum)
    MAX_PORT = 65535  # Maximum valid port number (16-bit maximum)

    # Service Constants - Performance and resource management standards
    DEFAULT_TIMEOUT = 60  # Default operation timeout (seconds)
    DEFAULT_MAX_WORKERS = 10  # Balanced worker count for standard load
    MIN_WORKERS = 1  # Minimum workers for functional server
    MAX_WORKERS = 100  # Maximum workers to prevent resource exhaustion

    # Validation Constants - String length and value limits
    MAX_SERVICE_NAME_LENGTH = 255  # Maximum service name length (database-safe)
    MAX_METHOD_NAME_LENGTH = 200  # Maximum method name length (URL-safe)
    MIN_TIMEOUT_SECONDS = 0.1  # Minimum meaningful timeout (100ms)
    MAX_TIMEOUT_SECONDS = 600.0  # Maximum timeout (10 minutes)

    # Operation Constants - Service operation requirements
    MIN_REQUIRED_ARGS = (
        2  # Minimum arguments for service operations (operation + target)
    )

    # Validation Patterns - Regular expressions for format validation
    HOST_NAME_PATTERN = (
        r"^[a-zA-Z0-9.-]+$"  # Valid hostname pattern (alphanumeric, dots, hyphens)
    )

    # Default Configuration Template - Complete configuration with enterprise defaults
    DEFAULT_CONFIG: ClassVar[dict[str, object]] = {
        "host": DEFAULT_HOST,  # localhost for development
        "port": DEFAULT_PORT,  # 50051 (standard gRPC)
        "timeout": DEFAULT_TIMEOUT,  # 60 seconds for reliable operations
        "max_workers": DEFAULT_MAX_WORKERS,  # 10 workers for balanced performance
    }


# =============================================================================
# LEGACY CONSTANTS - Backward compatibility aliases
# =============================================================================
# These module-level constants provide backward compatibility for existing code
# while encouraging migration to the class-based constant organization.

# Network configuration constants
FLEXT_GRPC_DEFAULT_HOST = FlextGrpcConstants.DEFAULT_HOST
FLEXT_GRPC_DEFAULT_PORT = FlextGrpcConstants.DEFAULT_PORT
FLEXT_GRPC_MIN_PORT = FlextGrpcConstants.MIN_PORT
FLEXT_GRPC_MAX_PORT = FlextGrpcConstants.MAX_PORT

# Service configuration constants
FLEXT_GRPC_DEFAULT_TIMEOUT = FlextGrpcConstants.DEFAULT_TIMEOUT
FLEXT_GRPC_DEFAULT_MAX_WORKERS = FlextGrpcConstants.DEFAULT_MAX_WORKERS
FLEXT_GRPC_MIN_WORKERS = FlextGrpcConstants.MIN_WORKERS
FLEXT_GRPC_MAX_WORKERS = FlextGrpcConstants.MAX_WORKERS

# Validation rule constants
FLEXT_GRPC_MAX_SERVICE_NAME_LENGTH = FlextGrpcConstants.MAX_SERVICE_NAME_LENGTH
FLEXT_GRPC_MAX_METHOD_NAME_LENGTH = FlextGrpcConstants.MAX_METHOD_NAME_LENGTH
FLEXT_GRPC_MIN_TIMEOUT_SECONDS = FlextGrpcConstants.MIN_TIMEOUT_SECONDS
FLEXT_GRPC_MAX_TIMEOUT_SECONDS = FlextGrpcConstants.MAX_TIMEOUT_SECONDS

# Pattern and configuration constants
FLEXT_GRPC_HOST_NAME_PATTERN = FlextGrpcConstants.HOST_NAME_PATTERN
FLEXT_GRPC_DEFAULT_CONFIG = FlextGrpcConstants.DEFAULT_CONFIG

# =============================================================================
# EXPORTS
# =============================================================================

__all__: list[str] = [
    # Legacy constants for backward compatibility
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
    # Main class
    "FlextGrpcConstants",
]
