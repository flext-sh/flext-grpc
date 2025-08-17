"""gRPC Exception Hierarchy - Modern Pydantic v2 Patterns.

This module provides gRPC-specific exceptions using modern patterns from flext-core.
All exceptions follow the FlextErrorMixin pattern with keyword-only arguments and
modern Python 3.13 type aliases for comprehensive error handling in gRPC operations.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping
from enum import Enum

from flext_core import FlextError
from flext_core.exceptions import FlextErrorMixin


class FlextGrpcErrorCodes(Enum):
    """Error codes for gRPC domain operations."""

    GRPC_ERROR = "GRPC_ERROR"
    GRPC_VALIDATION_ERROR = "GRPC_VALIDATION_ERROR"
    GRPC_CONNECTION_ERROR = "GRPC_CONNECTION_ERROR"
    GRPC_TIMEOUT_ERROR = "GRPC_TIMEOUT_ERROR"
    GRPC_CONFIGURATION_ERROR = "GRPC_CONFIGURATION_ERROR"
    GRPC_CHANNEL_ERROR = "GRPC_CHANNEL_ERROR"
    GRPC_SERVICE_ERROR = "GRPC_SERVICE_ERROR"
    GRPC_STREAM_ERROR = "GRPC_STREAM_ERROR"


# Base gRPC exception hierarchy using FlextErrorMixin pattern
class FlextGrpcError(FlextError, FlextErrorMixin):
    """Base gRPC error."""


class FlextGrpcValidationError(FlextGrpcError):
    """gRPC validation error."""


class FlextGrpcConnectionError(FlextGrpcError):
    """gRPC connection error."""


class FlextGrpcTimeoutError(FlextGrpcError):
    """gRPC timeout error."""


class FlextGrpcConfigurationError(FlextGrpcError):
    """gRPC configuration error."""


class FlextGrpcChannelError(FlextGrpcError):
    """gRPC channel error."""


class FlextGrpcServiceError(FlextGrpcError):
    """gRPC service error."""


class FlextGrpcStreamError(FlextGrpcError):
    """gRPC stream error."""


# Domain-specific exceptions for gRPC business logic
# Using modern FlextErrorMixin pattern with context support


class FlextGrpcFieldValidationError(FlextGrpcValidationError):
    """gRPC field validation errors with field context."""

    def __init__(
      self,
      message: str,
      *,
      field_name: str | None = None,
      field_value: object | None = None,
      validation_rule: str | None = None,
      entity_type: str | None = None,
      code: FlextGrpcErrorCodes | None = FlextGrpcErrorCodes.GRPC_VALIDATION_ERROR,
      context: Mapping[str, object] | None = None,
    ) -> None:
      """Initialize gRPC field validation error with field context."""
      context_dict: dict[str, object] = dict(context) if context else {}
      if field_name is not None:
          context_dict["field_name"] = field_name
      if field_value is not None:
          context_dict["field_value"] = field_value
      if validation_rule is not None:
          context_dict["validation_rule"] = validation_rule
      if entity_type is not None:
          context_dict["entity_type"] = entity_type

      super().__init__(
          message,
          code=code,
          context=context_dict,
      )


class FlextGrpcChannelOperationError(FlextGrpcChannelError):
    """gRPC channel operation errors with channel context."""

    def __init__(
      self,
      message: str,
      *,
      channel_target: str | None = None,
      channel_state: str | None = None,
      operation: str | None = None,
      retry_count: int | None = None,
      timeout_seconds: float | None = None,
      code: FlextGrpcErrorCodes | None = FlextGrpcErrorCodes.GRPC_CHANNEL_ERROR,
      context: Mapping[str, object] | None = None,
    ) -> None:
      """Initialize gRPC channel operation error with channel context."""
      context_dict: dict[str, object] = dict(context) if context else {}
      if channel_target is not None:
          context_dict["channel_target"] = channel_target
      if channel_state is not None:
          context_dict["channel_state"] = channel_state
      if operation is not None:
          context_dict["operation"] = operation
      if retry_count is not None:
          context_dict["retry_count"] = retry_count
      if timeout_seconds is not None:
          context_dict["timeout_seconds"] = timeout_seconds

      super().__init__(
          message,
          code=code,
          context=context_dict,
      )


class FlextGrpcConfigError(FlextGrpcConfigurationError):
    """gRPC configuration errors with config context."""

    def __init__(
      self,
      message: str,
      *,
      config_key: str | None = None,
      config_value: object | None = None,
      config_section: str | None = None,
      valid_range: str | None = None,
      code: FlextGrpcErrorCodes | None = FlextGrpcErrorCodes.GRPC_CONFIGURATION_ERROR,
      context: Mapping[str, object] | None = None,
    ) -> None:
      """Initialize gRPC configuration error with config context."""
      context_dict: dict[str, object] = dict(context) if context else {}
      if config_key is not None:
          context_dict["config_key"] = config_key
      if config_value is not None:
          context_dict["config_value"] = config_value
      if config_section is not None:
          context_dict["config_section"] = config_section
      if valid_range is not None:
          context_dict["valid_range"] = valid_range

      super().__init__(
          message,
          code=code,
          context=context_dict,
      )


__all__: list[str] = [
    "FlextGrpcChannelError",
    "FlextGrpcChannelOperationError",
    "FlextGrpcConfigError",
    "FlextGrpcConfigurationError",
    "FlextGrpcConnectionError",
    "FlextGrpcError",
    "FlextGrpcErrorCodes",
    "FlextGrpcFieldValidationError",
    "FlextGrpcServiceError",
    "FlextGrpcStreamError",
    "FlextGrpcTimeoutError",
    "FlextGrpcValidationError",
]
