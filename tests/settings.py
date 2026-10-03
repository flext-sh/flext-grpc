"""Runtime settings for flext-grpc tests.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsSettings

from flext_grpc import FlextGrpcSettings


class TestsFlextGrpcSettings(FlextGrpcSettings, FlextTestsSettings):
    """gRPC settings extended with the shared test namespace."""


__all__: list[str] = ["TestsFlextGrpcSettings"]
