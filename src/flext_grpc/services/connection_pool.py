"""Connection pool service mixin for flext-grpc.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import ClassVar

from flext_grpc import m, s
from flext_grpc.services._entities.connection_pool_impl import (
    FlextGrpcConnectionPoolImpl,
)


class FlextGrpcConnectionPool(s):
    """Mixin providing connection pooling for FlextGrpc facade."""

    ConnectionPool: ClassVar[type[FlextGrpcConnectionPoolImpl]] = (
        FlextGrpcConnectionPoolImpl
    )

    _resource_manager: FlextGrpcConnectionPoolImpl = m.PrivateAttr(
        default_factory=lambda: FlextGrpcConnectionPoolImpl(max_size=20),
    )


__all__: list[str] = ["FlextGrpcConnectionPool"]
