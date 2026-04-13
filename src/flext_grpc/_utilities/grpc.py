"""Internal gRPC utility mixin with typed entity factories."""

from __future__ import annotations

import logging
import os
import re
import socket
from uuid import uuid4

from flext_core import p, r
from flext_grpc import c, m, t

logger = logging.getLogger(__name__)


class FlextGrpcUtilitiesGrpc:
    """gRPC utility namespace composed into ``FlextGrpcUtilities.Grpc``."""

    @staticmethod
    def create_channel_entity(
        target: str,
        options: t.OptionalContainerValueMapping | None = None,
    ) -> p.Result[m.Grpc.Channel]:
        """Create a typed channel entity from validated inputs."""
        resolved_options = {} if options is None else dict(options)
        return r[m.Grpc.Channel].create_from_callable(
            lambda: m.Grpc.Channel(
                target=target,
                options=resolved_options,
            ),
        )

    @staticmethod
    def create_client_entity(
        target: str,
        options: t.OptionalContainerValueMapping | None = None,
    ) -> p.Result[m.Grpc.Client]:
        """Create a typed client entity backed by a typed channel entity."""
        resolved_options = {} if options is None else dict(options)
        channel_result = FlextGrpcUtilitiesGrpc.create_channel_entity(
            target=target,
            options=resolved_options,
        )
        if channel_result.failure:
            return r[m.Grpc.Client].fail(
                channel_result.error or "Client channel creation failed",
            )
        return r[m.Grpc.Client].create_from_callable(
            lambda: m.Grpc.Client(
                channel=channel_result.value,
                options=resolved_options,
            ),
        )

    @staticmethod
    def create_server_entity(
        host: str = c.Grpc.GrpcNetwork.DEFAULT_HOST,
        port: int = c.Grpc.GrpcNetwork.DEFAULT_GRPC_PORT,
        max_workers: int = c.Grpc.Service.DEFAULT_MAX_WORKERS,
    ) -> p.Result[m.Grpc.Server]:
        """Create a typed server entity from validated inputs."""
        return r[m.Grpc.Server].create_from_callable(
            lambda: m.Grpc.Server(
                host=host,
                port=port,
                max_workers=max_workers,
            ),
        )

    @staticmethod
    def create_service_entity(
        name: str,
        methods: t.StrSequence | None = None,
    ) -> p.Result[m.Grpc.Service]:
        """Create a typed service entity with a minimal valid method set."""
        resolved_methods = ["HealthCheck"] if methods is None else list(methods)
        return r[m.Grpc.Service].create_from_callable(
            lambda: m.Grpc.Service(
                name=name,
                methods=resolved_methods,
            ),
        )

    @staticmethod
    def create_stream_entity(
        method_name: str,
        stream_type: c.Grpc.GrpcOperations | str,
    ) -> p.Result[m.Grpc.GrpcStream]:
        """Create a typed stream entity from validated inputs."""
        resolved_stream_type = c.Grpc.GrpcOperations(stream_type)
        return r[m.Grpc.GrpcStream].create_from_callable(
            lambda: m.Grpc.GrpcStream(
                id=str(uuid4()),
                method_name=method_name,
                stream_type=resolved_stream_type,
            ),
        )

    @staticmethod
    def format_address(host: str, port: int) -> str:
        """Format host and port as a gRPC target string."""
        return f"{host}:{port}"

    @staticmethod
    def channel_state_name(
        state: c.Grpc.ChannelState | str,
    ) -> str:
        """Return the channel state name as its canonical string value."""
        if isinstance(state, c.Grpc.ChannelState):
            return state.value
        return str(state)

    @staticmethod
    def server_state_name(
        state: c.Grpc.ServerState | str,
    ) -> str:
        """Return the server state name as its canonical string value."""
        if isinstance(state, c.Grpc.ServerState):
            return state.value
        return str(state)

    @staticmethod
    def system_info() -> dict[str, t.ContainerValue]:
        """Return a small typed runtime snapshot for gRPC diagnostics."""
        return {
            "default_host": c.Grpc.GrpcNetwork.DEFAULT_HOST,
            "default_port": c.Grpc.GrpcNetwork.DEFAULT_GRPC_PORT,
            "hostname": socket.gethostname(),
            "pid": os.getpid(),
        }

    @staticmethod
    def parse_address(address: str) -> tuple[str, int]:
        """Parse a validated gRPC address into host and port."""
        return t.Grpc.GrpcValidation.parse_target(address)

    @staticmethod
    def validate_host(host: str) -> bool:
        """Validate a host token allowed by the gRPC target parser."""
        return bool(host) and re.fullmatch(r"[a-zA-Z0-9.-]+", host) is not None

    @staticmethod
    def validate_port(port: int) -> bool:
        """Validate that a port is within the canonical gRPC range."""
        return c.Grpc.GrpcNetwork.MIN_PORT <= port <= c.Grpc.GrpcNetwork.MAX_PORT

    @staticmethod
    def validate_target(target: str) -> bool:
        """Validate a gRPC target string in ``host:port`` format."""
        return t.Grpc.GrpcValidation.validate_target(target)


__all__: list[str] = ["FlextGrpcUtilitiesGrpc"]
