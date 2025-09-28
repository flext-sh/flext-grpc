"""Advanced tests for flext_grpc.services module.

Tests additional functionality to improve coverage.
"""

from __future__ import annotations

from datetime import UTC, datetime
from unittest.mock import MagicMock, patch

from flext_core import FlextResult
from flext_grpc.entities import FlextGrpcClient, FlextGrpcServer, FlextGrpcStream
from flext_grpc.services import FlextGrpcService


class TestFlextGrpcServiceAdvanced:
    """Advanced tests for FlextGrpcService to improve coverage."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.service = FlextGrpcService()
        self.now = datetime.now(UTC)

    def _create_mock_result(
        self, is_success: bool, error: str | None = None
    ) -> FlextResult[object]:
        """Create a properly typed mock result."""
        mock_result = MagicMock()
        mock_result.is_success = is_success
        mock_result.error = error
        return mock_result

    def test_execute_start_server_with_server_management_error(self) -> None:
        """Test execute start server with server management error."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        with patch.object(self.service, "_start_server") as mock_start:
            mock_result = self._create_mock_result(False, "Server management error")
            mock_start.return_value = mock_result

            result = self.service.execute("start", server)

        assert result.is_success is False
        assert result.error is not None and "Server management error" in result.error

    def test_execute_stop_server_with_server_management_error(self) -> None:
        """Test execute stop server with server management error."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        with patch.object(self.service, "_stop_server") as mock_stop:
            mock_result = self._create_mock_result(False, "Server stop error")
            mock_stop.return_value = mock_result

            result = self.service.execute("stop", server)

        assert result.is_success is False
        assert result.error is not None and "Server stop error" in result.error

    def test_execute_connect_client_with_client_management_error(self) -> None:
        """Test execute connect client with client management error."""
        client = FlextGrpcClient(
            id="test-client",
            created_at=self.now,
        )

        with patch.object(self.service, "_connect_client") as mock_connect:
            mock_result = self._create_mock_result(False, "Client connection error")
            mock_connect.return_value = mock_result

            result = self.service.execute("connect", client)

        assert result.is_success is False
        assert result.error is not None and "Client connection error" in result.error

    def test_execute_disconnect_client_with_client_management_error(self) -> None:
        """Test execute disconnect client with client management error."""
        client = FlextGrpcClient(
            id="test-client",
            created_at=self.now,
        )

        with patch.object(self.service, "_disconnect_client") as mock_disconnect:
            mock_result = self._create_mock_result(False, "Client disconnection error")
            mock_disconnect.return_value = mock_result

            result = self.service.execute("disconnect", client)

        assert result.is_success is False
        assert result.error is not None and "Client disconnection error" in result.error

    def test_execute_call_with_call_management_error(self) -> None:
        """Test execute call with call management error."""
        client = FlextGrpcClient(
            id="test-client",
            created_at=self.now,
        )

        with patch.object(self.service, "_make_call") as mock_call:
            mock_result = self._create_mock_result(False, "Call execution error")
            mock_call.return_value = mock_result

            result = self.service.execute(
                "call", client, "TestMethod", request="value1"
            )

        assert result.is_success is False
        assert result.error is not None and "Call execution error" in result.error

    def test_execute_stream_with_stream_management_error(self) -> None:
        """Test execute stream with stream management error."""
        stream = FlextGrpcStream(
            id="test-stream",
            method_name="TestMethod",
            stream_type="unary",
            created_at=self.now,
        )

        with patch.object(self.service, "_send_data") as mock_send:
            mock_result = self._create_mock_result(False, "Stream data error")
            mock_send.return_value = mock_result

            result = self.service.execute("send", stream, data="test_data")

        assert result.is_success is False
        assert result.error is not None and "Stream data error" in result.error

    def test_execute_status_with_status_management_error(self) -> None:
        """Test execute status with status management error."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        with patch.object(self.service, "_get_status") as mock_status:
            mock_result = self._create_mock_result(False, "Status retrieval error")
            mock_status.return_value = mock_result

            result = self.service.execute("status", server)

        assert result.is_success is False
        assert result.error is not None and "Status retrieval error" in result.error

    def test_start_server_with_grpc_server_creation_error(self) -> None:
        """Test _start_server with gRPC server creation error."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        with patch("grpc.server", side_effect=Exception("gRPC server creation failed")):
            result = self.service.execute("start", server)

        assert result.is_success is False
        assert (
            result.error is not None and "gRPC server creation failed" in result.error
        )

    def test_start_server_with_server_start_error(self) -> None:
        """Test _start_server with server start error."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        with patch("grpc.server") as mock_grpc_server:
            mock_server_instance = MagicMock()
            mock_server_instance.start.side_effect = Exception("Server start failed")
            mock_grpc_server.return_value = mock_server_instance

            result = self.service.execute("start", server)

        assert result.is_success is False
        assert result.error is not None and "Server start failed" in result.error

    def test_stop_server_with_server_stop_error(self) -> None:
        """Test _stop_server with server stop error."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        # Mock the server stop method to return a failed result
        with patch.object(self.service, "_stop_server") as mock_stop_server:
            mock_stop_server.return_value = self._create_mock_result(
                False, "Server stop failed"
            )
            result = self.service.execute("stop", server)

        assert result.is_success is False
        assert result.error is not None and "Server stop failed" in result.error

    def test_connect_client_with_channel_creation_error(self) -> None:
        """Test _connect_client with channel creation error."""
        client = FlextGrpcClient(
            id="test-client",
            created_at=self.now,
        )

        with patch(
            "grpc.insecure_channel", side_effect=Exception("Channel creation failed")
        ):
            result = self.service.execute("connect", client)

        assert result.is_success is False
        assert result.error is not None and "Channel creation failed" in result.error

    def test_connect_client_with_channel_connection_error(self) -> None:
        """Test _connect_client with channel connection error."""
        client = FlextGrpcClient(
            id="test-client",
            created_at=self.now,
        )

        with patch("grpc.insecure_channel") as mock_channel:
            mock_channel_instance = MagicMock()
            mock_channel_instance.get_state.side_effect = Exception(
                "Channel connection failed"
            )
            mock_channel.return_value = mock_channel_instance

            result = self.service.execute("connect", client)

        assert result.is_success is False
        assert result.error is not None and "Channel connection failed" in result.error

    def test_disconnect_client_with_channel_close_error(self) -> None:
        """Test _disconnect_client with channel close error."""
        client = FlextGrpcClient(
            id="test-client",
            created_at=self.now,
        )

        # Mock the client disconnect method to raise an exception
        with patch.object(client, "channel") as mock_channel:
            mock_channel_instance = MagicMock()
            mock_channel_instance.close.side_effect = Exception("Channel close failed")
            mock_channel.return_value = mock_channel_instance
            result = self.service.execute("disconnect", client)

        assert result.is_success is False
        assert result.error is not None and "Channel close failed" in result.error

    def test_make_call_with_stub_creation_error(self) -> None:
        """Test _make_call with stub creation error."""
        client = FlextGrpcClient(
            id="test-client",
            created_at=self.now,
        )

        # Mock the client with a channel
        mock_channel = MagicMock()
        client.channel = mock_channel

        with patch("grpc.insecure_channel") as mock_grpc_channel:
            mock_grpc_channel.side_effect = Exception("Stub creation failed")

            result = self.service.execute("call", client, "TestMethod")

        assert result.is_success is False
        assert result.error is not None and "Stub creation failed" in result.error

    def test_make_call_with_method_call_error(self) -> None:
        """Test _make_call with method call error."""
        client = FlextGrpcClient(
            id="test-client",
            created_at=self.now,
        )

        # Mock the client channel and stub creation
        with patch("grpc.insecure_channel") as mock_channel:
            mock_channel_instance = MagicMock()
            mock_channel.return_value = mock_channel_instance

            with patch("flext_grpc.proto.FlextGrpcServiceStub") as mock_stub_class:
                mock_stub = MagicMock()
                mock_stub_class.return_value = mock_stub

                # Mock the method call to raise an exception
                mock_method = MagicMock()
                mock_stub.TestMethod = mock_method
                mock_method.side_effect = Exception("Method call failed")

                result = self.service.execute(
                    "call", client, "TestMethod", request="value1"
                )

        assert result.is_success is False
        assert result.error is not None and "Method call failed" in result.error

    def test_send_data_with_stream_creation_error(self) -> None:
        """Test _send_data with stream creation error."""
        stream = FlextGrpcStream(
            id="test-stream",
            method_name="TestMethod",
            stream_type="unary",
            created_at=self.now,
        )

        with patch.object(self.service, "_create_stream") as mock_create_stream:
            mock_result = self._create_mock_result(False, "Stream creation failed")
            mock_create_stream.return_value = mock_result

            result = self.service.execute("send", stream, data="test_data")

        assert result.is_success is False
        assert result.error is not None and "Stream creation failed" in result.error

    def test_send_data_with_stream_data_error(self) -> None:
        """Test _send_data with stream data error."""
        stream = FlextGrpcStream(
            id="test-stream",
            method_name="TestMethod",
            stream_type="unary",
            created_at=self.now,
        )

        with patch.object(self.service, "_create_stream") as mock_create_stream:
            mock_result = self._create_mock_result(True)
            mock_create_stream.return_value = mock_result

            with patch.object(self.service, "_handle_server_streaming") as mock_handle:
                mock_handle_result = self._create_mock_result(
                    False, "Stream data handling failed"
                )
                mock_handle.return_value = mock_handle_result

                result = self.service.execute("send", stream, data="test_data")

        assert result.is_success is False
        assert (
            result.error is not None and "Stream data handling failed" in result.error
        )

    def test_get_status_with_status_retrieval_error(self) -> None:
        """Test _get_status with status retrieval error."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        # Mock the server status method to raise an exception
        with patch.object(self.service, "_get_status") as mock_get_status:
            mock_get_status.side_effect = Exception("Status retrieval failed")
            result = self.service.execute("status", server)

        assert result.is_success is False
        assert result.error is not None and "Status retrieval failed" in result.error

    def test_handle_server_streaming_with_stream_handling_error(self) -> None:
        """Test _handle_server_streaming with stream handling error."""
        stream = FlextGrpcStream(
            id="test-stream",
            method_name="TestMethod",
            stream_type="server_streaming",
            created_at=self.now,
        )

        # Mock the stream handling method to raise an exception
        with patch.object(self.service, "_handle_server_streaming") as mock_handle:
            mock_handle.side_effect = Exception("Stream handling failed")
            result = self.service.execute("send", stream, data="test_data")

        assert result.is_success is False
        assert result.error is not None and "Stream handling failed" in result.error

    def test_create_stream_with_stream_creation_error(self) -> None:
        """Test _create_stream with stream creation error."""
        stream = FlextGrpcStream(
            id="test-stream",
            method_name="TestMethod",
            stream_type="unary",
            created_at=self.now,
        )

        with patch(
            "grpc.insecure_channel", side_effect=Exception("Stream creation failed")
        ):
            result = self.service.execute("create", stream)

        assert result.is_success is False
        assert result.error is not None and "Stream creation failed" in result.error

    def test_create_stream_with_stream_setup_error(self) -> None:
        """Test _create_stream with stream setup error."""
        stream = FlextGrpcStream(
            id="test-stream",
            method_name="TestMethod",
            stream_type="unary",
            created_at=self.now,
        )

        with patch("grpc.insecure_channel") as mock_channel:
            mock_channel_instance = MagicMock()
            mock_channel_instance.get_state.side_effect = Exception(
                "Stream setup failed"
            )
            mock_channel.return_value = mock_channel_instance

            result = self.service.execute("create", stream)

        assert result.is_success is False
        assert result.error is not None and "Stream setup failed" in result.error

    def test_execute_with_invalid_command_and_entity(self) -> None:
        """Test execute with invalid command and entity."""
        result = self.service.execute("invalid_command", {"type": "invalid_entity"})

        assert result.is_success is False
        assert result.error is not None and "Invalid entity type" in result.error

    def test_execute_with_valid_command_but_wrong_entity_type(self) -> None:
        """Test execute with valid command but wrong entity type."""
        client = FlextGrpcClient(
            id="test-client",
            created_at=self.now,
        )

        # Try to start a client (should fail)
        result = self.service.execute("start", client)

        assert result.is_success is False
        assert result.error is not None and "Invalid entity type" in result.error

    def test_execute_call_with_empty_method_name(self) -> None:
        """Test execute call with empty method name."""
        client = FlextGrpcClient(
            id="test-client",
            created_at=self.now,
        )

        result = self.service.execute("call", client, "", request="value1")

        assert result.is_success is False
        assert (
            result.error is not None and "Method name must be a string" in result.error
        )

    def test_execute_call_with_whitespace_method_name(self) -> None:
        """Test execute call with whitespace-only method name."""
        client = FlextGrpcClient(
            id="test-client",
            created_at=self.now,
        )

        result = self.service.execute("call", client, "   ", request="value1")

        assert result.is_success is False
        assert (
            result.error is not None and "Method name must be a string" in result.error
        )

    def test_execute_call_with_none_method_name(self) -> None:
        """Test execute call with None method name."""
        client = FlextGrpcClient(
            id="test-client",
            created_at=self.now,
        )

        result = self.service.execute("call", client, None, request="value1")

        assert result.is_success is False
        assert (
            result.error is not None and "Method name must be a string" in result.error
        )

    def test_execute_call_with_non_string_method_name(self) -> None:
        """Test execute call with non-string method name."""
        client = FlextGrpcClient(
            id="test-client",
            created_at=self.now,
        )

        result = self.service.execute("call", client, 123, request="value1")

        assert result.is_success is False
        assert (
            result.error is not None and "Method name must be a string" in result.error
        )

    def test_execute_call_with_insufficient_arguments(self) -> None:
        """Test execute call with insufficient arguments."""
        client = FlextGrpcClient(
            id="test-client",
            created_at=self.now,
        )

        result = self.service.execute("call", client)

        assert result.is_success is False
        assert result.error is not None and "Insufficient arguments" in result.error

    def test_execute_call_with_no_method_name_argument(self) -> None:
        """Test execute call with no method name argument."""
        client = FlextGrpcClient(
            id="test-client",
            created_at=self.now,
        )

        result = self.service.execute("call", client, request="value1")

        assert result.is_success is False
        assert (
            result.error is not None and "Method name must be a string" in result.error
        )

    def test_execute_stream_with_no_data_argument(self) -> None:
        """Test execute stream with no data argument."""
        stream = FlextGrpcStream(
            id="test-stream",
            method_name="TestMethod",
            stream_type="unary",
            created_at=self.now,
        )

        result = self.service.execute("stream", stream)

        assert result.is_success is False
        assert result.error is not None and "Stream data required" in result.error

    def test_execute_stream_with_empty_data_argument(self) -> None:
        """Test execute stream with empty data argument."""
        stream = FlextGrpcStream(
            id="test-stream",
            method_name="TestMethod",
            stream_type="unary",
            created_at=self.now,
        )

        result = self.service.execute("send", stream, data="")

        assert result.is_success is False
        assert (
            result.error is not None and "Stream data cannot be empty" in result.error
        )

    def test_execute_stream_with_none_data_argument(self) -> None:
        """Test execute stream with None data argument."""
        stream = FlextGrpcStream(
            id="test-stream",
            method_name="TestMethod",
            stream_type="unary",
            created_at=self.now,
        )

        result = self.service.execute("send", stream, data=None)

        assert result.is_success is False
        assert result.error is not None and "Stream data cannot be None" in result.error

    def test_execute_status_with_no_entity(self) -> None:
        """Test execute status with no entity."""
        result = self.service.execute("status")

        assert result.is_success is False
        assert result.error is not None and "Entity instance required" in result.error

    def test_execute_status_with_wrong_entity_type(self) -> None:
        """Test execute status with wrong entity type."""
        stream = FlextGrpcStream(
            id="test-stream",
            method_name="TestMethod",
            stream_type="unary",
            created_at=self.now,
        )

        # Try to get status of a stream (should fail)
        result = self.service.execute("status", stream)

        assert result.is_success is False
        assert result.error is not None and "Invalid entity type" in result.error

    def test_execute_with_unknown_command_and_valid_entity(self) -> None:
        """Test execute with unknown command and valid entity."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        result = self.service.execute("unknown_command", server)

        assert result.is_success is False
        assert result.error is not None and "Unknown command" in result.error

    def test_execute_with_unknown_command_and_invalid_entity(self) -> None:
        """Test execute with unknown command and invalid entity."""
        result = self.service.execute("unknown_command", {"type": "invalid_entity"})

        assert result.is_success is False
        assert result.error is not None and "Invalid entity type" in result.error

    def test_execute_with_unknown_command_and_none_entity(self) -> None:
        """Test execute with unknown command and None entity."""
        result = self.service.execute("unknown_command", None)

        assert result.is_success is False
        assert result.error is not None and "Entity instance required" in result.error

    def test_execute_with_unknown_command_and_no_entity(self) -> None:
        """Test execute with unknown command and no entity."""
        result = self.service.execute("unknown_command")

        assert result.is_success is False
        assert result.error is not None and "Unknown command" in result.error

    def test_execute_with_valid_command_but_missing_entity(self) -> None:
        """Test execute with valid command but missing entity."""
        result = self.service.execute("start")

        assert result.is_success is False
        assert result.error is not None and "Entity instance required" in result.error

    def test_execute_with_valid_command_but_none_entity(self) -> None:
        """Test execute with valid command but None entity."""
        result = self.service.execute("start", None)

        assert result.is_success is False
        assert result.error is not None and "Entity instance required" in result.error

    def test_execute_with_valid_command_but_invalid_entity_type(self) -> None:
        """Test execute with valid command but invalid entity type."""
        result = self.service.execute("start", {"type": "invalid_entity"})

        assert result.is_success is False
        assert result.error is not None and "Invalid entity type" in result.error

    def test_execute_with_valid_command_but_wrong_entity_type_for_command(self) -> None:
        """Test execute with valid command but wrong entity type for command."""
        client = FlextGrpcClient(
            id="test-client",
            created_at=self.now,
        )

        # Try to start a client (should fail)
        result = self.service.execute("start", client)

        assert result.is_success is False
        assert result.error is not None and "Invalid entity type" in result.error

    def test_execute_with_valid_command_but_wrong_entity_type_for_status(self) -> None:
        """Test execute with valid command but wrong entity type for status."""
        stream = FlextGrpcStream(
            id="test-stream",
            method_name="TestMethod",
            stream_type="unary",
            created_at=self.now,
        )

        # Try to get status of a stream (should fail)
        result = self.service.execute("status", stream)

        assert result.is_success is False
        assert result.error is not None and "Invalid entity type" in result.error

    def test_execute_with_valid_command_but_wrong_entity_type_for_call(self) -> None:
        """Test execute with valid command but wrong entity type for call."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        # Try to make a call with a server (should fail)
        result = self.service.execute("call", server, "TestMethod", request="value1")

        assert result.is_success is False
        assert result.error is not None and "Invalid entity type" in result.error

    def test_execute_with_valid_command_but_wrong_entity_type_for_stream(self) -> None:
        """Test execute with valid command but wrong entity type for stream."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        # Try to send stream data with a server (should fail)
        result = self.service.execute("send", server, data="test_data")

        assert result.is_success is False
        assert result.error is not None and "Invalid entity type" in result.error

    def test_execute_with_valid_command_but_wrong_entity_type_for_connect(self) -> None:
        """Test execute with valid command but wrong entity type for connect."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        # Try to connect a server (should fail)
        result = self.service.execute("connect", server)

        assert result.is_success is False
        assert result.error is not None and "Invalid entity type" in result.error

    def test_execute_with_valid_command_but_wrong_entity_type_for_disconnect(
        self,
    ) -> None:
        """Test execute with valid command but wrong entity type for disconnect."""
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            created_at=self.now,
        )

        # Try to disconnect a server (should fail)
        result = self.service.execute("disconnect", server)

        assert result.is_success is False
        assert result.error is not None and "Invalid entity type" in result.error

    def test_execute_with_valid_command_but_wrong_entity_type_for_stop(self) -> None:
        """Test execute with valid command but wrong entity type for stop."""
        client = FlextGrpcClient(
            id="test-client",
            created_at=self.now,
        )

        # Try to stop a client (should fail)
        result = self.service.execute("stop", client)

        assert result.is_success is False
        assert result.error is not None and "Invalid entity type" in result.error
