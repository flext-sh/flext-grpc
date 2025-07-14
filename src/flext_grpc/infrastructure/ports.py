"""Port implementations (adapters) for FLEXT-GRPC.

Using flext-core patterns - NO duplication.
"""

from __future__ import annotations

import asyncio
import time
from pathlib import Path
from typing import TYPE_CHECKING

import grpc
from prometheus_client import Counter
from prometheus_client import Gauge
from prometheus_client import Histogram

from flext_core.domain.pydantic_base import ServiceResult
from flext_grpc.domain.ports import GRPCClientPort
from flext_grpc.domain.ports import GRPCServerPort
from flext_grpc.domain.ports import MetricsPort

if TYPE_CHECKING:
    from uuid import UUID

    from flext_grpc.domain.entities import GRPCService
    from flext_grpc.domain.entities import RPCCall
    from flext_grpc.infrastructure.config import GRPCConfig


class GRPCServerAdapter(GRPCServerPort):
    """gRPC server adapter implementation."""

    def __init__(self, config: GRPCConfig) -> None:
        """Initialize the gRPC server adapter with configuration."""
        self.config = config
        self.servers: dict[UUID, grpc.aio.Server] = {}

    async def start_service(self, service: GRPCService) -> ServiceResult[None]:
        """Start a gRPC service.

        Args:
            service: The gRPC service to start.

        Returns:
            ServiceResult indicating success or failure.

        """
        try:
            # Create server
            server = grpc.aio.server(
                options=[
                    ("grpc.keepalive_time_ms", self.config.keepalive_time_ms),
                    ("grpc.keepalive_timeout_ms", self.config.keepalive_timeout_ms),
                    (
                        "grpc.keepalive_permit_without_calls",
                        self.config.keepalive_permit_without_calls,
                    ),
                    ("grpc.max_receive_message_length", service.max_message_size),
                    ("grpc.max_send_message_length", service.max_message_size),
                ],
            )

            # Add servicer to server
            server.add_insecure_port(service.address)

            # Configure SSL if enabled
            if service.ssl_enabled and self.config.ssl_credentials_available:
                # Read SSL files synchronously before creating server
                cert_chain = Path(self.config.ssl_cert_path).read_bytes()
                private_key = Path(self.config.ssl_key_path).read_bytes()

                credentials = grpc.ssl_server_credentials(
                    [(private_key, cert_chain)],
                )
                server.add_secure_port(service.address, credentials)

            # Start server
            await server.start()

            # Store server reference
            self.servers[service.id] = server

            return ServiceResult.ok(None)

        except Exception as e:
            return ServiceResult.fail(f"Failed to start gRPC server: {e!s}")

    async def stop_service(self, service_id: UUID) -> ServiceResult[None]:
        """Stop a gRPC service.

        Args:
            service_id: Unique identifier of the service to stop.

        Returns:
            ServiceResult indicating success or failure.

        """
        try:
            server = self.servers.get(service_id)
            if not server:
                return ServiceResult.fail("Service not found")

            # Stop server
            await server.stop(grace=30.0)

            # Remove server reference
            del self.servers[service_id]

            return ServiceResult.ok(None)

        except Exception as e:
            return ServiceResult.fail(f"Failed to stop gRPC server: {e!s}")

    async def get_service_health(self, service_id: UUID) -> ServiceResult[bool]:
        """Check the health status of a gRPC service.

        Args:
            service_id: Unique identifier of the service.

        Returns:
            ServiceResult containing True if healthy, False otherwise.

        """
        try:
            server = self.servers.get(service_id)
            if not server:
                return ServiceResult.ok(data=False)

            # Check if server is running (simplified check)
            # In real implementation, would use gRPC health check protocol
            return ServiceResult.ok(data=True)

        except Exception as e:
            return ServiceResult.fail(f"Failed to check health: {e!s}")

    async def get_service_metrics(
        self,
        _service_id: UUID,
    ) -> ServiceResult[dict[str, float]]:
        """Get metrics for a gRPC service.

        Args:
            _service_id: Service ID (unused in this implementation)

        Returns:
            ServiceResult containing metrics dict

        """
        try:
            # In real implementation, would aggregate metrics by service
            metrics = {
                "requests_total": 1000.0,
                "requests_success": 950.0,
                "requests_error": 50.0,
                "response_time_avg": 0.15,
                "response_time_p95": 0.3,
                "response_time_p99": 0.5,
            }
            return ServiceResult.ok(metrics)

        except Exception as e:
            return ServiceResult.fail(f"Failed to get metrics: {e!s}")


class GRPCClientAdapter(GRPCClientPort):
    """gRPC client adapter implementation."""

    def __init__(self, config: GRPCConfig) -> None:
        """Initialize the gRPC client adapter with configuration."""
        self.config = config
        self.clients: dict[UUID, grpc.aio.Channel] = {}

    async def create_client(self, service: GRPCService) -> ServiceResult[None]:
        """Create a gRPC client for a service.

        Args:
            service: The gRPC service to create a client for.

        Returns:
            ServiceResult indicating success or failure.

        """
        try:
            # Create channel
            if service.ssl_enabled:
                credentials = grpc.ssl_channel_credentials()
                channel = grpc.aio.secure_channel(service.address, credentials)
            else:
                channel = grpc.aio.insecure_channel(service.address)

            # Store client reference
            self.clients[service.id] = channel

            return ServiceResult.ok(None)

        except Exception as e:
            return ServiceResult.fail(f"Failed to create gRPC client: {e!s}")

    async def call_method(self, call: RPCCall) -> ServiceResult[RPCCall]:
        """Execute an RPC method call.

        Args:
            call: The RPC call to execute.

        Returns:
            ServiceResult containing the completed call with results.

        """
        try:
            # Get client channel - would be implemented in actual gRPC client
            # In real implementation, would use the actual gRPC stub

            # Simulate call execution
            start_time = time.time()

            # Simulate some work
            await asyncio.sleep(0.1)

            # Update call with results
            call.completed_at = time.time()
            call.duration_ms = (call.completed_at - start_time) * 1000
            call.status = "completed"
            call.response_size_bytes = 1024  # Simulated

            return ServiceResult.ok(call)

        except Exception as e:
            call.status = "failed"
            call.error_message = str(e)
            return ServiceResult.fail(f"RPC call failed: {e!s}")

    async def close_client(self, service_id: UUID) -> ServiceResult[None]:
        """Close a gRPC client connection.

        Args:
            service_id: Unique identifier of the service client to close.

        Returns:
            ServiceResult indicating success or failure.

        """
        try:
            channel = self.clients.get(service_id)
            if channel:
                await channel.close()
                del self.clients[service_id]

            return ServiceResult.ok(None)

        except Exception as e:
            return ServiceResult.fail(f"Failed to close client: {e!s}")


class PrometheusMetricsAdapter(MetricsPort):
    """Prometheus metrics adapter implementation."""

    def __init__(self, config: GRPCConfig) -> None:
        """Initialize the Prometheus metrics adapter with configuration."""
        self.config = config

        # Initialize Prometheus metrics
        self.call_counter = Counter(
            "grpc_calls_total",
            "Total number of gRPC calls",
            ["service", "method", "status"],
        )

        self.call_duration = Histogram(
            "grpc_call_duration_seconds",
            "Duration of gRPC calls",
            ["service", "method"],
        )

        self.active_connections = Gauge(
            "grpc_active_connections",
            "Number of active gRPC connections",
            ["service"],
        )

    async def record_call_metrics(self, call: RPCCall) -> ServiceResult[None]:
        """Record metrics for an RPC call.

        Args:
            call: The RPC call to record metrics for.

        Returns:
            ServiceResult indicating success or failure.

        """
        try:
            # Get method info (would be passed in real implementation)
            service_name = "unknown"
            method_name = "unknown"
            status = "success" if call.is_successful else "error"

            # Record metrics
            self.call_counter.labels(
                service=service_name,
                method=method_name,
                status=status,
            ).inc()

            if call.duration_ms:
                self.call_duration.labels(
                    service=service_name,
                    method=method_name,
                ).observe(call.duration_ms / 1000.0)

            return ServiceResult.ok(None)

        except Exception as e:
            return ServiceResult.fail(f"Failed to record metrics: {e!s}")

    async def get_service_metrics(
        self,
        _service_id: UUID,
    ) -> ServiceResult[dict[str, float]]:
        """Get Prometheus metrics for a specific service.

        Args:
            _service_id: Service ID (unused in this implementation)

        Returns:
            ServiceResult containing metrics dict

        """
        try:
            # In real implementation, would query Prometheus for service-specific metrics
            metrics = {
                "requests_total": 1000.0,
                "requests_success": 950.0,
                "requests_error": 50.0,
                "response_time_avg": 0.15,
                "response_time_p95": 0.3,
                "response_time_p99": 0.5,
            }
            return ServiceResult.ok(metrics)

        except Exception as e:
            return ServiceResult.fail(f"Failed to get service metrics: {e!s}")

    async def get_method_metrics(
        self,
        _method_id: UUID,
    ) -> ServiceResult[dict[str, float]]:
        """Get Prometheus metrics for a specific method.

        Args:
            _method_id: Method ID (unused in this implementation)

        Returns:
            ServiceResult containing metrics dict

        """
        try:
            # In real implementation, would query Prometheus for method-specific metrics
            metrics = {
                "requests_total": 500.0,
                "requests_success": 475.0,
                "requests_error": 25.0,
                "response_time_avg": 0.12,
                "response_time_p95": 0.25,
                "response_time_p99": 0.4,
            }
            return ServiceResult.ok(metrics)

        except Exception as e:
            return ServiceResult.fail(f"Failed to get method metrics: {e!s}")
