"""gRPC service, configuration and metrics protocol contracts.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

from flext_grpc._protocols.channel_protocols import GrpcChannel
from flext_grpc._protocols.server_protocols import GrpcServer, GrpcServicer
from flext_grpc._protocols.stream_protocols import GrpcStream

if TYPE_CHECKING:
    from collections.abc import Mapping

    from flext_grpc import p, t


@runtime_checkable
class GrpcMethodHandler(Protocol):
    """Protocol for gRPC method handlers (duck typing)."""


@runtime_checkable
class Service(Protocol):
    """Protocol for gRPC service definition and management."""

    def create_service(
        self,
        service_name: str,
        methods: t.MappingKV[str, GrpcMethodHandler],
    ) -> p.Result[GrpcServicer]:
        """Create gRPC service definition.

        Args:
            service_name: Service name identifier.
            methods: Method handlers keyed by method name.

        Returns:
            The resulting ``p.Result[GrpcServicer]``.

        """
        ...

    def service_methods(
        self,
        service: GrpcServicer,
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
        service: GrpcServicer,
        server: GrpcServer,
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
        service: GrpcServicer,
    ) -> p.Result[bool]:
        """Validate gRPC service definition.

        Args:
            service: Servicer to validate.

        Returns:
            The resulting ``p.Result[bool]``.

        """
        ...


@runtime_checkable
class Metrics(Protocol):
    """Protocol for gRPC metrics collection and monitoring."""

    def collect_client_metrics(
        self,
        channel: GrpcChannel,
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
        server: GrpcServer,
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
        stream: GrpcStream,
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


__all__: list[str] = [
    "Configuration",
    "GrpcMethodHandler",
    "Metrics",
    "Service",
]
