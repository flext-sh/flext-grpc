"""Client connection service mixin for flext-grpc."""

from __future__ import annotations

import time
from collections.abc import (
    MutableMapping,
)

from flext_grpc import FlextGrpcUtilities, c, e, m, p, r, s, t
from flext_grpc.protos import flext_pb2_grpc
from flext_grpc.services import FlextGrpcConnectionPool, FlextGrpcMetrics


class FlextGrpcClient(s):
    """Mixin providing client connection management for FlextGrpc facade."""

    class GrpcClientManager:
        """Dedicated client connection management."""

        def __init__(self) -> None:
            """Initialize client manager with connection pooling."""
            super().__init__()
            self._active_channels: MutableMapping[str, p.Grpc.GrpcChannel] = {}
            self._connection_pool = FlextGrpcConnectionPool.ConnectionPool(
                max_size=c.Grpc.CONNECTION_DEFAULT_POOL_SIZE,
            )
            self._metrics = FlextGrpcMetrics.MetricsCollector()

        def connect(self, target: str) -> p.Result[p.Grpc.Client]:
            """Establish client connection with pooling."""
            if target in self._active_channels:
                return FlextGrpcUtilities.Grpc.create_client_entity(target=target)
            channel_result = FlextGrpcUtilities.Grpc.open_insecure_channel(target)
            if channel_result.failure:
                return r[p.Grpc.Client].fail_op(
                    "Connection",
                    FlextGrpcUtilities.Grpc.runtime_failure_message(channel_result),
                )
            grpc_channel = channel_result.value
            self._active_channels[target] = grpc_channel
            self._metrics.record_metric(f"{target}_connected_at", time.time())
            client_result = FlextGrpcUtilities.Grpc.create_client_entity(target=target)
            if client_result.failure:
                _ = FlextGrpcUtilities.Grpc.run_runtime(grpc_channel.close)
                del self._active_channels[target]
                return r[p.Grpc.Client].fail(
                    client_result.error or "Connection failed",
                )
            return client_result

        def disconnect(self, client: p.Grpc.Client) -> p.Result[p.Grpc.Client]:
            """Disconnect client and cleanup resources."""
            target = ""
            if client.channel is not None:
                target = client.channel.target or ""
            if target and target in self._active_channels:
                grpc_channel = self._active_channels[target]
                closing_result = FlextGrpcUtilities.Grpc.run_runtime(grpc_channel.close)
                if closing_result.failure:
                    return r[p.Grpc.Client].fail_op(
                        "Disconnect",
                        FlextGrpcUtilities.Grpc.runtime_failure_message(closing_result),
                    )
                del self._active_channels[target]
            return r[p.Grpc.Client].ok(client)

        def client_status(self, client: p.Grpc.Client) -> p.Result[m.Grpc.Payload]:
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
            client: p.Grpc.Client,
            method: str,
            request: t.JsonMapping | None,
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
                return e.fail_connection(
                    target or "<unset>",
                    options=m.ExceptionFactoryOptions(error="client not connected"),
                )
            grpc_channel = self._active_channels[target]
            generated_stub = flext_pb2_grpc.FlextGrpcServiceStub(grpc_channel)
            result: p.Result[m.Grpc.Payload]
            if method == c.Grpc.ServiceMethod.ECHO.value:
                echo_request_result = r[m.Grpc.EchoRequest].create_from_callable(
                    lambda: m.Grpc.EchoRequest.model_validate(request),
                )
                if echo_request_result.failure:
                    return r[m.Grpc.Payload].fail(
                        echo_request_result.error or "Invalid echo request",
                        exception=echo_request_result.exception,
                    )
                echo_message_result = FlextGrpcUtilities.Grpc.create_protobuf_message(
                    c.Grpc.ServiceMethod.ECHO,
                    {"message": echo_request_result.value.message},
                    response=False,
                )
                if echo_message_result.failure:
                    return r[m.Grpc.Payload].fail(
                        echo_message_result.error or "Echo message creation failed",
                        exception=echo_message_result.exception,
                    )
                echo_rpc: p.Grpc.EchoRpc = generated_stub.Echo
                echo_result: p.Result[p.Grpc.EchoResponseMessage] = (
                    FlextGrpcUtilities.Grpc.call_runtime(
                        lambda: echo_rpc(echo_message_result.value),
                    )
                )
                if echo_result.failure:
                    result = r[m.Grpc.Payload].fail_op(
                        "gRPC call",
                        FlextGrpcUtilities.Grpc.runtime_failure_message(echo_result),
                    )
                else:
                    echo_response = echo_result.value
                    result = r[m.Grpc.Payload].ok(
                        m.Grpc.Payload.from_values(
                            method="Echo",
                            message=echo_response.message,
                            server_id=echo_response.server_id,
                            timestamp=echo_response.timestamp,
                        ),
                    )
            elif method == c.Grpc.ServiceMethod.HEALTH_CHECK.value:
                health_request_result = r[m.Grpc.HealthRequest].create_from_callable(
                    lambda: m.Grpc.HealthRequest.model_validate(request),
                )
                if health_request_result.failure:
                    return r[m.Grpc.Payload].fail(
                        health_request_result.error or "Invalid health request",
                        exception=health_request_result.exception,
                    )
                health_message_result = FlextGrpcUtilities.Grpc.create_protobuf_message(
                    c.Grpc.ServiceMethod.HEALTH_CHECK,
                    {"service": health_request_result.value.service},
                    response=False,
                )
                if health_message_result.failure:
                    return r[m.Grpc.Payload].fail(
                        health_message_result.error or "Health message creation failed",
                        exception=health_message_result.exception,
                    )
                health_rpc: p.Grpc.HealthCheckRpc = generated_stub.HealthCheck
                health_result: p.Result[p.Grpc.HealthResponseMessage] = (
                    FlextGrpcUtilities.Grpc.call_runtime(
                        lambda: health_rpc(health_message_result.value),
                    )
                )
                if health_result.failure:
                    result = r[m.Grpc.Payload].fail_op(
                        "gRPC call",
                        FlextGrpcUtilities.Grpc.runtime_failure_message(health_result),
                    )
                else:
                    health_response = health_result.value
                    result = r[m.Grpc.Payload].ok(
                        m.Grpc.Payload.from_values(
                            method="HealthCheck",
                            status=health_response.status,
                            message=health_response.message,
                        ),
                    )
            else:
                result = r[m.Grpc.Payload].fail(f"Unsupported method: {method}")
            return result

    _client_manager: FlextGrpcClient.GrpcClientManager = m.PrivateAttr(
        default_factory=GrpcClientManager,
    )

    def connect_client(self, target: str) -> p.Result[p.Grpc.Client]:
        """Establish a client connection through the dedicated manager."""
        return self._client_manager.connect(target)

    def disconnect_client(self, client: p.Grpc.Client) -> p.Result[p.Grpc.Client]:
        """Disconnect a client connection through the dedicated manager."""
        return self._client_manager.disconnect(client)

    def client_status(self, client: p.Grpc.Client) -> p.Result[m.Grpc.Payload]:
        """Fetch client connection status via the dedicated manager."""
        return self._client_manager.client_status(client)

    def make_call(
        self,
        client: p.Grpc.Client,
        method: str,
        request: t.JsonMapping | None,
    ) -> p.Result[m.Grpc.Payload]:
        """Execute an RPC call through the dedicated client manager."""
        return self._client_manager.make_call(client, method, request)


__all__: list[str] = ["FlextGrpcClient"]
