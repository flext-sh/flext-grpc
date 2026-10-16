# AUTO-GENERATED FILE — Regenerate with: make gen
"""gRPC protocols for FLEXT ecosystem.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

from flext_cli import FlextCliProtocols

from flext_grpc._protocols import FlextGrpcProtocolsBase

if TYPE_CHECKING:
    import threading
    from collections.abc import Callable, Iterable, Mapping, Sequence
    from concurrent.futures import Executor

    from flext_grpc import c, t


class FlextGrpcProtocols(FlextCliProtocols):
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
    class Grpc(FlextGrpcProtocolsBase, Protocol):
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
                """Add gRPC service to server.

                Args:
                    service: Servicer implementing the service methods.
                    server: Server receiving the service registration.

                Returns:
                    The resulting ``p.Result[bool]``.

                """
                ...

            def configure_port(
                self,
                server: FlextGrpcProtocols.Grpc.GrpcServer,
                host: str,
                port: int,
                *,
                secure: bool = False,
            ) -> p.Result[int]:
                """Configure the server port binding.

                Args:
                    server: Server to bind.
                    host: Host address to bind.
                    port: Port number to bind.
                    secure: Whether to bind a secure port.

                Returns:
                    The resulting ``p.Result[int]``.

                """
                ...

            def server_status(self) -> p.Result[t.JsonValue | None]:
                """Get gRPC server status information.

                Returns:
                    The resulting ``p.Result[t.JsonValue | None]``.

                """
                ...

            def start_server(
                self,
                host: str,
                port: int,
                services: t.SequenceOf[FlextGrpcProtocols.Grpc.GrpcServicer]
                | None = None,
            ) -> p.Result[FlextGrpcProtocols.Grpc.GrpcServer]:
                """Start gRPC server.

                Args:
                    host: Host address to bind.
                    port: Port number to bind.
                    services: Optional servicers to register before starting.

                Returns:
                    The resulting ``p.Result[FlextGrpcProtocols.Grpc.GrpcServer]``.

                """
                ...

            def stop_server(self, *, grace_period: float = 30.0) -> p.Result[bool]:
                """Stop gRPC server.

                Args:
                    grace_period: Grace period in seconds for in-flight RPCs.

                Returns:
                    The resulting ``p.Result[bool]``.

                """
                ...

        @runtime_checkable
        class GrpcMessage(Protocol):
            """Protocol for gRPC message objects (duck typing for protobuf messages)."""

        @runtime_checkable
        class Client(Protocol):
            """Protocol for gRPC client communication operations."""

            def connect_client(
                self,
                target: str,
                *,
                timeout: float = 30.0,
            ) -> p.Result[FlextGrpcProtocols.Grpc.GrpcChannel]:
                """Connect gRPC client to server.

                Args:
                    target: gRPC server target address.
                    timeout: Connection timeout in seconds.

                Returns:
                    The resulting ``p.Result[FlextGrpcProtocols.Grpc.GrpcChannel]``.

                """
                ...

            def disconnect_client(
                self,
                channel: FlextGrpcProtocols.Grpc.GrpcChannel,
            ) -> p.Result[bool]:
                """Disconnect gRPC client.

                Args:
                    channel: Channel to close.

                Returns:
                    The resulting ``p.Result[bool]``.

                """
                ...

            def client_status(
                self,
                channel: FlextGrpcProtocols.Grpc.GrpcChannel,
            ) -> p.Result[t.JsonValue | None]:
                """Get gRPC client status information.

                Args:
                    channel: Channel to inspect.

                Returns:
                    The resulting ``p.Result[t.JsonValue | None]``.

                """
                ...

            def make_call(
                self,
                channel: FlextGrpcProtocols.Grpc.GrpcChannel,
                method: c.Grpc.GrpcOperations | str,
                request: FlextGrpcProtocols.Grpc.GrpcMessage,
                *,
                timeout: float = 30.0,
            ) -> p.Result[FlextGrpcProtocols.Grpc.GrpcMessage]:
                """Make gRPC method call.

                Args:
                    channel: Channel used for the call.
                    method: RPC operation or method name.
                    request: Request message.
                    timeout: Call timeout in seconds.

                Returns:
                    The resulting ``p.Result[FlextGrpcProtocols.Grpc.GrpcMessage]``.

                """
                ...

            def validate_connection(
                self,
                channel: FlextGrpcProtocols.Grpc.GrpcChannel,
            ) -> p.Result[bool]:
                """Validate gRPC client connection.

                Args:
                    channel: Channel to validate.

                Returns:
                    The resulting ``p.Result[bool]``.

                """
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
                """Close gRPC stream.

                Args:
                    stream: Stream to close.

                Returns:
                    The resulting ``p.Result[bool]``.

                """
                ...

            def create_stream(
                self,
                stream_type: c.Grpc.GrpcOperations | str,
                channel: FlextGrpcProtocols.Grpc.GrpcChannel,
                method: str,
            ) -> p.Result[FlextGrpcProtocols.Grpc.GrpcStream]:
                """Create gRPC stream.

                Args:
                    stream_type: Stream communication pattern.
                    channel: Channel carrying the stream.
                    method: RPC method name backing the stream.

                Returns:
                    The resulting ``p.Result[FlextGrpcProtocols.Grpc.GrpcStream]``.

                """
                ...

            def handle_bidirectional_streaming(
                self,
                stream: FlextGrpcProtocols.Grpc.GrpcStream,
            ) -> p.Result[t.JsonValue | None]:
                """Handle bidirectional streaming.

                Args:
                    stream: Stream to process.

                Returns:
                    The resulting ``p.Result[t.JsonValue | None]``.

                """
                ...

            def handle_client_streaming(
                self,
                stream: FlextGrpcProtocols.Grpc.GrpcStream,
                data_list: t.SequenceOf[FlextGrpcProtocols.Grpc.GrpcMessage],
            ) -> p.Result[FlextGrpcProtocols.Grpc.GrpcMessage]:
                """Handle client-side streaming.

                Args:
                    stream: Stream receiving the client messages.
                    data_list: Messages sent by the client.

                Returns:
                    The resulting ``p.Result[FlextGrpcProtocols.Grpc.GrpcMessage]``.

                """
                ...

            def handle_server_streaming(
                self,
                stream: FlextGrpcProtocols.Grpc.GrpcStream,
                request: FlextGrpcProtocols.Grpc.GrpcMessage,
            ) -> p.Result[Sequence[FlextGrpcProtocols.Grpc.GrpcMessage]]:
                """Handle server-side streaming.

                Args:
                    stream: Stream carrying the server messages.
                    request: Request message that starts the stream.

                Returns:
                    The resulting ``p.Result[Sequence[
                        FlextGrpcProtocols.Grpc.GrpcMessage
                    ]]``.

                """
                ...

            def send_data(
                self,
                stream: FlextGrpcProtocols.Grpc.GrpcStream,
                data: FlextGrpcProtocols.Grpc.GrpcMessage,
            ) -> p.Result[bool]:
                """Send data through gRPC stream.

                Args:
                    stream: Stream receiving the data.
                    data: Message to send.

                Returns:
                    The resulting ``p.Result[bool]``.

                """
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
                """Create gRPC service definition.

                Args:
                    service_name: Service name identifier.
                    methods: Method handlers keyed by method name.

                Returns:
                    The resulting ``p.Result[FlextGrpcProtocols.Grpc.GrpcServicer]``.

                """
                ...

            def service_methods(
                self,
                service: FlextGrpcProtocols.Grpc.GrpcServicer,
            ) -> p.Result[t.StrSequence]:
                """Get list of service methods.

                Args:
                    service: Servicer to inspect.

                Returns:
                    The resulting ``p.Result[t.StrSequence]``.

                """
                ...

            def register_service(
                self,
                service: FlextGrpcProtocols.Grpc.GrpcServicer,
                server: FlextGrpcProtocols.Grpc.GrpcServer,
            ) -> p.Result[bool]:
                """Register gRPC service with server.

                Args:
                    service: Servicer to register.
                    server: Server receiving the registration.

                Returns:
                    The resulting ``p.Result[bool]``.

                """
                ...

            def validate_service(
                self,
                service: FlextGrpcProtocols.Grpc.GrpcServicer,
            ) -> p.Result[bool]:
                """Validate gRPC service definition.

                Args:
                    service: Servicer to validate.

                Returns:
                    The resulting ``p.Result[bool]``.

                """
                ...

        @runtime_checkable
        class Channel(Protocol):
            """Protocol for gRPC channel management operations."""

            def close_channel(
                self,
                channel: FlextGrpcProtocols.Grpc.GrpcChannel,
            ) -> p.Result[bool]:
                """Close gRPC channel.

                Args:
                    channel: Channel to close.

                Returns:
                    The resulting ``p.Result[bool]``.

                """
                ...

            def create_channel(
                self,
                target: str,
                options: t.MappingKV[str, t.JsonValue | None] | None = None,
            ) -> p.Result[FlextGrpcProtocols.Grpc.GrpcChannel]:
                """Create gRPC channel.

                Args:
                    target: gRPC server target address.
                    options: Optional channel options keyed by name.

                Returns:
                    The resulting ``p.Result[FlextGrpcProtocols.Grpc.GrpcChannel]``.

                """
                ...

            def channel_state(
                self,
                channel: FlextGrpcProtocols.Grpc.GrpcChannel,
            ) -> p.Result[str]:
                """Get gRPC channel connection state.

                Args:
                    channel: Channel to inspect.

                Returns:
                    The resulting ``p.Result[str]``.

                """
                ...

            def wait_for_state_change(
                self,
                channel: FlextGrpcProtocols.Grpc.GrpcChannel,
                last_state: str,
                *,
                timeout: float = 30.0,
            ) -> p.Result[bool]:
                """Wait for channel state change.

                Args:
                    channel: Channel to observe.
                    last_state: Previously observed state name.
                    timeout: Maximum wait in seconds.

                Returns:
                    The resulting ``p.Result[bool]``.

                """
                ...

        @runtime_checkable
        class Metrics(Protocol):
            """Protocol for gRPC metrics collection and monitoring."""

            def collect_client_metrics(
                self,
                channel: FlextGrpcProtocols.Grpc.GrpcChannel,
            ) -> p.Result[Mapping[str, t.Numeric | str]]:
                """Collect gRPC client metrics.

                Args:
                    channel: Channel to measure.

                Returns:
                    The resulting ``p.Result[Mapping[str, t.Numeric | str]]``.

                """
                ...

            def collect_server_metrics(
                self,
                server: FlextGrpcProtocols.Grpc.GrpcServer,
            ) -> p.Result[Mapping[str, t.Numeric | str]]:
                """Collect gRPC server metrics.

                Args:
                    server: Server to measure.

                Returns:
                    The resulting ``p.Result[Mapping[str, t.Numeric | str]]``.

                """
                ...

            def collect_stream_metrics(
                self,
                stream: FlextGrpcProtocols.Grpc.GrpcStream,
            ) -> p.Result[Mapping[str, t.Numeric | str]]:
                """Collect gRPC stream metrics.

                Args:
                    stream: Stream to measure.

                Returns:
                    The resulting ``p.Result[Mapping[str, t.Numeric | str]]``.

                """
                ...

            def global_metrics(self) -> p.Result[Mapping[str, t.Numeric | str]]:
                """Get global gRPC metrics.

                Returns:
                    The resulting ``p.Result[Mapping[str, t.Numeric | str]]``.

                """
                ...

            def start_metrics_collection(
                self,
                *,
                interval: float = 60.0,
            ) -> p.Result[bool]:
                """Start automatic metrics collection.

                Args:
                    interval: Collection interval in seconds.

                Returns:
                    The resulting ``p.Result[bool]``.

                """
                ...

            def stop_metrics_collection(self) -> p.Result[bool]:
                """Stop automatic metrics collection.

                Returns:
                    The resulting ``p.Result[bool]``.

                """
                ...

        @runtime_checkable
        class Configuration(Protocol):
            """Protocol for gRPC configuration management."""

            def create_client_config(
                self,
                target: str,
                options: t.MappingKV[str, t.JsonValue | None] | None = None,
            ) -> p.Result[t.ScalarMapping]:
                """Create gRPC client configuration.

                Args:
                    target: gRPC server target address.
                    options: Optional client options keyed by name.

                Returns:
                    The resulting ``p.Result[t.ScalarMapping]``.

                """
                ...

            def create_server_config(
                self,
                host: str,
                port: int,
                options: t.MappingKV[str, t.JsonValue | None] | None = None,
            ) -> p.Result[t.ScalarMapping]:
                """Create gRPC server configuration.

                Args:
                    host: Server bind host address.
                    port: Server listen port number.
                    options: Optional server options keyed by name.

                Returns:
                    The resulting ``p.Result[t.ScalarMapping]``.

                """
                ...

            def parse_address(self, address: str) -> p.Result[tuple[str, int]]:
                """Parse gRPC address string.

                Args:
                    address: Address in the form ``host:port``.

                Returns:
                    The resulting ``p.Result[tuple[str, int]]``.

                """
                ...

            def validate_address(self, address: str) -> p.Result[bool]:
                """Validate gRPC address format.

                Args:
                    address: Address candidate.

                Returns:
                    The resulting ``p.Result[bool]``.

                """
                ...

            def validate_config(self) -> p.Result[bool]:
                """Validate gRPC configuration.

                Returns:
                    The resulting ``p.Result[bool]``.

                """
                ...

        @runtime_checkable
        class GrpcResource(Protocol):
            """Protocol for gRPC resource objects (channels, servers, streams)."""

        @runtime_checkable
        class ResourceManager(Protocol):
            """Protocol for gRPC resource management operations."""

            def acquire(self) -> p.Result[FlextGrpcProtocols.Grpc.GrpcResource]:
                """Acquire a resource.

                Returns:
                    The resulting ``p.Result[FlextGrpcProtocols.Grpc.GrpcResource]``.

                """
                ...

            def cleanup(self) -> p.Result[bool]:
                """Cleanup all resources.

                Returns:
                    The resulting ``p.Result[bool]``.

                """
                ...

            def release(
                self,
                resource: FlextGrpcProtocols.Grpc.GrpcResource,
            ) -> p.Result[bool]:
                """Release a resource.

                Args:
                    resource: Resource to release.

                Returns:
                    The resulting ``p.Result[bool]``.

                """
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

            def unsubscribe(self, callback: Callable[..., None]) -> None:
                """Remove a subscription callback from the channel.

                Args:
                    callback: Callback previously registered on the channel.

                """
                ...

        @runtime_checkable
        class GrpcRpcHandler(Protocol):
            """Protocol for gRPC RPC handlers."""

        @runtime_checkable
        class GrpcReadyFuture(Protocol):
            """Protocol for gRPC ready futures."""

            def result(self, timeout: float | None = None) -> None:
                """Wait until the underlying operation is ready.

                Args:
                    timeout: Maximum wait in seconds, or ``None`` to wait indefinitely.

                """
                ...

            def cancel(self) -> bool:
                """Release the channel subscription when readiness ends.

                Returns:
                    ``True`` when the pending readiness attempt was cancelled.

                """
                ...

        @runtime_checkable
        class GrpcServer(Protocol):
            """Protocol for gRPC server operations (duck typing for grpc.Server)."""

            def add_insecure_port(self, address: str) -> int:
                """Bind the server to an insecure address.

                Args:
                    address: Address in the form ``host:port``.

                Returns:
                    Bound port number.

                """
                ...

            def add_generic_rpc_handlers(
                self,
                generic_rpc_handlers: Iterable[FlextGrpcProtocols.Grpc.GrpcRpcHandler],
            ) -> None:
                """Add generic RPC handlers.

                Args:
                    generic_rpc_handlers: Handlers dispatching the RPC methods.

                """
                ...

            def start(self) -> None:
                """Start the server."""
                ...

            def stop(self, grace: float | None) -> threading.Event:
                """Stop the server with optional grace period.

                Args:
                    grace: Grace period in seconds, or ``None`` for immediate stop.

                Returns:
                    Event signalling full shutdown.

                """
                ...

        @runtime_checkable
        class GrpcServicerContext(Protocol):
            """Protocol for the per-RPC servicer context (grpc.ServicerContext)."""

            def peer(self) -> str:
                """Return the address of the calling peer.

                Returns:
                    Peer address string.

                """
                ...

        @runtime_checkable
        class GrpcStub(Protocol):
            """Protocol for gRPC client stub (duck typing for grpc stubs)."""

            def __init__(self, channel: FlextGrpcProtocols.Grpc.GrpcChannel) -> None:
                """Initialize the stub with a channel."""
                ...

        @runtime_checkable
        class GrpcChannelCredentials(Protocol):
            """Protocol for gRPC channel credentials.

            Duck typing for ``grpc.ChannelCredentials``.
            """

        @runtime_checkable
        class GrpcCallFailure(Protocol):
            """Protocol for gRPC call failures exposing status details."""

            def code(self) -> str | None:
                """Return the gRPC status code, if available.

                Returns:
                    Status code string, or ``None`` when unavailable.

                """
                ...

            def details(self) -> str:
                """Return the gRPC status details.

                Returns:
                    Status details string.

                """
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
                """Create an insecure channel for a target.

                Args:
                    target: gRPC server target address.

                Returns:
                    The created channel.

                """
                ...

            def channel_ready_future(
                self,
                channel: FlextGrpcProtocols.Grpc.GrpcChannel,
            ) -> FlextGrpcProtocols.Grpc.GrpcReadyFuture:
                """Create a future used to wait for channel readiness.

                Args:
                    channel: Channel whose readiness is awaited.

                Returns:
                    The readiness future.

                """
                ...

            def server(
                self,
                thread_pool: Executor,
            ) -> FlextGrpcProtocols.Grpc.GrpcServer:
                """Create a gRPC server using the given thread pool.

                Args:
                    thread_pool: Executor servicing RPC handlers.

                Returns:
                    The created server.

                """
                ...

        @runtime_checkable
        class EntityFactory(Protocol):
            """Protocol for entity factory callables."""

            def __call__(
                self,
                **kwargs: t.Scalar,
            ) -> p.Result[FlextGrpcProtocols.Grpc.GrpcResource]:
                """Create entity with given arguments.

                Args:
                    **kwargs: Field values applied to the entity.

                Returns:
                    The resulting ``p.Result[FlextGrpcProtocols.Grpc.GrpcResource]``.

                """
                ...

        @runtime_checkable
        class OperationHandler(Protocol):
            """Protocol for operation handler callables."""

            def __call__(
                self,
                **kwargs: t.Scalar,
            ) -> p.Result[FlextGrpcProtocols.Grpc.GrpcResource]:
                """Execute operation with given arguments.

                Args:
                    **kwargs: Operation arguments.

                Returns:
                    The resulting ``p.Result[FlextGrpcProtocols.Grpc.GrpcResource]``.

                """
                ...


p = FlextGrpcProtocols

__all__: list[str] = ["FlextGrpcProtocols", "p"]
