"""Enterprise gRPC Communication Platform for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_core import FlextExceptions, d, e, h, r, s, x

from flext_grpc.__version__ import __version__, __version_info__
from flext_grpc.api import FlextGrpc
from flext_grpc.constants import c
from flext_grpc.models import m
from flext_grpc.proto import FlextGrpcServiceStub
from flext_grpc.protocols import FlextGrpcProtocols, FlextGrpcProtocols as p
from flext_grpc.services import FlextGrpcServices
from flext_grpc.settings import FlextGrpcSettings
from flext_grpc.typings import t
from flext_grpc.utilities import u


class FlextGrpcError(FlextExceptions.BaseError):
    """Base gRPC error."""


class FlextGrpcValidationError(FlextExceptions.ValidationError):
    """gRPC validation error."""


class FlextGrpcConnectionError(FlextExceptions.ConnectionError):
    """gRPC connection error."""


class FlextGrpcTimeoutError(FlextExceptions.TimeoutError):
    """gRPC timeout error."""


class FlextGrpcSettingsurationError(FlextExceptions.ConfigurationError):
    """gRPC configuration/settings error."""


__all__ = [
    "FlextGrpc",
    "FlextGrpcConnectionError",
    "FlextGrpcConstants",
    "FlextGrpcError",
    "FlextGrpcModels",
    "FlextGrpcProtocols",
    "FlextGrpcServiceStub",
    "FlextGrpcServices",
    "FlextGrpcSettings",
    "FlextGrpcSettingsurationError",
    "FlextGrpcTimeoutError",
    "FlextGrpcTypes",
    "FlextGrpcUtilities",
    "FlextGrpcValidationError",
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
    "x",
]
