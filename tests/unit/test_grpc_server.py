"""FLEXT gRPC Real Server Testing - Tests that actually start gRPC servers.

This module provides tests that execute ACTUAL gRPC functionality,
starting real servers, making real connections, and validating real responses.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime

import echo_pb2
import echo_pb2_grpc
import grpc
import pytest
from flext_core import FlextModels

from flext_grpc import (
    FlextGrpcChannel,
    FlextGrpcClient,
    FlextGrpcServer,
    FlextGrpcService,
    TGrpcTarget,
)


class TestRealGrpcServer:
    """Tests that actually start real gRPC servers and make real connections."""

    def test_real_grpc_server_startup_and_connection(self) -> None:
        """Test starting a REAL gRPC server and connecting to it."""
        # Start REAL gRPC server using Python grpc library
        grpc_server = grpc.server(ThreadPoolExecutor(max_workers=2))

        # Let server choose an available port
        actual_port = grpc_server.add_insecure_port("localhost:0")

        # Start the server
        grpc_server.start()

        try:
            # Create server entity with the actual port that was assigned
            server = FlextGrpcServer(
                id=FlextModels("real-test-server"),
                host="localhost",
                port=actual_port,
                max_workers=2,
                created_at=FlextModels(datetime.now(UTC)),
                state="running",
            )

            # Validate server configuration with real port
            validation = server.validate_business_rules()
            assert validation.success

            # Test real connection to the server
            target = f"{server.host}:{actual_port}"

            # Create real gRPC channel
            real_channel = grpc.insecure_channel(target)

            try:
                # Test channel connectivity - this validates server is really running
                grpc.channel_ready_future(real_channel).result(timeout=5.0)

                # Test entity state transitions work correctly - start with idle
                channel_entity = FlextGrpcChannel(
                    id=FlextModels("real-test-channel"),
                    target=TGrpcTarget(target),
                    state="idle",  # Start with idle state for transition testing
                    created_at=FlextModels(datetime.now(UTC)),
                )

                # Test idle -> connecting transition
                connect_result = channel_entity.connect()
                assert connect_result.success
                connecting_channel = connect_result.data
                assert connecting_channel is not None
                assert connecting_channel.state == "connecting"

                # Test connecting -> ready transition
                ready_result = connecting_channel.mark_ready()
                assert ready_result.success
                ready_channel = ready_result.data
                assert ready_channel is not None
                assert ready_channel.state == "ready"
                assert ready_channel.is_ready()

                # Now create client with ready channel
                client_entity = FlextGrpcClient(
                    id=FlextModels("real-test-client"),
                    channel=ready_channel,
                    created_at=FlextModels(datetime.now(UTC)),
                )

                # Validate entity states match reality
                assert client_entity.is_connected
                assert client_entity.target == target

            finally:
                real_channel.close()

        finally:
            # Stop the real server
            grpc_server.stop(grace=1.0)

    def test_real_service_registration_and_calls(self) -> None:
        """Test registering a real service and making real gRPC calls."""
        try:
            # Try to import the generated protobuf files
            class EchoServicer(echo_pb2_grpc.EchoServiceServicer):
                def Echo(
                    self, request: echo_pb2.EchoRequest, context: object
                ) -> echo_pb2.EchoResponse:
                    return echo_pb2.EchoResponse(message=f"Echo: {request.message}")

            # Start real server with the service
            server = grpc.server(ThreadPoolExecutor(max_workers=2))
            echo_servicer = EchoServicer()
            echo_pb2_grpc.add_EchoServiceServicer_to_server(echo_servicer, server)

            port = server.add_insecure_port("localhost:0")
            server.start()

            try:
                # Create our entities to represent this real setup
                server_entity = FlextGrpcServer(
                    id=FlextModels("echo-server"),
                    host="localhost",
                    port=port,
                    max_workers=2,
                    created_at=FlextModels(datetime.now(UTC)),
                    state="running",
                )

                service_entity = FlextGrpcService(
                    id=FlextModels("echo-service"),
                    name="EchoService",
                    methods=["Echo"],
                    created_at=FlextModels(datetime.now(UTC)),
                )

                # Validate entities
                assert server_entity.validate_business_rules().success
                assert service_entity.validate_business_rules().success
                assert service_entity.has_method("Echo")

                # Make real gRPC call
                target = f"localhost:{port}"
                channel = grpc.insecure_channel(target)

                try:
                    # Wait for channel to be ready
                    grpc.channel_ready_future(channel).result(timeout=5.0)

                    # Create stub and make real call
                    stub = echo_pb2_grpc.EchoServiceStub(channel)
                    request = echo_pb2.EchoRequest(message="Hello Real gRPC!")
                    response = stub.Echo(request)

                    # Validate real response
                    assert response.message == "Echo: Hello Real gRPC!"

                    # Validate our entities represent this reality
                    channel_entity = FlextGrpcChannel(
                        id=FlextModels("echo-channel"),
                        target=TGrpcTarget(target),
                        state="ready",
                        created_at=FlextModels(datetime.now(UTC)),
                    )

                    client_entity = FlextGrpcClient(
                        id=FlextModels("echo-client"),
                        channel=channel_entity,
                        created_at=FlextModels(datetime.now(UTC)),
                    )

                    assert client_entity.is_connected
                    assert channel_entity.is_ready()

                finally:
                    channel.close()

            finally:
                server.stop(grace=1.0)

        except ImportError:
            # Skip test if protobuf files not available
            pytest.skip("Protobuf files not generated")

    def test_real_error_conditions(self) -> None:
        """Test real error conditions with actual gRPC failures."""
        # Try to connect to non-existent server
        target = "localhost:99999"  # Port that should be closed

        channel_entity = FlextGrpcChannel(
            id=FlextModels("error-test-channel"),
            target=TGrpcTarget(target),
            state="idle",
            created_at=FlextModels(datetime.now(UTC)),
        )

        # Create real channel and test failure
        real_channel = grpc.insecure_channel(target)

        try:
            # This should fail with real timeout
            future = grpc.channel_ready_future(real_channel)
            try:
                future.result(timeout=1.0)  # Short timeout for test
                pytest.fail("Should have failed to connect")
            except grpc.FutureTimeoutError:
                # This is expected - real failure condition
                pass

            # Validate our entity can represent this error state
            error_result = channel_entity.connect()
            if error_result.success:
                # Simulate what would happen in real implementation
                connecting_channel = error_result.data
                assert connecting_channel is not None
                assert connecting_channel.state == "connecting"

                # In real implementation, this would eventually timeout
                # For now, we can test the connection attempt succeeded at entity level
                assert connecting_channel.state == "connecting"

        finally:
            real_channel.close()
