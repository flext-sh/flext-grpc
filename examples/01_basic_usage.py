"""FLEXT gRPC Basic Usage Examples - Core functionality and facade patterns.

This module demonstrates the fundamental operations and patterns of the FLEXT gRPC
communication platform, showcasing the unified FlextGrpc facade for entity creation,
validation, configuration, and service operations following Clean Architecture and
Domain-Driven Design principles.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_cli import u as cli_u
from flext_grpc import FlextGrpc, FlextGrpcConstants, FlextGrpcSettings


def _emit(message: str) -> None:
    """Emit example output through the canonical CLI facade."""
    cli_u.Cli.formatters_u.Cli.print(message)


def example_1_basic_entities() -> None:
    """Create and use basic gRPC entities through the FlextGrpc facade."""
    grpc = FlextGrpc()
    server_result = grpc.create_server(
        host=FlextGrpcConstants.Grpc.NETWORK_DEFAULT_HOST,
        port=FlextGrpcConstants.Grpc.NETWORK_DEFAULT_GRPC_PORT,
        max_workers=10,
    )
    if server_result.success:
        server = server_result.value
        validation_result = server.validate_business_rules()
        if validation_result.failure:
            _emit(f"Server validation failed: {validation_result.error}")
    grpc.create_channel(
        target=f"{FlextGrpcConstants.Grpc.NETWORK_DEFAULT_HOST}:{FlextGrpcConstants.Grpc.NETWORK_DEFAULT_GRPC_PORT}"
    )
    client_result = grpc.create_client(
        target=f"{FlextGrpcConstants.Grpc.NETWORK_DEFAULT_HOST}:{FlextGrpcConstants.Grpc.NETWORK_DEFAULT_GRPC_PORT}"
    )
    if client_result.failure:
        _emit(f"Client creation failed: {client_result.error}")
    service_result = grpc.create_service(
        name="UserService",
        methods=["GetUser", "CreateUser", "UpdateUser", "DeleteUser"],
    )
    if service_result.failure:
        _emit(f"Service creation failed: {service_result.error}")


def example_2_configuration() -> None:
    """Use configuration through the FlextGrpc facade."""
    grpc = FlextGrpc()
    default_config = FlextGrpcSettings()
    _emit(
        f"Created settings with host: {default_config.Grpc.host}, port: {default_config.Grpc.port}"
    )
    custom_config = FlextGrpcSettings.model_validate({
        "Grpc": {"host": "example.com", "port": 9090, "max_workers": 20}
    })
    _emit(
        f"Created custom settings: {custom_config.Grpc.host}:{custom_config.Grpc.port}"
    )
    invalid_server_result = grpc.create_server(host="", port=0)
    if invalid_server_result.failure:
        _emit(f"Expected validation failure: {invalid_server_result.error}")


def example_3_operations() -> None:
    """Use gRPC operations through the FlextGrpc facade."""
    grpc = FlextGrpc()
    server_result = grpc.create_server(
        host=FlextGrpcConstants.Grpc.NETWORK_DEFAULT_HOST, port=7070
    )
    if server_result.success:
        server = server_result.value
        start_result = grpc.start_server(server)
        if start_result.success:
            started_server = start_result.value
            validation_result = started_server.validate_business_rules()
            if validation_result.success:
                _emit(f"Server status: {started_server.state}")
            stop_result = grpc.stop_server(started_server)
            if stop_result.success:
                _emit("Server stopped successfully")
    client_result = grpc.create_client(
        target=f"{FlextGrpcConstants.Grpc.NETWORK_DEFAULT_HOST}:7070"
    )
    if client_result.success:
        connect_result = grpc.connect_client(
            f"{FlextGrpcConstants.Grpc.NETWORK_DEFAULT_HOST}:7070"
        )
        if connect_result.success:
            connected_client = connect_result.value
            call_result = grpc.make_call(
                connected_client, "GetServerInfo", {"request_id": "12345"}
            )
            if call_result.success:
                _emit(f"Call result: {call_result.value}")
            disconnect_result = grpc.disconnect_client(connected_client)
            if disconnect_result.success:
                _emit("Client disconnected successfully")


def example_4_validation() -> None:
    """Validate domains through the FlextGrpc facade."""
    grpc = FlextGrpc()
    valid_server_result = grpc.create_server(
        host=FlextGrpcConstants.Grpc.NETWORK_DEFAULT_HOST,
        port=FlextGrpcConstants.Grpc.NETWORK_DEFAULT_GRPC_PORT,
        max_workers=5,
    )
    if valid_server_result.success:
        valid_server = valid_server_result.value
        validation = valid_server.validate_business_rules()
        if validation.success:
            _emit("Valid server passed validation")
    invalid_server_result = grpc.create_server(host="", port=0, max_workers=0)
    if invalid_server_result.failure:
        _emit(
            f"Invalid server creation failed as expected: {invalid_server_result.error}"
        )
    valid_channel_result = grpc.create_channel(
        target=f"{FlextGrpcConstants.Grpc.NETWORK_DEFAULT_HOST}:{FlextGrpcConstants.Grpc.NETWORK_DEFAULT_GRPC_PORT}"
    )
    if valid_channel_result.success:
        valid_channel = valid_channel_result.value
        validation = valid_channel.validate_business_rules()
        if validation.success:
            _emit("Valid channel passed validation")
    invalid_channel_result = grpc.create_channel(target="")
    if invalid_channel_result.failure:
        _emit(
            f"Invalid channel creation failed as expected: {invalid_channel_result.error}"
        )


def example_5_state_transitions() -> None:
    """Exercise state transitions through the FlextGrpc facade."""
    grpc = FlextGrpc()
    channel_result = grpc.create_channel(
        target=f"{FlextGrpcConstants.Grpc.NETWORK_DEFAULT_HOST}:{FlextGrpcConstants.Grpc.NETWORK_DEFAULT_GRPC_PORT}"
    )
    if channel_result.success:
        channel = channel_result.value
        _emit(f"Channel created with state: {channel.state}")
    server_result = grpc.create_server()
    if server_result.success:
        server = server_result.value
        start_result = grpc.start_server(server)
        if start_result.success:
            started_server = start_result.value
            _emit(f"Server started with state: {started_server.state}")
            stop_result = grpc.stop_server(started_server)
            if stop_result.success:
                stopped_server = stop_result.value
                _emit(f"Server stopped with state: {stopped_server.state}")


def main() -> None:
    """Run all examples."""
    example_1_basic_entities()
    example_2_configuration()
    example_3_operations()
    example_4_validation()
    example_5_state_transitions()


if __name__ == "__main__":
    main()
