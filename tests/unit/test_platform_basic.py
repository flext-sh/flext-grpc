"""Basic tests for flext_grpc.platform module.

Tests the main FlextGrpcPlatform class with basic functionality.
"""

from __future__ import annotations

from datetime import UTC, datetime
from unittest.mock import MagicMock, patch

from flext_grpc.entities import FlextGrpcClient, FlextGrpcServer
from flext_grpc.platform import FlextGrpcPlatform


class TestFlextGrpcPlatformBasic:
    """Test the main FlextGrpcPlatform class with basic tests."""

    def test_init_default(self) -> None:
        """Test platform initialization with default config."""
        platform = FlextGrpcPlatform()
        assert isinstance(platform, FlextGrpcPlatform)
        assert platform.config == {}
        assert platform.container is not None
        assert platform.service is not None

    def test_init_with_config(self) -> None:
        """Test platform initialization with custom config."""
        config = {"test": "value", "port": 50051}
        platform = FlextGrpcPlatform(config)
        assert platform.config == config

    def test_execute(self) -> None:
        """Test the execute method."""
        platform = FlextGrpcPlatform()
        result = platform.execute()

        assert result.is_success
        assert result.data is not None
        assert result.data["status"] == "operational"
        assert result.data["platform"] == "flext-grpc"
        assert "capabilities" in result.data

    def test_config_property(self) -> None:
        """Test config property."""
        config = {"test": "value"}
        platform = FlextGrpcPlatform(config)
        assert platform.config == config

    def test_container_property(self) -> None:
        """Test container property."""
        platform = FlextGrpcPlatform()
        container = platform.container
        assert container is not None

    def test_service_property(self) -> None:
        """Test service property."""
        platform = FlextGrpcPlatform()
        service = platform.service
        assert service is not None

    def test_start_server(self) -> None:
        """Test start_server method."""
        platform = FlextGrpcPlatform()
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            max_workers=10,
            services=[],
            created_at=datetime.now(UTC),
        )

        with patch.object(platform.ServerManagement, "start_server") as mock_start:
            mock_result = MagicMock()
            mock_result.is_success = True
            mock_result.value = server
            mock_start.return_value = mock_result

            result = platform.start_server(server)

        assert result.is_success
        mock_start.assert_called_once_with(server)

    def test_stop_server(self) -> None:
        """Test stop_server method."""
        platform = FlextGrpcPlatform()
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            max_workers=10,
            services=[],
            created_at=datetime.now(UTC),
        )

        with patch.object(platform.ServerManagement, "stop_server") as mock_stop:
            mock_result = MagicMock()
            mock_result.is_success = True
            mock_result.value = server
            mock_stop.return_value = mock_result

            result = platform.stop_server(server)

        assert result.is_success
        mock_stop.assert_called_once_with(server)

    def test_connect_client(self) -> None:
        """Test connect_client method."""
        platform = FlextGrpcPlatform()
        client = FlextGrpcClient(
            id="test-client",
            target="localhost:50051",
            channel=None,
            created_at=datetime.now(UTC),
        )

        with patch.object(platform.ClientManagement, "connect_client") as mock_connect:
            mock_result = MagicMock()
            mock_result.is_success = True
            mock_result.value = client
            mock_connect.return_value = mock_result

            result = platform.connect_client(client)

        assert result.is_success
        mock_connect.assert_called_once_with(client)

    def test_get_client_status(self) -> None:
        """Test get_client_status method."""
        platform = FlextGrpcPlatform()
        client = FlextGrpcClient(
            id="test-client",
            target="localhost:50051",
            channel=None,
            created_at=datetime.now(UTC),
        )

        with patch("flext_grpc.platform.FlextGrpcService") as mock_service_class:
            mock_service = MagicMock()
            mock_service_class.return_value = mock_service
            mock_result = MagicMock()
            mock_result.is_success = True
            mock_result.unwrap.return_value = {"status": "connected"}
            mock_service.execute.return_value = mock_result

            result = platform.get_client_status(client)

        assert result.is_success
        assert result.value["status"] == "connected"

    def test_get_status(self) -> None:
        """Test get_server_status method."""
        platform = FlextGrpcPlatform()
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            max_workers=10,
            services=[],
            created_at=datetime.now(UTC),
        )

        with patch.object(
            platform.ServerManagement, "get_server_status"
        ) as mock_status:
            mock_result = MagicMock()
            mock_result.is_success = True
            mock_result.value = {"status": "running"}
            mock_status.return_value = mock_result

            result = platform.get_server_status(server)

        assert result.is_success
        mock_status.assert_called_once_with(server)

    def test_server_operation(self) -> None:
        """Test server_operation method."""
        platform = FlextGrpcPlatform()
        server = FlextGrpcServer(
            id="test-server",
            host="localhost",
            port=50051,
            max_workers=10,
            services=[],
            created_at=datetime.now(UTC),
        )

        with patch("flext_grpc.platform.FlextGrpcService") as mock_service_class:
            mock_service = MagicMock()
            mock_service_class.return_value = mock_service
            mock_result = MagicMock()
            mock_result.is_success = True
            mock_result.unwrap.return_value = server
            mock_service.execute.return_value = mock_result

            result = platform.server_operation("test_op", server, arg1="value1")

        assert result.is_success

    def test_create_server_setup(self) -> None:
        """Test create_server_setup method."""
        platform = FlextGrpcPlatform()

        with patch("flext_grpc.platform.create_server") as mock_create_server:
            mock_server = FlextGrpcServer(
                id="test-server",
                host="localhost",
                port=50051,
                max_workers=10,
                services=[],
                created_at=datetime.now(UTC),
            )
            mock_create_server.return_value = mock_server

            result = platform.create_server_setup(
                host="localhost",
                port=50051,
                max_workers=10,
                service_name="test-service",
                methods=["TestMethod"],
            )

        assert result.is_success

    def test_create_client_setup(self) -> None:
        """Test create_client_setup method."""
        platform = FlextGrpcPlatform()

        with patch("flext_grpc.platform.create_client") as mock_create_client:
            mock_client = FlextGrpcClient(
                id="test-client",
                target="localhost:50051",
                channel=None,
                created_at=datetime.now(UTC),
            )
            mock_create_client.return_value = mock_client

            result = platform.create_client_setup(target="localhost:50051")

        assert result.is_success
