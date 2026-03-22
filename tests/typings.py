"""Test type aliases for flext-grpc.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsTypes

from flext_grpc import FlextGrpcTypes


class FlextGrpcTestTypes(FlextTestsTypes, FlextGrpcTypes):
    """Test type aliases for flext-grpc."""

    class Grpc(FlextGrpcTypes.Grpc):
        """Grpc domain test type aliases."""

        class Tests:
            """Test-specific type aliases."""


t = FlextGrpcTestTypes
__all__ = ["FlextGrpcTestTypes", "t"]
