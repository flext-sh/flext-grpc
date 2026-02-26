"""Tests for flext_grpc.config module."""

import pytest

from flext_grpc.models import m
from flext_grpc.settings import FlextGrpcSettings


class TestFlextGrpcSettings:
    """Test cases for FlextGrpcSettings class."""

    def test_init_default(self) -> None:
        """Test default configuration initialization."""
        config = FlextGrpcSettings()
        assert config is not None
        assert config.host == "127.0.0.1"
        assert config.port == 50051
        assert config.max_workers == 100

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
        config = FlextGrpcSettings()
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
        assert config.timeout == pytest.approx(30.0)  # default
        assert config.tls_enabled is False
        assert config.streaming_enabled is True

    def test_config_with_custom_network(self) -> None:
        """Test configuration with custom network settings."""
        config = FlextGrpcSettings(host="192.168.1.100", port=9090)
        assert config.host == "192.168.1.100"
        assert config.port == 9090

    def test_security_config_validation(self) -> None:
        """Test security configuration validation."""
        insecure_config = FlextGrpcSettings(
            security=m.SecurityConfig(
                tls_enabled=False,
                client_cert_required=True,
            )
        )

        insecure_result = insecure_config.validate_configuration()
        assert insecure_result.is_failure
        assert insecure_result.error == "Client certificates require TLS to be enabled"

        secure_config = FlextGrpcSettings(
            security=m.SecurityConfig(
                tls_enabled=True,
                client_cert_required=True,
            )
        )
        secure_result = secure_config.validate_configuration()
        assert secure_result.is_success

    def test_performance_config_defaults(self) -> None:
        """Test performance configuration defaults."""
        perf_config = FlextGrpcSettings().performance
        assert perf_config.max_workers == 100
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
        assert client_config.timeout == pytest.approx(30.0)
        assert client_config.retry_attempts == 3
        assert client_config.retry_backoff == pytest.approx(1.0)

    def test_monitoring_config_defaults(self) -> None:
        """Test monitoring configuration defaults."""
        monitoring_config = FlextGrpcSettings().monitoring
        assert monitoring_config.metrics_enabled is True
        assert monitoring_config.tracing_enabled is False
        assert monitoring_config.health_check_enabled is True
        assert monitoring_config.health_check_interval == 30
        assert monitoring_config.log_level == "INFO"
