"""FLEXT gRPC - Simple gRPC Library."""

from __future__ import annotations

# 🚨 ARCHITECTURAL COMPLIANCE: Using DI container for flext-core imports
from flext_grpc.infrastructure.di_container import get_service_result
from flext_grpc.simple_grpc import (
    create_client_config,
    create_server_config,
    format_grpc_error,
    validate_address,
)

ServiceResult = get_service_result()

__version__ = "1.0.0"

__all__ = [
    "ServiceResult",
    "__version__",
    "create_client_config",
    "create_server_config",
    "format_grpc_error",
    "validate_address",
]
