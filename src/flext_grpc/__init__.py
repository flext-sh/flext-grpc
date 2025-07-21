"""FLEXT GRPC - Enterprise gRPC Services with Zero Tolerance for Technical Debt.

Copyright (c) 2025 FLEXT Team. All rights reserved.

Version 0.7.0 - Clean Architecture with Domain-Driven Design.
"""

from __future__ import annotations

# Version
__version__ = "0.7.0"

# Domain exports
# Application exports
from flext_grpc.application.commands import (
    ExecuteRPCCallCommand,
    HealthCheckCommand,
    RegisterRPCMethodCommand,
    StartGRPCServiceCommand,
    StopGRPCServiceCommand,
)
from flext_grpc.domain.entities import (
    GRPCService,
    RPCCall,
    RPCMethod,
    RPCMethodType,
    ServiceStatus,
)

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
