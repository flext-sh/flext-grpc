"""Enterprise gRPC Communication Platform for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import importlib.metadata

from flext_core import FlextContainer, FlextResult, FlextTypes

from flext_grpc.api import (
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
from flext_grpc.config import FlextGrpcConfig
from flext_grpc.entities import (
    FlextGrpcChannel,
    FlextGrpcClient,
    FlextGrpcEntity,
    FlextGrpcServer,
    FlextGrpcService,
    FlextGrpcStream,
)
from flext_grpc.exceptions import (
    FlextGrpcConfigurationError,
    FlextGrpcConnectionError,
    FlextGrpcError,
    FlextGrpcTimeoutError,
    FlextGrpcValidationError,
)
from flext_grpc.services import (
    FlextGrpcClientService,
    FlextGrpcPlatform,
    FlextGrpcServerService,
    FlextGrpcStreamService,
)
from flext_grpc.typings import (
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

try:
    __version__ = importlib.metadata.version("flext-grpc")
except importlib.metadata.PackageNotFoundError:
    __version__ = "1.0.0"

__version_info__ = tuple(int(x) for x in __version__.split(".") if x.isdigit())

__all__: FlextTypes.Core.StringList = [
    "FlextContainer",
    "FlextGrpcChannel",
    "FlextGrpcClient",
    "FlextGrpcClientService",
    "FlextGrpcConfig",
    "FlextGrpcConfigurationError",
    "FlextGrpcConnectionError",
    "FlextGrpcEntity",
    "FlextGrpcError",
    "FlextGrpcPlatform",
    "FlextGrpcServer",
    "FlextGrpcServerService",
    "FlextGrpcService",
    "FlextGrpcStream",
    "FlextGrpcStreamService",
    "FlextGrpcTimeoutError",
    "FlextGrpcValidationError",
    "FlextResult",
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
