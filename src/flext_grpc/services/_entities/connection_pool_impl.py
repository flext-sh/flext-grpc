"""Connection pool implementation entity (ENFORCE-067: one class per module).

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import threading
from queue import Queue

from flext_grpc import e, p, r


class FlextGrpcConnectionPoolImpl:
    """Generic connection pool with resource management."""

    def __init__(self, max_size: int = 10) -> None:
        """Initialize connection pool.

        Args:
        max_size: Maximum pool size

        """
        super().__init__()
        self._pool: Queue[p.Grpc.GrpcChannel] = Queue(maxsize=max_size)
        self._active: set[p.Grpc.GrpcChannel] = set()
        self._lock = threading.RLock()

    def acquire(self) -> p.Result[p.Grpc.GrpcChannel]:
        """Acquire connection from pool.

        Returns:
            The resulting ``p.Result[p.Grpc.GrpcChannel]``.
        """
        with self._lock:
            if not self._pool.empty():
                conn = self._pool.get_nowait()
                self._active.add(conn)
                return r[p.Grpc.GrpcChannel].ok(conn)
            return e.fail_not_found("connection", "available")

    def cleanup(self) -> p.Result[bool]:
        """Cleanup all connections.

        Returns:
            The resulting ``p.Result[bool]``.
        """
        with self._lock:
            self._active.clear()
            while not self._pool.empty():
                _ = self._pool.get_nowait()
        return r[bool].ok(True)

    def release(self, connection: p.Grpc.GrpcChannel) -> p.Result[bool]:
        """Release connection back to pool.

        Returns:
            The resulting ``p.Result[bool]``.
        """
        with self._lock:
            if connection in self._active:
                self._active.remove(connection)
                if not self._pool.full():
                    self._pool.put_nowait(connection)
            return r[bool].ok(True)


__all__: list[str] = ["FlextGrpcConnectionPoolImpl"]
