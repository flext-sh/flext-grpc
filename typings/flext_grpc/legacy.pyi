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

__all__ = [
    "GRPC_DEFAULT_HOST",
    "GRPC_DEFAULT_PORT",
    "GRPC_DEFAULT_TIMEOUT",
    "GRPC_DEFAULT_WORKERS",
    "GrpcChannelError",
    "GrpcChannelErrorParams",
    "GrpcConfigurationError",
    "GrpcConfigurationErrorParams",
    "GrpcConnectionError",
    "GrpcError",
    "GrpcServiceError",
    "GrpcStreamError",
    "GrpcTimeoutError",
    "GrpcValidationError",
    "GrpcValidationErrorParams",
    "create_grpc_client",
    "create_grpc_config",
    "create_grpc_server",
    "setup_grpc_platform",
    "simple_grpc_call",
]

def GrpcError(*args: object, **kwargs: object) -> FlextGrpcError: ...
def GrpcValidationError(
    *args: object, **kwargs: object
) -> FlextGrpcValidationError: ...
def GrpcConnectionError(
    *args: object, **kwargs: object
) -> FlextGrpcConnectionError: ...
def GrpcTimeoutError(*args: object, **kwargs: object) -> FlextGrpcTimeoutError: ...
def GrpcConfigurationError(
    *args: object, **kwargs: object
) -> FlextGrpcConfigurationError: ...
def GrpcChannelError(*args: object, **kwargs: object) -> FlextGrpcChannelError: ...
def GrpcServiceError(*args: object, **kwargs: object) -> FlextGrpcServiceError: ...
def GrpcStreamError(*args: object, **kwargs: object) -> FlextGrpcStreamError: ...
def create_grpc_client(*args: object, **kwargs: object) -> object: ...
def create_grpc_server(*args: object, **kwargs: object) -> object: ...
def create_grpc_config(*args: object, **kwargs: object) -> object: ...
def setup_grpc_platform(*args: object, **kwargs: object) -> object: ...
def simple_grpc_call(*args: object, **kwargs: object) -> object: ...

GRPC_DEFAULT_HOST: str
GRPC_DEFAULT_PORT: int
GRPC_DEFAULT_WORKERS: int
GRPC_DEFAULT_TIMEOUT: float

def GrpcValidationErrorParams(*args: object, **kwargs: object) -> dict[str, object]: ...
def GrpcConfigurationErrorParams(
    *args: object, **kwargs: object
) -> dict[str, object]: ...
def GrpcChannelErrorParams(*args: object, **kwargs: object) -> dict[str, object]: ...
