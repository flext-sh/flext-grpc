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
from typing import TYPE_CHECKING, ClassVar

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
        NETWORK_HOST_RE: ClassVar[t.RegexPattern] = re.compile(
            FlextGrpcConstantsBase.NETWORK_HOST_PATTERN
        )

        # ===== Validation constants (derived — not a plain literal) =====
        VALIDATION_VERSION_RE: ClassVar[t.RegexPattern] = re.compile(
            FlextGrpcConstantsBase.VALIDATION_VERSION_PATTERN, re.IGNORECASE
        )

        # ===== Error messages =====

        # ===== Error codes =====

        # ===== Timeout validation =====

        # ===== Enum-derived frozensets (immutable collections) =====
        # Owned by ``FlextGrpcConstantsBase`` in ``_constants/base.py``
        # (ENFORCE-079): state enums and their derived frozensets resolve
        # through the MRO (``c.Grpc.ChannelState``, ``c.Grpc.CHANNEL_STATES``).


c = FlextGrpcConstants

__all__: t.StrSequence = ("FlextGrpcConstants", "c")
