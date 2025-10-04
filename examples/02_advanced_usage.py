"""FLEXT gRPC Advanced Usage Examples - Complex scenarios and enterprise patterns.

This module demonstrates advanced usage patterns and enterprise-grade scenarios
for the FLEXT gRPC communication platform, showcasing complex entity management,
service coordination, streaming patterns, and production-ready configurations
following Clean Architecture and Domain-Driven Design principles.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import contextlib
from datetime import UTC, datetime

from flext_core import FlextConstants, FlextTypes

from flext_grpc import (
    FlextGrpcChannel,
    FlextGrpcClient,
    FlextGrpcClientService,
    FlextGrpcConfig,
    FlextGrpcConstants,
    FlextGrpcServer,
    FlextGrpcServerService,
    FlextGrpcStream,
)
from flext_grpc.entities import FlextGrpcService
from flext_grpc.typings import FlextGrpcTypes


class GrpcServerManager:
    """Advanced server management example."""

    def __init__(self) -> None:
        """Initialize the gRPC server manager."""
        self.server_service = FlextGrpcServerService()
        self.servers: dict[str, FlextGrpcServer] = {}
        self.server_configs: dict[str, FlextGrpcConfig] = {}

    def create_server_pool(
        self,
        base_port: int = 8000,
        count: int = 3,
    ) -> list[FlextGrpcServer]:
        """Create a pool of servers on consecutive ports."""
        servers: list[FlextGrpcServer] = []

        for i in range(count):
            server_id = f"pool-server-{i}"
            port = base_port + i

            config = FlextGrpcConfig(
                host=FlextConstants.Platform.DEFAULT_HOST,
                port=port,
                max_workers=10 + (i * 5),  # Vary workers
                timeout=FlextConstants.Network.DEFAULT_TIMEOUT,
            )

            server = FlextGrpcServer(
                id=server_id,
                host=config.host,
                port=config.port,
                max_workers=config.max_workers,
                created_at=datetime.now(UTC),
            )

            self.servers[server_id] = server
            self.server_configs[server_id] = config
            servers.append(server)

        return servers

    def start_all_servers(self) -> FlextTypes.BoolDict:
        """Start all servers in the pool."""
        results = {}

        for server_id, server in self.servers.items():
            start_result = self.server_service.execute("start", server)
            if start_result.is_success and isinstance(
                start_result.data, FlextGrpcServer
            ):
                self.servers[server_id] = start_result.data
                results[server_id] = True
            else:
                results[server_id] = False

        return results

    def stop_all_servers(self) -> FlextTypes.BoolDict:
        """Stop all servers in the pool."""
        results = {}

        for server_id, server in self.servers.items():
            if server.is_running:
                stop_result = self.server_service.execute("stop", server)
                if stop_result.is_success and isinstance(
                    stop_result.data,
                    FlextGrpcServer,
                ):
                    self.servers[server_id] = stop_result.data
                    results[server_id] = True
                else:
                    results[server_id] = False
            else:
                results[server_id] = True

        return results

    def get_server_status(self) -> dict[str, FlextGrpcTypes.Core.GrpcHeaders]:
        """Get status of all servers."""
        status = {}

        for server_id, server in self.servers.items():
            config = self.server_configs[server_id]
            status[server_id] = {
                "address": server.address,
                "state": server.state,
                "max_workers": str(server.max_workers),
                "timeout": f"{config.timeout}s",
                "is_running": str(server.is_running),
                "is_valid": str(server.validate_business_rules().is_success),
            }

        return status


class GrpcClientPool:
    """Advanced client pool management."""

    def __init__(self) -> None:
        """Initialize the gRPC client pool."""
        self.client_service = FlextGrpcClientService()
        self.clients: dict[str, FlextGrpcClient] = {}
        self.connection_status: FlextTypes.BoolDict = {}

    def create_clients_for_servers(
        self,
        servers: list[FlextGrpcServer],
    ) -> list[FlextGrpcClient]:
        """Create clients for a list of servers."""
        clients: list[FlextGrpcClient] = []

        for i, server in enumerate(servers):
            client_id = f"client-for-{server.id}"
            target = server.address

            channel = FlextGrpcChannel(
                id=f"channel-{i}",
                target=target,  # GrpcTarget is type alias, not constructor
                created_at=datetime.now(UTC),
            )

            client = FlextGrpcClient(
                id=client_id,
                channel=channel,
                created_at=datetime.now(UTC),
            )

            self.clients[client_id] = client
            self.connection_status[client_id] = False
            clients.append(client)

        return clients

    def connect_all_clients(self) -> FlextTypes.BoolDict:
        """Connect all clients in the pool."""
        results = {}

        for client_id, client in self.clients.items():
            connect_result = self.client_service.execute("connect", client)
            if connect_result.is_success and isinstance(
                connect_result.data,
                FlextGrpcClient,
            ):
                self.clients[client_id] = connect_result.data
                self.connection_status[client_id] = True
                results[client_id] = True
            else:
                results[client_id] = False

        return results

    def broadcast_call(
        self,
        method_name: str,
        data: object = None,
    ) -> FlextGrpcTypes.Core.GrpcDict:
        """Broadcast a method call to all connected clients."""
        results = {}

        for client_id, client in self.clients.items():
            if self.connection_status[client_id] and client.is_connected:
                call_result = self.client_service.execute(
                    "call",
                    client,
                    method_name=method_name,
                    data=data,
                )
                if call_result.is_success:
                    results[client_id] = call_result.data or {
                        "method": method_name,
                        "status": "success",
                    }
                else:
                    results[client_id] = {"error": call_result.error}
            else:
                results[client_id] = {"error": "Client not connected"}

        return results


class ServiceRegistry:
    """Service registration and discovery example."""

    def __init__(self) -> None:
        """Initialize the service registry."""
        self.services: dict[str, FlextGrpcService] = {}
        self.service_servers: FlextGrpcTypes.Core.GrpcHeaders = {}  # service_id -> server_id

    def register_service(self, service: FlextGrpcService, server_id: str) -> bool:
        """Register a service with a server."""
        validation = service.validate_business_rules()
        if validation.is_failure:
            return False

        self.services[str(service.id)] = service
        self.service_servers[str(service.id)] = server_id
        return True

    def discover_services(self) -> dict[str, FlextGrpcTypes.Core.GrpcDict]:
        """Discover all registered services."""
        discovery = {}

        for service_id, service in self.services.items():
            server_id = self.service_servers[service_id]
            discovery[service_id] = {
                "name": service.name,
                "methods": service.methods,
                "server_id": server_id,
                "method_count": len(service.methods),
            }

        return discovery

    def find_service_by_method(
        self, method_name: str
    ) -> list[FlextGrpcTypes.Core.GrpcHeaders]:
        """Find services that support a specific method."""
        matches: list[FlextTypes.StringDict] = []

        for service_id, service in self.services.items():
            if service.has_method(method_name):
                server_id = self.service_servers[service_id]
                matches.append(
                    {
                        "service_id": service_id,
                        "service_name": service.name,
                        "server_id": server_id,
                    },
                )

        return matches


def example_1_server_pool() -> None:
    """Example 1: Server pool management."""
    manager = GrpcServerManager()

    # Create server pool
    manager.create_server_pool(base_port=8000, count=3)

    # Start all servers
    start_results = manager.start_all_servers()
    sum(1 for success in start_results.values() if success)

    # Get status
    status = manager.get_server_status()
    for _server_id, _info in status.items():
        pass

    # Stop all servers
    stop_results = manager.stop_all_servers()
    sum(1 for success in stop_results.values() if success)


def example_2_client_pool() -> None:
    """Example 2: Client pool and broadcasting."""
    # Create servers first
    server_manager = GrpcServerManager()
    servers = server_manager.create_server_pool(base_port=8100, count=2)
    server_manager.start_all_servers()

    # Create client pool
    client_pool = GrpcClientPool()
    client_pool.create_clients_for_servers(servers)

    # Connect all clients
    connect_results = client_pool.connect_all_clients()
    sum(1 for success in connect_results.values() if success)

    # Broadcast method calls
    broadcast_results = client_pool.broadcast_call(
        "GetStatus",
        {"timestamp": datetime.now(UTC).isoformat()},
    )

    for result in broadcast_results.values():
        if isinstance(result, dict) and "error" not in result:
            pass

    # Cleanup
    server_manager.stop_all_servers()


def example_3_service_registry() -> None:
    """Example 3: Service registry and discovery."""
    registry = ServiceRegistry()

    # Register multiple services
    user_service = FlextGrpcService(
        id="user-service",
        name="UserService",
        methods=["GetUser", "CreateUser", "UpdateUser", "DeleteUser", "ListUsers"],
        created_at=datetime.now(UTC),
    )

    order_service = FlextGrpcService(
        id="order-service",
        name="OrderService",
        methods=["GetOrder", "CreateOrder", "UpdateOrder", "CancelOrder", "ListOrders"],
        created_at=datetime.now(UTC),
    )

    notification_service = FlextGrpcService(
        id="notification-service",
        name="NotificationService",
        methods=["SendNotification", "GetNotifications", "MarkAsRead"],
        created_at=datetime.now(UTC),
    )

    # Register services with different servers
    registry.register_service(user_service, "server-1")
    registry.register_service(order_service, "server-2")
    registry.register_service(notification_service, "server-3")

    # Discover all services
    discovery = registry.discover_services()
    for _info in discovery.values():
        pass

    # Find services by method
    get_services = registry.find_service_by_method("GetUser")
    create_services = registry.find_service_by_method("CreateOrder")

    for _service in get_services:
        pass

    for _service in create_services:
        pass


def example_4_streaming() -> None:
    """Example 4: Streaming scenarios."""
    # Create different stream types
    streams = [
        FlextGrpcStream(
            id="unary-stream",
            method_name="GetUser",
            stream_type="unary",
            created_at=datetime.now(UTC),
        ),
        FlextGrpcStream(
            id="server-stream",
            method_name="StreamMessages",
            stream_type="server_streaming",
            created_at=datetime.now(UTC),
        ),
        FlextGrpcStream(
            id="client-stream",
            method_name="UploadData",
            stream_type="client_streaming",
            created_at=datetime.now(UTC),
        ),
        FlextGrpcStream(
            id="bidi-stream",
            method_name="Chat",
            stream_type="bidirectional",
            created_at=datetime.now(UTC),
        ),
    ]

    for stream in streams:
        validation = stream.validate_business_rules()
        if validation.is_failure:
            pass


def example_5_error_handling() -> None:
    """Example 5: Comprehensive error handling."""
    server_service = FlextGrpcServerService()

    # Server error scenarios

    # Try to start invalid server
    try:
        invalid_server = FlextGrpcServer(
            id="invalid-server",
            host="",  # Invalid
            port=0,  # Invalid
            created_at=datetime.now(UTC),
        )
        invalid_server.validate_business_rules()
    except (RuntimeError, ValueError, TypeError):
        pass

    # Try to start already running server
    server = FlextGrpcServer(
        id="test-server",
        created_at=datetime.now(UTC),
    )

    start1 = server_service.execute("start", server)
    if start1.is_success and isinstance(start1.data, FlextGrpcServer):
        running_server = start1.data
        server_service.execute("start", running_server)

    # Client error scenarios

    # Try to connect client without channel
    no_channel_client = FlextGrpcClient(
        id="no-channel-client",
        channel=None,
        created_at=datetime.now(UTC),
    )

    client_service = FlextGrpcClientService()
    client_service.execute("connect", no_channel_client)

    # Try to call method on disconnected client
    channel = FlextGrpcChannel(
        id="test-channel",
        target=f"{FlextConstants.Platform.DEFAULT_HOST}:{FlextGrpcConstants.DEFAULT_GRPC_PORT}",
        created_at=datetime.now(UTC),
    )

    disconnected_client = FlextGrpcClient(
        id="disconnected-client",
        channel=channel,
        created_at=datetime.now(UTC),
    )

    client_service.execute("call", disconnected_client, method_name="TestMethod")

    # Configuration error scenarios

    with contextlib.suppress(Exception):
        FlextGrpcConfig(host="")

    with contextlib.suppress(Exception):
        FlextGrpcConfig(port=0)

    with contextlib.suppress(Exception):
        FlextGrpcConfig(max_workers=0)

    with contextlib.suppress(Exception):
        FlextGrpcConfig(timeout=-1.0)


def main() -> None:
    """Run all advanced examples."""
    example_1_server_pool()
    example_2_client_pool()
    example_3_service_registry()
    example_4_streaming()
    example_5_error_handling()


if __name__ == "__main__":
    main()
