"""FLEXT GRPC - Enterprise gRPC Services with Zero Tolerance for Technical Debt.

Copyright (c) 2025 FLEXT Team. All rights reserved.

Version 0.7.0 - Clean Architecture with Domain-Driven Design.
"""

from __future__ import annotations

# Version
__version__ = "0.7.0"

# Domain exports
# Application exports
from flext_grpc.application.commands import ExecuteRPCCallCommand
from flext_grpc.application.commands import HealthCheckCommand
from flext_grpc.application.commands import RegisterRPCMethodCommand
from flext_grpc.application.commands import StartGRPCServiceCommand
from flext_grpc.application.commands import StopGRPCServiceCommand
from flext_grpc.domain.entities import GRPCService
from flext_grpc.domain.entities import RPCCall
from flext_grpc.domain.entities import RPCMethod
from flext_grpc.domain.entities import RPCMethodType
from flext_grpc.domain.entities import ServiceStatus

# Export all
__all__ = [
    # Application
    "ExecuteRPCCallCommand",
    # Domain
    "GRPCService",
    "HealthCheckCommand",
    "RPCCall",
    "RPCMethod",
    "RPCMethodType",
    "RegisterRPCMethodCommand",
    "ServiceStatus",
    "StartGRPCServiceCommand",
    "StopGRPCServiceCommand",
    # Version
    "__version__",
]
