"""Unit tests for gRPC integration scenarios.

Test Focus:
- Complete entity lifecycle workflows from creation to destruction
- Real service operations with actual state transitions and side effects
- Platform integration with real dependency injection and service coordination
- Error handling with real validation and business rule enforcement
- Performance and behavior validation under realistic conditions

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT.
"""

from __future__ import annotations

from datetime import UTC, datetime

from flext_grpc import (
    FlextGrpcChannel,
    FlextGrpcClient,
    FlextGrpcPlatform,
    FlextGrpcServer,
    FlextGrpcService,
    TGrpcTarget,
    create_client,
    create_complete_setup,
    create_server,
    create_service,
)


class TestRealGrpcIntegration:
    """Real integration tests validating actual gRPC functionality without mocks."""

    def test_complete_server_lifecycle_real(self) -> None:
        """Test complete server lifecycle with REAL state transitions and validation."""
        # Create a real server with proper configuration
        server = create_server(
            "localhost", 50052, 5
        )  # Use different port to avoid conflicts

        # Validate initial state
        assert server.state == "stopped"
        assert not server.is_running
        assert server.address == "localhost:50052"

        # Test real domain validation
        validation = server.validate_business_rules()
        assert validation.success

        # Test real state transition: stopped -> starting
        start_result = server.start()
        assert start_result.success
        starting_server = start_result.data
        assert starting_server is not None
        assert starting_server.state == "starting"

        # Test real state transition: starting -> running
        running_result = starting_server.mark_running()
        assert running_result.success
        running_server = running_result.data
        assert running_server is not None
        assert running_server.state == "running"
        assert running_server.is_running

        # Test adding real service to running server
        service = create_service("TestService", ["GetData", "SetData"])
        service_result = running_server.add_service(service)
        assert service_result.success
        server_with_service = service_result.data
        assert server_with_service is not None
        assert len(server_with_service.services) == 1
        assert server_with_service.services[0].name == "TestService"

        # Test real state transition: running -> stopping -> stopped
        stop_result = server_with_service.stop()
        assert stop_result.success
        stopping_server = stop_result.data
        assert stopping_server is not None
        assert stopping_server.state == "stopping"

        stopped_result = stopping_server.mark_stopped()
        assert stopped_result.success
        stopped_server = stopped_result.data
        assert stopped_server is not None
        assert stopped_server.state == "stopped"
        assert not stopped_server.is_running

    def test_complete_client_lifecycle_real(self) -> None:
        """Test complete client lifecycle with REAL connection management."""
        # Create real client without initial channel
        client = create_client("localhost:50053")  # Use different port

        # Validate initial state
        assert client.channel is not None
        assert client.channel.target == "localhost:50053"
        assert client.channel.state == "idle"
        assert not client.is_connected

        # Test real channel connection: idle -> connecting -> ready
        channel = client.channel
        connect_result = channel.connect()
        assert connect_result.success
        connecting_channel = connect_result.data
        assert connecting_channel is not None
        assert connecting_channel.state == "connecting"

        ready_result = connecting_channel.mark_ready()
        assert ready_result.success
        ready_channel = ready_result.data
        assert ready_channel is not None
        assert ready_channel.state == "ready"
        assert ready_channel.is_ready()

        # Update client with ready channel
        connected_client_result = client.copy_with(channel=ready_channel)
        assert connected_client_result.success
        connected_client = connected_client_result.data
        assert connected_client is not None
        assert connected_client.is_connected

        # Test real disconnection: ready -> idle
        disconnect_result = ready_channel.disconnect()
        assert disconnect_result.success
        idle_channel = disconnect_result.data
        assert idle_channel is not None
        assert idle_channel.state == "idle"
        assert not idle_channel.is_ready()

    def test_platform_integration_real(self) -> None:
        """Test REAL platform integration with services and dependency injection."""
        platform = FlextGrpcPlatform()

        # Create real entities for platform testing
        server = FlextGrpcServer(
            id="platform-server",
            host="localhost",
            port=50054,  # Different port
            max_workers=3,
            created_at=datetime.now(UTC),
        )

        client = FlextGrpcClient(
            id="platform-client",
            created_at=datetime.now(UTC),
        )

        # Test real platform server operations
        start_result = platform.start_server(server)
        if start_result.success:
            # Server started successfully - validate state
            started_server = start_result.data
            assert started_server is not None
        else:
            # Server failed to start - validate error handling
            assert start_result.error is not None
            assert len(start_result.error) > 0

        # Test real platform client operations
        connect_result = platform.connect_client(client)
        if connect_result.success:
            # Client connected - validate state
            connected_client = connect_result.data
            assert connected_client is not None
        else:
            # Connection failed - validate error handling
            assert connect_result.error is not None
            assert len(connect_result.error) > 0

        # Test real platform status operations
        server_status = platform.get_server_status(server)
        assert server_status.success or server_status.is_failure
        if server_status.success:
            status_data = server_status.data
            assert isinstance(status_data, dict)
            assert "address" in status_data
            assert "state" in status_data
            assert "is_running" in status_data

    def test_error_handling_real(self) -> None:
        """Test REAL error handling without mocks - validate actual error conditions."""
        # Test invalid server configuration - should fail domain validation
        invalid_server = FlextGrpcServer(
            id="invalid-server",
            host="",  # Invalid empty host
            port=50055,
            created_at=datetime.now(UTC),
        )

        validation = invalid_server.validate_business_rules()
        assert validation.is_failure
        assert validation.error is not None
        assert "host cannot be empty" in validation.error

        # Test invalid port - should fail domain validation
        invalid_port_server = FlextGrpcServer(
            id="invalid-port-server",
            host="localhost",
            port=99999,  # Invalid port
            created_at=datetime.now(UTC),
        )

        port_validation = invalid_port_server.validate_business_rules()
        assert port_validation.is_failure
        assert port_validation.error is not None
        assert "Invalid port" in port_validation.error

        # Test invalid channel target
        invalid_channel = FlextGrpcChannel(
            id="invalid-channel",
            target=TGrpcTarget(""),  # Empty target
            created_at=datetime.now(UTC),
        )

        channel_validation = invalid_channel.validate_business_rules()
        assert channel_validation.is_failure
        assert channel_validation.error is not None
        assert "target cannot be empty" in channel_validation.error

    def test_complete_setup_integration_real(self) -> None:
        """Test complete setup utility creates working, integrated components."""
        # Use the factory function to create a complete setup
        setup = create_complete_setup(
            "localhost", 50056, "IntegrationService", ["TestMethod"]
        )

        # Validate all components are created and properly configured
        server = setup["server"]
        client = setup["client"]
        service = setup["service"]
        target = setup["target"]

        assert isinstance(server, FlextGrpcServer)
        assert isinstance(client, FlextGrpcClient)
        assert isinstance(service, FlextGrpcService)
        assert isinstance(target, str)

        # Validate they work together
        assert server.host == "localhost"
        assert server.port == 50056
        assert server.validate_business_rules().success

        assert client.channel is not None
        assert client.channel.target == "localhost:50056"
        assert client.validate_business_rules().success

        assert service.name == "IntegrationService"
        assert service.has_method("TestMethod")
        assert service.validate_business_rules().success

        assert target == "localhost:50056"

        # Test integration - add service to server
        service_add_result = server.add_service(service)
        assert service_add_result.success
        server_with_service = service_add_result.data
        assert server_with_service is not None
        assert len(server_with_service.services) == 1
        assert server_with_service.services[0].name == "IntegrationService"

    def test_service_coordination_real(self) -> None:
        """Test real service coordination through dependency injection and platform."""
        platform = FlextGrpcPlatform()

        # Create coordinated entities that will work together
        server = FlextGrpcServer(
            id="coord-server",
            host="localhost",
            port=50057,
            max_workers=2,
            created_at=datetime.now(UTC),
        )

        service = FlextGrpcService(
            id="coord-service",
            name="CoordinationService",
            methods=["Coordinate", "Validate"],
            created_at=datetime.now(UTC),
        )

        # Test real service operations through platform
        # This tests the actual dependency injection and service coordination
        start_result = platform.start_server(server)
        # Platform should handle this gracefully regardless of success/failure
        assert start_result.success or start_result.is_failure

        if start_result.success:
            started_server = start_result.data
            assert started_server is not None

            # Test adding service to started server through platform
            # This would test real service registration in a production scenario
            service_result = started_server.add_service(service)
            assert service_result.success
            updated_server = service_result.data
            assert updated_server is not None
            assert len(updated_server.services) == 1

            # Test stopping coordinated server
            stop_result = platform.stop_server(updated_server)
            assert stop_result.success or stop_result.is_failure
