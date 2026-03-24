"""FLEXT gRPC - Generic Unified Facade with Patterns.

Generic facade using extensive Pydantic models, SOLID delegation,
functional composition, and Python 3.13+ patterns for minimal code.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Sequence

from typing import TypedDict

from flext_core import r

from flext_grpc import FlextGrpcServices, FlextGrpcSettings, ServicePayload, c, m, t, u


class FlextGrpc:
    """Generic unified gRPC facade with SOLID patterns and minimal code.

    Uses generic types, functional composition, Pydantic v2 models, and delegation
    to reduce bloat while maintaining full functionality with Python 3.13+ features.
    """

    def __init__(self, config: FlextGrpcSettings | None = None) -> None:
        """Initialize facade with FLEXT ecosystem integration."""
        super().__init__()
        self._service = FlextGrpcServices()
        self._grpc_config = (
            config if config is not None else FlextGrpcSettings.model_validate({})
        )
        object.__setattr__(self, "_config", self._grpc_config)

    @property
    def grpc_config(self) -> FlextGrpcSettings:
        """Get gRPC-specific configuration."""
        return self._grpc_config

    def close_stream(self, stream: m.Grpc.GrpcStream) -> r[m.Grpc.GrpcStream]:
        """Delegate stream closing.

        Args:
        stream: gRPC stream entity to close

        Returns:
        Closed stream entity

        """
        return self._service.close_stream(stream)

    def connect_client(self, target: str) -> r[m.Grpc.Client]:
        """Delegate client connection.

        Args:
        target: Target address to connect to

        Returns:
        Connected client entity

        """
        return self._service.connect_client(target)

    def create_channel(
        self, target: str, options: t.GrpcOptions | None = None
    ) -> r[m.Grpc.Channel]:
        """Create typed channel entity from validated inputs."""
        return u.create_channel_entity(
            target=target,
            options={} if options is None else options,
        )

    def create_client(
        self, target: str, options: t.GrpcOptions | None = None
    ) -> r[m.Grpc.Client]:
        """Create typed client entity from validated inputs."""
        return u.create_client_entity(target=target, options=options)

    def create_complete_setup(
        self,
        host: str = c.Grpc.GrpcNetwork.DEFAULT_HOST,
        port: int = c.Grpc.GrpcNetwork.DEFAULT_GRPC_PORT,
        service_name: str = "DefaultService",
        methods: Sequence[str] | None = None,
    ) -> r[GrpcCompleteSetup]:
        """Complete setup using functional composition."""
        resolved_methods = ["HealthCheck"] if methods is None else methods
        target = f"{host}:{port}"
        return (
            self
            .create_server(host=host, port=port)
            .flat_map(lambda s: self.create_client(target=target).map(lambda c: (s, c)))
            .flat_map(
                lambda pair: self.create_service(
                    name=service_name,
                    methods=resolved_methods,
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

    def create_server(
        self,
        host: str = c.Grpc.GrpcNetwork.DEFAULT_HOST,
        port: int = c.Grpc.GrpcNetwork.DEFAULT_GRPC_PORT,
        max_workers: int = c.Grpc.Service.DEFAULT_MAX_WORKERS,
    ) -> r[m.Grpc.Server]:
        """Create typed server entity from validated inputs."""
        return u.create_server_entity(
            host=host,
            port=port,
            max_workers=max_workers,
        )

    def create_service(
        self, name: str, methods: Sequence[str] | None = None
    ) -> r[m.Grpc.Service]:
        """Create typed service entity from validated inputs."""
        return u.create_service_entity(
            name=name,
            methods=[] if methods is None else methods,
        )

    def create_stream(
        self, method_name: str = "DefaultMethod", stream_type: str = "unary"
    ) -> r[m.Grpc.GrpcStream]:
        """Create typed stream entity from validated inputs."""
        if not method_name.strip():
            return r[m.Grpc.GrpcStream].fail("Stream method name cannot be empty")
        if stream_type not in c.Grpc.STREAM_TYPES:
            return r[m.Grpc.GrpcStream].fail(f"Invalid stream type: {stream_type}")
        return u.create_stream_entity(method_name=method_name, stream_type=stream_type)

    def disconnect_client(self, client: m.Grpc.Client) -> r[m.Grpc.Client]:
        """Delegate client disconnection.

        Args:
        client: gRPC client entity to disconnect

        Returns:
        Disconnected client entity

        """
        return self._service.disconnect_client(client)

    def execute(self) -> r[FlextGrpcSettings]:
        """Execute main facade operation."""
        return r[FlextGrpcSettings].ok(self.grpc_config)

    def execute_operation(
        self, request: m.Grpc.OperationExecutionRequest
    ) -> r[FlextGrpcSettings]:
        """Execute operation with validation, timeout, retry, and monitoring (Service protocol)."""
        kwargs = request.keyword_arguments
        match request.operation_name:
            case "connect_client":
                target = kwargs.get("target")
                if not isinstance(target, str):
                    return r[FlextGrpcSettings].fail(
                        "connect_client requires string target"
                    )
                result = self._service.connect_client(target)
            case _:
                return r[FlextGrpcSettings].fail(
                    f"Unknown operation: {request.operation_name}"
                )
        if result.is_failure:
            return r[FlextGrpcSettings].fail(result.error or "Unknown error")
        return r[FlextGrpcSettings].ok(self.grpc_config)

    def make_call(
        self, client: m.Grpc.Client, method: str, request: t.ConfigValue
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

    def parse_address(self, address: str) -> r[tuple[str, int]]:
        """Parse gRPC address string."""
        if not t.Grpc.GrpcValidation.validate_target(address):
            return r[tuple[str, int]].fail(f"Invalid address: {address}")
        return r[tuple[str, int]].ok(t.Grpc.GrpcValidation.parse_target(address))

    def send_data(
        self, stream: m.Grpc.GrpcStream, data: t.ConfigValue
    ) -> r[ServicePayload]:
        """Delegate data sending.

        Args:
        stream: gRPC stream entity
        data: Message data (gRPC protocol message - dynamic type)

        Returns:
        Response data dictionary

        Note: Uses t.NormalizedValue for gRPC message compatibility

        """
        return self._service.send_data(stream, data)

    def start_server(self, server: m.Grpc.Server) -> r[m.Grpc.Server]:
        """Delegate server start.

        Args:
        server: gRPC server entity to start

        Returns:
        Started server entity

        """
        return self._service.start_server(server)

    def stop_server(self, server: m.Grpc.Server) -> r[m.Grpc.Server]:
        """Delegate server stop.

        Args:
        server: gRPC server entity to stop

        Returns:
        Stopped server entity

        """
        return self._service.stop_server(server)

    def validate_target(self, target: str) -> bool:
        """Validate gRPC target string."""
        return t.Grpc.GrpcValidation.validate_target(target)


__all__ = ["FlextGrpc"]


class GrpcCompleteSetup(TypedDict):
    server: m.Grpc.Server
    client: m.Grpc.Client
    service: m.Grpc.Service
    target: str
