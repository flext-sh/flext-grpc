"""Models for gRPC operations.

This module provides data models for gRPC operations.
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator

from flext_core import FlextConstants, FlextModels
from flext_grpc.constants import FlextGrpcConstants


class FlextGrpcModels(FlextModels):
    """Comprehensive models for gRPC operations extending FlextModels.

    Provides standardized models for all gRPC domain entities including:
    - Server and client configurations
    - Stream management and monitoring
    - Channel operations and health tracking
    - Service definitions and metadata
    - Request/response handling patterns
    - Performance metrics and monitoring

    All nested classes inherit FlextModels validation and patterns.
    """

    # Core gRPC Configuration Models
    class ServerConfig(BaseModel):
        """gRPC server configuration model."""

        host: str = Field(
            default=FlextConstants.Platform.DEFAULT_HOST,
            description="Server host address",
        )
        port: int = Field(
            default=FlextGrpcConstants.DEFAULT_GRPC_PORT,
            description="Server port number",
        )
        max_workers: int = Field(default=10, description="Maximum worker threads")
        timeout: float = Field(
            default=FlextConstants.Network.DEFAULT_TIMEOUT,
            description="Request timeout in seconds",
        )

        @field_validator("port")
        @classmethod
        def validate_port(cls, v: int) -> int:
            """Validate port number is within valid range."""
            min_port = 1024
            max_port = 65535
            if not (min_port <= v <= max_port):
                msg = f"Port must be between {min_port} and {max_port}"
                raise ValueError(msg)
            return v

    class ClientConfig(BaseModel):
        """gRPC client configuration model."""

        target: str = Field(description="Target server address")
        timeout: float = Field(
            default=FlextConstants.Network.DEFAULT_TIMEOUT,
            description="Request timeout",
        )
        retry_attempts: int = Field(default=3, description="Maximum retry attempts")

        @field_validator("target")
        @classmethod
        def validate_target(cls, v: str) -> str:
            """Validate target address is not empty."""
            if not v or not v.strip():
                msg = "Target cannot be empty"
                raise ValueError(msg)
            return v.strip()

    class ChannelConfig(BaseModel):
        """gRPC channel configuration model."""

        address: str = Field(description="Channel target address")
        options: dict[str, object] | None = Field(
            default=None, description="Channel options"
        )
        credentials: str | None = Field(default=None, description="Channel credentials")

    # Stream Management Models
    class StreamInfo(BaseModel):
        """Comprehensive stream information tracking model."""

        stream_id: str = Field(description="Unique stream identifier")
        stream_type: str = Field(
            description="Type of stream (unary, server, client, bidirectional)"
        )
        created_at: datetime = Field(
            default_factory=datetime.now, description="Stream creation timestamp"
        )
        active: bool = Field(default=True, description="Stream active status")
        target: str = Field(description="Target service endpoint")

        # Performance metrics
        sequence_counter: int = Field(default=0, description="Message sequence counter")
        total_requests_sent: int = Field(default=0, description="Total requests sent")
        total_responses_received: int = Field(
            default=0, description="Total responses received"
        )
        bytes_sent: int = Field(default=0, description="Total bytes sent")
        bytes_received: int = Field(default=0, description="Total bytes received")
        error_count: int = Field(default=0, description="Total error count")
        average_latency_ms: float = Field(
            default=0.0, description="Average latency in milliseconds"
        )

        # Health and status
        health_status: str = Field(
            default="healthy", description="Stream health status"
        )
        last_activity: datetime | None = Field(
            default=None, description="Last activity timestamp"
        )
        last_health_check: datetime | None = Field(
            default=None, description="Last health check"
        )

    class StreamMetrics(BaseModel):
        """Stream performance metrics model."""

        stream_id: str = Field(description="Associated stream identifier")
        throughput_rps: float = Field(default=0.0, description="Requests per second")
        latency_p50: float = Field(default=0.0, description="50th percentile latency")
        latency_p95: float = Field(default=0.0, description="95th percentile latency")
        latency_p99: float = Field(default=0.0, description="99th percentile latency")
        error_rate: float = Field(default=0.0, description="Error rate percentage")
        memory_usage_bytes: int = Field(default=0, description="Memory usage in bytes")

    # Service and Entity Models
    class ServiceDefinition(BaseModel):
        """gRPC service definition model."""

        service_name: str = Field(description="Service name")
        methods: list[str] = Field(
            default_factory=list, description="Available service methods"
        )
        package: str | None = Field(default=None, description="Service package name")
        version: str | None = Field(default=None, description="Service version")

    class ServerEntity(BaseModel):
        """gRPC server entity model."""

        server_id: str = Field(description="Unique server identifier")
        address: str = Field(description="Server address")
        status: str = Field(default="stopped", description="Server status")
        services: list[dict[str, str | list[str] | dict[str, object]]] = Field(
            default_factory=list, description="Registered services"
        )
        created_at: datetime = Field(
            default_factory=datetime.now, description="Server creation time"
        )
        started_at: datetime | None = Field(
            default=None, description="Server start time"
        )

    class ClientEntity(BaseModel):
        """gRPC client entity model."""

        client_id: str = Field(description="Unique client identifier")
        target: str = Field(description="Target server address")
        status: str = Field(
            default="disconnected", description="Client connection status"
        )
        created_at: datetime = Field(
            default_factory=datetime.now, description="Client creation time"
        )
        connected_at: datetime | None = Field(
            default=None, description="Connection time"
        )

    class ChannelEntity(BaseModel):
        """gRPC channel entity model."""

        channel_id: str = Field(description="Unique channel identifier")
        target: str = Field(description="Channel target address")
        state: str = Field(default="idle", description="Channel state")
        created_at: datetime = Field(
            default_factory=datetime.now, description="Channel creation time"
        )

    # Request/Response Models
    class GrpcRequest(BaseModel):
        """Generic gRPC request model."""

        request_id: str = Field(description="Unique request identifier")
        method: str = Field(description="gRPC method name")
        payload: dict[str, object] = Field(
            default_factory=dict, description="Request payload"
        )
        metadata: dict[str, str] = Field(
            default_factory=dict, description="Request metadata"
        )
        timeout: float | None = Field(
            default=None, description="Request timeout override"
        )

    class GrpcResponse(BaseModel):
        """Generic gRPC response model."""

        request_id: str = Field(description="Associated request identifier")
        success: bool = Field(description="Response success status")
        payload: dict[str, object] | None = Field(
            default=None, description="Response payload"
        )
        error: str | None = Field(default=None, description="Error message if failed")
        metadata: dict[str, str] = Field(
            default_factory=dict, description="Response metadata"
        )
        duration_ms: float | None = Field(
            default=None, description="Request duration in milliseconds"
        )

    # Health and Monitoring Models
    class GrpcHealthCheck(BaseModel):
        """gRPC service health check model."""

        service_name: str = Field(description="Service being checked")
        status: str = Field(description="Health status (serving, not_serving, unknown)")
        timestamp: datetime = Field(
            default_factory=datetime.now, description="Health check timestamp"
        )
        details: str | None = Field(
            default=None, description="Additional health details"
        )

    class ServiceMetrics(BaseModel):
        """gRPC service metrics model."""

        service_name: str = Field(description="Service name")
        total_requests: int = Field(default=0, description="Total requests processed")
        successful_requests: int = Field(default=0, description="Successful requests")
        failed_requests: int = Field(default=0, description="Failed requests")
        average_response_time_ms: float = Field(
            default=0.0, description="Average response time"
        )
        active_connections: int = Field(
            default=0, description="Currently active connections"
        )

    # Platform Integration Models
    class PlatformConfig(BaseModel):
        """gRPC platform configuration model."""

        enable_reflection: bool = Field(
            default=False, description="Enable gRPC reflection"
        )
        enable_health_check: bool = Field(
            default=True, description="Enable health checking"
        )
        max_concurrent_streams: int = Field(
            default=100, description="Maximum concurrent streams"
        )
        keepalive_time_ms: int = Field(
            default=FlextGrpcConstants.DEFAULT_KEEPALIVE_TIME_MS,
            description="Keepalive time in milliseconds",
        )
        keepalive_timeout_ms: int = Field(
            default=FlextGrpcConstants.DEFAULT_KEEPALIVE_TIMEOUT_MS,
            description="Keepalive timeout in milliseconds",
        )
