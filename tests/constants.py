"""Test constants for flext-grpc.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsConstants

from tests import FlextGrpcConstants


class TestsFlextGrpcConstants(FlextTestsConstants, FlextGrpcConstants):
    """Test constants for flext-grpc."""

    class Tests(FlextTestsConstants.Tests):
        """Test-specific constants."""


c = TestsFlextGrpcConstants

__all__: list[str] = ["TestsFlextGrpcConstants", "c"]
