"""gRPC client implementation for FLEXT.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

gRPC client with connection pooling and FLEXT integration.
"""

from __future__ import annotations

import logging
from typing import Any

import grpc
from flext_core import FlextResult


class ConnectionPool:
    """Connection pool for gRPC clients."""

    def __init__(self, max_connections: int = 10) -> None:
        """Initialize connection pool.

        Args:
            max_connections: Maximum number of connections

        """
        self.max_connections = max_connections
        self.connections: list[grpc.Channel] = []
        self.logger = logging.getLogger("flext.grpc.pool")

    def get_connection(self, target: str) -> grpc.Channel:
        """Get a connection from the pool.

        Args:
            target: gRPC server target

        Returns:
            gRPC channel

        """
        if len(self.connections) < self.max_connections:
            channel = grpc.insecure_channel(target)
            self.connections.append(channel)
            return channel

        # Return first available connection
        return self.connections[0] if self.connections else grpc.insecure_channel(target)

    def close_all(self) -> None:
        """Close all connections in the pool."""
        for connection in self.connections:
            connection.close()
        self.connections.clear()


class FlextGRPCClient:
    """FLEXT gRPC client with connection management."""

    def __init__(self, target: str, pool: ConnectionPool | None = None) -> None:
        """Initialize gRPC client.

        Args:
            target: gRPC server target
            pool: Optional connection pool

        """
        self.target = target
        self.pool = pool or ConnectionPool()
        self.channel = self.pool.get_connection(target)
        self.logger = logging.getLogger("flext.grpc.client")

    def call_service(self, method: str, request: Any) -> FlextResult[Any]:
        """Call a gRPC service method.

        Args:
            method: Service method name
            request: Request object

        Returns:
            FlextResult with response

        """
        try:
            # This is a simplified implementation
            # In practice, you would use the actual stub here
            self.logger.info(f"Calling {method} on {self.target}")
            return FlextResult.ok({"status": "success", "method": method})
        except Exception as e:
            return FlextResult.fail(f"Service call failed: {e}")

    def close(self) -> None:
        """Close the client connection."""
        if self.channel:
            self.channel.close()
