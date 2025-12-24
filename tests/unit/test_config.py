"""Tests for flext_grpc.config module."""

import pytest

from flext_grpc.settings import FlextGrpcSettings


class TestFlextGrpcSettings:
    """Test cases for FlextGrpcSettings class."""

    def test_init_default(self) -> None:
        """Test default configuration initialization."""
        config = FlextGrpcSettings()
        assert config is not None
        assert config.host == "localhost"
        assert config.port == 50051
        assert config.max_workers == 10

    def test_init_custom(self) -> None:
        """Test custom configuration initialization."""
        config = FlextGrpcSettings(host="0.0.0.0", port=8080, max_workers=5)
        assert config.host == "0.0.0.0"
        assert config.port == 8080
        assert config.max_workers == 5

    def test_validation(self) -> None:
        """Test configuration validation."""
        config = FlextGrpcSettings()
        assert config.port >= 1
        assert config.port <= 65535
        assert config.max_workers >= 1
        assert config.max_workers <= 100

    def test_validate_configuration(self) -> None:
        """Test configuration validation method."""
        # Create a config with valid performance settings
        config = FlextGrpcSettings()
        # Adjust max_concurrent_rpcs to be within limits
        config.performance.max_concurrent_rpcs = 50  # Less than max_workers (10) * 10
        result = config.validate_configuration()
        assert result.is_success

    def test_create_production_config(self) -> None:
        """Test production configuration creation."""
        result = FlextGrpcSettings.create_production_config()
        assert result.is_success
        config = result.value
        assert isinstance(config, FlextGrpcSettings)

    def test_create_development_config(self) -> None:
        """Test development configuration creation."""
        result = FlextGrpcSettings.create_development_config()
        assert result.is_success
        config = result.value
        assert isinstance(config, FlextGrpcSettings)

    def test_properties(self) -> None:
        """Test configuration properties."""
        config = FlextGrpcSettings(host="127.0.0.1", port=8080, max_workers=20)
        assert config.host == "127.0.0.1"
        assert config.port == 8080
        assert config.max_workers == 20
        assert config.timeout == 30.0  # default
        assert config.tls_enabled is False
        assert config.streaming_enabled is True

    def test_config_with_custom_network(self) -> None:
        """Test configuration with custom network settings."""
        config = FlextGrpcSettings()
        config.network.host = "192.168.1.100"
        config.network.port = 9090
        assert config.network.host == "192.168.1.100"
        assert config.network.port == 9090

    def test_security_config_validation(self) -> None:
        """Test security configuration validation."""
        security_config = FlextGrpcSettings().security

        # Test valid config - Pydantic validates automatically
        assert security_config is not None

        # Test TLS without cert
        security_config.tls_enabled = True
        security_config.tls_cert_file = ""

        with pytest.raises(ValueError, match="TLS certificate required"):
            security_config.validate_security_config()

    def test_performance_config_defaults(self) -> None:
        """Test performance configuration defaults."""
        perf_config = FlextGrpcSettings().performance
        assert perf_config.max_workers == 10
        assert perf_config.max_concurrent_rpcs == 1000
        assert perf_config.max_receive_message_length == 4 * 1024 * 1024

    def test_streaming_config_defaults(self) -> None:
        """Test streaming configuration defaults."""
        stream_config = FlextGrpcSettings().streaming
        assert stream_config.enabled is True
        assert stream_config.max_concurrent_streams == 10
        assert stream_config.stream_buffer_size == 500
        assert stream_config.max_stream_duration == 300

    def test_client_config_defaults(self) -> None:
        """Test client configuration defaults."""
        client_config = FlextGrpcSettings().client
        assert client_config.timeout == 30.0
        assert client_config.retry_attempts == 3
        assert client_config.retry_backoff == 1.0

    def test_monitoring_config_defaults(self) -> None:
        """Test monitoring configuration defaults."""
        monitoring_config = FlextGrpcSettings().monitoring
        assert monitoring_config.metrics_enabled is True
        assert monitoring_config.tracing_enabled is False
        assert monitoring_config.health_check_enabled is True
        assert monitoring_config.health_check_interval == 30
        assert monitoring_config.log_level == "INFO"
