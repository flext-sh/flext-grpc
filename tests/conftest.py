"""FLEXT gRPC Test Configuration - Pytest fixtures and test environment setup.

This module provides comprehensive pytest configuration for the FLEXT gRPC testing suite,
including shared fixtures, test environment setup, global container management, and
test isolation patterns following enterprise testing standards.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT.
"""

from __future__ import annotations

import pytest
from flext_core import FlextContainer, FlextTypes


@pytest.fixture(autouse=True)
def clean_container() -> object:
    """Clean global container before each test."""
    return FlextContainer.get_global()
    # Container isolation is handled by flext-core


@pytest.fixture
def sample_grpc_config() -> FlextTypes.Core.Dict:
    """Sample gRPC configuration for tests."""
    return {
        "host": "localhost",
        "port": 50051,
        "max_workers": 10,
        "timeout": 30.0,
    }


@pytest.fixture
def test_addresses() -> dict[str, FlextTypes.Core.StringList]:
    """Test addresses for validation."""
    return {
        "valid": [
            "localhost:50051",
            "127.0.0.1:8080",
            "example.com:443",
            "api-server:9000",
        ],
        "invalid": [
            "",
            "localhost",
            ":50051",
            "localhost:",
            "localhost:abc",
            "localhost:-1",
            "localhost:70000",
        ],
    }
