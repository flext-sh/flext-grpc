"""FLEXT gRPC - Unified Facade for gRPC Operations.

Single unified facade class following FLEXT namespace pattern.
Provides all gRPC functionality through clean, integrated API.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import re
from uuid import uuid4

from flext_core import FlextCore

from flext_grpc.config import FlextGrpcConfig
from flext_grpc.constants import FlextGrpcConstants
from flext_grpc.entities import FlextGrpcEntities
from flext_grpc.services import FlextGrpcServices
from flext_grpc.typings import FlextGrpcTypings


class FlextGrpc(FlextCore.Service[FlextGrpcConfig]):
    """Unified gRPC facade providing all gRPC operations.

    Single entry point for all FLEXT gRPC functionality with complete
    flext-core integration. Provides direct access to all gRPC operations
    without unnecessary wrappers or aliases.

    Features:
    - Direct entity factory methods
    - High-level operations (start_server, connect_client, etc.)
    - Complete flext-core ecosystem integration
    - Clean API with minimal duplication
    """

    def __init__(self, config: FlextGrpcConfig | None = None) -> None:
        """Initialize unified gRPC facade with complete FLEXT integration."""
        super().__init__()

        # Complete FLEXT ecosystem integration
        self._container = FlextCore.Container.get_global()
        self._context = FlextCore.Context()
        self._bus = FlextCore.Bus()
        self._dispatcher = FlextCore.Dispatcher()
        self._processors = FlextCore.Processors()
        self._registry = FlextCore.Registry(dispatcher=self._dispatcher)
        # Logger is provided by parent class FlextCore.Service via property
        # No need to set it explicitly

        # Core service and configuration
        self._service = FlextGrpcServices()
        self._config = config or FlextGrpcConfig()

    @property
    def config(self) -> FlextGrpcConfig:
        """Get facade configuration."""
        return self._config

    def execute(self) -> FlextCore.Result[FlextGrpcConfig]:
        """Execute main facade operation."""
        return FlextCore.Result[FlextGrpcConfig].ok(self.config)

    # === ENTITY FACTORY METHODS ===

    def create_server(
        self,
        host: str = FlextGrpcConstants.Network.DEFAULT_HOST,
        port: int = FlextGrpcConstants.Network.DEFAULT_GRPC_PORT,
        max_workers: int = FlextGrpcConstants.Service.DEFAULT_MAX_WORKERS,
    ) -> FlextCore.Result[FlextGrpcEntities.Server]:
        """Create gRPC server entity."""
        try:
            server = FlextGrpcEntities.Server(
                id=str(uuid4()),
                host=host,
                port=port,
                max_workers=max_workers,
                state="stopped",
                services=[],
            )
            return FlextCore.Result[FlextGrpcEntities.Server].ok(server)
        except Exception as e:
            return FlextCore.Result[FlextGrpcEntities.Server].fail(
                f"Failed to create server: {e}"
            )

    def create_client(
        self,
        target: str = FlextGrpcConstants.Network.DEFAULT_HOST
        + ":"
        + str(FlextGrpcConstants.Network.DEFAULT_GRPC_PORT),
        options: FlextGrpcTypings.Dict | None = None,
    ) -> FlextCore.Result[FlextGrpcEntities.Client]:
        """Create gRPC client entity."""
        try:
            channel = FlextGrpcEntities.Channel(
                id=str(uuid4()),
                target=target,
                state="idle",
                options=options or {},
            )

            client = FlextGrpcEntities.Client(
                id=str(uuid4()),
                channel=channel,
                options=options or {},
            )
            return FlextCore.Result[FlextGrpcEntities.Client].ok(client)
        except Exception as e:
            return FlextCore.Result[FlextGrpcEntities.Client].fail(
                f"Failed to create client: {e}"
            )

    def create_channel(
        self,
        target: str = FlextGrpcConstants.Network.DEFAULT_HOST
        + ":"
        + str(FlextGrpcConstants.Network.DEFAULT_GRPC_PORT),
        options: FlextGrpcTypings.Dict | None = None,
    ) -> FlextCore.Result[FlextGrpcEntities.Channel]:
        """Create gRPC channel entity."""
        try:
            channel = FlextGrpcEntities.Channel(
                id=str(uuid4()),
                target=target,
                state="idle",
                options=options or {},
            )
            return FlextCore.Result[FlextGrpcEntities.Channel].ok(channel)
        except Exception as e:
            return FlextCore.Result[FlextGrpcEntities.Channel].fail(
                f"Failed to create channel: {e}"
            )

    def create_service(
        self,
        name: str = "DefaultService",
        methods: FlextCore.Types.StringList | None = None,
    ) -> FlextCore.Result[FlextGrpcEntities.Service]:
        """Create gRPC service entity."""
        try:
            service = FlextGrpcEntities.Service(
                id=str(uuid4()),
                name=name,
                methods=methods or [],
            )
            return FlextCore.Result[FlextGrpcEntities.Service].ok(service)
        except Exception as e:
            return FlextCore.Result[FlextGrpcEntities.Service].fail(
                f"Failed to create service: {e}"
            )

    def create_stream(
        self,
        method_name: str = "DefaultMethod",
        stream_type: FlextGrpcTypings.GrpcStreamType = "unary",
    ) -> FlextCore.Result[FlextGrpcEntities.GrpcStream]:
        """Create gRPC stream entity."""
        try:
            if not method_name or not method_name.strip():
                return FlextCore.Result[FlextGrpcEntities.GrpcStream].fail(
                    "Stream method name cannot be empty"
                )

            valid_types = FlextGrpcConstants.Literals.STREAM_TYPES
            if stream_type not in valid_types:
                return FlextCore.Result[FlextGrpcEntities.GrpcStream].fail(
                    f"Invalid stream type: {stream_type}"
                )

            stream = FlextGrpcEntities.GrpcStream(
                id=str(uuid4()),
                method_name=method_name,
                stream_type=stream_type,
            )
            return FlextCore.Result[FlextGrpcEntities.GrpcStream].ok(stream)
        except Exception as e:
            return FlextCore.Result[FlextGrpcEntities.GrpcStream].fail(
                f"Failed to create stream: {e}"
            )

    def create_config(
        self,
        host: str = FlextGrpcConstants.Network.DEFAULT_HOST,
        port: int = FlextGrpcConstants.Network.DEFAULT_GRPC_PORT,
        max_workers: int = FlextGrpcConstants.Service.DEFAULT_MAX_WORKERS,
        timeout: float = FlextGrpcConstants.Network.DEFAULT_TIMEOUT,
    ) -> FlextCore.Result[FlextGrpcConfig]:
        """Create gRPC configuration."""
        try:
            config_data = {
                "host": host,
                "port": port,
                "max_workers": max_workers,
                "timeout": timeout,
            }
            config = FlextGrpcConfig.model_validate(config_data)
            return FlextCore.Result[FlextGrpcConfig].ok(config)
        except Exception as e:
            return FlextCore.Result[FlextGrpcConfig].fail(
                f"Failed to create config: {e}"
            )

    # === HIGH-LEVEL OPERATIONS ===

    def start_server(
        self, server: FlextGrpcEntities.Server
    ) -> FlextCore.Result[FlextGrpcEntities.Server]:
        """Start gRPC server."""
        return self._service.start_server(server)

    def stop_server(
        self, server: FlextGrpcEntities.Server
    ) -> FlextCore.Result[FlextGrpcEntities.Server]:
        """Stop gRPC server."""
        return self._service.stop_server(server)

    def get_server_status(
        self, server: FlextGrpcEntities.Server
    ) -> FlextCore.Result[FlextCore.Types.Dict]:
        """Get server status."""
        return self._service.get_server_status(server)

    def connect_client(self, target: str) -> FlextCore.Result[FlextGrpcEntities.Client]:
        """Connect to gRPC server."""
        return self._service.connect_client(target)

    def disconnect_client(
        self, client: FlextGrpcEntities.Client
    ) -> FlextCore.Result[FlextGrpcEntities.Client]:
        """Disconnect gRPC client."""
        return self._service.disconnect_client(client)

    def make_call(
        self, client: FlextGrpcEntities.Client, method: str, request: object
    ) -> FlextCore.Result[FlextCore.Types.Dict]:
        """Make gRPC call."""
        return self._service.make_call(client, method, request)

    def get_client_status(
        self, client: FlextGrpcEntities.Client
    ) -> FlextCore.Result[FlextCore.Types.Dict]:
        """Get client status."""
        return self._service.get_client_status(client)

    def create_stream_op(
        self, stream_type: str = "unary", **kwargs: object
    ) -> FlextCore.Result[FlextGrpcEntities.GrpcStream]:
        """Create and setup gRPC stream."""
        return self._service.create_stream(stream_type=stream_type, **kwargs)

    def send_data(
        self, stream: FlextGrpcEntities.GrpcStream, data: object
    ) -> FlextCore.Result[FlextCore.Types.Dict]:
        """Send data through stream."""
        return self._service.send_data(stream, data)

    def close_stream(
        self, stream: FlextGrpcEntities.GrpcStream
    ) -> FlextCore.Result[FlextGrpcEntities.GrpcStream]:
        """Close gRPC stream."""
        return self._service.close_stream(stream)

    # === UTILITY METHODS ===

    def validate_address(self, address: str | None) -> FlextCore.Result[bool]:
        """Validate network address format."""
        try:
            if address is None or not address.strip():
                return FlextCore.Result[bool].fail("Address cannot be empty")

            target_is_valid = FlextGrpcTypings.GrpcValidation.validate_target(address)
            return FlextCore.Result[bool].ok(target_is_valid)
        except Exception as e:
            return FlextCore.Result[bool].fail(f"Address validation error: {e}")

    def parse_address(self, address: str) -> FlextCore.Result[dict[str, str | int]]:
        """Parse network address into components."""
        try:
            if not address or ":" not in address:
                return FlextCore.Result[dict[str, str | int]].fail(
                    "Address must be in host:port format"
                )

            parts = address.split(":")
            if len(parts) != FlextGrpcConstants.Validation.ADDRESS_PARTS_COUNT:
                return FlextCore.Result[dict[str, str | int]].fail(
                    "Address must be in host:port format"
                )

            host, port_str = parts
            if not host.strip():
                return FlextCore.Result[dict[str, str | int]].fail(
                    "Invalid host format"
                )

            try:
                port = int(port_str)
                if port < 1 or port > FlextGrpcConstants.Validation.MAX_PORT_NUMBER:
                    return FlextCore.Result[dict[str, str | int]].fail(
                        "Port must be between 1 and 65535"
                    )
            except ValueError:
                return FlextCore.Result[dict[str, str | int]].fail(
                    "Port must be a number"
                )

            return FlextCore.Result[dict[str, str | int]].ok({
                "host": host,
                "port": port,
            })
        except Exception as e:
            return FlextCore.Result[dict[str, str | int]].fail(
                f"Address parsing error: {e}"
            )

    def validate_host(self, host: str) -> bool:
        """Validate host address format."""
        if not host or not host.strip():
            return False
        pattern = r"^[a-zA-Z0-9.-]+$"
        return bool(re.match(pattern, host.strip()))

    def validate_port(self, port: int) -> bool:
        """Validate port number range."""
        return (
            FlextGrpcConstants.Network.MIN_PORT
            <= port
            <= FlextGrpcConstants.Network.MAX_PORT
        )

    def validate_target(self, target: str) -> bool:
        """Validate a gRPC target string in the form host:port."""
        return FlextGrpcTypings.GrpcValidation.validate_target(target)

    # === SETUP METHODS ===

    def create_complete_setup(
        self,
        host: str = FlextGrpcConstants.Network.DEFAULT_HOST,
        port: int = FlextGrpcConstants.Network.DEFAULT_GRPC_PORT,
        service_name: str = "DefaultService",
        methods: FlextGrpcTypings.StringList | None = None,
    ) -> FlextCore.Result[FlextCore.Types.Dict]:
        """Create complete gRPC setup."""
        try:
            if methods is None:
                methods = ["DefaultMethod"]

            # Create components
            server_result = self.create_server(host=host, port=port)
            if server_result.is_failure:
                return FlextCore.Result[FlextGrpcEntities.Server].fail(
                    f"Server creation failed: {server_result.error}"
                )

            target = f"{host}:{port}"
            client_result = self.create_client(target=target)
            if client_result.is_failure:
                return FlextCore.Result[FlextGrpcEntities.Client].fail(
                    f"Client creation failed: {client_result.error}"
                )

            service_result = self.create_service(name=service_name, methods=methods)
            if service_result.is_failure:
                return FlextCore.Result[FlextGrpcEntities.Service].fail(
                    f"Service creation failed: {service_result.error}"
                )

            return FlextCore.Result[FlextCore.Types.Dict].ok({
                "server": server_result.unwrap(),
                "client": client_result.unwrap(),
                "service": service_result.unwrap(),
                "target": target,
            })
        except Exception as e:
            return FlextCore.Result[FlextCore.Types.Dict].fail(
                f"Complete setup creation failed: {e}"
            )


__all__ = [
    # Main facade
    "FlextGrpc",
]
