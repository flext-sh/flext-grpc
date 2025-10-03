"""Integration tests for gRPC platform components.

Following enterprise testing standards with real component integration.
Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT.
"""

from __future__ import annotations

from typing import cast

from flext_core import FlextResult, FlextTypes
from flext_grpc import (
    FlextGrpcClient,
    FlextGrpcPlatform,
    FlextGrpcServer,
    FlextGrpcServerService,
    FlextGrpcStream,
    create_client,
    create_server,
    create_service,
)


class TestPlatformIntegration:
    """Test platform integration with all components."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.platform = FlextGrpcPlatform()
        self.service = FlextGrpcServerService()

    def execute_service_command(
        self,
        command: str,
        entity: FlextGrpcServer | FlextGrpcClient | FlextGrpcStream | None = None,
        *args: object,
        **kwargs: object,
    ) -> FlextResult[object]:
        """Route service commands to appropriate service instances."""
        return cast(
            "FlextResult[object]",
            self.service.execute(command, entity, *args, **kwargs),
        )

    def test_platform_server_lifecycle(self) -> None:
        """Test complete server lifecycle through platform."""
        # Create server
        server = create_server("localhost", 9000)

        # Start server
        start_result: FlextResult[FlextGrpcServer] = self.platform.start_server(server)
        assert start_result.is_success
        started_server: FlextGrpcServer = start_result.data
        assert started_server.is_running

        # Get server status
        status_result: FlextResult[FlextTypes.Dict] = self.platform.get_server_status(
            started_server
        )
        assert status_result.is_success
        status: FlextTypes.Dict = status_result.data
        if status["address"] != "localhost:9000":
            address_msg: str = f"Expected {'localhost:9000'}, got {status['address']}"
            raise AssertionError(address_msg)
        if not (status["is_running"]):
            running_msg: str = f"Expected True, got {status['is_running']}"
            raise AssertionError(running_msg)
        if status["state"] != "running":
            state_msg: str = f"Expected {'running'}, got {status['state']}"
            raise AssertionError(state_msg)

        # Stop server
        stop_result: FlextResult[FlextGrpcServer] = self.platform.stop_server(
            started_server
        )
        assert stop_result.is_success
        stopped_server: FlextGrpcServer = stop_result.data
        assert not stopped_server.is_running

    def test_platform_client_lifecycle(self) -> None:
        """Test complete client lifecycle through platform."""
        # Create client
        client = create_client("localhost:9001")

        # Connect client
        connect_result: FlextResult[FlextGrpcClient] = self.platform.connect_client(
            client
        )
        assert connect_result.is_success
        connected_client: FlextGrpcClient = connect_result.data
        assert connected_client.is_connected

        # Get client status
        status_result: FlextResult[FlextTypes.Dict] = self.platform.get_client_status(
            connected_client
        )
        assert status_result.is_success
        status: FlextTypes.Dict = status_result.data
        if not (status["is_connected"]):
            connected_msg: str = f"Expected True, got {status['is_connected']}"
            raise AssertionError(connected_msg)
        if status["target"] != "localhost:9001":
            target_msg: str = f"Expected {'localhost:9001'}, got {status['target']}"
            raise AssertionError(target_msg)
        assert status["channel_state"] == "ready"

        # Make call
        call_result: FlextResult[FlextTypes.Dict] = self.platform.make_call(
            connected_client,
            "test_method",
            data="test",
        )
        assert call_result.is_success
        response: FlextTypes.Dict = call_result.data
        if response["status"] != "success":
            status_msg: str = f"Expected {'success'}, got {response['status']}"
            raise AssertionError(status_msg)
        assert response["method"] == "test_method"

    def test_platform_stream_operations(self) -> None:
        """Test stream operations through platform."""
        # Create connected client
        client = create_client("localhost:9002")
        self.platform.connect_client(client)

        # Create stream
        stream_result: FlextResult[FlextGrpcStream] = self.platform.create_stream(
            "server_streaming",
            "stream_method",
        )
        assert stream_result.is_success
        stream: FlextGrpcStream = stream_result.data
        if stream.method_name != "stream_method":
            method_msg: str = f"Expected {'stream_method'}, got {stream.method_name}"
            raise AssertionError(method_msg)
        assert stream.stream_type == "server_streaming"
        assert stream.is_server_streaming

    def test_service_integration_with_platform(self) -> None:
        """Test direct service integration with platform."""
        server = create_server("localhost", 9003)

        # Test server operations through service
        start_result: FlextResult[object] = self.execute_service_command(
            "start", server
        )
        assert start_result.is_success

        # Test same operations through platform
        platform_start_result: FlextResult[object] = cast(
            "FlextResult[object]", self.platform.server_operation("start", server)
        )
        assert platform_start_result.is_success

        # Results should be consistent
        service_server: object = start_result.data
        platform_server: object = platform_start_result.data
        if (
            hasattr(service_server, "state")
            and hasattr(platform_server, "state")
            and service_server.state != platform_server.state
        ):
            consistency_msg: str = (
                f"Expected {platform_server.state}, got {service_server.state}"
            )
            raise AssertionError(consistency_msg)

    def test_full_grpc_workflow(self) -> None:
        """Test complete gRPC workflow integration."""
        # 1. Create and start server
        server: FlextGrpcServer = create_server("localhost", 9004, 5)
        start_result: FlextResult[FlextGrpcServer] = self.platform.start_server(server)
        started_server: FlextGrpcServer = start_result.data

        # 2. Add service to server
        service_entity = create_service("IntegrationService", ["integration_method"])
        add_service_result: FlextResult[object] = cast(
            "FlextResult[object]",
            self.platform.server_operation(
                "add_service",
                started_server,
                service=service_entity,
            ),
        )
        assert add_service_result.is_success
        server_with_service: object = add_service_result.data
        if (
            hasattr(server_with_service, "services")
            and server_with_service.services
            and len(server_with_service.services) != 1
        ):
            service_count_msg: str = (
                f"Expected {1}, got {len(server_with_service.services)}"
            )
            raise AssertionError(service_count_msg)

        # 3. Create and connect client
        client: FlextGrpcClient = create_client("localhost:9004")
        connect_result: FlextResult[FlextGrpcClient] = self.platform.connect_client(
            client
        )
        connected_client: FlextGrpcClient = connect_result.data

        # 4. Make call through client
        call_result: FlextResult[FlextTypes.Dict] = self.platform.make_call(
            connected_client,
            "integration_method",
            integration=True,
            test_data=[1, 2, 3],
        )
        assert call_result.is_success
        response: FlextTypes.Dict = call_result.data
        if response["method"] != "integration_method":
            method_name_msg: str = (
                f"Expected {'integration_method'}, got {response['method']}"
            )
            raise AssertionError(method_name_msg)
        response_data = response.get("data", {})
        if isinstance(response_data, dict) and not response_data.get("integration"):
            integration_msg: str = (
                f"Expected True, got {response_data.get('integration')}"
            )
            raise AssertionError(integration_msg)

        # 5. Create stream
        stream_result: FlextResult[FlextGrpcStream] = self.platform.create_stream(
            "bidirectional",
            "integration_stream",
        )
        assert stream_result.is_success
        stream: FlextGrpcStream = stream_result.data
        assert stream.is_bidirectional

        # 6. Get final status
        final_status: FlextResult[FlextTypes.Dict] = self.platform.get_server_status(
            started_server
        )
        assert final_status.is_success
        status: FlextTypes.Dict = final_status.data
        if status["service_count"] != 1:
            service_count_final_msg: str = (
                f"Expected {1}, got {status['service_count']}"
            )
            raise AssertionError(service_count_final_msg)
        if not (status["is_running"]):
            running_final_msg: str = f"Expected True, got {status['is_running']}"
            raise AssertionError(running_final_msg)

    def test_error_propagation_integration(self) -> None:
        """Test error propagation through all layers."""
        # Invalid server should fail at all levels
        invalid_server = create_server("", 0)  # Invalid configuration

        # Service level
        service_result: FlextResult[object] = self.execute_service_command(
            "start", invalid_server
        )
        assert service_result.is_failure
        if service_result.error and "Invalid server" not in service_result.error:
            error_msg: str = f"Expected {'Invalid server'} in {service_result.error}"
            raise AssertionError(error_msg)

        # Platform level
        platform_result: FlextResult[FlextGrpcServer] = self.platform.start_server(
            invalid_server
        )
        assert platform_result.is_failure
        if platform_result.error and "Invalid server" not in platform_result.error:
            platform_error_msg: str = (
                f"Expected {'Invalid server'} in {platform_result.error}"
            )
            raise AssertionError(platform_error_msg)

    def test_state_consistency_across_operations(self) -> None:
        """Test state consistency across different operations."""
        server = create_server("localhost", 9005)

        # Start through service
        service_result: FlextResult[object] = self.execute_service_command(
            "start", server
        )
        service_server: object = service_result.data

        # Check status through platform
        platform_status: FlextResult[FlextTypes.Dict] = self.platform.get_server_status(
            cast("FlextGrpcServer", service_server)
        )
        status: FlextTypes.Dict = platform_status.data

        # States should be consistent
        assert cast("FlextGrpcServer", service_server).is_running
        if not (status["is_running"]):
            running_consistency_msg: str = f"Expected True, got {status['is_running']}"
            raise AssertionError(running_consistency_msg)
        if status["state"] != "running":
            state_consistency_msg: str = f"Expected {'running'}, got {status['state']}"
            raise AssertionError(state_consistency_msg)

    def test_concurrent_operations(self) -> None:
        """Test concurrent operations don't interfere."""
        # Create multiple servers
        servers = [create_server("localhost", 9006 + i) for i in range(3)]

        # Start all servers
        started_servers: list[FlextGrpcServer] = []
        for server in servers:
            result: FlextResult[FlextGrpcServer] = self.platform.start_server(server)
            assert result.is_success
            started_servers.append(result.data)

        # All servers should be running independently
        for server in started_servers:
            assert server.is_running
            status_result: FlextResult[FlextTypes.Dict] = (
                self.platform.get_server_status(server)
            )
            assert status_result.is_success
            if not (status_result.data["is_running"]):
                concurrent_msg: str = (
                    f"Expected True, got {status_result.data['is_running']}"
                )
                raise AssertionError(concurrent_msg)

    def test_configuration_propagation(self) -> None:
        """Test configuration propagation through platform."""
        config = {"custom_option": "test_value"}
        platform = FlextGrpcPlatform(config)

        if platform.config != config:
            config_msg: str = f"Expected {config}, got {platform.config}"
            raise AssertionError(config_msg)

        # Platform should still work with custom config
        server: FlextGrpcServer = create_server()
        result: FlextResult[FlextGrpcServer] = platform.start_server(server)
        assert result.is_success

    def test_global_container_usage(self) -> None:
        """Test that platform uses global container correctly."""
        platform1 = FlextGrpcPlatform()
        platform2 = FlextGrpcPlatform()

        # Both platforms should share the same container
        assert platform1.container is platform2.container

        # Service should be registered globally
        service1 = platform1.service
        service2 = platform2.service

        # Should be the same instance from global container
        assert service1 is service2
