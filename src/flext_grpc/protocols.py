"""gRPC protocols for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Protocol, runtime_checkable

from flext_core import FlextProtocols, r, t

from flext_grpc import c
from flext_grpc.models import FlextGrpcModels

ServicePayload = FlextGrpcModels.Grpc.Payload


class FlextGrpcProtocols(FlextProtocols):
    """Unified gRPC protocols extending FlextProtocols.

    Extends FlextProtocols to inherit all foundation protocols (Result, Service, etc.)
    and adds gRPC-specific protocols in the Grpc namespace.

    Architecture:
    - EXTENDS: FlextProtocols (inherits Foundation, Domain, Application, etc.)
    - ADDS: gRPC-specific protocols in Grpc namespace
    - PROVIDES: Root-level alias `p` for convenient access

    Usage:
    from flext_grpc import p

    # Foundation protocols (inherited)
    result: p.Result[str]
    service: p.Service[str]

    # gRPC-specific protocols
    server: p.Grpc.Server
    client: p.Grpc.Client
    """

    class Grpc:
        """gRPC domain-specific protocols.

        Provides protocols for gRPC server management, client communication,
        streaming operations, service definitions, channel management,
        metrics collection, and configuration.
        """

        @runtime_checkable
        class GrpcServicer(Protocol):
            """Protocol for gRPC service implementations (duck typing)."""

        @runtime_checkable
        class Server(Protocol):
            """Protocol for gRPC server management operations."""

            def add_service(
                self,
                service: FlextGrpcProtocols.Grpc.GrpcServicer,
                server: FlextGrpcProtocols.Grpc.GrpcServer,
            ) -> FlextProtocols.Result[bool]:
                """Add gRPC service to server."""
                ...

            def configure_port(
                self,
                server: FlextGrpcProtocols.Grpc.GrpcServer,
                host: str,
                port: int,
                *,
                secure: bool = False,
            ) -> FlextProtocols.Result[int]:
                """Configure server port binding."""
                ...

            def get_server_status(
                self,
            ) -> FlextProtocols.Result[t.ContainerValue | None]:
                """Get gRPC server status information."""
                ...

            def start_server(
                self,
                host: str,
                port: int,
                services: list[FlextGrpcProtocols.Grpc.GrpcServicer] | None = None,
            ) -> FlextProtocols.Result[FlextGrpcProtocols.Grpc.GrpcServer]:
                """Start gRPC server."""
                ...

            def stop_server(
                self, *, grace_period: float = 30.0
            ) -> FlextProtocols.Result[bool]:
                """Stop gRPC server."""
                ...

        @runtime_checkable
        class GrpcMessage(Protocol):
            """Protocol for gRPC message objects (duck typing for protobuf messages)."""

        @runtime_checkable
        class Client(Protocol):
            """Protocol for gRPC client communication operations."""

            def connect_client(
                self, target: str, *, timeout: float = 30.0
            ) -> FlextProtocols.Result[FlextGrpcProtocols.Grpc.GrpcChannel]:
                """Connect gRPC client to server."""
                ...

            def disconnect_client(
                self, channel: FlextGrpcProtocols.Grpc.GrpcChannel
            ) -> FlextProtocols.Result[bool]:
                """Disconnect gRPC client."""
                ...

            def get_client_status(
                self, channel: FlextGrpcProtocols.Grpc.GrpcChannel
            ) -> FlextProtocols.Result[t.ContainerValue | None]:
                """Get gRPC client status information."""
                ...

            def make_call(
                self,
                channel: FlextGrpcProtocols.Grpc.GrpcChannel,
                method: c.Grpc.StreamTypeLiteral | str,
                request: FlextGrpcProtocols.Grpc.GrpcMessage,
                *,
                timeout: float = 30.0,
            ) -> FlextProtocols.Result[FlextGrpcProtocols.Grpc.GrpcMessage]:
                """Make gRPC method call."""
                ...

            def validate_connection(
                self, channel: FlextGrpcProtocols.Grpc.GrpcChannel
            ) -> FlextProtocols.Result[bool]:
                """Validate gRPC client connection."""
                ...

        @runtime_checkable
        class GrpcStream(Protocol):
            """Protocol for gRPC stream objects (duck typing)."""

        @runtime_checkable
        class Streaming(Protocol):
            """Protocol for gRPC streaming operations."""

            def close_stream(
                self, stream: FlextGrpcProtocols.Grpc.GrpcStream
            ) -> FlextProtocols.Result[bool]:
                """Close gRPC stream."""
                ...

            def create_stream(
                self,
                stream_type: c.Grpc.StreamTypeLiteral | str,
                channel: FlextGrpcProtocols.Grpc.GrpcChannel,
                method: str,
            ) -> FlextProtocols.Result[FlextGrpcProtocols.Grpc.GrpcStream]:
                """Create gRPC stream."""
                ...

            def handle_bidirectional_streaming(
                self, stream: FlextGrpcProtocols.Grpc.GrpcStream
            ) -> FlextProtocols.Result[t.ContainerValue | None]:
                """Handle bidirectional streaming."""
                ...

            def handle_client_streaming(
                self,
                stream: FlextGrpcProtocols.Grpc.GrpcStream,
                data_list: list[FlextGrpcProtocols.Grpc.GrpcMessage],
            ) -> FlextProtocols.Result[FlextGrpcProtocols.Grpc.GrpcMessage]:
                """Handle client-side streaming."""
                ...

            def handle_server_streaming(
                self,
                stream: FlextGrpcProtocols.Grpc.GrpcStream,
                request: FlextGrpcProtocols.Grpc.GrpcMessage,
            ) -> FlextProtocols.Result[list[FlextGrpcProtocols.Grpc.GrpcMessage]]:
                """Handle server-side streaming."""
                ...

            def send_data(
                self,
                stream: FlextGrpcProtocols.Grpc.GrpcStream,
                data: FlextGrpcProtocols.Grpc.GrpcMessage,
            ) -> FlextProtocols.Result[bool]:
                """Send data through gRPC stream."""
                ...

        @runtime_checkable
        class GrpcMethodHandler(Protocol):
            """Protocol for gRPC method handlers (duck typing)."""

        @runtime_checkable
        class Service(Protocol):
            """Protocol for gRPC service definition and management."""

            def create_service(
                self,
                service_name: str,
                methods: Mapping[str, FlextGrpcProtocols.Grpc.GrpcMethodHandler],
            ) -> FlextProtocols.Result[FlextGrpcProtocols.Grpc.GrpcServicer]:
                """Create gRPC service definition."""
                ...

            def get_service_methods(
                self, service: FlextGrpcProtocols.Grpc.GrpcServicer
            ) -> FlextProtocols.Result[list[str]]:
                """Get list of service methods."""
                ...

            def register_service(
                self,
                service: FlextGrpcProtocols.Grpc.GrpcServicer,
                server: FlextGrpcProtocols.Grpc.GrpcServer,
            ) -> FlextProtocols.Result[bool]:
                """Register gRPC service with server."""
                ...

            def validate_service(
                self, service: FlextGrpcProtocols.Grpc.GrpcServicer
            ) -> FlextProtocols.Result[bool]:
                """Validate gRPC service definition."""
                ...

        @runtime_checkable
        class Channel(Protocol):
            """Protocol for gRPC channel management operations."""

            def close_channel(
                self, channel: FlextGrpcProtocols.Grpc.GrpcChannel
            ) -> FlextProtocols.Result[bool]:
                """Close gRPC channel."""
                ...

            def create_channel(
                self,
                target: str,
                options: Mapping[str, t.ContainerValue | None] | None = None,
            ) -> FlextProtocols.Result[FlextGrpcProtocols.Grpc.GrpcChannel]:
                """Create gRPC channel."""
                ...

            def get_channel_state(
                self, channel: FlextGrpcProtocols.Grpc.GrpcChannel
            ) -> FlextProtocols.Result[str]:
                """Get gRPC channel connection state."""
                ...

            def wait_for_state_change(
                self,
                channel: FlextGrpcProtocols.Grpc.GrpcChannel,
                last_state: str,
                *,
                timeout: float = 30.0,
            ) -> FlextProtocols.Result[bool]:
                """Wait for channel state change."""
                ...

        @runtime_checkable
        class Metrics(Protocol):
            """Protocol for gRPC metrics collection and monitoring."""

            def collect_client_metrics(
                self, channel: FlextGrpcProtocols.Grpc.GrpcChannel
            ) -> FlextProtocols.Result[Mapping[str, int | float | str]]:
                """Collect gRPC client metrics."""
                ...

            def collect_server_metrics(
                self, server: FlextGrpcProtocols.Grpc.GrpcServer
            ) -> FlextProtocols.Result[Mapping[str, int | float | str]]:
                """Collect gRPC server metrics."""
                ...

            def collect_stream_metrics(
                self, stream: FlextGrpcProtocols.Grpc.GrpcStream
            ) -> FlextProtocols.Result[Mapping[str, int | float | str]]:
                """Collect gRPC stream metrics."""
                ...

            def get_global_metrics(
                self,
            ) -> FlextProtocols.Result[Mapping[str, int | float | str]]:
                """Get global gRPC metrics."""
                ...

            def start_metrics_collection(
                self, *, interval: float = 60.0
            ) -> FlextProtocols.Result[bool]:
                """Start automatic metrics collection."""
                ...

            def stop_metrics_collection(self) -> FlextProtocols.Result[bool]:
                """Stop automatic metrics collection."""
                ...

        @runtime_checkable
        class Configuration(Protocol):
            """Protocol for gRPC configuration management."""

            def create_client_config(
                self,
                target: str,
                options: Mapping[str, t.ContainerValue | None] | None = None,
            ) -> FlextProtocols.Result[Mapping[str, str | int | bool]]:
                """Create gRPC client configuration."""
                ...

            def create_server_config(
                self,
                host: str,
                port: int,
                options: Mapping[str, t.ContainerValue | None] | None = None,
            ) -> FlextProtocols.Result[Mapping[str, str | int | bool]]:
                """Create gRPC server configuration."""
                ...

            def parse_address(
                self, address: str
            ) -> FlextProtocols.Result[tuple[str, int]]:
                """Parse gRPC address string."""
                ...

            def validate_address(self, address: str) -> FlextProtocols.Result[bool]:
                """Validate gRPC address format."""
                ...

            def validate_config(self) -> r[bool]:
                """Validate gRPC configuration."""
                ...

        @runtime_checkable
        class GrpcResource(Protocol):
            """Protocol for gRPC resource objects (channels, servers, streams)."""

        @runtime_checkable
        class ResourceManager(Protocol):
            """Protocol for gRPC resource management operations."""

            def acquire(self) -> r[FlextGrpcProtocols.Grpc.GrpcResource]:
                """Acquire a resource."""
                ...

            def cleanup(self) -> r[bool]:
                """Cleanup all resources."""
                ...

            def release(
                self, resource: FlextGrpcProtocols.Grpc.GrpcResource
            ) -> r[bool]:
                """Release a resource."""
                ...

        @runtime_checkable
        class GrpcCallbackFunction(Protocol):
            """Protocol for gRPC callback functions."""

            def __call__(self, *args: t.Scalar, **kwargs: t.Scalar) -> None:
                """Call the callback."""
                ...

        @runtime_checkable
        class GrpcChannel(Protocol):
            """Protocol for gRPC channel operations (duck typing for grpc.Channel)."""

            def close(self) -> None:
                """Close the channel."""
                ...

            def unsubscribe(
                self, callback: FlextGrpcProtocols.Grpc.GrpcCallbackFunction
            ) -> None:
                """Remove a subscription callback from the channel."""
                ...

        @runtime_checkable
        class GrpcRpcHandler(Protocol):
            """Protocol for gRPC RPC handlers."""

        @runtime_checkable
        class GrpcServer(Protocol):
            """Protocol for gRPC server operations (duck typing for grpc.Server)."""

            def add_generic_rpc_handlers(
                self, handlers: list[FlextGrpcProtocols.Grpc.GrpcRpcHandler]
            ) -> None:
                """Add generic RPC handlers."""
                ...

            def start(self) -> None:
                """Start the server."""
                ...

            def stop(self, grace: float | None) -> None:
                """Stop the server with optional grace period."""
                ...

        @runtime_checkable
        class GrpcStub(Protocol):
            """Protocol for gRPC client stub (duck typing for grpc stubs)."""

            def __init__(self, channel: FlextGrpcProtocols.Grpc.GrpcChannel) -> None:
                """Initialize the stub with a channel."""
                ...

        @runtime_checkable
        class GrpcChannelCredentials(Protocol):
            """Protocol for gRPC channel credentials (duck typing for grpc.ChannelCredentials)."""

        @runtime_checkable
        class EntityFactory(Protocol):
            """Protocol for entity factory callables."""

            def __call__(
                self, **kwargs: t.Scalar
            ) -> r[FlextGrpcProtocols.Grpc.GrpcResource]:
                """Create entity with given arguments."""
                ...

        @runtime_checkable
        class OperationHandler(Protocol):
            """Protocol for operation handler callables."""

            def __call__(
                self, **kwargs: t.Scalar
            ) -> r[FlextGrpcProtocols.Grpc.GrpcResource]:
                """Execute operation with given arguments."""
                ...


__all__ = ["FlextGrpcProtocols", "p"]

p = FlextGrpcProtocols


class GrpcContextProtocol(Protocol):
    pass


class GrpcChannelProtocol(Protocol):
    pass


class GrpcServerProtocol(Protocol):
    pass


class ServerLifecycle(Protocol):
    """Protocol for server lifecycle management."""

    def start_server(
        self, server: FlextGrpcModels.Grpc.Server
    ) -> r[FlextGrpcModels.Grpc.Server]:
        """Start server implementation."""
        ...

    def stop_server(
        self, server: FlextGrpcModels.Grpc.Server
    ) -> r[FlextGrpcModels.Grpc.Server]:
        """Stop server implementation."""
        ...


class ClientConnection(Protocol):
    """Protocol for client connection management."""

    def connect(self, target: str) -> r[FlextGrpcModels.Grpc.Client]:
        """Connect to target."""
        ...

    def disconnect(
        self, client: FlextGrpcModels.Grpc.Client
    ) -> r[FlextGrpcModels.Grpc.Client]:
        """Disconnect client."""
        ...


class StreamProcessor(Protocol):
    """Protocol for stream processing."""

    def close_stream(
        self, stream: FlextGrpcModels.Grpc.GrpcStream
    ) -> r[FlextGrpcModels.Grpc.GrpcStream]:
        """Close stream."""
        ...

    def create_stream(
        self, **kwargs: t.ConfigValue
    ) -> r[FlextGrpcModels.Grpc.GrpcStream]:
        """Create stream."""
        ...

    def send_data(
        self, stream: FlextGrpcModels.Grpc.GrpcStream, data: t.ConfigValue
    ) -> r[ServicePayload]:
        """Send data through stream.

        Note: Uses t.ConfigValue for gRPC message compatibility
        """
        ...
