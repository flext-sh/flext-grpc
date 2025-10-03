"""Advanced tests for flext_grpc.utilities module.

Tests additional functionality to improve coverage.
"""

from __future__ import annotations

from collections.abc import Iterator
from unittest.mock import MagicMock, patch

import grpc

from flext_core import FlextTypes
from flext_grpc.utilities import FlextGrpcUtilities


class TestFlextGrpcUtilitiesAdvanced:
    """Advanced tests for FlextGrpcUtilities to improve coverage."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.utilities = FlextGrpcUtilities()

    def test_message_validation_validate_protobuf_message_with_field_validation_error(
        self,
    ) -> None:
        """Test MessageValidation.validate_protobuf_message with field validation error."""
        mock_message = MagicMock()
        mock_message.DESCRIPTOR = MagicMock()
        mock_message.DESCRIPTOR.fields = [MagicMock()]
        mock_message.HasField.return_value = False  # Field validation fails
        mock_message.SerializeToString.return_value = b"serialized_data"

        result = self.utilities.MessageValidation.validate_protobuf_message(
            mock_message
        )

        assert result.is_success is False
        assert result.error is not None and "Message validation failed" in result.error

    def test_message_validation_validate_protobuf_message_with_descriptor_fields_error(
        self,
    ) -> None:
        """Test MessageValidation.validate_protobuf_message with descriptor fields error."""
        mock_message = MagicMock()
        mock_message.DESCRIPTOR = MagicMock()
        mock_message.DESCRIPTOR.fields = [MagicMock()]
        mock_message.HasField.side_effect = Exception("Field validation error")

        result = self.utilities.MessageValidation.validate_protobuf_message(
            mock_message
        )

        assert result.is_success is False
        assert result.error is not None and "Message validation failed" in result.error

    def test_message_validation_validate_stream_message_sequence_with_empty_messages(
        self,
    ) -> None:
        """Test MessageValidation.validate_stream_message_sequence with empty messages."""
        result = self.utilities.MessageValidation.validate_stream_message_sequence([])

        assert result.is_success is True
        assert result.data is True

    def test_message_validation_validate_stream_message_sequence_with_none_messages(
        self,
    ) -> None:
        """Test MessageValidation.validate_stream_message_sequence with None messages."""
        result = self.utilities.MessageValidation.validate_stream_message_sequence(None)

        assert result.is_success is False
        assert result.error is not None and "Messages list is None" in result.error

    def test_message_validation_validate_stream_message_sequence_with_invalid_message_type(
        self,
    ) -> None:
        """Test MessageValidation.validate_stream_message_sequence with invalid message type."""
        result = self.utilities.MessageValidation.validate_stream_message_sequence([
            "invalid_message"
        ])

        assert result.is_success is False
        assert result.error is not None and "Invalid message type" in result.error

    def test_message_validation_validate_stream_message_sequence_with_order_mismatch(
        self,
    ) -> None:
        """Test MessageValidation.validate_stream_message_sequence with order mismatch."""
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
        expected_order = ["message2", "message1"]  # Wrong order

        result = self.utilities.MessageValidation.validate_stream_message_sequence(
            messages, expected_order
        )

        assert result.is_success is False
        assert result.error is not None and "Message order mismatch" in result.error

    def test_protobuf_conversion_dict_to_protobuf_with_none_dict(self) -> None:
        """Test ProtobufConversion.dict_to_protobuf with None dict."""
        result = self.utilities.ProtobufConversion.dict_to_protobuf(None, MagicMock())

        assert result.is_success is False
        assert result.error is not None and "Data dictionary is None" in result.error

    def test_protobuf_conversion_dict_to_protobuf_with_none_message_class(self) -> None:
        """Test ProtobufConversion.dict_to_protobuf with None message class."""
        result = self.utilities.ProtobufConversion.dict_to_protobuf(
            {"key": "value"}, None
        )

        assert result.is_success is False
        assert result.error is not None and "Message class is None" in result.error

    def test_protobuf_conversion_dict_to_protobuf_with_invalid_dict_type(self) -> None:
        """Test ProtobufConversion.dict_to_protobuf with invalid dict type."""
        result = self.utilities.ProtobufConversion.dict_to_protobuf(
            "invalid_dict", MagicMock()
        )

        assert result.is_success is False
        assert result.error is not None and "Data must be a dictionary" in result.error

    def test_protobuf_conversion_dict_to_protobuf_with_invalid_message_class_type(
        self,
    ) -> None:
        """Test ProtobufConversion.dict_to_protobuf with invalid message class type."""
        result = self.utilities.ProtobufConversion.dict_to_protobuf(
            {"key": "value"}, "invalid_class"
        )

        assert result.is_success is False
        assert (
            result.error is not None
            and "Message class must be callable" in result.error
        )

    def test_protobuf_conversion_protobuf_to_dict_with_none_message(self) -> None:
        """Test ProtobufConversion.protobuf_to_dict with None message."""
        result = self.utilities.ProtobufConversion.protobuf_to_dict(None)

        assert result.is_success is False
        assert result.error is not None and "Protobuf message is None" in result.error

    def test_protobuf_conversion_protobuf_to_dict_with_invalid_message_type(
        self,
    ) -> None:
        """Test ProtobufConversion.protobuf_to_dict with invalid message type."""
        result = self.utilities.ProtobufConversion.protobuf_to_dict("invalid_message")

        assert result.is_success is False
        assert (
            result.error is not None and "Invalid protobuf message type" in result.error
        )

    def test_protobuf_conversion_serialize_protobuf_with_none_message(self) -> None:
        """Test ProtobufConversion.serialize_protobuf with None message."""
        result = self.utilities.ProtobufConversion.serialize_protobuf(None)

        assert result.is_success is False
        assert result.error is not None and "Protobuf message is None" in result.error

    def test_protobuf_conversion_serialize_protobuf_with_invalid_message_type(
        self,
    ) -> None:
        """Test ProtobufConversion.serialize_protobuf with invalid message type."""
        result = self.utilities.ProtobufConversion.serialize_protobuf("invalid_message")

        assert result.is_success is False
        assert (
            result.error is not None and "Invalid protobuf message type" in result.error
        )

    def test_channel_management_get_channel_state_with_none_channel(self) -> None:
        """Test ChannelManagement.get_channel_state with None channel."""
        result = self.utilities.ChannelManagement.get_channel_state(None)

        assert result.is_success is False
        assert result.error is not None and "Channel is None" in result.error

    def test_channel_management_get_channel_state_with_invalid_channel_type(
        self,
    ) -> None:
        """Test ChannelManagement.get_channel_state with invalid channel type."""
        result = self.utilities.ChannelManagement.get_channel_state("invalid_channel")

        assert result.is_success is False
        assert result.error is not None and "Invalid channel type" in result.error

    def test_channel_management_close_channel_with_none_channel(self) -> None:
        """Test ChannelManagement.close_channel with None channel."""
        result = self.utilities.ChannelManagement.close_channel(None)

        assert result.is_success is False
        assert result.error is not None and "Channel is None" in result.error

    def test_channel_management_close_channel_with_invalid_channel_type(self) -> None:
        """Test ChannelManagement.close_channel with invalid channel type."""
        result = self.utilities.ChannelManagement.close_channel("invalid_channel")

        assert result.is_success is False
        assert result.error is not None and "Invalid channel type" in result.error

    def test_streaming_helpers_validate_stream_request_with_none_request(self) -> None:
        """Test StreamingHelpers.validate_stream_request with None request."""
        result = self.utilities.StreamingHelpers.validate_stream_request(None)

        assert result.is_success is False
        assert result.error is not None and "Request data is None" in result.error

    def test_streaming_helpers_validate_stream_request_with_invalid_request_type(
        self,
    ) -> None:
        """Test StreamingHelpers.validate_stream_request with invalid request type."""
        result = self.utilities.StreamingHelpers.validate_stream_request(
            "invalid_request"
        )

        assert result.is_success is False
        assert (
            result.error is not None
            and "Request data must be a dictionary" in result.error
        )

    def test_streaming_helpers_validate_stream_request_with_missing_method_field(
        self,
    ) -> None:
        """Test StreamingHelpers.validate_stream_request with missing method field."""
        request_data = {"data": "test_data"}  # Missing method field

        result = self.utilities.StreamingHelpers.validate_stream_request(request_data)

        assert result.is_success is False
        assert result.error is not None and "method" in result.error

    def test_streaming_helpers_validate_stream_request_with_empty_method_field(
        self,
    ) -> None:
        """Test StreamingHelpers.validate_stream_request with empty method field."""
        request_data = {"method": "", "data": "test_data"}

        result = self.utilities.StreamingHelpers.validate_stream_request(request_data)

        assert result.is_success is False
        assert result.error is not None and "Method cannot be empty" in result.error

    def test_streaming_helpers_validate_stream_request_with_whitespace_method_field(
        self,
    ) -> None:
        """Test StreamingHelpers.validate_stream_request with whitespace-only method field."""
        request_data = {"method": "   ", "data": "test_data"}

        result = self.utilities.StreamingHelpers.validate_stream_request(request_data)

        assert result.is_success is False
        assert result.error is not None and "Method cannot be empty" in result.error

    def test_streaming_helpers_validate_stream_request_with_missing_data_field(
        self,
    ) -> None:
        """Test StreamingHelpers.validate_stream_request with missing data field."""
        request_data = {"method": "TestMethod"}  # Missing data field

        result = self.utilities.StreamingHelpers.validate_stream_request(request_data)

        assert result.is_success is False
        assert result.error is not None and "data" in result.error

    def test_streaming_helpers_validate_stream_request_with_empty_data_field(
        self,
    ) -> None:
        """Test StreamingHelpers.validate_stream_request with empty data field."""
        request_data = {"method": "TestMethod", "data": ""}

        result = self.utilities.StreamingHelpers.validate_stream_request(request_data)

        assert result.is_success is False
        assert result.error is not None and "Data cannot be empty" in result.error

    def test_streaming_helpers_validate_stream_request_with_whitespace_data_field(
        self,
    ) -> None:
        """Test StreamingHelpers.validate_stream_request with whitespace-only data field."""
        request_data = {"method": "TestMethod", "data": "   "}

        result = self.utilities.StreamingHelpers.validate_stream_request(request_data)

        assert result.is_success is False
        assert result.error is not None and "Data cannot be empty" in result.error

    def test_streaming_helpers_create_stream_iterator_with_none_iterator(self) -> None:
        """Test StreamingHelpers.create_stream_iterator with None iterator."""
        result = self.utilities.StreamingHelpers.create_stream_iterator(None)

        assert result.is_success is False
        assert result.error is not None and "Iterator is None" in result.error

    def test_streaming_helpers_create_stream_iterator_with_invalid_iterator_type(
        self,
    ) -> None:
        """Test StreamingHelpers.create_stream_iterator with invalid iterator type."""
        result = self.utilities.StreamingHelpers.create_stream_iterator(
            "invalid_iterator"
        )

        assert result.is_success is False
        assert result.error is not None and "Invalid iterator type" in result.error

    def test_streaming_helpers_create_stream_iterator_with_empty_iterator(self) -> None:
        """Test StreamingHelpers.create_stream_iterator with empty iterator."""

        def empty_iterator() -> Iterator[FlextTypes.StringDict]:
            return iter([])

        result = self.utilities.StreamingHelpers.create_stream_iterator(
            empty_iterator()
        )

        assert result.is_success is True
        assert result.data == []

    def test_streaming_helpers_create_stream_iterator_with_iterator_error(self) -> None:
        """Test StreamingHelpers.create_stream_iterator with iterator error."""

        def error_iterator() -> Iterator[FlextTypes.StringDict]:
            yield {"message": "test1"}
            error_msg = "Iterator error"
            raise RuntimeError(error_msg)

        result = self.utilities.StreamingHelpers.create_stream_iterator(
            error_iterator()
        )

        assert result.is_success is False
        assert (
            result.error is not None
            and "Failed to create stream iterator" in result.error
        )

    def test_service_discovery_discover_services_with_none_target(self) -> None:
        """Test ServiceDiscovery.discover_services with None target."""
        result = self.utilities.ServiceDiscovery.discover_services(None)

        assert result.is_success is False
        assert result.error is not None and "Target is None" in result.error

    def test_service_discovery_discover_services_with_empty_target(self) -> None:
        """Test ServiceDiscovery.discover_services with empty target."""
        result = self.utilities.ServiceDiscovery.discover_services("")

        assert result.is_success is False
        assert result.error is not None and "Target cannot be empty" in result.error

    def test_service_discovery_discover_services_with_whitespace_target(self) -> None:
        """Test ServiceDiscovery.discover_services with whitespace-only target."""
        result = self.utilities.ServiceDiscovery.discover_services("   ")

        assert result.is_success is False
        assert result.error is not None and "Target cannot be empty" in result.error

    def test_service_discovery_discover_services_with_invalid_target_format(
        self,
    ) -> None:
        """Test ServiceDiscovery.discover_services with invalid target format."""
        result = self.utilities.ServiceDiscovery.discover_services(
            "invalid-target-format"
        )

        assert result.is_success is False
        assert result.error is not None and "Invalid target format" in result.error

    def test_service_discovery_discover_services_with_channel_creation_error(
        self,
    ) -> None:
        """Test ServiceDiscovery.discover_services with channel creation error."""
        target = "localhost:50051"

        with patch(
            "grpc.insecure_channel", side_effect=Exception("Channel creation failed")
        ):
            result = self.utilities.ServiceDiscovery.discover_services(target)

        assert result.is_success is False
        assert (
            result.error is not None and "Failed to discover services" in result.error
        )

    def test_service_discovery_discover_services_with_service_discovery_error(
        self,
    ) -> None:
        """Test ServiceDiscovery.discover_services with service discovery error."""
        target = "localhost:50051"

        with patch("grpc.insecure_channel") as mock_channel:
            mock_channel_instance = MagicMock()
            mock_channel_instance.get_state.side_effect = Exception(
                "Service discovery failed"
            )
            mock_channel.return_value = mock_channel_instance

            result = self.utilities.ServiceDiscovery.discover_services(target)

        assert result.is_success is False
        assert (
            result.error is not None and "Failed to discover services" in result.error
        )

    def test_error_handling_handle_grpc_error_with_none_error(self) -> None:
        """Test ErrorHandling.handle_grpc_error with None error."""
        result = self.utilities.ErrorHandling.handle_grpc_error(None)

        assert result.is_success is False
        assert result.error is not None and "Error is None" in result.error

    def test_error_handling_handle_grpc_error_with_invalid_error_type(self) -> None:
        """Test ErrorHandling.handle_grpc_error with invalid error type."""
        result = self.utilities.ErrorHandling.handle_grpc_error("invalid_error")

        assert result.is_success is False
        assert result.error is not None and "Invalid error type" in result.error

    def test_error_handling_handle_grpc_error_with_error_code_call_failure(
        self,
    ) -> None:
        """Test ErrorHandling.handle_grpc_error with error code call failure."""
        error = MagicMock()
        error.code = MagicMock(side_effect=Exception("Code call failed"))
        error.details = lambda: "Error details"

        result = self.utilities.ErrorHandling.handle_grpc_error(error)

        assert result.is_success is False
        assert result.error is not None and "Failed to get error code" in result.error

    def test_error_handling_handle_grpc_error_with_error_details_call_failure(
        self,
    ) -> None:
        """Test ErrorHandling.handle_grpc_error with error details call failure."""
        error = MagicMock()
        error.code = lambda: grpc.StatusCode.OK
        error.details = MagicMock(side_effect=Exception("Details call failed"))

        result = self.utilities.ErrorHandling.handle_grpc_error(error)

        assert result.is_success is False
        assert (
            result.error is not None and "Failed to get error details" in result.error
        )

    def test_error_handling_format_error_message_with_empty_message(self) -> None:
        """Test ErrorHandling.format_error_message with empty message."""
        result = self.utilities.ErrorHandling.format_error_message("")

        assert result.is_success is False
        assert (
            result.error is not None and "Error message cannot be empty" in result.error
        )

    def test_error_handling_format_error_message_with_whitespace_message(self) -> None:
        """Test ErrorHandling.format_error_message with whitespace-only message."""
        result = self.utilities.ErrorHandling.format_error_message("   ")

        assert result.is_success is False
        assert (
            result.error is not None and "Error message cannot be empty" in result.error
        )

    def test_error_handling_format_error_message_with_invalid_message_type(
        self,
    ) -> None:
        """Test ErrorHandling.format_error_message with invalid message type."""
        result = self.utilities.ErrorHandling.format_error_message(123)

        assert result.is_success is False
        assert (
            result.error is not None
            and "Error message must be a string" in result.error
        )

    def test_metrics_collection_collect_channel_metrics_with_none_channel(self) -> None:
        """Test MetricsCollection.collect_channel_metrics with None channel."""
        result = self.utilities.MetricsCollection.collect_channel_metrics(None)

        assert result.is_success is False
        assert result.error is not None and "Channel is None" in result.error

    def test_metrics_collection_collect_channel_metrics_with_invalid_channel_type(
        self,
    ) -> None:
        """Test MetricsCollection.collect_channel_metrics with invalid channel type."""
        result = self.utilities.MetricsCollection.collect_channel_metrics(
            "invalid_channel"
        )

        assert result.is_success is False
        assert result.error is not None and "Invalid channel type" in result.error

    def test_metrics_collection_collect_channel_metrics_with_channel_state_error(
        self,
    ) -> None:
        """Test MetricsCollection.collect_channel_metrics with channel state error."""
        mock_channel = MagicMock()
        mock_channel.get_state.side_effect = Exception("Channel state error")

        result = self.utilities.MetricsCollection.collect_channel_metrics(mock_channel)

        assert result.is_success is False
        assert (
            result.error is not None
            and "Failed to collect channel metrics" in result.error
        )

    def test_metrics_collection_collect_performance_metrics_with_invalid_start_time_type(
        self,
    ) -> None:
        """Test MetricsCollection.collect_performance_metrics with invalid start time type."""
        result = self.utilities.MetricsCollection.collect_performance_metrics(
            "invalid_start_time", 1001.0
        )

        assert result.is_success is False
        assert result.error is not None and "Invalid time parameters" in result.error

    def test_metrics_collection_collect_performance_metrics_with_invalid_end_time_type(
        self,
    ) -> None:
        """Test MetricsCollection.collect_performance_metrics with invalid end time type."""
        result = self.utilities.MetricsCollection.collect_performance_metrics(
            1000.0, "invalid_end_time"
        )

        assert result.is_success is False
        assert result.error is not None and "Invalid time parameters" in result.error

    def test_metrics_collection_collect_performance_metrics_with_negative_start_time(
        self,
    ) -> None:
        """Test MetricsCollection.collect_performance_metrics with negative start time."""
        result = self.utilities.MetricsCollection.collect_performance_metrics(
            -1000.0, 1001.0
        )

        assert result.is_success is False
        assert result.error is not None and "Invalid time parameters" in result.error

    def test_metrics_collection_collect_performance_metrics_with_negative_end_time(
        self,
    ) -> None:
        """Test MetricsCollection.collect_performance_metrics with negative end time."""
        result = self.utilities.MetricsCollection.collect_performance_metrics(
            1000.0, -1001.0
        )

        assert result.is_success is False
        assert result.error is not None and "Invalid time parameters" in result.error

    def test_metrics_collection_collect_performance_metrics_with_zero_duration(
        self,
    ) -> None:
        """Test MetricsCollection.collect_performance_metrics with zero duration."""
        result = self.utilities.MetricsCollection.collect_performance_metrics(
            1000.0,
            1000.0,  # Same start and end time
        )

        assert result.is_success is True
        assert result.data["duration"] == 0.0

    def test_metrics_collection_collect_performance_metrics_with_very_small_duration(
        self,
    ) -> None:
        """Test MetricsCollection.collect_performance_metrics with very small duration."""
        result = self.utilities.MetricsCollection.collect_performance_metrics(
            1000.0,
            1000.001,  # Very small duration
        )

        assert result.is_success is True
        assert result.data["duration"] == 0.001

    def test_metrics_collection_collect_performance_metrics_with_very_large_duration(
        self,
    ) -> None:
        """Test MetricsCollection.collect_performance_metrics with very large duration."""
        result = self.utilities.MetricsCollection.collect_performance_metrics(
            1000.0,
            2000.0,  # Large duration
        )

        assert result.is_success is True
        assert result.data["duration"] == 1000.0

    def test_utilities_execute_with_valid_command(self) -> None:
        """Test utilities execute with valid command."""
        result = self.utilities.execute("test_command", "test_data")

        assert result.is_success is False
        assert "Unknown command" in (result.error or "")

    def test_utilities_execute_with_no_arguments(self) -> None:
        """Test utilities execute with no arguments."""
        result = self.utilities.execute()

        assert result.is_success is False
        assert "Unknown command" in (result.error or "")

    def test_utilities_execute_with_none_command(self) -> None:
        """Test utilities execute with None command."""
        result = self.utilities.execute(None)

        assert result.is_success is False
        assert "Unknown command" in (result.error or "")

    def test_utilities_execute_with_empty_command(self) -> None:
        """Test utilities execute with empty command."""
        result = self.utilities.execute("")

        assert result.is_success is False
        assert "Unknown command" in (result.error or "")

    def test_utilities_execute_with_whitespace_command(self) -> None:
        """Test utilities execute with whitespace-only command."""
        result = self.utilities.execute("   ")

        assert result.is_success is False
        assert "Unknown command" in (result.error or "")

    def test_utilities_execute_with_invalid_command_type(self) -> None:
        """Test utilities execute with invalid command type."""
        result = self.utilities.execute(123)

        assert result.is_success is False
        assert "Unknown command" in (result.error or "")

    def test_utilities_execute_with_multiple_arguments(self) -> None:
        """Test utilities execute with multiple arguments."""
        result = self.utilities.execute("test_command", "arg1", "arg2", "arg3")

        assert result.is_success is False
        assert "Unknown command" in (result.error or "")

    def test_utilities_execute_with_keyword_arguments(self) -> None:
        """Test utilities execute with keyword arguments."""
        result = self.utilities.execute(
            "test_command", kwarg1="value1", kwarg2="value2"
        )

        assert result.is_success is False
        assert "Unknown command" in (result.error or "")

    def test_utilities_execute_with_mixed_arguments(self) -> None:
        """Test utilities execute with mixed arguments."""
        result = self.utilities.execute("test_command", "arg1", "arg2", kwarg1="value1")

        assert result.is_success is False
        assert "Unknown command" in (result.error or "")
