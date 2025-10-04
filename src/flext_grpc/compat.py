"""FLEXT gRPC Backward Compatibility - Factory functions for API compatibility.

This module provides backward compatibility factory functions that delegate
to the main FlextGrpc facade class. These functions maintain API stability
while following FLEXT patterns for backward compatibility.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextConstants, FlextTypes

from flext_grpc.api import FlextGrpc
from flext_grpc.config import FlextGrpcConfig
from flext_grpc.constants import FlextGrpcConstants
from flext_grpc.entities import (
    FlextGrpcChannel,
    FlextGrpcClient,
    FlextGrpcServer,
    FlextGrpcService,
    FlextGrpcStream,
)
from flext_grpc.models import FlextGrpcModels
from flext_grpc.typings import FlextGrpcTypes


# Factory functions for backward compatibility
def create_server(
    host: str | FlextGrpcModels.ServerConfig = FlextConstants.Platform.DEFAULT_HOST,
    port: int = FlextGrpcConstants.DEFAULT_GRPC_PORT,
    max_workers: int = FlextGrpcConstants.DEFAULT_MAX_WORKERS,
) -> FlextGrpcServer:
    """Create gRPC server (backward compatibility)."""
    facade = FlextGrpc()
    result = facade.create_server(host=host, port=port, max_workers=max_workers)
    if result.is_failure:
        msg = f"Server creation failed: {result.error}"
        raise ValueError(msg)
    return result.unwrap()


def create_client(
    target: str | FlextGrpcModels.ClientConfig = FlextConstants.Platform.DEFAULT_HOST
    + ":"
    + str(FlextGrpcConstants.DEFAULT_GRPC_PORT),
    options: FlextTypes.Dict | None = None,
) -> FlextGrpcClient:
    """Create gRPC client (backward compatibility)."""
    facade = FlextGrpc()
    result = facade.create_client(target=target, options=options)
    if result.is_failure:
        msg = f"Client creation failed: {result.error}"
        raise ValueError(msg)
    return result.unwrap()


def create_channel(
    target: str | FlextGrpcModels.ChannelConfig = FlextConstants.Platform.DEFAULT_HOST
    + ":"
    + str(FlextGrpcConstants.DEFAULT_GRPC_PORT),
    options: FlextTypes.Dict | None = None,
) -> FlextGrpcChannel:
    """Create gRPC channel (backward compatibility)."""
    facade = FlextGrpc()
    result = facade.create_channel(target=target, options=options)
    if result.is_failure:
        msg = f"Channel creation failed: {result.error}"
        raise ValueError(msg)
    return result.unwrap()


def create_service(
    name: str | FlextGrpcModels.ServiceDefinition = "DefaultService",
    methods: str | FlextTypes.StringList | None = None,
) -> FlextGrpcService:
    """Create gRPC service (backward compatibility)."""
    facade = FlextGrpc()
    result = facade.create_service(name=name, methods=methods)
    if result.is_failure:
        msg = f"Service creation failed: {result.error}"
        raise ValueError(msg)
    return result.unwrap()


def create_stream(
    method_name: str | FlextGrpcModels.StreamInfo = "DefaultMethod",
    stream_type: FlextGrpcTypes.GrpcStreamType = "unary",
) -> FlextGrpcStream:
    """Create gRPC stream (backward compatibility)."""
    facade = FlextGrpc()
    result = facade.create_stream(method_name=method_name, stream_type=stream_type)
    if result.is_failure:
        msg = f"Stream creation failed: {result.error}"
        raise ValueError(msg)
    return result.unwrap()


def create_config(
    server_config: FlextGrpcModels.ServerConfig | None = None,
    host: str = FlextConstants.Platform.DEFAULT_HOST,
    port: int = FlextGrpcConstants.DEFAULT_GRPC_PORT,
    max_workers: int = FlextGrpcConstants.DEFAULT_MAX_WORKERS,
    timeout: float = FlextConstants.Network.DEFAULT_TIMEOUT,
) -> FlextGrpcConfig:
    """Create gRPC configuration (backward compatibility)."""
    facade = FlextGrpc()
    result = facade.create_config(
        server_config=server_config,
        host=host,
        port=port,
        max_workers=max_workers,
        timeout=timeout,
    )
    if result.is_failure:
        msg = f"Config creation failed: {result.error}"
        raise ValueError(msg)
    return result.unwrap()


def create_complete_setup(
    host: str = FlextConstants.Platform.DEFAULT_HOST,
    port: int = FlextGrpcConstants.DEFAULT_GRPC_PORT,
    service_name: str = "DefaultService",
    service_methods: FlextGrpcTypes.Core.StringList | None = None,
) -> FlextTypes.Dict:
    """Create complete gRPC setup (backward compatibility)."""
    facade = FlextGrpc()
    result = facade.create_complete_setup(
        host=host,
        port=port,
        service_name=service_name,
        methods=service_methods,
    )
    if result.is_failure:
        msg = f"Complete setup creation failed: {result.error}"
        raise ValueError(msg)
    return result.unwrap()


def validate_address(address: str | None) -> FlextTypes.FlextResult[bool]:
    """Validate network address (backward compatibility)."""
    facade = FlextGrpc()
    return facade.validate_address(address)


def parse_address(address: str) -> dict[str, str | int]:
    """Parse network address (backward compatibility)."""
    facade = FlextGrpc()
    result = facade.parse_address(address)
    if result.is_failure:
        msg = f"Address parsing failed: {result.error}"
        raise ValueError(msg)
    return result.unwrap()


def validate_host(host: str) -> bool:
    """Validate host address (backward compatibility)."""
    facade = FlextGrpc()
    return facade.validate_host(host)


def validate_port(port: int) -> bool:
    """Validate port number (backward compatibility)."""
    facade = FlextGrpc()
    return facade.validate_port(port)


__all__ = [
    # Factory functions (backward compatibility)
    "create_channel",
    "create_client",
    "create_complete_setup",
    "create_config",
    "create_server",
    "create_service",
    "create_stream",
    # Validation functions (backward compatibility)
    "parse_address",
    "validate_address",
    "validate_host",
    "validate_port",
]
