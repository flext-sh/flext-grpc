"""FLEXT gRPC Utilities - Essential utilities for gRPC operations.

Simplified utilities module containing only actively used methods.
Follows FLEXT standards with minimal, focused functionality.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping
from typing import TypeGuard
from uuid import uuid4

import grpc
import psutil
from flext_core import FlextUtilities, r
from google.protobuf.message import Message

from flext_grpc import FlextGrpcConstants, FlextGrpcModels, c, t

GrpcChannelType = grpc.Channel
PSUTIL_AVAILABLE = True
PROTOBUF_AVAILABLE = True
ProtobufMessage = Message
__all__ = ["FlextGrpcUtilities", "u"]


def _is_valid_stream_type(value: str) -> TypeGuard[c.Grpc.StreamTypeLiteral]:
    """Check if value is a valid stream type literal."""
    return value in c.Grpc.STREAM_TYPES


class FlextGrpcUtilities(FlextUtilities):
    """Utilities for gRPC operations in FLEXT ecosystem.

    Provides helper methods for gRPC channel, server, and stream management.
    Follows FLEXT patterns with minimal, focused functionality.
    """

    @classmethod
    def create_channel_entity(
        cls, target: str, options: Mapping[str, t.ContainerValue] | None = None
    ) -> r[FlextGrpcModels.Grpc.Channel]:
        """Create a gRPC channel entity directly."""
        try:
            if not target or not target.strip():
                return r.fail("Channel target cannot be empty")
            channel = FlextGrpcModels.Grpc.Channel(
                unique_id=str(uuid4()),
                target=target,
                state="idle",
                options=dict(options) if options else {},
            )
            return r.ok(channel)
        except (grpc.RpcError, ConnectionError, TimeoutError) as e:
            return r.fail(f"Failed to create channel entity: {e}")

    @classmethod
    def create_client_entity(
        cls, target: str, options: Mapping[str, t.ContainerValue] | None = None
    ) -> r[FlextGrpcModels.Grpc.Client]:
        """Create a gRPC client entity directly."""
        try:
            if not target or not target.strip():
                return r.fail("Client target cannot be empty")
            channel = FlextGrpcModels.Grpc.Channel(
                unique_id=str(uuid4()),
                target=target,
                state="idle",
                options=dict(options) if options else {},
            )
            client = FlextGrpcModels.Grpc.Client(
                unique_id=str(uuid4()), channel=channel
            )
            return r.ok(client)
        except (grpc.RpcError, ConnectionError, TimeoutError) as e:
            return r.fail(f"Failed to create client entity: {e}")

    @classmethod
    def create_server_entity(
        cls,
        host: str = c.Grpc.GrpcNetwork.DEFAULT_HOST,
        port: int = c.Grpc.GrpcNetwork.DEFAULT_GRPC_PORT,
        max_workers: int = c.Grpc.Service.DEFAULT_MAX_WORKERS,
    ) -> r[FlextGrpcModels.Grpc.Server]:
        """Create a gRPC server entity directly."""
        try:
            server = FlextGrpcModels.Grpc.Server(
                unique_id=str(uuid4()), host=host, port=port, max_workers=max_workers
            )
            return r.ok(server)
        except (grpc.RpcError, ConnectionError, TimeoutError) as e:
            return r.fail(f"Failed to create server entity: {e}")

    @classmethod
    def create_service_entity(
        cls, name: str, methods: list[str] | None = None
    ) -> r[FlextGrpcModels.Grpc.Service]:
        """Create a gRPC service entity directly."""
        try:
            if not name or not name.strip():
                return r.fail("Service name cannot be empty")
            service = FlextGrpcModels.Grpc.Service(
                unique_id=str(uuid4()),
                name=name,
                methods=["HealthCheck"] if methods is None else methods,
            )
            return r.ok(service)
        except (grpc.RpcError, ConnectionError, TimeoutError) as e:
            return r.fail(f"Failed to create service entity: {e}")

    @classmethod
    def create_stream_entity(
        cls,
        method_name: str,
        stream_type: FlextGrpcConstants.Grpc.StreamTypeLiteral | str,
    ) -> r[FlextGrpcModels.Grpc.GrpcStream]:
        """Create a gRPC stream entity directly."""
        try:
            if not _is_valid_stream_type(stream_type):
                return r.fail(f"Invalid stream type: {stream_type}")
            if not method_name or not method_name.strip():
                return r.fail("Stream method name cannot be empty")
            stream = FlextGrpcModels.Grpc.GrpcStream(
                unique_id=str(uuid4()), method_name=method_name, stream_type=stream_type
            )
            return r.ok(stream)
        except (grpc.RpcError, ConnectionError, TimeoutError) as e:
            return r.fail(f"Failed to create stream entity: {e}")

    class Grpc:
        """gRPC-specific utility methods."""

        @staticmethod
        def format_address(host: str, port: int) -> str:
            """Format host and port into gRPC address."""
            return f"{host}:{port}"

        @staticmethod
        def get_channel_state_name(state: str) -> str:
            """Get human-readable channel state name."""
            state_names = {
                "idle": "Idle",
                "connecting": "Connecting",
                "ready": "Ready",
                "transient_failure": "Transient Failure",
                "shutdown": "Shutdown",
            }
            return state_names.get(state, "Unknown")

        @staticmethod
        def get_server_state_name(state: str) -> str:
            """Get human-readable server state name."""
            state_names = {
                "stopped": "Stopped",
                "starting": "Starting",
                "running": "Running",
                "stopping": "Stopping",
            }
            return state_names.get(state, "Unknown")

        @staticmethod
        def get_stream_type_name(stream_type: str) -> str:
            """Get human-readable stream type name."""
            type_names = {
                "unary": "Unary",
                "server_streaming": "Server Streaming",
                "client_streaming": "Client Streaming",
                "bidirectional": "Bidirectional",
            }
            return type_names.get(stream_type, "Unknown")

        @staticmethod
        def get_system_info() -> dict[str, t.ContainerValue]:
            """Get system information for gRPC diagnostics."""
            cpu: int = 0
            mem_total: int = 0
            mem_avail: int = 0
            try:
                cpu_val = psutil.cpu_count()
                if cpu_val is not None:
                    cpu_str: str = str(cpu_val)
                    cpu = int(cpu_str) if cpu_str.isdigit() else 0
            except Exception:
                pass
            try:
                mem_val = psutil.virtual_memory()
                total_val: t.ContainerValue = getattr(mem_val, "total", 0)
                avail_val: t.ContainerValue = getattr(mem_val, "available", 0)
                mem_total = int(str(total_val)) if total_val else 0
                mem_avail = int(str(avail_val)) if avail_val else 0
            except Exception:
                pass
            return {
                "cpu_count": cpu,
                "memory_total_mb": mem_total // (1024 * 1024),
                "memory_available_mb": mem_avail // (1024 * 1024),
            }

        @staticmethod
        def parse_address(address: str) -> tuple[str, int] | None:
            """Parse gRPC address into host and port."""
            if not address or ":" not in address:
                return None
            try:
                parts = address.rsplit(":", 1)
                host = parts[0]
                port = int(parts[1])
                if (
                    not c.Grpc.GrpcNetwork.MIN_PORT
                    <= port
                    <= c.Grpc.GrpcNetwork.MAX_PORT
                ):
                    return None
                return (host, port)
            except (ValueError, IndexError):
                return None

        @staticmethod
        def validate_host(host: str) -> bool:
            """Validate gRPC host."""
            return bool(host and host.strip())

        @staticmethod
        def validate_port(port: int) -> bool:
            """Validate gRPC port number."""
            return c.Grpc.GrpcNetwork.MIN_PORT <= port <= c.Grpc.GrpcNetwork.MAX_PORT


u = FlextGrpcUtilities
