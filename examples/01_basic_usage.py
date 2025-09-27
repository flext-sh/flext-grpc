"""FLEXT gRPC Basic Usage Examples - Core functionality and entity management patterns.

This module demonstrates the fundamental operations and patterns of the FLEXT gRPC
communication platform, showcasing entity creation, validation, configuration,
and basic service operations following Clean Architecture and Domain-Driven
Design principles.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import contextlib
from datetime import UTC, datetime

from flext_core import FlextConstants
from flext_grpc import (
    FlextGrpcChannel,
    FlextGrpcClient,
    FlextGrpcClientService,
    FlextGrpcConfig,
    FlextGrpcConstants,
    FlextGrpcServer,
    FlextGrpcServerService,
)
from flext_grpc.entities import FlextGrpcService


def example_1_basic_entities() -> None:
    """Example 1: Creating and using basic gRPC entities."""
    # Create a gRPC server
    server = FlextGrpcServer(
        id="example-server",
        host=FlextConstants.Platform.DEFAULT_HOST,
        port=FlextConstants.Platform.DEFAULT_HTTP_PORT,
        max_workers=10,
        created_at=datetime.now(UTC),
    )

    server.validate_business_rules()

    # Create a gRPC channel
    channel = FlextGrpcChannel(
        id="example-channel",
        target=f"{FlextConstants.Platform.DEFAULT_HOST}:{FlextConstants.Platform.DEFAULT_HTTP_PORT}",
        created_at=datetime.now(UTC),
    )

    # Create a gRPC client
    FlextGrpcClient(
        id="example-client",
        channel=channel,
        created_at=datetime.now(UTC),
    )

    # Create a gRPC service
    FlextGrpcService(
        id="example-service",
        name="UserService",
        methods=["GetUser", "CreateUser", "UpdateUser", "DeleteUser"],
        created_at=datetime.now(UTC),
    )


def example_2_configuration() -> None:
    """Example 2: Using configuration."""
    # Create default configuration
    FlextGrpcConfig()

    # Create custom configuration
    FlextGrpcConfig(
        host="example.com",
        port=FlextGrpcConstants.METRICS_PORT,
        max_workers=20,
        timeout=60.0,
    )

    # Configuration validation
    with contextlib.suppress(Exception):
        FlextGrpcConfig(host="", port=0)


def example_3_operations() -> None:
    """Example 3: Using gRPC operations."""
    # Create services for operations
    server_service = FlextGrpcServerService()
    client_service = FlextGrpcClientService()

    # Test services initialized

    # Create server for operations
    server = FlextGrpcServer(
        id="ops-server",
        host=FlextConstants.Platform.DEFAULT_HOST,
        port=7070,
        created_at=datetime.now(UTC),
    )

    # Start server
    start_result = server_service.execute("start", server)
    if start_result.is_success:
        pass

    # Stop server
    if start_result.is_success and start_result.data is not None:
        # Check if data is actually a server instance
        if isinstance(start_result.data, FlextGrpcServer):
            stop_result = server_service.execute("stop", start_result.data)
        else:
            return
        if stop_result.is_success:
            pass

    # Create client for operations
    channel = FlextGrpcChannel(
        id="ops-channel",
        target=f"{FlextConstants.Platform.DEFAULT_HOST}:7070",
        created_at=datetime.now(UTC),
    )

    client = FlextGrpcClient(
        id="ops-client",
        channel=channel,
        created_at=datetime.now(UTC),
    )

    # Connect client
    connect_result = client_service.execute("connect", client)
    if connect_result.is_success and isinstance(connect_result.data, FlextGrpcClient):
        # Call method
        call_result = client_service.execute(
            "call",
            connect_result.data,
            method_name="GetServerInfo",
            data={"request_id": "12345"},
        )
        if call_result.is_success:
            pass


def example_4_validation() -> None:
    """Example 4: Domain validation."""
    # Valid entities
    valid_server = FlextGrpcServer(
        id="valid-server",
        host=FlextConstants.Platform.DEFAULT_HOST,
        port=FlextConstants.Platform.DEFAULT_HTTP_PORT,
        max_workers=5,
        created_at=datetime.now(UTC),
    )

    validation = valid_server.validate_business_rules()

    # Invalid entities
    try:
        invalid_server = FlextGrpcServer(
            id="invalid-server",
            host="",  # Invalid empty host
            port=0,  # Invalid port
            max_workers=0,  # Invalid workers
            created_at=datetime.now(UTC),
        )

        validation = invalid_server.validate_business_rules()
        if validation.is_failure:
            pass
    except (RuntimeError, ValueError, TypeError):
        pass

    # Channel validation
    valid_channel = FlextGrpcChannel(
        id="valid-channel",
        target=f"{FlextConstants.Platform.DEFAULT_HOST}:{FlextConstants.Platform.DEFAULT_HTTP_PORT}",
        state="ready",
        created_at=datetime.now(UTC),
    )

    valid_channel.validate_business_rules()

    invalid_channel = FlextGrpcChannel(
        id="invalid-channel",
        target="",  # Invalid empty target
        created_at=datetime.now(UTC),
    )

    invalid_validation = invalid_channel.validate_business_rules()
    if invalid_validation.is_failure:
        pass


def example_5_state_transitions() -> None:
    """Example 5: State transitions."""
    # Channel state transitions
    channel = FlextGrpcChannel(
        id="transition-channel",
        target=f"{FlextConstants.Platform.DEFAULT_HOST}:{FlextConstants.Platform.DEFAULT_HTTP_PORT}",
        state="idle",
        created_at=datetime.now(UTC),
    )

    # Connect channel
    connect_result = channel.connect()
    if connect_result.is_success:
        connecting_channel = connect_result.data

        # Mark ready
        ready_result = connecting_channel.mark_ready()
        if ready_result.is_success:
            pass

    # Server state management
    server = FlextGrpcServer(
        id="transition-server",
        created_at=datetime.now(UTC),
    )

    server_service = FlextGrpcServerService()

    # Start server
    start_result = server_service.execute("start", server)
    if start_result.is_success:
        pass


def main() -> None:
    """Run all examples."""
    example_1_basic_entities()
    example_2_configuration()
    example_3_operations()
    example_4_validation()
    example_5_state_transitions()


if __name__ == "__main__":
    main()
