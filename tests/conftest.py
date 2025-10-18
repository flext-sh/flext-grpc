"""Test configuration and fixtures for flext-grpc.

Test isolation patterns following enterprise testing standards.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT.
"""

from __future__ import annotations

import pytest
from flext_core import FlextConstants, FlextContainer

from flext_grpc.constants import FlextGrpcConstants


@pytest.fixture(autouse=True)
def clean_container() -> object:
    """Clean global container before each test."""
    return FlextContainer.get_global()
    # Container isolation is handled by flext-core


@pytest.fixture
def sample_grpc_config() -> dict[str, object]:
    """Sample gRPC configuration for tests."""
    return {
        "host": FlextConstants.Platform.DEFAULT_HOST,
        "port": FlextGrpcConstants.Network.DEFAULT_GRPC_PORT,
        "max_workers": FlextGrpcConstants.Service.DEFAULT_MAX_WORKERS,
        "timeout": FlextConstants.Network.DEFAULT_TIMEOUT,
    }


@pytest.fixture
def test_addresses() -> dict[str, list[str]]:
    """Test addresses for validation."""
    return {
        "valid": [
            f"{FlextConstants.Platform.DEFAULT_HOST}:{FlextGrpcConstants.Network.DEFAULT_GRPC_PORT}",
            "127.0.0.1:8080",
            "example.com:443",
            "api-server:9000",
        ],
        "invalid": [
            "",
            "localhost",
            f":{FlextGrpcConstants.Network.DEFAULT_GRPC_PORT}",
            "localhost:",
            "localhost:abc",
            "localhost:-1",
            "localhost:70000",
        ],
    }
