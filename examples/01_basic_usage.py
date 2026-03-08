"""FLEXT gRPC Basic Usage Examples - Core functionality and facade patterns.

This module demonstrates the fundamental operations and patterns of the FLEXT gRPC
communication platform, showcasing the unified FlextGrpc facade for entity creation,
validation, configuration, and service operations following Clean Architecture and
Domain-Driven Design principles.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_grpc import FlextGrpc, FlextGrpcConstants, FlextGrpcModels, FlextGrpcSettings


def example_1_basic_entities() -> None:
    """Example 1: Creating and using basic gRPC entities through FlextGrpc facade."""
    grpc = FlextGrpc()
    server_result = grpc.create_server(
        host=FlextGrpcConstants.Grpc.GrpcNetwork.DEFAULT_HOST,
        port=FlextGrpcConstants.Grpc.GrpcNetwork.DEFAULT_GRPC_PORT,
        max_workers=10,
    )
    if server_result.is_success:
        server = server_result.value
        validation_result = server.validate_business_rules()
        if validation_result.is_failure:
            print(f"Server validation failed: {validation_result.error}")
    grpc.create_channel(
        target=f"{FlextGrpcConstants.Grpc.GrpcNetwork.DEFAULT_HOST}:{FlextGrpcConstants.Grpc.GrpcNetwork.DEFAULT_GRPC_PORT}"
    )
    client_result = grpc.create_client(
        target=f"{FlextGrpcConstants.Grpc.GrpcNetwork.DEFAULT_HOST}:{FlextGrpcConstants.Grpc.GrpcNetwork.DEFAULT_GRPC_PORT}"
    )
    if client_result.is_failure:
        print(f"Client creation failed: {client_result.error}")
    service_result = grpc.create_service(
        name="UserService",
        methods=["GetUser", "CreateUser", "UpdateUser", "DeleteUser"],
    )
    if service_result.is_failure:
        print(f"Service creation failed: {service_result.error}")


def example_2_configuration() -> None:
    """Example 2: Using configuration through FlextGrpc facade."""
    grpc = FlextGrpc()
    default_config = FlextGrpcSettings()
    print(
        f"Created config with host: {default_config.network.host}, port: {default_config.network.port}"
    )
    custom_config = FlextGrpcSettings(
        network=FlextGrpcModels.NetworkConfig(host="example.com", port=9090),
        performance=FlextGrpcModels.PerformanceConfig(max_workers=20),
    )
    print(
        f"Created custom config: {custom_config.network.host}:{custom_config.network.port}"
    )
    invalid_server_result = grpc.create_server(host="", port=0)
    if invalid_server_result.is_failure:
        print(f"Expected validation failure: {invalid_server_result.error}")


def example_3_operations() -> None:
    """Example 3: Using gRPC operations through FlextGrpc facade."""
    grpc = FlextGrpc()
    server_result = grpc.create_server(
        host=FlextGrpcConstants.Grpc.GrpcNetwork.DEFAULT_HOST, port=7070
    )
    if server_result.is_success:
        server = server_result.value
        start_result = grpc.start_server(server)
        if start_result.is_success:
            started_server = start_result.value
            validation_result = started_server.validate_business_rules()
            if validation_result.is_success:
                print(f"Server status: {started_server.state}")
            stop_result = grpc.stop_server(started_server)
            if stop_result.is_success:
                print("Server stopped successfully")
    client_result = grpc.create_client(
        target=f"{FlextGrpcConstants.Grpc.GrpcNetwork.DEFAULT_HOST}:7070"
    )
    if client_result.is_success:
        connect_result = grpc.connect_client(
            f"{FlextGrpcConstants.Grpc.GrpcNetwork.DEFAULT_HOST}:7070"
        )
        if connect_result.is_success:
            connected_client = connect_result.value
            call_result = grpc.make_call(
                connected_client, "GetServerInfo", {"request_id": "12345"}
            )
            if call_result.is_success:
                print(f"Call result: {call_result.value}")
            disconnect_result = grpc.disconnect_client(connected_client)
            if disconnect_result.is_success:
                print("Client disconnected successfully")


def example_4_validation() -> None:
    """Example 4: Domain validation through FlextGrpc facade."""
    grpc = FlextGrpc()
    valid_server_result = grpc.create_server(
        host=FlextGrpcConstants.Grpc.GrpcNetwork.DEFAULT_HOST,
        port=FlextGrpcConstants.Grpc.GrpcNetwork.DEFAULT_GRPC_PORT,
        max_workers=5,
    )
    if valid_server_result.is_success:
        valid_server = valid_server_result.value
        validation = valid_server.validate_business_rules()
        if validation.is_success:
            print("Valid server passed validation")
    invalid_server_result = grpc.create_server(host="", port=0, max_workers=0)
    if invalid_server_result.is_failure:
        print(
            f"Invalid server creation failed as expected: {invalid_server_result.error}"
        )
    valid_channel_result = grpc.create_channel(
        target=f"{FlextGrpcConstants.Grpc.GrpcNetwork.DEFAULT_HOST}:{FlextGrpcConstants.Grpc.GrpcNetwork.DEFAULT_GRPC_PORT}"
    )
    if valid_channel_result.is_success:
        valid_channel = valid_channel_result.value
        validation = valid_channel.validate_business_rules()
        if validation.is_success:
            print("Valid channel passed validation")
    invalid_channel_result = grpc.create_channel(target="")
    if invalid_channel_result.is_failure:
        print(
            f"Invalid channel creation failed as expected: {invalid_channel_result.error}"
        )


def example_5_state_transitions() -> None:
    """Example 5: State transitions through FlextGrpc facade."""
    grpc = FlextGrpc()
    channel_result = grpc.create_channel(
        target=f"{FlextGrpcConstants.Grpc.GrpcNetwork.DEFAULT_HOST}:{FlextGrpcConstants.Grpc.GrpcNetwork.DEFAULT_GRPC_PORT}"
    )
    if channel_result.is_success:
        channel = channel_result.value
        print(f"Channel created with state: {channel.state}")
    server_result = grpc.create_server()
    if server_result.is_success:
        server = server_result.value
        start_result = grpc.start_server(server)
        if start_result.is_success:
            started_server = start_result.value
            print(f"Server started with state: {started_server.state}")
            stop_result = grpc.stop_server(started_server)
            if stop_result.is_success:
                stopped_server = stop_result.value
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
