"""Connection pool service mixin for flext-grpc."""

from __future__ import annotations

import threading
from queue import Queue

from flext_grpc import p, r


class FlextGrpcConnectionPool:
    """Mixin providing connection pooling for FlextGrpc facade."""

    class ConnectionPool:
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
            """Acquire connection from pool."""
            with self._lock:
                if not self._pool.empty():
                    conn = self._pool.get_nowait()
                    self._active.add(conn)
                    return r[p.Grpc.GrpcChannel].ok(conn)
                return r[p.Grpc.GrpcChannel].fail("No available connections")

        def cleanup(self) -> p.Result[bool]:
            """Cleanup all connections."""
            with self._lock:
                self._active.clear()
                while not self._pool.empty():
                    _ = self._pool.get_nowait()
            return r[bool].ok(True)

        def release(self, connection: p.Grpc.GrpcChannel) -> p.Result[bool]:
            """Release connection back to pool."""
            with self._lock:
                if connection in self._active:
                    self._active.remove(connection)
                    if not self._pool.full():
                        self._pool.put_nowait(connection)
                return r[bool].ok(True)


__all__: list[str] = ["FlextGrpcConnectionPool"]
