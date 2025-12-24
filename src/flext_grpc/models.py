"""FLEXT gRPC Models - Consolidated Pydantic v2 Models.

Unified namespace with nested classes following FLEXT principles and SOLID design.
All domain models consolidated into a single class with nested structures.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from datetime import datetime
from typing import TypeVar

from flext_core._models.entity import FlextModelsEntity
from pydantic import BaseModel, Field, computed_field, field_validator

from flext import (
    FlextModels as m_core,
    FlextResult as r,
)


class FlextGrpcModels(m_core):
    """gRPC domain models extending flext-core FlextModels.

    Consolidated namespace class containing all gRPC domain models as nested classes.
    Follows FLEXT principles with clean separation of concerns and SOLID design.
    """

    def __init_subclass__(cls, **kwargs: object) -> None:
        """Warn when FlextGrpcModels is subclassed directly."""
        super().__init_subclass__(**kwargs)
        # Note: Subclassing warning removed to avoid import issues

    # =========================================================================
    # DOMAIN MODELS - Core business entities
    # =========================================================================

    class Domain:
        """Domain models for gRPC core business entities."""

        class StreamInfo(FlextModelsEntity.Value):
            """Basic stream information (immutable value object)."""

            stream_id: str
            stream_type: str
            target: str
            created_at: datetime = Field(default_factory=datetime.now)
            total_requests_sent: int = Field(default=0)
            average_latency_ms: float = Field(default=0.0)
            error_count: int = Field(default=0)

        class GrpcRequest(FlextModelsEntity.Value):
            """Basic gRPC request model (immutable value object)."""

            method: str = Field(description="gRPC method name")
            data: dict[str, object] | None = Field(
                default=None,
                description="Request data",
            )
            metadata: dict[str, object] | None = Field(
                default=None,
                description="Request metadata",
            )

        class GrpcHealthCheck(FlextModelsEntity.Value):
            """gRPC health check model (immutable value object)."""

            service_name: str = Field(description="Service name")
            status: str = Field(description="Health status")
            timestamp: datetime = Field(description="Check timestamp")

        class ServiceDefinition(FlextModelsEntity.Value):
            """gRPC service definition model (immutable value object)."""

            service_name: str = Field(description="Service name")
            methods: list[str] = Field(
                default_factory=list,
                description="Service methods",
            )
            endpoint: str | None = Field(default=None, description="Service endpoint")
            metadata: dict[str, object] | None = Field(
                default=None,
                description="Service metadata",
            )

        class StreamMetrics(FlextModelsEntity.Value):
            """gRPC stream metrics model (immutable value object)."""

            stream_id: str = Field(description="Stream ID")
            throughput_rps: float = Field(
                description="Throughput in requests per second",
            )
            latency_p50: float = Field(description="50th percentile latency")
            latency_p95: float = Field(description="95th percentile latency")
            latency_p99: float = Field(description="99th percentile latency")
            error_rate: float = Field(description="Error rate")
            memory_usage_bytes: int = Field(description="Memory usage in bytes")

        class ServiceMetrics(FlextModelsEntity.Value):
            """gRPC service metrics model (immutable value object)."""

            service_name: str = Field(description="Service name")
            total_requests: int = Field(description="Total requests")
            successful_requests: int = Field(description="Successful requests")
            failed_requests: int = Field(description="Failed requests")
            avg_response_time: float = Field(description="Average response time")
            active_connections: int = Field(description="Active connections")

        class OperationExecutionRequest(FlextModelsEntity.Value):
            """Operation execution request for gRPC service operations."""

            operation_name: str = Field(description="Operation name to execute")
            arguments: dict[str, object] = Field(
                default_factory=dict,
                description="Positional arguments as dict",
            )
            keyword_arguments: dict[str, object] = Field(
                default_factory=dict,
                description="Keyword arguments",
            )

    # =========================================================================
    # CONFIGURATION MODELS - Configuration-related models
    # =========================================================================

    class GrpcConfig:
        """Configuration models for gRPC settings."""

        class ServerConfig(FlextModelsEntity.Value):
            """Basic server configuration (immutable value object)."""

            host: str = Field(default="localhost")
            port: int = Field(default=50051)
            max_workers: int = Field(default=10)
            timeout: float = Field(default=30.0)

        class ClientConfig(FlextModelsEntity.Value):
            """Basic client configuration (immutable value object)."""

            target: str = Field(default="localhost:50051")
            timeout: float = Field(default=30.0)

        class ChannelConfig(FlextModelsEntity.Value):
            """Basic channel configuration (immutable value object)."""

            address: str
            options: dict[str, object] | None = None

    # =========================================================================
    # SETTINGS MODELS - FlextGrpcSettings and configuration components
    # =========================================================================

    class Settings:
        """Settings models for gRPC configuration (from settings.py)."""

        class SecurityConfig(FlextModelsEntity.Value):
            """Generic gRPC security configuration with validation."""

            tls_enabled: bool = Field(default=False, description="Enable TLS encryption")
            tls_cert_file: str | None = Field(
                default=None,
                description="TLS certificate file path",
            )
            tls_key_file: str | None = Field(
                default=None,
                description="TLS private key file path",
            )
            tls_ca_file: str | None = Field(
                default=None,
                description="TLS CA certificate file path",
            )
            auth_enabled: bool = Field(default=False, description="Enable authentication")
            auth_token: str | None = Field(default=None, description="Authentication token")
            client_cert_required: bool = Field(
                default=False,
                description="Require client certificates",
            )

        class NetworkConfig(FlextModelsEntity.Value):
            """Generic gRPC network configuration with validation."""

            host: str = Field(
                default="127.0.0.1",
                min_length=1,
                description="gRPC server host",
            )
            port: int = Field(
                default=50051,
                ge=1,
                le=65535,
                description="gRPC server port",
            )
            max_connections: int = Field(
                default=1000,
                ge=1,
                le=10000,
                description="Maximum concurrent connections",
            )
            keepalive_time: int = Field(
                default=30,
                ge=1,
                description="Keepalive ping interval (seconds)",
            )
            keepalive_timeout: int = Field(
                default=5,
                ge=1,
                description="Keepalive timeout (seconds)",
            )

        class PerformanceConfig(FlextModelsEntity.Value):
            """Generic gRPC performance configuration."""

            max_workers: int = Field(
                default=50,
                ge=1,
                le=1000,
                description="Maximum worker threads",
            )
            max_concurrent_rpcs: int = Field(
                default=1000,
                ge=1,
                le=10000,
                description="Maximum concurrent RPCs",
            )
            max_receive_message_length: int = Field(
                default=4 * 1024 * 1024,
                ge=1024,
                le=100 * 1024 * 1024,
                description="Maximum receive message length (bytes)",
            )
            max_send_message_length: int = Field(
                default=4 * 1024 * 1024,
                ge=1024,
                le=100 * 1024 * 1024,
                description="Maximum send message length (bytes)",
            )
            thread_pool_size: int = Field(
                default=50,
                ge=1,
                le=200,
                description="Thread pool size",
            )

        class StreamingConfig(FlextModelsEntity.Value):
            """Generic gRPC streaming configuration."""

            enabled: bool = Field(default=True, description="Enable streaming operations")
            max_concurrent_streams: int = Field(
                default=10,
                ge=1,
                le=100,
                description="Maximum concurrent streams",
            )
            stream_buffer_size: int = Field(
                default=500,
                ge=10,
                le=10000,
                description="Stream buffer size",
            )
            max_stream_duration: int = Field(
                default=300,
                ge=10,
                le=3600,
                description="Maximum stream duration (seconds)",
            )
            enable_compression: bool = Field(
                default=True,
                description="Enable message compression",
            )

        class ClientSettingsConfig(FlextModelsEntity.Value):
            """Generic gRPC client configuration."""

            timeout: float = Field(
                default=30.0,
                gt=0,
                le=300,
                description="RPC timeout (seconds)",
            )
            retry_attempts: int = Field(
                default=3,
                ge=0,
                le=10,
                description="Maximum retry attempts",
            )
            retry_backoff: float = Field(
                default=1.0,
                gt=0,
                le=60,
                description="Retry backoff multiplier",
            )
            load_balancing_policy: str = Field(
                default="round_robin",
                description="Load balancing policy",
            )
            channel_options: dict[str, str | int] = Field(
                default_factory=dict,
                description="Additional channel options",
            )

        class MonitoringConfig(FlextModelsEntity.Value):
            """Generic gRPC monitoring and observability configuration."""

            metrics_enabled: bool = Field(default=True, description="Enable metrics collection")
            tracing_enabled: bool = Field(
                default=False,
                description="Enable distributed tracing",
            )
            health_check_enabled: bool = Field(default=True, description="Enable health checks")
            health_check_interval: int = Field(
                default=30,
                ge=5,
                le=300,
                description="Health check interval (seconds)",
            )
            log_level: str = Field(default="INFO", description="Logging level")

    # =========================================================================
    # ENTITIES - Functional entity models and helpers
    # =========================================================================

    class Entities:
        """Entity models and validation helpers for gRPC operations."""

        class EntityValidator(FlextModelsEntity.Value):
            """Generic entity validator using functional composition.

            Provides validation methods that can be composed and delegated
            to entity classes for their field validation.
            """

            @classmethod
            def validate_required_string(cls, value: str, field_name: str) -> str:
                """Generic string validation."""
                if not value or not value.strip():
                    msg = f"{field_name} cannot be empty"
                    raise ValueError(msg)
                return value

            @classmethod
            def validate_enum(cls, value: str, allowed: set[str], field_name: str) -> str:
                """Generic enum validation."""
                if value not in allowed:
                    msg = f"{field_name} must be one of {allowed}, got {value}"
                    raise ValueError(msg)
                return value

            @classmethod
            def validate_list_not_empty(cls, value: list[object], field_name: str) -> list[object]:
                """Generic list validation."""
                if not value:
                    msg = f"{field_name} cannot be empty"
                    raise ValueError(msg)
                return value

        class StateMachine(FlextModelsEntity.Value):
            """Generic state machine with functional transitions.

            Provides state transition logic that can be composed into
            entity classes for state management.
            """

            def transition(
                self,
                current: str,
                target: str,
                allowed_transitions: dict[str, set[str]],
            ) -> object:
                """Generic state transition with validation.

                Args:
                    current: Current state
                    target: Target state
                    allowed_transitions: Map of allowed transitions

                Returns:
                    FlextResult with updated entity on success

                """
                if (
                    current not in allowed_transitions
                    or target not in allowed_transitions[current]
                ):
                    return r.fail(f"Invalid transition from {current} to {target}")
                # Return the updated state for delegating classes to use
                return r.ok({"state": target})

    # =========================================================================
    # API - Generic API models for gRPC operations
    # =========================================================================

    class API:
        """API models for gRPC request/response handling."""

        T = TypeVar("T", bound=BaseModel)

        class OperationSpec(FlextModelsEntity.Value):
            """Generic operation specification using Pydantic."""

            name: str = Field(min_length=1, description="Operation name")
            entity_type: str = Field(
                pattern=r"^[a-z_]+$",
                description="Type of entity to operate on",
            )
            method_name: str | None = Field(
                default=None,
                description="Method to invoke on entity",
            )
            parameters: dict[str, object] = Field(
                default_factory=dict,
                description="Operation parameters",
            )

            @field_validator("entity_type")
            @classmethod
            def validate_entity_type(cls, v: str) -> str:
                """Validate entity type against supported types."""
                supported = frozenset({"server", "client", "channel", "service", "stream"})
                if v not in supported:
                    msg = f"Unsupported entity type: {v}. Supported: {supported}"
                    raise ValueError(msg)
                return v

        class Request(FlextModelsEntity.Value):
            """Generic request model with validation."""

            operation: FlextGrpcModels.API.OperationSpec
            entity: BaseModel | None = Field(
                default=None,
                description="Associated entity",
            )
            data: object = Field(
                default=None,
                description="Request data",
            )

            @computed_field
            @property
            def is_valid(self) -> bool:
                """Check if request is valid."""
                return bool(self.operation.name.strip())

        class Response(FlextModelsEntity.Value):
            """Generic response model with metadata."""

            success: bool = Field(description="Operation success status")
            data: BaseModel | None = Field(
                default=None,
                description="Response data",
            )
            error: str | None = Field(
                default=None,
                description="Error message if failed",
            )
            metadata: dict[str, object] = Field(
                default_factory=dict,
                description="Response metadata",
            )

            @computed_field
            @property
            def has_error(self) -> bool:
                """Check if response has error."""
                return not self.success or self.error is not None


# =============================================================================
# POPULATE FlextModels.Grpc NAMESPACE
# =============================================================================
# Copy all models from FlextGrpcModels to FlextModels.Grpc namespace
# This allows access via both:
# - FlextGrpcModels.* (backward compatibility, deprecated)
# - FlextModels.Grpc.* (new namespace pattern)
# - m.Grpc.* (convenience alias)
# =============================================================================

# Get all attributes from FlextGrpcModels that are models, classes, or type aliases
# Exclude private attributes and special methods
_grpc_model_attrs = {
    name: attr
    for name, attr in vars(FlextGrpcModels).items()
    if not name.startswith("_")
    and (
        isinstance(attr, type)
        or hasattr(attr, "__origin__")  # TypeAlias
        or (callable(attr) and not isinstance(attr, type(FlextGrpcModels.__init__)))
    )
}

# Note: FlextModels.Grpc namespace does not exist in flext-core
# Models should be accessed directly via FlextGrpcModels.*

m = FlextGrpcModels
m_grpc = FlextGrpcModels

__all__ = ["FlextGrpcModels", "m", "m_grpc"]
