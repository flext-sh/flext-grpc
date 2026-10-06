"""Internal gRPC utility mixin with typed entity factories.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from uuid import uuid4

from flext_core import r
from flext_grpc import c, m, p, t


class FlextGrpcUtilitiesGrpc:
    """Typed gRPC entity factories and runtime-bound utility namespace."""

    @staticmethod
    def create_channel_entity(
        target: str,
        options: t.JsonMapping | None = None,
    ) -> p.Result[m.Grpc.Channel]:
        """Create a typed channel entity from validated inputs.

        Returns:
            The resulting ``p.Result[m.Grpc.Channel]``.
        """
        resolved_options = {} if options is None else dict(options)

        def _build_channel() -> m.Grpc.Channel:
            return m.Grpc.Channel(target=target, options=resolved_options)

        return r[m.Grpc.Channel].create_from_callable(_build_channel)

    @staticmethod
    def create_client_entity(
        target: str,
        options: t.JsonMapping | None = None,
    ) -> p.Result[m.Grpc.Client]:
        """Create a typed client entity backed by a typed channel entity.

        Returns:
            The resulting ``p.Result[m.Grpc.Client]``.
        """
        resolved_options = {} if options is None else dict(options)
        channel_result = FlextGrpcUtilitiesGrpc.create_channel_entity(
            target=target,
            options=resolved_options,
        )
        if channel_result.failure:
            return r[m.Grpc.Client].from_failure(channel_result)

        def _build_client() -> m.Grpc.Client:
            return m.Grpc.Client(channel=channel_result.value, options=resolved_options)

        return r[m.Grpc.Client].create_from_callable(_build_client)

    @staticmethod
    def create_server_entity(
        host: str = c.Grpc.NETWORK_DEFAULT_HOST,
        port: int = c.Grpc.NETWORK_DEFAULT_GRPC_PORT,
        max_workers: int = c.Grpc.SERVICE_DEFAULT_MAX_WORKERS,
    ) -> p.Result[m.Grpc.Server]:
        """Create a typed server entity from validated inputs.

        Returns:
            The resulting ``p.Result[m.Grpc.Server]``.
        """

        def _build_server() -> m.Grpc.Server:
            return m.Grpc.Server(host=host, port=port, max_workers=max_workers)

        return r[m.Grpc.Server].create_from_callable(_build_server)

    @staticmethod
    def create_service_entity(
        name: str,
        methods: t.StrSequence | None = None,
    ) -> p.Result[m.Grpc.Service]:
        """Create a typed service entity with a minimal valid method set.

        Returns:
            The resulting ``p.Result[m.Grpc.Service]``.
        """
        resolved_methods = ["HealthCheck"] if methods is None else list(methods)

        def _build_service() -> m.Grpc.Service:
            return m.Grpc.Service(name=name, methods=resolved_methods)

        return r[m.Grpc.Service].create_from_callable(_build_service)

    @staticmethod
    def create_stream_entity(
        method_name: str,
        stream_type: c.Grpc.GrpcOperations | str,
    ) -> p.Result[m.Grpc.GrpcStream]:
        """Create a typed stream entity from validated inputs.

        Returns:
            The resulting ``p.Result[m.Grpc.GrpcStream]``.
        """
        resolved_stream_type = c.Grpc.GrpcOperations(stream_type)

        def _build_stream() -> m.Grpc.GrpcStream:
            return m.Grpc.GrpcStream(
                id=str(uuid4()),
                method_name=method_name,
                stream_type=resolved_stream_type,
            )

        return r[m.Grpc.GrpcStream].create_from_callable(_build_stream)

    @staticmethod
    def parse_address(address: str) -> tuple[str, int]:
        """Parse a validated gRPC address into host and port.

        Returns:
            The resulting ``tuple[str, int]``.
        """
        return FlextGrpcUtilitiesGrpc.parse_target(address)

    @staticmethod
    def parse_target(target: str) -> tuple[str, int]:
        """Parse a validated gRPC target into (host, port).

        Returns:
            The resulting ``tuple[str, int]``.

        Raises:
            ValueError: If Invalid gRPC target.
        """
        if not FlextGrpcUtilitiesGrpc.validate_target(target):
            msg = f"Invalid gRPC target: {target}"
            raise ValueError(msg)
        host, port_str = target.split(":", 1)
        return (host, int(port_str))

    @staticmethod
    def validate_target(target: str) -> bool:
        """Validate a gRPC target string in the form host:port.

        Returns:
            The resulting ``bool``.
        """
        # Why: avoid an exception-driven sentinel branch (silent-failure gate);
        # port parsing is guarded by isdigit() instead of try/except ValueError.
        if not target or ":" not in target:
            return False
        host, port_str = target.split(":", 1)
        if not host or not port_str or not port_str.isdigit():
            return False
        if not c.Grpc.NETWORK_HOST_RE.match(host):
            return False
        max_port = 65535
        return 1 <= int(port_str) <= max_port

    @staticmethod
    def validate_port(port: int) -> bool:
        """Validate that a port is within the permitted gRPC range.

        Returns:
            The resulting ``bool``.
        """
        return c.Grpc.NETWORK_MIN_PORT <= port <= c.Grpc.NETWORK_MAX_PORT

    @staticmethod
    def validate_host(host: str) -> bool:
        """Validate that a host string is non-empty.

        Returns:
            The resulting ``bool``.
        """
        return bool(host and host.strip())

    @staticmethod
    def format_address(host: str, port: int) -> str:
        """Format a gRPC ``host:port`` address.

        Returns:
            The resulting ``str``.
        """
        return f"{host}:{port}"

    @staticmethod
    def channel_state_name(state: str) -> str:
        """Return a normalized channel state name."""
        normalized = state.lower()
        if normalized in c.Grpc.CHANNEL_STATES:
            return normalized
        return "unknown"

    @staticmethod
    def server_state_name(state: str) -> str:
        """Return a normalized server state name."""
        normalized = state.lower()
        if normalized in c.Grpc.SERVER_STATES:
            return normalized
        return "unknown"

    @staticmethod
    def system_info() -> t.JsonMapping:
        """Return gRPC utility system info."""
        channel_states: t.JsonValueList = list(c.Grpc.CHANNEL_STATES)
        server_states: t.JsonValueList = list(c.Grpc.SERVER_STATES)
        info: t.JsonMapping = {
            "default_host": c.Grpc.NETWORK_DEFAULT_HOST,
            "default_port": c.Grpc.NETWORK_DEFAULT_GRPC_PORT,
            "min_port": c.Grpc.NETWORK_MIN_PORT,
            "max_port": c.Grpc.NETWORK_MAX_PORT,
            "channel_states": channel_states,
            "server_states": server_states,
        }
        return info


__all__: list[str] = ["FlextGrpcUtilitiesGrpc"]
