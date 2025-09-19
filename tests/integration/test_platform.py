"""Integration tests for gRPC platform components.

Following enterprise testing standards with real component integration.
Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT.
"""

from __future__ import annotations

from flext_core import FlextResult
from flext_grpc import (
    FlextGrpcClientService,
    FlextGrpcPlatform,
    FlextGrpcServerService,
    FlextGrpcStreamService,
    create_client,
    create_server,
    create_service,
)


class TestPlatformIntegration:
    """Test platform integration with all components."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.platform = FlextGrpcPlatform()
        self.server_service = FlextGrpcServerService()
        self.client_service = FlextGrpcClientService()
        self.stream_service = FlextGrpcStreamService()

    def execute_service_command(
        self, service_type: str, command: str, *args: object, **kwargs: object,
    ) -> FlextResult:
        """Route service commands to appropriate service instances."""
        if service_type == "server":
            return self.server_service.execute(command, *args, **kwargs)
        if service_type == "client":
            return self.client_service.execute(command, *args, **kwargs)
        if service_type == "stream":
            return self.stream_service.execute(command, *args, **kwargs)

        return FlextResult.fail(f"Unknown service type: {service_type}")

    def test_platform_server_lifecycle(self) -> None:
        """Test complete server lifecycle through platform."""
        # Create server
        server = create_server("localhost", 9000)

        # Start server
        start_result = self.platform.start_server(server)
        assert start_result.success
        started_server = start_result.data
        assert started_server.is_running

        # Get server status
        status_result = self.platform.get_server_status(started_server)
        assert status_result.success
        status = status_result.data
        if status["address"] != "localhost:9000":
            msg: str = f"Expected {'localhost:9000'}, got {status['address']}"
            raise AssertionError(msg)
        if not (status["is_running"]):
            msg: str = f"Expected True, got {status['is_running']}"
            raise AssertionError(msg)
        if status["state"] != "running":
            msg: str = f"Expected {'running'}, got {status['state']}"
            raise AssertionError(msg)

        # Stop server
        stop_result = self.platform.stop_server(started_server)
        assert stop_result.success
        stopped_server = stop_result.data
        assert not stopped_server.is_running

    def test_platform_client_lifecycle(self) -> None:
        """Test complete client lifecycle through platform."""
        # Create client
        client = create_client("localhost:9001")

        # Connect client
        connect_result = self.platform.connect_client(client)
        assert connect_result.success
        connected_client = connect_result.data
        assert connected_client.is_connected

        # Get client status
        status_result = self.platform.get_client_status(connected_client)
        assert status_result.success
        status = status_result.data
        if not (status["is_connected"]):
            msg: str = f"Expected True, got {status['is_connected']}"
            raise AssertionError(msg)
        if status["target"] != "localhost:9001":
            msg: str = f"Expected {'localhost:9001'}, got {status['target']}"
            raise AssertionError(msg)
        assert status["channel_state"] == "ready"

        # Make call
        call_result = self.platform.make_call(
            connected_client,
            "test_method",
            {"data": "test"},
        )
        assert call_result.success
        response = call_result.data
        if response["status"] != "success":
            msg: str = f"Expected {'success'}, got {response['status']}"
            raise AssertionError(msg)
        assert response["method"] == "test_method"

    def test_platform_stream_operations(self) -> None:
        """Test stream operations through platform."""
        # Create connected client
        client = create_client("localhost:9002")
        connect_result = self.platform.connect_client(client)
        connected_client = connect_result.data

        # Create stream
        stream_result = self.platform.create_stream(
            connected_client,
            "stream_method",
            "server_streaming",
        )
        assert stream_result.success
        stream = stream_result.data
        if stream.method_name != "stream_method":
            msg: str = f"Expected {'stream_method'}, got {stream.method_name}"
            raise AssertionError(msg)
        assert stream.stream_type == "server_streaming"
        assert stream.is_server_streaming

    def test_service_integration_with_platform(self) -> None:
        """Test direct service integration with platform."""
        server = create_server("localhost", 9003)

        # Test server operations through service
        start_result = self.execute_service_command("server", "start", server)
        assert start_result.success

        # Test same operations through platform
        platform_start_result = self.platform.server_operation("start", server)
        assert platform_start_result.success

        # Results should be consistent
        service_server = start_result.data
        platform_server = platform_start_result.data
        if service_server.state != platform_server.state:
            msg: str = f"Expected {platform_server.state}, got {service_server.state}"
            raise AssertionError(msg)

    def test_full_grpc_workflow(self) -> None:
        """Test complete gRPC workflow integration."""
        # 1. Create and start server
        server = create_server("localhost", 9004, 5)
        start_result = self.platform.start_server(server)
        started_server = start_result.data

        # 2. Add service to server
        service_entity = create_service("IntegrationService", ["integration_method"])
        add_service_result = self.platform.server_operation(
            "add_service",
            started_server,
            service=service_entity,
        )
        assert add_service_result.success
        server_with_service = add_service_result.data
        if len(server_with_service.services) != 1:
            msg: str = f"Expected {1}, got {len(server_with_service.services)}"
            raise AssertionError(msg)

        # 3. Create and connect client
        client = create_client("localhost:9004")
        connect_result = self.platform.connect_client(client)
        connected_client = connect_result.data

        # 4. Make call through client
        call_result = self.platform.make_call(
            connected_client,
            "integration_method",
            {"integration": True, "test_data": [1, 2, 3]},
        )
        assert call_result.success
        response = call_result.data
        if response["method"] != "integration_method":
            msg: str = f"Expected {'integration_method'}, got {response['method']}"
            raise AssertionError(msg)
        if not (response["data"]["integration"]):
            msg: str = f"Expected True, got {response['data']['integration']}"
            raise AssertionError(msg)

        # 5. Create stream
        stream_result = self.platform.create_stream(
            connected_client,
            "integration_stream",
            "bidirectional",
        )
        assert stream_result.success
        stream = stream_result.data
        assert stream.is_bidirectional

        # 6. Get final status
        final_status = self.platform.get_server_status(server_with_service)
        assert final_status.success
        status = final_status.data
        if status["service_count"] != 1:
            msg: str = f"Expected {1}, got {status['service_count']}"
            raise AssertionError(msg)
        if not (status["is_running"]):
            msg: str = f"Expected True, got {status['is_running']}"
            raise AssertionError(msg)

    def test_error_propagation_integration(self) -> None:
        """Test error propagation through all layers."""
        # Invalid server should fail at all levels
        invalid_server = create_server("", 0)  # Invalid configuration

        # Service level
        service_result = self.execute_service_command("server", "start", invalid_server)
        assert service_result.is_failure
        if "Invalid server" not in service_result.error:
            msg: str = f"Expected {'Invalid server'} in {service_result.error}"
            raise AssertionError(msg)

        # Platform level
        platform_result = self.platform.start_server(invalid_server)
        assert platform_result.is_failure
        if "Invalid server" not in platform_result.error:
            msg: str = f"Expected {'Invalid server'} in {platform_result.error}"
            raise AssertionError(msg)

    def test_state_consistency_across_operations(self) -> None:
        """Test state consistency across different operations."""
        server = create_server("localhost", 9005)

        # Start through service
        service_result = self.execute_service_command("server", "start", server)
        service_server = service_result.data

        # Check status through platform
        platform_status = self.platform.get_server_status(service_server)
        status = platform_status.data

        # States should be consistent
        assert service_server.is_running
        if not (status["is_running"]):
            msg: str = f"Expected True, got {status['is_running']}"
            raise AssertionError(msg)
        if status["state"] != "running":
            msg: str = f"Expected {'running'}, got {status['state']}"
            raise AssertionError(msg)

    def test_concurrent_operations(self) -> None:
        """Test concurrent operations don't interfere."""
        # Create multiple servers
        servers = [create_server("localhost", 9006 + i) for i in range(3)]

        # Start all servers
        started_servers = []
        for server in servers:
            result = self.platform.start_server(server)
            assert result.success
            started_servers.append(result.data)

        # All servers should be running independently
        for server in started_servers:
            assert server.is_running
            status_result = self.platform.get_server_status(server)
            assert status_result.success
            if not (status_result.data["is_running"]):
                msg: str = f"Expected True, got {status_result.data['is_running']}"
                raise AssertionError(msg)

    def test_configuration_propagation(self) -> None:
        """Test configuration propagation through platform."""
        config = {"custom_option": "test_value"}
        platform = FlextGrpcPlatform(config)

        if platform.config != config:
            msg: str = f"Expected {config}, got {platform.config}"
            raise AssertionError(msg)

        # Platform should still work with custom config
        server = create_server()
        result = platform.start_server(server)
        assert result.success

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
