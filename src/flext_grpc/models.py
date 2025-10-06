"""Simple models for gRPC operations.

This module provides basic data models for gRPC operations.
"""

from __future__ import annotations

from datetime import datetime

from flext_core import FlextModels
from pydantic import BaseModel, Field

from flext_grpc.constants import FlextGrpcConstants


class FlextGrpcModels(FlextModels):
    """Simple models for gRPC operations.

    Provides basic configuration models used by the gRPC facade.
    """

    class ServerConfig(BaseModel):
        """Basic server configuration."""

        host: str = Field(default=FlextGrpcConstants.Network.DEFAULT_HOST)
        port: int = Field(default=FlextGrpcConstants.Network.DEFAULT_GRPC_PORT)
        max_workers: int = Field(default=FlextGrpcConstants.Service.DEFAULT_MAX_WORKERS)
        timeout: float = Field(default=FlextGrpcConstants.Network.DEFAULT_TIMEOUT)

    class ClientConfig(BaseModel):
        """Basic client configuration."""

        target: str = Field(
            default=f"{FlextGrpcConstants.Network.DEFAULT_HOST}:{FlextGrpcConstants.Network.DEFAULT_GRPC_PORT}"
        )
        timeout: float = Field(default=FlextGrpcConstants.Network.DEFAULT_TIMEOUT)

    class ChannelConfig(BaseModel):
        """Basic channel configuration."""

        address: str
        options: dict | None = None

    class StreamInfo(BaseModel):
        """Basic stream information."""

        stream_id: str
        stream_type: str
        target: str
        created_at: datetime = Field(default_factory=datetime.now)
        total_requests_sent: int = Field(default=0)
        average_latency_ms: float = Field(default=0.0)
        error_count: int = Field(default=0)

    class GrpcRequest(BaseModel):
        """Basic gRPC request model."""

        method: str = Field(description="gRPC method name")
        data: dict | None = Field(default=None, description="Request data")
        metadata: dict | None = Field(default=None, description="Request metadata")

    class GrpcHealthCheck(BaseModel):
        """gRPC health check model."""

        service_name: str = Field(description="Service name")
        status: str = Field(description="Health status")
        timestamp: datetime = Field(description="Check timestamp")

    class ServiceDefinition(BaseModel):
        """gRPC service definition model."""

        service_name: str = Field(description="Service name")
        methods: list[str] = Field(default_factory=list, description="Service methods")
        endpoint: str | None = Field(default=None, description="Service endpoint")
        metadata: dict | None = Field(default=None, description="Service metadata")

    class StreamMetrics(BaseModel):
        """gRPC stream metrics model."""

        stream_id: str = Field(description="Stream ID")
        throughput_rps: float = Field(description="Throughput in requests per second")
        latency_p50: float = Field(description="50th percentile latency")
        latency_p95: float = Field(description="95th percentile latency")
        latency_p99: float = Field(description="99th percentile latency")
        error_rate: float = Field(description="Error rate")
        memory_usage_bytes: int = Field(description="Memory usage in bytes")

    class ServiceMetrics(BaseModel):
        """gRPC service metrics model."""

        service_name: str = Field(description="Service name")
        total_requests: int = Field(description="Total requests")
        successful_requests: int = Field(description="Successful requests")
        failed_requests: int = Field(description="Failed requests")
        avg_response_time: float = Field(description="Average response time")
        active_connections: int = Field(description="Active connections")


__all__ = [
    "FlextGrpcModels",
]
