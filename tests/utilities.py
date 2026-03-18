"""Test utilities for flext-grpc tests.

Provides TestsFlextGrpcUtilities, extending u with flext-grpc-specific
utilities. All generic test utilities come from flext_tests.

Architecture:
- u (flext_tests) = Generic utilities for all FLEXT projects
- TestsFlextGrpcUtilities (tests/) = flext-grpc-specific utilities extending u

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import u

from flext_grpc import FlextGrpcUtilities


class TestsFlextGrpcUtilities(u, FlextGrpcUtilities):
    """Utilities for flext-grpc tests - extends u and FlextGrpcUtilities.

    Architecture: Extends both u and FlextGrpcUtilities with
    flext-grpc-specific utility methods. All generic utilities from u
    and production utilities from FlextGrpcUtilities are available through inheritance.

    Rules:
    - NEVER redeclare utilities from u or FlextGrpcUtilities
    - Only flext-grpc-specific test utilities allowed
    - All generic utilities come from u
    - All production utilities come from FlextGrpcUtilities
    """


__all__ = ["TestsFlextGrpcUtilities", "u"]

u = TestsFlextGrpcUtilities
