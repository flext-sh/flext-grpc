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
        **kwargs: object,
    ) -> r[object]:
        """Generic entity creation with Pydantic validation and delegation."""
        # Use match/case for cleaner entity type handling (Python 3.10+)
        entity_factories = self._get_entity_factories()

        factory = entity_factories.get(entity_type)
        if not factory:
            return r.fail(f"Unknown entity type: {entity_type}")

        # Call factory and handle result
        result = factory(**kwargs)
        if not result.is_success:
            return r.fail(f"Failed to create entity: {result.error}")

        entity = result.value

        # Delegate validation to entity if available
        if hasattr(entity, "validate_business_rules"):
            validate_method = getattr(entity, "validate_business_rules")
            if callable(validate_method):
                validation_result = validate_method()
            # Type narrowing: check if validation_result is a FlextResult
            if isinstance(validation_result, r) and not validation_result.is_success:
                return r.fail(
                    f"Entity validation failed: {validation_result.error}",
                )

        return r.ok(entity)

    def _get_entity_factories(
        self,
    ) -> dict[str, Callable[..., r[object]]]:
        """Get entity factories for dynamic dispatch."""
        # Dynamic dispatch pattern: callables return specific Result types
        # but dict requires common base type r[object]
        factories = {
            "server": FlextGrpcUtilities.create_server_entity,
            "client": FlextGrpcUtilities.create_client_entity,
            "channel": FlextGrpcUtilities.create_channel_entity,
            "service": FlextGrpcUtilities.create_service_entity,
            "stream": FlextGrpcUtilities.create_stream_entity,
        }
        return cast("dict[str, Callable[..., r[object]]]", factories)

    def execute_operation(
        self,
        request: FlextGrpcModels.Domain.OperationExecutionRequest,
    ) -> r[FlextGrpcSettings]:
        """Execute operation with validation, timeout, retry, and monitoring (Service protocol)."""
        operations = self._get_operations()

        operation = operations.get(request.operation_name)
        if not operation:
            return r.fail(f"Unknown operation: {request.operation_name}")

        # Execute operation with delegation
        result = operation(**request.arguments, **request.keyword_arguments)

        # Return config on success, fail on error
        return result.map(lambda _data: self.grpc_config).lash(
            lambda error_msg: r.fail(error_msg or "Unknown error"),
        )

    def _get_operations(self) -> dict[str, Callable[..., r[object]]]:
        """Get operations for dynamic dispatch."""
        # Dynamic dispatch pattern: methods return specific Result types
        operations = {
            "start_server": self._service.start_server,
            "stop_server": self._service.stop_server,
            "connect_client": self._service.connect_client,
            "disconnect_client": self._service.disconnect_client,
            "make_call": self._service.make_call,
            "send_data": self._service.send_data,
            "close_stream": self._service.close_stream,
        }
        return cast("dict[str, Callable[..., r[object]]]", operations)

    def create_server(
        self,
        **kwargs: str | int | bool | list[str] | None,
    ) -> r[FlextGrpcEntities.Server]:
        """Create server entity with functional defaults."""
        defaults = {
            "host": c.Grpc.GrpcNetwork.DEFAULT_HOST,
            "port": c.Grpc.GrpcNetwork.DEFAULT_GRPC_PORT,
            "max_workers": c.Grpc.Service.DEFAULT_MAX_WORKERS,
        }
        result = self.create_entity("server", **defaults | kwargs)
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
        **kwargs: str | int | bool | dict[str, object] | None,
    ) -> r[FlextGrpcEntities.Channel]:
        """Create channel entity with defaults."""
        defaults = {
            "target": f"{c.Grpc.GrpcNetwork.DEFAULT_HOST}:{c.Grpc.GrpcNetwork.DEFAULT_GRPC_PORT}",
            "options": {},
        }
        result = self.create_entity("channel", **defaults | kwargs)
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
        defaults = {"name": "DefaultService", "methods": ["default_method"]}
        result = self.create_entity("service", **defaults | kwargs)
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
    ) -> r[dict[str, object]]:
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
    ) -> r[dict[str, object]]:
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
    ) -> r[dict[str, object]]:
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
