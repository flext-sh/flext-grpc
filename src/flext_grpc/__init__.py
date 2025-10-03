"""Enterprise gRPC Communication Platform for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import importlib.metadata
from typing import Final

from flext_core import FlextContainer, FlextResult
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
from flext_grpc.constants import FlextGrpcConstants
from flext_grpc.entities import (
    FlextGrpcChannel,
    FlextGrpcClient,
    FlextGrpcEntity,
    FlextGrpcServer,
    FlextGrpcStream,
)
from flext_grpc.exceptions import (
    FlextGrpcConfigurationError,
    FlextGrpcConnectionError,
    FlextGrpcError,
    FlextGrpcTimeoutError,
    FlextGrpcValidationError,
)
from flext_grpc.models import FlextGrpcModels
from flext_grpc.platform import FlextGrpcPlatform
from flext_grpc.proto import EchoRequest, FlextGrpcServiceStub
from flext_grpc.protocols import FlextGrpcProtocols
from flext_grpc.services import (
    FlextGrpcClientService,
    FlextGrpcServerService,
    FlextGrpcService,
)
from flext_grpc.typings import FlextGrpcTypes
from flext_grpc.version import VERSION, FlextGrpcVersion

TGrpcTarget = FlextGrpcTypes.TGrpcTarget
GrpcTarget = FlextGrpcTypes.GrpcTarget

flext_grpc_validate_target = FlextGrpcTypes.GrpcValidation.validate_target
flext_grpc_parse_target = FlextGrpcTypes.GrpcValidation.parse_target

__version__ = importlib.metadata.version("flext-grpc")

PROJECT_VERSION: Final[FlextGrpcVersion] = VERSION

__version__: str = VERSION.version
__version_info__: tuple[int | str, ...] = VERSION.version_info

__all__ = [
    "PROJECT_VERSION",
    "VERSION",
    "EchoRequest",
    "FlextContainer",
    "FlextGrpcChannel",
    "FlextGrpcClient",
    "FlextGrpcClientService",
    "FlextGrpcConfig",
    "FlextGrpcConfigurationError",
    "FlextGrpcConnectionError",
    "FlextGrpcConstants",
    "FlextGrpcEntity",
    "FlextGrpcError",
    "FlextGrpcModels",
    "FlextGrpcPlatform",
    "FlextGrpcProtocols",
    "FlextGrpcServer",
    "FlextGrpcServerService",
    "FlextGrpcService",
    "FlextGrpcServiceStub",
    "FlextGrpcStream",
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
