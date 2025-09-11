"""FLEXT gRPC Basic Usage Examples - Core functionality and entity management patterns.

This module demonstrates the fundamental operations and patterns of the FLEXT gRPC
communication platform, showcasing entity creation, validation, configuration,
and basic service operations following Clean Architecture and Domain-Driven
Design principles.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations
from flext_core import FlextTypes


import sys
from datetime import UTC, datetime
from pathlib import Path

# Add src directory to Python path for development
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import contextlib

from flext_grpc import (
    FlextGrpcChannel,
    FlextGrpcClient,
    FlextGrpcClientService,
    FlextGrpcConfig,
    FlextGrpcServer,
    FlextGrpcServerService,
    FlextGrpcService,
    TGrpcTarget,
)

# FlextGrpcClient and FlextGrpcServer already imported above


def example_1_basic_entities() -> None:
    """Example 1: Creating and using basic gRPC entities."""
    # Create a gRPC server
    server = FlextGrpcServer(
        id="example-server",
        host="localhost",
        port=8080,
        max_workers=10,
        created_at=datetime.now(UTC),
    )

    server.validate_business_rules()

    # Create a gRPC channel
    channel = FlextGrpcChannel(
        id="example-channel",
        target=TGrpcTarget("localhost:8080"),
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
        port=9090,
        max_workers=20,
        timeout=60.0,
    )

    # Configuration validation
    with contextlib.suppress(RuntimeError, ValueError, TypeError):
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
        host="localhost",
        port=7070,
        created_at=datetime.now(UTC),
    )

    # Start server
    start_result = server_service.execute("start", server)
    if start_result.success:
        pass

    # Stop server
    if start_result.success and start_result.data is not None:
        # Check if data is actually a server instance
        if isinstance(start_result.data, FlextGrpcServer):
            stop_result = server_service.execute("stop", start_result.data)
        else:
            return
        if stop_result.success:
            pass

    # Create client for operations
    channel = FlextGrpcChannel(
        id="ops-channel",
        target=TGrpcTarget("localhost:7070"),
        created_at=datetime.now(UTC),
    )

    client = FlextGrpcClient(
        id="ops-client",
        channel=channel,
        created_at=datetime.now(UTC),
    )

    # Connect client
    connect_result = client_service.execute("connect", client)
    if connect_result.success and isinstance(connect_result.data, FlextGrpcClient):
        # Call method
        call_result = client_service.execute(
            "call",
            connect_result.data,
            method_name="GetServerInfo",
            data={"request_id": "12345"},
        )
        if call_result.success:
            pass


def example_4_validation() -> None:
    """Example 4: Domain validation."""
    # Valid entities
    valid_server = FlextGrpcServer(
        id="valid-server",
        host="localhost",
        port=8080,
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
        target=TGrpcTarget("localhost:8080"),
        state="ready",
        created_at=datetime.now(UTC),
    )

    valid_channel.validate_business_rules()

    invalid_channel = FlextGrpcChannel(
        id="invalid-channel",
        target=TGrpcTarget(""),  # Invalid empty target
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
        target=TGrpcTarget("localhost:8080"),
        state="idle",
        created_at=datetime.now(UTC),
    )

    # Connect channel
    connect_result = channel.connect()
    if connect_result.success:
        connecting_channel = connect_result.data

        # Mark ready
        ready_result = connecting_channel.mark_ready()
        if ready_result.success:
            pass

    # Server state management
    server = FlextGrpcServer(
        id="transition-server",
        created_at=datetime.now(UTC),
    )

    server_service = FlextGrpcServerService()

    # Start server
    start_result = server_service.execute("start", server)
    if start_result.success:
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
