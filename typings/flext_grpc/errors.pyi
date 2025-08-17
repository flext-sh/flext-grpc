from _typeshed import Incomplete
from flext_core import (
    FlextConfigurationError,
    FlextConnectionError,
    FlextError,
    FlextTimeoutError,
    FlextValidationError,
)

__all__ = [
    "FlextGrpcConfigurationError",
    "FlextGrpcConnectionError",
    "FlextGrpcError",
    "FlextGrpcTimeoutError",
    "FlextGrpcValidationError",
]

class FlextGrpcError(FlextError): ...

class FlextGrpcValidationError(FlextValidationError):
    field_name: Incomplete
    def __init__(self, message: str, field_name: str | None = None) -> None: ...

class FlextGrpcConnectionError(FlextConnectionError): ...
class FlextGrpcTimeoutError(FlextTimeoutError): ...

class FlextGrpcConfigurationError(FlextConfigurationError):
    config_key: Incomplete
    config_value: Incomplete
    def __init__(
        self, message: str, config_key: str | None = None, config_value: object = None
    ) -> None: ...
