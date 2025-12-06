"""gRPC protocols for FLEXT ecosystem."""

from typing import Protocol, runtime_checkable

from flext_core import FlextResult, p

from flext_grpc.constants import FlextGrpcConstants


class FlextGrpcProtocols(p):
    """Unified gRPC protocols extending FLEXT foundation protocols.

    This class extends p with gRPC-specific protocols while maintaining
    all foundation protocols from flext-core.

    Architecture:
    - EXTENDS: p with all foundation protocols
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

        class ServerProtocol(p.Service, Protocol):
            """Protocol for gRPC server management operations."""

            def start_server(
                self,
                host: str,
                port: int,
                services: list[object] | None = None,
            ) -> FlextResult[object]:
                """Start gRPC server."""
                ...

            def stop_server(self, *, grace_period: float = 30.0) -> FlextResult[bool]:
                """Stop gRPC server."""
                ...

            def add_service(self, service: object, server: object) -> FlextResult[bool]:
                """Add gRPC service to server."""
                ...

            def get_server_status(self) -> FlextResult[dict[str, object]]:
                """Get gRPC server status information."""
                ...

            def configure_port(
                self,
                server: object,
                host: str,
                port: int,
                *,
                secure: bool = False,
            ) -> FlextResult[int]:
                """Configure server port binding."""
                ...

        class ClientProtocol(p.Service, Protocol):
            """Protocol for gRPC client communication operations."""

            def connect_client(
                self,
                target: str,
                *,
                timeout: float = 30.0,
            ) -> FlextResult[object]:
                """Connect gRPC client to server."""
                ...

            def disconnect_client(self, channel: object) -> FlextResult[bool]:
                """Disconnect gRPC client."""
                ...

            def make_call(
                self,
                channel: object,
                method: FlextGrpcConstants.Literals.StreamTypeLiteral | str,
                request: object,
                *,
                timeout: float = 30.0,
            ) -> FlextResult[object]:
                """Make gRPC method call."""
                ...

            def get_client_status(
                self,
                channel: object,
            ) -> FlextResult[dict[str, object]]:
                """Get gRPC client status information."""
                ...

            def validate_connection(self, channel: object) -> FlextResult[bool]:
                """Validate gRPC client connection."""
                ...

        class StreamingProtocol(p.Service, Protocol):
            """Protocol for gRPC streaming operations."""

            def create_stream(
                self,
                stream_type: FlextGrpcConstants.Literals.StreamTypeLiteral | str,
                channel: object,
                method: str,  # gRPC method name (not StreamType)
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
                self,
                stream: object,
                data_list: list[object],
            ) -> FlextResult[object]:
                """Handle client-side streaming."""
                ...

            def handle_server_streaming(
                self,
                stream: object,
                request: object,
            ) -> FlextResult[list[object]]:
                """Handle server-side streaming."""
                ...

            def handle_bidirectional_streaming(
                self,
                stream: object,
            ) -> FlextResult[dict[str, object]]:
                """Handle bidirectional streaming."""
                ...

        class ServiceProtocol(p.Service, Protocol):
            """Protocol for gRPC service definition and management."""

            def create_service(
                self,
                service_name: str,
                methods: dict[str, object],
            ) -> FlextResult[object]:
                """Create gRPC service definition."""
                ...

            def register_service(
                self,
                service: object,
                server: object,
            ) -> FlextResult[bool]:
                """Register gRPC service with server."""
                ...

            def validate_service(self, service: object) -> FlextResult[bool]:
                """Validate gRPC service definition."""
                ...

            def get_service_methods(self, service: object) -> FlextResult[list[str]]:
                """Get list of service methods."""
                ...

        class ChannelProtocol(p.Service, Protocol):
            """Protocol for gRPC channel management operations."""

            def create_channel(
                self,
                target: str,
                options: dict[str, object] | None = None,
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
                self,
                channel: object,
                last_state: str,
                *,
                timeout: float = 30.0,
            ) -> FlextResult[bool]:
                """Wait for channel state change."""
                ...

        class MetricsProtocol(p.Service, Protocol):
            """Protocol for gRPC metrics collection and monitoring."""

            def collect_server_metrics(
                self,
                server: object,
            ) -> FlextResult[dict[str, object]]:
                """Collect gRPC server metrics."""
                ...

            def collect_client_metrics(
                self,
                channel: object,
            ) -> FlextResult[dict[str, object]]:
                """Collect gRPC client metrics."""
                ...

            def collect_stream_metrics(
                self,
                stream: object,
            ) -> FlextResult[dict[str, object]]:
                """Collect gRPC stream metrics."""
                ...

            def start_metrics_collection(
                self,
                *,
                interval: float = 60.0,
            ) -> FlextResult[bool]:
                """Start automatic metrics collection."""
                ...

            def stop_metrics_collection(self) -> FlextResult[bool]:
                """Stop automatic metrics collection."""
                ...

            def get_global_metrics(self) -> FlextResult[dict[str, object]]:
                """Get global gRPC metrics."""
                ...

        @runtime_checkable
        class ConfigurationProtocol(p.Service, Protocol):
            """Protocol for gRPC configuration management."""

            def create_server_config(
                self,
                host: str,
                port: int,
                options: dict[str, object] | None = None,
            ) -> FlextResult[dict[str, object]]:
                """Create gRPC server configuration."""
                ...

            def create_client_config(
                self,
                target: str,
                options: dict[str, object] | None = None,
            ) -> FlextResult[dict[str, object]]:
                """Create gRPC client configuration."""
                ...

            def validate_config(self) -> "p.ResultProtocol[bool]":
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
