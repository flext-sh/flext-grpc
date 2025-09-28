"""Additional tests for flext_grpc.services module.

Tests additional functionality to improve coverage.
"""

from __future__ import annotations

from datetime import UTC, datetime
from unittest.mock import MagicMock, patch

from flext_grpc.entities import FlextGrpcClient, FlextGrpcServer, FlextGrpcStream
from flext_grpc.services import FlextGrpcService


class TestFlextGrpcServiceAdditional:
    """Additional tests for FlextGrpcService to improve coverage."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.service = FlextGrpcService()

    def test_execute_invalid_command(self) -> None:
        """Test execute with invalid command."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            max_workers=10,
            services=[],
            created_at=datetime.now(UTC),
        )

        result = self.service.execute("invalid_command", server)

        assert result.is_success is False
        assert result.error is not None
        assert "Unknown command" in result.error

    def test_execute_start_command_with_server(self) -> None:
        """Test execute with start command and server."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            max_workers=10,
            services=[],
            created_at=datetime.now(UTC),
        )

        with patch.object(self.service, "_start_server") as mock_start:
            mock_result = MagicMock()
            mock_result.is_success = True
            mock_result.value = server
            mock_start.return_value = mock_result

            result = self.service.execute("start", server)

        assert result.is_success
        mock_start.assert_called_once_with(server)

    def test_execute_stop_command_with_server(self) -> None:
        """Test execute with stop command and server."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            max_workers=10,
            services=[],
            created_at=datetime.now(UTC),
        )

        with patch.object(self.service, "_stop_server") as mock_stop:
            mock_result = MagicMock()
            mock_result.is_success = True
            mock_result.value = server
            mock_stop.return_value = mock_result

            result = self.service.execute("stop", server)

        assert result.is_success
        mock_stop.assert_called_once_with(server)

    def test_execute_connect_command_with_client(self) -> None:
        """Test execute with connect command and client."""
        client = FlextGrpcClient(
            id="test-client",
            target="localhost:50051",
            channel=None,
            created_at=datetime.now(UTC),
        )

        with patch.object(self.service, "_connect_client") as mock_connect:
            mock_result = MagicMock()
            mock_result.is_success = True
            mock_result.value = client
            mock_connect.return_value = mock_result

            result = self.service.execute("connect", client)

        assert result.is_success
        mock_connect.assert_called_once_with(client)

    def test_execute_disconnect_command_with_client(self) -> None:
        """Test execute with disconnect command and client."""
        client = FlextGrpcClient(
            id="test-client",
            target="localhost:50051",
            channel=None,
            created_at=datetime.now(UTC),
        )

        with patch.object(self.service, "_disconnect_client") as mock_disconnect:
            mock_result = MagicMock()
            mock_result.is_success = True
            mock_result.value = client
            mock_disconnect.return_value = mock_result

            result = self.service.execute("disconnect", client)

        assert result.is_success
        mock_disconnect.assert_called_once_with(client)

    def test_execute_call_command_with_client(self) -> None:
        """Test execute with call command and client."""
        client = FlextGrpcClient(
            id="test-client",
            target="localhost:50051",
            channel=None,
            created_at=datetime.now(UTC),
        )

        with patch.object(self.service, "_make_call") as mock_call:
            mock_result = MagicMock()
            mock_result.is_success = True
            mock_result.value = {"result": "success"}
            mock_call.return_value = mock_result

            result = self.service.execute("call", client, "TestMethod", arg1="value1")

        assert result.is_success
        mock_call.assert_called_once_with(client, "TestMethod", arg1="value1")

    def test_execute_stream_command_with_stream(self) -> None:
        """Test execute with stream command and stream."""
        stream = FlextGrpcStream(
            id="test-stream",
            method_name="TestMethod",
            stream_type="unary",
            created_at=datetime.now(UTC),
        )

        with patch.object(self.service, "_send_data") as mock_send:
            mock_result = MagicMock()
            mock_result.is_success = True
            mock_result.value = {"result": "success"}
            mock_send.return_value = mock_result

            result = self.service.execute("stream", stream, data="test_data")

        assert result.is_success
        mock_send.assert_called_once_with(stream, data="test_data")

    def test_execute_status_command_with_server(self) -> None:
        """Test execute with status command and server."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            max_workers=10,
            services=[],
            created_at=datetime.now(UTC),
        )

        with patch.object(self.service, "_get_status") as mock_status:
            mock_result = MagicMock()
            mock_result.is_success = True
            mock_result.value = {"status": "running"}
            mock_status.return_value = mock_result

            result = self.service.execute("status", server)

        assert result.is_success
        mock_status.assert_called_once_with(server)

    def test_start_server_success(self) -> None:
        """Test _start_server with successful start."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            max_workers=10,
            services=[],
            created_at=datetime.now(UTC),
        )

        with patch("grpc.server") as mock_grpc_server:
            mock_server_instance = MagicMock()
            mock_grpc_server.return_value = mock_server_instance

            result = self.service._start_server(server)

        assert result.is_success

    def test_start_server_failure(self) -> None:
        """Test _start_server with failure."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            max_workers=10,
            services=[],
            created_at=datetime.now(UTC),
        )

        with patch("grpc.server", side_effect=Exception("Server start failed")):
            result = self.service._start_server(server)

        assert result.is_success is False
        assert result.error is not None
        assert "Server start failed" in result.error

    def test_stop_server_success(self) -> None:
        """Test _stop_server with successful stop."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            max_workers=10,
            services=[],
            created_at=datetime.now(UTC),
        )

        # Mock the server with a grpc_server
        mock_grpc_server = MagicMock()
        server.grpc_server = mock_grpc_server

        result = self.service._stop_server(server)

        assert result.is_success
        mock_grpc_server.stop.assert_called_once()

    def test_stop_server_no_grpc_server(self) -> None:
        """Test _stop_server when no grpc_server is set."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            max_workers=10,
            services=[],
            created_at=datetime.now(UTC),
        )

        # No grpc_server set
        result = self.service._stop_server(server)

        assert result.is_success is False
        assert result.error is not None
        assert "No active gRPC server" in result.error

    def test_connect_client_success(self) -> None:
        """Test _connect_client with successful connection."""
        client = FlextGrpcClient(
            id="test-client",
            target="localhost:50051",
            channel=None,
            created_at=datetime.now(UTC),
        )

        with patch("grpc.insecure_channel") as mock_channel:
            mock_channel_instance = MagicMock()
            mock_channel.return_value = mock_channel_instance

            result = self.service._connect_client(client)

        assert result.is_success

    def test_connect_client_failure(self) -> None:
        """Test _connect_client with connection failure."""
        client = FlextGrpcClient(
            id="test-client",
            target="localhost:50051",
            channel=None,
            created_at=datetime.now(UTC),
        )

        with patch("grpc.insecure_channel", side_effect=Exception("Connection failed")):
            result = self.service._connect_client(client)

        assert result.is_success is False
        assert result.error is not None
        assert "Connection failed" in result.error

    def test_disconnect_client_success(self) -> None:
        """Test _disconnect_client with successful disconnection."""
        client = FlextGrpcClient(
            id="test-client",
            target="localhost:50051",
            channel=None,
            created_at=datetime.now(UTC),
        )

        # Mock the client with a channel
        mock_channel = MagicMock()
        client.channel = mock_channel

        result = self.service._disconnect_client(client)

        assert result.is_success
        mock_channel.close.assert_called_once()

    def test_disconnect_client_no_channel(self) -> None:
        """Test _disconnect_client when no channel is set."""
        client = FlextGrpcClient(
            id="test-client",
            target="localhost:50051",
            channel=None,
            created_at=datetime.now(UTC),
        )

        # No channel set
        result = self.service._disconnect_client(client)

        assert result.is_success is False
        assert result.error is not None
        assert "No active gRPC channel" in result.error

    def test_make_call_success(self) -> None:
        """Test _make_call with successful call."""
        client = FlextGrpcClient(
            id="test-client",
            target="localhost:50051",
            channel=None,
            created_at=datetime.now(UTC),
        )

        # Mock the client with a channel and stub
        mock_channel = MagicMock()
        mock_stub = MagicMock()
        client.channel = mock_channel
        client.grpc_stub = mock_stub

        # Mock the method call
        mock_method = MagicMock()
        mock_stub.TestMethod = mock_method
        mock_method.return_value = {"result": "success"}

        result = self.service._make_call(client, "TestMethod", arg1="value1")

        assert result.is_success

    def test_make_call_no_channel(self) -> None:
        """Test _make_call when no channel is set."""
        client = FlextGrpcClient(
            id="test-client",
            target="localhost:50051",
            channel=None,
            created_at=datetime.now(UTC),
        )

        result = self.service._make_call(client, "TestMethod")

        assert result.is_success is False
        assert result.error is not None
        assert "No active gRPC channel" in result.error

    def test_send_data_success(self) -> None:
        """Test _send_data with successful send."""
        stream = FlextGrpcStream(
            id="test-stream",
            method_name="TestMethod",
            stream_type="unary",
            created_at=datetime.now(UTC),
        )

        with patch.object(self.service, "_handle_server_streaming") as mock_handle:
            mock_result = MagicMock()
            mock_result.is_success = True
            mock_result.value = {"result": "success"}
            mock_handle.return_value = mock_result

            result = self.service._send_data(stream, data="test_data")

        assert result.is_success
        mock_handle.assert_called_once()

    def test_get_status_success(self) -> None:
        """Test _get_status with successful status check."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            max_workers=10,
            services=[],
            created_at=datetime.now(UTC),
        )

        # Mock the server with a grpc_server
        mock_grpc_server = MagicMock()
        server.grpc_server = mock_grpc_server

        result = self.service._get_status(server)

        assert result.is_success
        assert "status" in result.value

    def test_get_status_no_grpc_server(self) -> None:
        """Test _get_status when no grpc_server is set."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            max_workers=10,
            services=[],
            created_at=datetime.now(UTC),
        )

        # No grpc_server set
        result = self.service._get_status(server)

        assert result.is_success is False
        assert result.error is not None
        assert "No active gRPC server" in result.error

    def test_handle_server_streaming_success(self) -> None:
        """Test _handle_server_streaming with successful streaming."""
        stream = FlextGrpcStream(
            id="test-stream",
            method_name="TestMethod",
            stream_type="server_streaming",
            created_at=datetime.now(UTC),
        )

        # Mock the stream with a grpc_stub
        mock_stub = MagicMock()
        stream.grpc_stub = mock_stub

        # Mock the streaming response
        mock_response = MagicMock()
        mock_response.data = "test_response"
        mock_stub.TestMethod.return_value = [mock_response]

        result = self.service._handle_server_streaming(stream)

        assert result.is_success

    def test_handle_server_streaming_no_stub(self) -> None:
        """Test _handle_server_streaming when no grpc_stub is set."""
        stream = FlextGrpcStream(
            id="test-stream",
            method_name="TestMethod",
            stream_type="server_streaming",
            created_at=datetime.now(UTC),
        )

        # No grpc_stub set
        result = self.service._handle_server_streaming(stream)

        assert result.is_success is False
        assert result.error is not None
        assert "No active gRPC stub" in result.error

    def test_create_stream_success(self) -> None:
        """Test _create_stream with successful stream creation."""
        stream = FlextGrpcStream(
            id="test-stream",
            method_name="TestMethod",
            stream_type="unary",
            created_at=datetime.now(UTC),
        )

        with patch("grpc.insecure_channel") as mock_channel:
            mock_channel_instance = MagicMock()
            mock_channel.return_value = mock_channel_instance

            result = self.service._create_stream(stream)

        assert result.is_success

    def test_create_stream_failure(self) -> None:
        """Test _create_stream with stream creation failure."""
        stream = FlextGrpcStream(
            id="test-stream",
            method_name="TestMethod",
            stream_type="unary",
            created_at=datetime.now(UTC),
        )

        with patch(
            "grpc.insecure_channel", side_effect=Exception("Stream creation failed")
        ):
            result = self.service._create_stream(stream)

        assert result.is_success is False
        assert result.error is not None
        assert "Stream creation failed" in result.error
