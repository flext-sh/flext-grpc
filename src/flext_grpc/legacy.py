"""Legacy compatibility layer for flext-grpc modernization.

This module provides backward compatibility for legacy exception classes and APIs
that were refactored during the flext-core modernization. All legacy names are
maintained as facades to the new FlextExceptions.ErrorMixin-based exceptions.

This layer will be deprecated in a future version. Please migrate to the new
FlextGrpc* exception classes for modern error handling patterns.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import warnings

from flext_grpc.exceptions import (
    FlextGrpcChannelError,
    FlextGrpcConfigurationError,
    FlextGrpcConnectionError,
    FlextGrpcError,
    FlextGrpcServiceError,
    FlextGrpcStreamError,
    FlextGrpcTimeoutError,
    FlextGrpcValidationError,
)

# Import modules for legacy functions
# Import availability flag - not a constant, can be reassigned
_imports_available = True
try:
    from flext_grpc import (
        FlextGrpcClient,
        FlextGrpcConfig,
        FlextGrpcPlatform,
        FlextGrpcServer,
    )
except ImportError:
    # Will be handled in individual functions
    _imports_available = False
    FlextGrpcConfig = None
    FlextGrpcClient = None
    FlextGrpcServer = None
    FlextGrpcPlatform = None


def _deprecation_warning(old_name: str, new_name: str) -> None:
    """Issue deprecation warning for legacy API usage."""
    warnings.warn(
        f"{old_name} is deprecated. Use {new_name} instead. "
        f"Legacy compatibility will be removed in a future version.",
        DeprecationWarning,
        stacklevel=3,
    )


# Legacy exception aliases following facade pattern
def GrpcError(*args: object, **kwargs: object) -> FlextGrpcError:  # noqa: N802
    """Legacy: Use FlextGrpcError instead."""
    _deprecation_warning("GrpcError", "FlextGrpcError")
    # Legacy function - use first arg as message or empty string
    message = str(args[0]) if args else kwargs.get("message", "")
    return FlextGrpcError(str(message))


def GrpcValidationError(*args: object, **kwargs: object) -> FlextGrpcValidationError:  # noqa: N802
    """Legacy: Use FlextGrpcValidationError instead."""
    _deprecation_warning("GrpcValidationError", "FlextGrpcValidationError")
    # Legacy function - use first arg as message or empty string
    message = str(args[0]) if args else kwargs.get("message", "")
    field_name_raw = kwargs.get("field_name")
    field_name = field_name_raw if isinstance(field_name_raw, str) else None
    return FlextGrpcValidationError(str(message), field_name=field_name)


def GrpcConnectionError(*args: object, **kwargs: object) -> FlextGrpcConnectionError:  # noqa: N802
    """Legacy: Use FlextGrpcConnectionError instead."""
    _deprecation_warning("GrpcConnectionError", "FlextGrpcConnectionError")
    # Legacy function - use first arg as message or empty string
    message = str(args[0]) if args else kwargs.get("message", "")
    return FlextGrpcConnectionError(str(message))


def GrpcTimeoutError(*args: object, **kwargs: object) -> FlextGrpcTimeoutError:  # noqa: N802
    """Legacy: Use FlextGrpcTimeoutError instead."""
    _deprecation_warning("GrpcTimeoutError", "FlextGrpcTimeoutError")
    # Legacy function - use first arg as message or empty string
    message = str(args[0]) if args else kwargs.get("message", "")
    return FlextGrpcTimeoutError(str(message))


def grpc_configuration_error(
    *args: object, **kwargs: object
) -> FlextGrpcConfigurationError:
    """Legacy: Use FlextGrpcConfigurationError instead."""
    _deprecation_warning("GrpcConfigurationError", "FlextGrpcConfigurationError")
    # Legacy function - use first arg as message or empty string
    message = str(args[0]) if args else kwargs.get("message", "")
    config_key_raw = kwargs.get("config_key")
    config_key = config_key_raw if isinstance(config_key_raw, str) else None
    config_value = kwargs.get("config_value")
    return FlextGrpcConfigurationError(
        str(message), config_key=config_key, config_value=config_value
    )


def GrpcChannelError(*args: object, **kwargs: object) -> FlextGrpcChannelError:  # noqa: N802
    """Legacy: Use FlextGrpcChannelError instead."""
    _deprecation_warning("GrpcChannelError", "FlextGrpcChannelError")
    # Legacy function - use first arg as message or empty string
    message = str(args[0]) if args else kwargs.get("message", "")
    return FlextGrpcChannelError(str(message))


def GrpcServiceError(*args: object, **kwargs: object) -> FlextGrpcServiceError:  # noqa: N802
    """Legacy: Use FlextGrpcServiceError instead."""
    _deprecation_warning("GrpcServiceError", "FlextGrpcServiceError")
    # Legacy function - use first arg as message or empty string
    message = str(args[0]) if args else kwargs.get("message", "")
    return FlextGrpcServiceError(str(message))


def GrpcStreamError(*args: object, **kwargs: object) -> FlextGrpcStreamError:  # noqa: N802
    """Legacy: Use FlextGrpcStreamError instead."""
    _deprecation_warning("GrpcStreamError", "FlextGrpcStreamError")
    # Legacy function - use first arg as message or empty string
    message = str(args[0]) if args else kwargs.get("message", "")
    return FlextGrpcStreamError(str(message))


# Legacy API function aliases
def create_grpc_client(*_args: object, **kwargs: object) -> object:
    """Legacy: Use FlextGrpcClient directly instead."""
    if not _imports_available or FlextGrpcClient is None:
        msg = "FlextGrpcClient not available"
        raise ImportError(msg) from None
    _deprecation_warning("create_grpc_client", "FlextGrpcClient")
    # Legacy function - ignore all type checking for backward compatibility
    return FlextGrpcClient(**kwargs)


def create_grpc_server(*_args: object, **kwargs: object) -> object:
    """Legacy: Use FlextGrpcServer directly instead."""
    if not _imports_available or FlextGrpcServer is None:
        msg = "FlextGrpcServer not available"
        raise ImportError(msg) from None
    _deprecation_warning("create_grpc_server", "FlextGrpcServer")
    # Legacy function - ignore all type checking for backward compatibility
    return FlextGrpcServer(**kwargs)


def create_grpc_config(*_args: object, **kwargs: object) -> object:
    """Legacy: Use FlextGrpcConfig directly instead."""
    if not _imports_available or FlextGrpcConfig is None:
        msg = "FlextGrpcConfig not available"
        raise ImportError(msg) from None
    _deprecation_warning("create_grpc_config", "FlextGrpcConfig")
    # Legacy function - ignore all type checking for backward compatibility
    return FlextGrpcConfig(**kwargs)


def setup_grpc_platform(*_args: object, **kwargs: object) -> object:
    """Legacy: Use FlextGrpcPlatform directly instead."""
    if not _imports_available or FlextGrpcPlatform is None:
        msg = "FlextGrpcPlatform not available"
        raise ImportError(msg) from None
    _deprecation_warning("setup_grpc_platform", "FlextGrpcPlatform")
    # Legacy function - ignore all type checking for backward compatibility
    return FlextGrpcPlatform(**kwargs)


def simple_grpc_call(*args: object, **kwargs: object) -> object:
    """Legacy: Use FlextGrpcPlatform.make_call instead."""
    if not _imports_available or FlextGrpcPlatform is None:
        msg = "FlextGrpcPlatform not available"
        raise ImportError(msg) from None
    _deprecation_warning("simple_grpc_call", "FlextGrpcPlatform.make_call")
    platform = FlextGrpcPlatform()
    # Legacy function - ignore all type checking for method call
    return platform.make_call(*args, **kwargs)


# Legacy constants and configuration
GRPC_DEFAULT_HOST = "localhost"
GRPC_DEFAULT_PORT = 50051
GRPC_DEFAULT_WORKERS = 10
GRPC_DEFAULT_TIMEOUT = 30.0


# Legacy parameter factories for compatibility
def GrpcValidationErrorParams(*args: object, **kwargs: object) -> dict[str, object]:  # noqa: N802,ARG001
    """Legacy: Create parameters for GrpcValidationError - use FlextGrpcValidationError context instead."""
    _deprecation_warning(
        "GrpcValidationErrorParams", "FlextGrpcValidationError context parameter"
    )
    return {
        "field_name": kwargs.get("field_name"),
        "field_value": kwargs.get("field_value"),
        "validation_rule": kwargs.get("validation_rule"),
        "entity_type": kwargs.get("entity_type"),
    }


def GrpcConfigurationErrorParams(*args: object, **kwargs: object) -> dict[str, object]:  # noqa: N802,ARG001
    """Legacy: Create parameters for GrpcConfigurationError - use FlextGrpcConfigurationError context instead."""
    _deprecation_warning(
        "GrpcConfigurationErrorParams", "FlextGrpcConfigurationError context parameter"
    )
    return {
        "config_key": kwargs.get("config_key"),
        "config_value": kwargs.get("config_value"),
        "config_section": kwargs.get("config_section"),
        "valid_range": kwargs.get("valid_range"),
    }


def GrpcChannelErrorParams(*args: object, **kwargs: object) -> dict[str, object]:  # noqa: N802,ARG001
    """Legacy: Create parameters for GrpcChannelError - use FlextGrpcChannelError context instead."""
    _deprecation_warning(
        "GrpcChannelErrorParams", "FlextGrpcChannelError context parameter"
    )
    return {
        "channel_target": kwargs.get("channel_target"),
        "channel_state": kwargs.get("channel_state"),
        "operation": kwargs.get("operation"),
        "retry_count": kwargs.get("retry_count"),
        "timeout_seconds": kwargs.get("timeout_seconds"),
    }


__all__: list[str] = [
    # Legacy constants
    "GRPC_DEFAULT_HOST",
    "GRPC_DEFAULT_PORT",
    "GRPC_DEFAULT_TIMEOUT",
    "GRPC_DEFAULT_WORKERS",
    # Legacy exception aliases
    "GrpcChannelError",
    "GrpcChannelErrorParams",
    "GrpcConfigurationErrorParams",
    "GrpcConnectionError",
    "GrpcError",
    "GrpcServiceError",
    "GrpcStreamError",
    "GrpcTimeoutError",
    "GrpcValidationError",
    "GrpcValidationErrorParams",
    # Legacy API functions
    "create_grpc_client",
    "create_grpc_config",
    "create_grpc_server",
    "grpc_configuration_error",
    # Legacy API functions continued
    "setup_grpc_platform",
    "simple_grpc_call",
]
