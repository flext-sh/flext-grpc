"""FLEXT gRPC Services REAL Implementation Tests.

This module validates that the gRPC domain services actually perform REAL gRPC operations,
not simulations. Tests start actual gRPC servers, make real connections, and validate
that the services work with real gRPC infrastructure.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from datetime import UTC, datetime

import grpc
from flext_core import FlextModels, FlextModels.Timestamp

from flext_grpc import (
    FlextGrpcChannel,
    FlextGrpcClient,
    FlextGrpcServer,
    FlextGrpcService,
)
from flext_grpc.services import FlextGrpcClientService, FlextGrpcServerService


class TestRealGrpcServices:
    """Test that domain services perform REAL gRPC operations."""

    def test_server_service_starts_real_grpc_server(self) -> None:
        """Test that FlextGrpcServerService starts a REAL gRPC server."""
        server_service = FlextGrpcServerService()

        # Create server entity
        server = FlextGrpcServer(
            id=FlextModels.EntityId("test-real-server"),
            host="localhost",
            port=0,  # Let gRPC choose port
            max_workers=2,
            created_at=FlextModels.Timestamp(datetime.now(UTC)),
        )

        # Start server - should create REAL gRPC server
        start_result = server_service.execute("start", server)
        assert start_result.success, f"Server start failed: {start_result.error}"

        running_server = start_result.data
        assert running_server is not None
        assert running_server.state == "running"
        assert running_server.port > 0  # Should have assigned a real port

        # Verify real gRPC server is accessible
        server_key = f"{running_server.host}:{running_server.port}"
        assert server_key in server_service._active_servers

        # Test real connectivity to the server
        test_channel = grpc.insecure_channel(
            f"{running_server.host}:{running_server.port}"
        )
        try:
            # This should succeed if real server is running
            grpc.channel_ready_future(test_channel).result(timeout=2.0)
            connectivity_success = True
        except grpc.FutureTimeoutError:
            connectivity_success = False
        finally:
            test_channel.close()

        assert connectivity_success, f"Real gRPC server not accessible at {server_key}"

        # Get status - should include real server info
        status_result = server_service.execute("status", running_server)
        assert status_result.success
        status = status_result.data
        assert isinstance(status, dict)
        assert status["grpc_server_active"] is True
        assert status["server_key"] == server_key

        # Stop server - should shutdown REAL gRPC server
        stop_result = server_service.execute("stop", running_server)
        assert stop_result.success, f"Server stop failed: {stop_result.error}"

        stopped_server = stop_result.data
        assert stopped_server is not None
        assert stopped_server.state == "stopped"

        # Verify real server was removed
        assert server_key not in server_service._active_servers

    def test_client_service_makes_real_grpc_connections(self) -> None:
        """Test that FlextGrpcClientService makes REAL gRPC connections."""
        # First, start a real server to connect to
        server_service = FlextGrpcServerService()

        server = FlextGrpcServer(
            id=FlextModels.EntityId("target-server"),
            host="localhost",
            port=0,
            max_workers=2,
            created_at=FlextModels.Timestamp(datetime.now(UTC)),
        )

        start_result = server_service.execute("start", server)
        assert start_result.success
        running_server = start_result.data
        assert running_server is not None

        try:
            # Create client and attempt real connection
            client_service = FlextGrpcClientService()

            target = f"{running_server.host}:{running_server.port}"
            channel = FlextGrpcChannel(
                id=FlextModels.EntityId("test-channel"),
                target=target,
                state="idle",
                created_at=FlextModels.Timestamp(datetime.now(UTC)),
            )

            client = FlextGrpcClient(
                id=FlextModels.EntityId("test-client"),
                channel=channel,
                created_at=FlextModels.Timestamp(datetime.now(UTC)),
            )

            # Connect - should make REAL gRPC connection
            connect_result = client_service.execute("connect", client)
            assert connect_result.success, (
                f"Client connect failed: {connect_result.error}"
            )

            connected_client = connect_result.data
            assert connected_client is not None
            assert connected_client.is_connected

            # Verify real gRPC channel was created
            assert target in client_service._active_channels

            # Get status - should include real channel info
            status_result = client_service.execute("status", connected_client)
            assert status_result.success
            status = status_result.data
            assert isinstance(status, dict)
            assert status["grpc_channel_active"] is True
            assert status["grpc_channel_ready"] is True

            # Add a real service first so we can make calls
            service_def = FlextGrpcService(
                id=FlextModels.EntityId("real-service"),
                name="FlextGrpcService",
                methods=["Echo", "HealthCheck"],
                created_at=FlextModels.Timestamp(datetime.now(UTC)),
            )

            add_result = server_service.execute(
                "add_service", running_server, service_def
            )
            assert add_result.success, f"Service add failed: {add_result.error}"

            # Make call using real Echo method - should validate real channel
            call_result = client_service.execute(
                "call",
                connected_client,
                "Echo",
                {
                    "message": "Test message for real gRPC call",
                    "metadata": {"test": "real", "client": "validation"},
                },
            )
            assert call_result.success, f"Client call failed: {call_result.error}"

            call_response = call_result.data
            assert isinstance(call_response, dict)
            assert call_response["method"] == "Echo"
            assert call_response["status"] == "success"
            assert "Test message for real gRPC call" in call_response["message"]
            assert call_response["channel_ready"] is True
            assert call_response["target"] == target

            # Disconnect - should close REAL gRPC channel
            disconnect_result = client_service.execute("disconnect", connected_client)
            assert disconnect_result.success, (
                f"Client disconnect failed: {disconnect_result.error}"
            )

            disconnected_client = disconnect_result.data
            assert disconnected_client is not None
            assert not disconnected_client.is_connected

            # Verify real channel was removed
            assert target not in client_service._active_channels

        finally:
            # Cleanup: stop the server
            server_service.execute("stop", running_server)

    def test_server_service_handles_multiple_servers(self) -> None:
        """Test that server service can manage multiple real gRPC servers."""
        server_service = FlextGrpcServerService()

        # Start multiple servers on different ports
        server1 = FlextGrpcServer(
            id=FlextModels.EntityId("server-1"),
            host="localhost",
            port=0,  # Auto-assign port
            max_workers=2,
            created_at=FlextModels.Timestamp(datetime.now(UTC)),
        )

        server2 = FlextGrpcServer(
            id=FlextModels.EntityId("server-2"),
            host="localhost",
            port=0,  # Auto-assign port
            max_workers=2,
            created_at=FlextModels.Timestamp(datetime.now(UTC)),
        )

        start1_result = server_service.execute("start", server1)
        assert start1_result.success, (
            f"First server start failed: {start1_result.error}"
        )
        running_server1 = start1_result.data
        assert running_server1 is not None

        start2_result = server_service.execute("start", server2)
        assert start2_result.success, (
            f"Second server start failed: {start2_result.error}"
        )
        running_server2 = start2_result.data
        assert running_server2 is not None

        try:
            # Validate both servers are running on different ports
            assert running_server1.port != running_server2.port, (
                "Servers should use different ports"
            )
            assert running_server1.port > 0
            assert running_server2.port > 0

            # Validate both are tracked in the service
            key1 = f"{running_server1.host}:{running_server1.port}"
            key2 = f"{running_server2.host}:{running_server2.port}"
            assert key1 in server_service._active_servers
            assert key2 in server_service._active_servers

            # Test real connectivity to both servers
            for server, key in [(running_server1, key1), (running_server2, key2)]:
                test_channel = grpc.insecure_channel(f"{server.host}:{server.port}")
                try:
                    grpc.channel_ready_future(test_channel).result(timeout=2.0)
                    connectivity_success = True
                except grpc.FutureTimeoutError:
                    connectivity_success = False
                finally:
                    test_channel.close()

                assert connectivity_success, f"Real gRPC server not accessible at {key}"

        finally:
            # Cleanup both servers
            server_service.execute("stop", running_server1)
            server_service.execute("stop", running_server2)

    def test_client_service_handles_connection_failures(self) -> None:
        """Test that client service handles real connection failures."""
        client_service = FlextGrpcClientService()

        # Try to connect to non-existent server
        target = "localhost:99999"  # Should be unused port
        channel = FlextGrpcChannel(
            id=FlextModels.EntityId("fail-channel"),
            target=target,
            state="idle",
            created_at=FlextModels.Timestamp(datetime.now(UTC)),
        )

        client = FlextGrpcClient(
            id=FlextModels.EntityId("fail-client"),
            channel=channel,
            created_at=FlextModels.Timestamp(datetime.now(UTC)),
        )

        # Connect should fail with real connection error
        connect_result = client_service.execute("connect", client)
        assert connect_result.is_failure
        assert (
            "timeout" in connect_result.error.lower()
            or "connect" in connect_result.error.lower()
        )

        # Verify no channel was created
        assert target not in client_service._active_channels

    def test_service_add_operation_requires_running_server(self) -> None:
        """Test that add_service requires a REAL running gRPC server."""
        server_service = FlextGrpcServerService()

        # Create server but don't start it
        server = FlextGrpcServer(
            id=FlextModels.EntityId("stopped-server"),
            host="localhost",
            port=50123,
            max_workers=2,
            created_at=FlextModels.Timestamp(datetime.now(UTC)),
        )

        service_def = FlextGrpcService(
            id=FlextModels.EntityId("test-service"),
            name="FlextGrpcService",
            methods=["Echo", "HealthCheck"],
            created_at=FlextModels.Timestamp(datetime.now(UTC)),
        )

        # Try to add service to stopped server - should fail
        add_result = server_service.execute("add_service", server, service_def)
        assert add_result.is_failure
        assert "state" in add_result.error.lower()

        # Start server and try again
        start_result = server_service.execute("start", server)
        assert start_result.success
        running_server = start_result.data
        assert running_server is not None

        try:
            # Now add_service should work
            add_result = server_service.execute(
                "add_service", running_server, service_def
            )
            assert add_result.success, f"Add service failed: {add_result.error}"

            server_with_service = add_result.data
            assert server_with_service is not None
            assert len(server_with_service.services) == 1
            assert server_with_service.services[0].name == "FlextGrpcService"

        finally:
            # Cleanup
            server_service.execute("stop", running_server)
