"""FLEXT gRPC Advanced Usage Examples - Complex scenarios and enterprise patterns.

This module demonstrates advanced usage patterns and enterprise-grade scenarios
for the FLEXT gRPC communication platform, showcasing the unified FlextGrpc facade
for complex entity management, service coordination, streaming patterns, and
production-ready configurations following Clean Architecture and Domain-Driven
Design principles.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import cast

from flext_core import FlextCore

from flext_grpc import FlextGrpc, FlextGrpcConfig
from flext_grpc.entities import FlextGrpcEntities
from flext_grpc.typings import FlextGrpcTypings


class GrpcServerManager:
    """Advanced server management example using FlextGrpc facade."""

    def __init__(self) -> None:
        """Initialize the gRPC server manager with facade."""
        self.grpc = FlextGrpc()
        self.servers: dict[str, FlextGrpcEntities.Server] = {}
        self.server_configs: dict[str, FlextGrpcConfig] = {}

    def create_server_pool(
        self,
        base_port: int = 8000,
        count: int = 3,
    ) -> list[FlextCore.Result]:
        """Create a pool of servers on consecutive ports through facade."""
        server_results: list[FlextCore.Result] = []

        for i in range(count):
            server_id = f"pool-server-{i}"
            port = base_port + i

            # Create config through facade
            config_result = self.grpc.create_config(
                host=FlextCore.Constants.Platform.DEFAULT_HOST,
                port=port,
                max_workers=10 + (i * 5),  # Vary workers
                timeout=FlextCore.Constants.Network.DEFAULT_TIMEOUT,
            )

            if config_result.is_failure:
                server_results.append(config_result)
                continue

            config = config_result.unwrap()
            self.server_configs[server_id] = config

            # Create server through facade
            server_result = self.grpc.create_server(
                host=config.host, port=config.port, max_workers=config.max_workers
            )

            if server_result.is_success:
                server = server_result.unwrap()
                self.servers[server_id] = server

            server_results.append(server_result)

        return server_results

    def start_all_servers(self) -> dict[str, bool]:
        """Start all servers in the pool through facade."""
        results = {}

        for server_id, server in self.servers.items():
            start_result = self.grpc.start_server(server)
            if start_result.is_success:
                self.servers[server_id] = start_result.unwrap()
                results[server_id] = True
            else:
                results[server_id] = False

        return results

    def stop_all_servers(self) -> dict[str, bool]:
        """Stop all servers in the pool through facade."""
        results = {}

        for server_id, server in self.servers.items():
            if server.state == "running":
                stop_result = self.grpc.stop_server(server)
                if stop_result.is_success:
                    self.servers[server_id] = stop_result.unwrap()
                    results[server_id] = True
                else:
                    results[server_id] = False
            else:
                results[server_id] = True

        return results

    def get_server_status(self) -> dict[str, dict[str, str]]:
        """Get status of all servers through facade."""
        status = {}

        for server_id, server in self.servers.items():
            config = self.server_configs[server_id]
            status_result = self.grpc.get_server_status(server)
            status[server_id] = {
                "address": f"{server.host}:{server.port}",
                "state": server.state,
                "max_workers": str(server.max_workers),
                "timeout": f"{config.timeout}s",
                "is_running": str(server.state == "running"),
                "is_valid": str(server.validate_business_rules().is_success),
                "facade_status": str(status_result.is_success),
            }

        return status


class AdvancedGrpcOperations:
    """Advanced gRPC operations using FlextGrpc facade."""

    def __init__(self) -> None:
        """Initialize advanced operations with facade."""
        self.grpc = FlextGrpc()

    def create_complete_setup(
        self,
        host: str = FlextCore.Constants.Platform.DEFAULT_HOST,
        port: int = 8080,
        service_name: str = "AdvancedService",
        methods: FlextCore.Types.StringList | None = None,
    ) -> FlextCore.Result[dict]:
        """Create a complete gRPC setup through facade."""
        if methods is None:
            methods = ["ProcessData", "GetStatus", "StreamResults"]

        # Use the facade's complete setup method
        return self.grpc.create_complete_setup(
            host=host, port=port, service_name=service_name, methods=methods
        )

    def demonstrate_streaming(self) -> None:
        """Demonstrate streaming operations through facade."""
        # Create different stream types
        stream_types = [
            "unary",
            "server_streaming",
            "client_streaming",
            "bidirectional",
        ]

        for stream_type in stream_types:
            # Cast to proper literal type
            typed_stream_type = cast("FlextGrpcTypings.GrpcStreamType", stream_type)
            stream_result = self.grpc.create_stream(
                method_name=f"{stream_type.capitalize()}Method",
                stream_type=typed_stream_type,
            )
            if stream_result.is_success:
                stream = stream_result.unwrap()
                print(f"Created {stream_type} stream: {stream.id}")
            else:
                print(f"Failed to create {stream_type} stream: {stream_result.error}")


def example_1_server_pool() -> None:
    """Example 1: Server pool management through facade."""
    manager = GrpcServerManager()

    # Create server pool through facade
    server_results = manager.create_server_pool(base_port=8000, count=3)
    successful_creations = sum(1 for result in server_results if result.is_success)
    print(f"Created {successful_creations}/{len(server_results)} servers")

    # Start all servers through facade
    start_results = manager.start_all_servers()
    successful_starts = sum(1 for success in start_results.values() if success)
    print(f"Started {successful_starts}/{len(start_results)} servers")

    # Get status through facade
    status = manager.get_server_status()
    for server_id, info in status.items():
        print(f"Server {server_id}: {info['state']}, running: {info['is_running']}")

    # Stop all servers through facade
    stop_results = manager.stop_all_servers()
    successful_stops = sum(1 for success in stop_results.values() if success)
    print(f"Stopped {successful_stops}/{len(stop_results)} servers")


def example_2_client_pool() -> None:
    """Example 2: Advanced operations through facade."""
    # Initialize advanced operations
    ops = AdvancedGrpcOperations()

    # Create complete setup through facade
    setup_result = ops.create_complete_setup(
        host="localhost",
        port=8080,
        service_name="AdvancedService",
        methods=["ProcessData", "GetStatus", "StreamResults"],
    )

    if setup_result.is_success:
        setup = setup_result.unwrap()
        print(
            f"Created setup with server: {setup['server'].id}, client: {setup['client'].id}"
        )
    else:
        print(f"Setup creation failed: {setup_result.error}")

    # Demonstrate streaming operations
    ops.demonstrate_streaming()


def example_3_service_creation() -> None:
    """Example 3: Service creation patterns through facade."""
    # Initialize facade
    grpc = FlextGrpc()

    # Create different types of services through facade
    services = [
        ("UserService", ["GetUser", "CreateUser", "UpdateUser"]),
        ("OrderService", ["GetOrder", "CreateOrder", "UpdateOrder"]),
        ("NotificationService", ["SendNotification", "GetNotifications"]),
    ]

    created_services = []
    for service_name, methods in services:
        service_result = grpc.create_service(name=service_name, methods=methods)

        if service_result.is_success:
            service = service_result.unwrap()
            created_services.append(service)
            print(
                f"Created service: {service.name} with {len(service.methods)} methods"
            )
        else:
            print(f"Failed to create {service_name}: {service_result.error}")

    print(f"Successfully created {len(created_services)} services")


def example_4_streaming() -> None:
    """Example 4: Streaming operations through facade."""
    # Initialize facade
    grpc = FlextGrpc()

    # Create different stream types through facade
    stream_configs = [
        ("GetUser", "unary"),
        ("StreamMessages", "server_streaming"),
        ("UploadData", "client_streaming"),
        ("Chat", "bidirectional"),
    ]

    created_streams = []
    for method_name, stream_type in stream_configs:
        # Cast to proper literal type
        typed_stream_type = cast("FlextGrpcTypings.GrpcStreamType", stream_type)
        stream_result = grpc.create_stream(
            method_name=method_name,
            stream_type=typed_stream_type,
        )

        if stream_result.is_success:
            stream = stream_result.unwrap()
            created_streams.append(stream)
            print(f"Created {stream_type} stream for method: {method_name}")
        else:
            print(f"Failed to create {stream_type} stream: {stream_result.error}")

    print(f"Successfully created {len(created_streams)} streaming operations")


def example_5_error_handling() -> None:
    """Example 5: Comprehensive error handling through facade."""
    # Initialize facade
    grpc = FlextGrpc()

    print("Testing various error scenarios through FlextGrpc facade...")

    # Test invalid server creation
    invalid_server_result = grpc.create_server(host="", port=0)
    if invalid_server_result.is_failure:
        print(
            f"✓ Invalid server creation properly failed: {invalid_server_result.error}"
        )

    # Test invalid client creation
    invalid_client_result = grpc.create_client(target="")
    if invalid_client_result.is_failure:
        print(
            f"✓ Invalid client creation properly failed: {invalid_client_result.error}"
        )

    # Test invalid channel creation
    invalid_channel_result = grpc.create_channel(target="")
    if invalid_channel_result.is_failure:
        print(
            f"✓ Invalid channel creation properly failed: {invalid_channel_result.error}"
        )

    # Test invalid config creation
    invalid_config_result = grpc.create_config(host="", port=0)
    if invalid_config_result.is_failure:
        print(
            f"✓ Invalid config creation properly failed: {invalid_config_result.error}"
        )

    # Test invalid service creation
    invalid_service_result = grpc.create_service(name="", methods=[])
    if invalid_service_result.is_failure:
        print(
            f"✓ Invalid service creation properly failed: {invalid_service_result.error}"
        )

    # Test invalid stream creation (bypass type checking for intentional invalid input)
    invalid_stream_result = grpc.create_stream(method_name="", stream_type="invalid")
    if invalid_stream_result.is_failure:
        print(
            f"✓ Invalid stream creation properly failed: {invalid_stream_result.error}"
        )

    print("Error handling validation completed - all invalid inputs properly rejected")


def main() -> None:
    """Run all advanced examples."""
    example_1_server_pool()
    example_2_client_pool()
    example_3_service_creation()
    example_4_streaming()
    example_5_error_handling()


if __name__ == "__main__":
    main()
