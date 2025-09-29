"""Models for gRPC operations.

This module provides data models for gRPC operations.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Self

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    computed_field,
    field_serializer,
    field_validator,
    model_validator,
)

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

    # Advanced Pydantic 2.11 configuration for comprehensive gRPC model behavior
    model_config = ConfigDict(
        validate_assignment=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
        extra="forbid",
        frozen=False,
        validate_return=True,
        ser_json_timedelta="iso8601",
        ser_json_bytes="base64",
        hide_input_in_errors=True,
        json_schema_extra={
            "title": "FlextGrpcModels",
            "description": "Comprehensive gRPC domain models with advanced Pydantic 2.11 features",
            "examples": [
                {
                    "server_config": {
                        "host": "localhost",
                        "port": 50051,
                        "max_workers": 10,
                    }
                }
            ],
        },
    )

    @computed_field
    @property
    def active_grpc_models_count(self) -> int:
        """Computed field returning the number of active gRPC model types."""
        # Count all nested gRPC model classes
        grpc_model_classes = [
            "ServerConfig",
            "ClientConfig",
            "ChannelConfig",
            "StreamInfo",
            "StreamMetrics",
            "ServiceDefinition",
            "ServerEntity",
            "ClientEntity",
            "ChannelEntity",
            "GrpcRequest",
            "GrpcResponse",
            "GrpcHealthCheck",
            "ServiceMetrics",
            "PlatformConfig",
        ]
        return len(grpc_model_classes)

    @computed_field
    @property
    def grpc_model_summary(self) -> dict[str, str]:
        """Computed field returning a summary of all available gRPC models."""
        return {
            "ServerConfig": "gRPC server configuration with validation",
            "ClientConfig": "gRPC client configuration and connection settings",
            "ChannelConfig": "gRPC channel configuration and options",
            "StreamInfo": "Stream management and monitoring information",
            "StreamMetrics": "Performance metrics for gRPC streams",
            "ServiceDefinition": "gRPC service definition and method registry",
            "ServerEntity": "gRPC server entity with lifecycle management",
            "ClientEntity": "gRPC client entity with connection tracking",
            "ChannelEntity": "gRPC channel entity with state management",
            "GrpcRequest": "Generic gRPC request model with metadata",
            "GrpcResponse": "Generic gRPC response model with error handling",
            "GrpcHealthCheck": "gRPC service health monitoring",
            "ServiceMetrics": "Service-level performance metrics",
            "PlatformConfig": "Platform-wide gRPC configuration settings",
        }

    @model_validator(mode="after")
    def validate_grpc_models_consistency(self) -> Self:
        """Cross-model validation ensuring gRPC models consistency."""
        # Ensure all required nested gRPC classes are properly defined
        required_grpc_classes = [
            "ServerConfig",
            "ClientConfig",
            "ChannelConfig",
            "StreamInfo",
            "ServiceDefinition",
            "GrpcRequest",
            "GrpcResponse",
        ]

        for class_name in required_grpc_classes:
            if not hasattr(self.__class__, class_name):
                error_message = f"Required gRPC nested class {class_name} not found"
                raise ValueError(error_message)

        return self

    @field_serializer("grpc_model_summary")
    def serialize_grpc_model_summary(
        self, value: dict[str, str], _info: object
    ) -> dict[str, dict[str, int | str] | str]:
        """Serialize gRPC model summary with additional metadata."""
        return {
            **value,
            "_grpc_metadata": {
                "generated_at": datetime.now(UTC).isoformat(),
                "total_grpc_models": len(value),
                "serialization_version": "2.11",
                "grpc_protocol_version": "3.0",
                "flext_ecosystem_version": "1.0.0",
            },
        }

    # Core gRPC Configuration Models
    class ServerConfig(BaseModel):
        """gRPC server configuration model."""

        model_config = ConfigDict(
            validate_assignment=True,
            use_enum_values=True,
            arbitrary_types_allowed=True,
            extra="forbid",
            validate_return=True,
        )

        host: str = Field(
            default=FlextConstants.Platform.DEFAULT_HOST,
            description="Server host address",
        )
        port: int = Field(
            default=FlextGrpcConstants.DEFAULT_GRPC_PORT,
            description="Server port number",
        )
        max_workers: int = Field(
            default=FlextGrpcConstants.DEFAULT_MAX_WORKERS,
            description="Maximum worker threads",
        )
        timeout: float = Field(
            default=FlextConstants.Network.DEFAULT_TIMEOUT,
            description="Request timeout in seconds",
        )

        @computed_field
        @property
        def server_address(self) -> str:
            """Computed field for complete server address."""
            return f"{self.host}:{self.port}"

        @computed_field
        @property
        def server_summary(self) -> dict[str, object]:
            """Computed field for server configuration summary."""
            return {
                "address": self.server_address,
                "max_workers": self.max_workers,
                "timeout_seconds": self.timeout,
                "is_production_ready": self.port >= FlextGrpcConstants.GRPC_DEFAULT_PORT
                and self.max_workers >= FlextGrpcConstants.PRODUCTION_MIN_WORKERS,
            }

        @model_validator(mode="after")
        def validate_server_config_consistency(self) -> Self:
            """Cross-field validation for server configuration."""
            # Production servers should use secure ports
            if (
                self.host != "localhost"
                and self.port < FlextGrpcConstants.PRODUCTION_MIN_PORT
            ):
                error_message = "Production servers should use ports >= 1024"
                raise ValueError(error_message)

            # High worker count should have appropriate timeout
            if (
                self.max_workers > FlextGrpcConstants.HIGH_WORKER_THRESHOLD
                and self.timeout < FlextGrpcConstants.HIGH_WORKER_TIMEOUT
            ):
                error_message = "High worker count should have timeout >= 30 seconds"
                raise ValueError(error_message)

            return self

        @field_serializer("host")
        def serialize_host(self, value: str, _info: object) -> str:
            """Serialize host with security considerations."""
            # Mask internal network addresses in logs
            if value.startswith(("192.168.", "10.")):
                return "***INTERNAL_ADDRESS***"
            return value

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

        @field_validator("max_workers")
        @classmethod
        def validate_max_workers(cls, v: int) -> int:
            """Validate max_workers is within valid range."""
            min_workers = 1
            max_workers = 100
            if not (min_workers <= v <= max_workers):
                msg = f"Max workers must be between {min_workers} and {max_workers}"
                raise ValueError(msg)
            return v

    class ClientConfig(BaseModel):
        """gRPC client configuration model."""

        model_config = ConfigDict(
            validate_assignment=True,
            use_enum_values=True,
            arbitrary_types_allowed=True,
            extra="forbid",
            validate_return=True,
        )

        target: str = Field(description="Target server address")
        timeout: float = Field(
            default=FlextConstants.Network.DEFAULT_TIMEOUT,
            description="Request timeout",
        )
        retry_attempts: int = Field(
            default=FlextConstants.Reliability.MAX_RETRY_ATTEMPTS,
            description="Maximum retry attempts",
        )

        @computed_field
        @property
        def client_summary(self) -> dict[str, object]:
            """Computed field for client configuration summary."""
            return {
                "target": self.target,
                "timeout_seconds": self.timeout,
                "retry_attempts": self.retry_attempts,
                "is_configured_for_production": self.retry_attempts
                >= FlextGrpcConstants.PRODUCTION_RETRY_ATTEMPTS
                and self.timeout >= FlextGrpcConstants.PRODUCTION_RETRY_TIMEOUT,
            }

        @computed_field
        @property
        def estimated_max_duration_seconds(self) -> float:
            """Computed field for maximum estimated request duration."""
            return self.timeout * (self.retry_attempts + 1)

        @model_validator(mode="after")
        def validate_client_consistency(self) -> Self:
            """Cross-field validation for client configuration."""
            # Retry attempts should have reasonable timeout
            if (
                self.retry_attempts > FlextGrpcConstants.MAX_RETRY_ATTEMPTS
                and self.timeout < FlextGrpcConstants.HIGH_RETRY_TIMEOUT
            ):
                error_message = "High retry attempts should have timeout >= 10 seconds"
                raise ValueError(error_message)

            return self

        @field_serializer("target")
        def serialize_target(self, value: str, _info: object) -> str:
            """Serialize target with security masking."""
            # Mask sensitive server addresses
            if "secret" in value.lower() or "internal" in value.lower():
                return "***PROTECTED_TARGET***"
            return value

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

        model_config = ConfigDict(
            validate_assignment=True,
            use_enum_values=True,
            arbitrary_types_allowed=True,
            extra="forbid",
            validate_return=True,
        )

        address: str = Field(description="Channel target address")
        options: dict[str, object] | None = Field(
            default=None, description="Channel options"
        )
        credentials: str | None = Field(default=None, description="Channel credentials")

        @computed_field
        @property
        def channel_summary(self) -> dict[str, object]:
            """Computed field for channel configuration summary."""
            return {
                "address": self.address,
                "has_options": self.options is not None,
                "has_credentials": self.credentials is not None,
                "options_count": len(self.options) if self.options else 0,
                "is_secure": self.credentials is not None,
            }

        @model_validator(mode="after")
        def validate_channel_consistency(self) -> Self:
            """Cross-field validation for channel configuration."""
            # Production channels should have credentials
            if not self.address.startswith("localhost") and not self.credentials:
                error_message = "Production channels should have credentials"
                raise ValueError(error_message)

            return self

        @field_serializer("credentials")
        def serialize_credentials(self, value: str | None, _info: object) -> str | None:
            """Serialize credentials with security masking."""
            if value:
                return "***CREDENTIALS_SET***"
            return value

    # Stream Management Models
    class StreamInfo(BaseModel):
        """Comprehensive stream information tracking model."""

        model_config = ConfigDict(
            validate_assignment=True,
            use_enum_values=True,
            arbitrary_types_allowed=True,
            extra="forbid",
            validate_return=True,
        )

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

        @computed_field
        @property
        def stream_age_seconds(self) -> float:
            """Computed field for stream age in seconds."""
            return (datetime.now(UTC) - self.created_at).total_seconds()

        @computed_field
        @property
        def stream_performance_summary(self) -> dict[str, object]:
            """Computed field for stream performance metrics."""
            success_rate = (
                (
                    (self.total_responses_received - self.error_count)
                    / self.total_responses_received
                    * 100
                )
                if self.total_responses_received > 0
                else 0.0
            )
            return {
                "stream_id": self.stream_id,
                "stream_type": self.stream_type,
                "success_rate_percent": round(success_rate, 2),
                "throughput_messages_per_second": (
                    self.total_requests_sent / self.stream_age_seconds
                    if self.stream_age_seconds > 0
                    else 0.0
                ),
                "average_latency_ms": self.average_latency_ms,
                "is_healthy": self.health_status == "healthy" and self.active,
                "age_seconds": self.stream_age_seconds,
            }

        @model_validator(mode="after")
        def validate_stream_consistency(self) -> Self:
            """Cross-field validation for stream consistency."""
            # Error count cannot exceed total responses
            if self.error_count > self.total_responses_received:
                error_message = "Error count cannot exceed total responses received"
                raise ValueError(error_message)

            # Bytes sent/received should be reasonable for request/response counts
            if self.total_requests_sent > 0:
                avg_bytes_per_request = self.bytes_sent / self.total_requests_sent
                max_bytes_per_request = (
                    FlextGrpcConstants.MAX_REQUEST_SIZE_MB * 1024 * 1024
                )
                if avg_bytes_per_request > max_bytes_per_request:
                    error_message = f"Average bytes per request seems excessive (>{FlextGrpcConstants.MAX_REQUEST_SIZE_MB}MB)"
                    raise ValueError(error_message)

            return self

        @field_serializer("target")
        def serialize_stream_target(self, value: str, _info: object) -> str:
            """Serialize stream target with security considerations."""
            # Mask internal service endpoints
            if "internal" in value.lower() or "private" in value.lower():
                return "***INTERNAL_ENDPOINT***"
            return value

    class StreamMetrics(BaseModel):
        """Stream performance metrics model."""

        model_config = ConfigDict(
            validate_assignment=True,
            use_enum_values=True,
            arbitrary_types_allowed=True,
            extra="forbid",
            validate_return=True,
        )

        stream_id: str = Field(description="Associated stream identifier")
        throughput_rps: float = Field(default=0.0, description="Requests per second")
        latency_p50: float = Field(default=0.0, description="50th percentile latency")
        latency_p95: float = Field(default=0.0, description="95th percentile latency")
        latency_p99: float = Field(default=0.0, description="99th percentile latency")
        error_rate: float = Field(default=0.0, description="Error rate percentage")
        memory_usage_bytes: int = Field(default=0, description="Memory usage in bytes")

        @computed_field
        @property
        def performance_grade(self) -> str:
            """Computed field for performance grade based on metrics."""
            if (
                self.latency_p95 < FlextGrpcConstants.PERFORMANCE_EXCELLENT_LATENCY_MS
                and self.error_rate
                < FlextGrpcConstants.PERFORMANCE_EXCELLENT_ERROR_RATE
            ):
                return "excellent"
            if (
                self.latency_p95 < FlextGrpcConstants.PERFORMANCE_GOOD_LATENCY_MS
                and self.error_rate < FlextGrpcConstants.PERFORMANCE_GOOD_ERROR_RATE
            ):
                return "good"
            if (
                self.latency_p95 < FlextGrpcConstants.PERFORMANCE_ACCEPTABLE_LATENCY_MS
                and self.error_rate
                < FlextGrpcConstants.PERFORMANCE_ACCEPTABLE_ERROR_RATE
            ):
                return "acceptable"
            return "poor"

        @computed_field
        @property
        def metrics_summary(self) -> dict[str, object]:
            """Computed field for comprehensive metrics summary."""
            return {
                "throughput_rps": self.throughput_rps,
                "latency_p95_ms": self.latency_p95,
                "error_rate_percent": self.error_rate,
                "memory_usage_mb": round(self.memory_usage_bytes / 1024 / 1024, 2),
                "performance_grade": self.performance_grade,
                "is_healthy": self.performance_grade in {"excellent", "good"},
            }

        @model_validator(mode="after")
        def validate_metrics_consistency(self) -> Self:
            """Cross-field validation for metrics consistency."""
            # Latency percentiles should be in ascending order
            if not (self.latency_p50 <= self.latency_p95 <= self.latency_p99):
                error_message = (
                    "Latency percentiles must be in ascending order (p50 <= p95 <= p99)"
                )
                raise ValueError(error_message)

            # Error rate should be between 0 and 100
            if not (
                0.0 <= self.error_rate <= FlextGrpcConstants.MAX_ERROR_RATE_PERCENT
            ):
                error_message = f"Error rate must be between 0 and {FlextGrpcConstants.MAX_ERROR_RATE_PERCENT} percent"
                raise ValueError(error_message)

            return self

    # Service and Entity Models
    class ServiceDefinition(BaseModel):
        """gRPC service definition model."""

        model_config = ConfigDict(
            validate_assignment=True,
            use_enum_values=True,
            arbitrary_types_allowed=True,
            extra="forbid",
            validate_return=True,
        )

        service_name: str = Field(description="Service name")
        methods: list[str] = Field(
            default_factory=list, description="Available service methods"
        )
        package: str | None = Field(default=None, description="Service package name")
        version: str | None = Field(default=None, description="Service version")

        @computed_field
        @property
        def service_summary(self) -> dict[str, object]:
            """Computed field for service definition summary."""
            return {
                "service_name": self.service_name,
                "methods_count": len(self.methods),
                "has_package": self.package is not None,
                "has_version": self.version is not None,
                "methods": self.methods,
                "is_complete": bool(self.service_name and self.methods),
            }

        @model_validator(mode="after")
        def validate_service_definition(self) -> Self:
            """Cross-field validation for service definition."""
            # Service should have at least one method
            if not self.methods:
                error_message = "Service definition should have at least one method"
                raise ValueError(error_message)

            # Method names should follow naming conventions
            for method in self.methods:
                if not method or not method[0].isupper():
                    error_message = (
                        f"Method '{method}' should start with uppercase letter"
                    )
                    raise ValueError(error_message)

            return self

    class ServerEntity(BaseModel):
        """gRPC server entity model."""

        model_config = ConfigDict(
            validate_assignment=True,
            use_enum_values=True,
            arbitrary_types_allowed=True,
            extra="forbid",
            validate_return=True,
        )

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

        @computed_field
        @property
        def server_uptime_seconds(self) -> float | None:
            """Computed field for server uptime in seconds."""
            if self.started_at and self.status == "running":
                return (datetime.now(UTC) - self.started_at).total_seconds()
            return None

        @computed_field
        @property
        def server_entity_summary(self) -> dict[str, object]:
            """Computed field for server entity summary."""
            return {
                "server_id": self.server_id,
                "address": self.address,
                "status": self.status,
                "services_count": len(self.services),
                "uptime_seconds": self.server_uptime_seconds,
                "is_running": self.status == "running",
                "has_services": len(self.services) > 0,
            }

        @model_validator(mode="after")
        def validate_server_entity(self) -> Self:
            """Cross-field validation for server entity."""
            # Running servers should have started_at timestamp
            if self.status == "running" and not self.started_at:
                error_message = "Running servers must have started_at timestamp"
                raise ValueError(error_message)

            # Started servers should have created_at before started_at
            if self.started_at and self.started_at < self.created_at:
                error_message = "started_at cannot be before created_at"
                raise ValueError(error_message)

            return self

    class ClientEntity(BaseModel):
        """gRPC client entity model."""

        model_config = ConfigDict(
            validate_assignment=True,
            use_enum_values=True,
            arbitrary_types_allowed=True,
            extra="forbid",
            validate_return=True,
        )

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

        @computed_field
        @property
        def connection_duration_seconds(self) -> float | None:
            """Computed field for connection duration in seconds."""
            if self.connected_at and self.status == "connected":
                return (datetime.now(UTC) - self.connected_at).total_seconds()
            return None

        @computed_field
        @property
        def client_entity_summary(self) -> dict[str, object]:
            """Computed field for client entity summary."""
            return {
                "client_id": self.client_id,
                "target": self.target,
                "status": self.status,
                "connection_duration_seconds": self.connection_duration_seconds,
                "is_connected": self.status == "connected",
                "has_connection_time": self.connected_at is not None,
            }

        @model_validator(mode="after")
        def validate_client_entity(self) -> Self:
            """Cross-field validation for client entity."""
            # Connected clients should have connected_at timestamp
            if self.status == "connected" and not self.connected_at:
                error_message = "Connected clients must have connected_at timestamp"
                raise ValueError(error_message)

            return self

    class ChannelEntity(BaseModel):
        """gRPC channel entity model."""

        model_config = ConfigDict(
            validate_assignment=True,
            use_enum_values=True,
            arbitrary_types_allowed=True,
            extra="forbid",
            validate_return=True,
        )

        channel_id: str = Field(description="Unique channel identifier")
        target: str = Field(description="Channel target address")
        state: str = Field(default="idle", description="Channel state")
        created_at: datetime = Field(
            default_factory=datetime.now, description="Channel creation time"
        )

        @computed_field
        @property
        def channel_age_seconds(self) -> float:
            """Computed field for channel age in seconds."""
            return (datetime.now(UTC) - self.created_at).total_seconds()

        @computed_field
        @property
        def channel_entity_summary(self) -> dict[str, object]:
            """Computed field for channel entity summary."""
            return {
                "channel_id": self.channel_id,
                "target": self.target,
                "state": self.state,
                "age_seconds": self.channel_age_seconds,
                "is_ready": self.state == "ready",
                "is_active": self.state in {"connecting", "ready"},
            }

    # Request/Response Models
    class GrpcRequest(BaseModel):
        """Generic gRPC request model."""

        model_config = ConfigDict(
            validate_assignment=True,
            use_enum_values=True,
            arbitrary_types_allowed=True,
            extra="forbid",
            validate_return=True,
        )

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

        @computed_field
        @property
        def request_summary(self) -> dict[str, object]:
            """Computed field for request summary."""
            return {
                "request_id": self.request_id,
                "method": self.method,
                "payload_size": len(str(self.payload)),
                "metadata_count": len(self.metadata),
                "has_timeout": self.timeout is not None,
                "has_payload": bool(self.payload),
            }

        @field_serializer("payload")
        def serialize_payload(
            self, value: dict[str, object], _info: object
        ) -> dict[str, object]:
            """Serialize payload with sensitive data masking."""
            # Mask sensitive keys in payload
            sensitive_keys = {
                "password",
                "token",
                "secret",
                "key",
                "auth",
                "credential",
            }
            return {
                k: (
                    "***MASKED***"
                    if any(sens in k.lower() for sens in sensitive_keys)
                    else v
                )
                for k, v in value.items()
            }

    class GrpcResponse(BaseModel):
        """Generic gRPC response model."""

        model_config = ConfigDict(
            validate_assignment=True,
            use_enum_values=True,
            arbitrary_types_allowed=True,
            extra="forbid",
            validate_return=True,
        )

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

        @computed_field
        @property
        def response_summary(self) -> dict[str, object]:
            """Computed field for response summary."""
            return {
                "request_id": self.request_id,
                "success": self.success,
                "has_payload": self.payload is not None,
                "has_error": self.error is not None,
                "duration_ms": self.duration_ms,
                "metadata_count": len(self.metadata),
                "response_size": len(str(self.payload)) if self.payload else 0,
            }

        @model_validator(mode="after")
        def validate_response_consistency(self) -> Self:
            """Cross-field validation for response consistency."""
            # Failed responses should have error message
            if not self.success and not self.error:
                error_message = "Failed responses must have error message"
                raise ValueError(error_message)

            # Successful responses should not have error message
            if self.success and self.error:
                error_message = "Successful responses should not have error message"
                raise ValueError(error_message)

            return self

        @field_serializer("payload")
        def serialize_response_payload(
            self, value: dict[str, object] | None, _info: object
        ) -> dict[str, object] | None:
            """Serialize response payload with sensitive data masking."""
            if not value:
                return value

            # Mask sensitive keys in response payload
            sensitive_keys = {
                "password",
                "token",
                "secret",
                "key",
                "auth",
                "credential",
            }
            return {
                k: (
                    "***MASKED***"
                    if any(sens in k.lower() for sens in sensitive_keys)
                    else v
                )
                for k, v in value.items()
            }

    # Health and Monitoring Models
    class GrpcHealthCheck(BaseModel):
        """gRPC service health check model."""

        model_config = ConfigDict(
            validate_assignment=True,
            use_enum_values=True,
            arbitrary_types_allowed=True,
            extra="forbid",
            validate_return=True,
        )

        service_name: str = Field(description="Service being checked")
        status: str = Field(description="Health status (serving, not_serving, unknown)")
        timestamp: datetime = Field(
            default_factory=datetime.now, description="Health check timestamp"
        )
        details: str | None = Field(
            default=None, description="Additional health details"
        )

        @computed_field
        @property
        def health_check_age_seconds(self) -> float:
            """Computed field for health check age in seconds."""
            return (datetime.now(UTC) - self.timestamp).total_seconds()

        @computed_field
        @property
        def health_summary(self) -> dict[str, object]:
            """Computed field for health check summary."""
            return {
                "service_name": self.service_name,
                "status": self.status,
                "is_healthy": self.status == "serving",
                "age_seconds": self.health_check_age_seconds,
                "has_details": self.details is not None,
                "is_recent": self.health_check_age_seconds
                < FlextGrpcConstants.HEALTH_CHECK_AGE_RECENT_SECONDS,
            }

        @model_validator(mode="after")
        def validate_health_check(self) -> Self:
            """Cross-field validation for health check."""
            valid_statuses = {"serving", "not_serving", "unknown"}
            if self.status not in valid_statuses:
                error_message = (
                    f"Invalid health status: {self.status}. Valid: {valid_statuses}"
                )
                raise ValueError(error_message)

            return self

    class ServiceMetrics(BaseModel):
        """gRPC service metrics model."""

        model_config = ConfigDict(
            validate_assignment=True,
            use_enum_values=True,
            arbitrary_types_allowed=True,
            extra="forbid",
            validate_return=True,
        )

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

        @computed_field
        @property
        def success_rate_percent(self) -> float:
            """Computed field for success rate percentage."""
            if self.total_requests == 0:
                return 0.0
            return (self.successful_requests / self.total_requests) * 100

        @computed_field
        @property
        def service_metrics_summary(self) -> dict[str, object]:
            """Computed field for service metrics summary."""
            return {
                "service_name": self.service_name,
                "total_requests": self.total_requests,
                "success_rate_percent": round(self.success_rate_percent, 2),
                "average_response_time_ms": self.average_response_time_ms,
                "active_connections": self.active_connections,
                "failed_requests": self.failed_requests,
                "is_healthy": self.success_rate_percent
                > FlextGrpcConstants.SUCCESS_RATE_HEALTHY_PERCENT
                and self.average_response_time_ms
                < FlextGrpcConstants.RESPONSE_TIME_HEALTHY_MS,
            }

        @model_validator(mode="after")
        def validate_service_metrics(self) -> Self:
            """Cross-field validation for service metrics."""
            # Total requests should equal successful + failed
            if self.total_requests != (self.successful_requests + self.failed_requests):
                error_message = (
                    "Total requests should equal successful + failed requests"
                )
                raise ValueError(error_message)

            # Active connections should be non-negative
            if self.active_connections < 0:
                error_message = "Active connections cannot be negative"
                raise ValueError(error_message)

            return self

    # Platform Integration Models
    class PlatformConfig(BaseModel):
        """gRPC platform configuration model."""

        model_config = ConfigDict(
            validate_assignment=True,
            use_enum_values=True,
            arbitrary_types_allowed=True,
            extra="forbid",
            validate_return=True,
        )

        enable_reflection: bool = Field(
            default=False, description="Enable gRPC reflection"
        )
        enable_health_check: bool = Field(
            default=True, description="Enable health checking"
        )
        max_concurrent_streams: int = Field(
            default=FlextGrpcConstants.PRODUCTION_MIN_CONCURRENT_STREAMS,
            description="Maximum concurrent streams",
        )
        keepalive_time_ms: int = Field(
            default=FlextGrpcConstants.DEFAULT_KEEPALIVE_TIME_MS,
            description="Keepalive time in milliseconds",
        )
        keepalive_timeout_ms: int = Field(
            default=FlextGrpcConstants.DEFAULT_KEEPALIVE_TIMEOUT_MS,
            description="Keepalive timeout in milliseconds",
        )

        @computed_field
        @property
        def platform_config_summary(self) -> dict[str, object]:
            """Computed field for platform configuration summary."""
            return {
                "enable_reflection": self.enable_reflection,
                "enable_health_check": self.enable_health_check,
                "max_concurrent_streams": self.max_concurrent_streams,
                "keepalive_time_seconds": self.keepalive_time_ms / 1000,
                "keepalive_timeout_seconds": self.keepalive_timeout_ms / 1000,
                "is_production_ready": (
                    self.enable_health_check
                    and self.max_concurrent_streams
                    >= FlextGrpcConstants.PRODUCTION_MIN_CONCURRENT_STREAMS
                    and self.keepalive_time_ms
                    >= FlextGrpcConstants.PRODUCTION_MIN_KEEPALIVE_TIME_MS
                ),
            }

        @model_validator(mode="after")
        def validate_platform_config(self) -> Self:
            """Cross-field validation for platform configuration."""
            # Keepalive timeout should be less than keepalive time
            if self.keepalive_timeout_ms >= self.keepalive_time_ms:
                error_message = "Keepalive timeout should be less than keepalive time"
                raise ValueError(error_message)

            # Max concurrent streams should be reasonable
            if (
                self.max_concurrent_streams
                > FlextGrpcConstants.MAX_CONCURRENT_STREAMS_LIMIT
            ):
                error_message = f"Max concurrent streams seems excessive (>{FlextGrpcConstants.MAX_CONCURRENT_STREAMS_LIMIT})"
                raise ValueError(error_message)

            return self

        @field_serializer("keepalive_time_ms", "keepalive_timeout_ms")
        def serialize_keepalive_values(
            self, value: int, _info: object
        ) -> dict[str, object]:
            """Serialize keepalive values with human-readable format."""
            return {
                "milliseconds": value,
                "seconds": value / 1000,
                "human_readable": f"{value / 1000}s",
            }
