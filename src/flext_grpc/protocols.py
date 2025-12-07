"""gRPC protocols for FLEXT ecosystem."""

from typing import Protocol, runtime_checkable

from flext_core.protocols import FlextProtocols
from flext_core.result import r

from flext_grpc.constants import c


class FlextGrpcProtocols(FlextProtocols):
    """Unified gRPC protocols extending FlextProtocols.

    Extends FlextProtocols to inherit all foundation protocols (Result, Service, etc.)
    and adds gRPC-specific protocols in the Grpc namespace.

    Architecture:
    - EXTENDS: FlextProtocols (inherits Foundation, Domain, Application, etc.)
    - ADDS: gRPC-specific protocols in Grpc namespace
    - PROVIDES: Root-level alias `p` for convenient access

    Usage:
    from flext_grpc.protocols import p

    # Foundation protocols (inherited)
    result: p.Result[str]
    service: p.Service[str]

    # gRPC-specific protocols
    server: p.Grpc.ServerProtocol
    client: p.Grpc.ClientProtocol
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
        class ServerProtocol(Protocol):
            """Protocol for gRPC server management operations."""

            def start_server(
                self,
                host: str,
                port: int,
                services: list[object] | None = None,
            ) -> FlextProtocols.Result[object]:
                """Start gRPC server."""
                ...

            def stop_server(
                self, *, grace_period: float = 30.0
            ) -> FlextProtocols.Result[bool]:
                """Stop gRPC server."""
                ...

            def add_service(
                self, service: object, server: object
            ) -> FlextProtocols.Result[bool]:
                """Add gRPC service to server."""
                ...

            def get_server_status(self) -> FlextProtocols.Result[dict[str, object]]:
                """Get gRPC server status information."""
                ...

            def configure_port(
                self,
                server: object,
                host: str,
                port: int,
                *,
                secure: bool = False,
            ) -> FlextProtocols.Result[int]:
                """Configure server port binding."""
                ...

        @runtime_checkable
        class ClientProtocol(Protocol):
            """Protocol for gRPC client communication operations."""

            def connect_client(
                self,
                target: str,
                *,
                timeout: float = 30.0,
            ) -> FlextProtocols.Result[object]:
                """Connect gRPC client to server."""
                ...

            def disconnect_client(self, channel: object) -> FlextProtocols.Result[bool]:
                """Disconnect gRPC client."""
                ...

            def make_call(
                self,
                channel: object,
                method: c.Grpc.StreamTypeLiteral | str,
                request: object,
                *,
                timeout: float = 30.0,
            ) -> FlextProtocols.Result[object]:
                """Make gRPC method call."""
                ...

            def get_client_status(
                self,
                channel: object,
            ) -> FlextProtocols.Result[dict[str, object]]:
                """Get gRPC client status information."""
                ...

            def validate_connection(
                self, channel: object
            ) -> FlextProtocols.Result[bool]:
                """Validate gRPC client connection."""
                ...

        @runtime_checkable
        class StreamingProtocol(Protocol):
            """Protocol for gRPC streaming operations."""

            def create_stream(
                self,
                stream_type: c.Grpc.StreamTypeLiteral | str,
                channel: object,
                method: str,  # gRPC method name (not StreamType)
            ) -> FlextProtocols.Result[object]:
                """Create gRPC stream."""
                ...

            def send_data(
                self, stream: object, data: object
            ) -> FlextProtocols.Result[bool]:
                """Send data through gRPC stream."""
                ...

            def close_stream(self, stream: object) -> FlextProtocols.Result[bool]:
                """Close gRPC stream."""
                ...

            def handle_client_streaming(
                self,
                stream: object,
                data_list: list[object],
            ) -> FlextProtocols.Result[object]:
                """Handle client-side streaming."""
                ...

            def handle_server_streaming(
                self,
                stream: object,
                request: object,
            ) -> FlextProtocols.Result[list[object]]:
                """Handle server-side streaming."""
                ...

            def handle_bidirectional_streaming(
                self,
                stream: object,
            ) -> FlextProtocols.Result[dict[str, object]]:
                """Handle bidirectional streaming."""
                ...

        @runtime_checkable
        class ServiceProtocol(Protocol):
            """Protocol for gRPC service definition and management."""

            def create_service(
                self,
                service_name: str,
                methods: dict[str, object],
            ) -> FlextProtocols.Result[object]:
                """Create gRPC service definition."""
                ...

            def register_service(
                self,
                service: object,
                server: object,
            ) -> FlextProtocols.Result[bool]:
                """Register gRPC service with server."""
                ...

            def validate_service(self, service: object) -> FlextProtocols.Result[bool]:
                """Validate gRPC service definition."""
                ...

            def get_service_methods(
                self, service: object
            ) -> FlextProtocols.Result[list[str]]:
                """Get list of service methods."""
                ...

        @runtime_checkable
        class ChannelProtocol(Protocol):
            """Protocol for gRPC channel management operations."""

            def create_channel(
                self,
                target: str,
                options: dict[str, object] | None = None,
            ) -> FlextProtocols.Result[object]:
                """Create gRPC channel."""
                ...

            def close_channel(self, channel: object) -> FlextProtocols.Result[bool]:
                """Close gRPC channel."""
                ...

            def get_channel_state(self, channel: object) -> FlextProtocols.Result[str]:
                """Get gRPC channel connection state."""
                ...

            def wait_for_state_change(
                self,
                channel: object,
                last_state: str,
                *,
                timeout: float = 30.0,
            ) -> FlextProtocols.Result[bool]:
                """Wait for channel state change."""
                ...

        @runtime_checkable
        class MetricsProtocol(Protocol):
            """Protocol for gRPC metrics collection and monitoring."""

            def collect_server_metrics(
                self,
                server: object,
            ) -> FlextProtocols.Result[dict[str, object]]:
                """Collect gRPC server metrics."""
                ...

            def collect_client_metrics(
                self,
                channel: object,
            ) -> FlextProtocols.Result[dict[str, object]]:
                """Collect gRPC client metrics."""
                ...

            def collect_stream_metrics(
                self,
                stream: object,
            ) -> FlextProtocols.Result[dict[str, object]]:
                """Collect gRPC stream metrics."""
                ...

            def start_metrics_collection(
                self,
                *,
                interval: float = 60.0,
            ) -> FlextProtocols.Result[bool]:
                """Start automatic metrics collection."""
                ...

            def stop_metrics_collection(self) -> FlextProtocols.Result[bool]:
                """Stop automatic metrics collection."""
                ...

            def get_global_metrics(
                self,
            ) -> FlextProtocols.Result[dict[str, object]]:
                """Get global gRPC metrics."""
                ...

        @runtime_checkable
        class ConfigurationProtocol(Protocol):
            """Protocol for gRPC configuration management."""

            def create_server_config(
                self,
                host: str,
                port: int,
                options: dict[str, object] | None = None,
            ) -> FlextProtocols.Result[dict[str, object]]:
                """Create gRPC server configuration."""
                ...

            def create_client_config(
                self,
                target: str,
                options: dict[str, object] | None = None,
            ) -> FlextProtocols.Result[dict[str, object]]:
                """Create gRPC client configuration."""
                ...

            def validate_config(self) -> "r[bool]":
                """Validate gRPC configuration."""
                ...

            def parse_address(
                self, address: str
            ) -> FlextProtocols.Result[tuple[str, int]]:
                """Parse gRPC address string."""
                ...

            def validate_address(self, address: str) -> FlextProtocols.Result[bool]:
                """Validate gRPC address format."""
                ...


# Runtime alias for simplified usage
p = FlextGrpcProtocols

__all__ = [
    "FlextGrpcProtocols",
    "p",
]
