"""Enterprise gRPC Communication Platform for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

# Use FlextExceptions from flext_core instead of custom exceptions
from flext_core import FlextExceptions as FlextGrpcExceptions

from flext_grpc.__version__ import __version__, __version_info__
from flext_grpc.api import FlextGrpc
from flext_grpc.config import FlextGrpcConfig
from flext_grpc.constants import FlextGrpcConstants
from flext_grpc.entities import (
    FlextGrpcEntities,
)
from flext_grpc.models import FlextGrpcModels
from flext_grpc.proto import EchoRequest, FlextGrpcServiceStub
from flext_grpc.protocols import FlextGrpcProtocols
from flext_grpc.services import FlextGrpcServices
from flext_grpc.typings import FlextGrpcTypes
from flext_grpc.utilities import FlextGrpcUtilities

# Model aliases for backward compatibility
GrpcHealthCheck = FlextGrpcModels.Domain.GrpcHealthCheck
GrpcRequest = FlextGrpcModels.Domain.GrpcRequest
ServiceDefinition = FlextGrpcModels.Domain.ServiceDefinition
ServiceMetrics = FlextGrpcModels.Domain.ServiceMetrics
StreamInfo = FlextGrpcModels.Domain.StreamInfo
StreamMetrics = FlextGrpcModels.Domain.StreamMetrics


# Service aliases for backward compatibility
FlextGrpcService = FlextGrpcServices

__all__ = [
    "EchoRequest",
    "FlextGrpc",
    "FlextGrpcConfig",
    "FlextGrpcConstants",
    "FlextGrpcEntities",
    "FlextGrpcExceptions",
    "FlextGrpcModels",
    "FlextGrpcProtocols",
    "FlextGrpcService",
    "FlextGrpcServiceStub",
    "FlextGrpcServices",
    "FlextGrpcTypes",
    "FlextGrpcUtilities",
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
