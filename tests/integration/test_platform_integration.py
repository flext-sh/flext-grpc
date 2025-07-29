"""Integration tests for FLEXT gRPC platform.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from datetime import UTC, datetime

import pytest
from flext_core.utilities import FlextGenerators

from flext_grpc.api import create_client, create_server, create_service
from flext_grpc.entities import FlextGrpcChannel, FlextGrpcService as FlextGrpcServiceEntity
from flext_grpc.platform import FlextGrpcPlatform
from flext_grpc.services import FlextGrpcService
from flext_grpc.types import TGrpcTarget


class TestPlatformIntegration:
    """Test platform integration with all components."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.platform = FlextGrpcPlatform()
        self.service = FlextGrpcService()
        
    def test_platform_server_lifecycle(self) -> None:
        """Test complete server lifecycle through platform."""
        # Create server
        server = create_server("localhost", 9000)
        
        # Start server
        start_result = self.platform.start_server(server)
        assert start_result.is_success
        started_server = start_result.data
        assert started_server.is_running()
        
        # Get server status
        status_result = self.platform.get_server_status(started_server)
        assert status_result.is_success
        status = status_result.data
        assert status["address"] == "localhost:9000"
        assert status["is_running"] is True
        assert status["state"] == "running"
        
        # Stop server
        stop_result = self.platform.stop_server(started_server)
        assert stop_result.is_success
        stopped_server = stop_result.data
        assert not stopped_server.is_running()

    def test_platform_client_lifecycle(self) -> None:
        """Test complete client lifecycle through platform."""
        # Create client
        client = create_client("localhost:9001")
        
        # Connect client
        connect_result = self.platform.connect_client(client)
        assert connect_result.is_success
        connected_client = connect_result.data
        assert connected_client.is_connected()
        
        # Get client status
        status_result = self.platform.get_client_status(connected_client)
        assert status_result.is_success
        status = status_result.data
        assert status["is_connected"] is True
        assert status["channel_target"] == "localhost:9001"
        assert status["channel_state"] == "ready"
        
        # Make call
        call_result = self.platform.make_call(
            connected_client, "test_method", {"data": "test"}
        )
        assert call_result.is_success
        response = call_result.data
        assert response["status"] == "success"
        assert response["method"] == "test_method"

    def test_platform_stream_operations(self) -> None:
        """Test stream operations through platform."""
        # Create connected client
        client = create_client("localhost:9002")
        connect_result = self.platform.connect_client(client)
        connected_client = connect_result.data
        
        # Create stream
        stream_result = self.platform.create_stream(
            connected_client, "stream_method", "server_streaming"
        )
        assert stream_result.is_success
        stream = stream_result.data
        assert stream.method_name == "stream_method"
        assert stream.stream_type == "server_streaming"
        assert stream.is_server_streaming()

    def test_service_integration_with_platform(self) -> None:
        """Test direct service integration with platform."""
        server = create_server("localhost", 9003)
        
        # Test server operations through service
        start_result = self.service.execute("server", "start", server)
        assert start_result.is_success
        
        # Test same operations through platform
        platform_start_result = self.platform.server_operation("start", server)
        assert platform_start_result.is_success
        
        # Results should be consistent
        service_server = start_result.data
        platform_server = platform_start_result.data
        assert service_server.state == platform_server.state

    def test_full_grpc_workflow(self) -> None:
        """Test complete gRPC workflow integration."""
        # 1. Create and start server
        server = create_server("localhost", 9004, 5)
        start_result = self.platform.start_server(server)
        started_server = start_result.data
        
        # 2. Add service to server
        service_entity = create_service("IntegrationService", ["integration_method"])
        add_service_result = self.platform.server_operation(
            "add_service", started_server, service=service_entity
        )
        assert add_service_result.is_success
        server_with_service = add_service_result.data
        assert len(server_with_service.services) == 1
        
        # 3. Create and connect client
        client = create_client("localhost:9004")
        connect_result = self.platform.connect_client(client)
        connected_client = connect_result.data
        
        # 4. Make call through client
        call_result = self.platform.make_call(
            connected_client, 
            "integration_method",
            {"integration": True, "test_data": [1, 2, 3]}
        )
        assert call_result.is_success
        response = call_result.data
        assert response["method"] == "integration_method"
        assert response["data"]["integration"] is True
        
        # 5. Create stream
        stream_result = self.platform.create_stream(
            connected_client, "integration_stream", "bidirectional"
        )
        assert stream_result.is_success
        stream = stream_result.data
        assert stream.is_bidirectional()
        
        # 6. Get final status
        final_status = self.platform.get_server_status(server_with_service)
        assert final_status.is_success
        status = final_status.data
        assert status["service_count"] == 1
        assert status["is_running"] is True

    def test_error_propagation_integration(self) -> None:
        """Test error propagation through all layers."""
        # Invalid server should fail at all levels
        invalid_server = create_server("", 0)  # Invalid configuration
        
        # Service level
        service_result = self.service.execute("server", "start", invalid_server)
        assert service_result.is_failure
        assert "Invalid server" in service_result.error
        
        # Platform level
        platform_result = self.platform.start_server(invalid_server)
        assert platform_result.is_failure
        assert "Invalid server" in platform_result.error

    def test_state_consistency_across_operations(self) -> None:
        """Test state consistency across different operations."""
        server = create_server("localhost", 9005)
        
        # Start through service
        service_result = self.service.execute("server", "start", server)
        service_server = service_result.data
        
        # Check status through platform
        platform_status = self.platform.get_server_status(service_server)
        status = platform_status.data
        
        # States should be consistent
        assert service_server.is_running()
        assert status["is_running"] is True
        assert status["state"] == "running"

    def test_concurrent_operations(self) -> None:
        """Test concurrent operations don't interfere."""
        # Create multiple servers
        servers = [
            create_server("localhost", 9006 + i) 
            for i in range(3)
        ]
        
        # Start all servers
        started_servers = []
        for server in servers:
            result = self.platform.start_server(server)
            assert result.is_success
            started_servers.append(result.data)
        
        # All servers should be running independently
        for server in started_servers:
            assert server.is_running()
            status_result = self.platform.get_server_status(server)
            assert status_result.is_success
            assert status_result.data["is_running"] is True

    def test_configuration_propagation(self) -> None:
        """Test configuration propagation through platform."""
        config = {"custom_option": "test_value"}
        platform = FlextGrpcPlatform(config)
        
        assert platform.config == config
        
        # Platform should still work with custom config
        server = create_server()
        result = platform.start_server(server)
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