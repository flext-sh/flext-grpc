"""gRPC protocols for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

from flext_cli import p

if TYPE_CHECKING:
    import threading
    from collections.abc import Callable, Iterable, Mapping, Sequence
    from concurrent.futures import Executor

    from flext_grpc import c, t


class FlextGrpcProtocols(p):
    """Unified gRPC protocols extending p.

    Extends p to inherit all foundation protocols (Result, Service, etc.)
    and adds gRPC-specific protocols in the Grpc namespace.

    Architecture:
    - EXTENDS: p (inherits Foundation, Domain, Application, etc.)
    - ADDS: gRPC-specific protocols in Grpc namespace
    - PROVIDES: Root-level alias `p` for convenient access

    Usage:
    from flext_grpc import p

    # Foundation protocols (inherited)
    result: p.Result[str]
    service: p.Grpc.Service[str]

    # gRPC-specific protocols
    server: p.Grpc.Server
    client: p.Grpc.Client
    """

    @runtime_checkable
    class Grpc(Protocol):
        """gRPC domain-specific protocols.

        Provides protocols for gRPC server management, client communication,
        streaming operations, service definitions, channel management,
        metrics collection, and configuration.
        """

        @runtime_checkable
        class ClientConnection(Protocol):
            """Base class for gRPC client connection management."""

        @runtime_checkable
        class ServerLifecycle(Protocol):
            """Base class for gRPC server lifecycle management."""

        @runtime_checkable
        class StreamProcessor(Protocol):
            """Base class for gRPC stream processing."""

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
            ) -> p.Result[bool]:
                """Add gRPC service to server."""
                ...

            def configure_port(
                self,
                server: FlextGrpcProtocols.Grpc.GrpcServer,
                host: str,
                port: int,
                *,
                secure: bool = False,
            ) -> p.Result[int]:
                """Configure server port binding."""
                ...

            def server_status(
                self,
            ) -> p.Result[t.JsonValue | None]:
                """Get gRPC server status information."""
                ...

            def start_server(
                self,
                host: str,
                port: int,
                services: t.SequenceOf[FlextGrpcProtocols.Grpc.GrpcServicer]
                | None = None,
            ) -> p.Result[FlextGrpcProtocols.Grpc.GrpcServer]:
                """Start gRPC server."""
                ...

            def stop_server(
                self,
                *,
                grace_period: float = 30.0,
            ) -> p.Result[bool]:
                """Stop gRPC server."""
                ...

        class GrpcMessage(Protocol):
            """Typed boundary shared by generated protobuf messages."""

            def __deepcopy__(
                self,
                memo: t.MutableMappingKV[
                    int,
                    FlextGrpcProtocols.Grpc.GrpcMessage,
                ]
                | None = None,
            ) -> FlextGrpcProtocols.Grpc.GrpcMessage:
                """Create an independent message preserving its schema type."""
                ...

        class EchoRequestMessage(GrpcMessage, Protocol):
            """Typed protobuf boundary for an echo request."""

            message: str

        class EchoResponseMessage(GrpcMessage, Protocol):
            """Typed protobuf boundary for an echo response."""

            message: str
            server_id: str
            timestamp: str

        class HealthRequestMessage(GrpcMessage, Protocol):
            """Typed protobuf boundary for a health request."""

            service: str

        class HealthResponseMessage(GrpcMessage, Protocol):
            """Typed protobuf boundary for a health response."""

            status: str
            message: str

        @runtime_checkable
        class GrpcServicerContext(Protocol):
            """Opaque runtime context supplied by grpcio to a servicer."""

        class EchoRpc(Protocol):
            """Typed callable for the generated Echo RPC."""

            def __call__(
                self,
                request: FlextGrpcProtocols.Grpc.GrpcMessage,
            ) -> FlextGrpcProtocols.Grpc.EchoResponseMessage:
                """Invoke Echo with a generated request message."""
                ...

        class HealthCheckRpc(Protocol):
            """Typed callable for the generated HealthCheck RPC."""

            def __call__(
                self,
                request: FlextGrpcProtocols.Grpc.GrpcMessage,
            ) -> FlextGrpcProtocols.Grpc.HealthResponseMessage:
                """Invoke HealthCheck with a generated request message."""
                ...

        @runtime_checkable
        class Client(Protocol):
            """Protocol for gRPC client communication operations."""

            def connect_client(
                self,
                target: str,
                *,
                timeout: float = 30.0,
            ) -> p.Result[FlextGrpcProtocols.Grpc.GrpcChannel]:
                """Connect gRPC client to server."""
                ...

            def disconnect_client(
                self,
                channel: FlextGrpcProtocols.Grpc.GrpcChannel,
            ) -> p.Result[bool]:
                """Disconnect gRPC client."""
                ...

            def client_status(
                self,
                channel: FlextGrpcProtocols.Grpc.GrpcChannel,
            ) -> p.Result[t.JsonValue | None]:
                """Get gRPC client status information."""
                ...

            def make_call(
                self,
                channel: FlextGrpcProtocols.Grpc.GrpcChannel,
                method: c.Grpc.GrpcOperations | str,
                request: FlextGrpcProtocols.Grpc.GrpcMessage,
                *,
                timeout: float = 30.0,
            ) -> p.Result[FlextGrpcProtocols.Grpc.GrpcMessage]:
                """Make gRPC method call."""
                ...

            def validate_connection(
                self,
                channel: FlextGrpcProtocols.Grpc.GrpcChannel,
            ) -> p.Result[bool]:
                """Validate gRPC client connection."""
                ...

        @runtime_checkable
        class GrpcStream(Protocol):
            """Protocol for gRPC stream objects (duck typing)."""

        @runtime_checkable
        class Streaming(Protocol):
            """Protocol for gRPC streaming operations."""

            def close_stream(
                self,
                stream: FlextGrpcProtocols.Grpc.GrpcStream,
            ) -> p.Result[bool]:
                """Close gRPC stream."""
                ...

            def create_stream(
                self,
                stream_type: c.Grpc.GrpcOperations | str,
                channel: FlextGrpcProtocols.Grpc.GrpcChannel,
                method: str,
            ) -> p.Result[FlextGrpcProtocols.Grpc.GrpcStream]:
                """Create gRPC stream."""
                ...

            def handle_bidirectional_streaming(
                self,
                stream: FlextGrpcProtocols.Grpc.GrpcStream,
            ) -> p.Result[t.JsonValue | None]:
                """Handle bidirectional streaming."""
                ...

            def handle_client_streaming(
                self,
                stream: FlextGrpcProtocols.Grpc.GrpcStream,
                data_list: t.SequenceOf[FlextGrpcProtocols.Grpc.GrpcMessage],
            ) -> p.Result[FlextGrpcProtocols.Grpc.GrpcMessage]:
                """Handle client-side streaming."""
                ...

            def handle_server_streaming(
                self,
                stream: FlextGrpcProtocols.Grpc.GrpcStream,
                request: FlextGrpcProtocols.Grpc.GrpcMessage,
            ) -> p.Result[Sequence[FlextGrpcProtocols.Grpc.GrpcMessage]]:
                """Handle server-side streaming."""
                ...

            def send_data(
                self,
                stream: FlextGrpcProtocols.Grpc.GrpcStream,
                data: FlextGrpcProtocols.Grpc.GrpcMessage,
            ) -> p.Result[bool]:
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
                methods: t.MappingKV[str, FlextGrpcProtocols.Grpc.GrpcMethodHandler],
            ) -> p.Result[FlextGrpcProtocols.Grpc.GrpcServicer]:
                """Create gRPC service definition."""
                ...

            def service_methods(
                self,
                service: FlextGrpcProtocols.Grpc.GrpcServicer,
            ) -> p.Result[t.StrSequence]:
                """Get list of service methods."""
                ...

            def register_service(
                self,
                service: FlextGrpcProtocols.Grpc.GrpcServicer,
                server: FlextGrpcProtocols.Grpc.GrpcServer,
            ) -> p.Result[bool]:
                """Register gRPC service with server."""
                ...

            def validate_service(
                self,
                service: FlextGrpcProtocols.Grpc.GrpcServicer,
            ) -> p.Result[bool]:
                """Validate gRPC service definition."""
                ...

        @runtime_checkable
        class Channel(Protocol):
            """Protocol for gRPC channel management operations."""

            def close_channel(
                self,
                channel: FlextGrpcProtocols.Grpc.GrpcChannel,
            ) -> p.Result[bool]:
                """Close gRPC channel."""
                ...

            def create_channel(
                self,
                target: str,
                options: t.MappingKV[str, t.JsonValue | None] | None = None,
            ) -> p.Result[FlextGrpcProtocols.Grpc.GrpcChannel]:
                """Create gRPC channel."""
                ...

            def channel_state(
                self,
                channel: FlextGrpcProtocols.Grpc.GrpcChannel,
            ) -> p.Result[str]:
                """Get gRPC channel connection state."""
                ...

            def wait_for_state_change(
                self,
                channel: FlextGrpcProtocols.Grpc.GrpcChannel,
                last_state: str,
                *,
                timeout: float = 30.0,
            ) -> p.Result[bool]:
                """Wait for channel state change."""
                ...

        @runtime_checkable
        class Metrics(Protocol):
            """Protocol for gRPC metrics collection and monitoring."""

            def collect_client_metrics(
                self,
                channel: FlextGrpcProtocols.Grpc.GrpcChannel,
            ) -> p.Result[Mapping[str, t.Numeric | str]]:
                """Collect gRPC client metrics."""
                ...

            def collect_server_metrics(
                self,
                server: FlextGrpcProtocols.Grpc.GrpcServer,
            ) -> p.Result[Mapping[str, t.Numeric | str]]:
                """Collect gRPC server metrics."""
                ...

            def collect_stream_metrics(
                self,
                stream: FlextGrpcProtocols.Grpc.GrpcStream,
            ) -> p.Result[Mapping[str, t.Numeric | str]]:
                """Collect gRPC stream metrics."""
                ...

            def global_metrics(
                self,
            ) -> p.Result[Mapping[str, t.Numeric | str]]:
                """Get global gRPC metrics."""
                ...

            def start_metrics_collection(
                self,
                *,
                interval: float = 60.0,
            ) -> p.Result[bool]:
                """Start automatic metrics collection."""
                ...

            def stop_metrics_collection(self) -> p.Result[bool]:
                """Stop automatic metrics collection."""
                ...

        @runtime_checkable
        class Configuration(Protocol):
            """Protocol for gRPC configuration management."""

            def create_client_config(
                self,
                target: str,
                options: t.MappingKV[str, t.JsonValue | None] | None = None,
            ) -> p.Result[t.ScalarMapping]:
                """Create gRPC client configuration."""
                ...

            def create_server_config(
                self,
                host: str,
                port: int,
                options: t.MappingKV[str, t.JsonValue | None] | None = None,
            ) -> p.Result[t.ScalarMapping]:
                """Create gRPC server configuration."""
                ...

            def parse_address(
                self,
                address: str,
            ) -> p.Result[tuple[str, int]]:
                """Parse gRPC address string."""
                ...

            def validate_address(self, address: str) -> p.Result[bool]:
                """Validate gRPC address format."""
                ...

            def validate_config(self) -> p.Result[bool]:
                """Validate gRPC configuration."""
                ...

        @runtime_checkable
        class GrpcResource(Protocol):
            """Protocol for gRPC resource objects (channels, servers, streams)."""

        @runtime_checkable
        class ResourceManager(Protocol):
            """Protocol for gRPC resource management operations."""

            def acquire(self) -> p.Result[FlextGrpcProtocols.Grpc.GrpcResource]:
                """Acquire a resource."""
                ...

            def cleanup(self) -> p.Result[bool]:
                """Cleanup all resources."""
                ...

            def release(
                self,
                resource: FlextGrpcProtocols.Grpc.GrpcResource,
            ) -> p.Result[bool]:
                """Release a resource."""
                ...

        @runtime_checkable
        class GrpcCallbackFunction(Protocol):
            """Protocol for gRPC callback functions."""

            def __call__(
                self,
                *args: t.Scalar,
                **kwargs: t.Scalar,
            ) -> None:
                """Call the callback."""
                ...

        @runtime_checkable
        class GrpcChannel(Protocol):
            """Protocol for gRPC channel operations (duck typing for grpc.Channel)."""

            def close(self) -> None:
                """Close the channel."""
                ...

            def unsubscribe(self, callback: Callable[..., None]) -> None:
                """Remove a subscription callback from the channel."""
                ...

        @runtime_checkable
        class GrpcRpcHandler(Protocol):
            """Protocol for gRPC RPC handlers."""

        @runtime_checkable
        class GrpcReadyFuture(Protocol):
            """Protocol for gRPC ready futures."""

            def result(self, timeout: float | None = None) -> None:
                """Wait until the underlying operation is ready."""
                ...

        @runtime_checkable
        class GrpcServer(Protocol):
            """Protocol for gRPC server operations (duck typing for grpc.Server)."""

            def add_insecure_port(self, address: str) -> int:
                """Bind the server to an insecure address."""
                ...

            def add_generic_rpc_handlers(
                self,
                generic_rpc_handlers: Iterable[FlextGrpcProtocols.Grpc.GrpcRpcHandler],
            ) -> None:
                """Add generic RPC handlers."""
                ...

            def start(self) -> None:
                """Start the server."""
                ...

            def stop(self, grace: float | None) -> threading.Event:
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
        class GrpcCallFailure(Protocol):
            """Protocol for gRPC call failures exposing status details."""

            def code(self) -> str | None:
                """Return the gRPC status code, if available."""
                ...

            def details(self) -> str:
                """Return the gRPC status details."""
                ...

        @runtime_checkable
        class GrpcRuntime(Protocol):
            """Protocol for the imported grpc runtime module."""

            RpcError: type[Exception]
            FutureTimeoutError: type[Exception]

            def insecure_channel(
                self,
                target: str,
            ) -> FlextGrpcProtocols.Grpc.GrpcChannel:
                """Create an insecure channel for a target."""
                ...

            def channel_ready_future(
                self,
                channel: FlextGrpcProtocols.Grpc.GrpcChannel,
            ) -> FlextGrpcProtocols.Grpc.GrpcReadyFuture:
                """Create a future used to wait for channel readiness."""
                ...

            def server(
                self,
                thread_pool: Executor,
            ) -> FlextGrpcProtocols.Grpc.GrpcServer:
                """Create a gRPC server using the given thread pool."""
                ...

        @runtime_checkable
        class EntityFactory(Protocol):
            """Protocol for entity factory callables."""

            def __call__(
                self,
                **kwargs: t.Scalar,
            ) -> p.Result[FlextGrpcProtocols.Grpc.GrpcResource]:
                """Create entity with given arguments."""
                ...

        @runtime_checkable
        class OperationHandler(Protocol):
            """Protocol for operation handler callables."""

            def __call__(
                self,
                **kwargs: t.Scalar,
            ) -> p.Result[FlextGrpcProtocols.Grpc.GrpcResource]:
                """Execute operation with given arguments."""
                ...


p = FlextGrpcProtocols

__all__: list[str] = [
    "FlextGrpcProtocols",
    "p",
]
