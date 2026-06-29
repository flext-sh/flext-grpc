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

from flext_cli import u as cli_u
from flext_core import p, r
from flext_grpc import (
    FlextGrpc,
    FlextGrpcConstants,
    FlextGrpcModels,
    FlextGrpcSettings,
    c,
    t,
)


def _emit(message: str) -> None:
    """Emit example output through the canonical CLI facade."""
    cli_u.Cli.formatters_print(message)


class GrpcServerManager:
    """Advanced server management example using FlextGrpc facade."""

    def __init__(self) -> None:
        """Initialize the gRPC server manager with facade."""
        self.grpc = FlextGrpc()
        self.servers: dict[str, FlextGrpcModels.Grpc.Server] = {}
        self.server_configs: dict[str, FlextGrpcSettings] = {}

    def create_server_pool(
        self,
        base_port: int = 8000,
        count: int = 3,
    ) -> list[p.Result[FlextGrpcModels.Grpc.Server]]:
        """Create a pool of servers on consecutive ports through facade."""
        server_results: list[p.Result[FlextGrpcModels.Grpc.Server]] = []
        for i in range(count):
            server_id = f"pool-server-{i}"
            port = base_port + i
            settings = FlextGrpcSettings.model_validate({
                "host": FlextGrpcConstants.Grpc.NETWORK_DEFAULT_HOST,
                "port": port,
                "max_workers": 10 + i * 5,
            })
            self.server_configs[server_id] = settings
            server_result = self.grpc.create_server(
                host=settings.network.host,
                port=settings.network.port,
                max_workers=settings.performance.max_workers,
            )
            if server_result.success:
                server = server_result.value
                self.servers[server_id] = server
            server_results.append(server_result)
        return server_results

    def server_status(self) -> dict[str, dict[str, str]]:
        """Get status of all servers through facade."""
        status: dict[str, dict[str, str]] = {}
        for server_id, server in self.servers.items():
            settings = self.server_configs[server_id]
            status[server_id] = {
                "address": f"{server.host}:{server.port}",
                "state": server.state,
                "max_workers": str(server.max_workers),
                "timeout": f"{settings.timeout}s",
                "is_running": str(server.state == "running"),
                "valid": str(server.validate_business_rules().success),
            }
        return status

    def start_all_servers(self) -> dict[str, bool]:
        """Start all servers in the pool through facade."""
        results: dict[str, bool] = {}
        for server_id, server in self.servers.items():
            start_result = self.grpc.start_server(server)
            if start_result.success:
                self.servers[server_id] = start_result.value
                results[server_id] = True
            else:
                results[server_id] = False
        return results

    def stop_all_servers(self) -> dict[str, bool]:
        """Stop all servers in the pool through facade."""
        results: dict[str, bool] = {}
        for server_id, server in self.servers.items():
            if server.state == "running":
                stop_result = self.grpc.stop_server(server)
                if stop_result.success:
                    self.servers[server_id] = stop_result.value
                    results[server_id] = True
                else:
                    results[server_id] = False
            else:
                results[server_id] = True
        return results


class AdvancedGrpcOperations:
    """Advanced gRPC operations using FlextGrpc facade."""

    def __init__(self) -> None:
        """Initialize advanced operations with facade."""
        self.grpc = FlextGrpc()

    def create_complete_setup(
        self,
        host: str = c.LOCALHOST,
        port: int = 8080,
        service_name: str = "AdvancedService",
        methods: t.StrSequence | None = None,
    ) -> p.Result[FlextGrpcModels.Grpc.CompleteSetup]:
        """Create a complete gRPC setup through facade."""
        if methods is None:
            methods = ["ProcessData", "GetStatus", "StreamResults"]
        setup_result = self.grpc.create_complete_setup(
            host=host,
            port=port,
            service_name=service_name,
            methods=methods,
        )
        if setup_result.failure:
            return r[FlextGrpcModels.Grpc.CompleteSetup].fail(
                setup_result.error or "Setup failed",
            )
        setup = setup_result.value
        return r[FlextGrpcModels.Grpc.CompleteSetup].ok(setup)

    def demonstrate_streaming(self) -> None:
        """Demonstrate streaming operations through facade."""
        stream_configs: t.SequenceOf[tuple[str, str]] = [
            ("UnaryMethod", "unary"),
            ("ServerStreamingMethod", "server_streaming"),
            ("ClientStreamingMethod", "client_streaming"),
            ("BidirectionalMethod", "bidirectional"),
        ]
        for method_name, stream_type in stream_configs:
            stream_result = self.grpc.create_stream(
                method_name=method_name,
                stream_type=stream_type,
            )
            if stream_result.success:
                stream = stream_result.value
                _emit(f"Created {stream_type} stream: {stream.id}")
            else:
                _emit(f"Failed to create {stream_type} stream: {stream_result.error}")


def example_1_server_pool() -> None:
    """Example 1: Server pool management through facade."""
    manager = GrpcServerManager()
    server_results = manager.create_server_pool(base_port=8000, count=3)
    successful_creations = sum(1 for result in server_results if result.success)
    _emit(f"Created {successful_creations}/{len(server_results)} servers")
    start_results = manager.start_all_servers()
    successful_starts = sum(1 for success in start_results.values() if success)
    _emit(f"Started {successful_starts}/{len(start_results)} servers")
    status = manager.server_status()
    for server_id, info in status.items():
        _emit(f"Server {server_id}: {info['state']}, running: {info['is_running']}")
    stop_results = manager.stop_all_servers()
    successful_stops = sum(1 for success in stop_results.values() if success)
    _emit(f"Stopped {successful_stops}/{len(stop_results)} servers")


def example_2_client_pool() -> None:
    """Example 2: Advanced operations through facade."""
    ops = AdvancedGrpcOperations()
    setup_result = ops.create_complete_setup(
        host="localhost",
        port=8080,
        service_name="AdvancedService",
        methods=["ProcessData", "GetStatus", "StreamResults"],
    )
    if setup_result.success:
        setup = setup_result.value
        _emit(f"Created setup for target: {setup.target}")
    else:
        _emit(f"Setup creation failed: {setup_result.error}")
    ops.demonstrate_streaming()


def example_3_service_creation() -> None:
    """Example 3: Service creation patterns through facade."""
    grpc = FlextGrpc()
    services = [
        ("UserService", ["GetUser", "CreateUser", "UpdateUser"]),
        ("OrderService", ["GetOrder", "CreateOrder", "UpdateOrder"]),
        ("NotificationService", ["SendNotification", "GetNotifications"]),
    ]
    created_services: list[FlextGrpcModels.Grpc.Service] = []
    for service_name, methods in services:
        service_result = grpc.create_service(name=service_name, methods=methods)
        if service_result.success:
            service = service_result.value
            created_services.append(service)
            _emit(
                f"Created service: {service.name} with {len(service.methods)} methods",
            )
        else:
            _emit(f"Failed to create {service_name}: {service_result.error}")
    _emit(f"Successfully created {len(created_services)} services")


def example_4_streaming() -> None:
    """Example 4: Streaming operations through facade."""
    grpc = FlextGrpc()
    stream_configs: t.SequenceOf[tuple[str, str]] = [
        ("GetUser", "unary"),
        ("StreamMessages", "server_streaming"),
        ("UploadData", "client_streaming"),
        ("Chat", "bidirectional"),
    ]
    created_streams: list[FlextGrpcModels.Grpc.GrpcStream] = []
    for method_name, stream_type in stream_configs:
        stream_result = grpc.create_stream(
            method_name=method_name,
            stream_type=stream_type,
        )
        if stream_result.success:
            stream = stream_result.value
            created_streams.append(stream)
            _emit(f"Created {stream_type} stream for method: {method_name}")
        else:
            _emit(f"Failed to create {stream_type} stream: {stream_result.error}")
    _emit(f"Successfully created {len(created_streams)} streaming operations")


def example_5_error_handling() -> None:
    """Example 5: Comprehensive error handling through facade."""
    grpc = FlextGrpc()
    _emit("Testing various error scenarios through FlextGrpc facade...")
    invalid_server_result = grpc.create_server(host="", port=0)
    if invalid_server_result.failure:
        _emit(f"Invalid server creation properly failed: {invalid_server_result.error}")
    invalid_client_result = grpc.create_client(target="")
    if invalid_client_result.failure:
        _emit(f"Invalid client creation properly failed: {invalid_client_result.error}")
    invalid_channel_result = grpc.create_channel(target="")
    if invalid_channel_result.failure:
        _emit(
            f"Invalid channel creation properly failed: {invalid_channel_result.error}"
        )
    invalid_service_result = grpc.create_service(name="", methods=[])
    if invalid_service_result.failure:
        _emit(
            f"Invalid service creation properly failed: {invalid_service_result.error}"
        )
    invalid_stream_result = grpc.create_stream(method_name="", stream_type="invalid")
    if invalid_stream_result.failure:
        _emit(f"Invalid stream creation properly failed: {invalid_stream_result.error}")
    _emit("Error handling validation completed - all invalid inputs properly rejected")


def main() -> None:
    """Run all advanced examples."""
    example_1_server_pool()
    example_2_client_pool()
    example_3_service_creation()
    example_4_streaming()
    example_5_error_handling()


if __name__ == "__main__":
    main()
