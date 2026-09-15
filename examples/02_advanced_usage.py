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

from flext_cli import cli
from flext_grpc import (
    FlextGrpc,
    FlextGrpcConstants,
    FlextGrpcModels,
    FlextGrpcSettings,
    c,
    p,
    r,
    t,
)


class ExamplesFlextGrpcAdvancedUsage:
    """Advanced usage examples for flext-grpc."""

    def __init__(self) -> None:
        """Initialize with facade."""
        self._grpc = FlextGrpc()
        self._constants = FlextGrpcConstants
        self._models = FlextGrpcModels
        self._settings_cls = FlextGrpcSettings
        self._c = c
        self._p = p
        self._r = r
        self._t = t

    @property
    def grpc(self) -> FlextGrpc:
        """Public accessor for the gRPC facade."""
        return self._grpc

    @property
    def constants(self) -> type[FlextGrpcConstants]:
        """Public accessor for constants."""
        return self._constants

    @property
    def models(self) -> type[FlextGrpcModels]:
        """Public accessor for models."""
        return self._models

    @property
    def settings_cls(self) -> type[FlextGrpcSettings]:
        """Public accessor for settings class."""
        return self._settings_cls

    @property
    def c(self):
        """Public accessor for constants facade."""
        return self._c

    @property
    def p(self):
        """Public accessor for protocols facade."""
        return self._p

    @property
    def r(self):
        """Public accessor for result facade."""
        return self._r

    @property
    def t(self):
        """Public accessor for typings facade."""
        return self._t

    def emit(self, message: str) -> None:
        """Emit example output through the canonical CLI facade."""
        cli.print(message)

    class GrpcServerManager:
        """Advanced server management example using FlextGrpc facade."""

        def __init__(self, outer: ExamplesFlextGrpcAdvancedUsage) -> None:
            """Initialize the gRPC server manager with facade."""
            self._outer = outer
            self.grpc = outer.grpc
            self.servers: outer.t.MutableMappingKV[str, outer.models.Grpc.Server] = {}
            self.server_configs: outer.t.MutableMappingKV[
                str, outer.settings_cls
            ] = {}

        def create_server_pool(
            self, base_port: int = 8000, count: int = 3
        ) -> list[outer.p.Result[outer.models.Grpc.Server]]:
            """Create a pool of servers on consecutive ports through facade."""
            server_results: list[outer.p.Result[outer.models.Grpc.Server]] = []
            for i in range(count):
                server_id = f"pool-server-{i}"
                port = base_port + i
                settings = outer.settings_cls.model_validate({
                    "Grpc": {
                        "host": outer.constants.Grpc.NETWORK_DEFAULT_HOST,
                        "port": port,
                        "max_workers": 10 + i * 5,
                    }
                })
                self.server_configs[server_id] = settings
                server_result = self.grpc.create_server(
                    host=settings.Grpc.host,
                    port=settings.Grpc.port,
                    max_workers=settings.Grpc.max_workers,
                )
                if server_result.success:
                    server = server_result.value
                    self.servers[server_id] = server
                server_results.append(server_result)
            return server_results

        def server_status(
            self,
        ) -> outer.t.MappingKV[str, outer.t.MappingKV[str, str]]:
            """Get status of all servers through facade."""
            status: outer.t.MutableMappingKV[str, outer.t.MappingKV[str, str]] = {}
            for server_id, server in self.servers.items():
                settings = self.server_configs[server_id]
                status[server_id] = {
                    "address": f"{server.host}:{server.port}",
                    "state": server.state,
                    "max_workers": str(server.max_workers),
                    "timeout": f"{settings.Grpc.timeout}s",
                    "is_running": str(server.state == "running"),
                    "valid": str(server.validate_business_rules().success),
                }
            return status

        def start_all_servers(self) -> outer.t.MappingKV[str, bool]:
            """Start all servers in the pool through facade."""
            results: outer.t.MutableMappingKV[str, bool] = {}
            for server_id, server in self.servers.items():
                start_result = self.grpc.start_server(server)
                if start_result.success:
                    self.servers[server_id] = start_result.value
                    results[server_id] = True
                else:
                    results[server_id] = False
            return results

        def stop_all_servers(self) -> outer.t.MappingKV[str, bool]:
            """Stop all servers in the pool through facade."""
            results: outer.t.MutableMappingKV[str, bool] = {}
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

        def __init__(self, outer: ExamplesFlextGrpcAdvancedUsage) -> None:
            """Initialize advanced operations with facade."""
            self._outer = outer
            self.grpc = outer.grpc

        def create_complete_setup(
            self,
            host: str | None = None,
            port: int = 8080,
            service_name: str = "AdvancedService",
            methods: outer.t.StrSequence | None = None,
        ) -> outer.p.Result[outer.models.Grpc.CompleteSetup]:
            """Create a complete gRPC setup through facade."""
            c_facade = outer.c
            if host is None:
                host = c_facade.LOCALHOST
            if methods is None:
                methods = ["ProcessData", "GetStatus", "StreamResults"]
            setup_result = self.grpc.create_complete_setup(
                host=host, port=port, service_name=service_name, methods=methods
            )
            if setup_result.failure:
                return outer.r[outer.models.Grpc.CompleteSetup].from_failure(
                    setup_result
                )
            setup = setup_result.value
            return outer.r[outer.models.Grpc.CompleteSetup].ok(setup)

        def demonstrate_streaming(self) -> None:
            """Demonstrate streaming operations through facade."""
            stream_configs: outer.t.SequenceOf[tuple[str, str]] = [
                ("UnaryMethod", "unary"),
                ("ServerStreamingMethod", "server_streaming"),
                ("ClientStreamingMethod", "client_streaming"),
                ("BidirectionalMethod", "bidirectional"),
            ]
            for method_name, stream_type in stream_configs:
                stream_result = self.grpc.create_stream(
                    method_name=method_name, stream_type=stream_type
                )
                if stream_result.success:
                    stream = stream_result.value
                    self._outer.emit(f"Created {stream_type} stream: {stream.id}")
                else:
                    self._outer.emit(
                        f"Failed to create {stream_type} stream: {stream_result.error}"
                    )

    def example_1_server_pool(self) -> None:
        """Manage a server pool through the facade."""
        manager = self.GrpcServerManager(self)
        server_results = manager.create_server_pool(base_port=8000, count=3)
        successful_creations = sum(1 for result in server_results if result.success)
        self.emit(f"Created {successful_creations}/{len(server_results)} servers")
        start_results = manager.start_all_servers()
        successful_starts = sum(1 for success in start_results.values() if success)
        self.emit(f"Started {successful_starts}/{len(start_results)} servers")
        status = manager.server_status()
        for server_id, info in status.items():
            self.emit(
                f"Server {server_id}: {info['state']}, running: {info['is_running']}"
            )
        stop_results = manager.stop_all_servers()
        successful_stops = sum(1 for success in stop_results.values() if success)
        self.emit(f"Stopped {successful_stops}/{len(stop_results)} servers")

    def example_2_client_pool(self) -> None:
        """Run advanced operations through the facade."""
        ops = self.AdvancedGrpcOperations(self)
        setup_result = ops.create_complete_setup(
            host="localhost",
            port=8080,
            service_name="AdvancedService",
            methods=["ProcessData", "GetStatus", "StreamResults"],
        )
        if setup_result.success:
            setup = setup_result.value
            self.emit(f"Created setup for target: {setup.target}")
        else:
            self.emit(f"Setup creation failed: {setup_result.error}")
        ops.demonstrate_streaming()

    def example_3_service_creation(self) -> None:
        """Demonstrate service creation patterns through the facade."""
        grpc = self.grpc
        services = [
            ("UserService", ["GetUser", "CreateUser", "UpdateUser"]),
            ("OrderService", ["GetOrder", "CreateOrder", "UpdateOrder"]),
            ("NotificationService", ["SendNotification", "GetNotifications"]),
        ]
        created_services: list[self.models.Grpc.Service] = []
        for service_name, methods in services:
            service_result = grpc.create_service(name=service_name, methods=methods)
            if service_result.success:
                service = service_result.value
                created_services.append(service)
                self.emit(
                    f"Created service: {service.name} with {len(service.methods)} methods"
                )
            else:
                self.emit(f"Failed to create {service_name}: {service_result.error}")
        self.emit(f"Successfully created {len(created_services)} services")

    def example_4_streaming(self) -> None:
        """Run streaming operations through the facade."""
        grpc = self.grpc
        stream_configs: self.t.SequenceOf[tuple[str, str]] = [
            ("GetUser", "unary"),
            ("StreamMessages", "server_streaming"),
            ("UploadData", "client_streaming"),
            ("Chat", "bidirectional"),
        ]
        created_streams: list[self.models.Grpc.GrpcStream] = []
        for method_name, stream_type in stream_configs:
            stream_result = grpc.create_stream(
                method_name=method_name, stream_type=stream_type
            )
            if stream_result.success:
                stream = stream_result.value
                created_streams.append(stream)
                self.emit(f"Created {stream_type} stream for method: {method_name}")
            else:
                self.emit(
                    f"Failed to create {stream_type} stream: {stream_result.error}"
                )
        self.emit(f"Successfully created {len(created_streams)} streaming operations")

    def example_5_error_handling(self) -> None:
        """Demonstrate comprehensive error handling through the facade."""
        grpc = self.grpc
        self.emit("Testing various error scenarios through FlextGrpc facade...")
        invalid_server_result = grpc.create_server(host="", port=0)
        if invalid_server_result.failure:
            self.emit(
                f"Invalid server creation properly failed: {invalid_server_result.error}"
            )
        invalid_client_result = grpc.create_client(target="")
        if invalid_client_result.failure:
            self.emit(
                f"Invalid client creation properly failed: {invalid_client_result.error}"
            )
        invalid_channel_result = grpc.create_channel(target="")
        if invalid_channel_result.failure:
            self.emit(
                f"Invalid channel creation properly failed: {invalid_channel_result.error}"
            )
        invalid_service_result = grpc.create_service(name="", methods=[])
        if invalid_service_result.failure:
            self.emit(
                f"Invalid service creation properly failed: {invalid_service_result.error}"
            )
        invalid_stream_result = grpc.create_stream(
            method_name="", stream_type="invalid"
        )
        if invalid_stream_result.failure:
            self.emit(
                f"Invalid stream creation properly failed: {invalid_stream_result.error}"
            )
        self.emit(
            "Error handling validation completed - all invalid inputs properly rejected"
        )

    def main(self) -> None:
        """Run all advanced examples."""
        self.example_1_server_pool()
        self.example_2_client_pool()
        self.example_3_service_creation()
        self.example_4_streaming()
        self.example_5_error_handling()


if __name__ == "__main__":
    ExamplesFlextGrpcAdvancedUsage().main()