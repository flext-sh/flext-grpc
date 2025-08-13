"""FLEXT gRPC Advanced Usage Examples - Complex scenarios and enterprise patterns.

This module demonstrates advanced usage patterns and enterprise-grade scenarios
for the FLEXT gRPC communication platform, showcasing complex entity management,
service coordination, streaming patterns, and production-ready configurations
following Clean Architecture and Domain-Driven Design principles.

Advanced Example Categories:
    The module provides comprehensive examples of advanced FLEXT gRPC functionality:
    - Complex Entity Management: Multi-entity coordination and lifecycle management
    - Service Coordination: Cross-service operations and dependency management
    - Streaming Patterns: Stream entity usage and streaming type validation
    - Platform Integration: FlextGrpcPlatform usage for unified operations
    - Production Configurations: Enterprise-grade configuration and deployment patterns

Current Implementation Status:
    - ✅ Complex Entity Patterns: Advanced entity lifecycle and coordination examples
    - ✅ Service Integration: Service coordination and platform integration examples
    - ✅ Stream Entities: Stream creation and type validation examples
    - ✅ Production Patterns: Enterprise configuration and deployment examples
    - ⚠️ Real Streaming: Limited by lack of Protocol Buffer implementation

Advanced Patterns Demonstrated:
    - Multi-Entity Coordination: Server, client, and service coordination patterns
    - Platform Operations: FlextGrpcPlatform facade usage for unified management
    - Stream Management: Stream entity creation with type safety validation
    - Configuration Management: Advanced configuration patterns for production
    - Error Recovery: Advanced error handling and recovery strategies

Example:
    Advanced platform integration pattern:

    >>> from flext_grpc import FlextGrpcPlatform, create_complete_setup
    >>> from flext_grpc.services import FlextGrpcService
    >>>
    >>> # Create complete setup with platform integration
    >>> setup = create_complete_setup(
    ...     host="api.production.com",
    ...     port=443,
    ...     service_name="ProductionService",
    ...     methods=["ProcessData", "GetStatus"],
    ... )
    >>>
    >>> platform = FlextGrpcPlatform()
    >>> server_result = platform.service.execute("validate", setup["server"])
    >>>
    >>> if server_result.success:
    ...     print("Advanced setup validated successfully")

Usage:
    Run this example to see FLEXT gRPC advanced functionality:

    >>> poetry run python examples/advanced_usage.py

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from datetime import UTC, datetime

from flext_grpc import (
    FlextGrpcChannel,
    FlextGrpcClient,
    FlextGrpcConfig,
    FlextGrpcServer,
    FlextGrpcService,
    FlextGrpcStream,
)
from flext_grpc.services import GrpcOperations
from flext_grpc.types import TGrpcTarget


class GrpcServerManager:
    """Advanced server management example."""

    def __init__(self) -> None:
        self.operations = GrpcOperations()
        self.servers: dict[str, FlextGrpcServer] = {}
        self.server_configs: dict[str, FlextGrpcConfig] = {}

    def create_server_pool(
        self, base_port: int = 8000, count: int = 3,
    ) -> list[FlextGrpcServer]:
        """Create a pool of servers on consecutive ports."""
        servers = []

        for i in range(count):
            server_id = f"pool-server-{i}"
            port = base_port + i

            config = FlextGrpcConfig(
                host="localhost",
                port=port,
                max_workers=10 + (i * 5),  # Vary workers
                timeout=30.0,
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

    def start_all_servers(self) -> dict[str, bool]:
        """Start all servers in the pool."""
        results = {}

        for server_id, server in self.servers.items():
            start_result = self.operations.start_server(server)
            if start_result.success:
                self.servers[server_id] = start_result.data
                results[server_id] = True
                print(f"✅ Started server {server_id} on {server.get_address()}")
            else:
                results[server_id] = False
                print(f"❌ Failed to start server {server_id}: {start_result.error}")

        return results

    def stop_all_servers(self) -> dict[str, bool]:
        """Stop all servers in the pool."""
        results = {}

        for server_id, server in self.servers.items():
            if server.is_running():
                stop_result = self.operations.stop_server(server)
                if stop_result.success:
                    self.servers[server_id] = stop_result.data
                    results[server_id] = True
                    print(f"✅ Stopped server {server_id}")
                else:
                    results[server_id] = False
                    print(f"❌ Failed to stop server {server_id}: {stop_result.error}")
            else:
                results[server_id] = True
                print(f"i Server {server_id} already stopped")

        return results

    def get_server_status(self) -> dict[str, dict[str, str]]:
        """Get status of all servers."""
        status = {}

        for server_id, server in self.servers.items():
            config = self.server_configs[server_id]
            status[server_id] = {
                "address": server.get_address(),
                "state": server.state,
                "max_workers": str(server.max_workers),
                "timeout": f"{config.timeout}s",
                "is_running": str(server.is_running()),
                "is_valid": str(server.is_valid()),
            }

        return status


class GrpcClientPool:
    """Advanced client pool management."""

    def __init__(self) -> None:
        self.operations = GrpcOperations()
        self.clients: dict[str, FlextGrpcClient] = {}
        self.connection_status: dict[str, bool] = {}

    def create_clients_for_servers(
        self, servers: list[FlextGrpcServer],
    ) -> list[FlextGrpcClient]:
        """Create clients for a list of servers."""
        clients = []

        for i, server in enumerate(servers):
            client_id = f"client-for-{server.id}"
            target = server.get_address()

            channel = FlextGrpcChannel(
                id=f"channel-{i}",
                target=TGrpcTarget(target),
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

    def connect_all_clients(self) -> dict[str, bool]:
        """Connect all clients in the pool."""
        results = {}

        for client_id, client in self.clients.items():
            connect_result = self.operations.connect_client(client)
            if connect_result.success:
                self.clients[client_id] = connect_result.data
                self.connection_status[client_id] = True
                results[client_id] = True
                print(f"✅ Connected client {client_id} to {client.channel.target}")
            else:
                results[client_id] = False
                print(
                    f"❌ Failed to connect client {client_id}: {connect_result.error}",
                )

        return results

    def broadcast_call(
        self, method_name: str, data: object = None,
    ) -> dict[str, object]:
        """Broadcast a method call to all connected clients."""
        results = {}

        for client_id, client in self.clients.items():
            if self.connection_status[client_id] and client.is_connected():
                call_result = self.operations.call_method(client, method_name, data)
                if call_result.success:
                    results[client_id] = call_result.data
                    print(f"✅ Called {method_name} on {client_id}")
                else:
                    results[client_id] = {"error": call_result.error}
                    print(
                        f"❌ Failed to call {method_name} on {client_id}: "
                        f"{call_result.error}",
                    )
            else:
                results[client_id] = {"error": "Client not connected"}
                print(f"⚠️ Client {client_id} not connected")

        return results


class ServiceRegistry:
    """Service registration and discovery example."""

    def __init__(self) -> None:
        self.services: dict[str, FlextGrpcService] = {}
        self.service_servers: dict[str, str] = {}  # service_id -> server_id

    def register_service(self, service: FlextGrpcService, server_id: str) -> bool:
        """Register a service with a server."""
        validation = service.validate_domain_rules()
        if validation.is_failure:
            print(f"❌ Service validation failed: {validation.error}")
            return False

        self.services[service.id] = service
        self.service_servers[service.id] = server_id
        print(f"✅ Registered service {service.name} with server {server_id}")
        return True

    def discover_services(self) -> dict[str, dict[str, object]]:
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

    def find_service_by_method(self, method_name: str) -> list[dict[str, str]]:
        """Find services that support a specific method."""
        matches = []

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
    print("=== Example 1: Server Pool Management ===")

    manager = GrpcServerManager()

    # Create server pool
    servers = manager.create_server_pool(base_port=8000, count=3)
    print(f"Created {len(servers)} servers")

    # Start all servers
    start_results = manager.start_all_servers()
    started_count = sum(1 for success in start_results.values() if success)
    print(f"Started {started_count}/{len(servers)} servers")

    # Get status
    status = manager.get_server_status()
    print("\nServer Status:")
    for server_id, info in status.items():
        print(
            f"  {server_id}: {info['address']} ({info['state']}) - "
            f"{info['max_workers']} workers",
        )

    # Stop all servers
    stop_results = manager.stop_all_servers()
    stopped_count = sum(1 for success in stop_results.values() if success)
    print(f"Stopped {stopped_count}/{len(servers)} servers")

    print()


def example_2_client_pool() -> None:
    """Example 2: Client pool and broadcasting."""
    print("=== Example 2: Client Pool and Broadcasting ===")

    # Create servers first
    server_manager = GrpcServerManager()
    servers = server_manager.create_server_pool(base_port=8100, count=2)
    server_manager.start_all_servers()

    # Create client pool
    client_pool = GrpcClientPool()
    clients = client_pool.create_clients_for_servers(servers)
    print(f"Created {len(clients)} clients")

    # Connect all clients
    connect_results = client_pool.connect_all_clients()
    connected_count = sum(1 for success in connect_results.values() if success)
    print(f"Connected {connected_count}/{len(clients)} clients")

    # Broadcast method calls
    print("\nBroadcasting 'GetStatus' call:")
    broadcast_results = client_pool.broadcast_call(
        "GetStatus", {"timestamp": datetime.now(UTC).isoformat()},
    )

    for client_id, result in broadcast_results.items():
        if "error" not in result:
            print(f"  {client_id}: {result['status']} - {result['method']}")
        else:
            print(f"  {client_id}: Error - {result['error']}")

    # Cleanup
    server_manager.stop_all_servers()

    print()


def example_3_service_registry() -> None:
    """Example 3: Service registry and discovery."""
    print("=== Example 3: Service Registry and Discovery ===")

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
    print("Registered Services:")
    for info in discovery.values():
        print(
            f"  {info['name']}: {info['method_count']} methods on {info['server_id']}",
        )

    # Find services by method
    get_services = registry.find_service_by_method("GetUser")
    create_services = registry.find_service_by_method("CreateOrder")

    print(f"\nServices with 'GetUser' method: {len(get_services)}")
    for service in get_services:
        print(f"  {service['service_name']} on {service['server_id']}")

    print(f"\nServices with 'CreateOrder' method: {len(create_services)}")
    for service in create_services:
        print(f"  {service['service_name']} on {service['server_id']}")

    print()


def example_4_streaming() -> None:
    """Example 4: Streaming scenarios."""
    print("=== Example 4: Streaming Scenarios ===")

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

    print("Stream Analysis:")
    for stream in streams:
        validation = stream.validate_domain_rules()
        print(f"  {stream.method_name} ({stream.stream_type}):")
        print(f"    Valid: {validation.success}")
        print(f"    Is Streaming: {stream.is_streaming()}")
        if validation.is_failure:
            print(f"    Error: {validation.error}")

    print()


def example_5_error_handling() -> None:
    """Example 5: Comprehensive error handling."""
    print("=== Example 5: Error Handling Patterns ===")

    ops = GrpcOperations()

    # Server error scenarios
    print("Server Error Scenarios:")

    # Try to start invalid server
    try:
        invalid_server = FlextGrpcServer(
            id="invalid-server",
            host="",  # Invalid
            port=0,  # Invalid
            created_at=datetime.now(UTC),
        )
        validation = invalid_server.validate_domain_rules()
        print(f"  Invalid server validation: {validation.error}")
    except (RuntimeError, ValueError, TypeError) as e:
        print(f"  Server creation failed: {e}")

    # Try to start already running server
    server = FlextGrpcServer(
        id="test-server",
        created_at=datetime.now(UTC),
    )

    start1 = ops.start_server(server)
    if start1.success:
        running_server = start1.data
        start2 = ops.start_server(running_server)
        print(f"  Double start error: {start2.error}")

    # Client error scenarios
    print("\nClient Error Scenarios:")

    # Try to connect client without channel
    no_channel_client = FlextGrpcClient(
        id="no-channel-client",
        channel=None,
        created_at=datetime.now(UTC),
    )

    connect_result = ops.connect_client(no_channel_client)
    print(f"  No channel error: {connect_result.error}")

    # Try to call method on disconnected client
    channel = FlextGrpcChannel(
        id="test-channel",
        target=TGrpcTarget("localhost:50051"),
        created_at=datetime.now(UTC),
    )

    disconnected_client = FlextGrpcClient(
        id="disconnected-client",
        channel=channel,
        created_at=datetime.now(UTC),
    )

    call_result = ops.call_method(disconnected_client, "TestMethod")
    print(f"  Disconnected call error: {call_result.error}")

    # Configuration error scenarios
    print("\nConfiguration Error Scenarios:")

    try:
        FlextGrpcConfig(host="")
    except (RuntimeError, ValueError, TypeError) as e:
        print(f"  Empty host error: {e}")

    try:
        FlextGrpcConfig(port=0)
    except (RuntimeError, ValueError, TypeError) as e:
        print(f"  Invalid port error: {e}")

    try:
        FlextGrpcConfig(max_workers=0)
    except (RuntimeError, ValueError, TypeError) as e:
        print(f"  Invalid workers error: {e}")

    try:
        FlextGrpcConfig(timeout=-1.0)
    except (RuntimeError, ValueError, TypeError) as e:
        print(f"  Invalid timeout error: {e}")

    print()


def main() -> None:
    """Run all advanced examples."""
    print("FLEXT gRPC Library - Advanced Usage Examples")
    print("=============================================")
    print()

    example_1_server_pool()
    example_2_client_pool()
    example_3_service_registry()
    example_4_streaming()
    example_5_error_handling()

    print("All advanced examples completed!")
    print()
    print("Advanced Patterns Demonstrated:")
    print("- Server pool management with automatic port allocation")
    print("- Client pool with broadcast messaging capabilities")
    print("- Service registry and discovery patterns")
    print("- Streaming type analysis and validation")
    print("- Comprehensive error handling and validation")
    print("- Clean separation of concerns between entities and operations")
    print("- Strong typing with domain validation")


if __name__ == "__main__":
    main()
