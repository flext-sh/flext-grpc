"""Additional tests for flext_grpc.entities module.

Tests additional functionality to improve coverage.
"""

from __future__ import annotations

from datetime import UTC, datetime
from unittest.mock import MagicMock

import pytest

from flext_grpc.entities import (
    FlextGrpcChannel,
    FlextGrpcClient,
    FlextGrpcEntity,
    FlextGrpcServer,
    FlextGrpcStream,
)


class TestFlextGrpcEntitiesAdditional:
    """Additional tests for FlextGrpc entities to improve coverage."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.now = datetime.now(UTC)

    def test_flext_grpc_entity_creation(self) -> None:
        """Test FlextGrpcEntity creation."""
        entity = FlextGrpcEntity(
            id="test-entity",
            created_at=self.now,
            updated_at=self.now,
        )

        assert entity.id == "test-entity"
        assert entity.created_at == self.now
        assert entity.updated_at == self.now

    def test_flext_grpc_channel_creation_with_defaults(self) -> None:
        """Test FlextGrpcChannel creation with default values."""
        channel = FlextGrpcChannel(
            id="test-channel",
            target="localhost:50051",
            created_at=self.now,
        )

        assert channel.id == "test-channel"
        assert channel.target == "localhost:50051"
        assert channel.state == "disconnected"
        assert channel.grpc_channel is None
        assert channel.created_at == self.now

    def test_flext_grpc_channel_creation_with_custom_values(self) -> None:
        """Test FlextGrpcChannel creation with custom values."""
        mock_channel = MagicMock()
        channel = FlextGrpcChannel(
            id="test-channel",
            target="localhost:50051",
            state="connected",
            grpc_channel=mock_channel,
            created_at=self.now,
        )

        assert channel.id == "test-channel"
        assert channel.target == "localhost:50051"
        assert channel.state == "connected"
        assert channel.grpc_channel == mock_channel
        assert channel.created_at == self.now

    def test_flext_grpc_channel_with_invalid_state(self) -> None:
        """Test FlextGrpcChannel with invalid state."""
        with pytest.raises(ValueError, match="Invalid channel state"):
            FlextGrpcChannel(
                id="test-channel",
                target="localhost:50051",
                state="invalid_state",
                created_at=self.now,
            )

    def test_flext_grpc_server_creation_with_defaults(self) -> None:
        """Test FlextGrpcServer creation with default values."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        assert server.id == "test-server"
        assert server.host == "localhost"
        assert server.port == 50051
        assert server.max_workers == 10
        assert server.state == "stopped"
        assert server.services == []
        assert server.grpc_server is None
        assert server.created_at == self.now

    def test_flext_grpc_server_creation_with_custom_values(self) -> None:
        """Test FlextGrpcServer creation with custom values."""
        mock_server = MagicMock()
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            max_workers=20,
            state="running",
            services=["TestService"],
            grpc_server=mock_server,
            created_at=self.now,
        )

        assert server.id == "test-server"
        assert server.host == "localhost"
        assert server.port == 50051
        assert server.max_workers == 20
        assert server.state == "running"
        assert server.services == ["TestService"]
        assert server.grpc_server == mock_server
        assert server.created_at == self.now

    def test_flext_grpc_client_creation_with_defaults(self) -> None:
        """Test FlextGrpcClient creation with default values."""
        client = FlextGrpcClient(
            id="test-client",
            target="localhost:50051",
            created_at=self.now,
        )

        assert client.id == "test-client"
        assert client.target == "localhost:50051"
        assert client.channel is None
        assert client.grpc_stub is None
        assert client.created_at == self.now

    def test_flext_grpc_client_creation_with_custom_values(self) -> None:
        """Test FlextGrpcClient creation with custom values."""
        mock_channel = MagicMock()
        mock_stub = MagicMock()
        client = FlextGrpcClient(
            id="test-client",
            target="localhost:50051",
            channel=mock_channel,
            grpc_stub=mock_stub,
            created_at=self.now,
        )

        assert client.id == "test-client"
        assert client.target == "localhost:50051"
        assert client.channel == mock_channel
        assert client.grpc_stub == mock_stub
        assert client.created_at == self.now

    def test_flext_grpc_stream_creation_with_defaults(self) -> None:
        """Test FlextGrpcStream creation with default values."""
        stream = FlextGrpcStream(
            id="test-stream",
            method_name="TestMethod",
            stream_type="unary",
            created_at=self.now,
        )

        assert stream.id == "test-stream"
        assert stream.method_name == "TestMethod"
        assert stream.stream_type == "unary"
        assert stream.grpc_stub is None
        assert stream.created_at == self.now

    def test_flext_grpc_stream_creation_with_custom_values(self) -> None:
        """Test FlextGrpcStream creation with custom values."""
        mock_stub = MagicMock()
        stream = FlextGrpcStream(
            id="test-stream",
            method_name="TestMethod",
            stream_type="server_streaming",
            grpc_stub=mock_stub,
            created_at=self.now,
        )

        assert stream.id == "test-stream"
        assert stream.method_name == "TestMethod"
        assert stream.stream_type == "server_streaming"
        assert stream.grpc_stub == mock_stub
        assert stream.created_at == self.now

    def test_flext_grpc_stream_with_invalid_method_name(self) -> None:
        """Test FlextGrpcStream with invalid method name."""
        with pytest.raises(ValueError, match="Method name cannot be empty"):
            FlextGrpcStream(
                id="test-stream",
                method_name="",
                stream_type="unary",
                created_at=self.now,
            )

    def test_flext_grpc_stream_with_whitespace_method_name(self) -> None:
        """Test FlextGrpcStream with whitespace-only method name."""
        with pytest.raises(ValueError, match="Method name cannot be empty"):
            FlextGrpcStream(
                id="test-stream",
                method_name="   ",
                stream_type="unary",
                created_at=self.now,
            )

    def test_flext_grpc_stream_with_invalid_stream_type(self) -> None:
        """Test FlextGrpcStream with invalid stream type."""
        with pytest.raises(ValueError, match="Invalid stream type"):
            FlextGrpcStream(
                id="test-stream",
                method_name="TestMethod",
                stream_type="invalid_type",
                created_at=self.now,
            )

    def test_flext_grpc_stream_properties_unary(self) -> None:
        """Test FlextGrpcStream properties for unary stream."""
        stream = FlextGrpcStream(
            id="test-stream",
            method_name="TestMethod",
            stream_type="unary",
            created_at=self.now,
        )

        assert not stream.is_server_streaming
        assert not stream.is_client_streaming
        assert not stream.is_bidirectional

    def test_flext_grpc_stream_properties_server_streaming(self) -> None:
        """Test FlextGrpcStream properties for server streaming."""
        stream = FlextGrpcStream(
            id="test-stream",
            method_name="TestMethod",
            stream_type="server_streaming",
            created_at=self.now,
        )

        assert stream.is_server_streaming
        assert not stream.is_client_streaming
        assert not stream.is_bidirectional

    def test_flext_grpc_stream_properties_client_streaming(self) -> None:
        """Test FlextGrpcStream properties for client streaming."""
        stream = FlextGrpcStream(
            id="test-stream",
            method_name="TestMethod",
            stream_type="client_streaming",
            created_at=self.now,
        )

        assert not stream.is_server_streaming
        assert stream.is_client_streaming
        assert not stream.is_bidirectional

    def test_flext_grpc_stream_properties_bidirectional(self) -> None:
        """Test FlextGrpcStream properties for bidirectional streaming."""
        stream = FlextGrpcStream(
            id="test-stream",
            method_name="TestMethod",
            stream_type="bidirectional",
            created_at=self.now,
        )

        assert not stream.is_server_streaming
        assert not stream.is_client_streaming
        assert stream.is_bidirectional

    def test_flext_grpc_stream_model_copy(self) -> None:
        """Test FlextGrpcStream model_copy method."""
        stream = FlextGrpcStream(
            id="test-stream",
            method_name="TestMethod",
            stream_type="unary",
            created_at=self.now,
        )

        updated_stream = stream.model_copy(update={"method_name": "UpdatedMethod"})

        assert updated_stream.id == "test-stream"
        assert updated_stream.method_name == "UpdatedMethod"
        assert updated_stream.stream_type == "unary"
        assert updated_stream.created_at == self.now

    def test_flext_grpc_channel_model_copy(self) -> None:
        """Test FlextGrpcChannel model_copy method."""
        channel = FlextGrpcChannel(
            id="test-channel",
            target="localhost:50051",
            created_at=self.now,
        )

        updated_channel = channel.model_copy(update={"state": "connected"})

        assert updated_channel.id == "test-channel"
        assert updated_channel.target == "localhost:50051"
        assert updated_channel.state == "connected"
        assert updated_channel.created_at == self.now

    def test_flext_grpc_server_model_copy(self) -> None:
        """Test FlextGrpcServer model_copy method."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        updated_server = server.model_copy(update={"max_workers": 20})

        assert updated_server.id == "test-server"
        assert updated_server.host == "localhost"
        assert updated_server.port == 50051
        assert updated_server.max_workers == 20
        assert updated_server.created_at == self.now

    def test_flext_grpc_client_model_copy(self) -> None:
        """Test FlextGrpcClient model_copy method."""
        client = FlextGrpcClient(
            id="test-client",
            target="localhost:50051",
            created_at=self.now,
        )

        updated_client = client.model_copy(update={"target": "localhost:8080"})

        assert updated_client.id == "test-client"
        assert updated_client.target == "localhost:8080"
        assert updated_client.created_at == self.now

    def test_flext_grpc_entity_model_copy(self) -> None:
        """Test FlextGrpcEntity model_copy method."""
        entity = FlextGrpcEntity(
            id="test-entity",
            created_at=self.now,
            updated_at=self.now,
        )

        updated_entity = entity.model_copy(update={"id": "updated-entity"})

        assert updated_entity.id == "updated-entity"
        assert updated_entity.created_at == self.now
        assert updated_entity.updated_at == self.now

    def test_flext_grpc_stream_all_valid_stream_types(self) -> None:
        """Test FlextGrpcStream with all valid stream types."""
        valid_types = ["unary", "server_streaming", "client_streaming", "bidirectional"]

        for stream_type in valid_types:
            stream = FlextGrpcStream(
                id=f"test-stream-{stream_type}",
                method_name="TestMethod",
                stream_type=stream_type,
                created_at=self.now,
            )

            assert stream.stream_type == stream_type

    def test_flext_grpc_channel_all_valid_states(self) -> None:
        """Test FlextGrpcChannel with all valid states."""
        valid_states = ["disconnected", "connecting", "connected", "disconnecting"]

        for state in valid_states:
            channel = FlextGrpcChannel(
                id=f"test-channel-{state}",
                target="localhost:50051",
                state=state,
                created_at=self.now,
            )

            assert channel.state == state

    def test_flext_grpc_server_edge_case_ports(self) -> None:
        """Test FlextGrpcServer with edge case ports."""
        # Test with minimum valid port
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=1024,
            created_at=self.now,
        )
        assert server.port == 1024

        # Test with maximum valid port
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=65535,
            created_at=self.now,
        )
        assert server.port == 65535

    def test_flext_grpc_server_edge_case_max_workers(self) -> None:
        """Test FlextGrpcServer with edge case max_workers."""
        # Test with minimum valid max_workers
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            max_workers=1,
            created_at=self.now,
        )
        assert server.max_workers == 1

        # Test with high max_workers
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            max_workers=100,
            created_at=self.now,
        )
        assert server.max_workers == 100

    def test_flext_grpc_stream_with_method_name_trimming(self) -> None:
        """Test FlextGrpcStream with method name trimming."""
        stream = FlextGrpcStream(
            id="test-stream",
            method_name="  TestMethod  ",
            stream_type="unary",
            created_at=self.now,
        )

        assert stream.method_name == "TestMethod"  # Should be trimmed

    def test_flext_grpc_entity_inheritance(self) -> None:
        """Test that all entities properly inherit from FlextGrpcEntity."""
        entities = [
            FlextGrpcChannel(id="test", target="localhost:50051", created_at=self.now),
            FlextGrpcServer(
                id="test", host="localhost", port=50051, created_at=self.now
            ),
            FlextGrpcClient(id="test", target="localhost:50051", created_at=self.now),
            FlextGrpcStream(
                id="test",
                method_name="TestMethod",
                stream_type="unary",
                created_at=self.now,
            ),
        ]

        for entity in entities:
            assert isinstance(entity, FlextGrpcEntity)
            assert hasattr(entity, "id")
            assert hasattr(entity, "created_at")
            assert hasattr(entity, "updated_at")
