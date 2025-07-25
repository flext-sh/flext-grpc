"""Tests for gRPC client functionality without mocks."""

from __future__ import annotations

import pytest

from flext_grpc.client import ConnectionPool, FlextGRPCClient

# Test constants
MOCK_JWT_TOKEN_FOR_TESTING = "Bearer mock_jwt_token_for_testing"


class TestFlextGRPCClient:
    """Test cases for gRPC client."""

    def test_client_initialization(self) -> None:
        """Test client initialization."""
        client = FlextGRPCClient()

        # Test that client is properly initialized
        assert client is not None
        assert hasattr(client, "_config")
        assert hasattr(client, "_logger")

    def test_base_client_initialization(self) -> None:
        """Test base client functionality."""
        from flext_grpc.client import FlextGrpcClientBase

        client = FlextGrpcClientBase()

        # Test that client has proper configuration access
        assert client is not None
        assert hasattr(client, "_config")
        assert hasattr(client, "_logger")

    def test_channel_options_configuration(self) -> None:
        """Test channel options configuration."""
        from flext_grpc.client import FlextGrpcClientBase

        client = FlextGrpcClientBase()
        options = client._get_channel_options()

        # Verify channel options are properly configured
        assert isinstance(options, list)
        assert len(options) > 0

        # Verify all options are tuples with proper structure
        for option in options:
            assert isinstance(option, tuple)
            assert len(option) == 2
            assert isinstance(option[0], str)

    def test_message_size_configuration(self) -> None:
        """Test message size configuration."""
        from flext_grpc.client import FlextGrpcClientBase

        client = FlextGrpcClientBase()
        message_size = client._get_grpc_message_size()

        # Verify message size is properly configured
        assert isinstance(message_size, int)
        assert message_size > 0

    def test_client_with_old_interface(self) -> None:
        """Test client with old interface for backwards compatibility."""
        from flext_grpc.client import FlextGRPCClientOld

        client = FlextGRPCClientOld(
            host="secure.example.com",
            port=443,
            tls_enabled=True,
            tls_cert_path="/path/to/ca.pem",
        )

        assert client.tls_enabled
        assert client.tls_cert_path == "/path/to/ca.pem"
        assert client.host == "secure.example.com"
        assert client.port == 443

    def test_client_connection_result(self) -> None:
        """Test client connection returns FlextResult."""
        from flext_grpc.client import FlextGRPCClientOld

        client = FlextGRPCClientOld()
        result = client.connect()

        # Verify FlextResult structure
        assert result is not None
        assert hasattr(result, "is_success")

    def test_client_address_property(self) -> None:
        """Test client address property."""
        from flext_grpc.client import FlextGRPCClientOld

        client = FlextGRPCClientOld(host="test.example.com", port=9999)
        address = client.address

        assert address == "test.example.com:9999"

    @pytest.mark.asyncio
    async def test_async_client_methods_exist(self) -> None:
        """Test that async client methods exist and are callable."""
        from flext_grpc.client import FlextGRPCClientOld

        client = FlextGRPCClientOld()

        # Verify async methods exist
        assert hasattr(client, "health_check")
        assert hasattr(client, "create_pipeline")
        assert hasattr(client, "get_pipeline")
        assert hasattr(client, "list_pipelines")
        assert hasattr(client, "execute_pipeline")

        # Call health check (should work without server)
        result = await client.health_check()
        assert isinstance(result, dict)
        assert "status" in result


class TestConnectionPool:
    """Test gRPC connection pooling."""

    def test_pool_initialization(self) -> None:
        """Test connection pool initialization."""
        pool = ConnectionPool(max_size=10)

        assert pool.max_size == 10
        assert isinstance(pool._channels, list)
        assert len(pool._channels) == 0

    def test_connection_pool_basic_functionality(self) -> None:
        """Test basic connection pool functionality."""
        pool = ConnectionPool(max_size=2)

        # Get channels from pool (will create new ones)
        channel1 = pool.get_channel("localhost:50051")
        channel2 = pool.get_channel("localhost:50052")

        # Verify channels are created
        assert channel1 is not None
        assert channel2 is not None

        # Verify they are different channels for different targets
        assert channel1 != channel2

    def test_secure_channel_creation(self) -> None:
        """Test secure channel creation in pool."""
        import grpc

        pool = ConnectionPool(max_size=5)

        # Create credentials for secure channel
        credentials = grpc.ssl_channel_credentials()

        # Get secure channel
        channel = pool.get_channel("secure.example.com:443", credentials)

        # Verify channel was created
        assert channel is not None

    def test_pool_close(self) -> None:
        """Test connection pool cleanup."""
        pool = ConnectionPool(max_size=2)

        # Create some real channels for testing
        channel1 = pool.get_channel("localhost:50051")
        channel2 = pool.get_channel("localhost:50052")

        # Add channels to pool for cleanup testing
        pool._channels = [channel1, channel2]

        # Close pool
        pool.close()

        # Verify channels are cleared
        assert len(pool._channels) == 0


class TestClientConfiguration:
    """Test client configuration and setup."""

    def test_grpc_channel_target_function(self) -> None:
        """Test gRPC channel target configuration."""
        from flext_grpc.client import get_grpc_channel_target

        target = get_grpc_channel_target()

        # Verify target is properly formatted
        assert isinstance(target, str)
        assert ":" in target  # Should contain host:port format

    def test_ssl_credentials_creation(self) -> None:
        """Test SSL credentials creation."""
        from flext_grpc.client import _create_ssl_credentials

        # Test with no certificates (should work)
        credentials = _create_ssl_credentials()

        # Verify credentials object is created
        assert credentials is not None

    def test_secure_channel_creation_function(self) -> None:
        """Test secure channel creation function."""
        from flext_grpc.client import create_secure_channel

        # Test creating secure channel
        channel = create_secure_channel("test.example.com:443")

        # Verify channel was created
        assert channel is not None
