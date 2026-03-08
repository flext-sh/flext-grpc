"""Test protocol definitions for flext-grpc.

Provides TestsFlextGrpcProtocols, combining FlextTestsProtocols with
FlextGrpcProtocols for test-specific protocol definitions.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsProtocols

from flext_grpc import FlextGrpcProtocols


class TestsFlextGrpcProtocols(FlextTestsProtocols, FlextGrpcProtocols):
    """Test protocols combining FlextTestsProtocols and FlextGrpcProtocols.

    Provides access to:
    - p.Tests.Docker.* (from FlextTestsProtocols)
    - p.Tests.Factory.* (from FlextTestsProtocols)
    - p.Grpc.* (from FlextGrpcProtocols)
    """


p = TestsFlextGrpcProtocols
__all__ = ["TestsFlextGrpcProtocols", "p"]
