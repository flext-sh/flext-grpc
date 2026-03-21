"""FLEXT gRPC Constants.

gRPC-specific constants including network settings, service configuration,
validation rules, and configuration defaults. Designed for consistent
configuration management and enterprise deployment standards.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from enum import StrEnum, unique
from typing import Final, Literal

from flext_core import FlextConstants


class FlextGrpcConstants(FlextConstants):
    """gRPC-specific constants following FLEXT unified single-class pattern.

    Defines ALL constants used by the flext-grpc project, including inherited
    constants redefined for gRPC context. NO direct imports from c
    should be used - all constants must come from this class.

    Layer N Foundation: gRPC domain-specific constants building on flext-core Layer 0.

    Usage:
    ```python
    from flext_grpc import FlextGrpcConstants

    timeout = FlextGrpcConstants.Grpc.GrpcNetwork.DEFAULT_TIMEOUT
    port = FlextGrpcConstants.Grpc.GrpcNetwork.DEFAULT_GRPC_PORT
    ```
    """

    class Grpc:
        """gRPC domain constants namespace.

        All gRPC-specific constants are organized here for better namespace
        organization and to enable composition with other domain constants.
        """

        class GrpcNetwork:
            """gRPC-specific network constants."""

            DEFAULT_HOST: Final[str] = "127.0.0.1"
            DEFAULT_GRPC_PORT: Final[int] = 50051
            MIN_PORT: Final[int] = 1
            MAX_PORT: Final[int] = 65535
            DEFAULT_TIMEOUT: Final[float] = float(
                FlextConstants.DEFAULT_TIMEOUT_SECONDS
            )
            HOST: Final[str] = "127.0.0.1"
            LOCALHOST_IP: Final[str] = "127.0.0.1"
            DEFAULT_KEEPALIVE_TIME_MS: Final[int] = 30000
            DEFAULT_KEEPALIVE_TIMEOUT_MS: Final[int] = 5000

        class Service:
            """gRPC service constants extending c.Service."""

            DEFAULT_MAX_WORKERS: Final[int] = 10
            MIN_WORKERS: Final[int] = 1
            MAX_WORKERS: Final[int] = 100
            DEFAULT_MAX_CONCURRENT_RPCS: Final[int] = 1000

        class Connection:
            """gRPC connection and performance constants."""

            MAX_WORKERS: Final[int] = 20
            DEFAULT_TIMEOUT: Final[float] = float(
                FlextConstants.DEFAULT_TIMEOUT_SECONDS
            )

        class Production:
            """gRPC production validation constants."""

            MIN_PORT: Final[int] = 1024
            RETRY_ATTEMPTS: Final[int] = FlextConstants.DEFAULT_MAX_RETRY_ATTEMPTS
            MAX_RETRY_ATTEMPTS: Final[int] = 5

        class GrpcValidation:
            """gRPC validation constants extending c."""

            ADDRESS_PARTS_COUNT: Final[int] = 2
            MAX_PORT_NUMBER: Final[int] = 65535

        class GrpcMessages:
            """gRPC-specific error and status messages."""

            TIMEOUT_ERROR: Final[str] = "gRPC operation timed out after {timeout}s"

        class GrpcErrors:
            """gRPC-specific error codes."""

            CONNECTION_ERROR: Final[str] = "GRPC_CONNECTION_ERROR"
            TIMEOUT_ERROR: Final[str] = "GRPC_TIMEOUT_ERROR"
            VALIDATION_ERROR: Final[str] = "GRPC_VALIDATION_ERROR"
            SERVER_ERROR: Final[str] = "GRPC_SERVER_ERROR"

        class GrpcPerformance:
            """gRPC performance and health check constants."""

        class GrpcLimits:
            """gRPC request and error rate limits."""

        class Timeouts:
            """gRPC timeout validation constants."""

            MAX_TIMEOUT_SECONDS: Final[float] = 300.0

        class Streaming:
            """gRPC streaming constants."""

            CLIENT_STREAMING_BUFFER_THRESHOLD: Final[int] = 10
            SERVER_STREAMING_BATCH_SIZE: Final[int] = 100
            BIDIRECTIONAL_STREAMING_QUEUE_SIZE: Final[int] = 1000

        @unique
        class ChannelState(StrEnum):
            """gRPC channel state enumeration (single source of truth).

            DRY Pattern:
                StrEnum is the single source of truth. Use ChannelState.IDLE.value
                or ChannelState.IDLE directly - no base strings needed.
            """

            IDLE = "idle"
            CONNECTING = "connecting"
            READY = "ready"
            TRANSIENT_FAILURE = "transient_failure"
            SHUTDOWN = "shutdown"

        @unique
        class ServerState(StrEnum):
            """gRPC server state enumeration (single source of truth).

            DRY Pattern:
                StrEnum is the single source of truth. Use ServerState.STOPPED.value
                or ServerState.STOPPED directly - no base strings needed.
            """

            STOPPED = "stopped"
            STARTING = "starting"
            RUNNING = "running"
            STOPPING = "stopping"

        @unique
        class GrpcOperations(StrEnum):
            """gRPC operation types (single source of truth).

            DRY Pattern:
                StrEnum is the single source of truth. Use GrpcOperations.UNARY.value
                or GrpcOperations.UNARY directly - no base strings needed.
            """

            UNARY = "unary"
            SERVER_STREAMING = "server_streaming"
            CLIENT_STREAMING = "client_streaming"
            BIDIRECTIONAL = "bidirectional"

        @unique
        class CompressionTypes(StrEnum):
            """gRPC compression types (single source of truth).

            DRY Pattern:
                StrEnum is the single source of truth. Use CompressionTypes.NONE.value
                or CompressionTypes.NONE directly - no base strings needed.
            """

            NONE = "none"
            GZIP = "gzip"
            DEFLATE = "deflate"

        @unique
        class LoadBalancingPolicies(StrEnum):
            """gRPC load balancing policies (single source of truth).

            DRY Pattern:
                StrEnum is the single source of truth. Use LoadBalancingPolicies.ROUND_ROBIN.value
                or LoadBalancingPolicies.ROUND_ROBIN directly - no base strings needed.
            """

            ROUND_ROBIN = "round_robin"
            PICK_FIRST = "pick_first"
            GRPCLB = "grpclb"
            XDS_CLUSTER_RESOLVER = "xds_cluster_resolver"

        type ChannelStateLiteral = Literal[
            "idle", "connecting", "ready", "transient_failure", "shutdown"
        ]
        "Channel state literal - references ChannelState StrEnum members."
        type ServerStateLiteral = Literal["stopped", "starting", "running", "stopping"]
        "Server state literal - references ServerState StrEnum members."
        type StreamTypeLiteral = Literal[
            "unary", "server_streaming", "client_streaming", "bidirectional"
        ]
        "Stream type literal - references GrpcOperations StrEnum members."
        type LoadBalancingPolicyLiteral = Literal[
            "round_robin", "pick_first", "grpclb", "xds_cluster_resolver"
        ]
        "Load balancing policy literal - references LoadBalancingPolicies StrEnum members."
        type CompressionTypeLiteral = Literal["none", "gzip", "deflate"]
        "Compression type literal - references CompressionTypes StrEnum members."
        type GrpcOperationLiteral = Literal[
            "unary", "server_streaming", "client_streaming", "bidirectional"
        ]
        "gRPC operation literal - references GrpcOperations StrEnum members."
        "Channel states tuple - generated from ChannelState StrEnum."
        "Server states tuple - generated from ServerState StrEnum."
        STREAM_TYPES: Final[tuple[str, ...]] = tuple(
            member.value for member in GrpcOperations.__members__.values()
        )
        "Stream types tuple - generated from GrpcOperations StrEnum."
        "Load balancing policies tuple - generated from LoadBalancingPolicies StrEnum."
        "Compression types tuple - generated from CompressionTypes StrEnum."


__all__: list[str] = ["FlextGrpcConstants", "c"]

c = FlextGrpcConstants
