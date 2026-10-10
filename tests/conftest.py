"""Test configuration and fixtures for flext-grpc.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import pytest

from flext_grpc import FlextGrpc
from flext_grpc.services.connection_pool import FlextGrpcConnectionPoolImpl
from flext_grpc.services.metrics import FlextGrpcMetricsCollectorImpl


@pytest.fixture(name="grpc_facade")
def fixture_grpc_facade() -> FlextGrpc:
    """Build the canonical public gRPC facade.

    Returns:
        The resulting ``FlextGrpc``.
    """
    return FlextGrpc()


@pytest.fixture(name="connection_pool")
def fixture_connection_pool() -> FlextGrpcConnectionPoolImpl:
    """Build a connection pool service component.

    Returns:
        The resulting ``FlextGrpcConnectionPoolImpl``.
    """
    return FlextGrpcConnectionPoolImpl(max_size=5)


@pytest.fixture(name="metrics_collector")
def fixture_metrics_collector() -> FlextGrpcMetricsCollectorImpl:
    """Build a metrics collector service component.

    Returns:
        The resulting ``FlextGrpcMetricsCollectorImpl``.
    """
    return FlextGrpcMetricsCollectorImpl()
