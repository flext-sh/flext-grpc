"""Pytest configuration for FLEXT gRPC tests.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import pytest
from flext_core import get_flext_container


@pytest.fixture(autouse=True)
def clean_container():
    """Clean global container before each test."""
    container = get_flext_container()
    # Container isolation is handled by flext-core
    yield container


@pytest.fixture
def sample_grpc_config():
    """Sample gRPC configuration for tests."""
    return {
        "host": "localhost",
        "port": 50051,
        "max_workers": 10,
        "timeout": 30.0,
    }


@pytest.fixture
def test_addresses():
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
        ]
    }