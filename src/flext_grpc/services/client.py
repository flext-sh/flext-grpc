"""Client connection service mixin for flext-grpc."""

from __future__ import annotations

import time
from collections.abc import (
    MutableMapping,
)

from flext_grpc import (
    FlextGrpcConnectionPool,
    FlextGrpcMetrics,
    FlextGrpcServiceStub,
    c,
    m,
    p,
    r,
    t,
    u,
)

EchoRequest = m.Grpc.EchoRequest
HealthRequest = m.Grpc.HealthRequest


class FlextGrpcClient:
    """Mixin providing client connection management for FlextGrpc facade."""

    class GrpcClientManager:
        """Dedicated client connection management."""

        def __init__(self) -> None:
            """Initialize client manager with connection pooling."""
            super().__init__()
            self._active_channels: MutableMapping[str, p.Grpc.GrpcChannel] = {}
            self._connection_pool = FlextGrpcConnectionPool.ConnectionPool(
                max_size=c.Grpc.Connection.DEFAULT_POOL_SIZE,
            )
            self._metrics = FlextGrpcMetrics.MetricsCollector()

        def connect(self, target: str) -> p.Result[m.Grpc.Client]:
            """Establish client connection with pooling."""
            if target in self._active_channels:
                return u.Grpc.create_client_entity(target=target)
            channel_result = u.Grpc.open_insecure_channel(target)
            if channel_result.failure:
                return r[m.Grpc.Client].fail(
                    f"Connection failed: {u.Grpc.runtime_failure_message(channel_result)}",
                )
            grpc_channel = channel_result.value
            self._active_channels[target] = grpc_channel
            self._metrics.record_metric(f"{target}_connected_at", time.time())
            client_result = u.Grpc.create_client_entity(target=target)
            if client_result.failure:
                _ = u.Grpc.run_runtime(grpc_channel.close)
                del self._active_channels[target]
                return r[m.Grpc.Client].fail(
                    client_result.error or "Connection failed",
                )
            return client_result

        def disconnect(self, client: m.Grpc.Client) -> p.Result[m.Grpc.Client]:
            """Disconnect client and cleanup resources."""
            target = ""
            if client.channel is not None:
                target = client.channel.target or ""
            if target and target in self._active_channels:
                grpc_channel = self._active_channels[target]
                closing_result = u.Grpc.run_runtime(grpc_channel.close)
                if closing_result.failure:
                    return r[m.Grpc.Client].fail(
                        f"Disconnect failed: {u.Grpc.runtime_failure_message(closing_result)}",
                    )
                del self._active_channels[target]
            return r[m.Grpc.Client].ok(client)

        def client_status(self, client: m.Grpc.Client) -> p.Result[m.Grpc.Payload]:
            """Get client connection status."""
            target = ""
            if client.channel is not None:
                target = client.channel.target or ""
            is_connected = bool(target and target in self._active_channels)
            return r[m.Grpc.Payload].ok(
                m.Grpc.Payload.from_values(connected=is_connected, target=target),
            )

        def make_call(
            self,
            client: m.Grpc.Client,
            method: str,
            request: t.OptionalContainerValueMapping,
        ) -> p.Result[m.Grpc.Payload]:
            """Execute gRPC call through client.

            Args:
            client: Client entity
            method: gRPC method name
            request: Request message (gRPC protocol message - dynamic type)

            """
            target = ""
            if client.channel is not None:
                target = client.channel.target or ""
            if not target or target not in self._active_channels:
                return r[m.Grpc.Payload].fail("Client not connected")
            grpc_channel = self._active_channels[target]
            stub = FlextGrpcServiceStub(grpc_channel)
            if method == c.Grpc.ServiceMethod.ECHO.value:
                echo_result = u.Grpc.call_runtime(
                    lambda: stub.Echo(EchoRequest(message=str(request))),
                )
                if echo_result.failure:
                    return r[m.Grpc.Payload].fail(
                        f"gRPC call failed: {u.Grpc.runtime_failure_message(echo_result)}",
                    )
                echo_response = echo_result.value
                return r[m.Grpc.Payload].ok(
                    m.Grpc.Payload.from_values(
                        method="Echo",
                        message=echo_response.message,
                        server_id=echo_response.server_id,
                        timestamp=echo_response.timestamp,
                    ),
                )
            if method == c.Grpc.ServiceMethod.HEALTH_CHECK.value:
                health_result = u.Grpc.call_runtime(
                    lambda: stub.HealthCheck(
                        HealthRequest(service="FlextGrpcService"),
                    ),
                )
                if health_result.failure:
                    return r[m.Grpc.Payload].fail(
                        f"gRPC call failed: {u.Grpc.runtime_failure_message(health_result)}",
                    )
                health_response = health_result.value
                return r[m.Grpc.Payload].ok(
                    m.Grpc.Payload.from_values(
                        method="HealthCheck",
                        status=health_response.status,
                        message=health_response.message,
                    ),
                )
            return r[m.Grpc.Payload].fail(f"Unsupported method: {method}")


__all__: list[str] = ["FlextGrpcClient"]
