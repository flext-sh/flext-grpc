"""Tests for flext_grpc.settings module."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from flext_tests import tm

from flext_grpc import FlextGrpcSettings, p

if TYPE_CHECKING:
    from collections.abc import Callable


@pytest.fixture(autouse=True)
def clear_grpc_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Ensure settings tests are isolated from environment overrides."""
    for env_key in (
        "FLEXT_GRPC_HOST",
        "FLEXT_GRPC_PORT",
        "FLEXT_GRPC_MAX_WORKERS",
        "FLEXT_GRPC_TIMEOUT",
        "FLEXT_GRPC_SECURITY",
        "FLEXT_GRPC_STREAMING",
    ):
        monkeypatch.delenv(env_key, raising=False)


class TestsFlextGrpcConfig:
    """Test cases for FlextGrpcSettings class."""

    def test_init_default(self) -> None:
        """Test default configuration initialization."""
        settings = FlextGrpcSettings.model_validate({})
        tm.that(settings, none=False)
        tm.that(settings.host, is_=str)
        tm.that(settings.host.strip(), ne="")
        tm.that(settings.port, gte=1, lte=65535)
        tm.that(settings.max_workers, gte=1, lte=100)

    def test_init_custom(self) -> None:
        """Test custom configuration initialization."""
        settings = FlextGrpcSettings(host="0.0.0.0", port=8080, max_workers=5)
        tm.that(settings.host, eq="0.0.0.0")
        tm.that(settings.port, eq=8080)
        tm.that(settings.max_workers, eq=5)

    def test_validate_configuration(self) -> None:
        """Test configuration validation method."""
        tm.ok(FlextGrpcSettings.model_validate({}).validate_configuration())

    @pytest.mark.parametrize(
        "factory",
        [
            FlextGrpcSettings.create_production_config,
            FlextGrpcSettings.create_development_config,
        ],
        ids=["production", "development"],
    )
    def test_create_environment_config(
        self,
        factory: Callable[[], p.Result[FlextGrpcSettings]],
    ) -> None:
        """Production/development factories return validated FlextGrpcSettings."""
        tm.ok(factory(), is_=FlextGrpcSettings)

    def test_properties(self) -> None:
        """Test configuration properties."""
        settings = FlextGrpcSettings(
            host="127.0.0.1",
            port=8080,
            max_workers=20,
            security={"tls_enabled": False},
            streaming={"enabled": True},
        )
        tm.that(settings.host, eq="127.0.0.1")
        tm.that(settings.port, eq=8080)
        tm.that(settings.max_workers, eq=20)
        tm.that(abs(settings.timeout - 30.0), lt=0.01)
        tm.that(settings.tls_enabled, eq=False)
        tm.that(settings.streaming_enabled, eq=True)

    def test_config_with_custom_network(self) -> None:
        """Test configuration with custom network settings."""
        settings = FlextGrpcSettings(host="192.168.1.100", port=9090)
        tm.that(settings.host, eq="192.168.1.100")
        tm.that(settings.port, eq=9090)

    def test_security_config_validation_insecure(self) -> None:
        """Client certificates without TLS must fail configuration validation."""
        result = FlextGrpcSettings.model_validate({
            "security": {"tls_enabled": False, "client_cert_required": True},
        }).validate_configuration()
        tm.fail(result, has="Client certificates require TLS to be enabled")

    def test_security_config_validation_secure(self) -> None:
        """Client certificates with TLS must pass configuration validation."""
        tm.ok(
            FlextGrpcSettings.model_validate({
                "security": {"tls_enabled": True, "client_cert_required": True},
            }).validate_configuration(),
        )

    def test_performance_config_defaults(self) -> None:
        """Test performance configuration defaults."""
        perf = FlextGrpcSettings.model_validate({}).performance
        tm.that(perf.max_workers, eq=100)
        tm.that(perf.max_concurrent_rpcs, eq=1000)
        tm.that(perf.max_receive_message_length, eq=4 * 1024 * 1024)

    def test_streaming_config_defaults(self) -> None:
        """Test streaming configuration defaults."""
        stream = FlextGrpcSettings.model_validate({}).streaming
        tm.that(stream.enabled, eq=True)
        tm.that(stream.max_concurrent_streams, eq=10)
        tm.that(stream.stream_buffer_size, eq=500)
        tm.that(stream.max_stream_duration, eq=300)

    def test_client_config_defaults(self) -> None:
        """Test client configuration defaults."""
        client = FlextGrpcSettings.model_validate({}).client
        tm.that(client.target, has=":")
        tm.that(abs(client.timeout - 30.0), lt=0.01)

    def test_monitoring_config_defaults(self) -> None:
        """Test monitoring configuration defaults."""
        monitoring = FlextGrpcSettings.model_validate({}).monitoring
        tm.that(monitoring.metrics_enabled, eq=True)
        tm.that(monitoring.tracing_enabled, eq=False)
        tm.that(monitoring.health_check_enabled, eq=True)
        tm.that(monitoring.health_check_interval, eq=30)
        tm.that(monitoring.log_level, eq="INFO")
