"""FLEXT gRPC - Generic Unified Facade with Patterns.

Generic facade using extensive Pydantic models, SOLID delegation,
functional composition, and Python 3.13+ patterns for minimal code.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Callable
from typing import TypeVar

from flext_core import FlextModels, r
from pydantic import BaseModel

from flext_grpc.constants import FlextGrpcConstants
from flext_grpc.entities import FlextGrpcEntities
from flext_grpc.models import FlextGrpcModels
from flext_grpc.services import FlextGrpcServices
from flext_grpc.settings import FlextGrpcSettings
from flext_grpc.typings import t
from flext_grpc.utilities import FlextGrpcUtilities


def _result_as_object[T](result: r[T]) -> r[object]:
    """Normalize any FlextResult to r[object] for homogeneous dict typing."""
    if result.is_success:
        return r.ok(result.value)
    return r.fail(result.error or "Unknown error")


# Import API models from models.py (centralized location)
_m = FlextGrpcModels
GenericOperationSpec = _m.API.OperationSpec
GenericRequest = _m.API.Request
GenericResponse = _m.API.Response

# Type aliases for convenience
c = FlextGrpcConstants
m_core = FlextModels

T = TypeVar("T", bound=BaseModel)
U = TypeVar("U")  # Generic return type for factory methods
E = TypeVar("E", bound=FlextGrpcEntities.Entity)  # Generic entity type

type EntityKwargValue = (
    str
    | int
    | bool
    | float
    | list[str]
    | list[t.JsonValue]
    | dict[str, t.JsonValue]
    | None
)


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
        return t.GrpcValidation.validate_target(target)

    def parse_address(self, address: str) -> r[tuple[str, int]]:
        """Parse gRPC address string."""
        if not t.GrpcValidation.validate_target(address):
            return r.fail(f"Invalid address: {address}")
        return r.ok(t.GrpcValidation.parse_target(address))

    def create_entity(
        self,
        entity_type: str,
        **kwargs: EntityKwargValue,
    ) -> r[object]:
        """Generic entity creation with Pydantic validation and delegation."""
        entity_factories: dict[str, Callable[..., r[object]]] = (
            self._get_entity_factories()
        )
        factory = entity_factories.get(entity_type)
        if factory is None:
            return r.fail(f"Unknown entity type: {entity_type}")

        # Call factory and handle result (typed so Pyright knows .is_success/.error)
        result: r[object] = factory(**kwargs)
        if not result.is_success:
            return r.fail(f"Failed to create entity: {result.error}")

        entity = result.value

        # Delegate validation to entity if available
        if hasattr(entity, "validate_business_rules"):
            validate_method = getattr(entity, "validate_business_rules")
            if callable(validate_method):
                validation_result = validate_method()
                is_success = getattr(validation_result, "is_success", None)
                error_message = getattr(validation_result, "error", None)
                if isinstance(is_success, bool) and not is_success:
                    message = (
                        error_message
                        if isinstance(error_message, str) and error_message
                        else "Unknown error"
                    )
                    return r.fail(f"Entity validation failed: {message}")

        return r.ok(entity)

    def _get_entity_factories(self) -> dict[str, Callable[..., r[object]]]:
        """Get entity factories for dynamic dispatch.

        Wrappers normalize return to r[object] for dict homogeneity.
        """

        def _wrap_factory[T](fn: Callable[..., r[T]]) -> Callable[..., r[object]]:
            def _inner(
                **kw: EntityKwargValue,
            ) -> r[object]:
                return _result_as_object(fn(**kw))

            return _inner

        factories: dict[str, Callable[..., r[object]]] = {}
        factories["server"] = _wrap_factory(FlextGrpcUtilities.create_server_entity)
        factories["client"] = _wrap_factory(FlextGrpcUtilities.create_client_entity)
        factories["channel"] = _wrap_factory(FlextGrpcUtilities.create_channel_entity)
        factories["service"] = _wrap_factory(FlextGrpcUtilities.create_service_entity)
        factories["stream"] = _wrap_factory(FlextGrpcUtilities.create_stream_entity)
        return factories

    def execute_operation(
        self,
        request: FlextGrpcModels.Grpc.OperationExecutionRequest,
    ) -> r[FlextGrpcSettings]:
        """Execute operation with validation, timeout, retry, and monitoring (Service protocol)."""
        operations = self._get_operations()

        operation = operations.get(request.operation_name)
        if not operation:
            return r.fail(f"Unknown operation: {request.operation_name}")

        # Execute operation with delegation
        result = operation(**request.arguments, **request.keyword_arguments)

        # Return config on success, fail on error
        def _to_config(_data: object) -> FlextGrpcSettings:
            return self.grpc_config

        def _fail_msg(error_msg: object) -> r[FlextGrpcSettings]:
            return r.fail(str(error_msg) if error_msg else "Unknown error")

        return result.map(_to_config).lash(_fail_msg)

    def _get_operations(self) -> dict[str, Callable[..., r[object]]]:
        """Get operations for dynamic dispatch.

        Wrappers normalize return to r[object] for dict homogeneity.
        """

        def _wrap_op[T](fn: Callable[..., r[T]]) -> Callable[..., r[object]]:
            def _inner(*args: object, **kwargs: object) -> r[object]:
                return _result_as_object(fn(*args, **kwargs))

            return _inner

        operations: dict[str, Callable[..., r[object]]] = {}
        operations["start_server"] = _wrap_op(self._service.start_server)
        operations["stop_server"] = _wrap_op(self._service.stop_server)
        operations["connect_client"] = _wrap_op(self._service.connect_client)
        operations["disconnect_client"] = _wrap_op(self._service.disconnect_client)
        operations["make_call"] = _wrap_op(self._service.make_call)
        operations["send_data"] = _wrap_op(self._service.send_data)
        operations["close_stream"] = _wrap_op(self._service.close_stream)
        return operations

    def create_server(
        self,
        **kwargs: str | int | bool | list[str] | None,
    ) -> r[FlextGrpcEntities.Server]:
        """Create server entity with functional defaults."""
        host = str(kwargs.get("host", c.Grpc.GrpcNetwork.DEFAULT_HOST))
        port_raw = kwargs.get("port", c.Grpc.GrpcNetwork.DEFAULT_GRPC_PORT)
        workers_raw = kwargs.get("max_workers", c.Grpc.Service.DEFAULT_MAX_WORKERS)
        port = (
            int(port_raw)
            if isinstance(port_raw, str | int)
            else c.Grpc.GrpcNetwork.DEFAULT_GRPC_PORT
        )
        max_workers = (
            int(workers_raw)
            if isinstance(workers_raw, str | int)
            else c.Grpc.Service.DEFAULT_MAX_WORKERS
        )
        result = self.create_entity(
            "server",
            host=host,
            port=port,
            max_workers=max_workers,
        )
        # Result is guaranteed to be Server type by factory implementation
        if result.is_failure:
            return r.fail(result.error or "Server creation failed")
        # Type assertion based on entity_type="server" guarantee
        entity = result.value
        if not isinstance(entity, FlextGrpcEntities.Server):
            return r.fail(f"Invalid server entity type: {type(entity)}")
        return r.ok(entity)

    def create_client(
        self,
        **kwargs: str | int | bool | None,
    ) -> r[FlextGrpcEntities.Client]:
        """Create client with channel composition."""
        result = self.create_entity("client", **kwargs)
        if result.is_failure:
            return r.fail(result.error or "Client creation failed")
        entity = result.value
        if not isinstance(entity, FlextGrpcEntities.Client):
            return r.fail(f"Invalid client entity type: {type(entity)}")
        return r.ok(entity)

    def create_channel(
        self,
        **kwargs: str | int | bool | dict[str, t.GeneralValueType] | None,
    ) -> r[FlextGrpcEntities.Channel]:
        """Create channel entity with defaults."""
        defaults: dict[str, t.GeneralValueType] = {
            "target": f"{c.Grpc.GrpcNetwork.DEFAULT_HOST}:{c.Grpc.GrpcNetwork.DEFAULT_GRPC_PORT}",
            "options": {},
        }
        merged = defaults | dict(kwargs)
        result = self.create_entity("channel", **merged)
        if result.is_failure:
            return r.fail(result.error or "Channel creation failed")
        entity = result.value
        if not isinstance(entity, FlextGrpcEntities.Channel):
            return r.fail(f"Invalid channel entity type: {type(entity)}")
        return r.ok(entity)

    def create_service(
        self,
        **kwargs: str | list[str] | None,
    ) -> r[FlextGrpcEntities.Service]:
        """Create service entity with defaults."""
        name = kwargs.get("name")
        methods = kwargs.get("methods")
        service_name = (
            name if isinstance(name, str) and name.strip() else "DefaultService"
        )
        if isinstance(methods, str):
            service_methods: list[str] = [methods]
        elif isinstance(methods, list):
            service_methods = [method for method in methods if isinstance(method, str)]
            if not service_methods:
                service_methods = ["default_method"]
        else:
            service_methods = ["default_method"]
        result = self.create_entity(
            "service",
            name=service_name,
            methods=service_methods,
        )
        if result.is_failure:
            return r.fail(result.error or "Service creation failed")
        entity = result.value
        if not isinstance(entity, FlextGrpcEntities.Service):
            return r.fail(f"Invalid service entity type: {type(entity)}")
        return r.ok(entity)

    def create_stream(
        self,
        method_name: str = "DefaultMethod",
        stream_type: str = "unary",
        **kwargs: str | int | bool | None,
    ) -> r[FlextGrpcEntities.GrpcStream]:
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
        entity = result.value
        if not isinstance(entity, FlextGrpcEntities.GrpcStream):
            return r.fail(f"Invalid stream entity type: {type(entity)}")
        return r.ok(entity)

    # === DELEGATED OPERATIONS ===

    def start_server(
        self,
        server: FlextGrpcEntities.Server,
    ) -> r[FlextGrpcEntities.Server]:
        """Delegate server start.

        Args:
        server: gRPC server entity to start

        Returns:
        Started server entity

        """
        return self._service.start_server(server)

    def stop_server(
        self,
        server: FlextGrpcEntities.Server,
    ) -> r[FlextGrpcEntities.Server]:
        """Delegate server stop.

        Args:
        server: gRPC server entity to stop

        Returns:
        Stopped server entity

        """
        return self._service.stop_server(server)

    def connect_client(self, target: str) -> r[FlextGrpcEntities.Client]:
        """Delegate client connection.

        Args:
        target: Target address to connect to

        Returns:
        Connected client entity

        """
        return self._service.connect_client(target)

    def disconnect_client(
        self,
        client: FlextGrpcEntities.Client,
    ) -> r[FlextGrpcEntities.Client]:
        """Delegate client disconnection.

        Args:
        client: gRPC client entity to disconnect

        Returns:
        Disconnected client entity

        """
        return self._service.disconnect_client(client)

    def make_call(
        self,
        client: FlextGrpcEntities.Client,
        method: str,
        request: t.ConfigValue,
    ) -> r[dict[str, t.GeneralValueType]]:
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
        stream: FlextGrpcEntities.GrpcStream,
        data: t.ConfigValue,
    ) -> r[dict[str, t.GeneralValueType]]:
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
        stream: FlextGrpcEntities.GrpcStream,
    ) -> r[FlextGrpcEntities.GrpcStream]:
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
    ) -> r[
        dict[
            str,
            FlextGrpcEntities.Server
            | FlextGrpcEntities.Client
            | FlextGrpcEntities.Service
            | str,
        ]
    ]:
        """Complete setup using functional composition."""
        host = kwargs.get("host", c.Grpc.GrpcNetwork.DEFAULT_HOST)
        port = kwargs.get("port", c.Grpc.GrpcNetwork.DEFAULT_GRPC_PORT)
        service_name_raw = kwargs.get("service_name", "DefaultService")
        service_name = (
            str(service_name_raw) if service_name_raw is not None else "DefaultService"
        )
        methods_raw = kwargs.get("methods", ["DefaultMethod"])
        # Ensure methods is the correct type for create_service
        if isinstance(methods_raw, int):
            methods: str | list[str] | None = str(methods_raw)
        elif isinstance(methods_raw, (str, list)):
            methods = methods_raw
        else:
            methods = ["DefaultMethod"]
        target = f"{host}:{port}"

        # Advanced functional composition
        return (
            self
            .create_server(host=host, port=port)
            .flat_map(lambda s: self.create_client(target=target).map(lambda c: (s, c)))
            .flat_map(
                lambda pair: self.create_service(
                    name=service_name,
                    methods=methods,
                ).map(
                    lambda svc: {
                        "server": pair[0],
                        "client": pair[1],
                        "service": svc,
                        "target": target,
                    },
                ),
            )
        )


__all__ = ["FlextGrpc", "GenericOperationSpec", "GenericRequest", "GenericResponse"]
