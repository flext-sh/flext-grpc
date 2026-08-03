"""FLEXT gRPC utilities facade."""

from __future__ import annotations

from typing import override

from flext_cli import u
from flext_grpc import c, m, p, t
from flext_grpc._utilities.grpc import FlextGrpcUtilitiesGrpc


class FlextGrpcUtilities(u, FlextGrpcUtilitiesGrpc):
    """Utilities for gRPC operations in the FLEXT ecosystem."""

    class Grpc(FlextGrpcUtilitiesGrpc):
        """Public gRPC utility namespace with explicit local signatures.

        This nested class re-exports the factory/validation helpers from
        ``FlextGrpcUtilitiesGrpc`` so that static type checkers see concrete
        return types for ``u.Grpc.*`` calls inside ``flext_grpc`` services.
        """

        @override
        @staticmethod
        def create_channel_entity(
            target: str, options: t.JsonMapping | None = None
        ) -> p.Result[m.Grpc.Channel]:
            """Create a typed channel entity from validated inputs."""
            return FlextGrpcUtilitiesGrpc.create_channel_entity(
                target=target, options=options
            )

        @override
        @staticmethod
        def create_client_entity(
            target: str, options: t.JsonMapping | None = None
        ) -> p.Result[m.Grpc.Client]:
            """Create a typed client entity backed by a typed channel entity."""
            return FlextGrpcUtilitiesGrpc.create_client_entity(
                target=target, options=options
            )

        @override
        @staticmethod
        def create_server_entity(
            host: str = c.Grpc.NETWORK_DEFAULT_HOST,
            port: int = c.Grpc.NETWORK_DEFAULT_GRPC_PORT,
            max_workers: int = c.Grpc.SERVICE_DEFAULT_MAX_WORKERS,
        ) -> p.Result[m.Grpc.Server]:
            """Create a typed server entity from validated inputs."""
            return FlextGrpcUtilitiesGrpc.create_server_entity(
                host=host, port=port, max_workers=max_workers
            )

        @override
        @staticmethod
        def create_service_entity(
            name: str, methods: t.StrSequence | None = None
        ) -> p.Result[m.Grpc.Service]:
            """Create a typed service entity with a minimal valid method set."""
            return FlextGrpcUtilitiesGrpc.create_service_entity(
                name=name, methods=methods
            )

        @override
        @staticmethod
        def create_stream_entity(
            method_name: str, stream_type: c.Grpc.GrpcOperations | str
        ) -> p.Result[m.Grpc.GrpcStream]:
            """Create a typed stream entity from validated inputs."""
            return FlextGrpcUtilitiesGrpc.create_stream_entity(
                method_name=method_name, stream_type=stream_type
            )

        @override
        @staticmethod
        def validate_target(target: str) -> bool:
            """Validate a gRPC target string in the form host:port."""
            return FlextGrpcUtilitiesGrpc.validate_target(target)


u = FlextGrpcUtilities

__all__: list[str] = ["FlextGrpcUtilities", "u"]
