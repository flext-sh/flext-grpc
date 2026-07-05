"""Behavioral tests for the flext_grpc.settings public contract.

Exercises FlextGrpcSettings through its public API only: constructor/model_validate
inputs, public/computed fields, the r[T] outcome of validate_configuration, the
environment factory classmethods, and validation error paths. No private attributes,
no internal-collaborator spying, no line-coverage pokes.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from flext_tests import tm

from flext_grpc import FlextGrpcSettings, c, p

if TYPE_CHECKING:
    from collections.abc import Callable


class TestsFlextGrpcConfig:
    """Behavioral contract for FlextGrpcSettings."""

    def test_defaults_satisfy_public_invariants(self) -> None:
        """An empty configuration yields sane, in-range public field values."""
        settings = FlextGrpcSettings.model_validate({})
        tm.that(settings.host, is_=str)
        tm.that(settings.host.strip(), ne="")
        tm.that(settings.port, gte=1, lte=65535)
        tm.that(settings.max_workers, gte=1, lte=100)
        tm.that(abs(settings.timeout - 30.0), lt=0.01)

    def test_constructor_sets_public_flat_fields(self) -> None:
        """Constructor values are surfaced verbatim through public fields."""
        settings = FlextGrpcSettings(host="0.0.0.0", port=8080, max_workers=5)
        tm.that(settings.host, eq="0.0.0.0")
        tm.that(settings.port, eq=8080)
        tm.that(settings.max_workers, eq=5)

    @pytest.mark.parametrize(
        ("host", "port"),
        [
            ("127.0.0.1", 9090),
            ("192.168.1.100", 9090),
            ("0.0.0.0", 50051),
        ],
    )
    def test_network_fields_round_trip(self, host: str, port: int) -> None:
        """Network host/port provided at construction are preserved."""
        settings = FlextGrpcSettings(host=host, port=port)
        tm.that(settings.host, eq=host)
        tm.that(settings.port, eq=port)

    @pytest.mark.parametrize("bad_port", [0, -1, 65536, 70000])
    def test_out_of_range_port_is_rejected(self, bad_port: int) -> None:
        """Ports outside 1..65535 fail validation (ValidationError <: ValueError)."""
        with pytest.raises(ValueError, match=r".*"):
            FlextGrpcSettings(port=bad_port)

    @pytest.mark.parametrize("tls_enabled", [True, False])
    def test_tls_computed_field_mirrors_security(self, *, tls_enabled: bool) -> None:
        """tls_enabled computed field reflects the nested security state."""
        settings = FlextGrpcSettings(security={"tls_enabled": tls_enabled})
        tm.that(settings.tls_enabled, eq=tls_enabled)

    @pytest.mark.parametrize("streaming_enabled", [True, False])
    def test_streaming_computed_field_mirrors_streaming(
        self,
        *,
        streaming_enabled: bool,
    ) -> None:
        """streaming_enabled computed field reflects the nested streaming state."""
        settings = FlextGrpcSettings(streaming={"enabled": streaming_enabled})
        tm.that(settings.streaming_enabled, eq=streaming_enabled)

    def test_validate_configuration_succeeds_for_consistent_config(self) -> None:
        """A consistent configuration validates to a successful r[True]."""
        result = FlextGrpcSettings.model_validate({}).validate_configuration()
        tm.that(tm.ok(result), eq=True)

    def test_validate_configuration_allows_client_certs_with_tls(self) -> None:
        """Client certificates with TLS enabled pass validation."""
        result = FlextGrpcSettings.model_validate({
            "security": {"tls_enabled": True, "client_cert_required": True},
        }).validate_configuration()
        tm.that(tm.ok(result), eq=True)

    def test_validate_configuration_rejects_client_certs_without_tls(self) -> None:
        """Client certificates without TLS produce a failure with an explaining error."""
        result = FlextGrpcSettings.model_validate({
            "security": {"tls_enabled": False, "client_cert_required": True},
        }).validate_configuration()
        tm.fail(result, has="Client certificates require TLS to be enabled")

    def test_production_factory_returns_tls_enabled_valid_config(self) -> None:
        """Production factory yields a TLS-enabled config that validates."""
        result = FlextGrpcSettings.create_production_config()
        tm.ok(result, is_=FlextGrpcSettings)
        settings = result.unwrap()
        tm.that(settings.tls_enabled, eq=True)
        tm.that(tm.ok(settings.validate_configuration()), eq=True)

    def test_development_factory_returns_loopback_valid_config(self) -> None:
        """Development factory yields a loopback-host config that validates."""
        result = FlextGrpcSettings.create_development_config()
        tm.ok(result, is_=FlextGrpcSettings)
        settings = result.unwrap()
        tm.that(settings.host, eq=c.LOOPBACK_IP)
        tm.that(tm.ok(settings.validate_configuration()), eq=True)

    @pytest.mark.parametrize(
        "factory",
        [
            FlextGrpcSettings.create_production_config,
            FlextGrpcSettings.create_development_config,
        ],
        ids=["production", "development"],
    )
    def test_environment_factories_return_settings(
        self,
        factory: Callable[[], p.Result[FlextGrpcSettings]],
    ) -> None:
        """Both environment factories return validated FlextGrpcSettings instances."""
        tm.ok(factory(), is_=FlextGrpcSettings)

    def test_performance_defaults_expose_documented_contract(self) -> None:
        """Default performance config exposes the documented public values."""
        perf = FlextGrpcSettings.model_validate({}).performance
        tm.that(perf.max_workers, eq=100)
        tm.that(perf.max_concurrent_rpcs, eq=1000)
        tm.that(perf.max_receive_message_length, eq=4 * 1024 * 1024)

    def test_streaming_defaults_expose_documented_contract(self) -> None:
        """Default streaming config exposes the documented public values."""
        stream = FlextGrpcSettings.model_validate({}).streaming
        tm.that(stream.enabled, eq=True)
        tm.that(stream.max_concurrent_streams, eq=10)
        tm.that(stream.stream_buffer_size, eq=500)
        tm.that(stream.max_stream_duration, eq=300)

    def test_client_defaults_expose_documented_contract(self) -> None:
        """Default client config exposes a target address and 30s timeout."""
        client = FlextGrpcSettings.model_validate({}).client
        tm.that(client.target, has=":")
        tm.that(abs(client.timeout - 30.0), lt=0.01)

    def test_monitoring_defaults_expose_documented_contract(self) -> None:
        """Default monitoring config exposes the documented public values."""
        monitoring = FlextGrpcSettings.model_validate({}).monitoring
        tm.that(monitoring.metrics_enabled, eq=True)
        tm.that(monitoring.tracing_enabled, eq=False)
        tm.that(monitoring.health_check_enabled, eq=True)
        tm.that(monitoring.health_check_interval, eq=30)
        tm.that(monitoring.log_level, eq="INFO")

    def test_model_dump_round_trips_through_model_validate(self) -> None:
        """Dumping and re-validating reproduces the same public state (idempotence)."""
        original = FlextGrpcSettings(host="10.0.0.5", port=6000, max_workers=7)
        restored = FlextGrpcSettings.model_validate(original.model_dump())
        tm.that(restored.host, eq="10.0.0.5")
        tm.that(restored.port, eq=6000)
        tm.that(restored.max_workers, eq=7)
        tm.that(restored.tls_enabled, eq=original.tls_enabled)
        tm.that(restored.streaming_enabled, eq=original.streaming_enabled)
