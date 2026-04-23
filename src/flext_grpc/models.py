"""FLEXT gRPC Models - Consolidated Pydantic v2 Models.

Unified namespace with nested classes following FLEXT principles and SOLID design.
All domain models consolidated into a single class with nested structures.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import (
    Mapping,
    Sequence,
)
from datetime import datetime
from types import MappingProxyType
from typing import Annotated, Self, override

from flext_cli import m, u

from flext_grpc import c, p, r, t


class FlextGrpcModels(m):
    """gRPC domain models extending flext-core m.

    Consolidated namespace class containing all gRPC domain models as nested classes.
    Follows FLEXT principles with clean separation of concerns and SOLID design.
    """

    # =========================================================================
    # DOMAIN MODELS - Core business entities
    # =========================================================================

    class Grpc:
        """Domain models for gRPC core business entities."""

        # =========================================================================
        # PROTO MESSAGE MODELS - RPC request/response messages
        # =========================================================================

        class EchoRequest(m.Value):
            """Echo request message (immutable value model)."""

            message: Annotated[str, u.Field(description="Echo message")]

        class EchoResponse(m.Value):
            """Echo response message (immutable value model)."""

            message: Annotated[str, u.Field(description="Echo message")]
            server_id: Annotated[str, u.Field(description="Server identifier")] = ""
            timestamp: datetime = u.Field(
                default_factory=datetime.now, description="Response timestamp"
            )

        class HealthRequest(m.Value):
            """Health check request message (immutable value model)."""

            service: Annotated[str, u.Field(description="Service name")] = ""

        class HealthResponse(m.Value):
            """Health check response message (immutable value model)."""

            status: Annotated[str, u.Field(description="Health status")]
            message: Annotated[str, u.Field(description="Health check message")] = ""

        class StreamInfo(m.Value):
            """Basic stream information (immutable value model)."""

            stream_id: str = u.Field(description="Unique stream identifier")
            stream_type: str = u.Field(description="Stream communication type")
            target: str = u.Field(description="Target endpoint address")
            created_at: datetime = u.Field(
                default_factory=datetime.now, description="Stream creation timestamp"
            )
            total_requests_sent: Annotated[
                t.NonNegativeInt, u.Field(description="Total requests sent on stream")
            ] = 0
            average_latency_ms: Annotated[
                t.NonNegativeFloat,
                u.Field(description="Average latency in milliseconds"),
            ] = 0.0
            error_count: Annotated[
                t.NonNegativeInt, u.Field(description="Number of errors on stream")
            ] = 0

        class HealthCheck(m.Value):
            """gRPC health check model (immutable value model)."""

            service_name: Annotated[str, u.Field(description="Service name")]
            status: Annotated[str, u.Field(description="Health status")]
            timestamp: Annotated[datetime, u.Field(description="Check timestamp")]

        class ServiceDefinition(m.Value):
            """gRPC service definition model (immutable value model)."""

            service_name: Annotated[str, u.Field(description="Service name")]
            methods: t.StrSequence = u.Field(
                default_factory=tuple, description="Service methods"
            )
            endpoint: Annotated[str | None, u.Field(description="Service endpoint")] = (
                None
            )
            metadata: Annotated[
                t.JsonMapping | None,
                u.Field(
                    description="Service metadata",
                ),
            ] = None

        class StreamMetrics(m.Value):
            """gRPC stream metrics model (immutable value model)."""

            stream_id: Annotated[str, u.Field(description="Stream ID")]
            throughput_rps: Annotated[
                t.NonNegativeFloat,
                u.Field(
                    description="Throughput in requests per second",
                ),
            ]
            latency_p50: Annotated[
                t.NonNegativeFloat,
                u.Field(description="50th percentile latency"),
            ]
            latency_p95: Annotated[
                t.NonNegativeFloat,
                u.Field(description="95th percentile latency"),
            ]
            latency_p99: Annotated[
                t.NonNegativeFloat,
                u.Field(description="99th percentile latency"),
            ]
            error_rate: Annotated[t.NonNegativeFloat, u.Field(description="Error rate")]
            memory_usage_bytes: Annotated[
                t.NonNegativeInt,
                u.Field(description="Memory usage in bytes"),
            ]

        class ServiceMetrics(m.Value):
            """gRPC service metrics model (immutable value model)."""

            service_name: Annotated[str, u.Field(description="Service name")]
            total_requests: Annotated[
                t.NonNegativeInt,
                u.Field(description="Total requests"),
            ]
            successful_requests: Annotated[
                t.NonNegativeInt,
                u.Field(description="Successful requests"),
            ]
            failed_requests: Annotated[
                t.NonNegativeInt,
                u.Field(description="Failed requests"),
            ]
            avg_response_time: Annotated[
                t.NonNegativeFloat,
                u.Field(description="Average response time"),
            ]
            active_connections: Annotated[
                t.NonNegativeInt,
                u.Field(description="Active connections"),
            ]

        class OperationExecutionRequest(m.Value):
            """Operation execution request for gRPC service operations."""

            operation_name: Annotated[
                str,
                u.Field(description="Operation name to execute"),
            ]
            arguments: t.ScalarMapping = u.Field(
                default_factory=lambda: MappingProxyType({}),
                description="Positional arguments as dict",
            )
            keyword_arguments: t.ScalarMapping = u.Field(
                default_factory=lambda: MappingProxyType({}),
                description="Keyword arguments",
            )

        class ServerConfig(m.Value):
            """Basic server configuration (immutable value model)."""

            host: Annotated[
                str,
                u.Field(
                    description="Server host address",
                ),
            ] = c.Grpc.GrpcNetwork.DEFAULT_HOST
            port: Annotated[
                t.PortNumber,
                u.Field(
                    description="Server port number",
                ),
            ] = c.Grpc.GrpcNetwork.DEFAULT_GRPC_PORT
            max_workers: Annotated[
                t.WorkerCount,
                u.Field(
                    description="Maximum worker threads",
                ),
            ] = c.Grpc.Service.DEFAULT_MAX_WORKERS
            timeout: Annotated[
                t.PositiveTimeout,
                u.Field(
                    description="Request timeout in seconds",
                ),
            ] = c.Grpc.GrpcNetwork.DEFAULT_TIMEOUT

        class ClientConfig(m.Value):
            """Basic client configuration (immutable value model)."""

            target: Annotated[
                str,
                u.Field(
                    description="Target server address",
                ),
            ] = f"{c.Grpc.GrpcNetwork.DEFAULT_HOST}:{c.Grpc.GrpcNetwork.DEFAULT_GRPC_PORT}"
            timeout: Annotated[
                t.PositiveTimeout,
                u.Field(
                    description="Request timeout in seconds",
                ),
            ] = c.Grpc.GrpcNetwork.DEFAULT_TIMEOUT

        class ChannelConfig(m.Value):
            """Basic channel configuration (immutable value model)."""

            address: str = u.Field(description="Channel address")
            options: Annotated[
                t.JsonMapping | None,
                u.Field(description="Channel options"),
            ] = None

        class SecurityConfig(m.Value):
            """Generic gRPC security configuration with validation."""

            tls_enabled: Annotated[
                bool,
                u.Field(
                    description="Enable TLS encryption",
                ),
            ] = False
            tls_cert_file: Annotated[
                str | None,
                u.Field(
                    description="TLS certificate file path",
                ),
            ] = None
            tls_key_file: Annotated[
                str | None,
                u.Field(
                    description="TLS private key file path",
                ),
            ] = None
            tls_ca_file: Annotated[
                str | None,
                u.Field(
                    description="TLS CA certificate file path",
                ),
            ] = None
            auth_enabled: Annotated[
                bool,
                u.Field(
                    description="Enable authentication",
                ),
            ] = False
            auth_token: Annotated[
                str | None,
                u.Field(
                    description="Authentication token",
                ),
            ] = None
            client_cert_required: Annotated[
                bool,
                u.Field(
                    description="Require client certificates",
                ),
            ] = False

        class NetworkConfig(m.Value):
            """Generic gRPC network configuration with validation."""

            host: Annotated[
                t.NonEmptyStr,
                u.Field(
                    description="gRPC server host",
                ),
            ] = c.Grpc.GrpcNetwork.DEFAULT_HOST
            port: Annotated[
                t.PortNumber,
                u.Field(
                    description="gRPC server port",
                ),
            ] = c.Grpc.GrpcNetwork.DEFAULT_GRPC_PORT
            max_connections: Annotated[
                t.BatchSize,
                u.Field(
                    description="Maximum concurrent connections",
                ),
            ] = c.Grpc.Service.DEFAULT_MAX_CONCURRENT_RPCS
            keepalive_time: Annotated[
                t.PositiveInt,
                u.Field(
                    description="Keepalive ping interval (seconds)",
                ),
            ] = c.Grpc.GrpcNetwork.DEFAULT_KEEPALIVE_TIME_MS // 1000
            keepalive_timeout: Annotated[
                t.PositiveInt,
                u.Field(
                    description="Keepalive timeout (seconds)",
                ),
            ] = c.Grpc.GrpcNetwork.DEFAULT_KEEPALIVE_TIMEOUT_MS // 1000

        class PerformanceConfig(m.Value):
            """Generic gRPC performance configuration."""

            max_workers: Annotated[
                int,
                u.Field(
                    ge=1,
                    le=1000,
                    description="Maximum worker threads",
                ),
            ] = c.Grpc.Service.MAX_WORKERS
            max_concurrent_rpcs: Annotated[
                t.BatchSize,
                u.Field(
                    description="Maximum concurrent RPCs",
                ),
            ] = c.Grpc.Service.DEFAULT_MAX_CONCURRENT_RPCS
            max_receive_message_length: Annotated[
                int,
                u.Field(
                    ge=c.Grpc.PerformanceLimits.MIN_MESSAGE_LENGTH,
                    le=c.Grpc.PerformanceLimits.MAX_MESSAGE_LENGTH,
                    description="Maximum receive message length (bytes)",
                ),
            ] = c.Grpc.PerformanceLimits.DEFAULT_MESSAGE_LENGTH
            max_send_message_length: Annotated[
                int,
                u.Field(
                    ge=c.Grpc.PerformanceLimits.MIN_MESSAGE_LENGTH,
                    le=c.Grpc.PerformanceLimits.MAX_MESSAGE_LENGTH,
                    description="Maximum send message length (bytes)",
                ),
            ] = c.Grpc.PerformanceLimits.DEFAULT_MESSAGE_LENGTH
            thread_pool_size: Annotated[
                int,
                u.Field(
                    ge=c.Grpc.PerformanceLimits.MIN_THREAD_POOL_SIZE,
                    le=c.Grpc.PerformanceLimits.MAX_THREAD_POOL_SIZE,
                    description="Thread pool size",
                ),
            ] = c.Grpc.PerformanceLimits.DEFAULT_THREAD_POOL_SIZE

        class StreamingConfig(m.Value):
            """Generic gRPC streaming configuration."""

            enabled: Annotated[
                bool,
                u.Field(
                    description="Enable streaming operations",
                ),
            ] = True
            max_concurrent_streams: Annotated[
                t.WorkerCount,
                u.Field(
                    description="Maximum concurrent streams",
                ),
            ] = c.Grpc.Streaming.DEFAULT_MAX_CONCURRENT_STREAMS
            stream_buffer_size: Annotated[
                int,
                u.Field(
                    ge=c.Grpc.Streaming.MIN_BUFFER_SIZE,
                    le=c.Grpc.Streaming.MAX_BUFFER_SIZE,
                    description="Stream buffer size",
                ),
            ] = c.Grpc.Streaming.DEFAULT_BUFFER_SIZE
            max_stream_duration: Annotated[
                int,
                u.Field(
                    ge=10,
                    le=3600,
                    description="Maximum stream duration (seconds)",
                ),
            ] = 300
            enable_compression: Annotated[
                bool,
                u.Field(
                    description="Enable message compression",
                ),
            ] = True

        class ClientSettingsConfig(m.Value):
            """Generic gRPC client configuration."""

            timeout: Annotated[
                t.PositiveTimeout,
                u.Field(
                    description="RPC timeout (seconds)",
                ),
            ] = 30.0
            retry_attempts: Annotated[
                t.RetryCount,
                u.Field(
                    description="Maximum retry attempts",
                ),
            ] = 3
            retry_backoff: Annotated[
                float,
                u.Field(
                    gt=0,
                    le=60,
                    description="Retry backoff multiplier",
                ),
            ] = 1.0
            load_balancing_policy: Annotated[
                str,
                u.Field(
                    description="Load balancing policy",
                ),
            ] = "round_robin"
            channel_options: Annotated[
                t.HeaderMapping,
                u.Field(
                    description="Additional channel options",
                ),
            ] = u.Field(default_factory=lambda: MappingProxyType({}))

        class MonitoringConfig(m.Value):
            """Generic gRPC monitoring and observability configuration."""

            metrics_enabled: Annotated[
                bool,
                u.Field(
                    description="Enable metrics collection",
                ),
            ] = True
            tracing_enabled: Annotated[
                bool,
                u.Field(
                    description="Enable distributed tracing",
                ),
            ] = False
            health_check_enabled: Annotated[
                bool,
                u.Field(
                    description="Enable health checks",
                ),
            ] = True
            health_check_interval: Annotated[
                int,
                u.Field(
                    ge=5,
                    le=300,
                    description="Health check interval (seconds)",
                ),
            ] = 30
            log_level: Annotated[str, u.Field(description="Logging level")] = "INFO"

        class StateTransition(m.Value):
            """State transition result model."""

            state: str = u.Field(description="Target state after transition")

        class EntityValidator(m.Value):
            """Generic entity validator using functional composition.

            Provides validation methods that can be composed and delegated
            to entity classes for their field validation.
            """

            @classmethod
            def validate_enum(
                cls,
                value: str,
                allowed: set[str],
                field_name: str,
            ) -> str:
                """Generic enum validation."""
                if value not in allowed:
                    msg = f"{field_name} must be one of {allowed}, got {value}"
                    raise ValueError(msg)
                return value

            @classmethod
            def validate_list_not_empty[T](
                cls,
                value: Sequence[T],
                field_name: str,
            ) -> Sequence[T]:
                """Generic list validation with type preservation."""
                if not value:
                    msg = f"{field_name} cannot be empty"
                    raise ValueError(msg)
                return value

            @classmethod
            def validate_required_string(cls, value: str, field_name: str) -> str:
                """Generic string validation."""
                if not value or not value.strip():
                    msg = f"{field_name} cannot be empty"
                    raise ValueError(msg)
                return value

        class StateMachine(m.BaseModel):
            """Generic state machine with functional transitions.

            Provides state transition logic that can be composed into
            entity classes for state management.

            Note: Uses BaseModel (not Value/ContractModel) because
            StateMachine is composed with Entity via multiple inheritance.
            Entity's model_post_init sets updated_at which requires
            the model to NOT be frozen.
            """

            def transition(
                self,
                current: str,
                target: str,
                allowed_transitions: Mapping[str, set[str]],
            ) -> p.Result[FlextGrpcModels.Grpc.StateTransition]:
                """Generic state transition with validation.

                Args:
                    current: Current state
                    target: Target state
                    allowed_transitions: Map of allowed transitions

                Returns:
                    r with state update dict on success

                """
                if (
                    current not in allowed_transitions
                    or target not in allowed_transitions[current]
                ):
                    return r[FlextGrpcModels.Grpc.StateTransition].fail(
                        f"Invalid transition from {current} to {target}",
                    )
                return r[FlextGrpcModels.Grpc.StateTransition].ok(
                    FlextGrpcModels.Grpc.StateTransition(state=target),
                )

        class OperationSpec(m.Value):
            """Generic operation specification using Pydantic."""

            name: Annotated[str, u.Field(min_length=1, description="Operation name")]
            entity_type: Annotated[
                t.Grpc.EntityKind,
                u.Field(description="Type of entity to operate on"),
            ]
            method_name: Annotated[
                str | None,
                u.Field(
                    description="Method to invoke on entity",
                ),
            ] = None
            parameters: Annotated[
                Mapping[str, t.JsonMapping | None],
                u.Field(
                    description="Operation parameters",
                ),
            ] = u.Field(default_factory=lambda: MappingProxyType({}))

        class Request(m.Value):
            """Generic request model with validation."""

            operation: FlextGrpcModels.Grpc.OperationSpec = u.Field(
                description="Operation specification to execute",
            )
            entity: Annotated[
                m.BaseModel | None,
                u.Field(
                    description="Associated entity",
                ),
            ] = None
            data: Annotated[
                t.JsonMapping | None,
                u.Field(
                    description="Request data",
                ),
            ] = None

            @u.computed_field()
            @property
            def valid(self) -> bool:
                """Check if request is valid."""
                return bool(self.operation.name.strip())

        class Response(m.Value):
            """Generic response model with metadata."""

            success: Annotated[bool, u.Field(description="Operation success status")]
            data: Annotated[
                m.BaseModel | None,
                u.Field(
                    description="Response data",
                ),
            ] = None
            error: Annotated[
                str | None,
                u.Field(
                    description="Error message if failed",
                ),
            ] = None
            metadata: Annotated[
                Mapping[str, t.JsonMapping | None],
                u.Field(
                    description="Response metadata",
                ),
            ] = u.Field(default_factory=lambda: MappingProxyType({}))

            @u.computed_field()
            @property
            def has_error(self) -> bool:
                """Check if response has error."""
                return not self.success or self.error is not None

        class Payload(m.BaseModel):
            """Structured payload model replacing ad-hoc dict responses."""

            values: t.JsonMapping = u.Field(
                default_factory=lambda: MappingProxyType({}),
                description="Key-value payload data",
            )

            @classmethod
            def from_values(cls, **values: t.JsonPayload | None) -> Self:
                """Build payload from keyword values."""

                def normalize_payload_value(
                    value: t.JsonPayload | None,
                ) -> t.JsonValue | None:
                    if value is None:
                        return ""
                    if u.primitive(value):
                        return value
                    return str(value)

                normalized_values: t.JsonMapping = {
                    metric_key: normalize_payload_value(metric_value)
                    for metric_key, metric_value in values.items()
                }
                return cls(values=normalized_values)

        class Entity(m.Entity):
            """Generic base entity with functional patterns."""

            def copy_with(self, **kwargs: t.Scalar | None) -> p.Result[Self]:
                """Functional copy using r.

                Args:
                **kwargs: u.Field updates for the entity

                """
                return r[Self].create_from_callable(
                    lambda: self.model_copy(update=kwargs),
                )

            def validate_business_rules(self) -> p.Result[bool]:
                """Override in subclasses for specific validation."""
                return r[bool].ok(True)

        class Channel(Entity, StateMachine):
            """Generic gRPC channel with state machine delegation."""

            target: Annotated[
                str, u.Field(description="gRPC server target address")
            ] = ""
            state: Annotated[
                c.Grpc.ChannelState,
                u.Field(
                    description="Current channel connection state",
                ),
            ] = c.Grpc.ChannelState.IDLE
            options: t.JsonMapping | None = u.Field(
                default_factory=lambda: MappingProxyType({}),
                description="Channel configuration options",
            )
            grpc_channel: Annotated[
                p.Grpc.GrpcChannel | None,
                u.Field(description="Underlying gRPC channel instance"),
            ] = None

            def connect(self) -> p.Result[Self]:
                """Transition to connecting."""
                return self.transition(
                    self.state,
                    "connecting",
                    {"idle": {"connecting"}},
                ).map(lambda update: self.model_copy(update=update.model_dump()))

            def disconnect(self) -> p.Result[Self]:
                """Transition to idle."""
                return r[Self](
                    value=self.model_copy(
                        update={"state": c.Grpc.ChannelState.IDLE.value}
                    ),
                    success=True,
                )

            def ready(self) -> bool:
                """Check readiness."""
                return self.state == "ready"

            def mark_ready(self) -> p.Result[Self]:
                """Transition to ready."""
                return self.transition(
                    self.state,
                    "ready",
                    {"connecting": {"ready"}},
                ).map(lambda update: self.model_copy(update=update.model_dump()))

            @override
            def validate_business_rules(self) -> p.Result[bool]:
                """Functional validation composition."""
                if not self.target.strip():
                    return r[bool].fail("Channel target cannot be empty")
                return r[bool].ok(True)

        class Server(Entity, StateMachine):
            """Generic gRPC server with state machine and validation delegation."""

            host: Annotated[
                str,
                u.Field(
                    description="Server bind host address",
                ),
            ] = c.Grpc.GrpcNetwork.DEFAULT_HOST
            port: Annotated[
                t.PortNumber,
                u.Field(
                    description="Server listen port number",
                ),
            ] = c.Grpc.GrpcNetwork.DEFAULT_GRPC_PORT
            state: Annotated[
                c.Grpc.ServerState,
                u.Field(
                    description="Current server lifecycle state",
                ),
            ] = c.Grpc.ServerState.STOPPED
            max_workers: Annotated[
                t.WorkerCount,
                u.Field(
                    description="Maximum worker threads for request handling",
                ),
            ] = c.Grpc.Service.DEFAULT_MAX_WORKERS
            services: Annotated[
                Sequence[p.Grpc.GrpcServicer],
                u.Field(description="gRPC services"),
            ] = u.Field(default_factory=tuple)
            grpc_server: Annotated[
                p.Grpc.GrpcServer | None,
                u.Field(description="Underlying gRPC server instance"),
            ] = None

            def add_service(self, service: p.Grpc.GrpcServicer) -> p.Result[Self]:
                """Add service functionally.

                Args:
                service: gRPC service t.JsonValue (dynamic type from grpc library)

                """
                return r[Self](
                    value=self.model_copy(
                        update={"services": [*self.services, service]}
                    ),
                    success=True,
                )

            def mark_running(self) -> p.Result[Self]:
                """Transition to running."""
                return self.transition(
                    self.state,
                    "running",
                    {"starting": {"running"}},
                ).map(lambda update: self.model_copy(update=update.model_dump()))

            def mark_stopped(self) -> p.Result[Self]:
                """Transition to stopped."""
                if self.state not in {"stopping", "running"}:
                    return (
                        r[Self]
                        .fail(f"Cannot mark stopped from {self.state}")
                        .map(lambda _unused: self)
                    )
                return r[Self](
                    value=self.model_copy(
                        update={"state": c.Grpc.ServerState.STOPPED.value}
                    ),
                    success=True,
                )

            def start(self) -> p.Result[Self]:
                """Transition to starting."""
                return self.transition(
                    self.state,
                    "starting",
                    {"stopped": {"starting"}},
                ).map(lambda update: self.model_copy(update=update.model_dump()))

            def stop(self) -> p.Result[Self]:
                """Transition to stopping."""
                return self.transition(
                    self.state,
                    "stopping",
                    {"running": {"stopping"}},
                ).map(lambda update: self.model_copy(update=update.model_dump()))

            @override
            def validate_business_rules(self) -> p.Result[bool]:
                """Delegate validation to generic validators."""
                if not self.host.strip():
                    return r[bool].fail("Server host cannot be empty")
                # Port range validation using IANA standard range
                min_port = 1
                max_port = 65535
                if not (min_port <= self.port <= max_port):
                    return r[bool].fail(f"Invalid port: {self.port}")
                if self.max_workers < 1:
                    return r[bool].fail("Max workers must be >= 1")
                return r[bool].ok(True)

        class Service(Entity):
            """Generic gRPC service with validation delegation."""

            name: Annotated[str, u.Field(description="Service name identifier")] = ""
            methods: t.StrSequence = u.Field(
                default_factory=tuple,
                description="Registered RPC method names",
            )

            @u.field_validator("methods")
            @classmethod
            def validate_methods(cls, v: t.StrSequence) -> t.StrSequence:
                """Validate methods list is not empty with valid items."""
                if not v:
                    msg = "methods cannot be empty"
                    raise ValueError(msg)
                for method in v:
                    if not method or not method.strip():
                        msg = "method cannot be empty"
                        raise ValueError(msg)
                return v

            @u.field_validator("name")
            @classmethod
            def validate_name(cls, v: str) -> str:
                """Validate name is not empty or whitespace."""
                if not v or not v.strip():
                    msg = "name cannot be empty"
                    raise ValueError(msg)
                return v

            def add_method(self, method_name: str) -> p.Result[Self]:
                """Add method functionally."""
                if not method_name.strip() or method_name in self.methods:
                    return r[Self].fail("Invalid method").map(lambda _unused: self)
                return r[Self](
                    value=self.model_copy(
                        update={"methods": [*self.methods, method_name]}
                    ),
                    success=True,
                )

            def has_method(self, method_name: str) -> bool:
                """Check method existence."""
                return method_name in self.methods

        class Client(Entity):
            """Generic gRPC client with channel delegation."""

            channel: Annotated[
                FlextGrpcModels.Grpc.Channel | None,
                u.Field(description="Associated gRPC channel for communication"),
            ] = None
            options: t.JsonMapping | None = u.Field(
                default_factory=lambda: MappingProxyType({}),
                description="Client configuration options",
            )
            grpc_stub: Annotated[
                p.Grpc.GrpcStub | None,
                u.Field(description="gRPC client stub for RPC calls"),
            ] = None

            def connect_to(self, target: str) -> p.Result[Self]:
                """Connect functionally."""
                channel = FlextGrpcModels.Grpc.Channel(
                    target=target,
                    state=c.Grpc.ChannelState.IDLE,
                    options={},
                    domain_events=[],
                )
                return r[Self](
                    value=self.model_copy(update={"channel": channel}), success=True
                )

            @override
            def validate_business_rules(self) -> p.Result[bool]:
                """Delegate validation."""
                if self.channel and self.channel.validate_business_rules().failure:
                    return r[bool].fail("Invalid channel")
                return r[bool].ok(True)

        class GrpcStream(Entity):
            """Generic gRPC stream with validation delegation."""

            id: Annotated[str, u.Field(description="Unique stream identifier")] = ""
            method_name: Annotated[
                str, u.Field(description="RPC method name for this stream")
            ] = ""
            stream_type: Annotated[
                c.Grpc.GrpcOperations,
                u.Field(
                    description="Stream communication pattern type",
                ),
            ] = c.Grpc.GrpcOperations.UNARY
            grpc_stub: Annotated[
                p.Grpc.GrpcStub | None,
                u.Field(description="gRPC stub used by this stream"),
            ] = None

            @u.field_validator("method_name")
            @classmethod
            def validate_method_name(cls, v: str) -> str:
                """Validate method_name is not empty or whitespace."""
                if not v or not v.strip():
                    msg = "method_name cannot be empty"
                    raise ValueError(msg)
                return v

        class CompleteSetup(m.BaseModel):
            """Complete gRPC setup result with server, client, and service."""

            server: FlextGrpcModels.Grpc.Server = u.Field(
                description="Configured gRPC server instance"
            )
            client: FlextGrpcModels.Grpc.Client = u.Field(
                description="Configured gRPC client instance"
            )
            service: FlextGrpcModels.Grpc.Service = u.Field(
                description="Configured gRPC service definition"
            )
            target: str = u.Field(description="Target server address for the setup")


m = FlextGrpcModels

__all__: list[str] = ["FlextGrpcModels", "m"]
