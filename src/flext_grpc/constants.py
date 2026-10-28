# AUTO-GENERATED FILE — Regenerate with: make gen
"""FLEXT gRPC Constants.

gRPC-specific constants including network settings, service configuration,
validation rules, and configuration defaults. Owns every compiled
``re.Pattern`` for the gRPC domain — consumer modules import the
pre-compiled ``*_RE`` constants directly; ``import re`` outside this
module is forbidden.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)

from flext_core import c as flext_core_c

from flext_grpc._constants import FlextGrpcConstantsBase, FlextGrpcConstantsDerived


class FlextGrpcConstants(flext_core_c):
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

    class Grpc(FlextGrpcConstantsBase, FlextGrpcConstantsDerived):
        """gRPC domain constants namespace.

        All gRPC-specific scalar constants are owned by ``FlextGrpcConstantsBase``
        in ``_constants/base.py`` (ENFORCE-079) and re-exported here via
        inheritance; ``c.Grpc.CONSTANT_NAME`` resolves through the MRO.
        This class adds only derived/composite values that cannot be plain
        literals: computed sizes, compiled patterns, enums, and frozensets.
        """

        # ===== Error messages =====

        # ===== Error codes =====

        # ===== Timeout validation =====

        # ===== Enum-derived frozensets (immutable collections) =====
        # Owned by ``FlextGrpcConstantsBase`` in ``_constants/base.py``
        # (ENFORCE-079): state enums and their derived frozensets resolve
        # through the MRO (``c.Grpc.ChannelState``, ``c.Grpc.CHANNEL_STATES``).


c = FlextGrpcConstants
__all__: list[str] = ["FlextGrpcConstants", "c"]
