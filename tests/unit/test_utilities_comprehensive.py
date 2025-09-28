"""Comprehensive tests for flext_grpc.utilities module.

Tests additional functionality to improve coverage.
"""

from __future__ import annotations

from collections.abc import Iterator
from typing import cast
from unittest.mock import MagicMock, patch

import grpc
from google.protobuf.message import Message as ProtobufMessage

from flext_core import FlextResult
from flext_grpc.utilities import FlextGrpcUtilities


class TestFlextGrpcUtilitiesComprehensive:
    """Comprehensive tests for FlextGrpcUtilities to improve coverage."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.utilities = FlextGrpcUtilities()

    def test_utilities_initialization(self) -> None:
        """Test utilities initialization."""
        assert self.utilities is not None
        assert hasattr(self.utilities, "execute")
        assert hasattr(self.utilities, "logger")
        assert hasattr(self.utilities, "container")
        assert hasattr(self.utilities, "MessageValidation")
        assert hasattr(self.utilities, "ProtobufConversion")
        assert hasattr(self.utilities, "ChannelManagement")
        assert hasattr(self.utilities, "StreamingHelpers")
        assert hasattr(self.utilities, "ServiceDiscovery")
        assert hasattr(self.utilities, "ErrorHandling")
        assert hasattr(self.utilities, "MetricsCollection")

    def test_message_validation_validate_protobuf_message_success(self) -> None:
        """Test MessageValidation.validate_protobuf_message with success."""
        mock_message = MagicMock()
        mock_message.DESCRIPTOR = MagicMock()
        mock_message.DESCRIPTOR.fields = []
        mock_message.HasField.return_value = True
        mock_message.SerializeToString.return_value = b"serialized_data"

        result = self.utilities.MessageValidation.validate_protobuf_message(
            mock_message
        )

        assert result.is_success
        assert result.data is True

    def test_message_validation_validate_protobuf_message_none(self) -> None:
        """Test MessageValidation.validate_protobuf_message with None."""
        result = self.utilities.MessageValidation.validate_protobuf_message(None)

        assert result.is_success is False
        assert result.error is not None
        assert "Invalid message instance" in result.error

    def test_message_validation_validate_protobuf_message_no_descriptor(self) -> None:
        """Test MessageValidation.validate_protobuf_message with no DESCRIPTOR."""
        mock_message = MagicMock(spec=[])

        result = self.utilities.MessageValidation.validate_protobuf_message(
            mock_message
        )

        assert result.is_success is False
        assert result.error is not None
        assert "Message descriptor not available" in result.error

    def test_message_validation_validate_protobuf_message_descriptor_none(self) -> None:
        """Test MessageValidation.validate_protobuf_message with None descriptor."""
        mock_message = MagicMock()
        mock_message.DESCRIPTOR = None

        result = self.utilities.MessageValidation.validate_protobuf_message(
            mock_message
        )

        assert result.is_success is False
        assert result.error is not None
        assert "Message descriptor is None" in result.error

    def test_message_validation_validate_protobuf_message_serialization_failure(
        self,
    ) -> None:
        """Test MessageValidation.validate_protobuf_message with serialization failure."""
        mock_message = MagicMock()
        mock_message.DESCRIPTOR = MagicMock()
        mock_message.DESCRIPTOR.fields = []
        mock_message.HasField.return_value = True
        mock_message.SerializeToString.side_effect = Exception("Serialization failed")

        result = self.utilities.MessageValidation.validate_protobuf_message(
            mock_message
        )

        assert result.is_success is False
        assert result.error is not None
        assert "Message serialization failed" in result.error

    def test_message_validation_validate_protobuf_message_validation_failure(
        self,
    ) -> None:
        """Test MessageValidation.validate_protobuf_message with validation failure."""
        mock_message = MagicMock()
        mock_message.DESCRIPTOR = MagicMock()
        # Create a mock field that will cause HasField to be called
        mock_field = MagicMock()
        mock_field.label = 2  # LABEL_REQUIRED
        mock_field.name = "test_field"
        mock_message.DESCRIPTOR.fields = [mock_field]
        mock_message.HasField.return_value = False  # Field is missing
        mock_message.SerializeToString.return_value = b"serialized_data"

        result = self.utilities.MessageValidation.validate_protobuf_message(
            mock_message
        )

        assert result.is_success is False
        assert result.error is not None
        assert "Required field 'test_field' is missing" in result.error

    def test_message_validation_validate_stream_message_sequence_success(self) -> None:
        """Test MessageValidation.validate_stream_message_sequence with success."""
        mock_msg1 = MagicMock()
        mock_msg1.DESCRIPTOR = MagicMock()
        mock_msg1.DESCRIPTOR.fields = []
        mock_msg1.HasField.return_value = True
        mock_msg1.SerializeToString.return_value = b"serialized"

        mock_msg2 = MagicMock()
        mock_msg2.DESCRIPTOR = MagicMock()
        mock_msg2.DESCRIPTOR.fields = []
        mock_msg2.HasField.return_value = True
        mock_msg2.SerializeToString.return_value = b"serialized"

        messages = [
            cast("ProtobufMessage", mock_msg1),
            cast("ProtobufMessage", mock_msg2),
        ]

        result = self.utilities.MessageValidation.validate_stream_message_sequence(
            messages
        )

        assert result.is_success
        assert result.data is True

    def test_message_validation_validate_stream_message_sequence_with_order_validation(
        self,
    ) -> None:
        """Test MessageValidation.validate_stream_message_sequence with order validation."""
        mock_msg1 = MagicMock()
        mock_msg1.DESCRIPTOR = MagicMock()
        mock_msg1.DESCRIPTOR.fields = []
        mock_msg1.DESCRIPTOR.name = "message1"
        mock_msg1.HasField.return_value = True
        mock_msg1.SerializeToString.return_value = b"serialized"
        mock_msg1.GetField.return_value = "message1"

        mock_msg2 = MagicMock()
        mock_msg2.DESCRIPTOR = MagicMock()
        mock_msg2.DESCRIPTOR.fields = []
        mock_msg2.DESCRIPTOR.name = "message2"
        mock_msg2.HasField.return_value = True
        mock_msg2.SerializeToString.return_value = b"serialized"
        mock_msg2.GetField.return_value = "message2"

        messages = [
            cast("ProtobufMessage", mock_msg1),
            cast("ProtobufMessage", mock_msg2),
        ]
        expected_order = ["message1", "message2"]

        result = self.utilities.MessageValidation.validate_stream_message_sequence(
            messages, expected_order
        )

        assert result.is_success
        assert result.data is True

    def test_message_validation_validate_stream_message_sequence_with_validation_error(
        self,
    ) -> None:
        """Test MessageValidation.validate_stream_message_sequence with validation error."""
        mock_msg = MagicMock()
        mock_msg.DESCRIPTOR = MagicMock()
        mock_msg.DESCRIPTOR.fields = []
        mock_msg.HasField.return_value = True
        mock_msg.SerializeToString.side_effect = Exception("Validation failed")

        messages = [cast("ProtobufMessage", mock_msg)]

        result = self.utilities.MessageValidation.validate_stream_message_sequence(
            messages
        )

        assert result.is_success is False
        assert result.error is not None
        assert "Message 0 validation failed" in result.error

    def test_protobuf_conversion_dict_to_protobuf_success(self) -> None:
        """Test ProtobufConversion.dict_to_protobuf with success."""
        data_dict = {"message": "test", "timestamp": 1234567890}
        mock_message_class = MagicMock()
        mock_instance = MagicMock()
        mock_message_class.return_value = mock_instance

        # Mock the json_format.ParseDict to not raise an exception
        with patch("google.protobuf.json_format.ParseDict") as mock_parse:
            mock_parse.return_value = None  # ParseDict doesn't return anything

            result = self.utilities.ProtobufConversion.dict_to_protobuf(
                data_dict, cast("type[ProtobufMessage]", mock_message_class)
            )

        assert result.is_success
        assert result.data == mock_instance

    def test_protobuf_conversion_dict_to_protobuf_failure(self) -> None:
        """Test ProtobufConversion.dict_to_protobuf with failure."""
        data_dict = {"message": "test", "timestamp": 1234567890}
        mock_message_class = MagicMock()
        mock_message_class.side_effect = Exception("Conversion failed")

        result = self.utilities.ProtobufConversion.dict_to_protobuf(
            data_dict, cast("type[ProtobufMessage]", mock_message_class)
        )

        assert result.is_success is False
        assert result.error is not None
        assert "Dict to protobuf conversion failed" in result.error

    def test_protobuf_conversion_protobuf_to_dict_success(self) -> None:
        """Test ProtobufConversion.protobuf_to_dict with success."""
        mock_message = MagicMock()
        mock_dict = {"message": "test", "timestamp": 1234567890}

        with patch("google.protobuf.json_format.MessageToDict", return_value=mock_dict):
            result = self.utilities.ProtobufConversion.protobuf_to_dict(mock_message)

        assert result.is_success
        assert result.data == mock_dict

    def test_protobuf_conversion_protobuf_to_dict_failure(self) -> None:
        """Test ProtobufConversion.protobuf_to_dict with failure."""
        mock_message = MagicMock()

        with patch(
            "google.protobuf.json_format.MessageToDict",
            side_effect=Exception("Conversion failed"),
        ):
            result = self.utilities.ProtobufConversion.protobuf_to_dict(mock_message)

        assert result.is_success is False
        assert result.error is not None
        assert "Protobuf to dict conversion failed" in result.error

    def test_protobuf_conversion_serialize_message_success(self) -> None:
        """Test ProtobufConversion.serialize_message with success."""
        mock_message = MagicMock()
        mock_serialized = b"serialized_data"
        mock_message.SerializeToString.return_value = mock_serialized

        result = self.utilities.ProtobufConversion.serialize_message(mock_message)

        assert result.is_success
        assert result.data == mock_serialized

    def test_protobuf_conversion_serialize_message_failure(self) -> None:
        """Test ProtobufConversion.serialize_message with failure."""
        mock_message = MagicMock()
        mock_message.SerializeToString.side_effect = Exception("Serialization failed")

        result = self.utilities.ProtobufConversion.serialize_message(mock_message)

        assert result.is_success is False
        assert result.error is not None
        assert "Message serialization failed" in result.error

    def test_channel_management_get_channel_state_success(self) -> None:
        """Test ChannelManagement.get_channel_state with success."""
        mock_channel = MagicMock()

        result: FlextResult[str] = self.utilities.ChannelManagement.get_channel_state(
            mock_channel
        )

        assert result.is_success
        assert result.data == "READY"

    def test_channel_management_get_channel_state_failure(self) -> None:
        """Test ChannelManagement.get_channel_state with failure."""
        mock_channel = None  # Test with None channel

        result: FlextResult[str] = self.utilities.ChannelManagement.get_channel_state(
            mock_channel
        )

        assert result.is_success is False
        assert result.error is not None
        assert "Channel is None" in result.error

    def test_channel_management_close_channel_success(self) -> None:
        """Test ChannelManagement.close_channel with success."""
        mock_channel = MagicMock()

        result = self.utilities.ChannelManagement.close_channel(mock_channel)

        assert result.is_success
        mock_channel.close.assert_called_once()

    def test_channel_management_close_channel_failure(self) -> None:
        """Test ChannelManagement.close_channel with failure."""
        mock_channel = MagicMock()
        mock_channel.close.side_effect = Exception("Close failed")

        result = self.utilities.ChannelManagement.close_channel(mock_channel)

        assert result.is_success is False
        assert result.error is not None
        assert "Channel closure failed" in result.error

    def test_streaming_helpers_create_stream_iterator_success(self) -> None:
        """Test StreamingHelpers.create_stream_iterator with success."""
        test_data = [{"message": "test1"}, {"message": "test2"}]

        result: FlextResult[Iterator[dict[str, str]]] = (
            self.utilities.StreamingHelpers.create_stream_iterator(test_data)
        )

        assert result.is_success
        assert result.data is not None
        # Test that we can iterate over the result
        items = list(result.data)
        assert len(items) == 2
        assert items[0] == {"message": "test1"}
        assert items[1] == {"message": "test2"}

    def test_streaming_helpers_create_stream_iterator_failure(self) -> None:
        """Test StreamingHelpers.create_stream_iterator with failure."""
        # Test with invalid data that might cause issues
        invalid_data = [object()]  # Non-serializable object

        result: FlextResult[Iterator[object]] = (
            self.utilities.StreamingHelpers.create_stream_iterator(invalid_data)
        )

        # This should still succeed as the method just creates an iterator
        assert result.is_success
        assert result.data is not None

    def test_service_discovery_discover_services_success(self) -> None:
        """Test ServiceDiscovery.discover_services with success."""
        mock_channel = MagicMock()

        result = self.utilities.ServiceDiscovery.discover_services(mock_channel)

        assert result.is_success
        assert isinstance(result.data, list)
        assert "grpc.reflection.v1alpha.ServerReflection" in result.data

    def test_service_discovery_discover_services_failure(self) -> None:
        """Test ServiceDiscovery.discover_services with failure."""
        # Create a mock channel that will be treated as None
        mock_channel = MagicMock()
        # Mock the channel to be falsy when checked
        mock_channel.__bool__ = lambda _: False

        result = self.utilities.ServiceDiscovery.discover_services(mock_channel)

        # The method should fail because the channel is treated as None
        assert result.is_success is False
        assert result.error is not None
        assert "Invalid channel provided" in result.error

    def test_error_handling_handle_grpc_error_success(self) -> None:
        """Test ErrorHandling.handle_grpc_error with success."""
        error = MagicMock()
        error.code = MagicMock(return_value=grpc.StatusCode.OK)
        error.details = MagicMock(return_value="Success")

        result = self.utilities.ErrorHandling.handle_grpc_error(error)

        assert result.is_success
        assert isinstance(result.data, dict)
        assert "code" in result.data

    def test_error_handling_handle_grpc_error_connection_error(self) -> None:
        """Test ErrorHandling.handle_grpc_error with connection error."""
        error = MagicMock()
        error.code = MagicMock(return_value=grpc.StatusCode.UNAVAILABLE)
        error.details = MagicMock(return_value="Connection failed")

        result = self.utilities.ErrorHandling.handle_grpc_error(error)

        assert result.is_success
        assert isinstance(result.data, dict)
        assert "code" in result.data

    def test_error_handling_handle_grpc_error_unknown_error(self) -> None:
        """Test ErrorHandling.handle_grpc_error with unknown error."""
        error = MagicMock()
        error.code = MagicMock(return_value=grpc.StatusCode.UNKNOWN)
        error.details = MagicMock(return_value="Unknown error")

        result = self.utilities.ErrorHandling.handle_grpc_error(error)

        assert result.is_success
        assert isinstance(result.data, dict)
        assert "code" in result.data

    def test_error_handling_format_error_message_success(self) -> None:
        """Test ErrorHandling.format_error_message with success."""
        error_msg = "Test error message"

        result: FlextResult[str] = self.utilities.ErrorHandling.format_error_message(
            error_msg
        )

        assert result.is_success
        assert "Error: Test error message" in result.data

    def test_error_handling_format_error_message_none(self) -> None:
        """Test ErrorHandling.format_error_message with None."""
        result: FlextResult[str] = self.utilities.ErrorHandling.format_error_message(
            None
        )

        assert result.is_success
        assert "Unknown error" in result.data

    def test_metrics_collection_collect_channel_metrics_success(self) -> None:
        """Test MetricsCollection.collect_channel_metrics with success."""
        mock_channel = MagicMock()

        result: FlextResult[dict[str, str]] = (
            self.utilities.MetricsCollection.collect_channel_metrics(mock_channel)
        )

        assert result.is_success
        assert isinstance(result.data, dict)
        assert "channel_state" in result.data

    def test_metrics_collection_collect_channel_metrics_failure(self) -> None:
        """Test MetricsCollection.collect_channel_metrics with failure."""
        mock_channel = None  # Test with None channel

        result: FlextResult[dict[str, str]] = (
            self.utilities.MetricsCollection.collect_channel_metrics(mock_channel)
        )

        assert result.is_success is False
        assert result.error is not None
        assert "Channel is None" in result.error

    def test_metrics_collection_collect_performance_metrics_success(self) -> None:
        """Test MetricsCollection.collect_performance_metrics with success."""
        start_time = 1000.0
        end_time = 1001.0

        result: FlextResult[dict[str, float]] = (
            self.utilities.MetricsCollection.collect_performance_metrics(
                start_time, end_time
            )
        )

        assert result.is_success
        assert isinstance(result.data, dict)
        assert "duration_ms" in result.data

    def test_metrics_collection_collect_performance_metrics_invalid_start_time(
        self,
    ) -> None:
        """Test MetricsCollection.collect_performance_metrics with invalid start time."""
        result: FlextResult[dict[str, float]] = (
            self.utilities.MetricsCollection.collect_performance_metrics(None, 1001.0)
        )

        assert result.is_success is False
        assert result.error is not None
        assert "Invalid time parameters" in result.error

    def test_metrics_collection_collect_performance_metrics_invalid_end_time(
        self,
    ) -> None:
        """Test MetricsCollection.collect_performance_metrics with invalid end time."""
        result: FlextResult[dict[str, float]] = (
            self.utilities.MetricsCollection.collect_performance_metrics(1000.0, None)
        )

        assert result.is_success is False
        assert result.error is not None
        assert "Invalid time parameters" in result.error

    def test_metrics_collection_collect_performance_metrics_negative_duration(
        self,
    ) -> None:
        """Test MetricsCollection.collect_performance_metrics with negative duration."""
        result: FlextResult[dict[str, float]] = (
            self.utilities.MetricsCollection.collect_performance_metrics(
                1001.0,
                1000.0,  # End time before start time
            )
        )

        # The method doesn't validate for negative duration, it just calculates it
        assert result.is_success
        assert isinstance(result.data, dict)
        assert "duration_ms" in result.data
        assert result.data["duration_ms"] == -1000.0  # Negative duration

    def test_utilities_execute_method(self) -> None:
        """Test utilities execute method."""
        result = self.utilities.execute()

        assert result.is_success
        assert isinstance(result.data, dict)
        assert "status" in result.data
        assert result.data["status"] == "operational"

    def test_utilities_properties(self) -> None:
        """Test utilities properties."""
        # Test logger property
        logger = self.utilities.logger
        assert logger is not None

        # Test container property
        container = self.utilities.container
        assert container is not None
