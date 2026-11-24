"""Test models for flext-grpc.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsModels

from tests import FlextGrpcModels


class TestsFlextGrpcModels(FlextTestsModels, FlextGrpcModels):
    """Test models for flext-grpc."""

    class Tests(FlextTestsModels.Tests):
        """Test-specific models."""


m = TestsFlextGrpcModels
__all__: list[str] = ["TestsFlextGrpcModels", "m"]
