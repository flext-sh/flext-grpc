"""FLEXT gRPC - Enterprise gRPC Communication Platform.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Enterprise-grade gRPC communication platform built on flext-core foundation.
Provides unified client/server management, streaming, and service discovery.

Simple usage:
>>> from flext_grpc import FlextGrpcServer, FlextGrpcClient
>>> from flext_grpc import create_flext_grpc_platform
>>>
>>> # Create unified platform
>>> platform = create_flext_grpc_platform()
>>>
>>> # Use modern gRPC services
>>> server = platform.get_grpc_server()
>>> client = platform.get_grpc_client()
>>> result = server.start(host="localhost", port=50051)
"""

from __future__ import annotations

import contextlib
import importlib.metadata
from typing import TYPE_CHECKING

# Import from flext-core for foundational patterns (standardized)
from flext_core import (
    FlextConstants,
    FlextContainer,
    FlextCoreSettings as BaseConfig,
    FlextEntity as DomainEntity,
    FlextField as Field,
    FlextResult,
    FlextValueObject as BaseModel,
    FlextValueObject as DomainBaseModel,
    FlextValueObject as DomainValueObject,
)

try:
    __version__ = importlib.metadata.version("flext-grpc")
except importlib.metadata.PackageNotFoundError:
    __version__ = "1.0.0"

__version_info__ = tuple(int(x) for x in __version__.split(".") if x.isdigit())

if TYPE_CHECKING:
    from flext_grpc.platform import FlextGrpcPlatform

# ================================
# SIMPLIFIED PUBLIC API EXPORTS
# ================================

# Application services - simplified imports
with contextlib.suppress(ImportError):
    from flext_grpc.application.services import (
        FlextGrpcClientService,
        FlextGrpcServerService,
        FlextGrpcStreamService,
    )

# Configuration and connection management - simplified imports
with contextlib.suppress(ImportError):
    from flext_grpc.config import (
        FlextGrpcClientConfig,
        FlextGrpcServerConfig,
    )

# Core domain entities - simplified imports
with contextlib.suppress(ImportError):
    from flext_grpc.domain.entities import (
        FlextGrpcChannel,
        FlextGrpcClient,
        FlextGrpcServer,
        FlextGrpcService,
        FlextGrpcStream,
    )

# Simple API for common operations - simplified imports
with contextlib.suppress(ImportError):
    from flext_grpc.simple_api import (
        create_flext_grpc_channel,
        create_flext_grpc_client,
        create_flext_grpc_server,
        validate_flext_grpc_address,
    )


# Platform factory function
def create_flext_grpc_platform(
    config: dict[str, object] | None = None,
) -> FlextGrpcPlatform:
    """Create unified FLEXT gRPC platform instance.

    Args:
        config: Optional configuration dictionary

    Returns:
        Configured FlextGrpcPlatform instance

    """
    from flext_grpc.platform import FlextGrpcPlatform

    return FlextGrpcPlatform(config or {})


# Backwards compatibility aliases
FlextGrpc = FlextGrpcServer if "FlextGrpcServer" in locals() else None

# Function aliases for backward compatibility
create_client_config = (
    create_flext_grpc_client if "create_flext_grpc_client" in locals() else None
)
create_server_config = (
    create_flext_grpc_server if "create_flext_grpc_server" in locals() else None
)
validate_address = (
    validate_flext_grpc_address if "validate_flext_grpc_address" in locals() else None
)

# ================================
# PUBLIC API EXPORTS
# ================================

__all__ = [
    # Core patterns from flext-core
    "BaseConfig",
    "BaseModel",
    "DomainBaseModel",
    "DomainEntity",
    "DomainValueObject",
    "Field",
    "FlextConstants",
    "FlextContainer",
    # gRPC Components
    "FlextGrpc",
    "FlextGrpcChannel",
    "FlextGrpcClient",
    "FlextGrpcClientConfig",
    "FlextGrpcClientService",
    "FlextGrpcServer",
    "FlextGrpcServerConfig",
    "FlextGrpcServerService",
    "FlextGrpcService",
    "FlextGrpcStream",
    "FlextGrpcStreamService",
    "FlextResult",
    # Metadata
    "__version__",
    "__version_info__",
    # Backward compatibility
    "create_client_config",
    # Simple API helpers
    "create_flext_grpc_channel",
    "create_flext_grpc_client",
    "create_flext_grpc_platform",
    "create_flext_grpc_server",
    "create_server_config",
    "validate_address",
    "validate_flext_grpc_address",
]
