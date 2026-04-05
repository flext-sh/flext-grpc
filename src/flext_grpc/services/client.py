"""Client connection service mixin for flext-grpc."""

from __future__ import annotations

import time
from collections.abc import MutableMapping

import grpc

from flext_grpc import (
    FlextGrpcConnectionPool,
    FlextGrpcMetrics,
    FlextGrpcServiceStub,
    c,
    m,
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
            self._active_channels: MutableMapping[str, grpc.Channel] = {}
            self._connection_pool = FlextGrpcConnectionPool.ConnectionPool(
                max_size=c.Grpc.Connection.DEFAULT_POOL_SIZE,
            )
            self._metrics = FlextGrpcMetrics.MetricsCollector()

        def connect(self, target: str) -> r[m.Grpc.Client]:
            """Establish client connection with pooling."""
            if target in self._active_channels:
                return u.Grpc.create_client_entity(target=target)

            def _connect() -> m.Grpc.Client:
                try:
                    grpc_channel: grpc.Channel = grpc.insecure_channel(target)
                    grpc.channel_ready_future(grpc_channel).result(
                        timeout=c.Grpc.GrpcNetwork.DEFAULT_CHANNEL_READY_TIMEOUT,
                    )
                except (grpc.RpcError, grpc.FutureTimeoutError) as exc:
                    raise RuntimeError(str(exc)) from exc
                self._active_channels[target] = grpc_channel
                self._metrics.record_metric(f"{target}_connected_at", time.time())
                client_result = u.Grpc.create_client_entity(target=target)
                if client_result.is_failure:
                    raise RuntimeError(client_result.error or "Connection failed")
                return client_result.value

            return u.try_(
                _connect,
                catch=(
                    ConnectionError,
                    TimeoutError,
                    RuntimeError,
                ),
            ).map_error(lambda e: f"Connection failed: {e}")

        def disconnect(self, client: m.Grpc.Client) -> r[m.Grpc.Client]:
            """Disconnect client and cleanup resources."""
            target = ""
            if client.channel is not None:
                target = client.channel.target or ""
            if target and target in self._active_channels:
                grpc_channel = self._active_channels[target]
                grpc_channel.close()
                del self._active_channels[target]
            return r[m.Grpc.Client].ok(client)

        def get_client_status(self, client: m.Grpc.Client) -> r[m.Grpc.Payload]:
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
        ) -> r[m.Grpc.Payload]:
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
            try:
                grpc_channel = self._active_channels[target]
                stub = FlextGrpcServiceStub(grpc_channel)
                if method == "Echo":
                    echo_response = stub.Echo(EchoRequest(message=str(request)))
                    return r[m.Grpc.Payload].ok(
                        m.Grpc.Payload.from_values(
                            method="Echo",
                            message=echo_response.message,
                            server_id=echo_response.server_id,
                            timestamp=echo_response.timestamp,
                        ),
                    )
                if method == "HealthCheck":
                    health_response = stub.HealthCheck(
                        HealthRequest(service="FlextGrpcService"),
                    )
                    return r[m.Grpc.Payload].ok(
                        m.Grpc.Payload.from_values(
                            method="HealthCheck",
                            status=health_response.status,
                            message=health_response.message,
                        ),
                    )
                return r[m.Grpc.Payload].fail(f"Unsupported method: {method}")
            except grpc.RpcError as e:
                code_val = e.code() if hasattr(e, "code") else None
                details_val = e.details() if hasattr(e, "details") else str(e)
                return r[m.Grpc.Payload].fail(
                    f"gRPC call failed: {code_val} - {details_val}",
                )
            except (ConnectionError, TimeoutError) as e:
                return r[m.Grpc.Payload].fail(f"Call execution failed: {e}")


__all__ = ["FlextGrpcClient"]
