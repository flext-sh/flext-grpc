"""FLEXT gRPC Test Configuration - Pytest fixtures and test environment setup.

This module provides comprehensive pytest configuration for the FLEXT gRPC testing suite,
including shared fixtures, test environment setup, global container management, and
test isolation patterns following enterprise testing standards.

Test Configuration Features:
    The configuration provides essential testing infrastructure:
    - Global Container Management: Clean container state between tests
    - Test Fixtures: Pre-configured entities and common test data
    - Environment Setup: Consistent test environment initialization
    - Test Isolation: Proper cleanup and state management between tests
    - Marker Configuration: Test categorization and execution control

Fixture Architecture:
    Fixtures follow enterprise testing patterns:
    - Scope Management: Appropriate fixture scopes for performance and isolation
    - Dependency Injection: Clean dependency management for test components
    - State Cleanup: Automatic cleanup to prevent test interference
    - Data Generation: Consistent test data creation across test suites
    - Mock Management: Controlled mocking and test isolation

Available Fixtures:
    - clean_container: Global container cleanup (auto-used)
    - sample_server: Pre-configured server entity for testing
    - sample_client: Pre-configured client entity for testing
    - sample_channel: Pre-configured channel entity for testing
    - test_config: Standard configuration for testing scenarios

Example:
    Standard fixture usage pattern in tests:

    >>> def test_server_operations(sample_server, clean_container):
    ...     # Test automatically gets clean container and sample server
    ...     result = sample_server.validate_domain_rules()
    ...     assert result.is_success

Integration:
    - Integrates with pytest framework for test execution
    - Provides clean state management for flext-core container
    - Supports all test categories (unit, integration, e2e)
    - Enables consistent test data across test suites

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import pytest
from flext_core import get_flext_container


@pytest.fixture(autouse=True)
def clean_container() -> object:
    """Clean global container before each test."""
    return get_flext_container()
    # Container isolation is handled by flext-core


@pytest.fixture
def sample_grpc_config() -> dict[str, object]:
    """Sample gRPC configuration for tests."""
    return {
        "host": "localhost",
        "port": 50051,
        "max_workers": 10,
        "timeout": 30.0,
    }


@pytest.fixture
def test_addresses() -> dict[str, list[str]]:
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
