"""Enterprise gRPC Communication Platform for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import importlib.metadata
from typing import Final

from flext_core import FlextContainer, FlextResult

from flext_grpc.api import (
    FlextGrpc,  # Main unified facade
)
from flext_grpc.compat import (
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
from flext_grpc.constants import FlextGrpcConstants
from flext_grpc.entities import FlextGrpcEntities
from flext_grpc.exceptions import (
    # Backward compatibility aliases
    FlextGrpcConfigurationError,
    FlextGrpcConnectionError,
    FlextGrpcError,
    FlextGrpcExceptions,
    FlextGrpcTimeoutError,
    FlextGrpcValidationError,
)
from flext_grpc.fields import FlextGrpcFields
from flext_grpc.models import FlextGrpcModels
from flext_grpc.platform import FlextGrpcPlatform
from flext_grpc.proto import EchoRequest, FlextGrpcServiceStub
from flext_grpc.protocols import FlextGrpcProtocols
from flext_grpc.services import FlextGrpcService
from flext_grpc.typings import FlextGrpcTypes
from flext_grpc.version import VERSION, FlextGrpcVersion

TGrpcTarget = FlextGrpcTypes.TGrpcTarget
GrpcTarget = FlextGrpcTypes.GrpcTarget

flext_grpc_validate_target = FlextGrpcTypes.GrpcValidation.validate_target
flext_grpc_parse_target = FlextGrpcTypes.GrpcValidation.parse_target

try:
    __version__ = importlib.metadata.version("flext-grpc")
except importlib.metadata.PackageNotFoundError:
    __version__ = VERSION.version

PROJECT_VERSION: Final[FlextGrpcVersion] = VERSION
__version_info__: tuple[int | str, ...] = VERSION.version_info

__all__ = [
    "PROJECT_VERSION",
    "VERSION",
    "EchoRequest",
    "FlextContainer",
    "FlextGrpc",
    "FlextGrpcChannel",
    "FlextGrpcClient",
    "FlextGrpcClientService",  # Backward compatibility alias
    "FlextGrpcConfig",
    "FlextGrpcConfigurationError",
    "FlextGrpcConnectionError",
    "FlextGrpcConstants",
    "FlextGrpcEntities",
    "FlextGrpcEntity",
    "FlextGrpcError",
    "FlextGrpcExceptions",
    "FlextGrpcFields",
    "FlextGrpcModels",
    "FlextGrpcPlatform",
    "FlextGrpcProtocols",
    "FlextGrpcServer",
    "FlextGrpcServerService",  # Backward compatibility alias
    "FlextGrpcService",
    "FlextGrpcServiceStub",
    "FlextGrpcStream",
    "FlextGrpcStreamService",  # Backward compatibility alias
    "FlextGrpcTimeoutError",
    "FlextGrpcTypes",
    "FlextGrpcValidationError",
    "FlextGrpcVersion",
    "FlextResult",
    "GrpcTarget",
    "TGrpcTarget",
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

__architecture__ = "Clean Architecture + DDD"

__copyright__ = "Copyright (c) 2025 FLEXT Contributors"
__status__ = "Production"

__email__ = "noreply@flext.dev"
__url__ = "https://github.com/flext/flext-grpc"

__api_version__ = "1.0"
__stability__ = "stable"
__compatibility__ = "Python 3.13+"

# Backward compatibility aliases for nested entity classes
FlextGrpcEntity = FlextGrpcEntities.Entity
FlextGrpcChannel = FlextGrpcEntities.Channel
FlextGrpcServer = FlextGrpcEntities.Server
FlextGrpcClient = FlextGrpcEntities.Client
FlextGrpcStream = FlextGrpcEntities.GrpcStream

# Backward compatibility aliases for nested service classes
FlextGrpcClientService = FlextGrpcService.ClientService
FlextGrpcServerService = FlextGrpcService.ServerService
FlextGrpcStreamService = FlextGrpcService.StreamService
