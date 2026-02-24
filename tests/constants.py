"""Constants for flext-grpc tests.

Provides TestsFlextGrpcConstants, extending FlextTestsConstants with flext-grpc-specific
constants using COMPOSITION INHERITANCE.

Inheritance hierarchy:
- FlextTestsConstants (flext_tests) - Provides .Tests.* namespace
- FlextGrpcConstants (production) - Provides .Grpc.* namespace

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Final, TypeAlias

from flext_tests.constants import FlextTestsConstants

from flext_grpc.constants import FlextGrpcConstants


class TestsFlextGrpcConstants(FlextTestsConstants, FlextGrpcConstants):
    """Constants for flext-grpc tests using COMPOSITION INHERITANCE.

    MANDATORY: Inherits from BOTH:
    1. FlextTestsConstants - for test infrastructure (.Tests.*)
    2. FlextGrpcConstants - for domain constants (.Grpc.*)

    Access patterns:
    - c.Tests.Docker.* (container testing)
    - c.Tests.Matcher.* (assertion messages)
    - c.Tests.Factory.* (test data generation)
    - c.Grpc.* (domain constants from production)
    - c.TestGrpc.* (project-specific test data)

    Rules:
    - NEVER duplicate constants from FlextTestsConstants or FlextGrpcConstants
    - Only flext-grpc-specific test constants allowed
    - All generic constants come from FlextTestsConstants
    - All production constants come from FlextGrpcConstants
    """

    class Paths:
        """Test path constants."""

        TEST_INPUT_DIR: Final[str] = "tests/fixtures/data/input"
        TEST_OUTPUT_DIR: Final[str] = "tests/fixtures/data/output"
        TEST_TEMP_PREFIX: Final[str] = "flext_grpc_test_"

    class TestGrpc:
        """gRPC test server constants."""

        DEFAULT_HOST: Final[str] = "localhost"
        DEFAULT_PORT: Final[int] = 50051
        TEST_SERVICE_NAME: Final[str] = "TestService"
        TEST_METHOD_NAME: Final[str] = "TestMethod"
        CONNECTION_TIMEOUT: Final[float] = 5.0
        OPERATION_TIMEOUT: Final[float] = 10.0

    class TestChannels:
        """gRPC channel test constants."""

        TEST_CHANNEL_HOST: Final[str] = "localhost"
        TEST_CHANNEL_PORT: Final[int] = 50052
        TEST_CHANNEL_TARGET: Final[str] = "localhost:50052"

    class TestStreaming:
        """gRPC streaming test constants."""

        TEST_BUFFER_SIZE: Final[int] = 1024
        TEST_BATCH_SIZE: Final[int] = 10
        TEST_QUEUE_SIZE: Final[int] = 100
        TEST_STREAM_TIMEOUT: Final[float] = 30.0

    class TestMessages:
        """gRPC message test constants."""

        TEST_REQUEST_MESSAGE: Final[str] = "test_request"
        TEST_RESPONSE_MESSAGE: Final[str] = "test_response"
        TEST_ERROR_MESSAGE: Final[str] = "test_error"

    class Literals:
        """Literal type aliases for test constants (Python 3.13 pattern)."""

        ChannelStateLiteral: TypeAlias = FlextGrpcConstants.Grpc.ChannelStateLiteral
        ServerStateLiteral: TypeAlias = FlextGrpcConstants.Grpc.ServerStateLiteral
        StreamTypeLiteral: TypeAlias = FlextGrpcConstants.Grpc.StreamTypeLiteral
        LoadBalancingPolicyLiteral: TypeAlias = (
            FlextGrpcConstants.Grpc.LoadBalancingPolicyLiteral
        )
        CompressionTypeLiteral: TypeAlias = (
            FlextGrpcConstants.Grpc.CompressionTypeLiteral
        )


# Short aliases per FLEXT convention
c = TestsFlextGrpcConstants  # Primary test constants alias
c = TestsFlextGrpcConstants  # Alternative alias for compatibility

__all__ = [
    "TestsFlextGrpcConstants",
    "c",
]
