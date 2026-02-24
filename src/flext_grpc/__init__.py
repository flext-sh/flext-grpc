"""Enterprise gRPC Communication Platform for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_grpc.__version__ import __version__, __version_info__
from flext_grpc.api import FlextGrpc
from flext_grpc.constants import FlextGrpcConstants, FlextGrpcConstants as c
from flext_grpc.entities import FlextGrpcEntities
from flext_grpc.models import FlextGrpcModels, FlextGrpcModels as m
from flext_grpc.proto import FlextGrpcServiceStub
from flext_grpc.protocols import FlextGrpcProtocols, FlextGrpcProtocols as p
from flext_grpc.services import FlextGrpcServices
from flext_grpc.settings import FlextGrpcSettings
from flext_grpc.typings import FlextGrpcTypes, FlextGrpcTypes as t
from flext_grpc.utilities import FlextGrpcUtilities, FlextGrpcUtilities as u

__all__ = [
    "FlextGrpc",
    "FlextGrpcConstants",
    "FlextGrpcEntities",
    "FlextGrpcModels",
    "FlextGrpcProtocols",
    "FlextGrpcServiceStub",
    "FlextGrpcServices",
    "FlextGrpcSettings",
    "FlextGrpcTypes",
    "FlextGrpcUtilities",
    "__version__",
    "__version_info__",
    "c",
    "m",
    "p",
    "t",
    "u",
]
