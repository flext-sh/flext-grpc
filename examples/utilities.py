"""Example utilities for flext-grpc.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_grpc import FlextGrpcUtilities


class ExamplesFlextGrpcUtilities(FlextGrpcUtilities):
    """Example utilities for flext-grpc."""

    class Grpc(FlextGrpcUtilities.Grpc):
        """Grpc domain example utilities."""

        class Examples:
            """Example-specific utilities."""


__all__: list[str] = ["ExamplesFlextGrpcUtilities"]
