"""Simplified tests for flext_grpc.utilities module.

Tests the main FlextGrpcUtilities class and key methods.
"""

from __future__ import annotations

from collections.abc import Iterator
from unittest.mock import MagicMock, patch

from flext_core import FlextResult
from flext_grpc.utilities import FlextGrpcUtilities


class TestFlextGrpcUtilitiesSimple:
    """Test the main FlextGrpcUtilities class with simple, focused tests."""

    def test_init(self) -> None:
        """Test FlextGrpcUtilities initialization."""
        utilities = FlextGrpcUtilities()
        assert isinstance(utilities, FlextGrpcUtilities)
        assert hasattr(utilities, "_container")
        assert hasattr(utilities, "_logger")

    def test_execute(self) -> None:
        """Test the execute method."""
        utilities = FlextGrpcUtilities()
        result = utilities.execute()

        assert result.is_success
        assert result.data is not None
        assert result.data["status"] == "operational"
        assert result.data["service"] == "flext-grpc-utilities"

    def test_logger_property(self) -> None:
        """Test logger property."""
        utilities = FlextGrpcUtilities()
        logger = utilities.logger
        assert logger is not None

    def test_container_property(self) -> None:
        """Test container property."""
        utilities = FlextGrpcUtilities()
        container = utilities.container
        assert container is not None

    def test_message_validation_validate_protobuf_message_none(self) -> None:
        """Test MessageValidation.validate_protobuf_message with None."""
        utilities = FlextGrpcUtilities()
        result = utilities.MessageValidation.validate_protobuf_message(None)

        assert result.is_success is False
        assert result.error is not None
        assert result.error is not None and "Invalid message instance" in result.error

    def test_message_validation_validate_protobuf_message_valid(self) -> None:
        """Test MessageValidation.validate_protobuf_message with valid message."""
        utilities = FlextGrpcUtilities()

        # Create a mock protobuf message
        mock_message = MagicMock()
        mock_message.DESCRIPTOR = MagicMock()
        mock_message.DESCRIPTOR.fields = []
        mock_message.HasField.return_value = True
        mock_message.SerializeToString.return_value = b"serialized"

        result = utilities.MessageValidation.validate_protobuf_message(mock_message)

        assert result.is_success
        assert result.data is True

    def test_message_validation_validate_stream_message_sequence_empty(self) -> None:
        """Test MessageValidation.validate_stream_message_sequence with empty list."""
        utilities = FlextGrpcUtilities()
        result = utilities.MessageValidation.validate_stream_message_sequence([])

        assert result.is_success is False
        assert result.error is not None
        assert (
            result.error is not None
            and "Message sequence cannot be empty" in result.error
        )

    def test_protobuf_conversion_dict_to_protobuf_success(self) -> None:
        """Test ProtobufConversion.dict_to_protobuf with successful conversion."""
        utilities = FlextGrpcUtilities()

        # Use empty dict to avoid protobuf validation issues
        data_dict: dict[str, object] = {}

        # Create a proper mock message class
        mock_message_class = MagicMock()
        mock_instance = MagicMock()
        mock_message_class.return_value = mock_instance

        # Configure the mock to behave like a protobuf message class
        mock_message_class.__name__ = "MockMessage"
        mock_message_class.__bases__ = (object,)

        result = utilities.ProtobufConversion.dict_to_protobuf(
            data_dict,
            mock_message_class,
        )

        assert result.is_success
        assert result.data == mock_instance

    def test_protobuf_conversion_dict_to_protobuf_error(self) -> None:
        """Test ProtobufConversion.dict_to_protobuf with conversion error."""
        utilities = FlextGrpcUtilities()

        data_dict: dict[str, object] = {"test": "data"}
        mock_message_class = MagicMock()
        mock_message_class.side_effect = Exception("Conversion failed")

        result = utilities.ProtobufConversion.dict_to_protobuf(
            data_dict,
            mock_message_class,
        )

        assert result.is_success is False
        assert result.error is not None
        assert (
            result.error is not None
            and "Dict to protobuf conversion failed" in result.error
        )

    def test_channel_management_create_secure_channel(self) -> None:
        """Test ChannelManagement.create_secure_channel."""
        utilities = FlextGrpcUtilities()

        with patch("grpc.secure_channel") as mock_secure_channel:
            mock_channel = MagicMock()
            mock_secure_channel.return_value = mock_channel

            result = utilities.ChannelManagement.create_secure_channel(
                "localhost:50051"
            )

        assert result.is_success
        assert result.data == mock_channel

    def test_channel_management_create_insecure_channel(self) -> None:
        """Test ChannelManagement.create_insecure_channel."""
        utilities = FlextGrpcUtilities()

        with patch("grpc.insecure_channel") as mock_insecure_channel:
            mock_channel = MagicMock()
            mock_insecure_channel.return_value = mock_channel

            result = utilities.ChannelManagement.create_insecure_channel(
                "localhost:50051"
            )

        assert result.is_success
        assert result.data == mock_channel

    def test_channel_management_get_channel_state_none(self) -> None:
        """Test ChannelManagement.get_channel_state with None channel."""
        utilities = FlextGrpcUtilities()
        result: FlextResult[str] = utilities.ChannelManagement.get_channel_state(None)

        assert result.is_success is False
        assert result.error is not None
        assert result.error is not None and "Channel is None" in result.error

    def test_channel_management_close_channel_none(self) -> None:
        """Test ChannelManagement.close_channel with None channel."""
        utilities = FlextGrpcUtilities()
        result: FlextResult[None] = utilities.ChannelManagement.close_channel(None)

        assert result.is_success is False
        assert result.error is not None
        assert result.error is not None and "Channel is None" in result.error

    def test_streaming_helpers_create_stream_iterator(self) -> None:
        """Test StreamingHelpers.create_stream_iterator."""
        utilities = FlextGrpcUtilities()

        test_data: list[dict[str, str]] = [{"message": "test1"}, {"message": "test2"}]
        result: FlextResult[Iterator[dict[str, str]]] = (
            utilities.StreamingHelpers.create_stream_iterator(test_data)
        )

        assert result.is_success
        iterator = result.data
        assert iterator is not None

        # Test iteration
        items = list(iterator)
        assert len(items) == 2
        assert items[0]["message"] == "test1"
        assert items[1]["message"] == "test2"

    def test_streaming_helpers_create_stream_iterator_empty(self) -> None:
        """Test StreamingHelpers.create_stream_iterator with empty data."""
        utilities = FlextGrpcUtilities()

        result: FlextResult[Iterator[object]] = (
            utilities.StreamingHelpers.create_stream_iterator([])
        )

        assert result.is_success
        iterator = result.data
        assert iterator is not None
        items = list(iterator)
        assert len(items) == 0

    def test_service_discovery_discover_services(self) -> None:
        """Test ServiceDiscovery.discover_services."""
        utilities = FlextGrpcUtilities()

        with patch("grpc.insecure_channel") as mock_channel:
            mock_channel_instance = MagicMock()
            mock_channel.return_value = mock_channel_instance

            result = utilities.ServiceDiscovery.discover_services(mock_channel_instance)

        assert result.is_success
        assert isinstance(result.data, list)

    def test_error_handling_handle_grpc_error_none(self) -> None:
        """Test ErrorHandling.handle_grpc_error with None error."""
        utilities = FlextGrpcUtilities()
        result: FlextResult[dict[str, object]] = (
            utilities.ErrorHandling.handle_grpc_error(None)
        )

        assert result.is_success is False
        assert result.error is not None
        assert result.error is not None and "Error is None" in result.error

    def test_error_handling_format_error_message_valid(self) -> None:
        """Test ErrorHandling.format_error_message with valid message."""
        utilities = FlextGrpcUtilities()
        result: FlextResult[str] = utilities.ErrorHandling.format_error_message(
            "Test error"
        )

        assert result.is_success
        assert "Test error" in result.data

    def test_error_handling_format_error_message_none(self) -> None:
        """Test ErrorHandling.format_error_message with None message."""
        utilities = FlextGrpcUtilities()
        result: FlextResult[str] = utilities.ErrorHandling.format_error_message(None)

        assert result.is_success
        assert "Unknown error" in result.data

    def test_metrics_collection_collect_channel_metrics_none(self) -> None:
        """Test MetricsCollection.collect_channel_metrics with None channel."""
        utilities = FlextGrpcUtilities()
        result: FlextResult[dict[str, object]] = (
            utilities.MetricsCollection.collect_channel_metrics(None)
        )

        assert result.is_success is False
        assert result.error is not None
        assert result.error is not None and "Channel is None" in result.error

    def test_metrics_collection_collect_performance_metrics_valid(self) -> None:
        """Test MetricsCollection.collect_performance_metrics with valid times."""
        utilities = FlextGrpcUtilities()
        result: FlextResult[dict[str, object]] = (
            utilities.MetricsCollection.collect_performance_metrics(1000.0, 1001.0)
        )

        assert result.is_success
        assert isinstance(result.data, dict)
        assert "duration_ms" in result.data
        assert result.data["duration_ms"] == 1000.0

    def test_metrics_collection_collect_performance_metrics_invalid(self) -> None:
        """Test MetricsCollection.collect_performance_metrics with invalid times."""
        utilities = FlextGrpcUtilities()
        result: FlextResult[dict[str, object]] = (
            utilities.MetricsCollection.collect_performance_metrics(None, None)
        )

        assert result.is_success is False
        assert result.error is not None
        assert result.error is not None and "Invalid time parameters" in result.error
