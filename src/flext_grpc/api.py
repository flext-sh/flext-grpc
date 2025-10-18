"""FLEXT gRPC - Generic Unified Facade with Advanced Patterns.

Generic facade class using extensive Pydantic models, SOLID delegation,
functional composition, and advanced Python 3.13+ patterns for minimal code.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import Any, TypeVar
from uuid import uuid4

from flext_core import FlextResult, FlextService
from pydantic import BaseModel, Field, field_validator

from flext_grpc.config import FlextGrpcConfig
from flext_grpc.constants import FlextGrpcConstants
from flext_grpc.entities import FlextGrpcEntities
from flext_grpc.services import FlextGrpcServices
from flext_grpc.typings import FlextGrpcTypings

T = TypeVar("T", bound=BaseModel)


class GrpcOperationSpec(BaseModel):
    """Generic operation specification using Pydantic."""

    name: str = Field(min_length=1)
    entity_type: str
    method_name: str | None = None
    parameters: dict[str, Any] = Field(default_factory=dict)

    @field_validator("entity_type")
    @classmethod
    def validate_entity_type(cls, v: str) -> str:
        """Validate entity type against supported types."""
        supported = {"server", "client", "channel", "service", "stream"}
        if v not in supported:
            msg = f"Unsupported entity type: {v}"
            raise ValueError(msg)
        return v


class GrpcRequest[T: BaseModel](BaseModel):
    """Generic gRPC request model."""

    operation: GrpcOperationSpec
    entity: T | None = None
    data: Any = None

    def validate_request(self) -> FlextResult[None]:
        """Validate request using functional composition."""
        if not self.operation.name.strip():
            return FlextResult.fail("Operation name cannot be empty")

        if self.entity and hasattr(self.entity, "validate_business_rules"):
            return self.entity.validate_business_rules()  # type: ignore

        return FlextResult.ok(None)


class GrpcResponse[T: BaseModel](BaseModel):
    """Generic gRPC response model."""

    success: bool
    data: T | None = None
    error: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class FlextGrpc[T: BaseModel](FlextService[FlextGrpcConfig]):
    """Generic unified gRPC facade with advanced SOLID patterns and minimal code.

    Uses generic types, functional composition, Pydantic v2 models, and delegation
    to reduce bloat while maintaining full functionality with Python 3.13+ features.
    """

    def __init__(self, config: FlextGrpcConfig | None = None) -> None:
        """Initialize facade with FLEXT ecosystem integration."""
        super().__init__()
        self._service = FlextGrpcServices()
        self._config = config or FlextGrpcConfig()
        self._entity_factory = self._create_entity_factory()
        self._operation_dispatcher = self._create_operation_dispatcher()

    @property
    def config(self) -> FlextGrpcConfig:
        """Get facade configuration."""
        return self._config

    def execute(self) -> FlextResult[FlextGrpcConfig]:
        """Execute main facade operation."""
        return FlextResult.ok(self._config)

    # === ADVANCED GENERIC FACTORIES ===

    def _create_entity_factory(self) -> dict[str, type[BaseModel]]:
        """Create generic entity factory mapping."""
        return {
            "server": FlextGrpcEntities.Server,
            "client": FlextGrpcEntities.Client,
            "channel": FlextGrpcEntities.Channel,
            "service": FlextGrpcEntities.Service,
            "stream": FlextGrpcEntities.GrpcStream,
        }

    def _create_operation_dispatcher(self) -> dict[str, callable]:
        """Create operation dispatcher mapping with delegation."""
        return {
            "create_server": self._service._create_server_entity,
            "create_client": self._service._create_client_entity,
            "create_channel": self._service._create_channel_entity,
            "create_service": self._service._create_service_entity,
            "create_stream": self._service._create_stream_entity,
            "start_server": self._service.start_server,
            "stop_server": self._service.stop_server,
            "connect_client": self._service.connect_client,
            "disconnect_client": self._service.disconnect_client,
            "make_call": self._service.make_call,
            "send_data": self._service.send_data,
            "close_stream": self._service.close_stream,
        }

    def create_entity(
        self,
        entity_type: str,
        **kwargs: Any,
    ) -> FlextResult[BaseModel]:
        """Generic entity creation with Pydantic validation."""
        if entity_type not in self._entity_factory:
            return FlextResult.fail(f"Unknown entity type: {entity_type}")

        try:
            entity_cls = self._entity_factory[entity_type]
            entity = entity_cls(id=str(uuid4()), **kwargs)

            # Delegate validation to entity
            if hasattr(entity, "validate_business_rules"):
                validation = entity.validate_business_rules()
                if validation.is_failure:
                    return validation

            return FlextResult.ok(entity)
        except Exception as e:
            return FlextResult.fail(f"Entity creation failed: {e}")

    # === DELEGATED CONVENIENCE METHODS ===

    def create_server(self, **kwargs: Any) -> FlextResult[FlextGrpcEntities.Server]:
        """Create server entity with defaults."""
        defaults = {
            "host": FlextGrpcConstants.GrpcNetwork.DEFAULT_HOST,
            "port": FlextGrpcConstants.GrpcNetwork.DEFAULT_GRPC_PORT,
            "max_workers": FlextGrpcConstants.Service.DEFAULT_MAX_WORKERS,
            "state": "stopped",
            "services": [],
        }
        return self.create_entity("server", **defaults | kwargs)  # type: ignore

    def create_client(self, **kwargs: Any) -> FlextResult[FlextGrpcEntities.Client]:
        """Create client with channel delegation."""
        target = kwargs.get(
            "target",
            f"{FlextGrpcConstants.GrpcNetwork.DEFAULT_HOST}:{FlextGrpcConstants.GrpcNetwork.DEFAULT_GRPC_PORT}",
        )
        options = kwargs.get("options") or {}

        # Delegate channel creation
        channel_result = self.create_channel(target=target, options=options)
        if channel_result.is_failure:
            return FlextResult.fail(channel_result.error)

        return self.create_entity(
            "client",
            channel=channel_result.unwrap(),
            options=options,
        )

    def create_channel(self, **kwargs: Any) -> FlextResult[FlextGrpcEntities.Channel]:
        """Create channel entity with defaults."""
        defaults = {
            "target": f"{FlextGrpcConstants.GrpcNetwork.DEFAULT_HOST}:{FlextGrpcConstants.GrpcNetwork.DEFAULT_GRPC_PORT}",
            "state": "idle",
            "options": {},
        }
        return self.create_entity("channel", **defaults | kwargs)  # type: ignore

    def create_service(self, **kwargs: Any) -> FlextResult[FlextGrpcEntities.Service]:
        """Create service entity with defaults."""
        defaults = {
            "name": "DefaultService",
            "methods": [],
        }
        return self.create_entity("service", **defaults | kwargs)  # type: ignore

    def create_stream(
        self,
        method_name: str = "DefaultMethod",
        stream_type: str = "unary",
        **kwargs: Any,
    ) -> FlextResult[FlextGrpcEntities.GrpcStream]:
        """Create stream with validation delegation."""
        if not method_name or not method_name.strip():
            return FlextResult.fail("Stream method name cannot be empty")

        if stream_type not in FlextGrpcConstants.Literals.STREAM_TYPES:
            return FlextResult.fail(f"Invalid stream type: {stream_type}")

        kwargs.update({"method_name": method_name, "stream_type": stream_type})
        return self.create_entity("stream", **kwargs)  # type: ignore

    # === GENERIC OPERATION EXECUTION ===

    def execute_operation(
        self,
        operation_spec: GrpcOperationSpec,
        **context: Any,
    ) -> FlextResult[GrpcResponse[Any]]:
        """Generic operation execution with functional composition."""
        if operation_spec.name not in self._operation_dispatcher:
            return FlextResult.fail(f"Unknown operation: {operation_spec.name}")

        try:
            # Delegate to service layer
            operation = self._operation_dispatcher[operation_spec.name]
            result = operation(**operation_spec.parameters, **context)

            # Wrap in response model
            if result.is_success:
                return FlextResult.ok(
                    GrpcResponse(
                        success=True,
                        data=result.unwrap(),
                        metadata={"operation": operation_spec.name},
                    )
                )
            return FlextResult.ok(
                GrpcResponse(
                    success=False,
                    error=result.error,
                    metadata={"operation": operation_spec.name},
                )
            )

        except Exception as e:
            return FlextResult.ok(
                GrpcResponse(
                    success=False,
                    error=str(e),
                    metadata={"operation": operation_spec.name},
                )
            )

    # === DELEGATED CONVENIENCE OPERATIONS ===

    def start_server(
        self, server: FlextGrpcEntities.Server
    ) -> FlextResult[FlextGrpcEntities.Server]:
        """Start server with delegation."""
        return self._service.start_server(server)

    def stop_server(
        self, server: FlextGrpcEntities.Server
    ) -> FlextResult[FlextGrpcEntities.Server]:
        """Stop server with delegation."""
        return self._service.stop_server(server)

    def connect_client(self, target: str) -> FlextResult[FlextGrpcEntities.Client]:
        """Connect client with delegation."""
        return self._service.connect_client(target)

    def disconnect_client(
        self, client: FlextGrpcEntities.Client
    ) -> FlextResult[FlextGrpcEntities.Client]:
        """Disconnect client with delegation."""
        return self._service.disconnect_client(client)

    def make_call(
        self, client: FlextGrpcEntities.Client, method: str, request: Any
    ) -> FlextResult[dict[str, Any]]:
        """Make call with delegation."""
        return self._service.make_call(client, method, request)

    def send_data(
        self, stream: FlextGrpcEntities.GrpcStream, data: Any
    ) -> FlextResult[dict[str, Any]]:
        """Send data with delegation."""
        return self._service.send_data(stream, data)

    def close_stream(
        self, stream: FlextGrpcEntities.GrpcStream
    ) -> FlextResult[FlextGrpcEntities.GrpcStream]:
        """Close stream with delegation."""
        return self._service.close_stream(stream)

    # === ADVANCED UTILITIES WITH DELEGATION ===

    def validate_target(self, target: str) -> bool:
        """Validate target with delegation."""
        return FlextGrpcTypings.GrpcValidation.validate_target(target)

    def parse_address(self, address: str) -> FlextResult[tuple[str, int]]:
        """Parse address with delegation."""
        try:
            return FlextResult.ok(FlextGrpcTypings.GrpcValidation.parse_target(address))
        except ValueError as e:
            return FlextResult.fail(str(e))

    # === FUNCTIONAL COMPOSITION UTILITIES ===

    def create_complete_setup(self, **kwargs: Any) -> FlextResult[dict[str, Any]]:
        """Complete setup using functional composition and delegation."""
        host = kwargs.get("host", FlextGrpcConstants.GrpcNetwork.DEFAULT_HOST)
        port = kwargs.get("port", FlextGrpcConstants.GrpcNetwork.DEFAULT_GRPC_PORT)
        service_name = kwargs.get("service_name", "DefaultService")
        methods = kwargs.get("methods", ["DefaultMethod"])
        target = f"{host}:{port}"

        # Functional composition with delegation
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


__all__ = ["FlextGrpc", "GrpcOperationSpec", "GrpcRequest", "GrpcResponse"]
