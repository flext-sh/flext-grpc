"""Module docstring."""

from __future__ import annotations

"""Models for gRPC operations.

This module provides data models for gRPC operations.
"""

from datetime import datetime

from pydantic import Field, field_validator

from flext_core import FlextModels


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
    class ServerConfig(FlextModels.BaseConfig):
        """gRPC server configuration model."""

        host: str = Field(default="localhost", description="Server host address")
        port: int = Field(default=50051, description="Server port number")
        max_workers: int = Field(default=10, description="Maximum worker threads")
        timeout: float = Field(default=30.0, description="Request timeout in seconds")

        @field_validator("port")
        @classmethod
        def validate_port(cls, v: int) -> int:
            if not (1024 <= v <= 65535):
                msg = "Port must be between 1024 and 65535"
                raise ValueError(msg)
            return v

    class ClientConfig(FlextModels.BaseConfig):
        """gRPC client configuration model."""

        target: str = Field(description="Target server address")
        timeout: float = Field(default=30.0, description="Request timeout")
        retry_attempts: int = Field(default=3, description="Maximum retry attempts")

        @field_validator("target")
        @classmethod
        def validate_target(cls, v: str) -> str:
            if not v or not v.strip():
                msg = "Target cannot be empty"
                raise ValueError(msg)
            return v.strip()

    class ChannelConfig(FlextModels.BaseConfig):
        """gRPC channel configuration model."""

        address: str = Field(description="Channel target address")
        options: dict[str, object] | None = Field(
            default=None, description="Channel options"
        )
        credentials: str | None = Field(default=None, description="Channel credentials")

    # Stream Management Models
    class StreamInfo(FlextModels.BaseModel):
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

    class StreamMetrics(FlextModels.BaseModel):
        """Stream performance metrics model."""

        stream_id: str = Field(description="Associated stream identifier")
        throughput_rps: float = Field(default=0.0, description="Requests per second")
        latency_p50: float = Field(default=0.0, description="50th percentile latency")
        latency_p95: float = Field(default=0.0, description="95th percentile latency")
        latency_p99: float = Field(default=0.0, description="99th percentile latency")
        error_rate: float = Field(default=0.0, description="Error rate percentage")
        memory_usage_bytes: int = Field(default=0, description="Memory usage in bytes")

    # Service and Entity Models
    class ServiceDefinition(FlextModels.BaseModel):
        """gRPC service definition model."""

        service_name: str = Field(description="Service name")
        methods: list[str] = Field(
            default_factory=list, description="Available service methods"
        )
        package: str | None = Field(default=None, description="Service package name")
        version: str | None = Field(default=None, description="Service version")

    class ServerEntity(FlextModels.BaseModel):
        """gRPC server entity model."""

        server_id: str = Field(description="Unique server identifier")
        address: str = Field(description="Server address")
        status: str = Field(default="stopped", description="Server status")
        services: list[ServiceDefinition] = Field(
            default_factory=list, description="Registered services"
        )
        created_at: datetime = Field(
            default_factory=datetime.now, description="Server creation time"
        )
        started_at: datetime | None = Field(
            default=None, description="Server start time"
        )

    class ClientEntity(FlextModels.BaseModel):
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

    class ChannelEntity(FlextModels.BaseModel):
        """gRPC channel entity model."""

        channel_id: str = Field(description="Unique channel identifier")
        target: str = Field(description="Channel target address")
        state: str = Field(default="idle", description="Channel state")
        created_at: datetime = Field(
            default_factory=datetime.now, description="Channel creation time"
        )

    # Request/Response Models
    class GrpcRequest(FlextModels.BaseModel):
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

    class GrpcResponse(FlextModels.BaseModel):
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
    class HealthCheck(FlextModels.BaseModel):
        """gRPC service health check model."""

        service_name: str = Field(description="Service being checked")
        status: str = Field(description="Health status (serving, not_serving, unknown)")
        timestamp: datetime = Field(
            default_factory=datetime.now, description="Health check timestamp"
        )
        details: str | None = Field(
            default=None, description="Additional health details"
        )

    class ServiceMetrics(FlextModels.BaseModel):
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
    class PlatformConfig(FlextModels.BaseConfig):
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
            default=30000, description="Keepalive time in milliseconds"
        )
        keepalive_timeout_ms: int = Field(
            default=5000, description="Keepalive timeout in milliseconds"
        )

    # Type aliases for backward compatibility and convenience
    GrpcMessage = dict[str, object]
    GrpcMessages = list[GrpcMessage]
    FlextGrpcChannel = object  # Placeholder for gRPC channel type
