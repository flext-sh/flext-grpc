"""Application commands for FLEXT-GRPC.

Using flext-core command patterns - NO duplication.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from uuid import UUID


# Base Command class for gRPC commands
class Command:
    """Base command class for gRPC operations."""


class StartGRPCServiceCommand:
    """Command to start a gRPC service."""

    name: str
    version = 10
    max_concurrent_rpcs: int = 100
    max_message_size: int = 104857600
    ssl_enabled: bool = False
    ssl_cert_path: str | None = None
    ssl_key_path: str | None = None
    ssl_ca_path: str | None = None


class StopGRPCServiceCommand:
    """Command to stop a gRPC service."""

    service_id: UUID
    graceful = True
    timeout_seconds: float = 30.0


class UpdateGRPCServiceCommand:
    """Command to update a gRPC service configuration."""

    service_id: UUID
    max_workers = None
    max_concurrent_rpcs: int | None = None
    max_message_size: int | None = None
    ssl_enabled: bool | None = None
    ssl_cert_path: str | None = None
    ssl_key_path: str | None = None
    ssl_ca_path: str | None = None


class RegisterRPCMethodCommand:
    """Command to register an RPC method."""

    service_id: UUID
    name: str
    timeout_seconds: float = 30.0
    retry_policy: dict[str, Any] | None = None


class UnregisterRPCMethodCommand:
    """Command to unregister an RPC method."""

    method_id: UUID


class ExecuteRPCCallCommand:
    """Command to execute an RPC call."""

    method_id: UUID
    client_id: str
    request_data: dict[str, Any]
    timeout_seconds: float | None = None
    metadata: dict[str, Any] | None = None


class HealthCheckCommand:
    """Command to perform health check on a service."""

    service_id: UUID


class GetServiceMetricsCommand:
    """Command to get service metrics."""

    service_id: UUID
    time_range_hours = 24


class GetMethodMetricsCommand:
    """Command to get method metrics."""

    method_id: UUID
    time_range_hours: int = 24
