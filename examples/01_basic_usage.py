"""FLEXT gRPC Basic Usage Examples - Core functionality and facade patterns.

This module demonstrates the fundamental operations and patterns of the FLEXT gRPC
communication platform, showcasing the unified FlextGrpc facade for entity creation,
validation, configuration, and service operations following Clean Architecture and
Domain-Driven Design principles.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_cli import cli


class ExamplesFlextGrpcBasicUsage:
    """Basic usage examples for flext-grpc."""

    def __init__(self) -> None:
        """Initialize with facade."""
        from flext_grpc import FlextGrpc, FlextGrpcConstants, FlextGrpcSettings

        self._grpc = FlextGrpc()
        self._constants = FlextGrpcConstants
        self._settings_cls = FlextGrpcSettings

    def _emit(self, message: str) -> None:
        """Emit example output through the canonical CLI facade."""
        cli.print(message)

    def example_1_basic_entities(self) -> None:
        """Create and use basic gRPC entities through the FlextGrpc facade."""
        grpc = self._grpc
        constants = self._constants
        server_result = grpc.create_server(
            host=constants.Grpc.NETWORK_DEFAULT_HOST,
            port=constants.Grpc.NETWORK_DEFAULT_GRPC_PORT,
            max_workers=10,
        )
        if server_result.success:
            server = server_result.value
            validation_result = server.validate_business_rules()
            if validation_result.failure:
                self._emit(f"Server validation failed: {validation_result.error}")
        grpc.create_channel(
            target=f"{constants.Grpc.NETWORK_DEFAULT_HOST}:{constants.Grpc.NETWORK_DEFAULT_GRPC_PORT}"
        )
        client_result = grpc.create_client(
            target=f"{constants.Grpc.NETWORK_DEFAULT_HOST}:{constants.Grpc.NETWORK_DEFAULT_GRPC_PORT}"
        )
        if client_result.failure:
            self._emit(f"Client creation failed: {client_result.error}")
        service_result = grpc.create_service(
            name="UserService",
            methods=["GetUser", "CreateUser", "UpdateUser", "DeleteUser"],
        )
        if service_result.failure:
            self._emit(f"Service creation failed: {service_result.error}")

    def example_2_configuration(self) -> None:
        """Use configuration through the FlextGrpc facade."""
        grpc = self._grpc
        settings_cls = self._settings_cls
        default_config = settings_cls()
        self._emit(
            f"Created settings with host: {default_config.Grpc.host}, port: {default_config.Grpc.port}"
        )
        custom_config = settings_cls.model_validate({
            "Grpc": {"host": "example.com", "port": 9090, "max_workers": 20}
        })
        self._emit(
            f"Created custom settings: {custom_config.Grpc.host}:{custom_config.Grpc.port}"
        )
        invalid_server_result = grpc.create_server(host="", port=0)
        if invalid_server_result.failure:
            self._emit(f"Expected validation failure: {invalid_server_result.error}")

    def example_3_operations(self) -> None:
        """Use gRPC operations through the FlextGrpc facade."""
        grpc = self._grpc
        constants = self._constants
        server_result = grpc.create_server(
            host=constants.Grpc.NETWORK_DEFAULT_HOST, port=7070
        )
        if server_result.success:
            server = server_result.value
            start_result = grpc.start_server(server)
            if start_result.success:
                started_server = start_result.value
                validation_result = started_server.validate_business_rules()
                if validation_result.success:
                    self._emit(f"Server status: {started_server.state}")
                stop_result = grpc.stop_server(started_server)
                if stop_result.success:
                    self._emit("Server stopped successfully")
        client_result = grpc.create_client(
            target=f"{constants.Grpc.NETWORK_DEFAULT_HOST}:7070"
        )
        if client_result.success:
            connect_result = grpc.connect_client(
                f"{constants.Grpc.NETWORK_DEFAULT_HOST}:7070"
            )
            if connect_result.success:
                connected_client = connect_result.value
                call_result = grpc.make_call(
                    connected_client, "GetServerInfo", {"request_id": "12345"}
                )
                if call_result.success:
                    self._emit(f"Call result: {call_result.value}")
                disconnect_result = grpc.disconnect_client(connected_client)
                if disconnect_result.success:
                    self._emit("Client disconnected successfully")

    def example_4_validation(self) -> None:
        """Validate domains through the FlextGrpc facade."""
        grpc = self._grpc
        constants = self._constants
        valid_server_result = grpc.create_server(
            host=constants.Grpc.NETWORK_DEFAULT_HOST,
            port=constants.Grpc.NETWORK_DEFAULT_GRPC_PORT,
            max_workers=5,
        )
        if valid_server_result.success:
            valid_server = valid_server_result.value
            validation = valid_server.validate_business_rules()
            if validation.success:
                self._emit("Valid server passed validation")
        invalid_server_result = grpc.create_server(host="", port=0, max_workers=0)
        if invalid_server_result.failure:
            self._emit(
                f"Invalid server creation failed as expected: {invalid_server_result.error}"
            )
        valid_channel_result = grpc.create_channel(
            target=f"{constants.Grpc.NETWORK_DEFAULT_HOST}:{constants.Grpc.NETWORK_DEFAULT_GRPC_PORT}"
        )
        if valid_channel_result.success:
            valid_channel = valid_channel_result.value
            validation = valid_channel.validate_business_rules()
            if validation.success:
                self._emit("Valid channel passed validation")
        invalid_channel_result = grpc.create_channel(target="")
        if invalid_channel_result.failure:
            self._emit(
                f"Invalid channel creation failed as expected: {invalid_channel_result.error}"
            )

    def example_5_state_transitions(self) -> None:
        """Exercise state transitions through the FlextGrpc facade."""
        grpc = self._grpc
        constants = self._constants
        channel_result = grpc.create_channel(
            target=f"{constants.Grpc.NETWORK_DEFAULT_HOST}:{constants.Grpc.NETWORK_DEFAULT_GRPC_PORT}"
        )
        if channel_result.success:
            channel = channel_result.value
            self._emit(f"Channel created with state: {channel.state}")
        server_result = grpc.create_server()
        if server_result.success:
            server = server_result.value
            start_result = grpc.start_server(server)
            if start_result.success:
                started_server = start_result.value
                self._emit(f"Server started with state: {started_server.state}")
                stop_result = grpc.stop_server(started_server)
                if stop_result.success:
                    stopped_server = stop_result.value
                    self._emit(f"Server stopped with state: {stopped_server.state}")

    def main(self) -> None:
        """Run all examples."""
        self.example_1_basic_entities()
        self.example_2_configuration()
        self.example_3_operations()
        self.example_4_validation()
        self.example_5_state_transitions()


if __name__ == "__main__":
    ExamplesFlextGrpcBasicUsage().main()
