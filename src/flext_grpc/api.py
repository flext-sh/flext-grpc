"""FLEXT gRPC - Generic Unified Facade with Patterns.

Generic facade using extensive Pydantic models, SOLID delegation,
functional composition, and Python 3.13+ patterns for minimal code.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Callable
from functools import partial
from typing import Any, TypeVar, cast
from uuid import uuid4

from flext_core import FlextModels, FlextResult, FlextService
from pydantic import BaseModel, Field, computed_field, field_validator

from flext_grpc.config import FlextGrpcConfig
from flext_grpc.constants import FlextGrpcConstants
from flext_grpc.entities import FlextGrpcEntities
from flext_grpc.services import FlextGrpcServices
from flext_grpc.typings import FlextGrpcTypes
from flext_grpc.utilities import FlextGrpcUtilities

T = TypeVar("T", bound=BaseModel)


class GenericOperationSpec(BaseModel):
    """Generic operation specification using Pydantic."""

    name: str = Field(min_length=1)
    entity_type: str = Field(pattern=r"^[a-z_]+$")
    method_name: str | None = None
    parameters: dict[str, object] = Field(default_factory=dict)

    @field_validator("entity_type")
    @classmethod
    def validate_entity_type(cls, v: str) -> str:
        """Validate entity type against supported types."""
        supported = frozenset({"server", "client", "channel", "service", "stream"})
        if v not in supported:
            msg = f"Unsupported entity type: {v}. Supported: {supported}"
            raise ValueError(msg)
        return v


class GenericRequest[T: BaseModel](BaseModel):
    """Generic request model with validation."""

    operation: GenericOperationSpec
    entity: T | None = None
    data: object = None

    @computed_field
    def is_valid(self) -> bool:
        """Check if request is valid."""
        return bool(self.operation.name.strip())


class GenericResponse[T: BaseModel](BaseModel):
    """Generic response model with metadata."""

    success: bool
    data: T | None = None
    error: str | None = None
    metadata: dict[str, object] = Field(default_factory=dict)

    @computed_field
    def has_error(self) -> bool:
        """Check if response has error."""
        return not self.success or self.error is not None


class FlextGrpc[T: BaseModel](FlextService[FlextGrpcConfig]):
    """Generic unified gRPC facade with SOLID patterns and minimal code.

    Uses generic types, functional composition, Pydantic v2 models, and delegation
    to reduce bloat while maintaining full functionality with Python 3.13+ features.
    """

    def __init__(self, config: FlextGrpcConfig | None = None) -> None:
        """Initialize facade with FLEXT ecosystem integration."""
        super().__init__()
        self._service = FlextGrpcServices()
        self._config = config or FlextGrpcConfig()

    @property
    def grpc_config(self) -> FlextGrpcConfig:
        """Get gRPC-specific configuration."""
        return self._config

    def execute(self) -> FlextResult[FlextGrpcConfig]:
        """Execute main facade operation."""
        return FlextResult.ok(self._config)

    def create_entity(
        self,
        entity_type: str,
        **kwargs: object,
    ) -> FlextResult[Any]:
        """Generic entity creation with Pydantic validation and delegation."""
        # Use match/case for cleaner entity type handling (Python 3.10+)
        entity_factories = self._get_entity_factories()

        factory = entity_factories.get(entity_type)
        if not factory:
            return FlextResult.fail(f"Unknown entity type: {entity_type}")

        # Call factory and handle result
        result = factory(id=str(uuid4()), **kwargs)
        if not result.is_success:
            return FlextResult.fail(f"Failed to create entity: {result.error}")

        entity = result.value

        # Delegate validation to entity if available
        if hasattr(entity, "validate_business_rules") and callable(
            getattr(entity, "validate_business_rules")
        ):
            validation_result = cast(
                "FlextResult[object]", getattr(entity, "validate_business_rules")()
            )
            if hasattr(validation_result, "map") and not validation_result.is_success:
                return FlextResult.fail(
                    f"Entity validation failed: {validation_result.error}"
                )

        return FlextResult.ok(entity)

    def _get_entity_factories(self) -> dict[str, Callable[..., FlextResult[Any]]]:
        """Get entity factories using partial application for clean delegation."""
        return {
            "server": cast(
                "Callable[..., FlextResult[Any]]",
                partial(FlextGrpcUtilities.create_server_entity),
            ),
            "client": cast(
                "Callable[..., FlextResult[Any]]",
                partial(FlextGrpcUtilities.create_client_entity),
            ),
            "channel": cast(
                "Callable[..., FlextResult[Any]]",
                partial(FlextGrpcUtilities.create_channel_entity),
            ),
            "service": cast(
                "Callable[..., FlextResult[Any]]",
                partial(FlextGrpcUtilities.create_service_entity),
            ),
            "stream": cast(
                "Callable[..., FlextResult[Any]]",
                partial(FlextGrpcUtilities.create_stream_entity),
            ),
        }

    def execute_operation(
        self,
        request: FlextModels.OperationExecutionRequest,
    ) -> FlextResult[FlextGrpcConfig]:
        """Execute operation with validation, timeout, retry, and monitoring (Domain.Service protocol)."""
        operations = self._get_operations()

        operation = operations.get(request.operation_name)
        if not operation:
            return FlextResult.fail(f"Unknown operation: {request.operation_name}")

        # Execute operation with delegation
        result = operation(**request.arguments, **request.keyword_arguments)

        # Return config on success, fail on error
        return result.map(lambda _data: self._config).lash(
            lambda error_msg: FlextResult.fail(error_msg or "Unknown error")
        )

    def _get_operations(self) -> dict[str, Callable[..., FlextResult[Any]]]:
        """Get operations using delegation to service layer."""
        return {
            "start_server": self._service.start_server,
            "stop_server": self._service.stop_server,
            "connect_client": self._service.connect_client,
            "disconnect_client": self._service.disconnect_client,
            "make_call": self._service.make_call,
            "send_data": self._service.send_data,
            "close_stream": self._service.close_stream,
        }

    def create_server(
        self, **kwargs: str | int | bool | list[str] | None
    ) -> FlextResult[FlextGrpcEntities.Server]:
        """Create server entity with functional defaults."""
        defaults = {
            "host": FlextGrpcConstants.GrpcNetwork.DEFAULT_HOST,
            "port": FlextGrpcConstants.GrpcNetwork.DEFAULT_GRPC_PORT,
            "max_workers": FlextGrpcConstants.Service.DEFAULT_MAX_WORKERS,
            "state": "stopped",
            "services": [],
        }
        return self.create_entity("server", **defaults | kwargs)

    def create_client(
        self, **kwargs: str | int | bool | None
    ) -> FlextResult[FlextGrpcEntities.Client]:
        """Create client with channel composition."""
        # Functional composition for client creation
        return self.create_channel(**kwargs).flat_map(
            lambda channel: cast(
                "FlextResult[FlextGrpcEntities.Client]",
                self.create_entity("client", channel=channel, **kwargs),
            )
        )

    def create_channel(
        self, **kwargs: str | int | bool | dict[str, object] | None
    ) -> FlextResult[FlextGrpcEntities.Channel]:
        """Create channel entity with defaults."""
        defaults = {
            "target": f"{FlextGrpcConstants.GrpcNetwork.DEFAULT_HOST}:{FlextGrpcConstants.GrpcNetwork.DEFAULT_GRPC_PORT}",
            "state": "idle",
            "options": {},
        }
        return self.create_entity("channel", **defaults | kwargs)

    def create_service(
        self, **kwargs: str | list[str] | None
    ) -> FlextResult[FlextGrpcEntities.Service]:
        """Create service entity with defaults."""
        defaults = {"name": "DefaultService", "methods": []}
        return self.create_entity("service", **defaults | kwargs)

    def create_stream(
        self,
        method_name: str = "DefaultMethod",
        stream_type: str = "unary",
        **kwargs: str | int | bool | None,
    ) -> FlextResult[FlextGrpcEntities.GrpcStream]:
        """Create stream with validation."""
        if not method_name.strip():
            return FlextResult.fail("Stream method name cannot be empty")

        if stream_type not in FlextGrpcConstants.Literals.STREAM_TYPES:
            return FlextResult.fail(f"Invalid stream type: {stream_type}")

        return self.create_entity(
            "stream", method_name=method_name, stream_type=stream_type, **kwargs
        )

    # === DELEGATED OPERATIONS ===

    def start_server(
        self, server: FlextGrpcEntities.Server
    ) -> FlextResult[FlextGrpcEntities.Server]:
        """Delegate server start.

        Args:
        server: gRPC server entity to start

        Returns:
        Started server entity

        """
        return self._service.start_server(server)

    def stop_server(
        self, server: FlextGrpcEntities.Server
    ) -> FlextResult[FlextGrpcEntities.Server]:
        """Delegate server stop.

        Args:
        server: gRPC server entity to stop

        Returns:
        Stopped server entity

        """
        return self._service.stop_server(server)

    def connect_client(self, target: str) -> FlextResult[FlextGrpcEntities.Client]:
        """Delegate client connection.

        Args:
        target: Target address to connect to

        Returns:
        Connected client entity

        """
        return self._service.connect_client(target)

    def disconnect_client(
        self, client: FlextGrpcEntities.Client
    ) -> FlextResult[FlextGrpcEntities.Client]:
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
        request: FlextGrpcTypes.ConfigValue,
    ) -> FlextResult[dict[str, object]]:
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
        self, stream: FlextGrpcEntities.GrpcStream, data: FlextGrpcTypes.ConfigValue
    ) -> FlextResult[dict[str, object]]:
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
        self, stream: FlextGrpcEntities.GrpcStream
    ) -> FlextResult[FlextGrpcEntities.GrpcStream]:
        """Delegate stream closing.

        Args:
        stream: gRPC stream entity to close

        Returns:
        Closed stream entity

        """
        return self._service.close_stream(stream)

    def create_complete_setup(
        self, **kwargs: str | int | list[str] | None
    ) -> FlextResult[dict[str, object]]:
        """Complete setup using functional composition."""
        host = kwargs.get("host", FlextGrpcConstants.GrpcNetwork.DEFAULT_HOST)
        port = kwargs.get("port", FlextGrpcConstants.GrpcNetwork.DEFAULT_GRPC_PORT)
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
            self.create_server(host=host, port=port)
            .flat_map(lambda s: self.create_client(target=target).map(lambda c: (s, c)))
            .flat_map(
                lambda pair: self.create_service(
                    name=service_name, methods=methods
                ).map(
                    lambda svc: {
                        "server": pair[0],
                        "client": pair[1],
                        "service": svc,
                        "target": target,
                    }
                )
            )
        )


__all__ = ["FlextGrpc", "GenericOperationSpec", "GenericRequest", "GenericResponse"]
