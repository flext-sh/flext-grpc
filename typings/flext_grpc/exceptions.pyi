from collections.abc import Mapping
from enum import Enum

from flext_core import FlextError
from flext_core.exceptions import FlextErrorMixin

__all__ = [
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

class FlextGrpcErrorCodes(Enum):
    GRPC_ERROR = "GRPC_ERROR"
    GRPC_VALIDATION_ERROR = "GRPC_VALIDATION_ERROR"
    GRPC_CONNECTION_ERROR = "GRPC_CONNECTION_ERROR"
    GRPC_TIMEOUT_ERROR = "GRPC_TIMEOUT_ERROR"
    GRPC_CONFIGURATION_ERROR = "GRPC_CONFIGURATION_ERROR"
    GRPC_CHANNEL_ERROR = "GRPC_CHANNEL_ERROR"
    GRPC_SERVICE_ERROR = "GRPC_SERVICE_ERROR"
    GRPC_STREAM_ERROR = "GRPC_STREAM_ERROR"

class FlextGrpcError(FlextError, FlextErrorMixin): ...
class FlextGrpcValidationError(FlextGrpcError): ...
class FlextGrpcConnectionError(FlextGrpcError): ...
class FlextGrpcTimeoutError(FlextGrpcError): ...
class FlextGrpcConfigurationError(FlextGrpcError): ...
class FlextGrpcChannelError(FlextGrpcError): ...
class FlextGrpcServiceError(FlextGrpcError): ...
class FlextGrpcStreamError(FlextGrpcError): ...

class FlextGrpcFieldValidationError(FlextGrpcValidationError):
    def __init__(
        self,
        message: str,
        *,
        field_name: str | None = None,
        field_value: object | None = None,
        validation_rule: str | None = None,
        entity_type: str | None = None,
        code: FlextGrpcErrorCodes | None = ...,
        context: Mapping[str, object] | None = None,
    ) -> None: ...

class FlextGrpcChannelOperationError(FlextGrpcChannelError):
    def __init__(
        self,
        message: str,
        *,
        channel_target: str | None = None,
        channel_state: str | None = None,
        operation: str | None = None,
        retry_count: int | None = None,
        timeout_seconds: float | None = None,
        code: FlextGrpcErrorCodes | None = ...,
        context: Mapping[str, object] | None = None,
    ) -> None: ...

class FlextGrpcConfigError(FlextGrpcConfigurationError):
    def __init__(
        self,
        message: str,
        *,
        config_key: str | None = None,
        config_value: object | None = None,
        config_section: str | None = None,
        valid_range: str | None = None,
        code: FlextGrpcErrorCodes | None = ...,
        context: Mapping[str, object] | None = None,
    ) -> None: ...
