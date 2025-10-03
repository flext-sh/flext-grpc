"""Tests for flext_grpc.utilities module.

Tests the FlextGrpcUtilities class and its nested utility classes.
"""

from __future__ import annotations

from collections.abc import Iterator
from datetime import UTC, datetime
from typing import cast
from unittest.mock import MagicMock, patch

import grpc
from google.protobuf import json_format
from google.protobuf.message import Message as ProtobufMessage
from google.protobuf.struct_pb2 import Struct

from flext_core import FlextTypes
from flext_grpc.models import FlextGrpcModels
from flext_grpc.utilities import FlextGrpcUtilities


class TestFlextGrpcUtilities:
    """Test the main FlextGrpcUtilities class."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.utilities = FlextGrpcUtilities()

    def test_init(self) -> None:
        """Test FlextGrpcUtilities initialization."""
        assert isinstance(self.utilities, FlextGrpcUtilities)
        assert hasattr(self.utilities, "_container")
        assert hasattr(self.utilities, "_logger")

    def test_execute(self) -> None:
        """Test the execute method."""
        result = self.utilities.execute()

        assert result.is_success
        assert result.data is not None
        assert result.data["status"] == "operational"
        assert result.data["service"] == "flext-grpc-utilities"
        assert "capabilities" in result.data
        assert len(result.data["capabilities"]) > 0

    def test_logger_property(self) -> None:
        """Test logger property."""
        logger = self.utilities.logger
        assert logger is not None

    def test_container_property(self) -> None:
        """Test container property."""
        container = self.utilities.container
        assert container is not None


class TestMessageValidation:
    """Test the MessageValidation nested class."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.utilities = FlextGrpcUtilities()
        self.validator = self.utilities.MessageValidation()

    def test_validate_protobuf_message_none(self) -> None:
        """Test validation with None message."""
        result = self.utilities.MessageValidation.validate_protobuf_message(None)

        assert result.is_failure
        assert result.error is not None
        assert result.error is not None and "Invalid message instance" in result.error

    def test_validate_protobuf_message_valid(self) -> None:
        """Test validation with valid message."""
        # Create a mock protobuf message
        mock_message = MagicMock(spec=ProtobufMessage)
        mock_message.DESCRIPTOR = MagicMock()
        mock_message.DESCRIPTOR.fields_by_name = {}

        result = self.utilities.MessageValidation.validate_protobuf_message(
            mock_message
        )

        assert result.is_success
        assert result.data is True

    def test_validate_grpc_request_valid(self) -> None:
        """Test gRPC request validation with valid request."""
        # Create a mock valid request
        mock_request = MagicMock(spec=FlextGrpcModels.GrpcRequest)
        mock_request.model_dump.return_value = {"method": "Test", "data": "test"}

        with patch.object(
            FlextGrpcModels.GrpcRequest, "model_validate"
        ) as mock_validate:
            mock_validate.return_value = mock_request

            result = self.utilities.MessageValidation.validate_grpc_request(
                mock_request
            )

        assert result.is_success
        assert result.data == mock_request

    def test_validate_grpc_request_invalid(self) -> None:
        """Test gRPC request validation with invalid request."""
        mock_request = MagicMock(spec=FlextGrpcModels.GrpcRequest)
        mock_request.model_dump.return_value = {"invalid": "data"}

        with patch.object(
            FlextGrpcModels.GrpcRequest,
            "model_validate",
            side_effect=Exception("Validation error"),
        ):
            result = self.utilities.MessageValidation.validate_grpc_request(
                mock_request
            )

        assert result.is_failure
        assert result.error is not None
        assert result.error is not None and "Request validation failed" in result.error

    def test_validate_stream_message_sequence_empty(self) -> None:
        """Test stream message sequence validation with empty sequence."""
        result = self.utilities.MessageValidation.validate_stream_message_sequence([])

        assert result.is_failure
        assert result.error is not None
        assert (
            result.error is not None
            and "Message sequence cannot be empty" in result.error
        )

    def test_validate_stream_message_sequence_valid(self) -> None:
        """Test stream message sequence validation with valid messages."""
        # Create mock messages that pass validation
        mock_msg1 = MagicMock(spec=ProtobufMessage)
        mock_msg1.DESCRIPTOR = MagicMock()
        mock_msg1.DESCRIPTOR.fields = []
        mock_msg1.HasField.return_value = True
        mock_msg1.SerializeToString.return_value = b"serialized"

        mock_msg2 = MagicMock(spec=ProtobufMessage)
        mock_msg2.DESCRIPTOR = MagicMock()
        mock_msg2.DESCRIPTOR.fields = []
        mock_msg2.HasField.return_value = True
        mock_msg2.SerializeToString.return_value = b"serialized"

        # Cast to proper type to satisfy type checker
        messages: list[ProtobufMessage] = [mock_msg1, mock_msg2]

        result = self.utilities.MessageValidation.validate_stream_message_sequence(
            messages
        )

        assert result.is_success
        assert result.data is True


class TestProtobufConversion:
    """Test the ProtobufConversion nested class."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.utilities = FlextGrpcUtilities()
        self.converter = self.utilities.ProtobufConversion()

    def test_dict_to_protobuf_valid(self) -> None:
        """Test converting dict to protobuf with valid data."""
        data_dict = {"message": "test", "timestamp": 1234567890}

        # Use a real protobuf message class for testing
        mock_message_class = Struct
        mock_instance = MagicMock(spec=ProtobufMessage)

        with patch.object(json_format, "ParseDict") as mock_parse:
            mock_parse.return_value = None  # ParseDict doesn't return anything

            with patch.object(
                mock_message_class, "__call__", return_value=mock_instance
            ):
                result = self.utilities.ProtobufConversion.dict_to_protobuf(
                    data_dict, mock_message_class
                )

        assert result.is_success
        assert result.data == mock_instance

    def test_dict_to_protobuf_invalid_data(self) -> None:
        """Test converting dict to protobuf with invalid data."""
        data_dict = {"invalid_field": "test"}

        # Create a proper mock class that satisfies type[ProtobufMessage]
        error_msg = "Invalid protobuf data"

        class MockProtobufClass:
            def __init__(self) -> None:
                raise ValueError(error_msg)

        mock_message_class = cast("type[ProtobufMessage]", MockProtobufClass)

        result = self.utilities.ProtobufConversion.dict_to_protobuf(
            data_dict, mock_message_class
        )

        assert result.is_failure
        assert result.error is not None
        assert (
            result.error is not None
            and "Dict to protobuf conversion failed" in result.error
        )

    def test_protobuf_to_dict_valid(self) -> None:
        """Test converting protobuf to dict with valid message."""
        mock_message = MagicMock(spec=ProtobufMessage)
        mock_dict = {"message": "test", "timestamp": 1234567890}

        with patch.object(json_format, "MessageToDict", return_value=mock_dict):
            result = self.utilities.ProtobufConversion.protobuf_to_dict(mock_message)

        assert result.is_success
        assert result.data == mock_dict

    def test_protobuf_to_dict_invalid_message(self) -> None:
        """Test converting protobuf to dict with invalid message."""
        mock_message = MagicMock(spec=ProtobufMessage)

        with patch.object(
            json_format, "MessageToDict", side_effect=Exception("Conversion error")
        ):
            result = self.utilities.ProtobufConversion.protobuf_to_dict(mock_message)

        assert result.is_failure
        assert result.error is not None
        assert (
            result.error is not None
            and "Protobuf to dict conversion failed" in result.error
        )

    def test_serialize_protobuf_valid(self) -> None:
        """Test protobuf serialization with valid message."""
        mock_message = MagicMock(spec=ProtobufMessage)
        mock_serialized = b"serialized_data"
        mock_message.SerializeToString.return_value = mock_serialized

        result = self.utilities.ProtobufConversion.serialize_message(mock_message)

        assert result.is_success
        assert result.data == mock_serialized

    def test_serialize_protobuf_invalid_message(self) -> None:
        """Test protobuf serialization with invalid message."""
        mock_message = MagicMock(spec=ProtobufMessage)
        mock_message.SerializeToString.side_effect = Exception("Serialization error")

        result = self.utilities.ProtobufConversion.serialize_message(mock_message)

        assert result.is_failure
        assert result.error is not None
        assert (
            result.error is not None and "Message serialization failed" in result.error
        )


class TestChannelManagement:
    """Test the ChannelManagement nested class."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.utilities = FlextGrpcUtilities()

    def test_create_secure_channel_valid(self) -> None:
        """Test creating secure channel with valid parameters."""
        target = "localhost:50051"

        with patch("grpc.secure_channel") as mock_secure_channel:
            mock_channel = MagicMock()
            mock_secure_channel.return_value = mock_channel

            result = self.utilities.ChannelManagement.create_secure_channel(target)

        assert result.is_success
        assert result.data == mock_channel

    def test_create_insecure_channel_valid(self) -> None:
        """Test creating insecure channel with valid parameters."""
        target = "localhost:50051"

        with patch("grpc.insecure_channel") as mock_insecure_channel:
            mock_channel = MagicMock()
            mock_insecure_channel.return_value = mock_channel

            result = self.utilities.ChannelManagement.create_insecure_channel(target)

        assert result.is_success
        assert result.data == mock_channel

    def test_check_channel_connectivity_valid(self) -> None:
        """Test checking channel connectivity with valid channel."""
        mock_channel = MagicMock()

        with patch("grpc.channel_ready_future") as mock_ready_future:
            mock_future = MagicMock()
            mock_future.result.return_value = None  # No exception means ready
            mock_ready_future.return_value = mock_future

            result = self.utilities.ChannelManagement.check_channel_connectivity(
                mock_channel
            )

        assert result.is_success
        assert result.data is True

    def test_check_channel_connectivity_invalid_channel(self) -> None:
        """Test checking channel connectivity with invalid channel."""
        mock_channel = MagicMock()
        mock_channel.close.side_effect = Exception("Channel error")

        with patch("grpc.channel_ready_future", side_effect=Exception("Channel error")):
            result = self.utilities.ChannelManagement.check_channel_connectivity(
                mock_channel
            )

        assert result.is_failure
        assert result.error is not None
        assert (
            result.error is not None
            and "Channel connectivity check failed" in result.error
        )

    def test_close_channel_valid(self) -> None:
        """Test closing channel with valid channel."""
        mock_channel = MagicMock()

        result = self.utilities.ChannelManagement.close_channel(mock_channel)

        assert result.is_success
        mock_channel.close.assert_called_once()

    def test_close_channel_invalid_channel(self) -> None:
        """Test closing channel with invalid channel."""
        mock_channel = MagicMock()
        mock_channel.close.side_effect = Exception("Channel error")

        result = self.utilities.ChannelManagement.close_channel(mock_channel)

        assert result.is_failure
        assert result.error is not None
        assert result.error is not None and "Channel closure failed" in result.error


class TestStreamingHelpers:
    """Test the StreamingHelpers nested class."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.utilities = FlextGrpcUtilities()

    def test_create_request_stream_valid(self) -> None:
        """Test creating request stream with valid data."""
        stream_data = [{"message": "test1"}, {"message": "test2"}]

        iterator = self.utilities.StreamingHelpers.create_request_stream(stream_data)

        assert iterator is not None
        # Test that we can iterate through it
        items: list[FlextTypes.StringDict] = list(iterator)
        assert len(items) == 2

    def test_create_request_stream_empty(self) -> None:
        """Test creating request stream with empty data."""
        iterator: Iterator[object] = (
            self.utilities.StreamingHelpers.create_request_stream([])
        )

        assert iterator is not None
        items: FlextTypes.List = list(iterator)
        assert len(items) == 0

    def test_validate_stream_metadata_valid(self) -> None:
        """Test validating stream metadata with valid data."""
        mock_metadata = MagicMock()

        def mock_iter(_self: object) -> Iterator[tuple[str, str]]:
            return iter([
                ("key1", "value1"),
                ("key2", "value2"),
            ])

        mock_metadata.__iter__ = mock_iter

        result = self.utilities.StreamingHelpers.validate_stream_metadata(mock_metadata)

        assert result.is_success
        assert isinstance(result.data, dict)
        assert "key1" in result.data
        assert "key2" in result.data


class TestServiceDiscovery:
    """Test the ServiceDiscovery nested class."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.utilities = FlextGrpcUtilities()

    def test_discover_services_valid(self) -> None:
        """Test service discovery with valid channel."""
        mock_channel = MagicMock()

        result = self.utilities.ServiceDiscovery.discover_services(mock_channel)

        assert result.is_success
        assert isinstance(result.data, list)

    def test_discover_services_invalid_channel(self) -> None:
        """Test service discovery with invalid channel."""
        mock_channel = MagicMock()
        # Simulate channel that raises exception when accessed

        def mock_bool(_self: object) -> bool:
            return False

        mock_channel.__bool__ = mock_bool

        result = self.utilities.ServiceDiscovery.discover_services(mock_channel)

        assert result.is_failure
        assert result.error is not None
        assert result.error is not None and "Invalid channel provided" in result.error


class TestErrorHandling:
    """Test the ErrorHandling nested class."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.utilities = FlextGrpcUtilities()

    def test_handle_grpc_error_connection_error(self) -> None:
        """Test handling gRPC connection error."""
        error = MagicMock(spec=grpc.RpcError)
        error.code = MagicMock(return_value=grpc.StatusCode.UNAVAILABLE)
        error.details = MagicMock(return_value="Connection failed")

        result = self.utilities.ErrorHandling.handle_grpc_error(error)

        assert result.is_success
        assert isinstance(result.data, dict)
        assert "code" in result.data
        assert "details" in result.data

    def test_handle_grpc_error_unknown_error(self) -> None:
        """Test handling unknown gRPC error."""
        error = MagicMock(spec=grpc.RpcError)
        error.code = MagicMock(return_value=grpc.StatusCode.UNKNOWN)
        error.details = MagicMock(return_value="Unknown error")

        result = self.utilities.ErrorHandling.handle_grpc_error(error)

        assert result.is_success
        assert isinstance(result.data, dict)
        assert "code" in result.data
        assert "details" in result.data

    def test_is_retryable_error_retryable(self) -> None:
        """Test checking retryable error."""
        error = MagicMock(spec=grpc.RpcError)
        error.code = MagicMock(return_value=grpc.StatusCode.UNAVAILABLE)

        result = self.utilities.ErrorHandling.is_retryable_error(error)

        assert result.is_success
        assert result.data is True

    def test_is_retryable_error_not_retryable(self) -> None:
        """Test checking non-retryable error."""
        error = MagicMock(spec=grpc.RpcError)
        error.code = MagicMock(return_value=grpc.StatusCode.INVALID_ARGUMENT)

        result = self.utilities.ErrorHandling.is_retryable_error(error)

        assert result.is_success
        assert result.data is False


class TestMetricsCollection:
    """Test the MetricsCollection nested class."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.utilities = FlextGrpcUtilities()

    def test_collect_stream_metrics_valid(self) -> None:
        """Test collecting stream metrics with valid stream info."""
        stream_info = FlextGrpcModels.StreamInfo(
            stream_id="test-stream",
            stream_type="unary",
            target="localhost:50051",
            created_at=datetime.now(UTC),  # Ensure timezone-aware datetime
            total_requests_sent=100,
            error_count=5,
            average_latency_ms=50.0,
        )

        result = self.utilities.MetricsCollection.collect_stream_metrics(stream_info)

        assert result.is_success
        assert isinstance(result.data, FlextGrpcModels.StreamMetrics)
        assert result.data.stream_id == "test-stream"

    def test_collect_service_metrics_valid(self) -> None:
        """Test collecting service metrics with valid data."""
        result = self.utilities.MetricsCollection.collect_service_metrics(
            service_name="test-service",
            request_count=1000,
            error_count=50,
            avg_response_time=0.1,
        )

        assert result.is_success
        assert isinstance(result.data, FlextGrpcModels.ServiceMetrics)
        assert result.data.service_name == "test-service"
        assert result.data.total_requests == 1000
        assert result.data.failed_requests == 50
