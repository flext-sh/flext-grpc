"""Test utilities for flext-grpc.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsUtilities

from flext_grpc import FlextGrpcUtilities


class FlextGrpcTestUtilities(FlextTestsUtilities, FlextGrpcUtilities):
    """Test utilities for flext-grpc."""

    class Grpc(FlextGrpcUtilities.Grpc):
        """Grpc domain test utilities."""

        class Tests:
            """Test-specific utilities."""


u = FlextGrpcTestUtilities
__all__ = ["FlextGrpcTestUtilities", "u"]
