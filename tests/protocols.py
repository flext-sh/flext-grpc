"""Test protocol definitions for flext-grpc.

Provides TestsFlextGrpcProtocols, combining FlextTestsProtocols with
FlextGrpcProtocols for test-specific protocol definitions.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests.protocols import FlextTestsProtocols

from flext_grpc.protocols import FlextGrpcProtocols


class TestsFlextGrpcProtocols(FlextTestsProtocols, FlextGrpcProtocols):
    """Test protocols combining FlextTestsProtocols and FlextGrpcProtocols.

    Provides access to:
    - p.Tests.Docker.* (from FlextTestsProtocols)
    - p.Tests.Factory.* (from FlextTestsProtocols)
    - p.Grpc.* (from FlextGrpcProtocols)
    """

    class Tests:
        """Project-specific test protocols.

        Extends FlextTestsProtocols.Tests with Grpc-specific protocols.
        """

        class Grpc:
            """Grpc-specific test protocols."""


# Runtime aliases
p = TestsFlextGrpcProtocols
p = TestsFlextGrpcProtocols

__all__ = ["TestsFlextGrpcProtocols", "p"]
