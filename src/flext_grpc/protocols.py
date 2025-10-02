"""gRPC protocols for FLEXT ecosystem."""

from typing import Protocol, runtime_checkable

from flext_core import FlextProtocols, FlextResult


class FlextGrpcProtocols(FlextProtocols):
    """gRPC protocols extending FlextProtocols with gRPC-specific interfaces.

    This class provides protocol definitions for gRPC server management,
    client communication, streaming operations, and service orchestration.
    """

    @runtime_checkable
    class ServerProtocol(FlextProtocols.Domain.Service, Protocol):
        """Protocol for gRPC server management operations."""

        def start_server(
            self, host: str, port: int, services: list[object] | None = None
        ) -> FlextResult[object]:
            """Start gRPC server.

            Args:
                host: Server host address
                port: Server port number
                services: List of gRPC services to register

            Returns:
                FlextResult[object]: Server instance or error

            """

        def stop_server(self, *, grace_period: float = 30.0) -> FlextResult[bool]:
            """Stop gRPC server.

            Args:
                grace_period: Graceful shutdown timeout in seconds

            Returns:
                FlextResult[bool]: Stop success status

            """

        def add_service(self, service: object, server: object) -> FlextResult[bool]:
            """Add gRPC service to server.

            Args:
                service: gRPC service instance
                server: gRPC server instance

            Returns:
                FlextResult[bool]: Service registration success status

            """

        def get_server_status(self) -> FlextResult[dict[str, object]]:
            """Get gRPC server status information.

            Returns:
                FlextResult[dict[str, object]]: Server status or error

            """

        def configure_port(
            self, server: object, host: str, port: int, *, secure: bool = False
        ) -> FlextResult[int]:
            """Configure server port binding.

            Args:
                server: gRPC server instance
                host: Server host address
                port: Server port number
                secure: Use secure connection

            Returns:
                FlextResult[int]: Actual bound port or error

            """

    @runtime_checkable
    class ClientProtocol(FlextProtocols.Domain.Service, Protocol):
        """Protocol for gRPC client communication operations."""

        def connect_client(
            self, target: str, *, timeout: float = 30.0
        ) -> FlextResult[object]:
            """Connect gRPC client to server.

            Args:
                target: Server target address
                timeout: Connection timeout in seconds

            Returns:
                FlextResult[object]: Channel instance or error

            """

        def disconnect_client(self, channel: object) -> FlextResult[bool]:
            """Disconnect gRPC client.

            Args:
                channel: gRPC channel instance

            Returns:
                FlextResult[bool]: Disconnect success status

            """

        def make_call(
            self,
            channel: object,
            method: str,
            request: object,
            *,
            timeout: float = 30.0,
        ) -> FlextResult[object]:
            """Make gRPC method call.

            Args:
                channel: gRPC channel instance
                method: Method name to call
                request: Request message
                timeout: Call timeout in seconds

            Returns:
                FlextResult[object]: Response message or error

            """

        def get_client_status(self, channel: object) -> FlextResult[dict[str, object]]:
            """Get gRPC client status information.

            Args:
                channel: gRPC channel instance

            Returns:
                FlextResult[dict[str, object]]: Client status or error

            """

        def validate_connection(self, channel: object) -> FlextResult[bool]:
            """Validate gRPC client connection.

            Args:
                channel: gRPC channel instance

            Returns:
                FlextResult[bool]: Connection validity status

            """

    @runtime_checkable
    class StreamingProtocol(FlextProtocols.Domain.Service, Protocol):
        """Protocol for gRPC streaming operations."""

        def create_stream(
            self, stream_type: str, channel: object, method: str
        ) -> FlextResult[object]:
            """Create gRPC stream.

            Args:
                stream_type: Type of stream (client, server, bidirectional)
                channel: gRPC channel instance
                method: Streaming method name

            Returns:
                FlextResult[object]: Stream instance or error

            """

        def send_data(self, stream: object, data: object) -> FlextResult[bool]:
            """Send data through gRPC stream.

            Args:
                stream: Stream instance
                data: Data to send

            Returns:
                FlextResult[bool]: Send success status

            """

        def close_stream(self, stream: object) -> FlextResult[bool]:
            """Close gRPC stream.

            Args:
                stream: Stream instance

            Returns:
                FlextResult[bool]: Close success status

            """

        def handle_client_streaming(
            self, stream: object, data_list: list[object]
        ) -> FlextResult[object]:
            """Handle client-side streaming.

            Args:
                stream: Client stream instance
                data_list: List of data to stream

            Returns:
                FlextResult[object]: Server response or error

            """

        def handle_server_streaming(
            self, stream: object, request: object
        ) -> FlextResult[list[object]]:
            """Handle server-side streaming.

            Args:
                stream: Server stream instance
                request: Client request

            Returns:
                FlextResult[list[object]]: Stream responses or error

            """

        def handle_bidirectional_streaming(
            self, stream: object
        ) -> FlextResult[dict[str, object]]:
            """Handle bidirectional streaming.

            Args:
                stream: Bidirectional stream instance

            Returns:
                FlextResult[dict[str, object]]: Stream result or error

            """

    @runtime_checkable
    class ServiceProtocol(FlextProtocols.Domain.Service, Protocol):
        """Protocol for gRPC service definition and management."""

        def create_service(
            self, service_name: str, methods: dict[str, object]
        ) -> FlextResult[object]:
            """Create gRPC service definition.

            Args:
                service_name: Name of the service
                methods: Dictionary of method implementations

            Returns:
                FlextResult[object]: Service instance or error

            """

        def register_service(
            self, service: object, server: object
        ) -> FlextResult[bool]:
            """Register gRPC service with server.

            Args:
                service: Service instance
                server: Server instance

            Returns:
                FlextResult[bool]: Registration success status

            """

        def validate_service(self, service: object) -> FlextResult[bool]:
            """Validate gRPC service definition.

            Args:
                service: Service instance to validate

            Returns:
                FlextResult[bool]: Validation success status

            """

        def get_service_methods(self, service: object) -> FlextResult[list[str]]:
            """Get list of service methods.

            Args:
                service: Service instance

            Returns:
                FlextResult[list[str]]: Method names or error

            """

    @runtime_checkable
    class ChannelProtocol(FlextProtocols.Domain.Service, Protocol):
        """Protocol for gRPC channel management operations."""

        def create_channel(
            self, target: str, options: dict[str, object] | None = None
        ) -> FlextResult[object]:
            """Create gRPC channel.

            Args:
                target: Server target address
                options: Channel options

            Returns:
                FlextResult[object]: Channel instance or error

            """

        def close_channel(self, channel: object) -> FlextResult[bool]:
            """Close gRPC channel.

            Args:
                channel: Channel instance

            Returns:
                FlextResult[bool]: Close success status

            """

        def get_channel_state(self, channel: object) -> FlextResult[str]:
            """Get gRPC channel connection state.

            Args:
                channel: Channel instance

            Returns:
                FlextResult[str]: Channel state or error

            """

        def wait_for_state_change(
            self, channel: object, last_state: str, *, timeout: float = 30.0
        ) -> FlextResult[bool]:
            """Wait for channel state change.

            Args:
                channel: Channel instance
                last_state: Previous known state
                timeout: Wait timeout in seconds

            Returns:
                FlextResult[bool]: State change success status

            """

    @runtime_checkable
    class MetricsProtocol(FlextProtocols.Domain.Service, Protocol):
        """Protocol for gRPC metrics collection and monitoring."""

        def collect_server_metrics(
            self, server: object
        ) -> FlextResult[dict[str, object]]:
            """Collect gRPC server metrics.

            Args:
                server: Server instance

            Returns:
                FlextResult[dict[str, object]]: Server metrics or error

            """

        def collect_client_metrics(
            self, channel: object
        ) -> FlextResult[dict[str, object]]:
            """Collect gRPC client metrics.

            Args:
                channel: Channel instance

            Returns:
                FlextResult[dict[str, object]]: Client metrics or error

            """

        def collect_stream_metrics(
            self, stream: object
        ) -> FlextResult[dict[str, object]]:
            """Collect gRPC stream metrics.

            Args:
                stream: Stream instance

            Returns:
                FlextResult[dict[str, object]]: Stream metrics or error

            """

        def start_metrics_collection(
            self, *, interval: float = 60.0
        ) -> FlextResult[bool]:
            """Start automatic metrics collection.

            Args:
                interval: Collection interval in seconds

            Returns:
                FlextResult[bool]: Start success status

            """

        def stop_metrics_collection(self) -> FlextResult[bool]:
            """Stop automatic metrics collection.

            Returns:
                FlextResult[bool]: Stop success status

            """

        def get_global_metrics(self) -> FlextResult[dict[str, object]]:
            """Get global gRPC metrics.

            Returns:
                FlextResult[dict[str, object]]: Global metrics or error

            """

    @runtime_checkable
    class ConfigurationProtocol(FlextProtocols.Domain.Service, Protocol):
        """Protocol for gRPC configuration management."""

        def create_server_config(
            self, host: str, port: int, options: dict[str, object] | None = None
        ) -> FlextResult[dict[str, object]]:
            """Create gRPC server configuration.

            Args:
                host: Server host
                port: Server port
                options: Additional options

            Returns:
                FlextResult[dict[str, object]]: Server config or error

            """

        def create_client_config(
            self, target: str, options: dict[str, object] | None = None
        ) -> FlextResult[dict[str, object]]:
            """Create gRPC client configuration.

            Args:
                target: Server target
                options: Additional options

            Returns:
                FlextResult[dict[str, object]]: Client config or error

            """

        def validate_config(self) -> FlextResult[None]:
            """Validate gRPC configuration.

            Returns:
                FlextResult[None]: Success or error

            """

        def parse_address(self, address: str) -> FlextResult[tuple[str, int]]:
            """Parse gRPC address string.

            Args:
                address: Address string to parse

            Returns:
                FlextResult[tuple[str, int]]: Host and port tuple or error

            """

        def validate_address(self, address: str) -> FlextResult[bool]:
            """Validate gRPC address format.

            Args:
                address: Address to validate

            Returns:
                FlextResult[bool]: Validation success status

            """

    # Convenience aliases for easier downstream usage
    GrpcServerProtocol = ServerProtocol
    GrpcClientProtocol = ClientProtocol
    GrpcStreamProtocol = StreamingProtocol
    GrpcServiceProtocol = ServiceProtocol
    GrpcChannelProtocol = ChannelProtocol
    GrpcMetricsProtocol = MetricsProtocol
    GrpcConfigProtocol = ConfigurationProtocol


__all__ = [
    "FlextGrpcProtocols",
]
