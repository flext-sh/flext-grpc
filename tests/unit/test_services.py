"""Unit tests for FLEXT gRPC services.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from datetime import UTC, datetime

from flext_core.utilities import FlextGenerators

from flext_grpc.entities import (
    FlextGrpcChannel,
    FlextGrpcClient,
    FlextGrpcServer,
    FlextGrpcService as FlextGrpcServiceEntity,
    FlextGrpcStream,
)
from flext_grpc.services import FlextGrpcService
from flext_grpc.types import TGrpcTarget


class TestFlextGrpcService:
    """Test FlextGrpcService application service."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.service = FlextGrpcService()

        self.server = FlextGrpcServer(
            id=FlextGenerators.generate_entity_id(),
            host="localhost",
            port=50051,
            created_at=datetime.now(UTC),
        )

        self.channel = FlextGrpcChannel(
            id=FlextGenerators.generate_entity_id(),
            target=TGrpcTarget("localhost:50051"),
            state="idle",
            created_at=datetime.now(UTC),
        )

        self.client = FlextGrpcClient(
            id=FlextGenerators.generate_entity_id(),
            channel=self.channel,
            created_at=datetime.now(UTC),
        )

    def test_execute_without_operation_type_fails(self) -> None:
        """Test execute without operation type fails."""
        result = self.service.execute()
        assert result.is_failure
        if "Missing operation type" not in result.error:
            raise AssertionError(
                f"Expected {'Missing operation type'} in {result.error}"
            )

    def test_execute_with_unknown_operation_type_fails(self) -> None:
        """Test execute with unknown operation type fails."""
        result = self.service.execute("unknown_type")
        assert result.is_failure
        if "Unknown operation type: unknown_type" not in result.error:
            raise AssertionError(
                f"Expected {'Unknown operation type: unknown_type'} in {result.error}"
            )

    def test_server_start_operation(self) -> None:
        """Test server start operation."""
        result = self.service.execute("server", "start", self.server)
        assert result.is_success
        started_server = result.data
        if started_server.state != "running":
            raise AssertionError(f"Expected {'running'}, got {started_server.state}")

    def test_server_start_already_running_fails(self) -> None:
        """Test starting already running server fails."""
        running_server = self.server.copy_with(state="running").data
        result = self.service.execute("server", "start", running_server)
        assert result.is_failure
        if "Server is already running" not in result.error:
            raise AssertionError(
                f"Expected {'Server is already running'} in {result.error}"
            )

    def test_server_start_invalid_server_fails(self) -> None:
        """Test starting invalid server fails."""
        invalid_server = self.server.copy_with(host="").data
        result = self.service.execute("server", "start", invalid_server)
        assert result.is_failure
        if "Invalid server" not in result.error:
            raise AssertionError(f"Expected {'Invalid server'} in {result.error}")

    def test_server_stop_operation(self) -> None:
        """Test server stop operation."""
        running_server = self.server.copy_with(state="running").data
        result = self.service.execute("server", "stop", running_server)
        assert result.is_success
        stopped_server = result.data
        if stopped_server.state != "stopped":
            raise AssertionError(f"Expected {'stopped'}, got {stopped_server.state}")

    def test_server_stop_not_running_fails(self) -> None:
        """Test stopping non-running server fails."""
        result = self.service.execute("server", "stop", self.server)
        assert result.is_failure
        if "Server is not running" not in result.error:
            raise AssertionError(
                f"Expected {'Server is not running'} in {result.error}"
            )

    def test_server_add_service_operation(self) -> None:
        """Test server add service operation."""
        service_entity = FlextGrpcServiceEntity(
            id=FlextGenerators.generate_entity_id(),
            name="TestService",
            methods=["test_method"],
            created_at=datetime.now(UTC),
        )

        result = self.service.execute(
            "server", "add_service", self.server, service=service_entity
        )
        assert result.is_success
        updated_server = result.data
        if len(updated_server.services) != 1:
            raise AssertionError(f"Expected {1}, got {len(updated_server.services)}")

    def test_server_add_service_without_service_fails(self) -> None:
        """Test server add service without service fails."""
        result = self.service.execute("server", "add_service", self.server)
        assert result.is_failure
        if "Service required" not in result.error:
            raise AssertionError(f"Expected {'Service required'} in {result.error}")

    def test_server_status_operation(self) -> None:
        """Test server status operation."""
        result = self.service.execute("server", "status", self.server)
        assert result.is_success
        status = result.data
        if status["address"] != "localhost:50051":
            raise AssertionError(
                f"Expected {'localhost:50051'}, got {status['address']}"
            )
        assert status["state"] == "stopped"
        if status["is_running"]:
            raise AssertionError(f"Expected False, got {status['is_running']}")
        assert status["service_count"] == 0
        if status["max_workers"] != 10:
            raise AssertionError(f"Expected {10}, got {status['max_workers']}")

    def test_server_unknown_operation_fails(self) -> None:
        """Test server unknown operation fails."""
        result = self.service.execute("server", "unknown_op", self.server)
        assert result.is_failure
        if "Unknown server operation: unknown_op" not in result.error:
            raise AssertionError(
                f"Expected {'Unknown server operation: unknown_op'} in {result.error}"
            )

    def test_client_connect_operation(self) -> None:
        """Test client connect operation."""
        result = self.service.execute("client", "connect", self.client)
        assert result.is_success
        connected_client = result.data
        if connected_client.channel.state != "ready":
            raise AssertionError(
                f"Expected {'ready'}, got {connected_client.channel.state}"
            )

    def test_client_connect_already_connected_fails(self) -> None:
        """Test connecting already connected client fails."""
        ready_channel = self.channel.copy_with(state="ready").data
        connected_client = self.client.copy_with(channel=ready_channel).data

        result = self.service.execute("client", "connect", connected_client)
        assert result.is_failure
        if "Client is already connected" not in result.error:
            raise AssertionError(
                f"Expected {'Client is already connected'} in {result.error}"
            )

    def test_client_connect_no_channel_fails(self) -> None:
        """Test connecting client without channel fails."""
        no_channel_client = self.client.copy_with(channel=None).data
        result = self.service.execute("client", "connect", no_channel_client)
        assert result.is_failure
        if "Client has no channel" not in result.error:
            raise AssertionError(
                f"Expected {'Client has no channel'} in {result.error}"
            )

    def test_client_disconnect_operation(self) -> None:
        """Test client disconnect operation."""
        ready_channel = self.channel.copy_with(state="ready").data
        connected_client = self.client.copy_with(channel=ready_channel).data

        result = self.service.execute("client", "disconnect", connected_client)
        assert result.is_success
        disconnected_client = result.data
        if disconnected_client.channel.state != "idle":
            raise AssertionError(
                f"Expected {'idle'}, got {disconnected_client.channel.state}"
            )

    def test_client_disconnect_not_connected_fails(self) -> None:
        """Test disconnecting non-connected client fails."""
        result = self.service.execute("client", "disconnect", self.client)
        assert result.is_failure
        if "Client is not connected" not in result.error:
            raise AssertionError(
                f"Expected {'Client is not connected'} in {result.error}"
            )

    def test_client_call_operation(self) -> None:
        """Test client call operation."""
        ready_channel = self.channel.copy_with(state="ready").data
        connected_client = self.client.copy_with(channel=ready_channel).data

        result = self.service.execute(
            "client",
            "call",
            connected_client,
            method_name="test_method",
            request_data={"key": "value"},
        )
        assert result.is_success
        response = result.data
        if response["status"] != "success":
            raise AssertionError(f"Expected {'success'}, got {response['status']}")
        assert response["method"] == "test_method"
        if response["client_id"] != connected_client.id:
            raise AssertionError(
                f"Expected {connected_client.id}, got {response['client_id']}"
            )
        assert response["data"] == {"key": "value"}

    def test_client_call_not_connected_fails(self) -> None:
        """Test calling with non-connected client fails."""
        result = self.service.execute(
            "client",
            "call",
            self.client,
            method_name="test_method",
        )
        assert result.is_failure
        if "Client is not connected" not in result.error:
            raise AssertionError(
                f"Expected {'Client is not connected'} in {result.error}"
            )

    def test_client_call_no_method_name_fails(self) -> None:
        """Test calling without method name fails."""
        ready_channel = self.channel.copy_with(state="ready").data
        connected_client = self.client.copy_with(channel=ready_channel).data

        result = self.service.execute("client", "call", connected_client)
        assert result.is_failure
        if "Method name is required" not in result.error:
            raise AssertionError(
                f"Expected {'Method name is required'} in {result.error}"
            )

    def test_client_status_operation(self) -> None:
        """Test client status operation."""
        result = self.service.execute("client", "status", self.client)
        assert result.is_success
        status = result.data
        if status["is_connected"]:
            raise AssertionError(f"Expected False, got {status['is_connected']}")
        assert status["channel_target"] == "localhost:50051"
        if status["channel_state"] != "idle":
            raise AssertionError(f"Expected {'idle'}, got {status['channel_state']}")

    def test_client_unknown_operation_fails(self) -> None:
        """Test client unknown operation fails."""
        result = self.service.execute("client", "unknown_op", self.client)
        assert result.is_failure
        if "Unknown client operation: unknown_op" not in result.error:
            raise AssertionError(
                f"Expected {'Unknown client operation: unknown_op'} in {result.error}"
            )

    def test_stream_create_operation(self) -> None:
        """Test stream create operation."""
        ready_channel = self.channel.copy_with(state="ready").data
        connected_client = self.client.copy_with(channel=ready_channel).data

        result = self.service.execute(
            "stream",
            "create",
            client=connected_client,
            method_name="stream_method",
            stream_type="server_streaming",
        )
        assert result.is_success
        stream = result.data
        if stream.method_name != "stream_method":
            raise AssertionError(
                f"Expected {'stream_method'}, got {stream.method_name}"
            )
        assert stream.stream_type == "server_streaming"

    def test_stream_create_no_client_fails(self) -> None:
        """Test stream create without client fails."""
        result = self.service.execute("stream", "create", method_name="test")
        assert result.is_failure
        if "Client required" not in result.error:
            raise AssertionError(f"Expected {'Client required'} in {result.error}")

    def test_stream_create_client_not_connected_fails(self) -> None:
        """Test stream create with disconnected client fails."""
        result = self.service.execute(
            "stream",
            "create",
            client=self.client,
            method_name="test",
        )
        assert result.is_failure
        if "Client is not connected" not in result.error:
            raise AssertionError(
                f"Expected {'Client is not connected'} in {result.error}"
            )

    def test_stream_create_no_method_name_fails(self) -> None:
        """Test stream create without method name fails."""
        ready_channel = self.channel.copy_with(state="ready").data
        connected_client = self.client.copy_with(channel=ready_channel).data

        result = self.service.execute("stream", "create", client=connected_client)
        assert result.is_failure
        if "Method name is required" not in result.error:
            raise AssertionError(
                f"Expected {'Method name is required'} in {result.error}"
            )

    def test_stream_send_operation(self) -> None:
        """Test stream send operation."""

        stream = FlextGrpcStream(
            id=FlextGenerators.generate_entity_id(),
            method_name="test_method",
            stream_type="unary",
            created_at=datetime.now(UTC),
        )

        result = self.service.execute("stream", "send", stream=stream)
        assert result.is_success
        if not (result.data):
            raise AssertionError(f"Expected True, got {result.data}")

    def test_stream_close_operation(self) -> None:
        """Test stream close operation."""

        stream = FlextGrpcStream(
            id=FlextGenerators.generate_entity_id(),
            method_name="test_method",
            stream_type="unary",
            created_at=datetime.now(UTC),
        )

        result = self.service.execute("stream", "close", stream=stream)
        assert result.is_success
        if not (result.data):
            raise AssertionError(f"Expected True, got {result.data}")

    def test_stream_unknown_operation_fails(self) -> None:
        """Test stream unknown operation fails."""
        result = self.service.execute("stream", "unknown_op")
        assert result.is_failure
        if "Unknown stream operation: unknown_op" not in result.error:
            raise AssertionError(
                f"Expected {'Unknown stream operation: unknown_op'} in {result.error}"
            )
