"""Behavioral tests for the flext_grpc._settings public contract.

Exercises FlextGrpcSettings through its public API only: the namespaced
``settings.Grpc.*`` scalar fields, constructor/model_validate inputs, field
range validation, and the singleton lifecycle helpers. No private attributes,
no internal-collaborator spying.

Copyright (c) 2026 FLEXT Team. All rights reserved.
tests/unit/test_config
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)

from typing import Final

import pytest

from flext_grpc import FlextGrpcSettings, settings
from tests import c, tm, u

_TIMEOUT_TOLERANCE: Final[float] = 0.01


class TestsFlextGrpcConfig:
    """Behavioral contract for FlextGrpcSettings."""

    @staticmethod
    def test_defaults_satisfy_public_invariants() -> None:
        """An empty configuration yields sane, in-range namespaced field values."""
        cfg = FlextGrpcSettings()
        tm_grpc = cfg.Grpc

        def port_in_range(value: int) -> bool:
            return 1 <= value <= c.MAX_PORT

        def workers_valid(value: int) -> bool:
            return value >= 1

        tm.that(tm_grpc.host, is_=str)
        tm.that(tm_grpc.host.strip(), ne="")
        tm.that(tm_grpc.port, where=port_in_range)
        tm.that(tm_grpc.max_workers, where=workers_valid)
        tm.that(
            abs(tm_grpc.timeout - c.Grpc.NETWORK_DEFAULT_TIMEOUT) < _TIMEOUT_TOLERANCE,
            truth=True,
        )

    @staticmethod
    def test_default_namespace_values() -> None:
        """Documented default namespace values are exposed verbatim."""
        grpc = FlextGrpcSettings().Grpc
        tm.that(grpc.host, eq="127.0.0.1")
        tm.that(grpc.port, eq=50051)
        tm.that(grpc.max_workers, eq=100)
        tm.that(
            abs(grpc.timeout - c.Grpc.NETWORK_DEFAULT_TIMEOUT) < _TIMEOUT_TOLERANCE,
            truth=True,
        )

    @staticmethod
    def test_constructor_sets_namespaced_fields() -> None:
        """Nested namespace values are surfaced through settings.Grpc.*."""
        cfg = FlextGrpcSettings.model_validate({
            "Grpc": {
                "host": "10.0.0.5",
                "port": 8080,
                "max_workers": 5,
            },
        })
        tm.that(cfg.Grpc.host, eq="10.0.0.5")
        tm.that(cfg.Grpc.port, eq=8080)
        tm.that(cfg.Grpc.max_workers, eq=5)

    @staticmethod
    @pytest.mark.parametrize(
        ("host", "port"),
        [
            ("127.0.0.1", 9090),
            ("192.168.1.100", 9090),
            ("10.0.0.5", 50051),
        ],
    )
    def test_network_fields_round_trip(host: str, port: int) -> None:
        """Network host/port provided at construction are preserved."""
        cfg = FlextGrpcSettings.model_validate({"Grpc": {"host": host, "port": port}})
        tm.that(cfg.Grpc.host, eq=host)
        tm.that(cfg.Grpc.port, eq=port)

    @staticmethod
    @pytest.mark.parametrize("bad_port", [0, -1, 65536, 70000])
    def test_out_of_range_port_is_rejected(bad_port: int) -> None:
        """Ports outside 1..65535 fail validation (ValidationError <: ValueError)."""
        with pytest.raises(ValueError, match=r".*"):
            FlextGrpcSettings.model_validate({"Grpc": {"port": bad_port}})

    @staticmethod
    @pytest.mark.parametrize("bad_workers", [0, -1])
    def test_non_positive_max_workers_is_rejected(bad_workers: int) -> None:
        """max_workers below 1 fails validation."""
        with pytest.raises(ValueError, match=r".*"):
            FlextGrpcSettings.model_validate({"Grpc": {"max_workers": bad_workers}})

    @staticmethod
    def test_model_dump_round_trips_through_model_validate() -> None:
        """Dumping and re-validating reproduces the same namespaced state."""
        original = FlextGrpcSettings.model_validate({
            "Grpc": {"host": "10.0.0.5", "port": 6000, "max_workers": 7},
        })
        restored = FlextGrpcSettings.model_validate(original.model_dump())
        tm.that(restored.Grpc.host, eq="10.0.0.5")
        tm.that(restored.Grpc.port, eq=6000)
        tm.that(restored.Grpc.max_workers, eq=7)

    @staticmethod
    def test_module_singleton_is_usable() -> None:
        """The exported singleton exposes the namespaced surface directly."""
        tm.that(settings, is_=FlextGrpcSettings)
        tm.that(settings.Grpc.port, is_=int)

    @staticmethod
    def test_singleton_lifecycle_helpers() -> None:
        """Reload sources in place without invalidating published handles."""
        first = FlextGrpcSettings.fetch_global()
        tm.that(first is FlextGrpcSettings.fetch_global(), eq=True)
        debug = first.debug
        prefix = tm.not_none(FlextGrpcSettings.model_config.get("env_prefix"))
        try:
            with u.Tests.env_vars_context(
                env_vars={f"{prefix}DEBUG": str(not debug).lower()},
            ):
                FlextGrpcSettings.reset_for_testing()
                tm.that(FlextGrpcSettings.fetch_global() is first, eq=True)
                tm.that(first is settings, eq=True)
                tm.that(first.debug, eq=not debug)
        finally:
            FlextGrpcSettings.reset_for_testing()
        tm.that(FlextGrpcSettings.fetch_global() is first, eq=True)
        tm.that(first.debug, eq=debug)

    @staticmethod
    def test_invalid_reload_preserves_published_settings() -> None:
        """Reject invalid sources without changing the published instance or state."""
        original = FlextGrpcSettings.fetch_global()
        state = original.model_dump(round_trip=True)
        prefix = tm.not_none(FlextGrpcSettings.model_config.get("env_prefix"))
        with u.Tests.env_vars_context(
            env_vars={f"{prefix}DEBUG": "not-a-boolean"},
        ):
            with pytest.raises(ValueError, match="debug"):
                FlextGrpcSettings.reset_for_testing()
            tm.that(FlextGrpcSettings.fetch_global() is original, eq=True)
            tm.that(original.model_dump(round_trip=True), eq=state)
