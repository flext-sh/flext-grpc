"""Server lifecycle service mixin for flext-grpc."""

from __future__ import annotations

import time
from collections.abc import MutableMapping
from concurrent.futures import ThreadPoolExecutor
from typing import override

from flext_core import r
from flext_grpc import FlextGrpcUtilities, c, m, p, s
from flext_grpc.protos import flext_pb2_grpc
from flext_grpc.services.metrics import FlextGrpcMetrics


class FlextGrpcServer(s):
    """Mixin providing server lifecycle management for FlextGrpc facade."""

    class GrpcServicer(flext_pb2_grpc.FlextGrpcServiceServicer):
        """Canonical implementation of the generated FLEXT gRPC service."""

        def __init__(self, server_id: str) -> None:
            """Bind responses to the serving endpoint identifier."""
            self._server_id = server_id

        @override
        def Echo(
            self,
            request: p.Grpc.EchoRequestMessage,
            context: p.Grpc.GrpcServicerContext,
        ) -> p.Grpc.GrpcMessage:
            """Validate and echo a protobuf request."""
            del context
            request_model = m.Grpc.EchoRequest(message=request.message)
            response_model = m.Grpc.EchoResponse(
                message=request_model.message,
                server_id=self._server_id,
            )
            response_result = FlextGrpcUtilities.Grpc.create_protobuf_message(
                c.Grpc.ServiceMethod.ECHO,
                {
                    "message": response_model.message,
                    "server_id": response_model.server_id,
                    "timestamp": response_model.timestamp.isoformat(),
                },
                response=True,
            )
            return response_result.unwrap()

        @override
        def HealthCheck(
            self,
            request: p.Grpc.HealthRequestMessage,
            context: p.Grpc.GrpcServicerContext,
        ) -> p.Grpc.GrpcMessage:
            """Validate and answer a protobuf health request."""
            del context
            request_model = m.Grpc.HealthRequest(service=request.service)
            response_model = m.Grpc.HealthResponse(
                status="SERVING",
                message=f"{request_model.service or 'FlextGrpcService'} is serving",
            )
            response_result = FlextGrpcUtilities.Grpc.create_protobuf_message(
                c.Grpc.ServiceMethod.HEALTH_CHECK,
                {
                    "status": response_model.status,
                    "message": response_model.message,
                },
                response=True,
            )
            return response_result.unwrap()

    @staticmethod
    def _create_real_servicer(server_key: str) -> p.Grpc.GrpcServicer:
        """Create runtime gRPC servicer instance for server registration."""
        return FlextGrpcServer.GrpcServicer(server_key)

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

        def server_metrics(
            self,
            server: m.Grpc.Server,
        ) -> p.Result[p.Grpc.Payload]:
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
            return r[p.Grpc.Payload].ok(
                m.Grpc.Payload.from_values(
                    is_active=server_key in self._active_servers,
                    started_at=started_at_str,
                    stopped_at=stopped_at_str,
                ),
            )

        def start_server(self, server: m.Grpc.Server) -> p.Result[p.Grpc.Server]:
            """Start gRPC server with proper lifecycle."""
            server_key = f"{server.host}:{server.port}"
            result: p.Result[p.Grpc.Server]
            if server_key in self._active_servers:
                result = r[p.Grpc.Server].fail(
                    f"Server already running: {server_key}",
                )
            else:
                try:
                    result = self._start_new_server(server_key, server)
                except (ConnectionError, TimeoutError) as e:
                    result = r[p.Grpc.Server].fail_op("Server start", e)
            return result

        def stop_server(self, server: m.Grpc.Server) -> p.Result[p.Grpc.Server]:
            """Stop gRPC server gracefully."""
            server_key = f"{server.host}:{server.port}"
            if server_key not in self._active_servers:
                return r[p.Grpc.Server].fail(f"No active server: {server_key}")
            try:
                return self._stop_active_server(server_key, server)
            except (ConnectionError, TimeoutError) as e:
                return r[p.Grpc.Server].fail_op("Server stop", e)

        def _start_new_server(
            self,
            server_key: str,
            server: m.Grpc.Server,
        ) -> p.Result[p.Grpc.Server]:
            """Start a server that is not already registered as active."""
            starting_result = server.start()
            if starting_result.failure:
                return starting_result
            starting_server = starting_result.value
            bound_result = self._create_bound_runtime_server(starting_server)
            if bound_result.failure:
                return r[p.Grpc.Server].fail(
                    f"Server start failed: {FlextGrpcUtilities.Grpc.runtime_failure_message(bound_result)}",
                )
            grpc_server = bound_result.value
            self._register_services(server_key, grpc_server)
            return self._activate_runtime_server(
                server_key,
                starting_server,
                grpc_server,
            )

        def _create_bound_runtime_server(
            self,
            starting_server: m.Grpc.Server,
        ) -> p.Result[p.Grpc.GrpcServer]:
            """Create a runtime server and bind it to the configured address."""
            server_result = FlextGrpcUtilities.Grpc.create_runtime_server(
                self._thread_pool
            )
            if server_result.failure:
                return r[p.Grpc.GrpcServer].fail(
                    FlextGrpcUtilities.Grpc.runtime_failure_message(server_result),
                    exception=server_result.exception,
                )
            grpc_server = server_result.value
            bind_result = FlextGrpcUtilities.Grpc.bind_insecure_port(
                grpc_server,
                f"{starting_server.host}:{starting_server.port}",
            )
            if bind_result.failure:
                return r[p.Grpc.GrpcServer].fail(
                    FlextGrpcUtilities.Grpc.runtime_failure_message(bind_result),
                    exception=bind_result.exception,
                )
            return r[p.Grpc.GrpcServer].ok(grpc_server)

        @staticmethod
        def _register_services(
            server_key: str,
            grpc_server: p.Grpc.GrpcServer,
        ) -> None:
            """Register configured services on the runtime server."""
            real_servicer = FlextGrpcServer._create_real_servicer(server_key)
            flext_pb2_grpc.add_FlextGrpcServiceServicer_to_server(
                real_servicer,
                grpc_server,
            )

        def _activate_runtime_server(
            self,
            server_key: str,
            starting_server: m.Grpc.Server,
            grpc_server: p.Grpc.GrpcServer,
        ) -> p.Result[p.Grpc.Server]:
            """Start the runtime server and mark the domain server as running."""
            start_result = FlextGrpcUtilities.Grpc.run_runtime(grpc_server.start)
            if start_result.failure:
                return r[p.Grpc.Server].fail(
                    f"Server start failed: {FlextGrpcUtilities.Grpc.runtime_failure_message(start_result)}",
                )
            self._active_servers[server_key] = grpc_server
            self._metrics.record_metric(f"{server_key}_started_at", time.time())
            return starting_server.mark_running()

        def _stop_active_server(
            self,
            server_key: str,
            server: m.Grpc.Server,
        ) -> p.Result[p.Grpc.Server]:
            """Stop a registered active server and record stop metrics."""
            stopping_result: p.Result[p.Grpc.Server] = server.stop()
            if stopping_result.failure:
                return stopping_result
            stopping_server = stopping_result.value
            grpc_server = self._active_servers[server_key]
            stop_result = FlextGrpcUtilities.Grpc.call_runtime(
                lambda: grpc_server.stop(
                    grace=c.Grpc.NETWORK_DEFAULT_GRACEFUL_SHUTDOWN_TIMEOUT,
                ),
            )
            if stop_result.failure:
                return r[p.Grpc.Server].fail(
                    f"Server stop failed: {FlextGrpcUtilities.Grpc.runtime_failure_message(stop_result)}",
                )
            del self._active_servers[server_key]
            self._metrics.record_metric(f"{server_key}_stopped_at", time.time())
            return stopping_server.mark_stopped()

    def start_server(self, server: m.Grpc.Server) -> p.Result[p.Grpc.Server]:
        """Start a server through the dedicated lifecycle manager."""
        return self._server_manager.start_server(server)

    def stop_server(self, server: m.Grpc.Server) -> p.Result[p.Grpc.Server]:
        """Stop a server through the dedicated lifecycle manager."""
        return self._server_manager.stop_server(server)

    def server_status(self, server: m.Grpc.Server) -> p.Result[p.Grpc.Payload]:
        """Fetch server runtime metrics through the dedicated manager."""
        return self._server_manager.server_metrics(server)

    _server_manager: FlextGrpcServer.GrpcServerManager = m.PrivateAttr(
        default_factory=GrpcServerManager,
    )


__all__: list[str] = ["FlextGrpcServer"]
