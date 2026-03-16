"""Test utilities for flext-grpc tests.

Provides TestsFlextGrpcUtilities, extending FlextTestsUtilities with flext-grpc-specific
utilities. All generic test utilities come from flext_tests.

Architecture:
- FlextTestsUtilities (flext_tests) = Generic utilities for all FLEXT projects
- TestsFlextGrpcUtilities (tests/) = flext-grpc-specific utilities extending FlextTestsUtilities

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsUtilities

from flext_grpc import FlextGrpcUtilities


class TestsFlextGrpcUtilities(FlextTestsUtilities, FlextGrpcUtilities):
    """Utilities for flext-grpc tests - extends FlextTestsUtilities and FlextGrpcUtilities.

    Architecture: Extends both FlextTestsUtilities and FlextGrpcUtilities with
    flext-grpc-specific utility methods. All generic utilities from FlextTestsUtilities
    and production utilities from FlextGrpcUtilities are available through inheritance.

    Rules:
    - NEVER redeclare utilities from FlextTestsUtilities or FlextGrpcUtilities
    - Only flext-grpc-specific test utilities allowed
    - All generic utilities come from FlextTestsUtilities
    - All production utilities come from FlextGrpcUtilities
    """


__all__ = ["TestsFlextGrpcUtilities", "u"]

u = TestsFlextGrpcUtilities
