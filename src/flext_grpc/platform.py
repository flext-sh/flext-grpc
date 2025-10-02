"""FLEXT gRPC Platform - Unified Platform Facade.

High-level facade for gRPC operations providing convenience methods
for common gRPC workflows following Clean Architecture and Domain-Driven
Design principles.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import cast

from flext_core import (
    FlextConstants,
    FlextContainer,
    FlextLogger,
    FlextResult,
    FlextService,
)
from flext_grpc.api import (
    create_client,
    create_server,
    create_service,
    create_stream,
    validate_address,
)
from flext_grpc.constants import FlextGrpcConstants
from flext_grpc.entities import (
    FlextGrpcClient,
    FlextGrpcServer,
    FlextGrpcStream,
)
from flext_grpc.services import FlextGrpcService


class FlextGrpcPlatform(FlextService[dict[str, object]]):
    """Unified gRPC platform facade providing high-level operations.

    This class serves as the main entry point for gRPC operations,
    providing convenience methods for common workflows while maintaining
    Clean Architecture principles and proper separation of concerns.

    Following Flext patterns:
    - Single class with nested classes for different operation areas
    - Proper error handling with FlextResult
    - Integration with FlextContainer and FlextLogger
    - Service-oriented architecture
    """

    def __init__(self, config: dict[str, object] | None = None) -> None:
        """Initialize the gRPC platform facade.

        Args:
            config: Optional configuration dictionary

        """
        super().__init__()
        self._container = FlextContainer.get_global()
        self._logger = FlextLogger(__name__)
        self._service_processor: FlextGrpcService = FlextGrpcService()
        self._config = config or {}

        self._server_service: FlextGrpcService = FlextGrpcService()
        self._client_service: FlextGrpcService = FlextGrpcService()
        self._stream_service: FlextGrpcService = FlextGrpcService()

    @property
    def config(self) -> dict[str, object]:
        """Get the platform configuration."""
        return self._config

    @property
    def container(self) -> FlextContainer:
        """Get the dependency injection container."""
        return self._container

    @property
    def service(self) -> FlextGrpcService:
        """Get the main service processor."""
        return self._service_processor

    def execute(self) -> FlextResult[dict[str, object]]:
        """Execute the main platform operation.

        Returns:
            FlextResult containing platform status and capabilities

        """
        return FlextResult[dict[str, object]].ok({
            "status": "operational",
            "platform": "flext-grpc",
            "capabilities": [
                "server_management",
                "client_management",
                "stream_management",
                "service_discovery",
                "health_monitoring",
                "configuration_management",
            ],
        })

    def start_server(self, server: FlextGrpcServer) -> FlextResult[FlextGrpcServer]:
        """Start a gRPC server.

        Args:
            server: Server entity to start

        Returns:
            FlextResult containing the started server

        """
        return self.ServerManagement.start_server(server)

    def stop_server(self, server: FlextGrpcServer) -> FlextResult[FlextGrpcServer]:
        """Stop a gRPC server.

        Args:
            server: Server entity to stop

        Returns:
            FlextResult containing the stopped server

        """
        return self.ServerManagement.stop_server(server)

    def get_server_status(
        self, server: FlextGrpcServer
    ) -> FlextResult[dict[str, object]]:
        """Get server status.

        Args:
            server: Server entity to check

        Returns:
            FlextResult containing server status

        """
        return self.ServerManagement.get_server_status(server)

    def connect_client(self, client: FlextGrpcClient) -> FlextResult[FlextGrpcClient]:
        """Connect a gRPC client.

        Args:
            client: Client entity to connect

        Returns:
            FlextResult containing the connected client

        """
        return self.ClientManagement.connect_client(client)

    def get_client_status(
        self, client: FlextGrpcClient
    ) -> FlextResult[dict[str, object]]:
        """Get client status.

        Args:
            client: Client entity to check

        Returns:
            FlextResult containing client status

        """
        service_processor = FlextGrpcService()
        result = service_processor.execute("status", client)
        return (
            FlextResult[dict[str, object]].ok(
                cast("dict[str, object]", result.unwrap())
            )
            if result.is_success
            else FlextResult[dict[str, object]].fail(result.error or "Unknown error")
        )

    def make_call(
        self, client: FlextGrpcClient, method_name: str, **kwargs: object
    ) -> FlextResult[dict[str, object]]:
        """Make a gRPC call.

        Args:
            client: Client entity
            method_name: Name of the method to call
            **kwargs: Method arguments

        Returns:
            FlextResult containing the call result

        """
        return self.ClientManagement.call_method(client, method_name, **kwargs)

    def create_stream(
        self, stream_type: str = "unary", method_name: str = "DefaultMethod"
    ) -> FlextResult[FlextGrpcStream]:
        """Create a stream.

        Args:
            stream_type: Type of stream (unary, streaming, bidirectional)
            method_name: Name of the gRPC method

        Returns:
            FlextResult containing the created stream

        """
        return self.StreamManagement.create_stream_setup(stream_type, method_name)

    def server_operation(
        self, operation: str, server: FlextGrpcServer, **kwargs: object
    ) -> FlextResult[FlextGrpcServer | dict[str, object]]:
        """Perform a server operation.

        Args:
            operation: Operation to perform
            server: Server entity
            **kwargs: Operation arguments

        Returns:
            FlextResult containing the operation result

        """
        service_processor = FlextGrpcService()
        result = service_processor.execute(operation, server, **kwargs)
        return cast("FlextResult[FlextGrpcServer | dict[str, object]]", result)

    def create_server_setup(
        self,
        host: str = FlextConstants.Platform.DEFAULT_HOST,
        port: int = FlextGrpcConstants.DEFAULT_GRPC_PORT,
        max_workers: int = FlextGrpcConstants.DEFAULT_MAX_WORKERS,
        service_name: str = "default-service",
        methods: list[str] | None = None,
    ) -> FlextResult[FlextGrpcServer]:
        """Create a complete server setup with service.

        Args:
            host: Server host address
            port: Server port number
            max_workers: Maximum worker threads
            service_name: Name of the service
            methods: List of service methods

        Returns:
            FlextResult containing the created server

        """
        try:
            # Create server
            server = create_server(host=host, port=port, max_workers=max_workers)

            # Create service if methods provided
            if methods:
                service = create_service(
                    name=service_name,
                    methods=methods,
                )
                # Add service to server
                add_result = self._service_processor.execute(
                    "add_service", server, service
                )
                if add_result.is_failure:
                    self._logger.warning(
                        f"Failed to add service to server: {add_result.error}"
                    )

            return FlextResult[FlextGrpcServer].ok(server)
        except Exception as e:
            error_msg = f"Failed to create server setup: {e}"
            self._logger.exception(error_msg)
            return FlextResult[FlextGrpcServer].fail(error_msg)

    def create_client_setup(
        self,
        target: str = f"{FlextConstants.Platform.DEFAULT_HOST}:{FlextGrpcConstants.DEFAULT_GRPC_PORT}",
    ) -> FlextResult[FlextGrpcClient]:
        """Create a complete client setup with channel.

        Args:
            target: gRPC target address
            timeout: Connection timeout

        Returns:
            FlextResult containing the created client

        """
        try:
            # Validate address first
            validation_result = validate_address(target)
            if validation_result.is_failure:
                return FlextResult[FlextGrpcClient].fail(
                    f"Invalid target address: {validation_result.error}"
                )

            # Create client
            client = create_client(target=target)
            return FlextResult[FlextGrpcClient].ok(client)
        except Exception as e:
            error_msg = f"Failed to create client setup: {e}"
            self._logger.exception(error_msg)
            return FlextResult[FlextGrpcClient].fail(error_msg)

    def create_complete_setup(
        self,
        server_host: str = FlextConstants.Platform.DEFAULT_HOST,
        server_port: int = FlextGrpcConstants.DEFAULT_GRPC_PORT,
        server_max_workers: int = FlextGrpcConstants.DEFAULT_MAX_WORKERS,
        service_name: str = "default-service",
        methods: list[str] | None = None,
    ) -> FlextResult[dict[str, FlextGrpcServer | FlextGrpcClient]]:
        """Create a complete gRPC setup with server, client, and service.

        Args:
            server_host: Server host address
            server_port: Server port number
            server_max_workers: Maximum worker threads
            service_name: Name of the service
            methods: List of service methods

        Returns:
            FlextResult containing the complete setup

        """
        try:
            # Create server setup
            server_result = self.create_server_setup(
                host=server_host,
                port=server_port,
                max_workers=server_max_workers,
                service_name=service_name,
                methods=methods,
            )
            if server_result.is_failure:
                return FlextResult[dict[str, FlextGrpcServer | FlextGrpcClient]].fail(
                    f"Failed to create server setup: {server_result.error}"
                )

            # Create client setup
            target = f"{server_host}:{server_port}"
            client_result = self.create_client_setup(target=target)
            if client_result.is_failure:
                return FlextResult[dict[str, FlextGrpcServer | FlextGrpcClient]].fail(
                    f"Failed to create client setup: {client_result.error}"
                )

            # Service creation is handled internally by the server setup

            setup: dict[str, FlextGrpcServer | FlextGrpcClient] = {
                "server": server_result.value,
                "client": client_result.value,
            }

            return FlextResult[dict[str, FlextGrpcServer | FlextGrpcClient]].ok(setup)
        except Exception as e:
            error_msg = f"Failed to create complete setup: {e}"
            self._logger.exception(error_msg)
            return FlextResult[dict[str, FlextGrpcServer | FlextGrpcClient]].fail(
                error_msg
            )

    class ServerManagement:
        """Nested class for server management operations."""

        @staticmethod
        def start_server(server: FlextGrpcServer) -> FlextResult[FlextGrpcServer]:
            """Start a gRPC server.

            Args:
                server: Server entity to start

            Returns:
                FlextResult containing the started server

            """
            service_processor = FlextGrpcService()
            result = service_processor.execute("start", server)
            return (
                FlextResult[FlextGrpcServer].ok(
                    cast("FlextGrpcServer", result.unwrap())
                )
                if result.is_success
                else FlextResult[FlextGrpcServer].fail(result.error or "Unknown error")
            )

        @staticmethod
        def stop_server(server: FlextGrpcServer) -> FlextResult[FlextGrpcServer]:
            """Stop a gRPC server.

            Args:
                server: Server entity to stop

            Returns:
                FlextResult containing the stopped server

            """
            service_processor = FlextGrpcService()
            result = service_processor.execute("stop", server)
            return (
                FlextResult[FlextGrpcServer].ok(
                    cast("FlextGrpcServer", result.unwrap())
                )
                if result.is_success
                else FlextResult[FlextGrpcServer].fail(result.error or "Unknown error")
            )

        @staticmethod
        def get_server_status(
            server: FlextGrpcServer,
        ) -> FlextResult[dict[str, object]]:
            """Get server status.

            Args:
                server: Server entity to check

            Returns:
                FlextResult containing server status

            """
            service_processor = FlextGrpcService()
            result = service_processor.execute("status", server)
            return (
                FlextResult[dict[str, object]].ok(
                    cast("dict[str, object]", result.unwrap())
                )
                if result.is_success
                else FlextResult[dict[str, object]].fail(
                    result.error or "Unknown error"
                )
            )

    class ClientManagement:
        """Nested class for client management operations."""

        @staticmethod
        def connect_client(client: FlextGrpcClient) -> FlextResult[FlextGrpcClient]:
            """Connect a gRPC client.

            Args:
                client: Client entity to connect

            Returns:
                FlextResult containing the connected client

            """
            service_processor = FlextGrpcService()
            result = service_processor.execute("connect", client)
            return (
                FlextResult[FlextGrpcClient].ok(
                    cast("FlextGrpcClient", result.unwrap())
                )
                if result.is_success
                else FlextResult[FlextGrpcClient].fail(result.error or "Unknown error")
            )

        @staticmethod
        def disconnect_client(client: FlextGrpcClient) -> FlextResult[FlextGrpcClient]:
            """Disconnect a gRPC client.

            Args:
                client: Client entity to disconnect

            Returns:
                FlextResult containing the disconnected client

            """
            service_processor = FlextGrpcService()
            result = service_processor.execute("disconnect", client)
            return (
                FlextResult[FlextGrpcClient].ok(
                    cast("FlextGrpcClient", result.unwrap())
                )
                if result.is_success
                else FlextResult[FlextGrpcClient].fail(result.error or "Unknown error")
            )

        @staticmethod
        def call_method(
            client: FlextGrpcClient, method_name: str, **kwargs: object
        ) -> FlextResult[dict[str, object]]:
            """Call a method on a gRPC client.

            Args:
                client: Client entity
                method_name: Name of the method to call
                **kwargs: Method arguments

            Returns:
                FlextResult containing the method result

            """
            service_processor = FlextGrpcService()
            result = service_processor.execute("call", client, method_name, **kwargs)
            return (
                FlextResult[dict[str, object]].ok(
                    cast("dict[str, object]", result.unwrap())
                )
                if result.is_success
                else FlextResult[dict[str, object]].fail(
                    result.error or "Unknown error"
                )
            )

    class StreamManagement:
        """Nested class for stream management operations."""

        @staticmethod
        def create_stream_setup(
            stream_type: str = "unary",
            method_name: str = "DefaultMethod",
        ) -> FlextResult[FlextGrpcStream]:
            """Create a stream setup.

            Args:
                stream_type: Type of stream (unary, streaming, bidirectional)
                method_name: Name of the gRPC method

            Returns:
                FlextResult containing the created stream

            """
            stream = create_stream(method_name=method_name, stream_type=stream_type)
            return FlextResult[FlextGrpcStream].ok(stream)

        @staticmethod
        def send_data(
            stream: FlextGrpcStream, data: dict[str, object]
        ) -> FlextResult[FlextGrpcStream]:
            """Send data through a stream.

            Args:
                stream: Stream entity
                data: Data to send

            Returns:
                FlextResult containing the stream

            """
            service_processor = FlextGrpcService()
            result = service_processor.execute("send", stream, data)
            return (
                FlextResult[FlextGrpcStream].ok(
                    cast("FlextGrpcStream", result.unwrap())
                )
                if result.is_success
                else FlextResult[FlextGrpcStream].fail(result.error or "Unknown error")
            )

        @staticmethod
        def close_stream(stream: FlextGrpcStream) -> FlextResult[FlextGrpcStream]:
            """Close a stream.

            Args:
                stream: Stream entity to close

            Returns:
                FlextResult containing the closed stream

            """
            service_processor = FlextGrpcService()
            result = service_processor.execute("close", stream)
            return (
                FlextResult[FlextGrpcStream].ok(
                    cast("FlextGrpcStream", result.unwrap())
                )
                if result.is_success
                else FlextResult[FlextGrpcStream].fail(result.error or "Unknown error")
            )
