"""FLEXT gRPC Models - Consolidated Pydantic v2 Models.

Unified namespace with nested classes following FLEXT principles and SOLID design.
All domain models consolidated into a single class with nested structures.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping
from datetime import UTC, datetime
from typing import Literal, Self

import grpc
from flext_core import FlextModels, m, r
from pydantic import BaseModel, Field, computed_field, field_validator

from flext_grpc.constants import c
from flext_grpc.protocols import FlextGrpcProtocols as p
from flext_grpc.typings import t


class FlextGrpcModels(FlextModels):
    """gRPC domain models extending flext-core FlextModels.

    Consolidated namespace class containing all gRPC domain models as nested classes.
    Follows FLEXT principles with clean separation of concerns and SOLID design.
    """

    # =========================================================================
    # DOMAIN MODELS - Core business entities
    # =========================================================================

    class Grpc:
        """Domain models for gRPC core business entities."""

        class StreamInfo(m.Value):
            """Basic stream information (immutable value model)."""

            stream_id: str
            stream_type: str
            target: str
            created_at: datetime = Field(default_factory=datetime.now)
            total_requests_sent: int = Field(default=0)
            average_latency_ms: float = Field(default=0.0)
            error_count: int = Field(default=0)

        class HealthCheck(m.Value):
            """gRPC health check model (immutable value model)."""

            service_name: str = Field(description="Service name")
            status: str = Field(description="Health status")
            timestamp: datetime = Field(description="Check timestamp")

        class ServiceDefinition(m.Value):
            """gRPC service definition model (immutable value model)."""

            service_name: str = Field(description="Service name")
            methods: list[str] = Field(
                default_factory=list,
                description="Service methods",
            )
            endpoint: str | None = Field(default=None, description="Service endpoint")
            metadata: t.Grpc.Metadata | None = Field(
                default=None,
                description="Service metadata",
            )

        class StreamMetrics(m.Value):
            """gRPC stream metrics model (immutable value model)."""

            stream_id: str = Field(description="Stream ID")
            throughput_rps: float = Field(
                description="Throughput in requests per second",
            )
            latency_p50: float = Field(description="50th percentile latency")
            latency_p95: float = Field(description="95th percentile latency")
            latency_p99: float = Field(description="99th percentile latency")
            error_rate: float = Field(description="Error rate")
            memory_usage_bytes: int = Field(description="Memory usage in bytes")

        class ServiceMetrics(m.Value):
            """gRPC service metrics model (immutable value model)."""

            service_name: str = Field(description="Service name")
            total_requests: int = Field(description="Total requests")
            successful_requests: int = Field(description="Successful requests")
            failed_requests: int = Field(description="Failed requests")
            avg_response_time: float = Field(description="Average response time")
            active_connections: int = Field(description="Active connections")

        class OperationExecutionRequest(m.Value):
            """Operation execution request for gRPC service operations."""

            operation_name: str = Field(description="Operation name to execute")
            arguments: Mapping[str, str | int | float | bool] = Field(
                default_factory=dict,
                description="Positional arguments as dict",
            )
            keyword_arguments: Mapping[str, str | int | float | bool] = Field(
                default_factory=dict,
                description="Keyword arguments",
            )

        class ServerConfig(m.Value):
            """Basic server configuration (immutable value model)."""

            host: str = Field(default=c.Grpc.GrpcNetwork.DEFAULT_HOST)
            port: int = Field(default=c.Grpc.GrpcNetwork.DEFAULT_GRPC_PORT)
            max_workers: int = Field(default=c.Grpc.Service.DEFAULT_MAX_WORKERS)
            timeout: float = Field(default=c.Grpc.GrpcNetwork.DEFAULT_TIMEOUT)

        class ClientConfig(m.Value):
            """Basic client configuration (immutable value model)."""

            target: str = Field(
                default=f"{c.Grpc.GrpcNetwork.DEFAULT_HOST}:{c.Grpc.GrpcNetwork.DEFAULT_GRPC_PORT}"
            )
            timeout: float = Field(default=c.Grpc.GrpcNetwork.DEFAULT_TIMEOUT)

        class ChannelConfig(m.Value):
            """Basic channel configuration (immutable value model)."""

            address: str
            options: Mapping[str, t.JsonValue] | None = None

        class SecurityConfig(m.Value):
            """Generic gRPC security configuration with validation."""

            tls_enabled: bool = Field(
                default=False, description="Enable TLS encryption"
            )
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
            auth_enabled: bool = Field(
                default=False, description="Enable authentication"
            )
            auth_token: str | None = Field(
                default=None, description="Authentication token"
            )
            client_cert_required: bool = Field(
                default=False,
                description="Require client certificates",
            )

        class NetworkConfig(m.Value):
            """Generic gRPC network configuration with validation."""

            host: str = Field(
                default=c.Grpc.GrpcNetwork.DEFAULT_HOST,
                min_length=1,
                description="gRPC server host",
            )
            port: int = Field(
                default=c.Grpc.GrpcNetwork.DEFAULT_GRPC_PORT,
                ge=1,
                le=65535,
                description="gRPC server port",
            )
            max_connections: int = Field(
                default=c.Grpc.Service.DEFAULT_MAX_CONCURRENT_RPCS,
                ge=1,
                le=10000,
                description="Maximum concurrent connections",
            )
            keepalive_time: int = Field(
                default=c.Grpc.GrpcNetwork.DEFAULT_KEEPALIVE_TIME_MS // 1000,
                ge=1,
                description="Keepalive ping interval (seconds)",
            )
            keepalive_timeout: int = Field(
                default=c.Grpc.GrpcNetwork.DEFAULT_KEEPALIVE_TIMEOUT_MS // 1000,
                ge=1,
                description="Keepalive timeout (seconds)",
            )

        class PerformanceConfig(m.Value):
            """Generic gRPC performance configuration."""

            max_workers: int = Field(
                default=c.Grpc.Service.MAX_WORKERS,
                ge=1,
                le=1000,
                description="Maximum worker threads",
            )
            max_concurrent_rpcs: int = Field(
                default=c.Grpc.Service.DEFAULT_MAX_CONCURRENT_RPCS,
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

        class StreamingConfig(m.Value):
            """Generic gRPC streaming configuration."""

            enabled: bool = Field(
                default=True, description="Enable streaming operations"
            )
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

        class ClientSettingsConfig(m.Value):
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
            channel_options: Mapping[str, str | int] = Field(
                default_factory=dict,
                description="Additional channel options",
            )

        class MonitoringConfig(m.Value):
            """Generic gRPC monitoring and observability configuration."""

            metrics_enabled: bool = Field(
                default=True, description="Enable metrics collection"
            )
            tracing_enabled: bool = Field(
                default=False,
                description="Enable distributed tracing",
            )
            health_check_enabled: bool = Field(
                default=True, description="Enable health checks"
            )
            health_check_interval: int = Field(
                default=30,
                ge=5,
                le=300,
                description="Health check interval (seconds)",
            )
            log_level: str = Field(default="INFO", description="Logging level")

        class StateTransition(m.Value):
            """State transition result model."""

            state: str

        class EntityValidator(m.Value):
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
            def validate_enum(
                cls, value: str, allowed: set[str], field_name: str
            ) -> str:
                """Generic enum validation."""
                if value not in allowed:
                    msg = f"{field_name} must be one of {allowed}, got {value}"
                    raise ValueError(msg)
                return value

            @classmethod
            def validate_list_not_empty[T](
                cls,
                value: list[T],
                field_name: str,
            ) -> list[T]:
                """Generic list validation with type preservation."""
                if not value:
                    msg = f"{field_name} cannot be empty"
                    raise ValueError(msg)
                return value

        class StateMachine(BaseModel):
            """Generic state machine with functional transitions.

            Provides state transition logic that can be composed into
            entity classes for state management.

            Note: Uses BaseModel (not Value/FrozenStrictModel) because
            StateMachine is composed with Entity via multiple inheritance.
            Entity's model_post_init sets updated_at which requires
            the model to NOT be frozen.
            """

            def transition(
                self,
                current: str,
                target: str,
                allowed_transitions: Mapping[str, set[str]],
            ) -> r[FlextGrpcModels.Grpc.StateTransition]:
                """Generic state transition with validation.

                Args:
                    current: Current state
                    target: Target state
                    allowed_transitions: Map of allowed transitions

                Returns:
                    FlextResult with state update dict on success

                """
                if (
                    current not in allowed_transitions
                    or target not in allowed_transitions[current]
                ):
                    return r[FlextGrpcModels.Grpc.StateTransition].fail(
                        f"Invalid transition from {current} to {target}",
                    )
                return r[FlextGrpcModels.Grpc.StateTransition].ok(
                    FlextGrpcModels.Grpc.StateTransition(state=target)
                )

        class OperationSpec(m.Value):
            """Generic operation specification using Pydantic."""

            name: str = Field(min_length=1, description="Operation name")
            entity_type: Literal["server", "client", "channel", "service", "stream"] = (
                Field(
                    description="Type of entity to operate on",
                )
            )
            method_name: str | None = Field(
                default=None,
                description="Method to invoke on entity",
            )
            parameters: Mapping[str, t.JsonValue] = Field(
                default_factory=dict,
                description="Operation parameters",
            )

        class Request(m.Value):
            """Generic request model with validation."""

            operation: FlextGrpcModels.Grpc.OperationSpec
            entity: BaseModel | None = Field(
                default=None,
                description="Associated entity",
            )
            data: t.JsonValue = Field(
                default=None,
                description="Request data",
            )

            @computed_field
            def is_valid(self) -> bool:
                """Check if request is valid."""
                return bool(self.operation.name.strip())

        class Response(m.Value):
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
            metadata: Mapping[str, t.JsonValue] = Field(
                default_factory=dict,
                description="Response metadata",
            )

            @computed_field
            def has_error(self) -> bool:
                """Check if response has error."""
                return not self.success or self.error is not None

        class Payload(BaseModel):
            """Structured payload model replacing ad-hoc dict responses."""

            values: t.Grpc.GrpcDict = Field(default_factory=dict)

            @classmethod
            def from_values(cls, **values: t.GeneralValueType) -> Self:
                """Build payload from keyword values."""
                return cls(values=values)

        class Entity(FlextModels.Entity):
            """Generic base entity with functional patterns."""

            created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

            def copy_with(self, **kwargs: str | int | bool | None) -> r[Self]:
                """Functional copy using r.

                Args:
                **kwargs: Field updates for the entity

                """
                try:
                    return r.ok(self.model_copy(update=kwargs))
                except (grpc.RpcError, ConnectionError, TimeoutError) as e:
                    return r.fail(str(e))

            def validate_business_rules(self) -> r[bool]:
                """Override in subclasses for specific validation."""
                return r.ok(True)

        class Channel(Entity, StateMachine):
            """Generic gRPC channel with state machine delegation."""

            target: str = ""
            state: c.Grpc.ChannelStateLiteral = "idle"
            options: dict[str, t.GeneralValueType] = Field(default_factory=dict)
            grpc_channel: p.Grpc.GrpcChannel | None = None

            def validate_business_rules(self) -> r[bool]:
                """Functional validation composition."""
                if not self.target.strip():
                    return r.fail("Channel target cannot be empty")
                return r.ok(True)

            def is_ready(self) -> bool:
                """Check readiness."""
                return self.state == "ready"

            def connect(self) -> r[Self]:
                """Transition to connecting."""
                return self.transition(
                    self.state,
                    "connecting",
                    {"idle": {"connecting"}},
                ).map(lambda update: self.model_copy(update=update.model_dump()))

            def mark_ready(self) -> r[Self]:
                """Transition to ready."""
                return self.transition(
                    self.state,
                    "ready",
                    {"connecting": {"ready"}},
                ).map(lambda update: self.model_copy(update=update.model_dump()))

            def disconnect(self) -> r[Self]:
                """Transition to idle."""
                return r.ok(
                    self.model_copy(update={"state": c.Grpc.ChannelState.IDLE.value})
                )

        class Server(Entity, StateMachine):
            """Generic gRPC server with state machine and validation delegation."""

            host: str = c.Grpc.GrpcNetwork.DEFAULT_HOST
            port: int = c.Grpc.GrpcNetwork.DEFAULT_GRPC_PORT
            state: c.Grpc.ServerStateLiteral = "stopped"
            max_workers: int = 10
            services: list[p.Grpc.GrpcServicer] = Field(default_factory=list)
            grpc_server: p.Grpc.GrpcServer | None = None

            def validate_business_rules(self) -> r[bool]:
                """Delegate validation to generic validators."""
                if not self.host.strip():
                    return r.fail("Server host cannot be empty")
                # Port range validation using IANA standard range
                min_port = 1
                max_port = 65535
                if not (min_port <= self.port <= max_port):
                    return r.fail(f"Invalid port: {self.port}")
                if self.max_workers < 1:
                    return r.fail("Max workers must be >= 1")
                return r.ok(True)

            def start(self) -> r[Self]:
                """Transition to starting."""
                return self.transition(
                    self.state,
                    "starting",
                    {"stopped": {"starting"}},
                ).map(lambda update: self.model_copy(update=update.model_dump()))

            def mark_running(self) -> r[Self]:
                """Transition to running."""
                return self.transition(
                    self.state,
                    "running",
                    {"starting": {"running"}},
                ).map(lambda update: self.model_copy(update=update.model_dump()))

            def stop(self) -> r[Self]:
                """Transition to stopping."""
                return self.transition(
                    self.state,
                    "stopping",
                    {"running": {"stopping"}},
                ).map(lambda update: self.model_copy(update=update.model_dump()))

            def mark_stopped(self) -> r[Self]:
                """Transition to stopped."""
                if self.state not in {"stopping", "running"}:
                    return r.fail(f"Cannot mark stopped from {self.state}")
                return r.ok(
                    self.model_copy(update={"state": c.Grpc.ServerState.STOPPED.value})
                )

            def add_service(self, service: p.Grpc.GrpcServicer) -> r[Self]:
                """Add service functionally.

                Args:
                service: gRPC service object (dynamic type from grpc library)

                """
                return r.ok(
                    self.model_copy(update={"services": [*self.services, service]}),
                )

        class Service(Entity):
            """Generic gRPC service with validation delegation."""

            name: str = ""
            methods: list[str] = Field(default_factory=list)

            @field_validator("name")
            @classmethod
            def validate_name(cls, v: str) -> str:
                """Validate name is not empty or whitespace."""
                if not v or not v.strip():
                    msg = "name cannot be empty"
                    raise ValueError(msg)
                return v

            @field_validator("methods")
            @classmethod
            def validate_methods(cls, v: list[str]) -> list[str]:
                """Validate methods list is not empty with valid items."""
                if not v:
                    msg = "methods cannot be empty"
                    raise ValueError(msg)
                for method in v:
                    if not method or not method.strip():
                        msg = "method cannot be empty"
                        raise ValueError(msg)
                return v

            def has_method(self, method_name: str) -> bool:
                """Check method existence."""
                return method_name in self.methods

            def add_method(self, method_name: str) -> r[Self]:
                """Add method functionally."""
                if not method_name.strip() or method_name in self.methods:
                    return r.fail("Invalid method")
                return r.ok(
                    self.model_copy(update={"methods": [*self.methods, method_name]}),
                )

        class Client(Entity):
            """Generic gRPC client with channel delegation."""

            channel: FlextGrpcModels.Grpc.Channel | None = None
            options: t.GrpcOptions = Field(default_factory=dict)
            grpc_stub: p.Grpc.GrpcStub | None = None

            def validate_business_rules(self) -> r[bool]:
                """Delegate validation."""
                if self.channel and self.channel.validate_business_rules().is_failure:
                    return r.fail("Invalid channel")
                return r.ok(True)

            def connect_to(self, target: str) -> r[Self]:
                """Connect functionally."""
                channel = FlextGrpcModels.Grpc.Channel(
                    target=target,
                    state=c.Grpc.ChannelState.IDLE.value,
                )
                return r.ok(self.model_copy(update={"channel": channel}))

        class GrpcStream(Entity):
            """Generic gRPC stream with validation delegation."""

            id: str = ""
            method_name: str = ""
            stream_type: c.Grpc.StreamTypeLiteral = "unary"
            grpc_stub: p.Grpc.GrpcStub | None = None

            @field_validator("method_name")
            @classmethod
            def validate_method_name(cls, v: str) -> str:
                """Validate method_name is not empty or whitespace."""
                if not v or not v.strip():
                    msg = "method_name cannot be empty"
                    raise ValueError(msg)
                return v

    # Class-level aliases at facade root (flat namespace: m.StreamInfo, m.Request, etc.)
    StreamInfo = Grpc.StreamInfo
    HealthCheck = Grpc.HealthCheck
    ServiceDefinition = Grpc.ServiceDefinition
    StreamMetrics = Grpc.StreamMetrics
    ServiceMetrics = Grpc.ServiceMetrics
    OperationExecutionRequest = Grpc.OperationExecutionRequest
    ServerConfig = Grpc.ServerConfig
    ClientConfig = Grpc.ClientConfig
    ChannelConfig = Grpc.ChannelConfig
    SecurityConfig = Grpc.SecurityConfig
    NetworkConfig = Grpc.NetworkConfig
    PerformanceConfig = Grpc.PerformanceConfig
    StreamingConfig = Grpc.StreamingConfig
    ClientSettingsConfig = Grpc.ClientSettingsConfig
    MonitoringConfig = Grpc.MonitoringConfig
    StateTransition = Grpc.StateTransition
    EntityValidator = Grpc.EntityValidator
    OperationSpec = Grpc.OperationSpec
    Request = Grpc.Request
    Response = Grpc.Response
    Payload = Grpc.Payload
    Entity = Grpc.Entity
    Channel = Grpc.Channel
    Server = Grpc.Server
    Client = Grpc.Client
    GrpcStream = Grpc.GrpcStream
    StateMachine = Grpc.StateMachine


m = FlextGrpcModels

__all__ = ["FlextGrpcModels", "m"]
