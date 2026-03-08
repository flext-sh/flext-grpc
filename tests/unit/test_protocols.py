"""Tests for FlextGrpcProtocols.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

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
        """Test that ServerProtocol exists."""
        assert hasattr(FlextGrpcProtocols.Grpc, "ServerProtocol")

    def test_client_protocol_exists(self) -> None:
        """Test that ClientProtocol exists."""
        assert hasattr(FlextGrpcProtocols.Grpc, "ClientProtocol")

    def test_streaming_protocol_exists(self) -> None:
        """Test that StreamingProtocol exists."""
        assert hasattr(FlextGrpcProtocols.Grpc, "StreamingProtocol")

    def test_service_protocol_exists(self) -> None:
        """Test that ServiceProtocol exists."""
        assert hasattr(FlextGrpcProtocols.Grpc, "ServiceProtocol")

    def test_channel_protocol_exists(self) -> None:
        """Test that ChannelProtocol exists."""
        assert hasattr(FlextGrpcProtocols.Grpc, "ChannelProtocol")

    def test_metrics_protocol_exists(self) -> None:
        """Test that MetricsProtocol exists."""
        assert hasattr(FlextGrpcProtocols.Grpc, "MetricsProtocol")

    def test_configuration_protocol_exists(self) -> None:
        """Test that ConfigurationProtocol exists."""
        assert hasattr(FlextGrpcProtocols.Grpc, "ConfigurationProtocol")

    def test_protocols_are_protocols(self) -> None:
        """Test that protocols are proper Protocol subclasses."""
        assert is_protocol(FlextGrpcProtocols.Grpc.ServerProtocol)
        assert is_protocol(FlextGrpcProtocols.Grpc.ClientProtocol)
        assert is_protocol(FlextGrpcProtocols.Grpc.StreamingProtocol)
        assert is_protocol(FlextGrpcProtocols.Grpc.ServiceProtocol)
