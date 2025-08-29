"""FLEXT gRPC Services Gap Testing - Targeted coverage for service validation paths.

This module provides surgical testing for uncovered service validation and error
paths, specifically targeting missing coverage lines in services.py to improve
coverage without breaking existing functionality.

Test Focus:
    - Service validation error paths currently uncovered
    - Operation argument validation not tested
    - Edge case error handling missing from main test suite
    - Service execution branches not covered

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from datetime import UTC, datetime

from flext_core import FlextModels, FlextModels.Timestamp

from flext_grpc import (
    FlextGrpcChannel,
    FlextGrpcClient,
    FlextGrpcClientService,
    FlextGrpcServer,
    FlextGrpcServerService,
    FlextGrpcService,
    FlextGrpcStream,
    FlextGrpcStreamService,
    TGrpcTarget,
)


class TestServicesValidationGaps:
    """Surgical tests for uncovered service validation and error paths."""

    def test_server_service_unknown_command(self) -> None:
        """Test server service with unknown command."""
        service = FlextGrpcServerService()
        server = FlextGrpcServer(
            id=FlextModels.EntityId("test-server"),
            host="localhost",
            port=50051,
            max_workers=10,
            created_at=FlextModels.Timestamp(datetime.now(UTC)),
        )

        result = service.execute("unknown_command", server)
        assert result.is_failure
        assert result.error is not None
        assert result.error is not None
        assert "Unknown server command" in result.error

    def test_client_service_unknown_command(self) -> None:
        """Test client service with unknown command."""
        service = FlextGrpcClientService()
        client = FlextGrpcClient(
            id=FlextModels.EntityId("test-client"),
            created_at=FlextModels.Timestamp(datetime.now(UTC)),
        )

        result = service.execute("unknown_command", client)
        assert result.is_failure
        assert result.error is not None
        assert "Unknown client command" in result.error

    def test_stream_service_unknown_command(self) -> None:
        """Test stream service with unknown command."""
        service = FlextGrpcStreamService()
        stream = FlextGrpcStream(
            id=FlextModels.EntityId("test-stream"),
            stream_type="unary",
            method_name="TestMethod",
            created_at=FlextModels.Timestamp(datetime.now(UTC)),
        )

        result = service.execute("unknown_command", stream)
        assert result.is_failure
        assert result.error is not None
        assert "Unknown stream command" in result.error

    def test_server_service_invalid_server_state(self) -> None:
        """Test server service operations with invalid server state."""
        service = FlextGrpcServerService()
        # Create server with invalid port to trigger validation failure
        server = FlextGrpcServer(
            id=FlextModels.EntityId("test-server"),
            host="",  # Invalid empty host
            port=50051,
            max_workers=10,
            created_at=FlextModels.Timestamp(datetime.now(UTC)),
        )

        result = service.execute("start", server)
        assert result.is_failure
        assert result.error is not None
        assert "Server validation failed" in result.error

    def test_client_service_missing_channel(self) -> None:
        """Test client operations when channel is None."""
        service = FlextGrpcClientService()
        client = FlextGrpcClient(
            id=FlextModels.EntityId("test-client"),
            channel=None,  # No channel
            created_at=FlextModels.Timestamp(datetime.now(UTC)),
        )

        result = service.execute("connect", client)
        assert result.is_failure
        assert result.error is not None
        assert "has no channel" in result.error

    def test_client_service_call_not_connected(self) -> None:
        """Test client call when not connected."""
        service = FlextGrpcClientService()
        channel = FlextGrpcChannel(
            id=FlextModels.EntityId("test-channel"),
            target=TGrpcTarget("localhost:50051"),
            state="idle",  # Not connected
            created_at=FlextModels.Timestamp(datetime.now(UTC)),
        )
        client = FlextGrpcClient(
            id=FlextModels.EntityId("test-client"),
            channel=channel,
            created_at=FlextModels.Timestamp(datetime.now(UTC)),
        )

        result = service.execute("call", client, "TestMethod", {"data": "test"})
        assert result.is_failure
        assert result.error is not None
        assert "Cannot make call with disconnected client" in result.error

    def test_server_service_add_service_wrong_state(self) -> None:
        """Test adding service to server in wrong state."""
        service = FlextGrpcServerService()
        server = FlextGrpcServer(
            id=FlextModels.EntityId("test-server"),
            host="localhost",
            port=50051,
            max_workers=10,
            state="stopped",  # Wrong state for adding service
            created_at=FlextModels.Timestamp(datetime.now(UTC)),
        )

        grpc_service = FlextGrpcService(
            id=FlextModels.EntityId("test-service"),
            name="TestService",
            methods=["TestMethod"],
            created_at=FlextModels.Timestamp(datetime.now(UTC)),
        )

        result = service.execute("add_service", server, grpc_service)
        assert result.is_failure
        assert result.error is not None
        assert "Cannot add service to server in state" in result.error

    def test_stream_service_validation_errors(self) -> None:
        """Test stream service with validation errors."""
        service = FlextGrpcStreamService()
        # Create stream with empty method name to trigger validation
        stream = FlextGrpcStream(
            id=FlextModels.EntityId("test-stream"),
            stream_type="unary",
            method_name="",  # Invalid empty method name
            created_at=FlextModels.Timestamp(datetime.now(UTC)),
        )

        result = service.execute("create", stream)
        assert result.is_failure
        assert result.error is not None
        assert "Stream validation failed" in result.error

    def test_service_execute_insufficient_arguments_variations(self) -> None:
        """Test various insufficient argument scenarios."""
        server_service = FlextGrpcServerService()
        client_service = FlextGrpcClientService()

        # Test server service - call method requires method name
        server = FlextGrpcServer(
            id=FlextModels.EntityId("test-server"),
            host="localhost",
            port=50051,
            max_workers=10,
            created_at=FlextModels.Timestamp(datetime.now(UTC)),
        )

        # This should work - valid operation
        result = server_service.execute("status", server)
        assert result.success

        # Test client service - call without method name should fail
        channel = FlextGrpcChannel(
            id=FlextModels.EntityId("test-channel"),
            target=TGrpcTarget("localhost:50051"),
            state="ready",
            created_at=FlextModels.Timestamp(datetime.now(UTC)),
        )
        client = FlextGrpcClient(
            id=FlextModels.EntityId("test-client"),
            channel=channel,
            created_at=FlextModels.Timestamp(datetime.now(UTC)),
        )

        result = client_service.execute("call", client)  # Missing method name
        assert result.is_failure
        assert result.error is not None
        assert "Method name must be string" in result.error
