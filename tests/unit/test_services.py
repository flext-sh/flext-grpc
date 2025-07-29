"""Unit tests for FLEXT gRPC services.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from datetime import UTC, datetime

import pytest
from flext_core.utilities import FlextGenerators

from flext_grpc.entities import (
    FlextGrpcChannel,
    FlextGrpcClient,
    FlextGrpcServer,
    FlextGrpcService as FlextGrpcServiceEntity,
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
        assert "Missing operation type" in result.error

    def test_execute_with_unknown_operation_type_fails(self) -> None:
        """Test execute with unknown operation type fails."""
        result = self.service.execute("unknown_type")
        assert result.is_failure
        assert "Unknown operation type: unknown_type" in result.error

    def test_server_start_operation(self) -> None:
        """Test server start operation."""
        result = self.service.execute("server", "start", self.server)
        assert result.is_success
        started_server = result.data
        assert started_server.state == "running"

    def test_server_start_already_running_fails(self) -> None:
        """Test starting already running server fails."""
        running_server = self.server.copy_with(state="running").data
        result = self.service.execute("server", "start", running_server)
        assert result.is_failure
        assert "Server is already running" in result.error

    def test_server_start_invalid_server_fails(self) -> None:
        """Test starting invalid server fails."""
        invalid_server = self.server.copy_with(host="").data
        result = self.service.execute("server", "start", invalid_server)
        assert result.is_failure
        assert "Invalid server" in result.error

    def test_server_stop_operation(self) -> None:
        """Test server stop operation."""
        running_server = self.server.copy_with(state="running").data
        result = self.service.execute("server", "stop", running_server)
        assert result.is_success
        stopped_server = result.data
        assert stopped_server.state == "stopped"

    def test_server_stop_not_running_fails(self) -> None:
        """Test stopping non-running server fails."""
        result = self.service.execute("server", "stop", self.server)
        assert result.is_failure
        assert "Server is not running" in result.error

    def test_server_add_service_operation(self) -> None:
        """Test server add service operation."""
        service_entity = FlextGrpcServiceEntity(
            id=FlextGenerators.generate_entity_id(),
            name="TestService",
            methods=["test_method"],
            created_at=datetime.now(UTC),
        )
        
        result = self.service.execute("server", "add_service", self.server, service=service_entity)
        assert result.is_success
        updated_server = result.data
        assert len(updated_server.services) == 1

    def test_server_add_service_without_service_fails(self) -> None:
        """Test server add service without service fails."""
        result = self.service.execute("server", "add_service", self.server)
        assert result.is_failure
        assert "Service required" in result.error

    def test_server_status_operation(self) -> None:
        """Test server status operation."""
        result = self.service.execute("server", "status", self.server)
        assert result.is_success
        status = result.data
        assert status["address"] == "localhost:50051"
        assert status["state"] == "stopped" 
        assert status["is_running"] is False
        assert status["service_count"] == 0
        assert status["max_workers"] == 10

    def test_server_unknown_operation_fails(self) -> None:
        """Test server unknown operation fails."""
        result = self.service.execute("server", "unknown_op", self.server)
        assert result.is_failure
        assert "Unknown server operation: unknown_op" in result.error

    def test_client_connect_operation(self) -> None:
        """Test client connect operation."""
        result = self.service.execute("client", "connect", self.client)
        assert result.is_success
        connected_client = result.data
        assert connected_client.channel.state == "ready"

    def test_client_connect_already_connected_fails(self) -> None:
        """Test connecting already connected client fails."""
        ready_channel = self.channel.copy_with(state="ready").data
        connected_client = self.client.copy_with(channel=ready_channel).data
        
        result = self.service.execute("client", "connect", connected_client)
        assert result.is_failure
        assert "Client is already connected" in result.error

    def test_client_connect_no_channel_fails(self) -> None:
        """Test connecting client without channel fails."""
        no_channel_client = self.client.copy_with(channel=None).data
        result = self.service.execute("client", "connect", no_channel_client)
        assert result.is_failure
        assert "Client has no channel" in result.error

    def test_client_disconnect_operation(self) -> None:
        """Test client disconnect operation."""
        ready_channel = self.channel.copy_with(state="ready").data
        connected_client = self.client.copy_with(channel=ready_channel).data
        
        result = self.service.execute("client", "disconnect", connected_client)
        assert result.is_success
        disconnected_client = result.data
        assert disconnected_client.channel.state == "idle"

    def test_client_disconnect_not_connected_fails(self) -> None:
        """Test disconnecting non-connected client fails."""
        result = self.service.execute("client", "disconnect", self.client)
        assert result.is_failure
        assert "Client is not connected" in result.error

    def test_client_call_operation(self) -> None:
        """Test client call operation.""" 
        ready_channel = self.channel.copy_with(state="ready").data
        connected_client = self.client.copy_with(channel=ready_channel).data
        
        result = self.service.execute(
            "client", "call", connected_client,
            method_name="test_method",
            request_data={"key": "value"}
        )
        assert result.is_success
        response = result.data
        assert response["status"] == "success"
        assert response["method"] == "test_method"
        assert response["client_id"] == connected_client.id
        assert response["data"] == {"key": "value"}

    def test_client_call_not_connected_fails(self) -> None:
        """Test calling with non-connected client fails."""
        result = self.service.execute(
            "client", "call", self.client,
            method_name="test_method"
        )
        assert result.is_failure
        assert "Client is not connected" in result.error

    def test_client_call_no_method_name_fails(self) -> None:
        """Test calling without method name fails."""
        ready_channel = self.channel.copy_with(state="ready").data
        connected_client = self.client.copy_with(channel=ready_channel).data
        
        result = self.service.execute("client", "call", connected_client)
        assert result.is_failure
        assert "Method name is required" in result.error

    def test_client_status_operation(self) -> None:
        """Test client status operation."""
        result = self.service.execute("client", "status", self.client)
        assert result.is_success
        status = result.data
        assert status["is_connected"] is False
        assert status["channel_target"] == "localhost:50051"
        assert status["channel_state"] == "idle"

    def test_client_unknown_operation_fails(self) -> None:
        """Test client unknown operation fails."""
        result = self.service.execute("client", "unknown_op", self.client)
        assert result.is_failure
        assert "Unknown client operation: unknown_op" in result.error

    def test_stream_create_operation(self) -> None:
        """Test stream create operation."""
        ready_channel = self.channel.copy_with(state="ready").data
        connected_client = self.client.copy_with(channel=ready_channel).data
        
        result = self.service.execute(
            "stream", "create",
            client=connected_client,
            method_name="stream_method",
            stream_type="server_streaming"
        )
        assert result.is_success
        stream = result.data
        assert stream.method_name == "stream_method"
        assert stream.stream_type == "server_streaming"

    def test_stream_create_no_client_fails(self) -> None:
        """Test stream create without client fails."""
        result = self.service.execute("stream", "create", method_name="test")
        assert result.is_failure
        assert "Client required" in result.error

    def test_stream_create_client_not_connected_fails(self) -> None:
        """Test stream create with disconnected client fails."""
        result = self.service.execute(
            "stream", "create",
            client=self.client,
            method_name="test"
        )
        assert result.is_failure
        assert "Client is not connected" in result.error

    def test_stream_create_no_method_name_fails(self) -> None:
        """Test stream create without method name fails."""
        ready_channel = self.channel.copy_with(state="ready").data
        connected_client = self.client.copy_with(channel=ready_channel).data
        
        result = self.service.execute("stream", "create", client=connected_client)
        assert result.is_failure
        assert "Method name is required" in result.error

    def test_stream_send_operation(self) -> None:
        """Test stream send operation."""
        from flext_grpc.entities import FlextGrpcStream
        
        stream = FlextGrpcStream(
            id=FlextGenerators.generate_entity_id(),
            method_name="test_method",
            stream_type="unary",
            created_at=datetime.now(UTC),
        )
        
        result = self.service.execute("stream", "send", stream=stream)
        assert result.is_success
        assert result.data is True

    def test_stream_close_operation(self) -> None:
        """Test stream close operation."""
        from flext_grpc.entities import FlextGrpcStream
        
        stream = FlextGrpcStream(
            id=FlextGenerators.generate_entity_id(),
            method_name="test_method",
            stream_type="unary",
            created_at=datetime.now(UTC),
        )
        
        result = self.service.execute("stream", "close", stream=stream)
        assert result.is_success
        assert result.data is True

    def test_stream_unknown_operation_fails(self) -> None:
        """Test stream unknown operation fails."""
        result = self.service.execute("stream", "unknown_op")
        assert result.is_failure
        assert "Unknown stream operation: unknown_op" in result.error