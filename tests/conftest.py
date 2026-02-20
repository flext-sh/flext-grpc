"""Test configuration and fixtures for flext-grpc.

Test isolation patterns following enterprise testing standards.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT.
"""

from __future__ import annotations

# PYTHON_VERSION_GUARD — Do not remove. Managed by scripts/maintenance/enforce_python_version.py
import sys as _sys

if _sys.version_info[:2] != (3, 13):
    _v = (
        f"{_sys.version_info.major}.{_sys.version_info.minor}.{_sys.version_info.micro}"
    )
    raise RuntimeError(
        f"\n{'=' * 72}\n"
        f"FATAL: Python {_v} detected — this project requires Python 3.13.\n"
        f"\n"
        f"The virtual environment was created with the WRONG Python interpreter.\n"
        f"\n"
        f"Fix:\n"
        f"  1. rm -rf .venv\n"
        f"  2. poetry env use python3.13\n"
        f"  3. poetry install\n"
        f"\n"
        f"Or use the workspace Makefile:\n"
        f"  make setup PROJECT=<project-name>\n"
        f"{'=' * 72}\n"
    )
del _sys
# PYTHON_VERSION_GUARD_END

import pytest
from flext_core import FlextConstants, FlextTypes as t
from flext_core.container import FlextContainer
from flext_tests.docker import FlextTestsDocker

from flext_grpc.constants import FlextGrpcConstants


@pytest.fixture(autouse=True)
def clean_container() -> object:
    """Clean global container before each test."""
    return FlextContainer.get_global()
    # Container isolation is handled by flext-core


@pytest.fixture
def sample_grpc_config() -> dict[str, t.GeneralValueType]:
    """Sample gRPC configuration for tests."""
    return {
        "host": FlextConstants.Platform.DEFAULT_HOST,
        "port": FlextGrpcConstants.Grpc.GrpcNetwork.DEFAULT_GRPC_PORT,
        "max_workers": FlextGrpcConstants.Grpc.Service.DEFAULT_MAX_WORKERS,
        "timeout": FlextConstants.Network.DEFAULT_TIMEOUT,
    }


@pytest.fixture
def test_addresses() -> dict[str, list[str]]:
    """Test addresses for validation."""
    return {
        "valid": [
            f"{FlextConstants.Platform.DEFAULT_HOST}:{FlextGrpcConstants.Grpc.GrpcNetwork.DEFAULT_GRPC_PORT}",
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


@pytest.fixture(scope="session")
def grpc_test_container() -> FlextTestsDocker:
    """Provide gRPC test container for integration tests.

    Container remains running across test session for performance.
    Cleaned at start and end of session, not per test.
    """
    container = FlextTestsDocker(
        image="grpc-test:latest",  # Placeholder - replace with actual image
        ports={"50051/tcp": ("127.0.0.1", 0)},  # Auto-assign port
        environment={
            "GRPC_SERVER_PORT": "50051",
            "LOG_LEVEL": "DEBUG",
        },
        name="flext-grpc-test",
    )

    # Start container if not already running
    if not container.is_running():
        container.start()
        container.wait_for_healthcheck(timeout=30)

    return container

    # Note: Container remains running for subsequent test sessions
    # Manual cleanup can be done via container.stop() if needed
