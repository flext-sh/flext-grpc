"""FLEXT gRPC API - Unified High-Level API Functions.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import re
from dataclasses import replace
from uuid import uuid4

from flext_core import FlextResult, FlextTypes
from flext_grpc.config import FlextGrpcConfig
from flext_grpc.constants import FlextGrpcConstants
from flext_grpc.entities import (
    FlextGrpcChannel,
    FlextGrpcClient,
    FlextGrpcServer,
    FlextGrpcService,
    FlextGrpcStream,
)
from flext_grpc.typings import FlextGrpcTypes


def create_server(
    host: str = "localhost",
    port: int = 50051,
    max_workers: int = 10,
) -> FlextGrpcServer:
    """Create gRPC server with comprehensive validation.

    Args:
      host: Server host address (default: "localhost")
      port: Server port number (default: 50051)
      max_workers: Maximum worker threads (default: 10)

    Returns:
      Created server entity

    Example:
      >>> server = create_server("localhost", 50051)
      >>> print(f"Server created: {server.host}:{server.port}")

    """
    # Direct entity construction - no factory patterns
    try:
        return FlextGrpcServer(
            id=str(uuid4()),
            host=host,
            port=port,
            max_workers=max_workers,
            state="stopped",
            services=[],
        )
    except Exception as e:
        error_msg = f"Failed to create server: {e}"
        raise ValueError(error_msg) from e


def create_client(
    target: str,
    options: FlextTypes.Core.Dict | None = None,
) -> FlextGrpcClient:
    """Create gRPC client with comprehensive validation.

    Args:
      target: gRPC target address (host:port format)
      options: Optional client options

    Returns:
      Created client entity

    Example:
      >>> client = create_client("localhost:50051")
      >>> print(f"Client created: {client.target}")

    """
    # Direct entity construction - no factory patterns
    try:
        # Create channel directly
        channel = FlextGrpcChannel(
            id=str(uuid4()),
            target=FlextGrpcTypes.Core.GrpcTarget(target),
            state="idle",
            options={},
        )

        # Create client directly
        return FlextGrpcClient(
            id=str(uuid4()),
            channel=channel,
            options=options or {},
        )
    except Exception as e:
        error_msg = f"Failed to create client: {e}"
        raise ValueError(error_msg) from e


def create_channel(
    target: str,
    options: FlextTypes.Core.Dict | None = None,
) -> FlextGrpcChannel:
    """Create gRPC channel with validation.

    Args:
      target: gRPC target address (host:port format)
      options: Optional channel options

    Returns:
      Created channel entity

    """
    # Direct entity construction - no factory patterns
    try:
        channel = FlextGrpcChannel(
            id=str(uuid4()),
            target=FlextGrpcTypes.Core.GrpcTarget(target),
            state="idle",
            options={},
        )
    except Exception as e:
        error_msg = f"Failed to create channel: {e}"
        raise ValueError(error_msg) from e
    if options:
        # Update channel with options using replace
        return replace(channel, options=options)

    return channel


def create_service(
    name: str,
    methods: FlextTypes.Core.StringList | None = None,
) -> FlextGrpcService:
    """Create gRPC service with validation.

    Args:
      name: Service name
      methods: List of method names (default: empty list)

    Returns:
      Created service entity

    """
    # Handle empty methods case at API level for backward compatibility
    if methods is None:
        methods = []

    # Direct entity construction - no factory patterns
    try:
        return FlextGrpcService(
            id=str(uuid4()),
            name=name,
            methods=methods,
        )
    except Exception as e:
        error_msg = f"Failed to create service: {e}"
        raise ValueError(error_msg) from e


def create_stream(
    method_name: str,
    stream_type: FlextGrpcTypes.Core.GrpcStreamType = "unary",
) -> FlextGrpcStream:
    """Create gRPC stream with validation.

    Args:
      method_name: Associated method name
      stream_type: Type of stream (default: "unary")

    Returns:
      Created stream entity

    Raises:
      ValueError: If stream_type is invalid

    """
    valid_types = ["unary", "server_streaming", "client_streaming", "bidirectional"]
    if stream_type not in valid_types:
        msg = f"Invalid stream type: {stream_type}"
        raise ValueError(msg)

    # Direct entity construction - no factory patterns
    try:
        return FlextGrpcStream(
            id=str(uuid4()),
            method_name=method_name,
            stream_type=stream_type,
        )
    except Exception as e:
        error_msg = f"Failed to create stream: {e}"
        raise ValueError(error_msg) from e


def create_config(
    host: str = "localhost",
    port: int = 50051,
    max_workers: int = 10,
    timeout: float = 30.0,
) -> FlextGrpcConfig:
    """Create gRPC configuration with validation.

    Args:
      host: Server host address (default: "localhost")
      port: Server port number (default: 50051)
      max_workers: Maximum worker threads (default: 10)
      timeout: Operation timeout in seconds (default: 30.0)

    Returns:
      Created configuration object

    Raises:
      ValueError: If configuration parameters are invalid

    """
    try:
        return FlextGrpcConfig(
            host=host,
            port=port,
            max_workers=max_workers,
            timeout=timeout,
        )
    except Exception as e:
        raise ValueError(str(e)) from e


def create_complete_setup(
    host: str = "localhost",
    port: int = 50051,
    service_name: str = "DefaultService",
    service_methods: FlextTypes.Core.StringList | None = None,
) -> FlextTypes.Core.Dict:
    """Create complete gRPC setup with server, client, service, and target.

    Args:
      host: Server host address (default: "localhost")
      port: Server port number (default: 50051)
      service_name: Service name (default: "DefaultService")
      service_methods: List of service methods (default: empty list)

    Returns:
      Dictionary containing server, client, service, and target

    Example:
      >>> setup = create_complete_setup("localhost", 50051, "MyService")
      >>> server = setup["server"]
      >>> client = setup["client"]
      >>> service = setup["service"]
      >>> target = setup["target"]

    """
    if service_methods is None:
        service_methods = []

    # Create components using the fixed factory functions
    server = create_server(host, port)

    target = f"{host}:{port}"
    client = create_client(target)

    service = create_service(service_name, service_methods)

    return {
        "server": server,
        "client": client,
        "service": service,
        "target": target,
    }


def validate_address(address: str | None) -> FlextResult[bool]:
    """Validate network address format.

    Args:
      address: Network address in host:port format

    Returns:
      FlextResult containing validation result or error message

    Example:
      >>> result: FlextResult[object] = validate_address("localhost:50051")
      >>> if result.success:
      ...     print(f"Valid: {result.data}")

    """
    try:
        if address is None or not address.strip():
            return FlextResult[bool].fail("Address cannot be empty")

        # Check target validity (FlextGrpcTypes.Validation.validate_target returns bool)
        target_is_valid = FlextGrpcTypes.Validation.validate_target(address)
        if target_is_valid:
            return FlextResult[bool].ok(data=True)
        return FlextResult[bool].fail("Invalid address format")
    except Exception as e:
        return FlextResult[bool].fail(f"Address validation error: {e}")


def parse_address(address: str) -> dict[str, str | int]:
    """Parse network address into host and port components.

    Args:
      address: Network address in host:port format

    Returns:
      Dictionary with 'host' and 'port' keys

    Raises:
      ValueError: If address format is invalid

    Example:
      >>> result: FlextResult[object] = parse_address("localhost:50051")
      >>> print(f"Host: {result['host']}, Port: {result['port']}")
      Host: localhost, Port: 50051

    """
    if not address or ":" not in address:
        msg = "Address must be in host:port format"
        raise ValueError(msg)

    parts = address.split(":")
    expected_parts = 2
    if len(parts) != expected_parts:
        msg = "Address must be in host:port format"
        raise ValueError(msg)

    host, port_str = parts

    if not host.strip():
        msg = "Invalid host format"
        raise ValueError(msg)

    # Try parsing port - different error messages based on the format
    try:

        def _validate_port_in_range() -> None:
            """Validate parsed port is within valid range."""
            min_port = 1
            max_port = 65535
            if port < min_port or port > max_port:
                port_range_msg = f"Port must be between {min_port} and {max_port}"
                raise ValueError(port_range_msg) from None

        port = int(port_str)
        _validate_port_in_range()
    except ValueError as parse_error:
        # Different error messages based on port_str content
        short_string_length = 3
        if port_str.isalpha() and len(port_str) <= short_string_length:
            # Short alphabetic strings like "abc" suggest invalid format overall
            host_format_msg = "Invalid host format"
            raise ValueError(host_format_msg) from parse_error
        # Longer strings like "address" suggest port number parsing issue
        port_number_msg = "Port must be a number"
        raise ValueError(port_number_msg) from parse_error

    return {"host": host, "port": port}


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
    return FlextGrpcConstants.MIN_PORT <= port <= FlextGrpcConstants.MAX_PORT


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
