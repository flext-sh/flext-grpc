"""Server lifecycle service mixin for flext-grpc."""

from __future__ import annotations

import time
from collections.abc import MutableMapping
from concurrent.futures import ThreadPoolExecutor

import grpc

from flext_grpc import (
    FlextGrpcMetrics,
    FlextGrpcServiceServicer,
    add_FlextGrpcServiceServicer_to_server,
    c,
    m,
    r,
)


class FlextGrpcServer:
    """Mixin providing server lifecycle management for FlextGrpc facade."""

    @staticmethod
    def _create_real_servicer(_server_key: str) -> FlextGrpcServiceServicer:
        """Create runtime gRPC servicer instance for server registration."""
        return FlextGrpcServiceServicer()

    class GrpcServerManager:
        """Dedicated server lifecycle management."""

        def __init__(self) -> None:
            """Initialize server manager with metrics tracking."""
            super().__init__()
            self._active_servers: MutableMapping[str, grpc.Server] = {}
            self._metrics = FlextGrpcMetrics.MetricsCollector()
            self._thread_pool = ThreadPoolExecutor(
                max_workers=50,
                thread_name_prefix="flext-grpc-server",
            )

        def get_server_metrics(self, server: m.Grpc.Server) -> r[m.Grpc.Payload]:
            """Get server metrics."""
            server_key = f"{server.host}:{server.port}"
            started_at_raw = self._metrics.get_metric(f"{server_key}_started_at")
            stopped_at_raw = self._metrics.get_metric(f"{server_key}_stopped_at")
            started_at_str: str = (
                str(started_at_raw) if started_at_raw is not None else ""
            )
            stopped_at_str: str = (
                str(stopped_at_raw) if stopped_at_raw is not None else ""
            )
            return r[m.Grpc.Payload].ok(
                m.Grpc.Payload.from_values(
                    is_active=server_key in self._active_servers,
                    started_at=started_at_str,
                    stopped_at=stopped_at_str,
                ),
            )

        def start_server(self, server: m.Grpc.Server) -> r[m.Grpc.Server]:
            """Start gRPC server with proper lifecycle."""
            server_key = f"{server.host}:{server.port}"
            if server_key in self._active_servers:
                return r[m.Grpc.Server].fail(
                    f"Server already running: {server_key}",
                )
            try:
                starting_result = server.start()
                if starting_result.is_failure:
                    return starting_result
                starting_server = starting_result.value
                grpc_server = grpc.server(self._thread_pool)
                _ = grpc_server.add_insecure_port(
                    f"{starting_server.host}:{starting_server.port}",
                )
                for _service in starting_server.services:
                    real_servicer = FlextGrpcServer._create_real_servicer(
                        server_key,
                    )
                    add_FlextGrpcServiceServicer_to_server(
                        real_servicer,
                        grpc_server,
                    )
                grpc_server.start()
                self._active_servers[server_key] = grpc_server
                self._metrics.record_metric(f"{server_key}_started_at", time.time())
                return starting_server.mark_running()
            except (grpc.RpcError, ConnectionError, TimeoutError) as e:
                return r[m.Grpc.Server].fail(f"Server start failed: {e}")

        def stop_server(self, server: m.Grpc.Server) -> r[m.Grpc.Server]:
            """Stop gRPC server gracefully."""
            server_key = f"{server.host}:{server.port}"
            if server_key not in self._active_servers:
                return r[m.Grpc.Server].fail(f"No active server: {server_key}")
            try:
                stopping_result = server.stop()
                if stopping_result.is_failure:
                    return stopping_result
                stopping_server = stopping_result.value
                grpc_server = self._active_servers[server_key]
                _ = grpc_server.stop(
                    grace=c.Grpc.GrpcNetwork.DEFAULT_GRACEFUL_SHUTDOWN_TIMEOUT,
                )
                del self._active_servers[server_key]
                self._metrics.record_metric(f"{server_key}_stopped_at", time.time())
                return stopping_server.mark_stopped()
            except (grpc.RpcError, ConnectionError, TimeoutError) as e:
                return r[m.Grpc.Server].fail(f"Server stop failed: {e}")


__all__ = ["FlextGrpcServer"]
