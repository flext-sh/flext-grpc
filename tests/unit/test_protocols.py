"""Tests for FlextGrpcProtocols.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import is_protocol

from flext_grpc import FlextGrpcProtocols


class TestFlextGrpcProtocols:
    """Test cases for FlextGrpcProtocols."""

    def test_protocols_class_exists(self) -> None:
        """Test that FlextGrpcProtocols class exists."""
        assert FlextGrpcProtocols is not None

    def test_grpc_namespace_exists(self) -> None:
        """Test that Grpc namespace exists."""
        assert hasattr(FlextGrpcProtocols, "Grpc")

    def test_server_protocol_exists(self) -> None:
        """Test that Server exists."""
        assert hasattr(FlextGrpcProtocols.Grpc, "Server")

    def test_client_protocol_exists(self) -> None:
        """Test that Client exists."""
        assert hasattr(FlextGrpcProtocols.Grpc, "Client")

    def test_streaming_protocol_exists(self) -> None:
        """Test that Streaming exists."""
        assert hasattr(FlextGrpcProtocols.Grpc, "Streaming")

    def test_service_protocol_exists(self) -> None:
        """Test that Service exists."""
        assert hasattr(FlextGrpcProtocols.Grpc, "Service")

    def test_channel_protocol_exists(self) -> None:
        """Test that Channel exists."""
        assert hasattr(FlextGrpcProtocols.Grpc, "Channel")

    def test_metrics_protocol_exists(self) -> None:
        """Test that Metrics exists."""
        assert hasattr(FlextGrpcProtocols.Grpc, "Metrics")

    def test_configuration_protocol_exists(self) -> None:
        """Test that Configuration exists."""
        assert hasattr(FlextGrpcProtocols.Grpc, "Configuration")

    def test_protocols_are_protocols(self) -> None:
        """Test that protocols are proper Protocol subclasses."""
        assert is_protocol(FlextGrpcProtocols.Grpc.Server)
        assert is_protocol(FlextGrpcProtocols.Grpc.Client)
        assert is_protocol(FlextGrpcProtocols.Grpc.Streaming)
        assert is_protocol(FlextGrpcProtocols.Grpc.Service)
