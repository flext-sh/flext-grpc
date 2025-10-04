"""FLEXT gRPC - Unified Facade for gRPC Operations.

Single unified facade class following FLEXT namespace pattern.
Provides all gRPC functionality through clean, integrated API.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import logging
import re
from uuid import uuid4

from flext_core import (
    FlextBus,
    FlextConstants,
    FlextContainer,
    FlextContext,
    FlextDispatcher,
    FlextLogger,
    FlextProcessors,
    FlextRegistry,
    FlextResult,
    FlextService,
    FlextTypes,
)

from flext_grpc.config import FlextGrpcConfig
from flext_grpc.constants import FlextGrpcConstants
from flext_grpc.entities import (
    FlextGrpcChannel,
    FlextGrpcClient,
    FlextGrpcServer,
    FlextGrpcService,
    FlextGrpcStream,
)
from flext_grpc.models import FlextGrpcModels
from flext_grpc.services import FlextGrpcService as FlextGrpcServiceImpl
from flext_grpc.typings import FlextGrpcTypes


class FlextGrpc(FlextService[FlextGrpcConfig]):
    """Unified gRPC facade providing all gRPC operations.

    Single entry point for all FLEXT gRPC functionality with complete
    flext-core integration. Follows FLEXT namespace pattern with nested
    helper classes for clean organization.

    Features:
    - Entity factory methods (create_server, create_client, etc.)
    - High-level operations (start_server, connect_client, etc.)
    - Complete flext-core ecosystem integration
    - Clean API with backward compatibility
    """

    def __init__(self, config: FlextGrpcConfig | None = None) -> None:
        """Initialize unified gRPC facade with complete FLEXT integration."""
        super().__init__()

        # Complete FLEXT ecosystem integration
        self._container = FlextContainer.get_global()
        self._context = FlextContext()
        self._bus = FlextBus()
        self._dispatcher = FlextDispatcher()
        self._processors = FlextProcessors()
        self._registry = FlextRegistry(dispatcher=self._dispatcher)
        self._logger: logging.Logger = FlextLogger(__name__) or logging.getLogger(
            __name__
        )

        # Core service implementation
        self._service = FlextGrpcServiceImpl()
        self._config = config or FlextGrpcConfig()

    @property
    def config(self) -> FlextGrpcConfig | None:
        """Get facade configuration."""
        return self._config

    def execute(self) -> FlextResult[FlextGrpcConfig]:
        """Execute main facade operation."""
        return FlextResult.ok(self._config)

    # === ENTITY FACTORY METHODS ===

    def create_server(
        self,
        host: str | FlextGrpcModels.ServerConfig = FlextConstants.Platform.DEFAULT_HOST,
        port: int = FlextGrpcConstants.DEFAULT_GRPC_PORT,
        max_workers: int = FlextGrpcConstants.DEFAULT_MAX_WORKERS,
    ) -> FlextResult[FlextGrpcServer]:
        """Create gRPC server entity."""
        try:
            if isinstance(host, FlextGrpcModels.ServerConfig):
                config = host
            else:
                config = FlextGrpcModels.ServerConfig(
                    host=host, port=port, max_workers=max_workers
                )

            server = FlextGrpcServer(
                id=str(uuid4()),
                host=config.host,
                port=config.port,
                max_workers=config.max_workers,
                state="stopped",
                services=[],
            )
            return FlextResult.ok(server)
        except Exception as e:
            return FlextResult.fail(f"Failed to create server: {e}")

    def create_client(
        self,
        target: str
        | FlextGrpcModels.ClientConfig = FlextConstants.Platform.DEFAULT_HOST
        + ":"
        + str(FlextGrpcConstants.DEFAULT_GRPC_PORT),
        options: FlextTypes.Dict | None = None,
    ) -> FlextResult[FlextGrpcClient]:
        """Create gRPC client entity."""
        try:
            if isinstance(target, FlextGrpcModels.ClientConfig):
                config = target
            else:
                config = FlextGrpcModels.ClientConfig(
                    target=target,
                    timeout=FlextGrpcConstants.DEFAULT_TIMEOUT,
                    retry_attempts=3,
                )

            channel = FlextGrpcChannel(
                id=str(uuid4()),
                target=config.target,
                state="idle",
                options=options or {},
            )

            client = FlextGrpcClient(
                id=str(uuid4()),
                channel=channel,
                options=options or {},
            )
            return FlextResult.ok(client)
        except Exception as e:
            return FlextResult.fail(f"Failed to create client: {e}")

    def create_channel(
        self,
        target: str
        | FlextGrpcModels.ChannelConfig = FlextConstants.Platform.DEFAULT_HOST
        + ":"
        + str(FlextGrpcConstants.DEFAULT_GRPC_PORT),
        options: FlextTypes.Dict | None = None,
    ) -> FlextResult[FlextGrpcChannel]:
        """Create gRPC channel entity."""
        try:
            if isinstance(target, FlextGrpcModels.ChannelConfig):
                config = target
            else:
                config = FlextGrpcModels.ChannelConfig(address=target, options=options)

            channel = FlextGrpcChannel(
                id=str(uuid4()),
                target=config.address,
                state="idle",
                options=config.options or {},
            )
            return FlextResult.ok(channel)
        except Exception as e:
            return FlextResult.fail(f"Failed to create channel: {e}")

    def create_service(
        self,
        name: str | FlextGrpcModels.ServiceDefinition = "DefaultService",
        methods: str | FlextTypes.StringList | None = None,
    ) -> FlextResult[FlextGrpcService]:
        """Create gRPC service entity."""
        try:
            if isinstance(name, FlextGrpcModels.ServiceDefinition):
                definition = name
            else:
                if isinstance(methods, str):
                    methods_list = [methods]
                elif methods is None:
                    methods_list = []
                else:
                    methods_list = methods

                definition = FlextGrpcModels.ServiceDefinition(
                    service_name=name, methods=methods_list
                )

            service = FlextGrpcService(
                id=str(uuid4()),
                name=definition.service_name,
                methods=definition.methods,
            )
            return FlextResult.ok(service)
        except Exception as e:
            return FlextResult.fail(f"Failed to create service: {e}")

    def create_stream(
        self,
        method_name: str | FlextGrpcModels.StreamInfo = "DefaultMethod",
        stream_type: FlextGrpcTypes.GrpcStreamType = "unary",
    ) -> FlextResult[FlextGrpcStream]:
        """Create gRPC stream entity."""
        try:
            if isinstance(method_name, FlextGrpcModels.StreamInfo):
                stream_info = method_name
            else:
                if not method_name or not method_name.strip():
                    return FlextResult.fail("Stream method name cannot be empty")

                valid_types = [
                    "unary",
                    "server_streaming",
                    "client_streaming",
                    "bidirectional",
                ]
                if stream_type not in valid_types:
                    return FlextResult.fail(f"Invalid stream type: {stream_type}")

                stream_info = FlextGrpcModels.StreamInfo(
                    stream_id=str(uuid4()),
                    stream_type=stream_type,
                    target=f"{FlextConstants.Platform.DEFAULT_HOST}:{FlextGrpcConstants.DEFAULT_GRPC_PORT}",
                )

            stream = FlextGrpcStream(
                id=stream_info.stream_id,
                method_name=method_name
                if isinstance(method_name, str)
                else "DefaultMethod",
                stream_type=stream_info.stream_type,
            )
            return FlextResult.ok(stream)
        except Exception as e:
            return FlextResult.fail(f"Failed to create stream: {e}")

    def create_config(
        self,
        server_config: FlextGrpcModels.ServerConfig | None = None,
        host: str = FlextConstants.Platform.DEFAULT_HOST,
        port: int = FlextGrpcConstants.DEFAULT_GRPC_PORT,
        max_workers: int = FlextGrpcConstants.DEFAULT_MAX_WORKERS,
        timeout: float = FlextConstants.Network.DEFAULT_TIMEOUT,
    ) -> FlextResult[FlextGrpcConfig]:
        """Create gRPC configuration."""
        try:
            if server_config is None:
                server_config = FlextGrpcModels.ServerConfig(
                    host=host, port=port, max_workers=max_workers, timeout=timeout
                )

            return FlextResult.ok(FlextGrpcConfig.from_server_config(server_config))
        except Exception as e:
            return FlextResult.fail(f"Failed to create config: {e}")

    # === HIGH-LEVEL OPERATIONS ===

    def start_server(self, server: FlextGrpcServer) -> FlextResult[FlextGrpcServer]:
        """Start gRPC server."""
        return self._service.start_server(server)

    def stop_server(self, server: FlextGrpcServer) -> FlextResult[FlextGrpcServer]:
        """Stop gRPC server."""
        return self._service.stop_server(server)

    def get_server_status(
        self, server: FlextGrpcServer
    ) -> FlextResult[FlextTypes.Dict]:
        """Get server status."""
        return self._service.get_server_status(server)

    def connect_client(self, target: str) -> FlextResult[FlextGrpcClient]:
        """Connect to gRPC server."""
        return self._service.connect_client(target)

    def disconnect_client(
        self, client: FlextGrpcClient
    ) -> FlextResult[FlextGrpcClient]:
        """Disconnect gRPC client."""
        return self._service.disconnect_client(client)

    def make_call(
        self, client: FlextGrpcClient, method: str, request: object
    ) -> FlextResult[FlextTypes.Dict]:
        """Make gRPC call."""
        return self._service.make_call(client, method, request)

    def get_client_status(
        self, client: FlextGrpcClient
    ) -> FlextResult[FlextTypes.Dict]:
        """Get client status."""
        return self._service.get_client_status(client)

    def create_stream_op(
        self, stream_type: str = "unary", **kwargs: object
    ) -> FlextResult[FlextGrpcStream]:
        """Create and setup gRPC stream."""
        return self._service.create_stream(stream_type=stream_type, **kwargs)

    def send_data(
        self, stream: FlextGrpcStream, data: object
    ) -> FlextResult[FlextTypes.Dict]:
        """Send data through stream."""
        return self._service.send_data(stream, data)

    def close_stream(self, stream: FlextGrpcStream) -> FlextResult[FlextGrpcStream]:
        """Close gRPC stream."""
        return self._service.close_stream(stream)

    # === UTILITY METHODS ===

    def validate_address(self, address: str | None) -> FlextResult[bool]:
        """Validate network address format."""
        try:
            if address is None or not address.strip():
                return FlextResult.fail("Address cannot be empty")

            target_is_valid = FlextGrpcTypes.GrpcValidation.validate_target(address)
            return FlextResult.ok(target_is_valid)
        except Exception as e:
            return FlextResult.fail(f"Address validation error: {e}")

    def parse_address(self, address: str) -> FlextResult[dict[str, str | int]]:
        """Parse network address into components."""
        try:
            if not address or ":" not in address:
                return FlextResult.fail("Address must be in host:port format")

            parts = address.split(":")
            if len(parts) != FlextGrpcConstants.ADDRESS_PARTS_COUNT:
                return FlextResult.fail("Address must be in host:port format")

            host, port_str = parts
            if not host.strip():
                return FlextResult.fail("Invalid host format")

            try:
                port = int(port_str)
                if port < 1 or port > FlextGrpcConstants.MAX_PORT_NUMBER:
                    return FlextResult.fail("Port must be between 1 and 65535")
            except ValueError:
                return FlextResult.fail("Port must be a number")

            return FlextResult.ok({"host": host, "port": port})
        except Exception as e:
            return FlextResult.fail(f"Address parsing error: {e}")

    def validate_host(self, host: str) -> bool:
        """Validate host address format."""
        if not host or not host.strip():
            return False
        pattern = r"^[a-zA-Z0-9.-]+$"
        return bool(re.match(pattern, host.strip()))

    def validate_port(self, port: int) -> bool:
        """Validate port number range."""
        return FlextGrpcConstants.MIN_PORT <= port <= FlextGrpcConstants.MAX_PORT

    # === SETUP METHODS ===

    def create_complete_setup(
        self,
        host: str = FlextConstants.Platform.DEFAULT_HOST,
        port: int = FlextGrpcConstants.DEFAULT_GRPC_PORT,
        service_name: str = "DefaultService",
        methods: FlextTypes.StringList | None = None,
    ) -> FlextResult[FlextTypes.Dict]:
        """Create complete gRPC setup."""
        try:
            if methods is None:
                methods = ["DefaultMethod"]

            # Create components
            server_result = self.create_server(host=host, port=port)
            if server_result.is_failure:
                return FlextResult.fail(
                    f"Server creation failed: {server_result.error}"
                )

            target = f"{host}:{port}"
            client_result = self.create_client(target=target)
            if client_result.is_failure:
                return FlextResult.fail(
                    f"Client creation failed: {client_result.error}"
                )

            service_result = self.create_service(name=service_name, methods=methods)
            if service_result.is_failure:
                return FlextResult.fail(
                    f"Service creation failed: {service_result.error}"
                )

            return FlextResult.ok({
                "server": server_result.unwrap(),
                "client": client_result.unwrap(),
                "service": service_result.unwrap(),
                "target": target,
            })
        except Exception as e:
            return FlextResult.fail(f"Complete setup creation failed: {e}")


__all__ = [
    # Main facade
    "FlextGrpc",
]
