"""Connection pool service mixin for flext-grpc."""

from __future__ import annotations

import threading
from queue import Queue

import grpc
from flext_core import r

from flext_grpc import u


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
            self._pool: Queue[grpc.Channel] = Queue(maxsize=max_size)
            self._active: set[grpc.Channel] = set()
            self._lock = threading.RLock()

        def acquire(self) -> r[grpc.Channel]:
            """Acquire connection from pool."""
            try:
                with self._lock:
                    if not self._pool.empty():
                        conn = self._pool.get_nowait()
                        self._active.add(conn)
                        return r[grpc.Channel].ok(conn)
                    return r[grpc.Channel].fail("No available connections")
            except (grpc.RpcError, ConnectionError, TimeoutError) as e:
                return r[grpc.Channel].fail(f"Connection acquisition failed: {e}")

        def cleanup(self) -> r[bool]:
            """Cleanup all connections."""
            with self._lock:
                self._active.clear()
                while not self._pool.empty():
                    try:
                        _ = self._pool.get_nowait()
                    except (grpc.RpcError, ConnectionError, TimeoutError):
                        break
            return r[bool].ok(True)

        def release(self, connection: grpc.Channel) -> r[bool]:
            """Release connection back to pool."""

            def _release() -> bool:
                with self._lock:
                    if connection in self._active:
                        self._active.remove(connection)
                        if self._pool.full():
                            return True
                        self._pool.put_nowait(connection)
                    return True

            return u.try_(
                _release,
                catch=(grpc.RpcError, ConnectionError, TimeoutError),
            ).map_error(lambda e: f"Connection release failed: {e}")


__all__ = ["FlextGrpcConnectionPool"]
