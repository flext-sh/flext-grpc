"""Private constants base for flext-grpc.

Owns constant values that must not live in the public ``constants.py``
facade module directly (ENFORCE-079); the facade re-exports them via
``c.Grpc.*``.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Final


class FlextGrpcConstantsBase:
    """Private constants owner for gRPC network defaults."""

    NETWORK_DEFAULT_CHANNEL_READY_TIMEOUT: Final[float] = 5.0


__all__: list[str] = ["FlextGrpcConstantsBase"]
