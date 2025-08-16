"""FLEXT gRPC API - Unified High-Level API Functions.

🎯 CONSOLIDATES 1 API FILE INTO SINGLE PEP8 MODULE:
- api.py (600+ lines) - High-level API functions and utilities for gRPC operations

TOTAL CONSOLIDATION: 600+ lines → grpc_api.py (PEP8 organized)

This module provides comprehensive high-level API for all gRPC operations,
offering convenient factory functions and utilities for creating, configuring,
and managing gRPC entities with enterprise-grade validation and error handling.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import re

from flext_core import FlextResult

from flext_grpc.entities import (
    FlextGrpcChannel,
    FlextGrpcClient,
    FlextGrpcEntityFactory,
    FlextGrpcServer,
    FlextGrpcService,
    FlextGrpcStream,
)
from flext_grpc.grpc_config import FlextGrpcConfig
from flext_grpc.grpc_models import (
    TGrpcTarget,
    flext_grpc_parse_target,
    flext_grpc_validate_target,
)

from .grpc_config import FLEXT_GRPC_MAX_PORT, FLEXT_GRPC_MIN_PORT

# =============================================================================
# ENTITY FACTORY FUNCTIONS
# =============================================================================


def create_server(
    host: str,
    port: int,
    max_workers: int = 10,
) -> FlextResult[FlextGrpcServer]:
    """Create gRPC server with comprehensive validation.

    Args:
        host: Server host address
        port: Server port number
        max_workers: Maximum worker threads (default: 10)

    Returns:
        FlextResult containing created server or error message

    Example:
        >>> result = create_server("localhost", 50051)
        >>> if result.success:
        ...     server = result.data
        ...     print(f"Server created: {server.host}:{server.port}")

    """
    return FlextGrpcEntityFactory.create_server(
        host=host,
        port=port,
        max_workers=max_workers,
    )


def create_client(
    target: str,
) -> FlextResult[FlextGrpcClient]:
    """Create gRPC client with comprehensive validation.

    Args:
        target: gRPC target address (host:port format)

    Returns:
        FlextResult containing created client or error message

    Example:
        >>> result = create_client(
        ...     f"{FlextGrpcConstants.Network.DEFAULT_HOST}:{FlextGrpcConstants.Network.DEFAULT_PORT}"
        ... )
        >>> if result.success:
        ...     client = result.data
        ...     print(f"Client created: {client.target}")

    """
    return FlextGrpcEntityFactory.create_client(target=target)


def create_channel(
    target: str,
) -> FlextResult[FlextGrpcChannel]:
    """Create gRPC channel with validation.

    Args:
        target: gRPC target address (host:port format)

    Returns:
        FlextResult containing created channel or error message

    """
    return FlextGrpcEntityFactory.create_channel(target=target)


def create_service(
    name: str,
    methods: list[str] | None = None,
) -> FlextResult[FlextGrpcService]:
    """Create gRPC service with validation.

    Args:
        name: Service name
        methods: List of method names (default: empty list)

    Returns:
        FlextResult containing created service or error message

    """
    return FlextGrpcEntityFactory.create_service(name=name, methods=methods)


def create_stream(
    stream_type: str,
    method_name: str,
) -> FlextResult[FlextGrpcStream]:
    """Create gRPC stream with validation.

    Args:
        stream_type: Type of stream (unary, server_streaming, client_streaming, bidirectional)
        method_name: Associated method name

    Returns:
        FlextResult containing created stream or error message

    """
    return FlextGrpcEntityFactory.create_stream(
        method_name=method_name,
        stream_type=stream_type,
    )


def create_config(
    host: str = "localhost",
    port: int = 50051,
    max_workers: int = 10,
    timeout: float = 30.0,
) -> FlextResult[object]:
    """Create gRPC configuration with validation.

    Args:
        host: Server host address (default: "localhost")
        port: Server port number (default: 50051)
        max_workers: Maximum worker threads (default: 10)
        timeout: Operation timeout in seconds (default: 30.0)

    Returns:
        FlextResult containing created configuration or error message

    """
    try:
        config = FlextGrpcConfig(
            host=host,
            port=port,
            max_workers=max_workers,
            timeout=timeout,
        )
        return FlextResult.ok(config)
    except Exception as e:
        return FlextResult.fail(str(e))


def create_complete_setup(
    _server_id: str = "default-server",
    _client_id: str = "default-client",
    host: str = "localhost",
    port: int = 50051,
    max_workers: int = 10,
    *,
    _ssl_enabled: bool = False,
) -> FlextResult[dict[str, object]]:
    """Create complete gRPC setup with server and client.

    Args:
        server_id: Server identifier
        client_id: Client identifier
        host: Server host address
        port: Server port number
        max_workers: Maximum worker threads
        ssl_enabled: Enable SSL/TLS encryption

    Returns:
        FlextResult containing complete setup (server, client, config) or error

    Example:
        >>> result = create_complete_setup("api-server", "api-client")
        >>> if result.success:
        ...     setup = result.data
        ...     server = setup["server"]
        ...     client = setup["client"]
        ...     config = setup["config"]

    """
    # Create server
    server_result = create_server(host, port, max_workers)
    if server_result.is_failure:
        return FlextResult.fail(f"Server creation failed: {server_result.error}")

    # Create client
    target = f"{host}:{port}"
    client_result = create_client(target)
    if client_result.is_failure:
        return FlextResult.fail(f"Client creation failed: {client_result.error}")

    # Create configuration
    config_result = create_config(host, port, max_workers)
    if config_result.is_failure:
        return FlextResult.fail(f"Config creation failed: {config_result.error}")

    setup = {
        "server": server_result.data,
        "client": client_result.data,
        "config": config_result.data,
    }

    return FlextResult.ok(setup)


# =============================================================================
# ADDRESS VALIDATION AND PARSING
# =============================================================================


def validate_address(address: str) -> bool:
    """Validate network address format.

    Args:
        address: Network address in host:port format

    Returns:
        True if address is valid, False otherwise

    Example:
        >>> validate_address(
        ...     f"{FlextGrpcConstants.Network.DEFAULT_HOST}:{FlextGrpcConstants.Network.DEFAULT_PORT}"
        ... )
        True
        >>> validate_address("invalid-address")
        False

    """
    return flext_grpc_validate_target(address)


def parse_address(address: str) -> FlextResult[tuple[str, int]]:
    """Parse network address into host and port components.

    Args:
        address: Network address in host:port format

    Returns:
        FlextResult containing (host, port) tuple or error message

    Example:
        >>> result = parse_address(
        ...     f"{FlextGrpcConstants.Network.DEFAULT_HOST}:{FlextGrpcConstants.Network.DEFAULT_PORT}"
        ... )
        >>> if result.success:
        ...     host, port = result.data
        ...     print(f"Host: {host}, Port: {port}")
        Host: localhost, Port: 50051

    """
    if not validate_address(address):
        return FlextResult.fail(f"Invalid address format: {address}")

    try:
        host, port = flext_grpc_parse_target(TGrpcTarget(address))
        return FlextResult.ok((str(host), int(port)))
    except Exception as e:
        return FlextResult.fail(f"Address parsing failed: {e}")


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================


def validate_host(host: str) -> bool:
    """Validate host address format.

    Args:
        host: Host address (hostname or IP)

    Returns:
        True if host is valid, False otherwise

    """
    if not host or not host.strip():
        return False

    # Basic hostname/IP validation
    pattern = r"^[a-zA-Z0-9.-]+$"
    return bool(re.match(pattern, host.strip()))


def validate_port(port: int) -> bool:
    """Validate port number range.

    Args:
        port: Port number

    Returns:
        True if port is valid, False otherwise

    """
    return FLEXT_GRPC_MIN_PORT <= port <= FLEXT_GRPC_MAX_PORT


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    # Factory functions
    "create_channel",
    "create_client",
    "create_complete_setup",
    "create_config",
    "create_server",
    "create_service",
    "create_stream",
    # Validation functions
    "parse_address",
    "validate_address",
    "validate_host",
    "validate_port",
]
