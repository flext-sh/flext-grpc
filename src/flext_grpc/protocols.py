"""gRPC protocols for FLEXT ecosystem."""

from typing import Protocol, runtime_checkable

from flext_core import p as p_core, r

from flext_grpc.constants import FlextGrpcConstants


class FlextGrpcProtocols(p_core):
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

        class ServerProtocol(Protocol):
            """Protocol for gRPC server management operations."""

            def start_server(
                self,
                host: str,
                port: int,
                services: list[object] | None = None,
            ) -> r[object]:
                """Start gRPC server."""
                ...

            def stop_server(self, *, grace_period: float = 30.0) -> r[bool]:
                """Stop gRPC server."""
                ...

            def add_service(self, service: object, server: object) -> r[bool]:
                """Add gRPC service to server."""
                ...

            def get_server_status(self) -> r[dict[str, object]]:
                """Get gRPC server status information."""
                ...

            def configure_port(
                self,
                server: object,
                host: str,
                port: int,
                *,
                secure: bool = False,
            ) -> r[int]:
                """Configure server port binding."""
                ...

        class ClientProtocol(Protocol):
            """Protocol for gRPC client communication operations."""

            def connect_client(
                self,
                target: str,
                *,
                timeout: float = 30.0,
            ) -> r[object]:
                """Connect gRPC client to server."""
                ...

            def disconnect_client(self, channel: object) -> r[bool]:
                """Disconnect gRPC client."""
                ...

            def make_call(
                self,
                channel: object,
                method: FlextGrpcConstants.Literals.StreamTypeLiteral | str,
                request: object,
                *,
                timeout: float = 30.0,
            ) -> r[object]:
                """Make gRPC method call."""
                ...

            def get_client_status(
                self,
                channel: object,
            ) -> r[dict[str, object]]:
                """Get gRPC client status information."""
                ...

            def validate_connection(self, channel: object) -> r[bool]:
                """Validate gRPC client connection."""
                ...

        class StreamingProtocol(Protocol):
            """Protocol for gRPC streaming operations."""

            def create_stream(
                self,
                stream_type: FlextGrpcConstants.Literals.StreamTypeLiteral | str,
                channel: object,
                method: str,  # gRPC method name (not StreamType)
            ) -> r[object]:
                """Create gRPC stream."""
                ...

            def send_data(self, stream: object, data: object) -> r[bool]:
                """Send data through gRPC stream."""
                ...

            def close_stream(self, stream: object) -> r[bool]:
                """Close gRPC stream."""
                ...

            def handle_client_streaming(
                self,
                stream: object,
                data_list: list[object],
            ) -> r[object]:
                """Handle client-side streaming."""
                ...

            def handle_server_streaming(
                self,
                stream: object,
                request: object,
            ) -> r[list[object]]:
                """Handle server-side streaming."""
                ...

            def handle_bidirectional_streaming(
                self,
                stream: object,
            ) -> r[dict[str, object]]:
                """Handle bidirectional streaming."""
                ...

        class ServiceProtocol(Protocol):
            """Protocol for gRPC service definition and management."""

            def create_service(
                self,
                service_name: str,
                methods: dict[str, object],
            ) -> r[object]:
                """Create gRPC service definition."""
                ...

            def register_service(
                self,
                service: object,
                server: object,
            ) -> r[bool]:
                """Register gRPC service with server."""
                ...

            def validate_service(self, service: object) -> r[bool]:
                """Validate gRPC service definition."""
                ...

            def get_service_methods(self, service: object) -> r[list[str]]:
                """Get list of service methods."""
                ...

        class ChannelProtocol(Protocol):
            """Protocol for gRPC channel management operations."""

            def create_channel(
                self,
                target: str,
                options: dict[str, object] | None = None,
            ) -> r[object]:
                """Create gRPC channel."""
                ...

            def close_channel(self, channel: object) -> r[bool]:
                """Close gRPC channel."""
                ...

            def get_channel_state(self, channel: object) -> r[str]:
                """Get gRPC channel connection state."""
                ...

            def wait_for_state_change(
                self,
                channel: object,
                last_state: str,
                *,
                timeout: float = 30.0,
            ) -> r[bool]:
                """Wait for channel state change."""
                ...

        class MetricsProtocol(Protocol):
            """Protocol for gRPC metrics collection and monitoring."""

            def collect_server_metrics(
                self,
                server: object,
            ) -> r[dict[str, object]]:
                """Collect gRPC server metrics."""
                ...

            def collect_client_metrics(
                self,
                channel: object,
            ) -> r[dict[str, object]]:
                """Collect gRPC client metrics."""
                ...

            def collect_stream_metrics(
                self,
                stream: object,
            ) -> r[dict[str, object]]:
                """Collect gRPC stream metrics."""
                ...

            def start_metrics_collection(
                self,
                *,
                interval: float = 60.0,
            ) -> r[bool]:
                """Start automatic metrics collection."""
                ...

            def stop_metrics_collection(self) -> r[bool]:
                """Stop automatic metrics collection."""
                ...

            def get_global_metrics(self) -> r[dict[str, object]]:
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
            ) -> r[dict[str, object]]:
                """Create gRPC server configuration."""
                ...

            def create_client_config(
                self,
                target: str,
                options: dict[str, object] | None = None,
            ) -> r[dict[str, object]]:
                """Create gRPC client configuration."""
                ...

            def validate_config(self) -> "r[bool]":
                """Validate gRPC configuration."""
                ...

            def parse_address(self, address: str) -> r[tuple[str, int]]:
                """Parse gRPC address string."""
                ...

            def validate_address(self, address: str) -> r[bool]:
                """Validate gRPC address format."""
                ...


__all__ = [
    "FlextGrpcProtocols",
]
