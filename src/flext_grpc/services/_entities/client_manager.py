"""gRPC client manager implementation entity (ENFORCE-067: one class per module).

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import time
from typing import TYPE_CHECKING

from flext_grpc import c, e, m, p, r, t, u
from flext_grpc.proto.stub import FlextGrpcServiceStub
from flext_grpc.services._entities.connection_pool_impl import (
    FlextGrpcConnectionPoolImpl,
)
from flext_grpc.services._entities.metrics_collector import (
    FlextGrpcMetricsCollectorImpl,
)

if TYPE_CHECKING:
    from collections.abc import MutableMapping


class FlextGrpcClientManagerImpl:
    """Dedicated client connection management."""

    def __init__(self) -> None:
        """Initialize client manager with connection pooling."""
        super().__init__()
        self._active_channels: MutableMapping[str, p.Grpc.GrpcChannel] = {}
        self._connection_pool = FlextGrpcConnectionPoolImpl(
            max_size=c.Grpc.CONNECTION_DEFAULT_POOL_SIZE,
        )
        self._metrics = FlextGrpcMetricsCollectorImpl()

    def connect(self, target: str) -> p.Result[m.Grpc.Client]:
        """Establish client connection with pooling.

        Returns:
            The resulting ``p.Result[m.Grpc.Client]``.
        """
        if target in self._active_channels:
            return u.Grpc.create_client_entity(target=target)
        channel_result = u.Grpc.open_insecure_channel(target)
        if channel_result.failure:
            return r[m.Grpc.Client].fail_op(
                "Connection",
                u.Grpc.runtime_failure_message(channel_result),
            )
        grpc_channel = channel_result.value
        self._active_channels[target] = grpc_channel
        self._metrics.record_metric(f"{target}_connected_at", time.time())
        client_result = u.Grpc.create_client_entity(target=target)
        if client_result.failure:
            _ = u.Grpc.run_runtime(grpc_channel.close)
            del self._active_channels[target]
            return r[m.Grpc.Client].from_failure(client_result)
        return client_result

    def disconnect(self, client: m.Grpc.Client) -> p.Result[m.Grpc.Client]:
        """Disconnect client and cleanup resources.

        Returns:
            The resulting ``p.Result[m.Grpc.Client]``.
        """
        target = ""
        if client.channel is not None:
            target = client.channel.target or ""
        if target and target in self._active_channels:
            grpc_channel = self._active_channels[target]
            closing_result = u.Grpc.run_runtime(grpc_channel.close)
            if closing_result.failure:
                return r[m.Grpc.Client].fail_op(
                    "Disconnect",
                    u.Grpc.runtime_failure_message(closing_result),
                )
            del self._active_channels[target]
        return r[m.Grpc.Client].ok(client)

    def client_status(self, client: m.Grpc.Client) -> p.Result[m.Grpc.Payload]:
        """Get client connection status.

        Returns:
            The resulting ``p.Result[m.Grpc.Payload]``.
        """
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
        request: t.JsonMapping | None,
    ) -> p.Result[m.Grpc.Payload]:
        """Execute gRPC call through client.

        Args:
        client: Client entity
        method: gRPC method name
        request: Request message (gRPC protocol message - dynamic type)

        Returns:
            The resulting ``p.Result[m.Grpc.Payload]``.
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
        stub = FlextGrpcServiceStub(grpc_channel)
        result: p.Result[m.Grpc.Payload]
        if method == c.Grpc.ServiceMethod.ECHO.value:
            echo_request = u.validate_value(m.Grpc.EchoRequest, request)
            if echo_request.failure:
                return r[m.Grpc.Payload].from_failure(echo_request)
            echo_message = echo_request.value
            echo_result = u.Grpc.call_runtime(lambda: stub.echo(echo_message))
            if echo_result.failure:
                result = r[m.Grpc.Payload].fail_op(
                    "gRPC call",
                    u.Grpc.runtime_failure_message(echo_result),
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
            health_request = u.validate_value(m.Grpc.HealthRequest, request or {})
            if health_request.failure:
                return r[m.Grpc.Payload].from_failure(health_request)
            health_message = health_request.value
            health_result = u.Grpc.call_runtime(
                lambda: stub.health_check(health_message),
            )
            if health_result.failure:
                result = r[m.Grpc.Payload].fail_op(
                    "gRPC call",
                    u.Grpc.runtime_failure_message(health_result),
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


__all__: list[str] = ["FlextGrpcClientManagerImpl"]
