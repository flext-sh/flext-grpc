"""Enterprise gRPC Communication Platform for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_core import (
    FlextDecorators,
    FlextExceptions,
    FlextExceptions as FlextGrpcExceptions,
    FlextHandlers,
    FlextMixins,
    FlextResult,
    FlextService,
)

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

# Domain-specific aliases (extending flext-core base classes)
u = FlextGrpcUtilities  # Utilities (FlextGrpcUtilities extends FlextUtilities)
m = FlextGrpcModels  # Models (FlextGrpcModels extends FlextModels)
c = FlextGrpcConstants  # Constants (FlextGrpcConstants extends FlextConstants)
t = FlextGrpcTypes  # Types (FlextGrpcTypes extends FlextTypes)
p = FlextGrpcProtocols  # Protocols (FlextGrpcProtocols extends FlextProtocols)

r = FlextResult  # Shared from flext-core
e = FlextExceptions  # Shared from flext-core
d = FlextDecorators  # Shared from flext-core
s = FlextService  # Shared from flext-core
x = FlextMixins  # Shared from flext-core
h = FlextHandlers  # Shared from flext-core


# Exception classes with real inheritance for backward compatibility
class FlextGrpcError(FlextGrpcExceptions.BaseError):
    """FlextGrpcError - real inheritance from BaseError."""


class FlextGrpcConfigurationError(FlextGrpcExceptions.ConfigurationError):
    """FlextGrpcConfigurationError - real inheritance from ConfigurationError."""


class FlextGrpcConnectionError(FlextGrpcExceptions.ConnectionError):
    """FlextGrpcConnectionError - real inheritance from ConnectionError."""


class FlextGrpcTimeoutError(FlextGrpcExceptions.TimeoutError):
    """FlextGrpcTimeoutError - real inheritance from TimeoutError."""


class FlextGrpcValidationError(FlextGrpcExceptions.ValidationError):
    """FlextGrpcValidationError - real inheritance from ValidationError."""


# Model classes with real inheritance for backward compatibility
class GrpcHealthCheck(FlextGrpcModels.Domain.GrpcHealthCheck):
    """GrpcHealthCheck - real inheritance from Domain.GrpcHealthCheck."""


class GrpcRequest(FlextGrpcModels.Domain.GrpcRequest):
    """GrpcRequest - real inheritance from Domain.GrpcRequest."""


class ServiceDefinition(FlextGrpcModels.ServiceDefinition):
    """ServiceDefinition - real inheritance from ServiceDefinition."""


class ServiceMetrics(FlextGrpcModels.ServiceMetrics):
    """ServiceMetrics - real inheritance from ServiceMetrics."""


class StreamInfo(FlextGrpcModels.Domain.StreamInfo):
    """StreamInfo - real inheritance from Domain.StreamInfo."""


class StreamMetrics(FlextGrpcModels.Domain.StreamMetrics):
    """StreamMetrics - real inheritance from Domain.StreamMetrics."""


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
    "FlextGrpcTypes",
    "FlextGrpcUtilities",
    "FlextGrpcValidationError",
    "GrpcHealthCheck",
    "GrpcRequest",
    "ServiceDefinition",
    "ServiceMetrics",
    "StreamInfo",
    "StreamMetrics",
    "__version__",
    "__version_info__",
    # Domain-specific aliases
    "c",
    # Global aliases
    "d",
    "e",
    "h",
    "m",
    "p",
    "r",
    "s",
    "t",
    "u",
    "x",
]

__architecture__ = "Clean Architecture + DDD"

__copyright__ = "Copyright (c) 2025 FLEXT Contributors"
__status__ = "Production"

__url__ = "https://github.com/flext/flext-grpc"

__api_version__ = "1.0"
__stability__ = "stable"
__compatibility__ = "Python 3.13+"
