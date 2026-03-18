"""Tests for flext_grpc.config module."""

from __future__ import annotations

import pytest
from flext_tests import tm

from flext_grpc import FlextGrpcSettings, m


class TestFlextGrpcSettings:
    """Test cases for FlextGrpcSettings class."""

    def test_init_default(self) -> None:
        """Test default configuration initialization."""
        config = FlextGrpcSettings()
        tm.that(config is not None, eq=True)
        tm.that(config.host == "127.0.0.1", eq=True)
        tm.that(config.port == 50051, eq=True)
        tm.that(config.max_workers == 100, eq=True)

    def test_init_custom(self) -> None:
        """Test custom configuration initialization."""
        config = FlextGrpcSettings(host="0.0.0.0", port=8080, max_workers=5)
        tm.that(config.host == "0.0.0.0", eq=True)
        tm.that(config.port == 8080, eq=True)
        tm.that(config.max_workers == 5, eq=True)

    def test_validation(self) -> None:
        """Test configuration validation."""
        config = FlextGrpcSettings()
        tm.that(config.port >= 1, eq=True)
        tm.that(config.port <= 65535, eq=True)
        tm.that(config.max_workers >= 1, eq=True)
        tm.that(config.max_workers <= 100, eq=True)

    def test_validate_configuration(self) -> None:
        """Test configuration validation method."""
        config = FlextGrpcSettings()
        result = config.validate_configuration()
        tm.that(result.is_success, eq=True)

    def test_create_production_config(self) -> None:
        """Test production configuration creation."""
        result = FlextGrpcSettings.create_production_config()
        tm.that(result.is_success, eq=True)
        config = result.value
        tm.that(isinstance(config, FlextGrpcSettings), eq=True)

    def test_create_development_config(self) -> None:
        """Test development configuration creation."""
        result = FlextGrpcSettings.create_development_config()
        tm.that(result.is_success, eq=True)
        config = result.value
        tm.that(isinstance(config, FlextGrpcSettings), eq=True)

    def test_properties(self) -> None:
        """Test configuration properties."""
        config = FlextGrpcSettings(host="127.0.0.1", port=8080, max_workers=20)
        tm.that(config.host == "127.0.0.1", eq=True)
        tm.that(config.port == 8080, eq=True)
        tm.that(config.max_workers == 20, eq=True)
        tm.that(config.timeout == pytest.approx(30.0), eq=True)
        tm.that(config.tls_enabled is False, eq=True)
        tm.that(config.streaming_enabled is True, eq=True)

    def test_config_with_custom_network(self) -> None:
        """Test configuration with custom network settings."""
        config = FlextGrpcSettings(host="192.168.1.100", port=9090)
        tm.that(config.host == "192.168.1.100", eq=True)
        tm.that(config.port == 9090, eq=True)

    def test_security_config_validation(self) -> None:
        """Test security configuration validation."""
        insecure_config = FlextGrpcSettings(
            security=m.SecurityConfig(tls_enabled=False, client_cert_required=True)
        )
        insecure_result = insecure_config.validate_configuration()
        tm.that(insecure_result.is_failure, eq=True)
        tm.that(
            insecure_result.error == "Client certificates require TLS to be enabled",
            eq=True,
        )
        secure_config = FlextGrpcSettings(
            security=m.SecurityConfig(tls_enabled=True, client_cert_required=True)
        )
        secure_result = secure_config.validate_configuration()
        tm.that(secure_result.is_success, eq=True)

    def test_performance_config_defaults(self) -> None:
        """Test performance configuration defaults."""
        perf_config = FlextGrpcSettings().performance
        tm.that(perf_config.max_workers == 100, eq=True)
        tm.that(perf_config.max_concurrent_rpcs == 1000, eq=True)
        tm.that(perf_config.max_receive_message_length == 4 * 1024 * 1024, eq=True)

    def test_streaming_config_defaults(self) -> None:
        """Test streaming configuration defaults."""
        stream_config = FlextGrpcSettings().streaming
        tm.that(stream_config.enabled is True, eq=True)
        tm.that(stream_config.max_concurrent_streams == 10, eq=True)
        tm.that(stream_config.stream_buffer_size == 500, eq=True)
        tm.that(stream_config.max_stream_duration == 300, eq=True)

    def test_client_config_defaults(self) -> None:
        """Test client configuration defaults."""
        client_config = FlextGrpcSettings().client
        tm.that(client_config.timeout == pytest.approx(30.0), eq=True)
        tm.that(client_config.retry_attempts == 3, eq=True)
        tm.that(client_config.retry_backoff == pytest.approx(1.0), eq=True)

    def test_monitoring_config_defaults(self) -> None:
        """Test monitoring configuration defaults."""
        monitoring_config = FlextGrpcSettings().monitoring
        tm.that(monitoring_config.metrics_enabled is True, eq=True)
        tm.that(monitoring_config.tracing_enabled is False, eq=True)
        tm.that(monitoring_config.health_check_enabled is True, eq=True)
        tm.that(monitoring_config.health_check_interval == 30, eq=True)
        tm.that(monitoring_config.log_level == "INFO", eq=True)
