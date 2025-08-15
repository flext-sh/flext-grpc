"""Enterprise gRPC Communication Platform for FLEXT ecosystem."""

from __future__ import annotations

import importlib.metadata

from flext_core import FlextContainer, FlextResult

# Import from consolidated PEP8 files
from .grpc_api import (
    create_channel,
    create_client,
    create_complete_setup,
    create_config,
    create_server,
    create_service,
    create_stream,
    parse_address,
    validate_address,
)
from .grpc_config import FlextGrpcConfig
from .grpc_exceptions import (
    FlextGrpcConfigurationError,
    FlextGrpcConnectionError,
    FlextGrpcError,
    FlextGrpcTimeoutError,
    FlextGrpcValidationError,
)
from .grpc_models import (
    FlextGrpcChannel,
    FlextGrpcClient,
    FlextGrpcServer,
    FlextGrpcService,
    FlextGrpcStream,
    TGrpcChannelState,
    TGrpcHost,
    TGrpcMethodName,
    TGrpcPort,
    TGrpcServerState,
    TGrpcServiceName,
    TGrpcStreamType,
    TGrpcTarget,
    TGrpcTimeout,
    flext_grpc_parse_target,
    flext_grpc_validate_target,
)
from .grpc_services import (
    FlextGrpcClientService,
    FlextGrpcPlatform,
    FlextGrpcServerService,
    FlextGrpcStreamService,
)

try:
    __version__ = importlib.metadata.version("flext-grpc")
except importlib.metadata.PackageNotFoundError:
    __version__ = "1.0.0"

__version_info__ = tuple(int(x) for x in __version__.split(".") if x.isdigit())

__all__: list[str] = [
    # Core
    "FlextContainer",
    # Domain Entities
    "FlextGrpcChannel",
    "FlextGrpcClient",
    "FlextGrpcClientService",
    # Configuration
    "FlextGrpcConfig",
    # Errors
    "FlextGrpcConfigurationError",
    "FlextGrpcConnectionError",
    "FlextGrpcError",
    "FlextGrpcPlatform",
    "FlextGrpcServer",
    # Domain Services
    "FlextGrpcServerService",
    "FlextGrpcService",
    "FlextGrpcStream",
    "FlextGrpcStreamService",
    "FlextGrpcTimeoutError",
    "FlextGrpcValidationError",
    "FlextResult",
    # Types
    "TGrpcChannelState",
    "TGrpcHost",
    "TGrpcMethodName",
    "TGrpcPort",
    "TGrpcServerState",
    "TGrpcServiceName",
    "TGrpcStreamType",
    "TGrpcTarget",
    "TGrpcTimeout",
    "__version__",
    "__version_info__",
    # API Functions
    "create_channel",
    "create_client",
    "create_complete_setup",
    "create_config",
    "create_server",
    "create_service",
    "create_stream",
    "flext_grpc_parse_target",
    "flext_grpc_validate_target",
    "parse_address",
    "validate_address",
]

# Module metadata for API documentation and tooling
__architecture__ = "Clean Architecture + DDD"
__author__ = "FLEXT Development Team"
__license__ = "MIT"
__copyright__ = "Copyright (c) 2025 FLEXT Contributors"
__status__ = "Production"
__maintainer__ = "FLEXT Development Team"
__email__ = "noreply@flext.dev"
__url__ = "https://github.com/flext/flext-grpc"
__description__ = "Enterprise gRPC communication platform with Clean Architecture"

# API stability and compatibility information
__api_version__ = "1.0"
__stability__ = "stable"
__compatibility__ = "Python 3.13+"
