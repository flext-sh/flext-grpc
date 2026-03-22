"""Test protocols for flext-grpc.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsProtocols

from flext_grpc import FlextGrpcProtocols


class FlextGrpcTestProtocols(FlextTestsProtocols, FlextGrpcProtocols):
    """Test protocols for flext-grpc."""

    class Grpc(FlextGrpcProtocols.Grpc):
        """Grpc domain test protocols."""

        class Tests:
            """Test-specific protocols."""


p = FlextGrpcTestProtocols
__all__ = ["FlextGrpcTestProtocols", "p"]
