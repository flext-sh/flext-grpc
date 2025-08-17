"""FLEXT gRPC Basic Usage Examples - Core functionality and entity management patterns.

This module demonstrates the fundamental operations and patterns of the FLEXT gRPC
communication platform, showcasing entity creation, validation, configuration,
and basic service operations following Clean Architecture and Domain-Driven
Design principles.

Example Categories:
    The module provides comprehensive examples of core FLEXT gRPC functionality:
    - Entity Creation: Server, Client, Channel, Service entity creation and validation
    - Configuration Management: FlextGrpcConfig usage with validation and defaults
    - Domain Validation: Entity validation rules and business logic verification
    - Service Operations: Basic service operations and state management
    - Error Handling: FlextResult pattern usage for robust error handling

Current Implementation Status:
    - ✅ Entity Creation: Complete entity lifecycle and validation examples
    - ✅ Configuration: Configuration management with validation examples
    - ✅ Domain Logic: Domain rule validation and business logic examples
    - ✅ Error Handling: FlextResult pattern usage and error scenarios
    - ⚠️ Network Communication: Limited by lack of Protocol Buffer implementation

Key Patterns Demonstrated:
    - Entity Factory Functions: Using create_server(), create_client() API functions
    - Domain Validation: validate_domain_rules() pattern with FlextResult handling
    - State Management: Entity state transitions and lifecycle management
    - Configuration Patterns: FlextGrpcConfig creation and validation
    - Error Handling: Comprehensive FlextResult success/failure pattern usage

Example:
    Standard entity creation and validation pattern:

    >>> from flext_grpc import create_server, create_client
    >>> from flext_grpc import FlextGrpcServer
    >>>
    >>> # Create server entity with validation
    >>> server = create_server(host="localhost", port=50051, max_workers=10)
    >>> validation_result = server.validate_domain_rules()
    >>>
    >>> if validation_result.success:
    ...     print(f"Server created successfully: {server.address}")
    ... else:
    ...     print(f"Validation failed: {validation_result.error}")

Usage:
    Run this example to see FLEXT gRPC core functionality:

    >>> poetry run python examples/basic_usage.py

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from datetime import UTC, datetime

from flext_grpc import (
    FlextGrpcChannel,
    FlextGrpcClient,
    FlextGrpcConfig,
    FlextGrpcServer,
    FlextGrpcService,
    GrpcOperations,
    TGrpcTarget,
)


def example_1_basic_entities() -> None:
    """Example 1: Creating and using basic gRPC entities."""
    print("=== Example 1: Basic Entities ===")

    # Create a gRPC server
    server = FlextGrpcServer(
      id="example-server",
      host="localhost",
      port=8080,
      max_workers=10,
      created_at=datetime.now(UTC),
    )

    print(f"Created server: {server.get_address()}")
    print(f"Server state: {server.state}")
    print(f"Server is valid: {server.is_valid()}")

    # Create a gRPC channel
    channel = FlextGrpcChannel(
      id="example-channel",
      target=TGrpcTarget("localhost:8080"),
      created_at=datetime.now(UTC),
    )

    print(f"Created channel: {channel.target}")
    print(f"Channel is ready: {channel.is_ready()}")

    # Create a gRPC client
    client = FlextGrpcClient(
      id="example-client",
      channel=channel,
      created_at=datetime.now(UTC),
    )

    print(f"Created client with channel: {client.channel.target}")
    print(f"Client is connected: {client.is_connected()}")

    # Create a gRPC service
    service = FlextGrpcService(
      id="example-service",
      name="UserService",
      methods=["GetUser", "CreateUser", "UpdateUser", "DeleteUser"],
      created_at=datetime.now(UTC),
    )

    print(f"Created service: {service.name}")
    print(f"Service methods: {service.methods}")
    print(f"Has GetUser method: {service.has_method('GetUser')}")
    print(f"Has InvalidMethod: {service.has_method('InvalidMethod')}")

    print()


def example_2_configuration() -> None:
    """Example 2: Using configuration."""
    print("=== Example 2: Configuration ===")

    # Create default configuration
    default_config = FlextGrpcConfig()
    print(f"Default config: {default_config.get_address()}")
    print(f"Default timeout: {default_config.timeout}s")
    print(f"Default workers: {default_config.max_workers}")

    # Create custom configuration
    custom_config = FlextGrpcConfig(
      host="example.com",
      port=9090,
      max_workers=20,
      timeout=60.0,
    )

    print(f"Custom config: {custom_config.get_address()}")
    print(f"Custom timeout: {custom_config.timeout}s")
    print(f"Custom workers: {custom_config.max_workers}")

    # Configuration validation
    try:
      FlextGrpcConfig(host="", port=0)
    except (RuntimeError, ValueError, TypeError) as e:
      print(f"Configuration validation works: {e}")

    print()


def example_3_operations() -> None:
    """Example 3: Using gRPC operations."""
    print("=== Example 3: gRPC Operations ===")

    # Create operations service
    ops = GrpcOperations()

    # Test operations service
    execute_result = ops.execute()
    print(f"Operations status: {execute_result.data}")

    # Create server for operations
    server = FlextGrpcServer(
      id="ops-server",
      host="localhost",
      port=7070,
      created_at=datetime.now(UTC),
    )

    print(f"Initial server state: {server.state}")

    # Start server
    start_result = ops.start_server(server)
    if start_result.success:
      running_server = start_result.data
      print(f"Server started: {running_server.state}")
    else:
      print(f"Failed to start server: {start_result.error}")

    # Stop server
    if start_result.success:
      stop_result = ops.stop_server(running_server)
      if stop_result.success:
          stopped_server = stop_result.data
          print(f"Server stopped: {stopped_server.state}")
      else:
          print(f"Failed to stop server: {stop_result.error}")

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

    print(f"Initial client connected: {client.is_connected()}")

    # Connect client
    connect_result = ops.connect_client(client)
    if connect_result.success:
      connected_client = connect_result.data
      print(f"Client connected: {connected_client.is_connected()}")

      # Call method
      call_result = ops.call_method(
          connected_client,
          "GetServerInfo",
          {"request_id": "12345"},
      )
      if call_result.success:
          response = call_result.data
          print(f"Method call successful: {response['method']}")
          print(f"Response status: {response['status']}")
          print(f"Response data: {response['data']}")
      else:
          print(f"Method call failed: {call_result.error}")
    else:
      print(f"Failed to connect client: {connect_result.error}")

    print()


def example_4_validation() -> None:
    """Example 4: Domain validation."""
    print("=== Example 4: Domain Validation ===")

    # Valid entities
    valid_server = FlextGrpcServer(
      id="valid-server",
      host="localhost",
      port=8080,
      max_workers=5,
      created_at=datetime.now(UTC),
    )

    validation = valid_server.validate_domain_rules()
    print(f"Valid server validation: {validation.success}")

    # Invalid entities
    try:
      invalid_server = FlextGrpcServer(
          id="invalid-server",
          host="",  # Invalid empty host
          port=0,  # Invalid port
          max_workers=0,  # Invalid workers
          created_at=datetime.now(UTC),
      )

      validation = invalid_server.validate_domain_rules()
      print(f"Invalid server validation: {validation.success}")
      if validation.is_failure:
          print(f"Validation error: {validation.error}")
    except (RuntimeError, ValueError, TypeError) as e:
      print(f"Server creation failed during validation: {e}")

    # Channel validation
    valid_channel = FlextGrpcChannel(
      id="valid-channel",
      target=TGrpcTarget("localhost:8080"),
      state="ready",
      created_at=datetime.now(UTC),
    )

    channel_validation = valid_channel.validate_domain_rules()
    print(f"Valid channel validation: {channel_validation.success}")

    invalid_channel = FlextGrpcChannel(
      id="invalid-channel",
      target=TGrpcTarget(""),  # Invalid empty target
      created_at=datetime.now(UTC),
    )

    invalid_validation = invalid_channel.validate_domain_rules()
    print(f"Invalid channel validation: {invalid_validation.success}")
    if invalid_validation.is_failure:
      print(f"Channel validation error: {invalid_validation.error}")

    print()


def example_5_state_transitions() -> None:
    """Example 5: State transitions."""
    print("=== Example 5: State Transitions ===")

    # Channel state transitions
    channel = FlextGrpcChannel(
      id="transition-channel",
      target=TGrpcTarget("localhost:8080"),
      state="idle",
      created_at=datetime.now(UTC),
    )

    print(f"Initial channel state: {channel.state}")

    # Connect channel
    connect_result = channel.connect()
    if connect_result.success:
      connecting_channel = connect_result.data
      print(f"After connect: {connecting_channel.state}")

      # Mark ready
      ready_result = connecting_channel.mark_ready()
      if ready_result.success:
          ready_channel = ready_result.data
          print(f"After mark ready: {ready_channel.state}")
          print(f"Channel is ready: {ready_channel.is_ready()}")
      else:
          print(f"Failed to mark ready: {ready_result.error}")
    else:
      print(f"Failed to connect: {connect_result.error}")

    # Server state management
    server = FlextGrpcServer(
      id="transition-server",
      created_at=datetime.now(UTC),
    )

    print(f"Initial server state: {server.state}")
    print(f"Server is running: {server.is_running()}")

    ops = GrpcOperations()

    # Start server
    start_result = ops.start_server(server)
    if start_result.success:
      running_server = start_result.data
      print(f"After start: {running_server.state}")
      print(f"Server is running: {running_server.is_running()}")

    print()


def main() -> None:
    """Run all examples."""
    print("FLEXT gRPC Library - Usage Examples")
    print("=====================================")
    print()

    example_1_basic_entities()
    example_2_configuration()
    example_3_operations()
    example_4_validation()
    example_5_state_transitions()

    print("All examples completed successfully!")
    print()
    print("Key Benefits of Refactored Library:")
    print("- Simplified API with only 8 exports (down from 33)")
    print("- Clean method names without redundant prefixes")
    print("- Direct entity construction instead of factory functions")
    print("- Focused operations service for business logic")
    print("- Strong domain validation with FlextResult patterns")
    print("- Immutable entities with copy_with() for state changes")


if __name__ == "__main__":
    main()
