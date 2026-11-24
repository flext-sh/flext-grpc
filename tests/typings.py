"""Test type aliases for flext-grpc.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsTypes

from tests import FlextGrpcTypes


class TestsFlextGrpcTypes(FlextTestsTypes, FlextGrpcTypes):
    """Test type aliases for flext-grpc."""

    class Tests(FlextTestsTypes.Tests):
        """Test-specific type aliases."""


t = TestsFlextGrpcTypes
__all__: list[str] = ["TestsFlextGrpcTypes", "t"]
