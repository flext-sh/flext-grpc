"""Tests for FlextGrpcProtocols.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import is_protocol

from flext_tests import tm

from flext_grpc import FlextGrpcProtocols


class TestFlextGrpcProtocols:
    """Test cases for FlextGrpcProtocols."""

    def test_protocols_class_exists(self) -> None:
        """Test that FlextGrpcProtocols class exists."""
        tm.that(FlextGrpcProtocols is not None, eq=True)

    def test_grpc_namespace_exists(self) -> None:
        """Test that Grpc namespace exists."""
        tm.that(hasattr(FlextGrpcProtocols, "Grpc"), eq=True)

    def test_server_protocol_exists(self) -> None:
        """Test that Server exists."""
        tm.that(hasattr(FlextGrpcProtocols.Grpc, "Server"), eq=True)

    def test_client_protocol_exists(self) -> None:
        """Test that Client exists."""
        tm.that(hasattr(FlextGrpcProtocols.Grpc, "Client"), eq=True)

    def test_streaming_protocol_exists(self) -> None:
        """Test that Streaming exists."""
        tm.that(hasattr(FlextGrpcProtocols.Grpc, "Streaming"), eq=True)

    def test_service_protocol_exists(self) -> None:
        """Test that Service exists."""
        tm.that(hasattr(FlextGrpcProtocols.Grpc, "Service"), eq=True)

    def test_channel_protocol_exists(self) -> None:
        """Test that Channel exists."""
        tm.that(hasattr(FlextGrpcProtocols.Grpc, "Channel"), eq=True)

    def test_metrics_protocol_exists(self) -> None:
        """Test that Metrics exists."""
        tm.that(hasattr(FlextGrpcProtocols.Grpc, "Metrics"), eq=True)

    def test_configuration_protocol_exists(self) -> None:
        """Test that Configuration exists."""
        tm.that(hasattr(FlextGrpcProtocols.Grpc, "Configuration"), eq=True)

    def test_protocols_are_protocols(self) -> None:
        """Test that protocols are proper Protocol subclasses."""
        tm.that(is_protocol(FlextGrpcProtocols.Grpc.Server), eq=True)
        tm.that(is_protocol(FlextGrpcProtocols.Grpc.Client), eq=True)
        tm.that(is_protocol(FlextGrpcProtocols.Grpc.Streaming), eq=True)
        tm.that(is_protocol(FlextGrpcProtocols.Grpc.Service), eq=True)
