"""gRPC server manager implementation entity (ENFORCE-067: one class per module)."""

from __future__ import annotations

import time
from concurrent.futures import ThreadPoolExecutor
from typing import TYPE_CHECKING

from flext_core import r
from flext_grpc import FlextGrpcModels, FlextGrpcUtilities, c, p
from flext_grpc.proto.servicer import FlextGrpcProtoServicer

from .metrics_collector import FlextGrpcMetricsCollectorImpl

if TYPE_CHECKING:
    from collections.abc import MutableMapping


class FlextGrpcServerManagerImpl:
    """Dedicated server lifecycle management."""

    def __init__(self) -> None:
        """Initialize server manager with metrics tracking."""
        super().__init__()
        self._active_servers: MutableMapping[str, p.Grpc.GrpcServer] = {}
        self._metrics = FlextGrpcMetricsCollectorImpl()
        self._thread_pool = ThreadPoolExecutor(
            max_workers=50, thread_name_prefix="flext-grpc-server"
        )

    def _create_real_servicer(self, _server_key: str) -> p.Grpc.GrpcServicer:
        """Create runtime gRPC servicer instance for server registration."""
        return FlextGrpcProtoServicer.Servicer()

    def server_metrics(
        self, server: FlextGrpcModels.Grpc.Server
    ) -> p.Result[FlextGrpcModels.Grpc.Payload]:
        """Get server metrics."""
        server_key = f"{server.host}:{server.port}"
        started_at_raw = self._metrics.metric(f"{server_key}_started_at")
        stopped_at_raw = self._metrics.metric(f"{server_key}_stopped_at")
        started_at_str: str = str(started_at_raw) if started_at_raw is not None else ""
        stopped_at_str: str = str(stopped_at_raw) if stopped_at_raw is not None else ""
        return r[FlextGrpcModels.Grpc.Payload].ok(
            FlextGrpcModels.Grpc.Payload.from_values(
                is_active=server_key in self._active_servers,
                started_at=started_at_str,
                stopped_at=stopped_at_str,
            )
        )

    def start_server(
        self, server: FlextGrpcModels.Grpc.Server
    ) -> p.Result[FlextGrpcModels.Grpc.Server]:
        """Start gRPC server with proper lifecycle."""
        server_key = f"{server.host}:{server.port}"
        result: p.Result[FlextGrpcModels.Grpc.Server]
        if server_key in self._active_servers:
            result = r[FlextGrpcModels.Grpc.Server].fail(
                f"Server already running: {server_key}"
            )
        else:
            try:
                result = self._start_new_server(server_key, server)
            except (ConnectionError, TimeoutError) as e:
                result = r[FlextGrpcModels.Grpc.Server].fail_op("Server start", e)
        return result

    def stop_server(
        self, server: FlextGrpcModels.Grpc.Server
    ) -> p.Result[FlextGrpcModels.Grpc.Server]:
        """Stop gRPC server gracefully."""
        server_key = f"{server.host}:{server.port}"
        if server_key not in self._active_servers:
            return r[FlextGrpcModels.Grpc.Server].fail(
                f"No active server: {server_key}"
            )
        try:
            return self._stop_active_server(server_key, server)
        except (ConnectionError, TimeoutError) as e:
            return r[FlextGrpcModels.Grpc.Server].fail_op("Server stop", e)

    def _start_new_server(
        self, server_key: str, server: FlextGrpcModels.Grpc.Server
    ) -> p.Result[FlextGrpcModels.Grpc.Server]:
        """Start a server that is not already registered as active."""
        starting_result = server.start()
        if starting_result.failure:
            return starting_result
        starting_server = starting_result.value
        bound_result = self._create_bound_runtime_server(starting_server)
        if bound_result.failure:
            return r[FlextGrpcModels.Grpc.Server].fail(
                f"Server start failed: {FlextGrpcUtilities.Grpc.runtime_failure_message(bound_result)}"
            )
        grpc_server = bound_result.value
        self._register_services(server_key, starting_server, grpc_server)
        return self._activate_runtime_server(server_key, starting_server, grpc_server)

    def _create_bound_runtime_server(
        self, starting_server: FlextGrpcModels.Grpc.Server
    ) -> p.Result[p.Grpc.GrpcServer]:
        """Create a runtime server and bind it to the configured address."""
        server_result = FlextGrpcUtilities.Grpc.create_runtime_server(self._thread_pool)
        if server_result.failure:
            return r[p.Grpc.GrpcServer].fail(
                FlextGrpcUtilities.Grpc.runtime_failure_message(server_result),
                exception=server_result.exception,
            )
        grpc_server = server_result.value
        bind_result = FlextGrpcUtilities.Grpc.bind_insecure_port(
            grpc_server, f"{starting_server.host}:{starting_server.port}"
        )
        if bind_result.failure:
            return r[p.Grpc.GrpcServer].fail(
                FlextGrpcUtilities.Grpc.runtime_failure_message(bind_result),
                exception=bind_result.exception,
            )
        return r[p.Grpc.GrpcServer].ok(grpc_server)

    def _register_services(
        self,
        server_key: str,
        starting_server: FlextGrpcModels.Grpc.Server,
        grpc_server: p.Grpc.GrpcServer,
    ) -> None:
        """Register configured services on the runtime server."""
        for _service in starting_server.services:
            real_servicer = self._create_real_servicer(server_key)
            FlextGrpcProtoServicer.add_flext_grpc_service_servicer_to_server(
                real_servicer, grpc_server
            )

    def _activate_runtime_server(
        self,
        server_key: str,
        starting_server: FlextGrpcModels.Grpc.Server,
        grpc_server: p.Grpc.GrpcServer,
    ) -> p.Result[FlextGrpcModels.Grpc.Server]:
        """Start the runtime server and mark the domain server as running."""
        start_result = FlextGrpcUtilities.Grpc.run_runtime(grpc_server.start)
        if start_result.failure:
            return r[FlextGrpcModels.Grpc.Server].fail(
                f"Server start failed: {FlextGrpcUtilities.Grpc.runtime_failure_message(start_result)}"
            )
        self._active_servers[server_key] = grpc_server
        self._metrics.record_metric(f"{server_key}_started_at", time.time())
        return starting_server.mark_running()

    def _stop_active_server(
        self, server_key: str, server: FlextGrpcModels.Grpc.Server
    ) -> p.Result[FlextGrpcModels.Grpc.Server]:
        """Stop a registered active server and record stop metrics."""
        stopping_result: p.Result[FlextGrpcModels.Grpc.Server] = server.stop()
        if stopping_result.failure:
            return stopping_result
        stopping_server = stopping_result.value
        grpc_server = self._active_servers[server_key]
        stop_result = FlextGrpcUtilities.Grpc.call_runtime(
            lambda: grpc_server.stop(
                grace=c.Grpc.NETWORK_DEFAULT_GRACEFUL_SHUTDOWN_TIMEOUT
            )
        )
        if stop_result.failure:
            return r[FlextGrpcModels.Grpc.Server].fail(
                f"Server stop failed: {FlextGrpcUtilities.Grpc.runtime_failure_message(stop_result)}"
            )
        del self._active_servers[server_key]
        self._metrics.record_metric(f"{server_key}_stopped_at", time.time())
        return stopping_server.mark_stopped()


__all__: list[str] = ["FlextGrpcServerManagerImpl"]
