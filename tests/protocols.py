"""Test protocols for flext-grpc.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_grpc import FlextGrpcProtocols
from flext_tests import FlextTestsProtocols


class TestsFlextGrpcProtocols(FlextTestsProtocols, FlextGrpcProtocols):
    """Test protocols for flext-grpc."""

    class Grpc(FlextGrpcProtocols.Grpc):
        """Grpc domain test protocols."""

        class Tests:
            """Test-specific protocols."""


p = TestsFlextGrpcProtocols
__all__: list[str] = ["TestsFlextGrpcProtocols", "p"]
