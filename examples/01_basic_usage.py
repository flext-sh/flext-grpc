"""FLEXT gRPC Basic Usage Examples - Core functionality and facade patterns.

This module demonstrates the fundamental operations and patterns of the FLEXT gRPC
communication platform, showcasing the unified FlextGrpc facade for entity creation,
validation, configuration, and service operations following Clean Architecture and
Domain-Driven Design principles.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextConstants

from flext_grpc import FlextGrpc


def example_1_basic_entities() -> None:
    """Example 1: Creating and using basic gRPC entities through FlextGrpc facade."""
    # Initialize the unified gRPC facade
    grpc = FlextGrpc()

    # Create a gRPC server through facade
    server_result = grpc.create_server(
        host=FlextConstants.Platform.DEFAULT_HOST,
        port=FlextConstants.Platform.DEFAULT_HTTP_PORT,
        max_workers=10,
    )

    if server_result.is_success:
        server = server_result.unwrap()
        # Validate server through facade
        validation_result = server.validate_business_rules()
        if validation_result.is_failure:
            print(f"Server validation failed: {validation_result.error}")

    # Create a gRPC channel through facade
    grpc.create_channel(
        target=f"{FlextConstants.Platform.DEFAULT_HOST}:{FlextConstants.Platform.DEFAULT_HTTP_PORT}"
    )

    # Create a gRPC client through facade
    client_result = grpc.create_client(
        target=f"{FlextConstants.Platform.DEFAULT_HOST}:{FlextConstants.Platform.DEFAULT_HTTP_PORT}"
    )
    if client_result.is_failure:
        print(f"Client creation failed: {client_result.error}")

    # Create a gRPC service through facade
    service_result = grpc.create_service(
        name="UserService",
        methods=["GetUser", "CreateUser", "UpdateUser", "DeleteUser"],
    )

    if service_result.is_failure:
        print(f"Service creation failed: {service_result.error}")


def example_2_configuration() -> None:
    """Example 2: Using configuration through FlextGrpc facade."""
    # Initialize facade
    grpc = FlextGrpc()

    # Create default configuration through facade
    config_result = grpc.create_config()
    if config_result.is_success:
        config = config_result.unwrap()
        print(f"Created config with host: {config.grpc_host}, port: {config.grpc_port}")

    # Create custom configuration through facade
    custom_config_result = grpc.create_config(
        host="example.com",
        port=9090,  # Use numeric port
        max_workers=20,
        timeout=60.0,
    )

    if custom_config_result.is_success:
        custom_config = custom_config_result.unwrap()
        print(
            f"Created custom config: {custom_config.grpc_host}:{custom_config.grpc_port}"
        )

    # Configuration validation - invalid config will fail
    invalid_config_result = grpc.create_config(host="", port=0)
    if invalid_config_result.is_failure:
        print(f"Expected config validation failure: {invalid_config_result.error}")


def example_3_operations() -> None:
    """Example 3: Using gRPC operations through FlextGrpc facade."""
    # Initialize facade
    grpc = FlextGrpc()

    # Create and start server through facade
    server_result = grpc.create_server(
        host=FlextConstants.Platform.DEFAULT_HOST, port=7070
    )

    if server_result.is_success:
        server = server_result.unwrap()

        # Start server through facade
        start_result = grpc.start_server(server)
        if start_result.is_success:
            started_server = start_result.unwrap()

            # Get server status through facade
            status_result = grpc.get_server_status(started_server)
            if status_result.is_success:
                print(f"Server status: {status_result.unwrap()}")

            # Stop server through facade
            stop_result = grpc.stop_server(started_server)
            if stop_result.is_success:
                print("Server stopped successfully")

    # Create and connect client through facade
    client_result = grpc.create_client(
        target=f"{FlextConstants.Platform.DEFAULT_HOST}:7070"
    )

    if client_result.is_success:
        # Connect client through facade
        connect_result = grpc.connect_client(
            f"{FlextConstants.Platform.DEFAULT_HOST}:7070"
        )
        if connect_result.is_success:
            connected_client = connect_result.unwrap()

            # Make call through facade
            call_result = grpc.make_call(
                connected_client, "GetServerInfo", {"request_id": "12345"}
            )
            if call_result.is_success:
                print(f"Call result: {call_result.unwrap()}")

            # Disconnect client through facade
            disconnect_result = grpc.disconnect_client(connected_client)
            if disconnect_result.is_success:
                print("Client disconnected successfully")


def example_4_validation() -> None:
    """Example 4: Domain validation through FlextGrpc facade."""
    # Initialize facade
    grpc = FlextGrpc()

    # Valid entities through facade
    valid_server_result = grpc.create_server(
        host=FlextConstants.Platform.DEFAULT_HOST,
        port=FlextConstants.Platform.DEFAULT_HTTP_PORT,
        max_workers=5,
    )

    if valid_server_result.is_success:
        valid_server = valid_server_result.unwrap()
        validation = valid_server.validate_business_rules()
        if validation.is_success:
            print("Valid server passed validation")

    # Invalid entities - facade will return failure
    invalid_server_result = grpc.create_server(
        host="",  # Invalid empty host
        port=0,  # Invalid port
        max_workers=0,  # Invalid workers
    )

    if invalid_server_result.is_failure:
        print(
            f"Invalid server creation failed as expected: {invalid_server_result.error}"
        )

    # Channel validation through facade
    valid_channel_result = grpc.create_channel(
        target=f"{FlextConstants.Platform.DEFAULT_HOST}:{FlextConstants.Platform.DEFAULT_HTTP_PORT}"
    )

    if valid_channel_result.is_success:
        valid_channel = valid_channel_result.unwrap()
        validation = valid_channel.validate_business_rules()
        if validation.is_success:
            print("Valid channel passed validation")

    # Invalid channel - facade will return failure
    invalid_channel_result = grpc.create_channel(target="")

    if invalid_channel_result.is_failure:
        print(
            f"Invalid channel creation failed as expected: {invalid_channel_result.error}"
        )


def example_5_state_transitions() -> None:
    """Example 5: State transitions through FlextGrpc facade."""
    # Initialize facade
    grpc = FlextGrpc()

    # Create channel through facade
    channel_result = grpc.create_channel(
        target=f"{FlextConstants.Platform.DEFAULT_HOST}:{FlextConstants.Platform.DEFAULT_HTTP_PORT}"
    )

    if channel_result.is_success:
        channel = channel_result.unwrap()

        # Note: State transitions are handled internally by facade operations
        # Channels transition through states during connect/disconnect operations
        print(f"Channel created with state: {channel.state}")

    # Server state management through facade
    server_result = grpc.create_server()

    if server_result.is_success:
        server = server_result.unwrap()

        # Start server - transitions to running state
        start_result = grpc.start_server(server)
        if start_result.is_success:
            started_server = start_result.unwrap()
            print(f"Server started with state: {started_server.state}")

            # Stop server - transitions back to stopped state
            stop_result = grpc.stop_server(started_server)
            if stop_result.is_success:
                stopped_server = stop_result.unwrap()
                print(f"Server stopped with state: {stopped_server.state}")


def main() -> None:
    """Run all examples."""
    example_1_basic_entities()
    example_2_configuration()
    example_3_operations()
    example_4_validation()
    example_5_state_transitions()


if __name__ == "__main__":
    main()
