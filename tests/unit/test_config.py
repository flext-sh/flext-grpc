"""Tests for flext_grpc.config module."""

from flext_grpc.config import FlextGrpcConfig


class TestFlextGrpcConfig:
    """Test cases for FlextGrpcConfig class."""

    def test_init_default(self) -> None:
        """Test default configuration initialization."""
        config = FlextGrpcConfig()
        assert config is not None
        assert config.host == "127.0.0.1"
        assert config.port == 50051
        assert config.max_workers == 10

    def test_init_custom(self) -> None:
        """Test custom configuration initialization."""
        config = FlextGrpcConfig(host="0.0.0.0", port=8080, max_workers=5)
        assert config.host == "0.0.0.0"
        assert config.port == 8080
        assert config.max_workers == 5

    def test_validation(self) -> None:
        """Test configuration validation."""
        config = FlextGrpcConfig()
        assert config.port >= 1
        assert config.port <= 65535
        assert config.max_workers >= 1
        assert config.max_workers <= 100
