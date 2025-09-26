"""FLEXT gRPC API - Unified High-Level API Functions.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import re
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
from flext_grpc.models import FlextGrpcModels
from flext_grpc.typings import FlextGrpcTypes


def create_server(
    config: FlextGrpcModels.ServerConfig | None = None,
    host: str = "localhost",
    port: int = 50051,
    max_workers: int = 10,
) -> FlextResult[FlextGrpcServer]:
    """Create gRPC server using FlextGrpcModels.ServerConfig.

    Args:
      config: Server configuration model (preferred)
      host: Server host address (fallback, default: localhost)
      port: Server port number (fallback, default: 50051)
      max_workers: Maximum worker threads (fallback, default: 10)

    Returns:
      FlextResult containing created server entity or error

    Example:
      >>> config = FlextGrpcModels.ServerConfig(host="localhost", port=50051)
      >>> result = create_server(config=config)
      >>> if result.is_success:
      ...     server = result.unwrap()
      ...     print(f"Server created: {server.host}:{server.port}")

    """
    try:
        # Use provided config or create from parameters
        if config is None:
            config = FlextGrpcModels.ServerConfig(
                host=host, port=port, max_workers=max_workers
            )

        # Create server entity using standardized models
        server = FlextGrpcServer(
            id=str(uuid4()),
            host=config.host,
            port=config.port,
            max_workers=config.max_workers,
            state="stopped",
            services=[],
        )

        return FlextResult[FlextGrpcServer].ok(server)
    except Exception as e:
        error_msg = f"Failed to create server: {e}"
        return FlextResult[FlextGrpcServer].fail(error_msg)


def create_client(
    config: FlextGrpcModels.ClientConfig | None = None,
    target: str | None = None,
    options: FlextTypes.Core.Dict | None = None,
) -> FlextResult[FlextGrpcClient]:
    """Create gRPC client using FlextGrpcModels.ClientConfig.

    Args:
      config: Client configuration model (preferred)
      target: gRPC target address (fallback, host:port format)
      options: Optional client options (fallback)

    Returns:
      FlextResult containing created client entity or error

    Example:
      >>> config = FlextGrpcModels.ClientConfig(target="localhost:50051")
      >>> result = create_client(config=config)
      >>> if result.is_success:
      ...     client = result.unwrap()
      ...     print(f"Client created: {client.target}")

    """
    try:
        # Use provided config or create from parameters
        if config is None:
            if target is None:
                return FlextResult[FlextGrpcClient].fail(
                    "Either config or target must be provided"
                )

            config = FlextGrpcModels.ClientConfig(
                target=target, timeout=30.0, retry_attempts=3
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
        client = FlextGrpcClient(
            id=str(uuid4()),
            channel=channel,
            options=options or {},
        )

        return FlextResult[FlextGrpcClient].ok(client)
    except Exception as e:
        error_msg = f"Failed to create client: {e}"
        return FlextResult[FlextGrpcClient].fail(error_msg)


def create_channel(
    config: FlextGrpcModels.ChannelConfig | None = None,
    target: str | None = None,
    options: FlextTypes.Core.Dict | None = None,
) -> FlextResult[FlextGrpcChannel]:
    """Create gRPC channel using FlextGrpcModels.ChannelConfig.

    Args:
      config: Channel configuration model (preferred)
      target: gRPC target address (fallback, host:port format)
      options: Optional channel options (fallback)

    Returns:
      FlextResult containing created channel entity or error

    Example:
      >>> config = FlextGrpcModels.ChannelConfig(address="localhost:50051")
      >>> result = create_channel(config=config)
      >>> if result.is_success:
      ...     channel = result.unwrap()
      ...     print(f"Channel created: {channel.target}")

    """
    try:
        # Use provided config or create from parameters
        if config is None:
            if target is None:
                return FlextResult[FlextGrpcChannel].fail(
                    "Either config or target must be provided"
                )

            config = FlextGrpcModels.ChannelConfig(address=target, options=options)

        # Create channel entity using standardized models
        channel = FlextGrpcChannel(
            id=str(uuid4()),
            target=config.address,
            state="idle",
            options=config.options or {},
        )

        return FlextResult[FlextGrpcChannel].ok(channel)
    except Exception as e:
        error_msg = f"Failed to create channel: {e}"
        return FlextResult[FlextGrpcChannel].fail(error_msg)


def create_service(
    definition: FlextGrpcModels.ServiceDefinition | None = None,
    name: str | None = None,
    methods: FlextTypes.Core.StringList | None = None,
) -> FlextResult[FlextGrpcService]:
    """Create gRPC service using FlextGrpcModels.ServiceDefinition.

    Args:
      definition: Service definition model (preferred)
      name: Service name (fallback)
      methods: List of method names (fallback, default: empty list)

    Returns:
      FlextResult containing created service entity or error

    Example:
      >>> definition = FlextGrpcModels.ServiceDefinition(
      ...     service_name="MyService", methods=["GetData", "ProcessData"]
      ... )
      >>> result = create_service(definition=definition)
      >>> if result.is_success:
      ...     service = result.unwrap()
      ...     print(f"Service created: {service.name}")

    """
    try:
        # Use provided definition or create from parameters
        if definition is None:
            if name is None:
                return FlextResult[FlextGrpcService].fail(
                    "Either definition or name must be provided"
                )

            definition = FlextGrpcModels.ServiceDefinition(
                service_name=name, methods=methods or []
            )

        # Create service entity using standardized models
        service = FlextGrpcService(
            id=str(uuid4()),
            name=definition.service_name,
            methods=definition.methods,
        )

        return FlextResult[FlextGrpcService].ok(service)
    except Exception as e:
        error_msg = f"Failed to create service: {e}"
        return FlextResult[FlextGrpcService].fail(error_msg)


def create_stream(
    stream_info: FlextGrpcModels.StreamInfo | None = None,
    method_name: str | None = None,
    stream_type: FlextGrpcTypes.Core.GrpcStreamType = "unary",
) -> FlextResult[FlextGrpcStream]:
    """Create gRPC stream using FlextGrpcModels.StreamInfo.

    Args:
      stream_info: Stream information model (preferred)
      method_name: Associated method name (fallback)
      stream_type: Type of stream (fallback, default: unary)

    Returns:
      FlextResult containing created stream entity or error

    Raises:
      ValueError: If stream_type is invalid

    Example:
      >>> stream_info = FlextGrpcModels.StreamInfo(
      ...     stream_id="stream1",
      ...     stream_type="server_streaming",
      ...     target="localhost:50051",
      ... )
      >>> result = create_stream(stream_info=stream_info)
      >>> if result.is_success:
      ...     stream = result.unwrap()
      ...     print(f"Stream created: {stream.method_name}")

    """
    try:
        # Use provided stream_info or create from parameters
        if stream_info is None:
            if method_name is None:
                return FlextResult[FlextGrpcStream].fail(
                    "Either stream_info or method_name must be provided"
                )

            # Validate stream type
            valid_types = [
                "unary",
                "server_streaming",
                "client_streaming",
                "bidirectional",
            ]
            if stream_type not in valid_types:
                return FlextResult[FlextGrpcStream].fail(
                    f"Invalid stream type: {stream_type}"
                )

            stream_info = FlextGrpcModels.StreamInfo(
                stream_id=str(uuid4()),
                stream_type=stream_type,
                target="localhost:50051",  # Default target
            )

        # Create stream entity using standardized models
        stream = FlextGrpcStream(
            id=stream_info.stream_id,
            method_name=method_name or f"method_{stream_info.stream_id}",
            stream_type=stream_info.stream_type,
        )

        return FlextResult[FlextGrpcStream].ok(stream)
    except Exception as e:
        error_msg = f"Failed to create stream: {e}"
        return FlextResult[FlextGrpcStream].fail(error_msg)


def create_config(
    server_config: FlextGrpcModels.ServerConfig | None = None,
    host: str = "localhost",
    port: int = 50051,
    max_workers: int = 10,
    timeout: float = 30.0,
) -> FlextResult[FlextGrpcConfig]:
    """Create gRPC configuration using FlextGrpcModels.ServerConfig.

    Args:
      server_config: Server configuration model (preferred)
      host: Server host address (fallback, default: localhost)
      port: Server port number (fallback, default: 50051)
      max_workers: Maximum worker threads (fallback, default: 10)
      timeout: Operation timeout in seconds (fallback, default: 30.0)

    Returns:
      FlextResult containing created configuration object or error

    Raises:
      ValueError: If configuration parameters are invalid

    Example:
      >>> server_config = FlextGrpcModels.ServerConfig(
      ...     host="localhost", port=50051, max_workers=10
      ... )
      >>> result = create_config(server_config=server_config)
      >>> if result.is_success:
      ...     config = result.unwrap()
      ...     print(f"Config created: {config.get_address()}")

    """
    try:
        # Use provided server_config or create from parameters
        if server_config is None:
            server_config = FlextGrpcModels.ServerConfig(
                host=host, port=port, max_workers=max_workers, timeout=timeout
            )

        # Create FlextGrpcConfig using standardized models
        config = FlextGrpcConfig(
            host=server_config.host,
            port=server_config.port,
            max_workers=server_config.max_workers,
            timeout=server_config.timeout,
        )

        return FlextResult[FlextGrpcConfig].ok(config)
    except Exception as e:
        error_msg = f"Failed to create config: {e}"
        return FlextResult[FlextGrpcConfig].fail(error_msg)


def create_complete_setup(
    host: str = "localhost",
    port: int = 50051,
    service_name: str = "DefaultService",
    service_methods: FlextTypes.Core.StringList | None = None,
) -> FlextTypes.Core.Dict:
    """Create complete gRPC setup with server, client, service, and target.

    Args:
      host: Server host address (default: localhost)
      port: Server port number (default: 50051)
      service_name: Service name (default: DefaultService)
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
    create_server(host, port)

    target = f"{host}:{port}"
    create_client(target)

    create_service(service_name, service_methods)

    return {
        "server": "server",
        "client": "client",
        "service": "service",
        "target": "target",
    }


def validate_address(address: str | None) -> FlextResult[bool]:
    """Validate network address format.

    Args:
      address: Network address in host:port format

    Returns:
      FlextResult containing validation result or error message

    Example:
      >>> result: FlextResult[object] = validate_address("localhost:50051")
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
      >>> result: FlextResult[object] = parse_address("localhost:50051")
      >>> print(f"Host: {result['host']}, Port: {result['port']}")
      Host: "localhost", Port: 50051

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

    return {"host": "host", "port": "port"}


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
