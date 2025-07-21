"""DEPRECATED: Legacy gRPC error handling utilities for FLEXT gRPC.

This module is deprecated in favor of the BaseGrpcService patterns from flext-core.
New code should use flext_core.infrastructure.grpc_base.BaseGrpcService instead.

The error handling functions in this module use the old pattern of directly
manipulating gRPC context, which is inconsistent with the BaseGrpcService
execute_with_error_handling pattern.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import warnings
from typing import TYPE_CHECKING

import grpc
from flext_observability.logging import get_logger

if TYPE_CHECKING:
    from flext_grpc.types import ServicerContext

logger = get_logger(__name__)


def handle_grpc_error(
    context: ServicerContext,
    error: Exception,
    operation: str,
) -> None:
    """DEPRECATED: Handle gRPC errors with proper logging and status codes.

    This function is deprecated. Use BaseGrpcService.execute_with_error_handling
    instead.

    Args:
        context: gRPC service context
        error: Exception that occurred
        operation: Description of the operation that failed

    """
    warnings.warn(
        "handle_grpc_error is deprecated. Use "
        "BaseGrpcService.execute_with_error_handling instead",
        DeprecationWarning,
        stacklevel=2,
    )

    logger.error("gRPC %s failed", operation, extra={"error": str(error)})

    # Map common exception types to appropriate gRPC status codes
    if isinstance(error, ValueError):
        context.set_code(grpc.StatusCode.INVALID_ARGUMENT.value[0])
    elif isinstance(error, PermissionError):
        context.set_code(grpc.StatusCode.PERMISSION_DENIED.value[0])
    elif isinstance(error, FileNotFoundError):
        context.set_code(grpc.StatusCode.NOT_FOUND.value[0])
    elif isinstance(error, TimeoutError):
        context.set_code(grpc.StatusCode.DEADLINE_EXCEEDED.value[0])
    else:
        context.set_code(internal.invalid.value[0])

    context.set_details(f"{operation} failed: {error}")


def handle_validation_error(
    context: ServicerContext,
    field_name: str,
    error_message: str,
) -> None:
    """DEPRECATED: Handle validation errors with specific field information.

    This function is deprecated. Use BaseGrpcService.execute_with_error_handling
    instead.

    Args:
        context: gRPC service context
        field_name: Name of the field that failed validation
        error_message: Specific validation error message

    """
    warnings.warn(
        "handle_validation_error is deprecated. Use "
        "BaseGrpcService.execute_with_error_handling instead",
        DeprecationWarning,
        stacklevel=2,
    )

    logger.warning("Validation failed for field '%s': %s", field_name, error_message)
    context.set_code(grpc.StatusCode.INVALID_ARGUMENT.value[0])
    context.set_details(f"Validation failed for {field_name}: {error_message}")


def handle_not_found_error(
    context: ServicerContext,
    resource_type: str,
    resource_id: str,
) -> None:
    """DEPRECATED: Handle resource not found errors.

    This function is deprecated. Use BaseGrpcService.execute_with_error_handling
    instead.

    Args:
        context: gRPC service context
        resource_type: Type of resource (e.g., "pipeline", "execution")
        resource_id: ID of the resource that wasn't found

    """
    warnings.warn(
        "handle_not_found_error is deprecated. Use "
        "BaseGrpcService.execute_with_error_handling instead",
        DeprecationWarning,
        stacklevel=2,
    )

    logger.warning("%s not found: %s", resource_type, resource_id)
    context.set_code(grpc.StatusCode.NOT_FOUND.value[0])
    context.set_details(f"{resource_type} with ID '{resource_id}' not found")
