"""Additional tests for flext_grpc.api module.

Tests additional functionality to improve coverage.
"""

from __future__ import annotations

from datetime import UTC, datetime
from unittest.mock import MagicMock, patch

import pytest

from flext_grpc.api import (
    create_client,
    create_server,
    create_service,
    create_stream,
)
from flext_grpc.entities import FlextGrpcClient, FlextGrpcServer, FlextGrpcStream


class TestFlextGrpcApiAdditional:
    """Additional tests for flext_grpc.api module to improve coverage."""

    def test_create_client_with_invalid_target(self) -> None:
        """Test create_client with invalid target."""
        with pytest.raises(ValueError, match="Target cannot be empty"):
            create_client("")

    def test_create_client_with_whitespace_target(self) -> None:
        """Test create_client with whitespace-only target."""
        with pytest.raises(ValueError, match="Target cannot be empty"):
            create_client("   ")

    def test_create_server_with_invalid_host(self) -> None:
        """Test create_server with invalid host."""
        with pytest.raises(ValueError, match="Host cannot be empty"):
            create_server("", 50051)

    def test_create_server_with_whitespace_host(self) -> None:
        """Test create_server with whitespace-only host."""
        with pytest.raises(ValueError, match="Host cannot be empty"):
            create_server("   ", 50051)

    def test_create_server_with_invalid_port(self) -> None:
        """Test create_server with invalid port."""
        with pytest.raises(ValueError, match="Port must be between 1 and 65535"):
            create_server("localhost", 0)

    def test_create_server_with_negative_port(self) -> None:
        """Test create_server with negative port."""
        with pytest.raises(ValueError, match="Port must be between 1 and 65535"):
            create_server("localhost", -1)

    def test_create_server_with_high_port(self) -> None:
        """Test create_server with port > 65535."""
        with pytest.raises(ValueError, match="Port must be between 1 and 65535"):
            create_server("localhost", 70000)

    def test_create_server_with_invalid_max_workers(self) -> None:
        """Test create_server with invalid max_workers."""
        with pytest.raises(ValueError, match="Max workers must be between 1 and 100"):
            create_server("localhost", 50051, max_workers=0)

    def test_create_server_with_high_max_workers(self) -> None:
        """Test create_server with max_workers > 100."""
        with pytest.raises(ValueError, match="Max workers must be between 1 and 100"):
            create_server("localhost", 50051, max_workers=101)

    def test_create_stream_with_invalid_method_name(self) -> None:
        """Test create_stream with invalid method_name."""
        with pytest.raises(ValueError, match="Stream method name cannot be empty"):
            create_stream("", "unary")

    def test_create_stream_with_whitespace_method_name(self) -> None:
        """Test create_stream with whitespace-only method_name."""
        with pytest.raises(ValueError, match="Stream method name cannot be empty"):
            create_stream("   ", "unary")

    def test_create_stream_with_invalid_stream_type(self) -> None:
        """Test create_stream with invalid stream_type."""
        with pytest.raises(ValueError, match="Invalid stream type"):
            create_stream("TestMethod", "invalid_type")

    def test_create_client_success(self) -> None:
        """Test create_client with successful creation."""
        client = create_client("localhost:50051")
        
        assert isinstance(client, FlextGrpcClient)
        assert client.target == "localhost:50051"
        assert client.channel is None

    def test_create_server_success(self) -> None:
        """Test create_server with successful creation."""
        server = create_server("localhost", 50051, max_workers=10)
        
        assert isinstance(server, FlextGrpcServer)
        assert server.host == "localhost"
        assert server.port == 50051
        assert server.max_workers == 10
        assert server.services == []

    def test_create_stream_success(self) -> None:
        """Test create_stream with successful creation."""
        stream = create_stream("TestMethod", "unary")
        
        assert isinstance(stream, FlextGrpcStream)
        assert stream.method_name == "TestMethod"
        assert stream.stream_type == "unary"

    def test_create_stream_server_streaming(self) -> None:
        """Test create_stream with server_streaming type."""
        stream = create_stream("TestMethod", "server_streaming")
        
        assert isinstance(stream, FlextGrpcStream)
        assert stream.method_name == "TestMethod"
        assert stream.stream_type == "server_streaming"
        assert stream.is_server_streaming is True

    def test_create_stream_client_streaming(self) -> None:
        """Test create_stream with client_streaming type."""
        stream = create_stream("TestMethod", "client_streaming")
        
        assert isinstance(stream, FlextGrpcStream)
        assert stream.method_name == "TestMethod"
        assert stream.stream_type == "client_streaming"
        assert stream.is_client_streaming is True

    def test_create_stream_bidirectional(self) -> None:
        """Test create_stream with bidirectional type."""
        stream = create_stream("TestMethod", "bidirectional")
        
        assert isinstance(stream, FlextGrpcStream)
        assert stream.method_name == "TestMethod"
        assert stream.stream_type == "bidirectional"
        assert stream.is_bidirectional is True

    def test_create_service_success(self) -> None:
        """Test create_service with successful creation."""
        service = create_service("TestService", ["TestMethod1", "TestMethod2"])
        
        assert isinstance(service, dict)
        assert "name" in service
        assert "methods" in service
        assert service["name"] == "TestService"
        assert service["methods"] == ["TestMethod1", "TestMethod2"]

    def test_create_service_with_empty_name(self) -> None:
        """Test create_service with empty name."""
        with pytest.raises(ValueError, match="Service name cannot be empty"):
            create_service("", ["TestMethod"])

    def test_create_service_with_whitespace_name(self) -> None:
        """Test create_service with whitespace-only name."""
        with pytest.raises(ValueError, match="Service name cannot be empty"):
            create_service("   ", ["TestMethod"])

    def test_create_service_with_empty_methods(self) -> None:
        """Test create_service with empty methods list."""
        with pytest.raises(ValueError, match="Methods list cannot be empty"):
            create_service("TestService", [])

    def test_create_service_with_invalid_methods(self) -> None:
        """Test create_service with invalid methods (not a list)."""
        with pytest.raises(ValueError, match="Methods must be a list"):
            create_service("TestService", "TestMethod")

    def test_create_service_with_methods_containing_empty_strings(self) -> None:
        """Test create_service with methods containing empty strings."""
        with pytest.raises(ValueError, match="Method names cannot be empty"):
            create_service("TestService", ["TestMethod", ""])

    def test_create_service_with_methods_containing_whitespace(self) -> None:
        """Test create_service with methods containing whitespace-only strings."""
        with pytest.raises(ValueError, match="Method names cannot be empty"):
            create_service("TestService", ["TestMethod", "   "])

    def test_create_server_with_default_parameters(self) -> None:
        """Test create_server with default parameters."""
        server = create_server("localhost", 50051)
        
        assert isinstance(server, FlextGrpcServer)
        assert server.host == "localhost"
        assert server.port == 50051
        assert server.max_workers == 10  # Default value

    def test_create_client_with_custom_parameters(self) -> None:
        """Test create_client with custom parameters."""
        client = create_client("localhost:50051")
        
        assert isinstance(client, FlextGrpcClient)
        assert client.target == "localhost:50051"
        assert client.channel is None

    def test_create_stream_with_custom_parameters(self) -> None:
        """Test create_stream with custom parameters."""
        stream = create_stream("CustomMethod", "server_streaming")
        
        assert isinstance(stream, FlextGrpcStream)
        assert stream.method_name == "CustomMethod"
        assert stream.stream_type == "server_streaming"
        assert stream.is_server_streaming is True
        assert not stream.is_client_streaming
        assert not stream.is_bidirectional

    def test_create_service_with_single_method(self) -> None:
        """Test create_service with single method."""
        service = create_service("SingleMethodService", ["SingleMethod"])
        
        assert isinstance(service, dict)
        assert service["name"] == "SingleMethodService"
        assert service["methods"] == ["SingleMethod"]

    def test_create_service_with_multiple_methods(self) -> None:
        """Test create_service with multiple methods."""
        methods = ["Method1", "Method2", "Method3", "Method4"]
        service = create_service("MultiMethodService", methods)
        
        assert isinstance(service, dict)
        assert service["name"] == "MultiMethodService"
        assert service["methods"] == methods

    def test_create_stream_edge_case_method_names(self) -> None:
        """Test create_stream with edge case method names."""
        # Test with method name that has special characters
        stream = create_stream("TestMethod_With_Underscores", "unary")
        assert stream.method_name == "TestMethod_With_Underscores"
        
        # Test with method name that has numbers
        stream = create_stream("TestMethod123", "unary")
        assert stream.method_name == "TestMethod123"
        
        # Test with method name that has mixed case
        stream = create_stream("TestMethodMixedCase", "unary")
        assert stream.method_name == "TestMethodMixedCase"

    def test_create_server_edge_case_ports(self) -> None:
        """Test create_server with edge case ports."""
        # Test with minimum valid port
        server = create_server("localhost", 1)
        assert server.port == 1
        
        # Test with maximum valid port
        server = create_server("localhost", 65535)
        assert server.port == 65535

    def test_create_server_edge_case_max_workers(self) -> None:
        """Test create_server with edge case max_workers."""
        # Test with minimum valid max_workers
        server = create_server("localhost", 50051, max_workers=1)
        assert server.max_workers == 1
        
        # Test with maximum valid max_workers
        server = create_server("localhost", 50051, max_workers=100)
        assert server.max_workers == 100
