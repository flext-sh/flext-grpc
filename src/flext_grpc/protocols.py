"""gRPC protocols for FLEXT ecosystem."""

from typing import Protocol, runtime_checkable

from flext_core import FlextProtocols, FlextResult, FlextTypes


class FlextGrpcProtocols(FlextProtocols):
    """Unified gRPC protocols extending FLEXT foundation protocols.

    This class extends FlextProtocols with gRPC-specific protocols while maintaining
    all foundation protocols from flext-core.

    Architecture:
        - EXTENDS: FlextProtocols with all foundation protocols
        - ADDS: gRPC-specific protocols in Grpc namespace
        - MAINTAINS: Zero breaking changes through inheritance pattern

    Usage:
        from flext_grpc.protocols import FlextGrpcProtocols

        # Foundation access (inherited)
        FlextGrpcProtocols.Foundation.ResultProtocol

        # gRPC-specific access
        FlextGrpcProtocols.Grpc.ServerProtocol
    """

    # =========================================================================
    # GRPC-SPECIFIC PROTOCOLS (Extending foundation protocols)
    # =========================================================================
    # Domain-specific protocols for gRPC server management, client communication,
    # streaming operations, service definitions, channel management, metrics, and configuration.

    # =========================================================================
    # GRPC-SPECIFIC PROTOCOLS
    # =========================================================================
    # Domain-specific protocols for gRPC server management, client communication,
    # streaming operations, service definitions, channel management, metrics, and configuration.

    class Grpc:
        """gRPC domain-specific protocols.

        Provides protocols for gRPC server management, client communication,
        streaming operations, service definitions, channel management,
        metrics collection, and configuration.
        """

        @runtime_checkable
        class ServerProtocol(FlextProtocols.Domain.Service, Protocol):
            """Protocol for gRPC server management operations."""

            def start_server(
                self, host: str, port: int, services: FlextTypes.List | None = None
            ) -> FlextResult[object]:
                """Start gRPC server."""
                ...

            def stop_server(self, *, grace_period: float = 30.0) -> FlextResult[bool]:
                """Stop gRPC server."""
                ...

            def add_service(self, service: object, server: object) -> FlextResult[bool]:
                """Add gRPC service to server."""
                ...

            def get_server_status(self) -> FlextResult[FlextTypes.Dict]:
                """Get gRPC server status information."""
                ...

            def configure_port(
                self, server: object, host: str, port: int, *, secure: bool = False
            ) -> FlextResult[int]:
                """Configure server port binding."""
                ...

        @runtime_checkable
        class ClientProtocol(FlextProtocols.Domain.Service, Protocol):
            """Protocol for gRPC client communication operations."""

            def connect_client(
                self, target: str, *, timeout: float = 30.0
            ) -> FlextResult[object]:
                """Connect gRPC client to server."""
                ...

            def disconnect_client(self, channel: object) -> FlextResult[bool]:
                """Disconnect gRPC client."""
                ...

            def make_call(
                self,
                channel: object,
                method: str,
                request: object,
                *,
                timeout: float = 30.0,
            ) -> FlextResult[object]:
                """Make gRPC method call."""
                ...

            def get_client_status(
                self, channel: object
            ) -> FlextResult[FlextTypes.Dict]:
                """Get gRPC client status information."""
                ...

            def validate_connection(self, channel: object) -> FlextResult[bool]:
                """Validate gRPC client connection."""
                ...

        @runtime_checkable
        class StreamingProtocol(FlextProtocols.Domain.Service, Protocol):
            """Protocol for gRPC streaming operations."""

            def create_stream(
                self, stream_type: str, channel: object, method: str
            ) -> FlextResult[object]:
                """Create gRPC stream."""
                ...

            def send_data(self, stream: object, data: object) -> FlextResult[bool]:
                """Send data through gRPC stream."""
                ...

            def close_stream(self, stream: object) -> FlextResult[bool]:
                """Close gRPC stream."""
                ...

            def handle_client_streaming(
                self, stream: object, data_list: FlextTypes.List
            ) -> FlextResult[object]:
                """Handle client-side streaming."""
                ...

            def handle_server_streaming(
                self, stream: object, request: object
            ) -> FlextResult[FlextTypes.List]:
                """Handle server-side streaming."""
                ...

            def handle_bidirectional_streaming(
                self, stream: object
            ) -> FlextResult[FlextTypes.Dict]:
                """Handle bidirectional streaming."""
                ...

        @runtime_checkable
        class ServiceProtocol(FlextProtocols.Domain.Service, Protocol):
            """Protocol for gRPC service definition and management."""

            def create_service(
                self, service_name: str, methods: FlextTypes.Dict
            ) -> FlextResult[object]:
                """Create gRPC service definition."""
                ...

            def register_service(
                self, service: object, server: object
            ) -> FlextResult[bool]:
                """Register gRPC service with server."""
                ...

            def validate_service(self, service: object) -> FlextResult[bool]:
                """Validate gRPC service definition."""
                ...

            def get_service_methods(
                self, service: object
            ) -> FlextResult[FlextTypes.StringList]:
                """Get list of service methods."""
                ...

        @runtime_checkable
        class ChannelProtocol(FlextProtocols.Domain.Service, Protocol):
            """Protocol for gRPC channel management operations."""

            def create_channel(
                self, target: str, options: FlextTypes.Dict | None = None
            ) -> FlextResult[object]:
                """Create gRPC channel."""
                ...

            def close_channel(self, channel: object) -> FlextResult[bool]:
                """Close gRPC channel."""
                ...

            def get_channel_state(self, channel: object) -> FlextResult[str]:
                """Get gRPC channel connection state."""
                ...

            def wait_for_state_change(
                self, channel: object, last_state: str, *, timeout: float = 30.0
            ) -> FlextResult[bool]:
                """Wait for channel state change."""
                ...

        @runtime_checkable
        class MetricsProtocol(FlextProtocols.Domain.Service, Protocol):
            """Protocol for gRPC metrics collection and monitoring."""

            def collect_server_metrics(
                self, server: object
            ) -> FlextResult[FlextTypes.Dict]:
                """Collect gRPC server metrics."""
                ...

            def collect_client_metrics(
                self, channel: object
            ) -> FlextResult[FlextTypes.Dict]:
                """Collect gRPC client metrics."""
                ...

            def collect_stream_metrics(
                self, stream: object
            ) -> FlextResult[FlextTypes.Dict]:
                """Collect gRPC stream metrics."""
                ...

            def start_metrics_collection(
                self, *, interval: float = 60.0
            ) -> FlextResult[bool]:
                """Start automatic metrics collection."""
                ...

            def stop_metrics_collection(self) -> FlextResult[bool]:
                """Stop automatic metrics collection."""
                ...

            def get_global_metrics(self) -> FlextResult[FlextTypes.Dict]:
                """Get global gRPC metrics."""
                ...

        @runtime_checkable
        class ConfigurationProtocol(FlextProtocols.Domain.Service, Protocol):
            """Protocol for gRPC configuration management."""

            def create_server_config(
                self, host: str, port: int, options: FlextTypes.Dict | None = None
            ) -> FlextResult[FlextTypes.Dict]:
                """Create gRPC server configuration."""
                ...

            def create_client_config(
                self, target: str, options: FlextTypes.Dict | None = None
            ) -> FlextResult[FlextTypes.Dict]:
                """Create gRPC client configuration."""
                ...

            def validate_config(self) -> FlextResult[None]:
                """Validate gRPC configuration."""
                ...

            def parse_address(self, address: str) -> FlextResult[tuple[str, int]]:
                """Parse gRPC address string."""
                ...

            def validate_address(self, address: str) -> FlextResult[bool]:
                """Validate gRPC address format."""
                ...


__all__ = [
    "FlextGrpcProtocols",
]
