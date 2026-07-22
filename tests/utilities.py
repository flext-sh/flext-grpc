"""Test utilities for flext-grpc.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_grpc import FlextGrpcUtilities
from flext_tests import FlextTestsUtilities


class TestsFlextGrpcUtilities(FlextTestsUtilities, FlextGrpcUtilities):
    """Test utilities for flext-grpc."""

    class Grpc(FlextGrpcUtilities.Grpc):
        """Grpc domain test utilities."""

        class Tests:
            """Test-specific utilities."""


u = TestsFlextGrpcUtilities
__all__: list[str] = ["TestsFlextGrpcUtilities", "u"]
