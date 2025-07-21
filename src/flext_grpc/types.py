"""FLEXT gRPC types - Unified typing system using flext-core.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

This module imports from the unified typing system in flext-core and defines
gRPC-specific protocol types using modern Python 3.13 patterns and Pydantic v2.
Zero tolerance for mock implementations - real gRPC protocols only.
"""

from __future__ import annotations

from collections.abc import AsyncIterator, Callable, Sequence
from typing import Protocol, TypeVar

# Import from unified core typing system
from flext_core.domain.shared_types import (
    ConfigMapping,
    HandlerFunction,
)

# Type variables for generic gRPC protocols
TRequestContra_contra = TypeVar("TRequestContra_contra", contravariant=True)
TResponseCo_co = TypeVar("TResponseCo_co", covariant=True)
TServicer = TypeVar("TServicer")

# ==============================================================================
# GRPC SPECIFIC TYPES - Building on unified types
# ==============================================================================

# gRPC protocol types using modern Python 3.13 patterns
type GrpcMetadata = Sequence[tuple[str, str | bytes]]
type GrpcStatusCode = int  # grpc.StatusCode values are integers
type GrpcStatus = object  # grpc.Status object
type GrpcServerCredentials = object  # grpc.ServerCredentials object
type GrpcHandlerCallDetails = object  # grpc.HandlerCallDetails object
type GrpcContinuation = Callable[[object], object]
type GrpcServiceMethod = HandlerFunction[object, object]
type GrpcStreamingMethod = Callable[[AsyncIterator[object]], AsyncIterator[object]]


class ServicerContext(Protocol):
    """Protocol for gRPC servicer context.

    Provides interface for gRPC service context operations including
    authentication, metadata handling, and response control.
    """

    def abort(self, code: GrpcStatusCode, details: str = "") -> None:
        """Abort the RPC with a status code and details.

        Args:
            code: gRPC status code.
            details: Error details.

        """

    def abort_with_status(self, status: GrpcStatus) -> None:
        """Abort the RPC with a status object.

        Args:
            status: gRPC status object.

        """

    def auth_context(self) -> ConfigMapping:
        """Get authentication context.

        Returns:
            Authentication context mapping.

        """

    def peer(self) -> str:
        """Get peer address.

        Returns:
            Peer address string.

        """

    def peer_identities(self) -> Sequence[bytes] | None:
        """Get peer identities.

        Returns:
            Sequence of peer identity bytes or None.

        """

    def peer_identity_key(self) -> str | None:
        """Get peer identity key.

        Returns:
            Peer identity key or None.

        """

    def invocation_metadata(self) -> GrpcMetadata:
        """Get invocation metadata.

        Returns:
            gRPC metadata.

        """

    def send_initial_metadata(self, metadata: GrpcMetadata) -> None:
        """Send initial metadata.

        Args:
            metadata: Metadata to send.

        """

    def set_trailing_metadata(self, metadata: GrpcMetadata) -> None:
        """Set trailing metadata.

        Args:
            metadata: Trailing metadata to set.

        """

    def set_code(self, code: GrpcStatusCode) -> None:
        """Set response status code.

        Args:
            code: gRPC status code.

        """

    def set_details(self, details: str) -> None:
        """Set response details.

        Args:
            details: Response details.

        """


# ==============================================================================
# GRPC METHOD PROTOCOLS - Using modern Python 3.13 generic syntax
# ==============================================================================


class UnaryUnaryMethod[TRequest, TResponse](Protocol):
    """Protocol for unary-unary gRPC method.

    Defines the interface for gRPC methods that take a single request
    and return a single response using modern Python 3.13 generic syntax.
    """

    async def __call__(self, request: TRequest, context: ServicerContext) -> TResponse:
        """Call the unary-unary method.

        Args:
            request: The request message.
            context: The gRPC service context.

        Returns:
            The response message.

        """


class UnaryStreamMethod[TRequest, TResponse](Protocol):
    """Protocol for unary-stream gRPC method.

    Defines the interface for gRPC methods that take a single request
    and return a stream of responses using modern Python 3.13 patterns.
    """

    async def __call__(
        self,
        request: TRequest,
        context: ServicerContext,
    ) -> AsyncIterator[TResponse]:
        """Call the unary-stream method.

        Args:
            request: The request message.
            context: The gRPC service context.

        Returns:
            Async iterator of response messages.

        """


class StreamUnaryMethod[TRequest, TResponse](Protocol):
    """Protocol for stream-unary gRPC method.

    Defines the interface for gRPC methods that take a stream of requests
    and return a single response using composition patterns.
    """

    async def __call__(
        self,
        request_iterator: AsyncIterator[TRequest],
        context: ServicerContext,
    ) -> TResponse:
        """Call the stream-unary method.

        Args:
            request_iterator: Async iterator of request messages.
            context: The gRPC service context.

        Returns:
            The response message.

        """


class StreamStreamMethod[TRequest, TResponse](Protocol):
    """Protocol for stream-stream gRPC method.

    Defines the interface for gRPC methods that take a stream of requests
    and return a stream of responses using modern async patterns.
    """

    async def __call__(
        self,
        request_iterator: AsyncIterator[TRequest],
        context: ServicerContext,
    ) -> AsyncIterator[TResponse]:
        """Call the stream-stream method.

        Args:
            request_iterator: Async iterator of request messages.
            context: The gRPC service context.

        Returns:
            Async iterator of response messages.

        """


class GenericServicer:
    """Base protocol for gRPC servicers.

    Provides common interface for all gRPC service implementations.
    """

    def add_to_server(self, server: object) -> None:
        """Add this servicer to a gRPC server.

        Args:
            server: The gRPC server instance.

        """


class GrpcServer(Protocol):
    """Protocol for gRPC server.

    Defines the interface for gRPC server lifecycle management.
    """

    def add_servicer(self, servicer: GenericServicer) -> None:
        """Add a servicer to the server.

        Args:
            servicer: The servicer to add.

        """

    def add_insecure_port(self, address: str) -> int:
        """Add an insecure port to the server.

        Args:
            address: The address to bind to.

        Returns:
            The port number bound to.

        """

    def add_secure_port(self, address: str, credentials: GrpcServerCredentials) -> int:
        """Add a secure port to the server.

        Args:
            address: The address to bind to.
            credentials: Server credentials for TLS.

        Returns:
            The port number bound to.

        """

    async def start(self) -> None:
        """Start the server."""

    async def stop(self, grace: float | None = None) -> None:
        """Stop the server.

        Args:
            grace: Grace period for shutdown.

        """

    async def wait_for_termination(self) -> None:
        """Wait for server termination."""


class GrpcChannel(Protocol):
    """Protocol for gRPC channel.

    Defines the interface for gRPC client channels.
    """

    def close(self) -> None:
        """Close the channel."""

    def get_state(self, *, try_to_connect: bool = False) -> int:
        """Get channel state.

        Args:
            try_to_connect: Whether to try to connect.

        Returns:
            Channel state code.

        """


class GrpcInterceptor:
    """Protocol for gRPC interceptors.

    Defines the interface for gRPC request/response interceptors.
    """

    def intercept_service(
        self,
        continuation: GrpcContinuation,
        handler_call_details: GrpcHandlerCallDetails,
    ) -> object:
        """Intercept a service call.

        Args:
            continuation: The continuation function.
            handler_call_details: Details about the handler call.

        Returns:
            The intercepted result.

        """


# ==============================================================================
# EXPORTS - ALL GRPC TYPES
# ==============================================================================

__all__ = [
    # Core types from unified system
    "ConfigMapping",
    "GenericServicer",
    "GrpcChannel",
    "GrpcContinuation",
    "GrpcHandlerCallDetails",
    "GrpcInterceptor",
    "GrpcMetadata",
    "GrpcServer",
    "GrpcServerCredentials",
    "GrpcServiceMethod",
    "GrpcStatus",
    "GrpcStatusCode",
    "GrpcStreamingMethod",
    "HandlerFunction",
    "ServicerContext",
    "StreamStreamMethod",
    "StreamUnaryMethod",
    "TRequestContra_contra",
    "TResponseCo_co",
    "TServicer",
    "UnaryStreamMethod",
    "UnaryUnaryMethod",
]
