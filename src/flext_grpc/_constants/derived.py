"""FLEXT gRPC derived and compiled constants.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, ClassVar

from flext_grpc._constants import FlextGrpcConstantsBase

if TYPE_CHECKING:
    from flext_grpc import t


class FlextGrpcConstantsDerived:
    """Derived gRPC constants that cannot be plain literals.

    Compiled patterns resolve their source patterns from
    ``FlextGrpcConstantsBase`` (ENFORCE-079) through the namespace MRO.
    """

    # ===== Network constants (derived — not a plain literal) =====
    NETWORK_HOST_RE: ClassVar[t.RegexPattern] = re.compile(
        FlextGrpcConstantsBase.NETWORK_HOST_PATTERN,
    )

    # ===== Validation constants (derived — not a plain literal) =====
    VALIDATION_VERSION_RE: ClassVar[t.RegexPattern] = re.compile(
        FlextGrpcConstantsBase.VALIDATION_VERSION_PATTERN,
        re.IGNORECASE,
    )


__all__: list[str] = ["FlextGrpcConstantsDerived"]
