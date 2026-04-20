"""Server lifecycle service mixin for flext-grpc."""

from __future__ import annotations

import time
from collections.abc import (
    MutableMapping,
)
from concurrent.futures import ThreadPoolExecutor

from flext_grpc import (
    FlextGrpcMetrics,
    FlextGrpcServiceServicer,
    add_FlextGrpcServiceServicer_to_server,
    c,
    m,
    p,
    r,
    u,
)


class FlextGrpcServer:
    """Mixin providing server lifecycle management for FlextGrpc facade."""

    @staticmethod
    def _create_real_servicer(_server_key: str) -> p.Grpc.GrpcServicer:
        """Create runtime gRPC servicer instance for server registration."""
        return FlextGrpcServiceServicer()

    class GrpcServerManager:
        """Dedicated server lifecycle management."""

        def __init__(self) -> None:
            """Initialize server manager with metrics tracking."""
            super().__init__()
            self._active_servers: MutableMapping[str, p.Grpc.GrpcServer] = {}
            self._metrics = FlextGrpcMetrics.MetricsCollector()
            self._thread_pool = ThreadPoolExecutor(
                max_workers=50,
                thread_name_prefix="flext-grpc-server",
            )

        def server_metrics(self, server: m.Grpc.Server) -> p.Result[m.Grpc.Payload]:
            """Get server metrics."""
            server_key = f"{server.host}:{server.port}"
            started_at_raw = self._metrics.metric(f"{server_key}_started_at")
            stopped_at_raw = self._metrics.metric(f"{server_key}_stopped_at")
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

        def start_server(self, server: m.Grpc.Server) -> p.Result[m.Grpc.Server]:
            """Start gRPC server with proper lifecycle."""
            server_key = f"{server.host}:{server.port}"
            if server_key in self._active_servers:
                return r[m.Grpc.Server].fail(
                    f"Server already running: {server_key}",
                )
            try:
                starting_result = server.start()
                if starting_result.failure:
                    return starting_result
                starting_server = starting_result.value
                server_result = u.Grpc.create_runtime_server(self._thread_pool)
                if server_result.failure:
                    return r[m.Grpc.Server].fail(
                        f"Server start failed: {u.Grpc.runtime_failure_message(server_result)}",
                    )
                grpc_server = server_result.value
                bind_result = u.Grpc.bind_insecure_port(
                    grpc_server,
                    f"{starting_server.host}:{starting_server.port}",
                )
                if bind_result.failure:
                    return r[m.Grpc.Server].fail(
                        f"Server start failed: {u.Grpc.runtime_failure_message(bind_result)}",
                    )
                for _service in starting_server.services:
                    real_servicer = FlextGrpcServer._create_real_servicer(
                        server_key,
                    )
                    add_FlextGrpcServiceServicer_to_server(
                        real_servicer,
                        grpc_server,
                    )
                start_result = u.Grpc.run_runtime(grpc_server.start)
                if start_result.failure:
                    return r[m.Grpc.Server].fail(
                        f"Server start failed: {u.Grpc.runtime_failure_message(start_result)}",
                    )
                self._active_servers[server_key] = grpc_server
                self._metrics.record_metric(f"{server_key}_started_at", time.time())
                return starting_server.mark_running()
            except (ConnectionError, TimeoutError) as e:
                return r[m.Grpc.Server].fail(f"Server start failed: {e}")

        def stop_server(self, server: m.Grpc.Server) -> p.Result[m.Grpc.Server]:
            """Stop gRPC server gracefully."""
            server_key = f"{server.host}:{server.port}"
            if server_key not in self._active_servers:
                return r[m.Grpc.Server].fail(f"No active server: {server_key}")
            try:
                stopping_result = server.stop()
                if stopping_result.failure:
                    return stopping_result
                stopping_server = stopping_result.value
                grpc_server = self._active_servers[server_key]
                stop_result = u.Grpc.call_runtime(
                    lambda: grpc_server.stop(
                        grace=c.Grpc.GrpcNetwork.DEFAULT_GRACEFUL_SHUTDOWN_TIMEOUT,
                    ),
                )
                if stop_result.failure:
                    return r[m.Grpc.Server].fail(
                        f"Server stop failed: {u.Grpc.runtime_failure_message(stop_result)}",
                    )
                del self._active_servers[server_key]
                self._metrics.record_metric(f"{server_key}_stopped_at", time.time())
                return stopping_server.mark_stopped()
            except (ConnectionError, TimeoutError) as e:
                return r[m.Grpc.Server].fail(f"Server stop failed: {e}")


__all__: list[str] = ["FlextGrpcServer"]
