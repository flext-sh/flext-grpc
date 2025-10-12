"""Domain models for gRPC operations.

This module provides domain-specific models for gRPC operations.
"""

from __future__ import annotations

from datetime import datetime

from flext_core import FlextCore
from pydantic import BaseModel, Field


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
    methods: FlextCore.Types.StringList = Field(
        default_factory=list, description="Service methods"
    )
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
    "GrpcHealthCheck",
    "GrpcRequest",
    "ServiceDefinition",
    "ServiceMetrics",
    "StreamInfo",
    "StreamMetrics",
]
