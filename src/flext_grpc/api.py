"""FLEXT gRPC - Generic Unified Facade with Patterns.

Generic facade using extensive Pydantic models, SOLID delegation,
functional composition, and Python 3.13+ patterns for minimal code.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Callable
from typing import TypeVar

from flext_core import r
from pydantic import BaseModel, ConfigDict, Field, ValidationError

from flext_grpc.models import FlextGrpcModels as m
from flext_grpc.constants import c
from flext_grpc.services import FlextGrpcServices, ServicePayload
from flext_grpc.settings import FlextGrpcSettings
from flext_grpc.typings import t
from flext_grpc.utilities import FlextGrpcUtilities

T = TypeVar("T", bound=BaseModel)
type EntityKwargValue = object


class _EntityValidationSnapshot(BaseModel):
    """Normalized validation snapshot for entity rule checks."""

    model_config = ConfigDict(from_attributes=True)

    is_success: bool = True
    error: str | None = None


class _ServerCreateInput(BaseModel):
    """Validated input payload for server creation."""

    host: str = c.Grpc.GrpcNetwork.DEFAULT_HOST
    port: int = c.Grpc.GrpcNetwork.DEFAULT_GRPC_PORT
    max_workers: int = c.Grpc.Service.DEFAULT_MAX_WORKERS


class _ChannelCreateInput(BaseModel):
    """Validated input payload for channel creation."""

    target: str
    options: t.GrpcOptions = Field(default_factory=dict)


class _ServiceCreateInput(BaseModel):
    """Validated input payload for service creation."""

    name: str
    methods: list[str] = Field(default_factory=list)


class _CompleteSetupInput(BaseModel):
    """Validated input payload for complete setup creation."""

    host: str = c.Grpc.GrpcNetwork.DEFAULT_HOST
    port: int = c.Grpc.GrpcNetwork.DEFAULT_GRPC_PORT
    service_name: str = "DefaultService"
    methods: list[str] = Field(default_factory=lambda: ["HealthCheck"])


class _CompleteSetupResult(BaseModel):
    """Typed payload for complete setup creation."""

    server: m.Server
    client: m.Client
    service: m.Service
    target: str


class _ServerEntityEnvelope(BaseModel):
    """Typed envelope validating server entity results."""

    entity: m.Server


class _ClientEntityEnvelope(BaseModel):
    """Typed envelope validating client entity results."""

    entity: m.Client


class _ChannelEntityEnvelope(BaseModel):
    """Typed envelope validating channel entity results."""

    entity: m.Channel


class _ServiceEntityEnvelope(BaseModel):
    """Typed envelope validating service entity results."""

    entity: m.Service


class _StreamEntityEnvelope(BaseModel):
    """Typed envelope validating stream entity results."""

    entity: m.GrpcStream


def _result_as_object[T](result: r[T]) -> r[object]:
    """Normalize typed FlextResult values into object-typed results."""
    if result.is_failure:
        return r.fail(result.error or "Operation failed")
    return r.ok(result.value)


GenericOperationSpec = m.OperationSpec
GenericRequest = m.Request
GenericResponse = m.Response


class FlextGrpc:
    """Generic unified gRPC facade with SOLID patterns and minimal code.

    Uses generic types, functional composition, Pydantic v2 models, and delegation
    to reduce bloat while maintaining full functionality with Python 3.13+ features.
    """

    def __init__(self, config: FlextGrpcSettings | None = None) -> None:
        """Initialize facade with FLEXT ecosystem integration."""
        super().__init__()
        self._service = FlextGrpcServices()
        self._grpc_config = config if config is not None else FlextGrpcSettings()
        # Use object.__setattr__ to bypass type checker for dynamic attribute assignment
        # since base class expects FlextSettings | None but we use FlextGrpcSettings
        object.__setattr__(self, "_config", self._grpc_config)

    @property
    def grpc_config(self) -> FlextGrpcSettings:
        """Get gRPC-specific configuration."""
        # Type narrowing: _grpc_config is always FlextGrpcSettings by design
        return self._grpc_config

    def execute(self, **_kwargs: object) -> r[FlextGrpcSettings]:
        """Execute main facade operation."""
        return r.ok(self.grpc_config)

    def validate_target(self, target: str) -> bool:
        """Validate gRPC target string."""
        return t.Grpc.GrpcValidation.validate_target(target)

    def parse_address(self, address: str) -> r[tuple[str, int]]:
        """Parse gRPC address string."""
        if not t.Grpc.GrpcValidation.validate_target(address):
            return r.fail(f"Invalid address: {address}")
        return r.ok(t.Grpc.GrpcValidation.parse_target(address))

    def create_entity(
        self,
        entity_type: str,
        **kwargs: EntityKwargValue,
    ) -> r[object]:
        """Generic entity creation with Pydantic validation and delegation."""
        factory = self._get_entity_factory(entity_type)
        if factory is None:
            return r.fail(f"Unknown entity type: {entity_type}")

        # Call factory and handle result (typed so Pyright knows .is_success/.error)
        result: r[object] = factory(**kwargs)
        if not result.is_success:
            return r.fail(f"Failed to create entity: {result.error}")

        entity = result.value

        validate_method = (
            entity.validate_business_rules
            if hasattr(entity, "validate_business_rules")
            else None
        )
        if validate_method is not None and callable(validate_method):
            validation_result = validate_method()
            try:
                validation_snapshot = _EntityValidationSnapshot.model_validate(
                    validation_result,
                )
            except ValidationError:
                validation_snapshot = _EntityValidationSnapshot()
            if not validation_snapshot.is_success:
                message = validation_snapshot.error or "Unknown error"
                return r.fail(f"Entity validation failed: {message}")

        return r.ok(entity)

    def _get_entity_factory(self, entity_type: str) -> Callable[..., r[object]] | None:
        """Get entity factory for dynamic dispatch.

        Wrappers normalize return to r[object] for homogeneous dispatch.
        """

        def _wrap_factory[T](fn: Callable[..., r[T]]) -> Callable[..., r[object]]:
            def _inner(
                **kw: EntityKwargValue,
            ) -> r[object]:
                return _result_as_object(fn(**kw))

            return _inner

        match entity_type:
            case "server":
                return _wrap_factory(FlextGrpcUtilities.create_server_entity)
            case "client":
                return _wrap_factory(FlextGrpcUtilities.create_client_entity)
            case "channel":
                return _wrap_factory(FlextGrpcUtilities.create_channel_entity)
            case "service":
                return _wrap_factory(FlextGrpcUtilities.create_service_entity)
            case "stream":
                return _wrap_factory(FlextGrpcUtilities.create_stream_entity)
            case _:
                return None

    def execute_operation(
        self,
        request: m.OperationExecutionRequest,
    ) -> r[FlextGrpcSettings]:
        """Execute operation with validation, timeout, retry, and monitoring (Service protocol)."""
        operation = self._get_operation(request.operation_name)
        if operation is None:
            return r.fail(f"Unknown operation: {request.operation_name}")

        # Execute operation with delegation
        result = operation(**request.arguments, **request.keyword_arguments)
        if result.is_failure:
            return r.fail(result.error or "Unknown error")
        return r.ok(self.grpc_config)

    def _get_operation(self, operation_name: str) -> Callable[..., r[object]] | None:
        """Get operation handler for dynamic dispatch.

        Wrappers normalize return to r[object] for homogeneous dispatch.
        """

        def _wrap_op[T](fn: Callable[..., r[T]]) -> Callable[..., r[object]]:
            def _inner(*args: object, **kwargs: object) -> r[object]:
                return _result_as_object(fn(*args, **kwargs))

            return _inner

        match operation_name:
            case "start_server":
                return _wrap_op(self._service.start_server)
            case "stop_server":
                return _wrap_op(self._service.stop_server)
            case "connect_client":
                return _wrap_op(self._service.connect_client)
            case "disconnect_client":
                return _wrap_op(self._service.disconnect_client)
            case "make_call":
                return _wrap_op(self._service.make_call)
            case "send_data":
                return _wrap_op(self._service.send_data)
            case "close_stream":
                return _wrap_op(self._service.close_stream)
            case _:
                return None

    def create_server(
        self,
        **kwargs: str | int | bool | list[str] | None,
    ) -> r[m.Server]:
        """Create server entity with functional defaults."""
        try:
            server_input = _ServerCreateInput.model_validate(kwargs)
        except ValidationError as e:
            return r.fail(f"Server input validation failed: {e}")

        result = self.create_entity(
            "server",
            host=server_input.host,
            port=server_input.port,
            max_workers=server_input.max_workers,
        )
        if result.is_failure:
            return r.fail(result.error or "Server creation failed")

        try:
            validated_server = _ServerEntityEnvelope.model_validate(
                {"entity": result.value},
            )
        except ValidationError:
            return r.fail(f"Invalid server entity type: {type(result.value)}")

        return r.ok(validated_server.entity)

    def create_client(
        self,
        **kwargs: str | int | bool | None,
    ) -> r[m.Client]:
        """Create client with channel composition."""
        result = self.create_entity("client", **kwargs)
        if result.is_failure:
            return r.fail(result.error or "Client creation failed")

        try:
            validated_client = _ClientEntityEnvelope.model_validate(
                {"entity": result.value},
            )
        except ValidationError:
            return r.fail(f"Invalid client entity type: {type(result.value)}")

        return r.ok(validated_client.entity)

    def create_channel(
        self,
        **kwargs: EntityKwargValue,
    ) -> r[m.Channel]:
        """Create channel entity with defaults."""
        try:
            channel_input = _ChannelCreateInput.model_validate(kwargs)
        except ValidationError as e:
            return r.fail(f"Channel input validation failed: {e}")

        result = self.create_entity(
            "channel",
            target=channel_input.target,
            options=channel_input.options,
        )
        if result.is_failure:
            return r.fail(result.error or "Channel creation failed")

        try:
            validated_channel = _ChannelEntityEnvelope.model_validate(
                {"entity": result.value},
            )
        except ValidationError:
            return r.fail(f"Invalid channel entity type: {type(result.value)}")

        return r.ok(validated_channel.entity)

    def create_service(
        self,
        **kwargs: str | list[str] | None,
    ) -> r[m.Service]:
        """Create service entity with defaults."""
        try:
            service_input = _ServiceCreateInput.model_validate(kwargs)
        except ValidationError as e:
            return r.fail(f"Service input validation failed: {e}")

        result = self.create_entity(
            "service",
            name=service_input.name,
            methods=service_input.methods,
        )
        if result.is_failure:
            return r.fail(result.error or "Service creation failed")

        try:
            validated_service = _ServiceEntityEnvelope.model_validate(
                {"entity": result.value},
            )
        except ValidationError:
            return r.fail(f"Invalid service entity type: {type(result.value)}")

        return r.ok(validated_service.entity)

    def create_stream(
        self,
        method_name: str = "DefaultMethod",
        stream_type: str = "unary",
        **kwargs: str | int | bool | None,
    ) -> r[m.GrpcStream]:
        """Create stream with validation."""
        if not method_name.strip():
            return r.fail("Stream method name cannot be empty")

        if stream_type not in c.Grpc.STREAM_TYPES:
            return r.fail(f"Invalid stream type: {stream_type}")

        result = self.create_entity(
            "stream",
            method_name=method_name,
            stream_type=stream_type,
            **kwargs,
        )
        if result.is_failure:
            return r.fail(result.error or "Stream creation failed")

        try:
            validated_stream = _StreamEntityEnvelope.model_validate(
                {"entity": result.value},
            )
        except ValidationError:
            return r.fail(f"Invalid stream entity type: {type(result.value)}")

        return r.ok(validated_stream.entity)

    # === DELEGATED OPERATIONS ===

    def start_server(
        self,
        server: m.Server,
    ) -> r[m.Server]:
        """Delegate server start.

        Args:
        server: gRPC server entity to start

        Returns:
        Started server entity

        """
        return self._service.start_server(server)

    def stop_server(
        self,
        server: m.Server,
    ) -> r[m.Server]:
        """Delegate server stop.

        Args:
        server: gRPC server entity to stop

        Returns:
        Stopped server entity

        """
        return self._service.stop_server(server)

    def connect_client(self, target: str) -> r[m.Client]:
        """Delegate client connection.

        Args:
        target: Target address to connect to

        Returns:
        Connected client entity

        """
        return self._service.connect_client(target)

    def disconnect_client(
        self,
        client: m.Client,
    ) -> r[m.Client]:
        """Delegate client disconnection.

        Args:
        client: gRPC client entity to disconnect

        Returns:
        Disconnected client entity

        """
        return self._service.disconnect_client(client)

    def make_call(
        self,
        client: m.Client,
        method: str,
        request: t.ConfigValue,
    ) -> r[ServicePayload]:
        """Delegate method calls.

        Args:
        client: gRPC client entity
        method: gRPC method name
        request: Request message (gRPC protocol message - dynamic type)

        Returns:
        Response data dictionary

        Note: Uses ConfigValue for gRPC protocol message compatibility

        """
        return self._service.make_call(client, method, request)

    def send_data(
        self,
        stream: m.GrpcStream,
        data: t.ConfigValue,
    ) -> r[ServicePayload]:
        """Delegate data sending.

        Args:
        stream: gRPC stream entity
        data: Message data (gRPC protocol message - dynamic type)

        Returns:
        Response data dictionary

        Note: Uses object for gRPC message compatibility

        """
        return self._service.send_data(stream, data)

    def close_stream(
        self,
        stream: m.GrpcStream,
    ) -> r[m.GrpcStream]:
        """Delegate stream closing.

        Args:
        stream: gRPC stream entity to close

        Returns:
        Closed stream entity

        """
        return self._service.close_stream(stream)

    def create_complete_setup(
        self,
        **kwargs: str | int | list[str] | None,
    ) -> r[_CompleteSetupResult]:
        """Complete setup using functional composition."""
        try:
            setup_input = _CompleteSetupInput.model_validate(kwargs)
        except ValidationError as e:
            return r.fail(f"Complete setup validation failed: {e}")

        target = f"{setup_input.host}:{setup_input.port}"

        # Advanced functional composition
        return (
            self
            .create_server(host=setup_input.host, port=setup_input.port)
            .flat_map(lambda s: self.create_client(target=target).map(lambda c: (s, c)))
            .flat_map(
                lambda pair: self.create_service(
                    name=setup_input.service_name,
                    methods=setup_input.methods,
                ).map(
                    lambda svc: _CompleteSetupResult(
                        server=pair[0],
                        client=pair[1],
                        service=svc,
                        target=target,
                    ),
                ),
            )
        )


__all__ = ["FlextGrpc", "GenericOperationSpec", "GenericRequest", "GenericResponse"]
