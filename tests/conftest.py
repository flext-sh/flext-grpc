"""Test configuration and fixtures for flext-grpc.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT.
"""

from __future__ import annotations

import pytest

from flext_grpc import FlextGrpc
from flext_grpc.services.connection_pool import FlextGrpcConnectionPool
from flext_grpc.services.metrics import FlextGrpcMetrics


@pytest.fixture(name="grpc_facade")
def fixture_grpc_facade() -> FlextGrpc:
    """Build the canonical public gRPC facade."""
    return FlextGrpc()


@pytest.fixture(name="connection_pool")
def fixture_connection_pool() -> FlextGrpcConnectionPool.ConnectionPool:
    """Build a connection pool service component."""
    return FlextGrpcConnectionPool.ConnectionPool(max_size=5)


@pytest.fixture(name="metrics_collector")
def fixture_metrics_collector() -> FlextGrpcMetrics.MetricsCollector:
    """Build a metrics collector service component."""
    return FlextGrpcMetrics.MetricsCollector()
