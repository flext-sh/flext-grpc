"""FLEXT gRPC Constants.

gRPC-specific constants including network settings, service configuration,
validation rules, and configuration defaults. Owns every compiled
``re.Pattern`` for the gRPC domain — consumer modules import the
pre-compiled ``*_RE`` constants directly; ``import re`` outside this
module is forbidden.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import re
from enum import StrEnum, unique
from typing import TYPE_CHECKING, ClassVar, Final

from flext_core import c as _flext_core_c

from ._constants.base import FlextGrpcConstantsBase

if TYPE_CHECKING:
    from flext_grpc import t


class FlextGrpcConstants(_flext_core_c):
    """gRPC-specific constants following FLEXT unified single-class pattern.

    Defines ALL constants used by the flext-grpc project, including inherited
    constants redefined for gRPC context. NO direct imports from c
    should be used - all constants must come from this class.

    Layer N Foundation: gRPC domain-specific constants building on flext-core Layer 0.

    Usage:
    ```python
    from flext_grpc import FlextGrpcConstants, t

    timeout = FlextGrpcConstants.Grpc.NETWORK_DEFAULT_TIMEOUT
    port = FlextGrpcConstants.Grpc.NETWORK_DEFAULT_GRPC_PORT
    ```
    """

    class Grpc(FlextGrpcConstantsBase):
        """gRPC domain constants namespace.

        All gRPC-specific scalar constants are owned by ``FlextGrpcConstantsBase``
        in ``_constants/base.py`` (ENFORCE-079) and re-exported here via
        inheritance; ``c.Grpc.CONSTANT_NAME`` resolves through the MRO.
        This class adds only derived/composite values that cannot be plain
        literals: computed sizes, compiled patterns, enums, and frozensets.
        """

        # ===== Network constants (derived — not a plain literal) =====
        NETWORK_DEFAULT_TIMEOUT: Final[float] = float(
            _flext_core_c.DEFAULT_TIMEOUT_SECONDS
        )
        NETWORK_HOST_RE: ClassVar[t.RegexPattern] = re.compile(
            FlextGrpcConstantsBase.NETWORK_HOST_PATTERN
        )

        # ===== Performance limits (derived — not a plain literal) =====
        PERFORMANCE_DEFAULT_MESSAGE_LENGTH: Final[int] = 4 * 1024 * 1024
        PERFORMANCE_MAX_MESSAGE_LENGTH: Final[int] = 100 * 1024 * 1024

        # ===== Validation constants (derived — not a plain literal) =====
        VALIDATION_VERSION_RE: ClassVar[t.RegexPattern] = re.compile(
            FlextGrpcConstantsBase.VALIDATION_VERSION_PATTERN, re.IGNORECASE
        )

        # ===== Error messages =====

        # ===== Error codes =====

        # ===== Timeout validation =====

        # ===== Enums (single source of truth) =====
        @unique
        class ChannelState(StrEnum):
            """gRPC channel state enumeration (single source of truth).

            DRY Pattern:
                StrEnum is the single source of truth. Use ChannelState.IDLE.value
                or ChannelState.IDLE directly - no base strings needed.
            """

            IDLE = "idle"
            READY = "ready"

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

        @unique
        class ServiceMethod(StrEnum):
            """gRPC service method names (single source of truth).

            DRY Pattern:
                StrEnum is the single source of truth. Use ServiceMethod.ECHO.value
                or ServiceMethod.ECHO directly - no base strings needed.
            """

            ECHO = "Echo"
            HEALTH_CHECK = "HealthCheck"

        @unique
        class CompressionTypes(StrEnum):
            """gRPC compression types (single source of truth).

            DRY Pattern:
                StrEnum is the single source of truth. Use CompressionTypes.NONE.value
                or CompressionTypes.NONE directly - no base strings needed.
            """

            NONE = "none"

        @unique
        class LoadBalancingPolicies(StrEnum):
            """gRPC load balancing policies (single source of truth).

            DRY Pattern:
                StrEnum is the single source of truth. Use LoadBalancingPolicies.ROUND_ROBIN.value
                or LoadBalancingPolicies.ROUND_ROBIN directly - no base strings needed.
            """

        # ===== Enum-derived frozensets (immutable collections) =====
        CHANNEL_STATES: Final[frozenset[str]] = frozenset(
            member.value for member in ChannelState.__members__.values()
        )
        """Channel states frozenset - generated from ChannelState StrEnum."""

        SERVER_STATES: Final[frozenset[str]] = frozenset(
            member.value for member in ServerState.__members__.values()
        )
        """Server states frozenset - generated from ServerState StrEnum."""

        STREAM_TYPES: Final[frozenset[str]] = frozenset(
            member.value for member in GrpcOperations.__members__.values()
        )
        """Stream types frozenset - generated from GrpcOperations StrEnum."""


c = FlextGrpcConstants

__all__: t.StrSequence = ("FlextGrpcConstants", "c")
