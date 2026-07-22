"""Test models for flext-grpc.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_grpc import FlextGrpcModels
from flext_tests import FlextTestsModels


class TestsFlextGrpcModels(FlextTestsModels, FlextGrpcModels):
    """Test models for flext-grpc."""

    class Grpc(FlextGrpcModels.Grpc):
        """Grpc domain test models."""

        class Tests:
            """Test-specific models."""


m = TestsFlextGrpcModels
__all__: list[str] = ["TestsFlextGrpcModels", "m"]
