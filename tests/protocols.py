"""Test protocols for flext-grpc.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from flext_tests import FlextTestsProtocols

from flext_grpc import FlextGrpcProtocols


class TestsFlextGrpcProtocols(FlextTestsProtocols, FlextGrpcProtocols):
    """Test protocols for flext-grpc."""

    class Grpc(FlextGrpcProtocols.Grpc):
        """Grpc domain test protocols."""

        class Tests:
            """Test-specific protocols."""

            @runtime_checkable
            class DuckInstance(Protocol):
                """Opaque duck-typed instance used for runtime protocol checks."""


p = TestsFlextGrpcProtocols
__all__: list[str] = ["TestsFlextGrpcProtocols", "p"]
