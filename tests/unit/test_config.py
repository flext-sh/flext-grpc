"""Tests for flext_grpc.config module."""

from __future__ import annotations

import pytest
from flext_tests import tm

from flext_grpc import FlextGrpcSettings


class TestFlextGrpcSettings:
    """Test cases for FlextGrpcSettings class."""

    def test_init_default(self) -> None:
        """Test default configuration initialization."""
        config = FlextGrpcSettings.model_validate({})
        tm.that(config, none=False)
        tm.that(config.host, eq="127.0.0.1")
        tm.that(config.port, eq=50051)
        tm.that(config.max_workers, eq=100)

    def test_init_custom(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test custom configuration initialization."""
        monkeypatch.delenv("GRPC_PORT", raising=False)
        monkeypatch.delenv("GRPC_HOST", raising=False)
        monkeypatch.delenv("GRPC_MAX_WORKERS", raising=False)
        monkeypatch.delenv("FLEXT_HOST", raising=False)
        monkeypatch.delenv("FLEXT_PORT", raising=False)
        monkeypatch.delenv("FLEXT_MAX_WORKERS", raising=False)
        config = FlextGrpcSettings(
            host="0.0.0.0",
            port=8080,
            max_workers=5,
        )
        tm.that(config.host, eq="0.0.0.0")
        tm.that(config.port, eq=8080)
        tm.that(config.max_workers, eq=5)

    def test_validation(self) -> None:
        """Test configuration validation."""
        config = FlextGrpcSettings.model_validate({})
        tm.that(config.port, gte=1)
        tm.that(config.port, lte=65535)
        tm.that(config.max_workers, gte=1)
        tm.that(config.max_workers, lte=100)

    def test_validate_configuration(self) -> None:
        """Test configuration validation method."""
        config = FlextGrpcSettings.model_validate({})
        result = config.validate_configuration()
        tm.that(result.success, eq=True)

    def test_create_production_config(self) -> None:
        """Test production configuration creation."""
        result = FlextGrpcSettings.create_production_config()
        tm.that(result.success, eq=True)
        config = result.value
        tm.that(config, is_=FlextGrpcSettings)

    def test_create_development_config(self) -> None:
        """Test development configuration creation."""
        result = FlextGrpcSettings.create_development_config()
        tm.that(result.success, eq=True)
        config = result.value
        tm.that(config, is_=FlextGrpcSettings)

    def test_properties(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test configuration properties."""
        monkeypatch.delenv("GRPC_PORT", raising=False)
        monkeypatch.delenv("GRPC_HOST", raising=False)
        monkeypatch.delenv("GRPC_MAX_WORKERS", raising=False)
        monkeypatch.delenv("FLEXT_HOST", raising=False)
        monkeypatch.delenv("FLEXT_PORT", raising=False)
        monkeypatch.delenv("FLEXT_MAX_WORKERS", raising=False)
        monkeypatch.delenv("FLEXT_TIMEOUT", raising=False)
        config = FlextGrpcSettings(
            host="127.0.0.1",
            port=8080,
            max_workers=20,
        )
        tm.that(config.host, eq="127.0.0.1")
        tm.that(config.port, eq=8080)
        tm.that(config.max_workers, eq=20)
        timeout_val: float = config.timeout
        tm.that(abs(timeout_val - 30.0), lt=0.01)
        tm.that(config.tls_enabled is False, eq=True)
        tm.that(config.streaming_enabled is True, eq=True)

    def test_config_with_custom_network(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test configuration with custom network settings."""
        monkeypatch.delenv("GRPC_PORT", raising=False)
        monkeypatch.delenv("GRPC_HOST", raising=False)
        monkeypatch.delenv("FLEXT_HOST", raising=False)
        monkeypatch.delenv("FLEXT_PORT", raising=False)
        config = FlextGrpcSettings(
            host="192.168.1.100",
            port=9090,
        )
        tm.that(config.host, eq="192.168.1.100")
        tm.that(config.port, eq=9090)

    def test_security_config_validation(self) -> None:
        """Test security configuration validation."""
        insecure_config = FlextGrpcSettings.model_validate({
            "security": {"tls_enabled": False, "client_cert_required": True},
        })
        insecure_result = insecure_config.validate_configuration()
        tm.that(insecure_result.failure, eq=True)
        tm.that(
            insecure_result.error,
            eq="Client certificates require TLS to be enabled",
        )
        secure_config = FlextGrpcSettings.model_validate({
            "security": {"tls_enabled": True, "client_cert_required": True},
        })
        secure_result = secure_config.validate_configuration()
        tm.that(secure_result.success, eq=True)

    def test_performance_config_defaults(self) -> None:
        """Test performance configuration defaults."""
        perf_config = FlextGrpcSettings.model_validate({}).performance
        tm.that(perf_config.max_workers, eq=100)
        tm.that(perf_config.max_concurrent_rpcs, eq=1000)
        tm.that(perf_config.max_receive_message_length, eq=4 * 1024 * 1024)

    def test_streaming_config_defaults(self) -> None:
        """Test streaming configuration defaults."""
        stream_config = FlextGrpcSettings.model_validate({}).streaming
        tm.that(stream_config.enabled is True, eq=True)
        tm.that(stream_config.max_concurrent_streams, eq=10)
        tm.that(stream_config.stream_buffer_size, eq=500)
        tm.that(stream_config.max_stream_duration, eq=300)

    def test_client_config_defaults(self) -> None:
        """Test client configuration defaults."""
        client_config = FlextGrpcSettings.model_validate({}).client
        tm.that(client_config.target, eq="127.0.0.1:50051")
        timeout_val: float = client_config.timeout
        tm.that(abs(timeout_val - 30.0), lt=0.01)

    def test_monitoring_config_defaults(self) -> None:
        """Test monitoring configuration defaults."""
        monitoring_config = FlextGrpcSettings.model_validate({}).monitoring
        tm.that(monitoring_config.metrics_enabled is True, eq=True)
        tm.that(monitoring_config.tracing_enabled is False, eq=True)
        tm.that(monitoring_config.health_check_enabled is True, eq=True)
        tm.that(monitoring_config.health_check_interval, eq=30)
        tm.that(monitoring_config.log_level, eq="INFO")
