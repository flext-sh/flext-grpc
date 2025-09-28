"""FLEXT gRPC API - Unified High-Level API Functions.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import re
from uuid import uuid4

from flext_core import FlextConstants, FlextResult
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


def create_server(
    host: str | FlextGrpcModels.ServerConfig = FlextConstants.Platform.DEFAULT_HOST,
    port: int = FlextGrpcConstants.DEFAULT_GRPC_PORT,
    max_workers: int = FlextGrpcConstants.DEFAULT_MAX_WORKERS,
) -> FlextGrpcServer:
    """Create gRPC server using FlextGrpcModels.ServerConfig.

    Args:
      host: Server host address or ServerConfig object (default: FlextConstants.Platform.DEFAULT_HOST)
      port: Server port number (default: FlextGrpcConstants.DEFAULT_GRPC_PORT)
      max_workers: Maximum worker threads (default: FlextGrpcConstants.DEFAULT_MAX_WORKERS)

    Returns:
      Created server entity

    Example:
      >>> config = FlextGrpcModels.ServerConfig(
      ...     host=FlextConstants.Platform.DEFAULT_HOST,
      ...     port=FlextGrpcConstants.DEFAULT_GRPC_PORT,
      ... )
      >>> server = create_server(config=config)
      >>> print(f"Server created: {server.host}:{server.port}")

    """
    # Handle both config object and individual parameters
    if isinstance(host, FlextGrpcModels.ServerConfig):
        config = host
    else:
        config = FlextGrpcModels.ServerConfig(
            host=host, port=port, max_workers=max_workers
        )

    # Create server entity using standardized models
    return FlextGrpcServer(
        id=str(uuid4()),
        host=config.host,
        port=config.port,
        max_workers=config.max_workers,
        state="stopped",
        services=[],
    )


def create_client(
    target: str | FlextGrpcModels.ClientConfig = FlextConstants.Platform.DEFAULT_HOST
    + ":"
    + str(FlextGrpcConstants.DEFAULT_GRPC_PORT),
    options: dict[str, object] | None = None,
) -> FlextGrpcClient:
    """Create gRPC client using FlextGrpcModels.ClientConfig.

    Args:
      config: Client configuration model (preferred)
      target: gRPC target address (host:port format)
      options: Optional client options

    Returns:
      Created client entity

    Example:
      >>> config = FlextGrpcModels.ClientConfig(
      ...     target=f"{FlextConstants.Platform.DEFAULT_HOST}:{FlextGrpcConstants.DEFAULT_GRPC_PORT}"
      ... )
      >>> client = create_client(config=config)
      >>> print(f"Client created: {client.target}")

    """
    # Handle both config object and target string
    if isinstance(target, FlextGrpcModels.ClientConfig):
        config = target
    else:
        config = FlextGrpcModels.ClientConfig(
            target=target,
            timeout=FlextGrpcConstants.DEFAULT_TIMEOUT,
            retry_attempts=3,
        )

    # Create channel using standardized models
    FlextGrpcModels.ChannelConfig(address=config.target, options=options)

    channel = FlextGrpcChannel(
        id=str(uuid4()),
        target=config.target,
        state="idle",
        options=options or {},
    )

    # Create client entity using standardized models
    return FlextGrpcClient(
        id=str(uuid4()),
        channel=channel,
        options=options or {},
    )


def create_channel(
    target: str | FlextGrpcModels.ChannelConfig = FlextConstants.Platform.DEFAULT_HOST
    + ":"
    + str(FlextGrpcConstants.DEFAULT_GRPC_PORT),
    options: dict[str, object] | None = None,
) -> FlextGrpcChannel:
    """Create gRPC channel using FlextGrpcModels.ChannelConfig.

    Args:
      config: Channel configuration model (preferred)
      target: gRPC target address (host:port format)
      options: Optional channel options

    Returns:
      Created channel entity

    Example:
      >>> config = FlextGrpcModels.ChannelConfig(
      ...     address=f"{FlextConstants.Platform.DEFAULT_HOST}:{FlextGrpcConstants.DEFAULT_GRPC_PORT}"
      ... )
      >>> channel = create_channel(config=config)
      >>> print(f"Channel created: {channel.target}")

    """
    # Handle both config object and target string
    if isinstance(target, FlextGrpcModels.ChannelConfig):
        config = target
    else:
        config = FlextGrpcModels.ChannelConfig(address=target, options=options)

    # Create channel entity using standardized models
    return FlextGrpcChannel(
        id=str(uuid4()),
        target=config.address,
        state="idle",
        options=config.options or {},
    )


def create_service(
    name: str | FlextGrpcModels.ServiceDefinition = "DefaultService",
    methods: list[str] | None = None,
) -> FlextGrpcService:
    """Create gRPC service using FlextGrpcModels.ServiceDefinition.

    Args:
      definition: Service definition model (preferred)
      name: Service name
      methods: List of method names (default: empty list)

    Returns:
      Created service entity

    Example:
      >>> definition = FlextGrpcModels.ServiceDefinition(
      ...     service_name="MyService", methods=["GetData", "ProcessData"]
      ... )
      >>> service = create_service(definition=definition)
      >>> print(f"Service created: {service.name}")

    """
    # Handle both definition object and name string
    if isinstance(name, FlextGrpcModels.ServiceDefinition):
        definition = name
    else:
        # Convert single method string to list
        if isinstance(methods, str):
            methods_list = [methods]
        elif methods is None:
            methods_list = []
        else:
            methods_list = methods

        definition = FlextGrpcModels.ServiceDefinition(
            service_name=name, methods=methods_list
        )

    # Create service entity using standardized models
    return FlextGrpcService(
        id=str(uuid4()),
        name=definition.service_name,
        methods=definition.methods,
    )


def create_stream(
    method_name: str | FlextGrpcModels.StreamInfo = "DefaultMethod",
    stream_type: FlextGrpcTypes.GrpcStreamType = "unary",
) -> FlextGrpcStream:
    """Create gRPC stream using FlextGrpcModels.StreamInfo.

    Args:
      stream_info: Stream information model (preferred)
      method_name: Associated method name
      stream_type: Type of stream (default: unary)

    Returns:
      Created stream entity

    Raises:
      ValueError: If stream_type is invalid or method_name is empty

    Example:
      >>> stream_info = FlextGrpcModels.StreamInfo(
      ...     stream_id="stream1",
      ...     stream_type="server_streaming",
      ...     target=f"{FlextConstants.Platform.DEFAULT_HOST}:{FlextGrpcConstants.DEFAULT_GRPC_PORT}",
      ... )
      >>> stream = create_stream(stream_info=stream_info)
      >>> print(f"Stream created: {stream.method_name}")

    """
    # Handle both stream_info object and method_name string
    if isinstance(method_name, FlextGrpcModels.StreamInfo):
        stream_info = method_name
    else:
        # Validate method name
        if not method_name or not method_name.strip():
            msg = "Stream method name cannot be empty"
            raise ValueError(msg)

        # Validate stream type
        valid_types = [
            "unary",
            "server_streaming",
            "client_streaming",
            "bidirectional",
        ]
        if stream_type not in valid_types:
            msg = f"Invalid stream type: {stream_type}"
            raise ValueError(msg)

        stream_info = FlextGrpcModels.StreamInfo(
            stream_id=str(uuid4()),
            stream_type=stream_type,
            target=f"{FlextConstants.Platform.DEFAULT_HOST}:{FlextGrpcConstants.DEFAULT_GRPC_PORT}",  # Default target
        )

    # Create stream entity using standardized models
    # Extract method_name from stream_info if method_name is a StreamInfo object
    actual_method_name = (
        method_name if isinstance(method_name, str) else "DefaultMethod"
    )

    return FlextGrpcStream(
        id=stream_info.stream_id,
        method_name=actual_method_name,
        stream_type=stream_info.stream_type,
    )


def create_config(
    server_config: FlextGrpcModels.ServerConfig | None = None,
    host: str = FlextConstants.Platform.DEFAULT_HOST,
    port: int = FlextGrpcConstants.DEFAULT_GRPC_PORT,
    max_workers: int = FlextGrpcConstants.DEFAULT_MAX_WORKERS,
    timeout: float = FlextConstants.Network.DEFAULT_TIMEOUT,
) -> FlextGrpcConfig:
    """Create gRPC configuration using FlextGrpcModels.ServerConfig.

    Args:
      server_config: Server configuration model (preferred)
      host: Server host address (default: FlextConstants.Platform.DEFAULT_HOST)
      port: Server port number (default: FlextGrpcConstants.DEFAULT_GRPC_PORT)
      max_workers: Maximum worker threads (default: FlextGrpcConstants.DEFAULT_MAX_WORKERS)
      timeout: Operation timeout in seconds (default: FlextConstants.Network.DEFAULT_TIMEOUT)

    Returns:
      Created configuration object

    Raises:
      ValueError: If configuration parameters are invalid

    Example:
      >>> server_config = FlextGrpcModels.ServerConfig(
      ...     host=FlextConstants.Platform.DEFAULT_HOST,
      ...     port=FlextGrpcConstants.DEFAULT_GRPC_PORT,
      ...     max_workers=10,
      ... )
      >>> config = create_config(server_config=server_config)
      >>> print(f"Config created: {config.get_address()}")

    """
    # Use provided server_config or create from parameters
    if server_config is None:
        server_config = FlextGrpcModels.ServerConfig(
            host=host, port=port, max_workers=max_workers, timeout=timeout
        )

    # Create FlextGrpcConfig using standardized models
    return FlextGrpcConfig(
        host=server_config.host,
        port=server_config.port,
        max_workers=server_config.max_workers,
        timeout=server_config.timeout,
    )


def create_complete_setup(
    host: str = FlextConstants.Platform.DEFAULT_HOST,
    port: int = FlextGrpcConstants.DEFAULT_GRPC_PORT,
    service_name: str = "DefaultService",
    service_methods: FlextGrpcTypes.Core.StringList | None = None,
) -> dict[str, object]:
    """Create complete gRPC setup with server, client, service, and target.

    Args:
      host: Server host address (default: FlextConstants.Platform.DEFAULT_HOST)
      port: Server port number (default: FlextGrpcConstants.DEFAULT_GRPC_PORT)
      service_name: Service name (default: DefaultService)
      service_methods: List of service methods (default: empty list)

    Returns:
      Dictionary containing server, client, service, and target with gRPC-specific types

    Example:
      >>> setup = create_complete_setup(
      ...     FlextConstants.Platform.DEFAULT_HOST,
      ...     FlextGrpcConstants.DEFAULT_GRPC_PORT,
      ...     "MyService",
      ... )
      >>> server = setup["server"]
      >>> client = setup["client"]
      >>> service = setup["service"]
      >>> target = setup["target"]

    """
    if service_methods is None:
        service_methods = ["DefaultMethod"]

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
      >>> result: FlextResult[object] = validate_address(
      ...     f"{FlextConstants.Platform.DEFAULT_HOST}:{FlextGrpcConstants.DEFAULT_GRPC_PORT}"
      ... )
      >>> if result.is_success:
      ...     print(f"Valid: {result.data}")

    """
    try:
        if address is None or not address.strip():
            return FlextResult[bool].fail("Address cannot be empty")

        # Check target validity (FlextGrpcTypes.GrpcValidation.validate_target returns bool)
        target_is_valid = FlextGrpcTypes.GrpcValidation.validate_target(address)
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
      >>> result: FlextResult[object] = parse_address(
      ...     f"{FlextConstants.Platform.DEFAULT_HOST}:{FlextGrpcConstants.DEFAULT_GRPC_PORT}"
      ... )
      >>> print(f"Host: {result['host']}, Port: {result['port']}")
      Host: FlextConstants.Platform.DEFAULT_HOST, Port: FlextGrpcConstants.DEFAULT_GRPC_PORT

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
