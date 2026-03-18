"""Test models for flext-grpc tests.

Provides TestsFlextGrpcModels, extending m with flext-grpc-specific
models using COMPOSITION INHERITANCE.

Inheritance hierarchy:
- m (flext_tests) - Provides .Tests.* namespace
- FlextGrpcModels (production) - Provides .Domain.*, .GrpcConfig.* namespaces

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import m

from flext_grpc import FlextGrpcModels


class TestsFlextGrpcModels(m, FlextGrpcModels):
    """Models for flext-grpc tests using COMPOSITION INHERITANCE.

    MANDATORY: Inherits from BOTH:
    1. m - for test infrastructure (.Tests.*)
    2. FlextGrpcModels - for domain models (.Domain.*, .GrpcConfig.*)

    Access patterns:
    - tm.Tests.* (generic test models from m)
    - tm.Domain.* (gRPC domain models from FlextGrpcModels)
    - tm.GrpcConfig.* (gRPC config models from FlextGrpcModels)
    - m.Domain.* (production models via alternative alias)

    Rules:
    - NEVER duplicate models from m or FlextGrpcModels
    - Only flext-grpc-specific test fixtures allowed
    - All generic test models come from m
    - All production models come from FlextGrpcModels
    """


# Short aliases per FLEXT convention
tm = TestsFlextGrpcModels

__all__ = [
    "TestsFlextGrpcModels",
    "m",
    "tm",
]

m = TestsFlextGrpcModels
