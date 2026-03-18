"""Test protocol definitions for flext-grpc.

Provides TestsFlextGrpcProtocols, combining p with
FlextGrpcProtocols for test-specific protocol definitions.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import p

from flext_grpc import FlextGrpcProtocols


class TestsFlextGrpcProtocols(p, FlextGrpcProtocols):
    """Test protocols combining p and FlextGrpcProtocols.

    Provides access to:
    - p.Tests.Docker.* (from p)
    - p.Tests.Factory.* (from p)
    - p.Grpc.* (from FlextGrpcProtocols)
    """


__all__ = ["TestsFlextGrpcProtocols", "p"]

p = TestsFlextGrpcProtocols
