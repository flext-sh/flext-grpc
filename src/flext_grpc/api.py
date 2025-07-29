"""FLEXT gRPC API - Unified API for all gRPC operations.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Single API module consolidating all gRPC functionality.
"""

from __future__ import annotations

import re
from datetime import UTC, datetime

from flext_core import FlextResult
from flext_core.utilities import FlextGenerators

from flext_grpc.config import FlextGrpcConfig
from flext_grpc.entities import (
    FlextGrpcChannel,
    FlextGrpcClient,
    FlextGrpcServer,
    FlextGrpcService as FlextGrpcServiceEntity,
    FlextGrpcStream,
)
from flext_grpc.types import TGrpcTarget

# Constants for validation
MIN_PORT = 1
MAX_PORT = 65535
ADDRESS_PARTS_COUNT = 2


def create_server(
    host: str = "localhost",
    port: int = 50051,
    max_workers: int = 10,
) -> FlextGrpcServer:
    """Create a new gRPC server."""
    return FlextGrpcServer(
        id=FlextGenerators.generate_entity_id(),
        host=host,
        port=port,
        max_workers=max_workers,
        state="stopped",
        services=[],
        created_at=datetime.now(UTC),
    )


def create_client(
    target: str,
    options: dict[str, object] | None = None,
) -> FlextGrpcClient:
    """Create a new gRPC client."""
    channel = create_channel(target, options)

    return FlextGrpcClient(
        id=FlextGenerators.generate_entity_id(),
        channel=channel,
        options=options or {},
        created_at=datetime.now(UTC),
    )


def create_channel(
    target: str,
    options: dict[str, object] | None = None,
) -> FlextGrpcChannel:
    """Create a new gRPC channel."""
    return FlextGrpcChannel(
        id=FlextGenerators.generate_entity_id(),
        target=TGrpcTarget(target),
        state="idle",
        options=options or {},
        created_at=datetime.now(UTC),
    )


def create_service(
    name: str,
    methods: list[str] | None = None,
) -> FlextGrpcServiceEntity:
    """Create a new gRPC service."""
    return FlextGrpcServiceEntity(
        id=FlextGenerators.generate_entity_id(),
        name=name,
        methods=methods or [],
        created_at=datetime.now(UTC),
    )


def create_stream(
    method_name: str,
    stream_type: str = "unary",
) -> FlextGrpcStream:
    """Create a new gRPC stream."""
    return FlextGrpcStream(
        id=FlextGenerators.generate_entity_id(),
        method_name=method_name,
        stream_type=stream_type,
        created_at=datetime.now(UTC),
    )


def create_config(
    host: str = "localhost",
    port: int = 50051,
    max_workers: int = 10,
    timeout: float = 30.0,
) -> FlextGrpcConfig:
    """Create a new gRPC configuration."""
    return FlextGrpcConfig(
        host=host,
        port=port,
        max_workers=max_workers,
        timeout=timeout,
    )


def validate_address(address: str) -> FlextResult[bool]:
    """Validate a gRPC address format."""
    try:
        # Validate basic address format
        validation_error = _validate_address_format(address)
        if validation_error:
            return FlextResult.fail(validation_error)

        # Parse and validate components
        host, port_str = address.split(":")
        validation_error = _validate_host_and_port(host, port_str)
        if validation_error:
            return FlextResult.fail(validation_error)

        return FlextResult.ok(value=True)

    except (ValueError, AttributeError) as e:
        return FlextResult.fail(f"Address validation error: {e}")


def _validate_address_format(address: str) -> str | None:
    """Validate basic address format. Returns error message or None."""
    if not address:
        return "Address cannot be empty"

    if ":" not in address:
        return "Address must be in host:port format"

    parts = address.split(":")
    if len(parts) != ADDRESS_PARTS_COUNT:
        return "Address must be in host:port format"

    return None


def _validate_host_and_port(host: str, port_str: str) -> str | None:
    """Validate host and port components. Returns error message or None."""
    if not host:
        return "Host cannot be empty"

    if not re.match(r"^[a-zA-Z0-9.-]+$", host):
        return "Invalid host format"

    try:
        port = int(port_str)
        if not (MIN_PORT <= port <= MAX_PORT):
            return f"Port must be between {MIN_PORT} and {MAX_PORT}"
    except ValueError:
        return "Port must be a number"

    return None


def parse_address(address: str) -> dict[str, int | str]:
    """Parse a gRPC address into components."""
    validation_result = validate_address(address)
    if not validation_result.is_success:
        raise ValueError(validation_result.error)

    host, port_str = address.split(":")
    return {
        "host": host,
        "port": int(port_str),
    }


def create_complete_setup(
    host: str = "localhost",
    port: int = 50051,
    service_name: str = "DefaultService",
    methods: list[str] | None = None,
) -> dict[str, FlextGrpcServer | FlextGrpcClient | FlextGrpcServiceEntity | str]:
    """Create a complete gRPC setup with server, client and service."""
    server = create_server(host=host, port=port)
    target = f"{host}:{port}"
    client = create_client(target=target)
    service = create_service(name=service_name, methods=methods)

    return {
        "server": server,
        "client": client,
        "service": service,
        "target": target,
    }
