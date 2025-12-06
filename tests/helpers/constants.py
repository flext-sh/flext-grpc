"""Test constants for flext-grpc tests.

Centralized constants for test fixtures, factories, and test data.
Does NOT duplicate src/flext_grpc/constants.py - only test-specific constants.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Final, TypeAlias

from flext_grpc.constants import FlextGrpcConstants


class TestsConstants(FlextGrpcConstants):
    """Centralized test constants following flext-core nested class pattern."""

    class Paths:
        """Test path constants."""

        TEST_INPUT_DIR: Final[str] = "tests/fixtures/data/input"
        TEST_OUTPUT_DIR: Final[str] = "tests/fixtures/data/output"
        TEST_TEMP_PREFIX: Final[str] = "flext_grpc_test_"

    class Grpc:
        """gRPC test server constants."""

        DEFAULT_HOST: Final[str] = "localhost"
        DEFAULT_PORT: Final[int] = 50051
        TEST_SERVICE_NAME: Final[str] = "TestService"
        TEST_METHOD_NAME: Final[str] = "TestMethod"
        CONNECTION_TIMEOUT: Final[float] = 5.0
        OPERATION_TIMEOUT: Final[float] = 10.0

    class Channels:
        """gRPC channel test constants."""

        TEST_CHANNEL_HOST: Final[str] = "localhost"
        TEST_CHANNEL_PORT: Final[int] = 50052
        TEST_CHANNEL_TARGET: Final[str] = "localhost:50052"

    class Streaming:
        """gRPC streaming test constants."""

        TEST_BUFFER_SIZE: Final[int] = 1024
        TEST_BATCH_SIZE: Final[int] = 10
        TEST_QUEUE_SIZE: Final[int] = 100
        TEST_STREAM_TIMEOUT: Final[float] = 30.0

    class Messages:
        """gRPC message test constants."""

        TEST_REQUEST_MESSAGE: Final[str] = "test_request"
        TEST_RESPONSE_MESSAGE: Final[str] = "test_response"
        TEST_ERROR_MESSAGE: Final[str] = "test_error"

    class Literals:
        """Literal type aliases for test constants (Python 3.13 pattern).

        These type aliases reuse production Literals from FlextGrpcConstants
        to ensure consistency between tests and production code.
        """

        # Reuse production Literals for consistency (Python 3.13+ best practices)
        # Channel state literal (reusing production type)
        ChannelStateLiteral: TypeAlias = FlextGrpcConstants.Literals.ChannelStateLiteral

        # Server state literal (reusing production type)
        ServerStateLiteral: TypeAlias = FlextGrpcConstants.Literals.ServerStateLiteral

        # Stream type literal (reusing production type)
        StreamTypeLiteral: TypeAlias = FlextGrpcConstants.Literals.StreamTypeLiteral

        # Load balancing policy literal (reusing production type)
        LoadBalancingPolicyLiteral: TypeAlias = (
            FlextGrpcConstants.Literals.LoadBalancingPolicyLiteral
        )

        # Compression type literal (reusing production type)
        CompressionTypeLiteral: TypeAlias = (
            FlextGrpcConstants.Literals.CompressionTypeLiteral
        )


# Standardized short name for use in tests
c = TestsConstants
__all__ = ["TestsConstants", "c"]
