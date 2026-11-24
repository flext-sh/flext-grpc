"""Test utilities for flext-grpc.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsUtilities

from tests import FlextGrpcUtilities


class TestsFlextGrpcUtilities(FlextTestsUtilities, FlextGrpcUtilities):
    """Test utilities for flext-grpc."""

    class Tests(FlextTestsUtilities.Tests):
        """Test-specific utilities."""


u = TestsFlextGrpcUtilities
__all__: list[str] = ["TestsFlextGrpcUtilities", "u"]
