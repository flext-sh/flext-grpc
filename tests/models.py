"""Test models for flext-grpc.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsModels

from flext_grpc import FlextGrpcModels


class FlextGrpcTestModels(FlextTestsModels, FlextGrpcModels):
    """Test models for flext-grpc."""

    class Grpc(FlextGrpcModels.Grpc):
        """Grpc domain test models."""

        class Tests:
            """Test-specific models."""


m = FlextGrpcTestModels
__all__ = ["FlextGrpcTestModels", "m"]
