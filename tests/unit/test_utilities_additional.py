"""Additional tests for flext_grpc.utilities module.

Tests additional functionality to improve coverage.
"""

from __future__ import annotations

from collections.abc import Iterator
from unittest.mock import MagicMock, patch

import grpc

from flext_core import FlextTypes
from flext_grpc.utilities import FlextGrpcUtilities


class TestFlextGrpcUtilitiesAdditional:
    """Additional tests for FlextGrpcUtilities to improve coverage."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.utilities = FlextGrpcUtilities()

    def test_message_validation_validate_protobuf_message_descriptor_none(self) -> None:
        """Test MessageValidation.validate_protobuf_message with None descriptor."""
        mock_message = MagicMock()
        mock_message.DESCRIPTOR = None

        result = self.utilities.MessageValidation.validate_protobuf_message(
            mock_message
        )

        assert result.is_success is False
        assert result.error is not None and "Message descriptor is None" in result.error

    def test_message_validation_validate_protobuf_message_no_descriptor(self) -> None:
        """Test MessageValidation.validate_protobuf_message with no DESCRIPTOR attribute."""
        mock_message = MagicMock(spec=[])
        # No DESCRIPTOR attribute

        result = self.utilities.MessageValidation.validate_protobuf_message(
            mock_message
        )

        assert result.is_success is False
        assert (
            result.error is not None
            and "Message descriptor not available" in result.error
        )

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
        assert (
            result.error is not None and "Message serialization failed" in result.error
        )

    def test_message_validation_validate_protobuf_message_validation_failure(
        self,
    ) -> None:
        """Test MessageValidation.validate_protobuf_message with validation failure."""
        mock_message = MagicMock()
        mock_message.DESCRIPTOR = MagicMock()
        mock_message.DESCRIPTOR.fields = []
        mock_message.HasField.return_value = True
        mock_message.SerializeToString.side_effect = Exception("Validation failed")

        result = self.utilities.MessageValidation.validate_protobuf_message(
            mock_message
        )

        assert result.is_success is False
        assert result.error is not None and "Message validation failed" in result.error

    def test_protobuf_conversion_protobuf_to_dict_success(self) -> None:
        """Test ProtobufConversion.protobuf_to_dict with successful conversion."""
        mock_message = MagicMock()
        mock_dict = {"message": "test", "timestamp": 1234567890}

        with patch("json_format.MessageToDict", return_value=mock_dict):
            result = self.utilities.ProtobufConversion.protobuf_to_dict(mock_message)

        assert result.is_success
        assert result.data == mock_dict

    def test_protobuf_conversion_protobuf_to_dict_failure(self) -> None:
        """Test ProtobufConversion.protobuf_to_dict with conversion failure."""
        mock_message = MagicMock()

        with patch(
            "json_format.MessageToDict", side_effect=Exception("Conversion failed")
        ):
            result = self.utilities.ProtobufConversion.protobuf_to_dict(mock_message)

        assert result.is_success is False
        assert (
            result.error is not None
            and "Failed to convert protobuf to dict" in result.error
        )

    def test_protobuf_conversion_serialize_protobuf_success(self) -> None:
        """Test ProtobufConversion.serialize_protobuf with successful serialization."""
        mock_message = MagicMock()
        mock_serialized = b"serialized_data"
        mock_message.SerializeToString.return_value = mock_serialized

        result = self.utilities.ProtobufConversion.serialize_protobuf(mock_message)

        assert result.is_success
        assert result.data == mock_serialized

    def test_protobuf_conversion_serialize_protobuf_failure(self) -> None:
        """Test ProtobufConversion.serialize_protobuf with serialization failure."""
        mock_message = MagicMock()
        mock_message.SerializeToString.side_effect = Exception("Serialization failed")

        result = self.utilities.ProtobufConversion.serialize_protobuf(mock_message)

        assert result.is_success is False
        assert (
            result.error is not None
            and "Failed to serialize protobuf message" in result.error
        )

    def test_channel_management_get_channel_state_success(self) -> None:
        """Test ChannelManagement.get_channel_state with successful state retrieval."""
        mock_channel = MagicMock()
        mock_channel.get_state.return_value = grpc.ChannelConnectivity.READY

        result = self.utilities.ChannelManagement.get_channel_state(mock_channel)

        assert result.is_success
        assert result.data == grpc.ChannelConnectivity.READY

    def test_channel_management_close_channel_success(self) -> None:
        """Test ChannelManagement.close_channel with successful channel closure."""
        mock_channel = MagicMock()

        result = self.utilities.ChannelManagement.close_channel(mock_channel)

        assert result.is_success
        mock_channel.close.assert_called_once()

    def test_channel_management_close_channel_failure(self) -> None:
        """Test ChannelManagement.close_channel with closure failure."""
        mock_channel = MagicMock()
        mock_channel.close.side_effect = Exception("Close failed")

        result = self.utilities.ChannelManagement.close_channel(mock_channel)

        assert result.is_success is False
        assert result.error is not None and "Channel closure failed" in result.error

    def test_streaming_helpers_validate_stream_request_valid(self) -> None:
        """Test StreamingHelpers.validate_stream_request with valid request."""
        request_data = {"method": "TestMethod", "data": "test_data"}

        result = self.utilities.StreamingHelpers.validate_stream_request(request_data)

        assert result.is_success
        assert result.data is True

    def test_streaming_helpers_validate_stream_request_invalid(self) -> None:
        """Test StreamingHelpers.validate_stream_request with invalid request."""
        request_data = {}  # Missing required fields

        result = self.utilities.StreamingHelpers.validate_stream_request(request_data)

        assert result.is_success is False
        assert result.error is not None and "method" in result.error

    def test_service_discovery_discover_services_failure(self) -> None:
        """Test ServiceDiscovery.discover_services with discovery failure."""
        target = "invalid-target"

        with patch("grpc.insecure_channel", side_effect=Exception("Connection failed")):
            result = self.utilities.ServiceDiscovery.discover_services(target)

        assert result.is_success is False
        assert (
            result.error is not None and "Failed to discover services" in result.error
        )

    def test_error_handling_handle_grpc_error_connection_error(self) -> None:
        """Test ErrorHandling.handle_grpc_error with connection error."""
        error = grpc.RpcError()
        error.code = lambda: grpc.StatusCode.UNAVAILABLE
        error.details = lambda: "Connection failed"

        result = self.utilities.ErrorHandling.handle_grpc_error(error)

        assert result.is_success is False
        assert result.error is not None and "Connection error" in result.error

    def test_error_handling_handle_grpc_error_unknown_error(self) -> None:
        """Test ErrorHandling.handle_grpc_error with unknown error."""
        error = grpc.RpcError()
        error.code = lambda: grpc.StatusCode.UNKNOWN
        error.details = lambda: "Unknown error"

        result = self.utilities.ErrorHandling.handle_grpc_error(error)

        assert result.is_success is False
        assert result.error is not None and "Unknown error" in result.error

    def test_metrics_collection_collect_channel_metrics_success(self) -> None:
        """Test MetricsCollection.collect_channel_metrics with successful collection."""
        mock_channel = MagicMock()
        mock_channel.get_state.return_value = grpc.ChannelConnectivity.READY

        result = self.utilities.MetricsCollection.collect_channel_metrics(mock_channel)

        assert result.is_success
        assert isinstance(result.data, dict)
        assert "state" in result.data

    def test_metrics_collection_collect_channel_metrics_failure(self) -> None:
        """Test MetricsCollection.collect_channel_metrics with collection failure."""
        mock_channel = MagicMock()
        mock_channel.get_state.side_effect = Exception("Metrics collection failed")

        result = self.utilities.MetricsCollection.collect_channel_metrics(mock_channel)

        assert result.is_success is False
        assert (
            result.error is not None
            and "Failed to collect channel metrics" in result.error
        )

    def test_metrics_collection_collect_performance_metrics_invalid_start_time(
        self,
    ) -> None:
        """Test MetricsCollection.collect_performance_metrics with invalid start time."""
        result = self.utilities.MetricsCollection.collect_performance_metrics(
            None, 1001.0
        )

        assert result.is_success is False
        assert result.error is not None and "Invalid time parameters" in result.error

    def test_metrics_collection_collect_performance_metrics_invalid_end_time(
        self,
    ) -> None:
        """Test MetricsCollection.collect_performance_metrics with invalid end time."""
        result = self.utilities.MetricsCollection.collect_performance_metrics(
            1000.0, None
        )

        assert result.is_success is False
        assert result.error is not None and "Invalid time parameters" in result.error

    def test_metrics_collection_collect_performance_metrics_negative_duration(
        self,
    ) -> None:
        """Test MetricsCollection.collect_performance_metrics with negative duration."""
        result = self.utilities.MetricsCollection.collect_performance_metrics(
            1001.0,
            1000.0,  # End time before start time
        )

        assert result.is_success is False
        assert result.error is not None and "Invalid time parameters" in result.error

    def test_streaming_helpers_create_stream_iterator_with_error(self) -> None:
        """Test StreamingHelpers.create_stream_iterator with iterator error."""

        def error_stream_data() -> Iterator[FlextTypes.StringDict]:
            yield {"message": "test1"}
            error_msg = "Iterator error"
            raise RuntimeError(error_msg)

        result = self.utilities.StreamingHelpers.create_stream_iterator(
            error_stream_data()
        )

        assert result.is_success is False
        assert (
            result.error is not None
            and "Failed to create stream iterator" in result.error
        )

    def test_message_validation_validate_stream_message_sequence_with_validation_error(
        self,
    ) -> None:
        """Test MessageValidation.validate_stream_message_sequence with validation error."""
        mock_msg = MagicMock()
        mock_msg.DESCRIPTOR = MagicMock()
        mock_msg.DESCRIPTOR.fields = []
        mock_msg.HasField.return_value = True
        mock_msg.SerializeToString.side_effect = Exception("Validation failed")

        messages = [mock_msg]

        result = self.utilities.MessageValidation.validate_stream_message_sequence(
            messages
        )

        assert result.is_success is False
        assert (
            result.error is not None and "Message 0 validation failed" in result.error
        )

    def test_message_validation_validate_stream_message_sequence_with_order_validation(
        self,
    ) -> None:
        """Test MessageValidation.validate_stream_message_sequence with order validation."""
        mock_msg1 = MagicMock()
        mock_msg1.DESCRIPTOR = MagicMock()
        mock_msg1.DESCRIPTOR.fields = []
        mock_msg1.HasField.return_value = True
        mock_msg1.SerializeToString.return_value = b"serialized"
        mock_msg1.GetField.return_value = "message1"

        mock_msg2 = MagicMock()
        mock_msg2.DESCRIPTOR = MagicMock()
        mock_msg2.DESCRIPTOR.fields = []
        mock_msg2.HasField.return_value = True
        mock_msg2.SerializeToString.return_value = b"serialized"
        mock_msg2.GetField.return_value = "message2"

        messages = [mock_msg1, mock_msg2]
        expected_order = ["message1", "wrong_order"]

        result = self.utilities.MessageValidation.validate_stream_message_sequence(
            messages, expected_order
        )

        assert result.is_success is False
        assert result.error is not None and "Sequence validation failed" in result.error
