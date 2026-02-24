"""Enterprise gRPC Communication Platform for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import flext_core

d = flext_core.FlextDecorators
FlextExceptions = flext_core.FlextExceptions
e = flext_core.FlextExceptions
h = flext_core.FlextHandlers
r = flext_core.r
s = flext_core.FlextService

from flext_grpc.__version__ import __version__, __version_info__
from flext_grpc.api import (
    FlextGrpc,
    GenericOperationSpec,
    GenericRequest,
    GenericResponse,
)
from flext_grpc.constants import FlextGrpcConstants, FlextGrpcConstants as c
from flext_grpc.entities import FlextGrpcEntities
from flext_grpc.models import FlextGrpcModels, FlextGrpcModels as m
from flext_grpc.proto import EchoRequest, FlextGrpcServiceStub
from flext_grpc.protocols import FlextGrpcProtocols, FlextGrpcProtocols as p
from flext_grpc.services import (
    ConnectionPool,
    FlextGrpcServices,
    FlextGrpcServices as FlextGrpcService,
    MetricsCollector,
)
from flext_grpc.settings import FlextGrpcSettings
from flext_grpc.typings import FlextGrpcTypes, FlextGrpcTypes as t
from flext_grpc.utilities import FlextGrpcUtilities, FlextGrpcUtilities as u

FlextGrpcError = FlextExceptions.BaseError
FlextGrpcSettingsurationError = FlextExceptions.ConfigurationError
FlextGrpcConnectionError = FlextExceptions.ConnectionError
FlextGrpcTimeoutError = FlextExceptions.TimeoutError
FlextGrpcValidationError = FlextExceptions.ValidationError

GrpcHealthCheck = FlextGrpcModels.Grpc.GrpcHealthCheck
GrpcRequest = FlextGrpcModels.Grpc.GrpcRequest
ServiceDefinition = FlextGrpcModels.Grpc.ServiceDefinition
ServiceMetrics = FlextGrpcModels.Grpc.ServiceMetrics
StreamInfo = FlextGrpcModels.Grpc.StreamInfo
StreamMetrics = FlextGrpcModels.Grpc.StreamMetrics

__all__ = [
    "ConnectionPool",
    "EchoRequest",
    "FlextExceptions",
    "FlextGrpc",
    "FlextGrpcConnectionError",
    "FlextGrpcConstants",
    "FlextGrpcEntities",
    "FlextGrpcError",
    "FlextGrpcModels",
    "FlextGrpcProtocols",
    "FlextGrpcService",
    "FlextGrpcServiceStub",
    "FlextGrpcServices",
    "FlextGrpcSettings",
    "FlextGrpcSettingsurationError",
    "FlextGrpcTimeoutError",
    "FlextGrpcTypes",
    "FlextGrpcUtilities",
    "FlextGrpcValidationError",
    "GenericOperationSpec",
    "GenericRequest",
    "GenericResponse",
    "GrpcHealthCheck",
    "GrpcRequest",
    "MetricsCollector",
    "ServiceDefinition",
    "ServiceMetrics",
    "StreamInfo",
    "StreamMetrics",
    "__api_version__",
    "__architecture__",
    "__compatibility__",
    "__copyright__",
    "__stability__",
    "__status__",
    "__url__",
    "__version__",
    "__version_info__",
    "c",
    "d",
    "e",
    "h",
    "m",
    "p",
    "r",
    "s",
    "t",
    "u",
]

from flext_grpc._metadata import (
    __api_version__,
    __architecture__,
    __compatibility__,
    __copyright__,
    __stability__,
    __status__,
    __url__,
)
