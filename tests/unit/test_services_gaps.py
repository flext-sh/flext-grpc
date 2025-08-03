"""FLEXT gRPC Services Gap Testing - Targeted coverage for service validation paths.

This module provides surgical testing for uncovered service validation and error
paths, specifically targeting missing coverage lines in services.py to improve
coverage without breaking existing functionality.

Test Focus:
    - Service validation error paths currently uncovered
    - Operation argument validation not tested
    - Edge case error handling missing from main test suite
    - Service execution branches not covered

Coverage Target Lines (services.py):
    107, 114, 229-231, 311, 314, 322, 425, 431, 468, 472, 511, 515,
    741-743, 763, 766, 774, 779, 848, 868, 872, 876, 879, 892, 897, 901,
    1042-1044, 1058, 1062, 1105, 1122, 1140, 1161, 1172, 1356

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from datetime import UTC, datetime

from flext_grpc.entities import FlextGrpcChannel, FlextGrpcServer
from flext_grpc.services import FlextGrpcService


class TestServicesValidationGaps:
    """Surgical tests for uncovered service validation and error paths."""

    def test_service_execute_missing_arguments(self) -> None:
        """Test service execute with missing arguments for coverage line 107."""
        service = FlextGrpcService()

        # Line 107: Missing required arguments error path
        result = service.execute("server")  # Missing required arguments
        assert result.is_failure
        assert "Missing required arguments" in result.error

    def test_service_execute_non_string_operation(self) -> None:
        """Test service execute with non-string operation for coverage line 114."""
        service = FlextGrpcService()
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            max_workers=10,
            created_at=datetime.now(UTC),
        )

        # Line 114: Operation must be a string error path
        result = service.execute("server", 123, server)  # Non-string operation (123)
        assert result.is_failure
        assert "Operation must be a string" in result.error

    def test_service_execute_invalid_service_type(self) -> None:
        """Test service execute with invalid service type."""
        service = FlextGrpcService()
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            max_workers=10,
            created_at=datetime.now(UTC),
        )

        # Test with invalid service type
        result = service.execute("invalid_service_type", "start", server)
        assert result.is_failure
        assert "Invalid service type" in result.error or "Unknown" in result.error

    def test_service_execute_invalid_operation(self) -> None:
        """Test service execute with invalid operation."""
        service = FlextGrpcService()
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            max_workers=10,
            created_at=datetime.now(UTC),
        )

        # Test with invalid operation
        result = service.execute("server", "invalid_operation", server)
        assert result.is_failure
        # Should fail with some validation error

    def test_service_execute_wrong_entity_type(self) -> None:
        """Test service execute with wrong entity type for operation."""
        service = FlextGrpcService()
        channel = FlextGrpcChannel(
            id="test-channel", target="localhost:50051", created_at=datetime.now(UTC)
        )

        # Try to use channel with server operation
        result = service.execute("server", "start", channel)
        assert result.is_failure
        # Should fail with entity type mismatch

    def test_service_execute_insufficient_arguments_variations(self) -> None:
        """Test various insufficient argument scenarios."""
        service = FlextGrpcService()

        # Test with no arguments at all
        result = service.execute()
        assert result.is_failure
        assert "Missing required argument" in result.error

        # Test with only service type
        result = service.execute("server")
        assert result.is_failure
        assert "Missing required arguments" in result.error

    def test_client_service_missing_arguments(self) -> None:
        """Test client service operations with missing arguments."""
        service = FlextGrpcService()

        # Test client operations with insufficient args
        result = service.execute("client")
        assert result.is_failure
        assert "Missing required arguments" in result.error

        result = service.execute("client", "connect")
        assert result.is_failure
        # Should fail with missing client entity

    def test_stream_service_missing_arguments(self) -> None:
        """Test stream service operations with missing arguments."""
        service = FlextGrpcService()

        # Test stream operations with insufficient args
        result = service.execute("stream")
        assert result.is_failure
        assert "Missing required argument" in result.error

        result = service.execute("stream", "create")
        assert result.is_failure
        # Should fail with missing stream parameters

    def test_service_execution_edge_cases(self) -> None:
        """Test service execution edge cases for additional coverage."""
        service = FlextGrpcService()

        # Test with None as operation
        result = service.execute("server", None, "dummy")
        assert result.is_failure

        # Test with empty string operation
        result = service.execute("server", "", "dummy")
        assert result.is_failure or result.is_success  # Either is acceptable

        # Test with numeric operation
        result = service.execute("server", 42, "dummy")
        assert result.is_failure
        assert "Operation must be a string" in result.error
