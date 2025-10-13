"""Enterprise gRPC Communication Platform for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_grpc.__version__ import __version__, __version_info__
from flext_grpc.api import FlextGrpc
from flext_grpc.config import FlextGrpcConfig
from flext_grpc.constants import FlextGrpcConstants
from flext_grpc.entities import (
    FlextGrpcEntities,
)
from flext_grpc.exceptions import (
    FlextGrpcExceptions,
)
from flext_grpc.models import FlextGrpcModels

# Model aliases for backward compatibility
GrpcHealthCheck = FlextGrpcModels.Domain.GrpcHealthCheck
GrpcRequest = FlextGrpcModels.Domain.GrpcRequest
ServiceDefinition = FlextGrpcModels.Domain.ServiceDefinition
ServiceMetrics = FlextGrpcModels.Domain.ServiceMetrics
StreamInfo = FlextGrpcModels.Domain.StreamInfo
StreamMetrics = FlextGrpcModels.Domain.StreamMetrics
from flext_grpc.proto import EchoRequest, FlextGrpcServiceStub
from flext_grpc.protocols import FlextGrpcProtocols
from flext_grpc.services import FlextGrpcServices
from flext_grpc.typings import FlextGrpcTypings
from flext_grpc.utilities import FlextGrpcUtilities

# Exception aliases for backward compatibility
FlextGrpcError = FlextGrpcExceptions.BaseError
FlextGrpcValidationError = FlextGrpcExceptions.ValidationError
FlextGrpcConnectionError = FlextGrpcExceptions.ConnectionError
FlextGrpcTimeoutError = FlextGrpcExceptions.TimeoutError
FlextGrpcConfigurationError = FlextGrpcExceptions.ConfigurationError

# Service aliases for backward compatibility
FlextGrpcService = FlextGrpcServices

__all__ = [
    "EchoRequest",
    "FlextGrpc",
    "FlextGrpcConfig",
    "FlextGrpcConfigurationError",
    "FlextGrpcConnectionError",
    "FlextGrpcConstants",
    "FlextGrpcEntities",
    "FlextGrpcError",
    "FlextGrpcExceptions",
    "FlextGrpcModels",
    "FlextGrpcProtocols",
    "FlextGrpcService",
    "FlextGrpcServiceStub",
    "FlextGrpcServices",
    "FlextGrpcTimeoutError",
    "FlextGrpcTypings",
    "FlextGrpcUtilities",
    "FlextGrpcValidationError",
    "FlextGrpcVersion",
    "GrpcHealthCheck",
    "GrpcRequest",
    "ServiceDefinition",
    "ServiceMetrics",
    "StreamInfo",
    "StreamMetrics",
    "__version__",
    "__version_info__",
]

__architecture__ = "Clean Architecture + DDD"

__copyright__ = "Copyright (c) 2025 FLEXT Contributors"
__status__ = "Production"

__url__ = "https://github.com/flext/flext-grpc"

__api_version__ = "1.0"
__stability__ = "stable"
__compatibility__ = "Python 3.13+"
