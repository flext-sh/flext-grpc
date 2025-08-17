from typing import ClassVar

from _typeshed import Incomplete
from flext_core import FlextBaseConfigModel, FlextConstants

__all__ = [
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
    "FlextGrpcConfig",
    "FlextGrpcConfigurationError",
    "FlextGrpcConstants",
    "FlextGrpcSemanticConstants",
]

class FlextGrpcSemanticConstants(FlextConstants):
    class Network:
        DEFAULT_HOST: Incomplete
        DEFAULT_PORT: int
        MIN_PORT: Incomplete
        MAX_PORT: Incomplete
        HOST_NAME_PATTERN: str

    class Service:
        DEFAULT_TIMEOUT: Incomplete
        DEFAULT_MAX_WORKERS: int
        MIN_WORKERS: int
        MAX_WORKERS: int
        MIN_REQUIRED_ARGS: int

    class Validation:
        MAX_SERVICE_NAME_LENGTH: int
        MAX_METHOD_NAME_LENGTH: int
        MIN_TIMEOUT_SECONDS: float
        MAX_TIMEOUT_SECONDS: float

    class Config:
        DEFAULT_CONFIG: ClassVar[dict[str, object]]

class FlextGrpcConstants(FlextGrpcSemanticConstants):
    Network = FlextGrpcSemanticConstants.Network
    Service = FlextGrpcSemanticConstants.Service
    Validation = FlextGrpcSemanticConstants.Validation
    Config = FlextGrpcSemanticConstants.Config
    DEFAULT_HOST: Incomplete
    DEFAULT_PORT: Incomplete
    MIN_PORT: Incomplete
    MAX_PORT: Incomplete
    HOST_NAME_PATTERN: Incomplete
    DEFAULT_TIMEOUT: Incomplete
    DEFAULT_MAX_WORKERS: Incomplete
    MIN_WORKERS: Incomplete
    MAX_WORKERS: Incomplete
    MIN_REQUIRED_ARGS: Incomplete
    MAX_SERVICE_NAME_LENGTH: Incomplete
    MAX_METHOD_NAME_LENGTH: Incomplete
    MIN_TIMEOUT_SECONDS: Incomplete
    MAX_TIMEOUT_SECONDS: Incomplete
    DEFAULT_CONFIG: Incomplete

FLEXT_GRPC_DEFAULT_HOST: Incomplete
FLEXT_GRPC_DEFAULT_PORT: Incomplete
FLEXT_GRPC_MIN_PORT: Incomplete
FLEXT_GRPC_MAX_PORT: Incomplete
FLEXT_GRPC_HOST_NAME_PATTERN: Incomplete
FLEXT_GRPC_DEFAULT_TIMEOUT: Incomplete
FLEXT_GRPC_DEFAULT_MAX_WORKERS: Incomplete
FLEXT_GRPC_MIN_WORKERS: Incomplete
FLEXT_GRPC_MAX_WORKERS: Incomplete
FLEXT_GRPC_MAX_SERVICE_NAME_LENGTH: Incomplete
FLEXT_GRPC_MAX_METHOD_NAME_LENGTH: Incomplete
FLEXT_GRPC_MIN_TIMEOUT_SECONDS: Incomplete
FLEXT_GRPC_MAX_TIMEOUT_SECONDS: Incomplete
FLEXT_GRPC_DEFAULT_CONFIG: Incomplete
FlextGrpcConfigurationError: Incomplete

class FlextGrpcConfig(FlextBaseConfigModel):
    host: str
    port: int
    max_workers: int
    timeout: float
    @classmethod
    def validate_host(cls, v: str) -> str: ...
    @classmethod
    def validate_port(cls, v: int) -> int: ...
    @classmethod
    def validate_max_workers(cls, v: int) -> int: ...
    @classmethod
    def validate_timeout(cls, v: float) -> float: ...
