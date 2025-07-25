"""FLEXT gRPC Simple API - Factory functions for easy gRPC setup.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Simple factory functions for creating gRPC entities and configurations.
"""

from __future__ import annotations

import re
import uuid
from datetime import datetime
from typing import Any

from flext_core import FlextResult

from flext_grpc.config import FlextGrpcClientConfig, FlextGrpcServerConfig
from flext_grpc.domain.entities import (
    FlextGrpcChannel,
    FlextGrpcClient,
    FlextGrpcServer,
    FlextGrpcService,
    FlextGrpcStream,
    GrpcChannelState,
    GrpcServerState,
)


def create_flext_grpc_server(
    host: str = "localhost",
    port: int = 50051,
    max_workers: int = 10,
    options: dict[str, Any] | None = None,
) -> FlextGrpcServer:
    """Create a new FlextGrpcServer entity.

    Args:
        host: Server host address
        port: Server port
        max_workers: Maximum number of worker threads
        options: Additional server options

    Returns:
        New FlextGrpcServer entity

    """
    return FlextGrpcServer(
        entity_id=str(uuid.uuid4()),
        host=host,
        port=port,
        options=options,
        state=GrpcServerState.STOPPED,
        created_at=datetime.now(),
    )


def create_flext_grpc_client(
    target: str,
    options: dict[str, Any] | None = None,
) -> FlextGrpcClient:
    """Create a new FlextGrpcClient entity.

    Args:
        target: Target server address
        options: Additional client options

    Returns:
        New FlextGrpcClient entity

    """
    channel = create_flext_grpc_channel(target, options)

    return FlextGrpcClient(
        entity_id=str(uuid.uuid4()),
        channel=channel,
        options=options,
        created_at=datetime.now(),
    )


def create_flext_grpc_channel(
    target: str,
    options: dict[str, Any] | None = None,
) -> FlextGrpcChannel:
    """Create a new FlextGrpcChannel entity.

    Args:
        target: Target server address
        options: Channel options

    Returns:
        New FlextGrpcChannel entity

    """
    return FlextGrpcChannel(
        entity_id=str(uuid.uuid4()),
        target=target,
        options=options,
        state=GrpcChannelState.IDLE,
        created_at=datetime.now(),
    )


def create_flext_grpc_service(
    name: str,
    methods: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> FlextGrpcService:
    """Create a new FlextGrpcService entity.

    Args:
        name: Service name
        methods: List of service methods
        metadata: Service metadata

    Returns:
        New FlextGrpcService entity

    """
    return FlextGrpcService(
        entity_id=str(uuid.uuid4()),
        name=name,
        methods=methods,
        metadata=metadata,
        created_at=datetime.now(),
    )


def create_flext_grpc_stream(
    method_name: str,
    stream_type: str = "unary",
    metadata: dict[str, Any] | None = None,
) -> FlextGrpcStream:
    """Create a new FlextGrpcStream entity.

    Args:
        method_name: Name of the streaming method
        stream_type: Type of stream
        metadata: Stream metadata

    Returns:
        New FlextGrpcStream entity

    """
    return FlextGrpcStream(
        entity_id=str(uuid.uuid4()),
        method_name=method_name,
        stream_type=stream_type,
        metadata=metadata,
        created_at=datetime.now(),
    )


def create_flext_grpc_server_config(
    host: str = "localhost",
    port: int = 50051,
    max_workers: int = 10,
    **options: Any,
) -> FlextGrpcServerConfig:
    """Create a new FlextGrpcServerConfig entity.

    Args:
        host: Server host address
        port: Server port
        max_workers: Maximum number of worker threads
        **options: Additional configuration options

    Returns:
        New FlextGrpcServerConfig entity

    """
    return FlextGrpcServerConfig(
        entity_id=str(uuid.uuid4()),
        host=host,
        port=port,
        max_workers=max_workers,
        options=options,
        created_at=datetime.now(),
    )


def create_flext_grpc_client_config(
    target: str,
    timeout: float | None = None,
    **options: Any,
) -> FlextGrpcClientConfig:
    """Create a new FlextGrpcClientConfig entity.

    Args:
        target: Target server address
        timeout: Request timeout in seconds
        **options: Additional configuration options

    Returns:
        New FlextGrpcClientConfig entity

    """
    return FlextGrpcClientConfig(
        entity_id=str(uuid.uuid4()),
        target=target,
        timeout=timeout,
        options=options,
        created_at=datetime.now(),
    )


def validate_flext_grpc_address(address: str) -> FlextResult[bool]:
    """Validate a gRPC address format.

    Args:
        address: Address to validate (host:port format)

    Returns:
        FlextResult indicating if address is valid

    """
    try:
        if not address:
            return FlextResult.fail("Address cannot be empty")

        # Basic validation for host:port format
        if ":" not in address:
            return FlextResult.fail("Address must be in host:port format")

        parts = address.split(":")
        if len(parts) != 2:
            return FlextResult.fail("Address must be in host:port format")

        host, port_str = parts

        # Validate host
        if not host:
            return FlextResult.fail("Host cannot be empty")

        # Basic hostname/IP validation
        if not re.match(r"^[a-zA-Z0-9.-]+$", host):
            return FlextResult.fail("Invalid host format")

        # Validate port
        try:
            port = int(port_str)
            if not (1 <= port <= 65535):
                return FlextResult.fail("Port must be between 1 and 65535")
        except ValueError:
            return FlextResult.fail("Port must be a number")

        return FlextResult.ok(True)

    except Exception as e:
        return FlextResult.fail(f"Address validation error: {e}")


def create_server_from_config(config: FlextGrpcServerConfig) -> FlextGrpcServer:
    """Create a gRPC server from configuration.

    Args:
        config: Server configuration

    Returns:
        New FlextGrpcServer entity

    Raises:
        ValueError: If configuration is invalid

    """
    if not config.is_valid():
        msg = "Invalid server configuration"
        raise ValueError(msg)

    return FlextGrpcServer(
        entity_id=str(uuid.uuid4()),
        host=config.host,
        port=config.port,
        options=config.options.copy(),
        state=GrpcServerState.STOPPED,
        created_at=datetime.now(),
    )


def create_client_from_config(config: FlextGrpcClientConfig) -> FlextGrpcClient:
    """Create a gRPC client from configuration.

    Args:
        config: Client configuration

    Returns:
        New FlextGrpcClient entity

    Raises:
        ValueError: If configuration is invalid

    """
    if not config.is_valid():
        msg = "Invalid client configuration"
        raise ValueError(msg)

    channel = FlextGrpcChannel(
        entity_id=str(uuid.uuid4()),
        target=config.target,
        options=config.options.copy(),
        state=GrpcChannelState.IDLE,
        created_at=datetime.now(),
    )

    return FlextGrpcClient(
        entity_id=str(uuid.uuid4()),
        channel=channel,
        options=config.options.copy(),
        created_at=datetime.now(),
    )


def parse_grpc_address(address: str) -> dict[str, Any]:
    """Parse a gRPC address into components.

    Args:
        address: Address to parse (host:port format)

    Returns:
        Dictionary with 'host' and 'port' keys

    Raises:
        ValueError: If address format is invalid

    """
    validation_result = validate_flext_grpc_address(address)
    if not validation_result.is_success:
        raise ValueError(validation_result.error_message)

    host, port_str = address.split(":")
    return {
        "host": host,
        "port": int(port_str),
    }


# Backwards compatibility aliases
create_grpc_server = create_flext_grpc_server
create_grpc_client = create_flext_grpc_client
create_grpc_channel = create_flext_grpc_channel
create_grpc_service = create_flext_grpc_service
create_grpc_stream = create_flext_grpc_stream
validate_grpc_address = validate_flext_grpc_address
