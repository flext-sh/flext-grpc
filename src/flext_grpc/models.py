"""FLEXT gRPC Models - Consolidated Pydantic v2 Models.

Unified namespace with nested classes following FLEXT principles and SOLID design.
All domain models consolidated into a single class with nested structures.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Annotated, Self, override

from pydantic import BaseModel, Field, computed_field, field_validator

from flext_core import m
from flext_grpc import c, p, r, t, u


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

            message: Annotated[str, Field(description="Echo message")]

        class EchoResponse(m.Value):
            """Echo response message (immutable value model)."""

            message: Annotated[str, Field(description="Echo message")]
            server_id: Annotated[
                str,
                Field(default="", description="Server identifier"),
            ]
            timestamp: datetime = Field(
                default_factory=datetime.now, description="Response timestamp"
            )

        class HealthRequest(m.Value):
            """Health check request message (immutable value model)."""

            service: Annotated[str, Field(default="", description="Service name")]

        class HealthResponse(m.Value):
            """Health check response message (immutable value model)."""

            status: Annotated[str, Field(description="Health status")]
            message: Annotated[
                str,
                Field(default="", description="Health check message"),
            ]

        class StreamInfo(m.Value):
            """Basic stream information (immutable value model)."""

            stream_id: str = Field(description="Unique stream identifier")
            stream_type: str = Field(description="Stream communication type")
            target: str = Field(description="Target endpoint address")
            created_at: datetime = Field(
                default_factory=datetime.now, description="Stream creation timestamp"
            )
            total_requests_sent: t.NonNegativeInt = Field(
                default=0, description="Total requests sent on stream"
            )
            average_latency_ms: t.NonNegativeFloat = Field(
                default=0.0, description="Average latency in milliseconds"
            )
            error_count: t.NonNegativeInt = Field(
                default=0, description="Number of errors on stream"
            )

        class HealthCheck(m.Value):
            """gRPC health check model (immutable value model)."""

            service_name: Annotated[str, Field(description="Service name")]
            status: Annotated[str, Field(description="Health status")]
            timestamp: Annotated[datetime, Field(description="Check timestamp")]

        class ServiceDefinition(m.Value):
            """gRPC service definition model (immutable value model)."""

            service_name: Annotated[str, Field(description="Service name")]
            methods: t.StrSequence = Field(
                default_factory=list, description="Service methods"
            )
            endpoint: Annotated[
                str | None,
                Field(default=None, description="Service endpoint"),
            ]
            metadata: Annotated[
                t.OptionalContainerValueMapping | None,
                Field(
                    default=None,
                    description="Service metadata",
                ),
            ]

        class StreamMetrics(m.Value):
            """gRPC stream metrics model (immutable value model)."""

            stream_id: Annotated[str, Field(description="Stream ID")]
            throughput_rps: Annotated[
                t.NonNegativeFloat,
                Field(
                    description="Throughput in requests per second",
                ),
            ]
            latency_p50: Annotated[
                t.NonNegativeFloat,
                Field(description="50th percentile latency"),
            ]
            latency_p95: Annotated[
                t.NonNegativeFloat,
                Field(description="95th percentile latency"),
            ]
            latency_p99: Annotated[
                t.NonNegativeFloat,
                Field(description="99th percentile latency"),
            ]
            error_rate: Annotated[t.NonNegativeFloat, Field(description="Error rate")]
            memory_usage_bytes: Annotated[
                t.NonNegativeInt,
                Field(description="Memory usage in bytes"),
            ]

        class ServiceMetrics(m.Value):
            """gRPC service metrics model (immutable value model)."""

            service_name: Annotated[str, Field(description="Service name")]
            total_requests: Annotated[
                t.NonNegativeInt,
                Field(description="Total requests"),
            ]
            successful_requests: Annotated[
                t.NonNegativeInt,
                Field(description="Successful requests"),
            ]
            failed_requests: Annotated[
                t.NonNegativeInt,
                Field(description="Failed requests"),
            ]
            avg_response_time: Annotated[
                t.NonNegativeFloat,
                Field(description="Average response time"),
            ]
            active_connections: Annotated[
                t.NonNegativeInt,
                Field(description="Active connections"),
            ]

        class OperationExecutionRequest(m.Value):
            """Operation execution request for gRPC service operations."""

            operation_name: Annotated[
                str,
                Field(description="Operation name to execute"),
            ]
            arguments: t.ConfigurationMapping = Field(
                default_factory=dict, description="Positional arguments as dict"
            )
            keyword_arguments: t.ConfigurationMapping = Field(
                default_factory=dict, description="Keyword arguments"
            )

        class ServerConfig(m.Value):
            """Basic server configuration (immutable value model)."""

            host: str = Field(
                default=c.Grpc.GrpcNetwork.DEFAULT_HOST,
                description="Server host address",
            )
            port: t.PortNumber = Field(
                default=c.Grpc.GrpcNetwork.DEFAULT_GRPC_PORT,
                description="Server port number",
            )
            max_workers: t.WorkerCount = Field(
                default=c.Grpc.Service.DEFAULT_MAX_WORKERS,
                description="Maximum worker threads",
            )
            timeout: t.PositiveTimeout = Field(
                default=c.Grpc.GrpcNetwork.DEFAULT_TIMEOUT,
                description="Request timeout in seconds",
            )

        class ClientConfig(m.Value):
            """Basic client configuration (immutable value model)."""

            target: str = Field(
                default=f"{c.Grpc.GrpcNetwork.DEFAULT_HOST}:{c.Grpc.GrpcNetwork.DEFAULT_GRPC_PORT}",
                description="Target server address",
            )
            timeout: t.PositiveTimeout = Field(
                default=c.Grpc.GrpcNetwork.DEFAULT_TIMEOUT,
                description="Request timeout in seconds",
            )

        class ChannelConfig(m.Value):
            """Basic channel configuration (immutable value model)."""

            address: str = Field(description="Channel address")
            options: t.OptionalContainerValueMapping | None = Field(
                default=None, description="Channel options"
            )

        class SecurityConfig(m.Value):
            """Generic gRPC security configuration with validation."""

            tls_enabled: Annotated[
                bool,
                Field(
                    default=False,
                    description="Enable TLS encryption",
                ),
            ]
            tls_cert_file: Annotated[
                str | None,
                Field(
                    default=None,
                    description="TLS certificate file path",
                ),
            ]
            tls_key_file: Annotated[
                str | None,
                Field(
                    default=None,
                    description="TLS private key file path",
                ),
            ]
            tls_ca_file: Annotated[
                str | None,
                Field(
                    default=None,
                    description="TLS CA certificate file path",
                ),
            ]
            auth_enabled: Annotated[
                bool,
                Field(
                    default=False,
                    description="Enable authentication",
                ),
            ]
            auth_token: Annotated[
                str | None,
                Field(
                    default=None,
                    description="Authentication token",
                ),
            ]
            client_cert_required: Annotated[
                bool,
                Field(
                    default=False,
                    description="Require client certificates",
                ),
            ]

        class NetworkConfig(m.Value):
            """Generic gRPC network configuration with validation."""

            host: Annotated[
                t.NonEmptyStr,
                Field(
                    default=c.Grpc.GrpcNetwork.DEFAULT_HOST,
                    description="gRPC server host",
                ),
            ]
            port: Annotated[
                t.PortNumber,
                Field(
                    default=c.Grpc.GrpcNetwork.DEFAULT_GRPC_PORT,
                    description="gRPC server port",
                ),
            ]
            max_connections: Annotated[
                t.BatchSize,
                Field(
                    default=c.Grpc.Service.DEFAULT_MAX_CONCURRENT_RPCS,
                    description="Maximum concurrent connections",
                ),
            ]
            keepalive_time: Annotated[
                t.PositiveInt,
                Field(
                    default=c.Grpc.GrpcNetwork.DEFAULT_KEEPALIVE_TIME_MS // 1000,
                    description="Keepalive ping interval (seconds)",
                ),
            ]
            keepalive_timeout: Annotated[
                t.PositiveInt,
                Field(
                    default=c.Grpc.GrpcNetwork.DEFAULT_KEEPALIVE_TIMEOUT_MS // 1000,
                    description="Keepalive timeout (seconds)",
                ),
            ]

        class PerformanceConfig(m.Value):
            """Generic gRPC performance configuration."""

            max_workers: Annotated[
                int,
                Field(
                    default=c.Grpc.Service.MAX_WORKERS,
                    ge=1,
                    le=1000,
                    description="Maximum worker threads",
                ),
            ]
            max_concurrent_rpcs: Annotated[
                t.BatchSize,
                Field(
                    default=c.Grpc.Service.DEFAULT_MAX_CONCURRENT_RPCS,
                    description="Maximum concurrent RPCs",
                ),
            ]
            max_receive_message_length: Annotated[
                int,
                Field(
                    default=c.Grpc.PerformanceLimits.DEFAULT_MESSAGE_LENGTH,
                    ge=c.Grpc.PerformanceLimits.MIN_MESSAGE_LENGTH,
                    le=c.Grpc.PerformanceLimits.MAX_MESSAGE_LENGTH,
                    description="Maximum receive message length (bytes)",
                ),
            ]
            max_send_message_length: Annotated[
                int,
                Field(
                    default=c.Grpc.PerformanceLimits.DEFAULT_MESSAGE_LENGTH,
                    ge=c.Grpc.PerformanceLimits.MIN_MESSAGE_LENGTH,
                    le=c.Grpc.PerformanceLimits.MAX_MESSAGE_LENGTH,
                    description="Maximum send message length (bytes)",
                ),
            ]
            thread_pool_size: Annotated[
                int,
                Field(
                    default=c.Grpc.PerformanceLimits.DEFAULT_THREAD_POOL_SIZE,
                    ge=c.Grpc.PerformanceLimits.MIN_THREAD_POOL_SIZE,
                    le=c.Grpc.PerformanceLimits.MAX_THREAD_POOL_SIZE,
                    description="Thread pool size",
                ),
            ]

        class StreamingConfig(m.Value):
            """Generic gRPC streaming configuration."""

            enabled: Annotated[
                bool,
                Field(
                    default=True,
                    description="Enable streaming operations",
                ),
            ]
            max_concurrent_streams: Annotated[
                t.WorkerCount,
                Field(
                    default=c.Grpc.Streaming.DEFAULT_MAX_CONCURRENT_STREAMS,
                    description="Maximum concurrent streams",
                ),
            ]
            stream_buffer_size: Annotated[
                int,
                Field(
                    default=c.Grpc.Streaming.DEFAULT_BUFFER_SIZE,
                    ge=c.Grpc.Streaming.MIN_BUFFER_SIZE,
                    le=c.Grpc.Streaming.MAX_BUFFER_SIZE,
                    description="Stream buffer size",
                ),
            ]
            max_stream_duration: Annotated[
                int,
                Field(
                    default=300,
                    ge=10,
                    le=3600,
                    description="Maximum stream duration (seconds)",
                ),
            ]
            enable_compression: Annotated[
                bool,
                Field(
                    default=True,
                    description="Enable message compression",
                ),
            ]

        class ClientSettingsConfig(m.Value):
            """Generic gRPC client configuration."""

            timeout: Annotated[
                t.PositiveTimeout,
                Field(
                    default=30.0,
                    description="RPC timeout (seconds)",
                ),
            ]
            retry_attempts: Annotated[
                t.RetryCount,
                Field(
                    default=3,
                    description="Maximum retry attempts",
                ),
            ]
            retry_backoff: Annotated[
                float,
                Field(
                    default=1.0,
                    gt=0,
                    le=60,
                    description="Retry backoff multiplier",
                ),
            ]
            load_balancing_policy: Annotated[
                str,
                Field(
                    default="round_robin",
                    description="Load balancing policy",
                ),
            ]
            channel_options: Annotated[
                t.HeaderMapping,
                Field(
                    description="Additional channel options",
                ),
            ] = Field(default_factory=dict)

        class MonitoringConfig(m.Value):
            """Generic gRPC monitoring and observability configuration."""

            metrics_enabled: Annotated[
                bool,
                Field(
                    default=True,
                    description="Enable metrics collection",
                ),
            ]
            tracing_enabled: Annotated[
                bool,
                Field(
                    default=False,
                    description="Enable distributed tracing",
                ),
            ]
            health_check_enabled: Annotated[
                bool,
                Field(
                    default=True,
                    description="Enable health checks",
                ),
            ]
            health_check_interval: Annotated[
                int,
                Field(
                    default=30,
                    ge=5,
                    le=300,
                    description="Health check interval (seconds)",
                ),
            ]
            log_level: Annotated[
                str,
                Field(default="INFO", description="Logging level"),
            ]

        class StateTransition(m.Value):
            """State transition result model."""

            state: str = Field(description="Target state after transition")

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

        class StateMachine(BaseModel):
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

            name: Annotated[str, Field(min_length=1, description="Operation name")]
            entity_type: Annotated[
                t.Grpc.EntityKind,
                Field(description="Type of entity to operate on"),
            ]
            method_name: Annotated[
                str | None,
                Field(
                    default=None,
                    description="Method to invoke on entity",
                ),
            ]
            parameters: Annotated[
                Mapping[str, t.OptionalContainerValueMapping],
                Field(
                    description="Operation parameters",
                ),
            ] = Field(default_factory=dict)

        class Request(m.Value):
            """Generic request model with validation."""

            operation: FlextGrpcModels.Grpc.OperationSpec = Field(
                description="Operation specification to execute",
            )
            entity: Annotated[
                BaseModel | None,
                Field(
                    default=None,
                    description="Associated entity",
                ),
            ]
            data: Annotated[
                t.OptionalContainerValueMapping | None,
                Field(
                    default=None,
                    description="Request data",
                ),
            ]

            @computed_field
            def valid(self) -> bool:
                """Check if request is valid."""
                return bool(self.operation.name.strip())

        class Response(m.Value):
            """Generic response model with metadata."""

            success: Annotated[bool, Field(description="Operation success status")]
            data: Annotated[
                BaseModel | None,
                Field(
                    default=None,
                    description="Response data",
                ),
            ]
            error: Annotated[
                str | None,
                Field(
                    default=None,
                    description="Error message if failed",
                ),
            ]
            metadata: Annotated[
                Mapping[str, t.OptionalContainerValueMapping],
                Field(
                    description="Response metadata",
                ),
            ] = Field(default_factory=dict)

            @computed_field
            def has_error(self) -> bool:
                """Check if response has error."""
                return not self.success or self.error is not None

        class Payload(BaseModel):
            """Structured payload model replacing ad-hoc dict responses."""

            values: t.OptionalContainerValueMapping = Field(
                default_factory=dict, description="Key-value payload data"
            )

            @classmethod
            def from_values(cls, **values: t.OptionalContainerValue) -> Self:
                """Build payload from keyword values."""

                def normalize_payload_value(
                    value: t.OptionalContainerValue,
                ) -> t.OptionalContainerValue:
                    if value is None:
                        return ""
                    if u.primitive(value):
                        return value
                    return str(value)

                normalized_values: t.OptionalContainerValueMapping = {
                    metric_key: normalize_payload_value(metric_value)
                    for metric_key, metric_value in values.items()
                }
                return cls(values=normalized_values)

        class Entity(m.Entity):
            """Generic base entity with functional patterns."""

            def copy_with(self, **kwargs: t.Scalar | None) -> p.Result[Self]:
                """Functional copy using r.

                Args:
                **kwargs: Field updates for the entity

                """
                return r[Self].create_from_callable(
                    lambda: self.model_copy(update=kwargs),
                )

            def validate_business_rules(self) -> p.Result[bool]:
                """Override in subclasses for specific validation."""
                return r[bool].ok(True)

        class Channel(Entity, StateMachine):
            """Generic gRPC channel with state machine delegation."""

            target: str = Field(default="", description="gRPC server target address")
            state: c.Grpc.ChannelState = Field(
                default=c.Grpc.ChannelState.IDLE,
                description="Current channel connection state",
            )
            options: t.OptionalContainerValueMapping = Field(
                default_factory=dict, description="Channel configuration options"
            )
            grpc_channel: Annotated[
                p.Grpc.GrpcChannel | None,
                Field(default=None, description="Underlying gRPC channel instance"),
            ]

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

            host: str = Field(
                default=c.Grpc.GrpcNetwork.DEFAULT_HOST,
                description="Server bind host address",
            )
            port: t.PortNumber = Field(
                default=c.Grpc.GrpcNetwork.DEFAULT_GRPC_PORT,
                description="Server listen port number",
            )
            state: c.Grpc.ServerState = Field(
                default=c.Grpc.ServerState.STOPPED,
                description="Current server lifecycle state",
            )
            max_workers: t.WorkerCount = Field(
                default=c.Grpc.Service.DEFAULT_MAX_WORKERS,
                description="Maximum worker threads for request handling",
            )
            services: Annotated[
                Sequence[p.Grpc.GrpcServicer],
                Field(description="gRPC services"),
            ] = Field(default_factory=list)
            grpc_server: Annotated[
                p.Grpc.GrpcServer | None,
                Field(default=None, description="Underlying gRPC server instance"),
            ]

            def add_service(self, service: p.Grpc.GrpcServicer) -> p.Result[Self]:
                """Add service functionally.

                Args:
                service: gRPC service t.RecursiveContainer (dynamic type from grpc library)

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

            name: str = Field(default="", description="Service name identifier")
            methods: t.StrSequence = Field(
                default_factory=list, description="Registered RPC method names"
            )

            @field_validator("methods")
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

            @field_validator("name")
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

            channel: FlextGrpcModels.Grpc.Channel | None = Field(
                default=None, description="Associated gRPC channel for communication"
            )
            options: t.OptionalContainerValueMapping = Field(
                default_factory=dict, description="Client configuration options"
            )
            grpc_stub: Annotated[
                p.Grpc.GrpcStub | None,
                Field(default=None, description="gRPC client stub for RPC calls"),
            ]

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

            id: str = Field(default="", description="Unique stream identifier")
            method_name: str = Field(
                default="", description="RPC method name for this stream"
            )
            stream_type: c.Grpc.GrpcOperations = Field(
                default=c.Grpc.GrpcOperations.UNARY,
                description="Stream communication pattern type",
            )
            grpc_stub: Annotated[
                p.Grpc.GrpcStub | None,
                Field(default=None, description="gRPC stub used by this stream"),
            ]

            @field_validator("method_name")
            @classmethod
            def validate_method_name(cls, v: str) -> str:
                """Validate method_name is not empty or whitespace."""
                if not v or not v.strip():
                    msg = "method_name cannot be empty"
                    raise ValueError(msg)
                return v

        class CompleteSetup(BaseModel):
            """Complete gRPC setup result with server, client, and service."""

            server: FlextGrpcModels.Grpc.Server = Field(
                description="Configured gRPC server instance"
            )
            client: FlextGrpcModels.Grpc.Client = Field(
                description="Configured gRPC client instance"
            )
            service: FlextGrpcModels.Grpc.Service = Field(
                description="Configured gRPC service definition"
            )
            target: str = Field(description="Target server address for the setup")


m = FlextGrpcModels

__all__: list[str] = ["FlextGrpcModels", "m"]
