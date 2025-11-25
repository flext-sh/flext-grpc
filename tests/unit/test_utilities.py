"""Tests for flext_grpc.utilities module."""

from google.protobuf.message import Message

from flext_grpc.utilities import FlextGrpcUtilities


class TestFlextGrpcUtilities:
    """Test cases for FlextGrpcUtilities class."""

    def test_init(self) -> None:
        """Test FlextGrpcUtilities initialization."""
        utilities = FlextGrpcUtilities()
        assert utilities is not None

    def test_system_utilities(self) -> None:
        """Test system utilities."""
        utilities = FlextGrpcUtilities()
        assert hasattr(utilities, "SystemUtilities")

    def test_execute_method(self) -> None:
        """Test execute method."""
        utilities = FlextGrpcUtilities()
        result = utilities.execute()
        assert result.is_success
        assert "status" in result.value
        assert result.value["status"] == "operational"

    def test_execute_with_parameters(self) -> None:
        """Test execute method with command and data."""
        utilities = FlextGrpcUtilities()
        result = utilities.execute(command="test", data={"key": "value"})
        assert result.is_success
        assert result.value["command"] == "test"
        assert result.value["data"] == {"key": "value"}

    def test_create_client_entity(self) -> None:
        """Test client entity creation."""
        result = FlextGrpcUtilities.create_client_entity("localhost:50051")
        assert result.is_success
        client = result.unwrap()
        assert client.channel.target == "localhost:50051"

    def test_create_server_entity(self) -> None:
        """Test server entity creation."""
        result = FlextGrpcUtilities.create_server_entity("localhost", 50051)
        assert result.is_success
        server = result.unwrap()
        assert server.host == "localhost"
        assert server.port == 50051

    def test_create_channel_entity(self) -> None:
        """Test channel entity creation."""
        result = FlextGrpcUtilities.create_channel_entity("localhost:50051")
        assert result.is_success
        channel = result.unwrap()
        assert channel.target == "localhost:50051"

    def test_create_service_entity(self) -> None:
        """Test service entity creation."""
        result = FlextGrpcUtilities.create_service_entity("TestService", ["method1"])
        assert result.is_success
        service = result.unwrap()
        assert service.name == "TestService"
        assert service.methods == ["method1"]

    def test_create_stream_entity(self) -> None:
        """Test stream entity creation."""
        result = FlextGrpcUtilities.create_stream_entity("test_method", "unary")
        assert result.is_success
        stream = result.unwrap()
        assert stream.method_name == "test_method"
        assert stream.stream_type == "unary"

    def test_system_memory_usage(self) -> None:
        """Test system memory usage retrieval."""
        usage = FlextGrpcUtilities.SystemUtilities.get_system_memory_usage()
        assert isinstance(usage, float)
        assert 0 <= usage <= 100  # Percentage should be between 0 and 100

    def test_buffer_size_bytes(self) -> None:
        """Test buffer size calculation."""
        size = FlextGrpcUtilities.SystemUtilities.get_buffer_size_bytes("test")
        assert isinstance(size, int)
        assert size >= 0

    def test_validate_message_basic_checks(self) -> None:
        """Test basic message validation."""
        # Create a mock protobuf message if possible
        mock_msg = Message()
        result = FlextGrpcUtilities.MessageValidation.validate_message_basic_checks(
            mock_msg
        )
        assert result.is_success

    def test_validate_message_basic_checks_invalid(self) -> None:
        """Test basic message validation with invalid input."""
        result = FlextGrpcUtilities.MessageValidation.validate_message_basic_checks(
            None
        )
        assert result.is_failure

    def test_metadata_conversion(self) -> None:
        """Test gRPC metadata conversion."""
        # Create a mock metadata iterable
        metadata = [("key1", b"value1"), ("key2", "value2")]
        result = FlextGrpcUtilities.StreamingHelpers.validate_stream_metadata(
            iter(metadata)
        )
        assert result.is_success
        metadata_dict = result.unwrap()
        assert metadata_dict["key1"] == "value1"
        assert metadata_dict["key2"] == "value2"
