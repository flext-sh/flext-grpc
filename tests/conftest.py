"""Test configuration and fixtures for flext-grpc.

Test isolation patterns following enterprise testing standards.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping

import pytest

from flext_grpc import FlextGrpcSettings
from tests import c, t

pytest_plugins = ["flext_tests.conftest_plugin"]


@pytest.fixture
def grpc_settings(
    settings_factory: Callable[..., FlextGrpcSettings],
) -> FlextGrpcSettings:
    """Provide clean FlextGrpcSettings for tests."""
    return settings_factory(FlextGrpcSettings)


@pytest.fixture
def sample_grpc_config() -> t.ConfigValueMapping:
    """Sample gRPC configuration for tests."""
    return {
        "host": c.LOCALHOST,
        "port": c.Grpc.GrpcNetwork.DEFAULT_GRPC_PORT,
        "max_workers": c.Grpc.Service.DEFAULT_MAX_WORKERS,
        "timeout": c.DEFAULT_TIMEOUT_SECONDS,
    }


@pytest.fixture
def test_addresses() -> Mapping[str, t.StrSequence]:
    """Test addresses for validation."""
    return {
        "valid": [
            f"{c.LOCALHOST}:{c.Grpc.GrpcNetwork.DEFAULT_GRPC_PORT}",
            "127.0.0.1:8080",
            "example.com:443",
            "api-server:9000",
        ],
        "invalid": [
            "",
            "localhost",
            f":{c.Grpc.GrpcNetwork.DEFAULT_GRPC_PORT}",
            "localhost:",
            "localhost:abc",
            "localhost:-1",
            "localhost:70000",
        ],
    }
