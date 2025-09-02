"""FLEXT gRPC Complete REAL Implementation Tests.

This module validates 100% REAL gRPC functionality:
- Real protocol buffer calls
- Real service registration
- Real streaming operations
- Real error handling

NO SIMULATIONS - Everything is actual gRPC communication.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from datetime import UTC, datetime

import grpc
from flext_core import FlextModels

from flext_grpc import (
    FlextGrpcChannel,
    FlextGrpcClient,
    FlextGrpcServer,
    FlextGrpcService,
    FlextGrpcStream,
)
from flext_grpc.proto import (
    EchoRequest,
    FlextGrpcServiceStub,
)
from flext_grpc.services import (
    FlextGrpcClientService,
    FlextGrpcServerService,
    FlextGrpcStreamService,
)


class TestCompleteRealGrpc:
    """Test 100% REAL gRPC implementation - no simulations."""

    def test_complete_real_grpc_workflow(self) -> None:
        """Test complete REAL gRPC workflow: server + service + client + calls."""
        server_service = FlextGrpcServerService()

        # 1. Start REAL gRPC server
        server = FlextGrpcServer(
            id=FlextModels("complete-real-server"),
            host="localhost",
            port=0,  # Auto-assign
            max_workers=2,
            created_at=FlextModels(datetime.now(UTC)),
        )

        start_result = server_service.execute("start", server)
        assert start_result.success, f"Server start failed: {start_result.error}"
        running_server = start_result.data
        assert running_server is not None

        try:
            # 2. Add REAL gRPC service to server
            service_def = FlextGrpcService(
                id=FlextModels("real-grpc-service"),
                name="FlextGrpcService",
                methods=["Echo", "HealthCheck"],
                created_at=FlextModels(datetime.now(UTC)),
            )

            add_result = server_service.execute(
                "add_service", running_server, service_def
            )
            assert add_result.success, f"Service add failed: {add_result.error}"
            server_with_service = add_result.data
            assert server_with_service is not None
            assert len(server_with_service.services) == 1

            # 3. Create REAL gRPC client
            client_service = FlextGrpcClientService()

            target = f"{running_server.host}:{running_server.port}"
            channel = FlextGrpcChannel(
                id=FlextModels("real-client-channel"),
                target=target,
                state="idle",
                created_at=FlextModels(datetime.now(UTC)),
            )

            client = FlextGrpcClient(
                id=FlextModels("real-grpc-client"),
                channel=channel,
                created_at=FlextModels(datetime.now(UTC)),
            )

            # 4. Connect client to REAL server
            connect_result = client_service.execute("connect", client)
            assert connect_result.success, (
                f"Client connect failed: {connect_result.error}"
            )
            connected_client = connect_result.data
            assert connected_client is not None
            assert connected_client.is_connected

            # 5. Make REAL gRPC Echo call
            echo_result = client_service.execute(
                "call",
                connected_client,
                "Echo",
                {
                    "message": "Real gRPC test message",
                    "metadata": {"test": "real", "client": "flext"},
                },
            )
            assert echo_result.success, f"Echo call failed: {echo_result.error}"

            echo_response = echo_result.data
            assert isinstance(echo_response, dict)
            assert echo_response["method"] == "Echo"
            assert echo_response["status"] == "success"
            assert "Real gRPC test message" in echo_response["message"]
            assert "server_id" in echo_response
            assert "timestamp" in echo_response

            # 6. Make REAL gRPC HealthCheck call
            health_result = client_service.execute(
                "call", connected_client, "HealthCheck", {}
            )
            assert health_result.success, f"Health check failed: {health_result.error}"

            health_response = health_result.data
            assert isinstance(health_response, dict)
            assert health_response["method"] == "HealthCheck"
            assert health_response["status"] == "success"
            assert "serving_status" in health_response

            # 7. Disconnect client
            disconnect_result = client_service.execute("disconnect", connected_client)
            assert disconnect_result.success, (
                f"Disconnect failed: {disconnect_result.error}"
            )

        finally:
            # Cleanup
            server_service.execute("stop", running_server)

    def test_real_grpc_streaming_operations(self) -> None:
        """Test REAL gRPC streaming operations."""
        server_service = FlextGrpcServerService()

        # Start server with service
        server = FlextGrpcServer(
            id=FlextModels("streaming-server"),
            host="localhost",
            port=0,
            max_workers=2,
            created_at=FlextModels(datetime.now(UTC)),
        )

        start_result = server_service.execute("start", server)
        assert start_result.success
        running_server = start_result.data
        assert running_server is not None

        try:
            # Add service
            service_def = FlextGrpcService(
                id=FlextModels("streaming-service"),
                name="FlextGrpcService",
                methods=["ServerStream", "ClientStream", "BidirectionalStream"],
                created_at=FlextModels(datetime.now(UTC)),
            )

            add_result = server_service.execute(
                "add_service", running_server, service_def
            )
            assert add_result.success

            # Test streaming service
            stream_service = FlextGrpcStreamService()
            target = f"{running_server.host}:{running_server.port}"

            # Test server streaming
            server_stream = FlextGrpcStream(
                id=FlextModels("server-stream-test"),
                method_name="ServerStream",
                stream_type="server_streaming",
                created_at=FlextModels(datetime.now(UTC)),
            )

            create_result = stream_service.execute("create", server_stream, target)
            assert create_result.success, f"Stream create failed: {create_result.error}"

            # Send data through REAL server stream
            send_result = stream_service.execute(
                "send", server_stream, "Real streaming data"
            )
            assert send_result.success, f"Stream send failed: {send_result.error}"

            stream_response = send_result.data
            assert isinstance(stream_response, dict)
            assert stream_response["stream_type"] == "server_streaming"
            assert "responses" in stream_response
            assert stream_response["response_count"] > 0

            # Test client streaming
            client_stream = FlextGrpcStream(
                id=FlextModels("client-stream-test"),
                method_name="ClientStream",
                stream_type="client_streaming",
                created_at=FlextModels(datetime.now(UTC)),
            )

            create_result = stream_service.execute("create", client_stream, target)
            assert create_result.success

            # Send first request - should be buffered
            send_result = stream_service.execute(
                "send", client_stream, "Client stream data 1"
            )
            assert send_result.success

            client_response = send_result.data
            assert isinstance(client_response, dict)
            assert client_response["stream_type"] == "client_streaming"
            assert client_response["buffer_status"] == "buffered"

            # Send more requests to trigger buffer flush
            stream_service.execute("send", client_stream, "Client stream data 2")
            send_result = stream_service.execute(
                "send", client_stream, "Client stream data 3"
            )
            assert send_result.success

            # Now should have response since buffer threshold reached
            client_response = send_result.data
            assert isinstance(client_response, dict)
            assert client_response["stream_type"] == "client_streaming"
            assert "response" in client_response

            # Test bidirectional streaming
            bidirectional_stream = FlextGrpcStream(
                id=FlextModels("bidirectional-stream-test"),
                method_name="BidirectionalStream",
                stream_type="bidirectional",
                created_at=FlextModels(datetime.now(UTC)),
            )

            create_result = stream_service.execute(
                "create", bidirectional_stream, target
            )
            assert create_result.success

            send_result = stream_service.execute(
                "send", bidirectional_stream, "Bidirectional data"
            )
            assert send_result.success

            bidir_response = send_result.data
            assert isinstance(bidir_response, dict)
            assert bidir_response["stream_type"] == "bidirectional"
            assert "responses" in bidir_response

            # Close streams
            stream_service.execute("close", server_stream)
            stream_service.execute("close", client_stream)
            stream_service.execute("close", bidirectional_stream)

        finally:
            server_service.execute("stop", running_server)

    def test_real_grpc_error_handling(self) -> None:
        """Test REAL gRPC error handling with actual gRPC errors."""
        client_service = FlextGrpcClientService()

        # Try to connect to non-existent server
        channel = FlextGrpcChannel(
            id=FlextModels("error-channel"),
            target="localhost:99999",  # Should fail
            state="idle",
            created_at=FlextModels(datetime.now(UTC)),
        )

        client = FlextGrpcClient(
            id=FlextModels("error-client"),
            channel=channel,
            created_at=FlextModels(datetime.now(UTC)),
        )

        # Connection should fail with REAL gRPC error
        connect_result = client_service.execute("connect", client)
        assert connect_result.is_failure
        assert (
            "timeout" in connect_result.error.lower()
            or "connect" in connect_result.error.lower()
        )

    def test_real_grpc_concurrent_clients(self) -> None:
        """Test multiple REAL gRPC clients concurrently."""
        server_service = FlextGrpcServerService()

        # Start server
        server = FlextGrpcServer(
            id=FlextModels("concurrent-server"),
            host="localhost",
            port=0,
            max_workers=5,  # Support multiple clients
            created_at=FlextModels(datetime.now(UTC)),
        )

        start_result = server_service.execute("start", server)
        assert start_result.success
        running_server = start_result.data
        assert running_server is not None

        try:
            # Add service
            service_def = FlextGrpcService(
                id=FlextModels("concurrent-service"),
                name="FlextGrpcService",
                methods=["Echo"],
                created_at=FlextModels(datetime.now(UTC)),
            )

            add_result = server_service.execute(
                "add_service", running_server, service_def
            )
            assert add_result.success

            # Create multiple clients
            target = f"{running_server.host}:{running_server.port}"
            client_service = FlextGrpcClientService()

            clients = []
            for i in range(3):
                channel = FlextGrpcChannel(
                    id=FlextModels(f"concurrent-channel-{i}"),
                    target=target,
                    state="idle",
                    created_at=FlextModels(datetime.now(UTC)),
                )

                client = FlextGrpcClient(
                    id=FlextModels(f"concurrent-client-{i}"),
                    channel=channel,
                    created_at=FlextModels(datetime.now(UTC)),
                )

                connect_result = client_service.execute("connect", client)
                assert connect_result.success
                clients.append(connect_result.data)

            # Make concurrent calls
            for i, client in enumerate(clients):
                call_result = client_service.execute(
                    "call",
                    client,
                    "Echo",
                    {
                        "message": f"Concurrent message {i}",
                        "metadata": {"client_id": str(i)},
                    },
                )
                assert call_result.success, (
                    f"Client {i} call failed: {call_result.error}"
                )

                response = call_result.data
                assert isinstance(response, dict)
                assert f"Concurrent message {i}" in response["message"]

            # Disconnect all clients
            for client in clients:
                disconnect_result = client_service.execute("disconnect", client)
                assert disconnect_result.success

        finally:
            server_service.execute("stop", running_server)

    def test_real_protocol_buffer_direct_usage(self) -> None:
        """Test direct usage of protocol buffers with REAL gRPC calls."""
        server_service = FlextGrpcServerService()

        # Start server
        server = FlextGrpcServer(
            id=FlextModels("pb-direct-server"),
            host="localhost",
            port=0,
            max_workers=2,
            created_at=FlextModels(datetime.now(UTC)),
        )

        start_result = server_service.execute("start", server)
        assert start_result.success
        running_server = start_result.data
        assert running_server is not None

        try:
            # Add service
            service_def = FlextGrpcService(
                id=FlextModels("pb-service"),
                name="FlextGrpcService",
                methods=["Echo"],
                created_at=FlextModels(datetime.now(UTC)),
            )

            add_result = server_service.execute(
                "add_service", running_server, service_def
            )
            assert add_result.success

            # Make direct gRPC call using protocol buffers
            target = f"{running_server.host}:{running_server.port}"
            channel = grpc.insecure_channel(target)

            try:
                # Wait for channel to be ready
                grpc.channel_ready_future(channel).result(timeout=5.0)

                # Create stub and make REAL protocol buffer call
                stub = FlextGrpcServiceStub(channel)

                # Create real protocol buffer request
                request = EchoRequest(
                    message="Direct protocol buffer call",
                    metadata={"type": "direct", "test": "pb"},
                )

                # Make REAL gRPC call
                response = stub.Echo(request, timeout=10.0)

                # Validate REAL protocol buffer response
                assert response.message.startswith(
                    "Echo: Direct protocol buffer call (metadata:"
                )
                assert "type=direct" in response.message
                assert "test=pb" in response.message
                assert response.server_id.startswith("localhost:")
                assert response.timestamp > 0

            finally:
                channel.close()

        finally:
            server_service.execute("stop", running_server)
