"""Test configuration and fixtures for flext-grpc.

Test isolation patterns following enterprise testing standards.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT.
"""

from __future__ import annotations

from collections.abc import Mapping

import pytest
from flext_core import FlextContainer

from flext_grpc import FlextGrpcConstants, FlextGrpcSettings, t
from tests import c


@pytest.fixture(autouse=True)
def clean_container() -> FlextContainer:
    """Clean global container and settings before each test."""
    FlextGrpcSettings._instances.clear()
    return FlextContainer.get_global()


@pytest.fixture
def sample_grpc_config() -> Mapping[str, str | int | float]:
    """Sample gRPC configuration for tests."""
    return {
        "host": c.LOCALHOST,
        "port": FlextGrpcConstants.Grpc.GrpcNetwork.DEFAULT_GRPC_PORT,
        "max_workers": FlextGrpcConstants.Grpc.Service.DEFAULT_MAX_WORKERS,
        "timeout": c.DEFAULT_TIMEOUT_SECONDS,
    }


@pytest.fixture
def test_addresses() -> Mapping[str, t.StrSequence]:
    """Test addresses for validation."""
    return {
        "valid": [
            f"{c.LOCALHOST}:{FlextGrpcConstants.Grpc.GrpcNetwork.DEFAULT_GRPC_PORT}",
            "127.0.0.1:8080",
            "example.com:443",
            "api-server:9000",
        ],
        "invalid": [
            "",
            "localhost",
            f":{FlextGrpcConstants.Grpc.GrpcNetwork.DEFAULT_GRPC_PORT}",
            "localhost:",
            "localhost:abc",
            "localhost:-1",
            "localhost:70000",
        ],
    }
