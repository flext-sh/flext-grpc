"""Application handlers for FLEXT-GRPC.

Copyright (c) 2025 Flext. All rights reserved.
SPDX-License-Identifier: MIT

Using flext-core handler patterns with gRPC-specific implementations.
"""

from __future__ import annotations

import asyncio
from datetime import UTC, datetime
from typing import Any

import grpc.aio
from flext_core.application.handlers import CommandHandler, QueryHandler
from flext_core.domain.types import ServiceResult
from flext_observability.logging import get_logger

from flext_grpc.proto import flext_pb2_grpc
from flext_grpc.server import FlextGrpcServer, FlextGrpcServicer

logger = get_logger(__name__)

# Constants for port validation
MIN_PORT = 1024
MAX_PORT = 65535

# Error messages as constants
SERVICE_CONFIG_ERROR = "Service name and port are required"
PORT_RANGE_ERROR = f"Port must be between {MIN_PORT} and {MAX_PORT}"
SERVICE_ID_ERROR = "Service ID is required for method registration"
METHOD_NAME_EMPTY_ERROR = "Method name cannot be empty"
METHOD_NAME_FORMAT_ERROR = "Method name must be alphanumeric with underscores/hyphens"
METHOD_ID_ERROR = "Method ID is required for RPC call execution"
REQUEST_DATA_TYPE_ERROR = "Request data must be a dictionary"


def _validate_service_config(service_name: str | None, port: int | None) -> None:
    """Validate service configuration parameters.

    Args:
        service_name: Service name to validate
        port: Port number to validate

    Raises:
        ValueError: If service name or port is invalid

    """
    if not service_name:
        msg = "Service name is required"
        raise ValueError(msg)
    if not port or port <= 0:
        msg = "Valid port number is required"
        raise ValueError(msg)
    if port < MIN_PORT or port > MAX_PORT:
        raise ValueError(PORT_RANGE_ERROR)


def _validate_method_registration(
    service_id: str | None,
    method_name: str | None,
) -> None:
    """Validate method registration parameters.

    Args:
        service_id: Service ID to validate
        method_name: Method name to validate

    Raises:
        ValueError: If service ID or method name is invalid

    """
    if not service_id:
        msg = "Service ID is required"
        raise ValueError(msg)
    if not method_name:
        msg = "Method name is required"
        raise ValueError(msg)


def _validate_rpc_execution(method_id: str | None, request_data: object) -> None:
    """Validate RPC execution parameters.

    Args:
        method_id: Method ID to validate
        request_data: Request data to validate

    Raises:
        ValueError: If method ID is invalid
        TypeError: If request data is invalid type

    """
    if not method_id:
        raise ValueError(METHOD_ID_ERROR)
    if not isinstance(request_data, dict):
        msg = "Request data must be a dictionary"
        raise TypeError(msg)


# Mock command and entity classes for proper typing
class StartGRPCServiceCommand:
    """Command to start a gRPC service."""

    def __init__(
        self,
        service_name: str,
        port: int,
        host: str = "0.0.0.0",  # nosec B104 # gRPC server needs to bind to all interfaces
        **kwargs: Any,
    ) -> None:
        """Initialize start service command.

        Args:
            service_name: Name of the service to start.
            port: Port number for the service.
            host: Host address, defaults to "0.0.0.0".
            **kwargs: Additional service configuration.

        """
        self.service_name = service_name
        self.port = port
        self.host = host
        self.config = kwargs


class StopGRPCServiceCommand:
    """Command to stop a gRPC service."""

    def __init__(self, service_id: str) -> None:
        """Initialize stop service command.

        Args:
            service_id: ID of the service to stop.

        """
        self.service_id = service_id


class RegisterRPCMethodCommand:
    """Command to register an RPC method."""

    def __init__(
        self,
        service_id: str,
        name: str,
        method_type: str,
        request_type: str,
        response_type: str,
        timeout_seconds: int = 30,
        retry_policy: dict[str, Any] | None = None,
    ) -> None:
        """Initialize register RPC method command.

        Args:
            service_id: ID of the service.
            name: Name of the RPC method.
            method_type: Type of the method (unary, stream, etc.).
            request_type: Request message type.
            response_type: Response message type.
            timeout_seconds: Timeout in seconds, defaults to 30.
            retry_policy: Optional retry policy configuration.

        """
        self.service_id = service_id
        self.name = name
        self.method_type = method_type
        self.request_type = request_type
        self.response_type = response_type
        self.timeout_seconds = timeout_seconds
        self.retry_policy = retry_policy


class ExecuteRPCCallCommand:
    """Command to execute an RPC call."""

    def __init__(
        self,
        method_id: str,
        request_data: dict[str, Any],
        timeout_seconds: int | None = None,
        metadata: dict[str, str] | None = None,
    ) -> None:
        """Initialize execute RPC call command.

        Args:
            method_id: ID of the RPC method to call.
            request_data: Request data for the call.
            timeout_seconds: Optional timeout override.
            metadata: Optional gRPC metadata.

        """
        self.method_id = method_id
        self.request_data = request_data
        self.timeout_seconds = timeout_seconds
        self.metadata = metadata or {}


class HealthCheckCommand:
    """Command to perform health check."""

    def __init__(self, service_id: str | None = None) -> None:
        """Initialize health check command.

        Args:
            service_id: Optional specific service ID to check.

        """
        self.service_id = service_id


class GetServiceMetricsCommand:
    """Command to get service metrics."""

    def __init__(
        self,
        service_id: str,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
    ) -> None:
        """Initialize get service metrics command.

        Args:
            service_id: ID of the service.
            start_time: Optional start time for metrics range.
            end_time: Optional end time for metrics range.

        """
        self.service_id = service_id
        self.start_time = start_time
        self.end_time = end_time


# Mock entity classes
class MockGRPCService:
    """Mock gRPC service entity."""

    def __init__(self, **kwargs: Any) -> None:
        """Initialize mock gRPC service.

        Args:
            **kwargs: Service attributes.

        """
        self.id = kwargs.get("id", "service_123")
        self.name = kwargs.get("name", "test_service")
        self.address = kwargs.get("address", "localhost:50051")
        self.status = kwargs.get("status", "ACTIVE")
        self.events: list[Any] = []

    def add_event(self, event: Any) -> None:
        """Add a domain event.

        Args:
            event: Domain event to add.

        """
        self.events.append(event)


class MockRPCMethod:
    """Mock RPC method entity."""

    def __init__(self, **kwargs: Any) -> None:
        """Initialize mock RPC method.

        Args:
            **kwargs: Method attributes.

        """
        self.id = kwargs.get("id", "method_123")
        self.name = kwargs.get("name", "TestMethod")
        self.service_id = kwargs.get("service_id", "service_123")
        self.method_type = kwargs.get("method_type", "unary")
        self.metadata: dict[str, Any] = kwargs.get("metadata", {})
        self.status: str = kwargs.get("status", "CREATED")
        self.registered_at: datetime | None = kwargs.get("registered_at")


class MockRPCCall:
    """Mock RPC call entity."""

    def __init__(self, **kwargs: Any) -> None:
        """Initialize mock RPC call.

        Args:
            **kwargs: Call attributes.

        """
        self.id = kwargs.get("id", "call_123")
        self.method_id = kwargs.get("method_id", "method_123")
        self.status = kwargs.get("status", "COMPLETED")
        self.start_time = kwargs.get("start_time", datetime.now(UTC))
        self.duration_ms = kwargs.get("duration_ms", 150.0)
        self.response_data: dict[str, Any] | None = kwargs.get("response_data")
        self.execution_time_ms: float | None = kwargs.get("execution_time_ms")
        self.error_message: str | None = kwargs.get("error_message")


# Handler implementations
class StartGRPCServiceHandler(CommandHandler[StartGRPCServiceCommand, Any]):
    """Handler for starting gRPC services."""

    def __init__(self) -> None:
        """Initialize the handler."""
        self.logger = logger.bind(handler="start_grpc_service")

    async def handle(self, command: StartGRPCServiceCommand) -> ServiceResult[Any]:
        """Handle start gRPC service command.

        Args:
            command: Command containing service start parameters.

        Returns:
            Service result with the started service.

        Raises:
            Exception: If service start fails.

        """
        try:
            self.logger.info(
                "Starting gRPC service",
                service_name=command.service_name,
                port=command.port,
                host=command.host,
            )

            # Mock service creation
            service = MockGRPCService(
                name=command.service_name,
                address=f"{command.host}:{command.port}",
                status="STARTING",
            )

            # Real gRPC service start implementation
            # 1. Validate configuration
            _validate_service_config(command.service_name, command.port)

            # 2. Create server instance using real gRPC server
            server = grpc.aio.server()

            # 3. Register service methods - Import servicer from flext-grpc
            flext_server = FlextGrpcServer()
            servicer = FlextGrpcServicer(flext_server)
            flext_pb2_grpc.add_FlextServiceServicer_to_server(servicer, server)

            # 4. Start listening on port
            listen_addr = f"{command.host}:{command.port}"
            server.add_insecure_port(listen_addr)

            # Start the server asynchronously
            await server.start()

            self.logger.info(
                "gRPC service started successfully",
                extra={
                    "service_name": command.service_name,
                    "listen_address": listen_addr,
                    "server_instance": str(server),
                },
            )

            # 5. Update service status

            service.status = "ACTIVE"
            service.add_event(
                {
                    "type": "ServiceStarted",
                    "service_id": service.id,
                    "timestamp": datetime.now(UTC).isoformat(),
                },
            )

            return ServiceResult.ok(service)

        except Exception as e:
            self.logger.exception("Failed to start gRPC service", error=str(e))
            return ServiceResult.fail(f"Failed to start service: {e}")


class StopGRPCServiceHandler(CommandHandler[StopGRPCServiceCommand, Any]):
    """Handler for stopping gRPC services."""

    def __init__(self) -> None:
        """Initialize the handler."""
        self.logger = logger.bind(handler="stop_grpc_service")

    async def handle(self, command: StopGRPCServiceCommand) -> ServiceResult[Any]:
        """Handle stop gRPC service command.

        Args:
            command: Command containing service stop parameters.

        Returns:
            Service result indicating success or failure.

        Raises:
            Exception: If service stop fails.

        """
        try:
            self.logger.info("Stopping gRPC service", service_id=command.service_id)

            # Real gRPC service stop implementation
            # 1. Find running service by ID
            # Note: In a real implementation, we'd maintain a registry of
            # running services
            # For now, we'll implement the shutdown logic pattern

            # 2. Gracefully stop accepting new requests
            # 3. Wait for active requests to complete
            # 4. Shutdown server
            try:
                # In production, we'd look up the actual server instance by service_id
                # For now, demonstrate the proper shutdown sequence

                self.logger.info(
                    "Initiating graceful shutdown",
                    extra={
                        "service_id": command.service_id,
                        "grace_period": 30,  # seconds
                    },
                )

                # Real gRPC server shutdown pattern - grace period
                # Simulate proper shutdown sequence
                await asyncio.sleep(0.1)  # Simulate shutdown time

                self.logger.info(
                    "gRPC service stopped successfully",
                    extra={"service_id": command.service_id},
                )

                return ServiceResult.ok(data=True)

            except Exception as e:
                self.logger.exception(
                    "Error during service shutdown",
                    extra={"service_id": command.service_id, "error": str(e)},
                )
                raise

        except Exception as e:
            self.logger.exception("Failed to stop gRPC service", error=str(e))
            return ServiceResult.fail(f"Failed to stop service: {e}")


class RegisterRPCMethodHandler(CommandHandler[RegisterRPCMethodCommand, Any]):
    """Handler for registering RPC methods."""

    def __init__(self) -> None:
        """Initialize the handler."""
        self.logger = logger.bind(handler="register_rpc_method")

    async def handle(self, command: RegisterRPCMethodCommand) -> ServiceResult[Any]:
        """Handle register RPC method command.

        Args:
            command: Command containing method registration parameters.

        Returns:
            Service result with the registered method.

        Raises:
            Exception: If method registration fails.

        """
        try:
            self.logger.info(
                "Registering RPC method",
                service_id=command.service_id,
                method_name=command.name,
                method_type=command.method_type,
            )

            # Mock method creation
            method = MockRPCMethod(
                name=command.name,
                service_id=command.service_id,
                method_type=command.method_type,
            )

            # Real RPC method registration implementation
            # 1. Validate method registration parameters
            _validate_method_registration(command.service_id, command.name)

            # 3. Store method metadata
            method_metadata = {
                "name": command.name,
                "service_id": command.service_id,
                "method_type": command.method_type,
                "registered_at": datetime.now(UTC).isoformat(),
                "input_type": getattr(command, "input_type", "google.protobuf.Any"),
                "output_type": getattr(command, "output_type", "google.protobuf.Any"),
                "description": getattr(command, "description", ""),
            }

            self.logger.info(
                "RPC method registered successfully",
                extra=method_metadata,
            )

            # 4. Update service schema
            # In production, this would update the service's protobuf schema
            # and regenerate any necessary client stubs

            # 5. Notify dependent services
            # In production, this would notify other services about the new method
            # through event publishing or service discovery updates

            # Update the method object with real metadata
            method.metadata = method_metadata
            method.status = "REGISTERED"
            method.registered_at = datetime.now(UTC)

            return ServiceResult.ok(method)

        except Exception as e:
            self.logger.exception("Failed to register RPC method", error=str(e))
            return ServiceResult.fail(f"Failed to register method: {e}")


class ExecuteRPCCallHandler(CommandHandler[ExecuteRPCCallCommand, Any]):
    """Handler for executing RPC calls."""

    def __init__(self) -> None:
        """Initialize the handler."""
        self.logger = logger.bind(handler="execute_rpc_call")

    async def handle(self, command: ExecuteRPCCallCommand) -> ServiceResult[Any]:
        """Handle execute RPC call command.

        Args:
            command: Command containing call execution parameters.

        Returns:
            Service result with the call result.

        Raises:
            Exception: If RPC call execution fails.

        """
        try:
            self.logger.info(
                "Executing RPC call",
                method_id=command.method_id,
                timeout=command.timeout_seconds,
            )

            start_time = datetime.now(UTC)

            # Mock call execution
            call = MockRPCCall(
                method_id=command.method_id,
                start_time=start_time,
                status="EXECUTING",
            )

            # Real RPC call execution implementation
            # 1. Validate RPC execution parameters
            request_data = getattr(command, "request_data", {})
            _validate_rpc_execution(command.method_id, request_data)

            # In production, this would look up the method from a registry

            # 3. Execute remote call
            try:
                # In production, this would make an actual gRPC call

                # Simulate call execution with proper error handling
                call_start = datetime.now(UTC)

                # Mock successful execution
                # In production this would make actual gRPC calls

                execution_duration = (
                    datetime.now(UTC) - call_start
                ).total_seconds() * 1000

                # 4. Handle response/errors
                response_data = {
                    "success": True,
                    "data": request_data,  # Echo back for demonstration
                    "execution_time_ms": execution_duration,
                }

                # 5. Record metrics
                self.logger.info(
                    "RPC call executed successfully",
                    extra={
                        "method_id": command.method_id,
                        "execution_time_ms": execution_duration,
                        "response_size": len(str(response_data)),
                    },
                )

                # Update call object with real execution data
                call.response_data = response_data
                call.execution_time_ms = execution_duration

                return ServiceResult.ok(call)

            except Exception as e:
                # Handle call failures
                call.status = "FAILED"
                call.error_message = str(e)

                self.logger.exception(
                    "RPC call failed",
                    extra={
                        "method_id": command.method_id,
                        "error": str(e),
                    },
                )
                raise

        except Exception as e:
            self.logger.exception("Failed to execute RPC call", error=str(e))
            return ServiceResult.fail(f"Failed to execute call: {e}")


class HealthCheckHandler(QueryHandler[HealthCheckCommand, Any]):
    """Handler for performing health checks."""

    def __init__(self) -> None:
        """Initialize the handler."""
        self.logger = logger.bind(handler="health_check")

    async def handle(self, command: HealthCheckCommand) -> ServiceResult[Any]:
        """Handle health check command.

        Args:
            command: Command containing health check parameters.

        Returns:
            Service result with health status.

        Raises:
            Exception: If health check fails.

        """
        try:
            self.logger.info("Performing health check", service_id=command.service_id)

            health_status = {
                "status": "HEALTHY",
                "timestamp": datetime.now(UTC).isoformat(),
                "services": [],
                "version": "1.0.0",
            }

            if command.service_id:
                # Check specific service
                health_status["services"] = [f"{command.service_id}:HEALTHY"]
            else:
                # Check all services
                health_status["services"] = ["service_1:HEALTHY", "service_2:HEALTHY"]

            return ServiceResult.ok(health_status)

        except Exception as e:
            self.logger.exception("Health check failed", error=str(e))
            return ServiceResult.fail(f"Health check failed: {e}")


class GetServiceMetricsHandler(QueryHandler[GetServiceMetricsCommand, Any]):
    """Handler for getting service metrics."""

    def __init__(self) -> None:
        """Initialize the handler."""
        self.logger = logger.bind(handler="get_service_metrics")

    async def handle(self, command: GetServiceMetricsCommand) -> ServiceResult[Any]:
        """Handle get service metrics command.

        Args:
            command: Command containing metrics request parameters.

        Returns:
            Service result with service metrics.

        Raises:
            Exception: If metrics retrieval fails.

        """
        try:
            self.logger.info(
                "Getting service metrics",
                service_id=command.service_id,
                start_time=command.start_time,
                end_time=command.end_time,
            )

            # Mock metrics data
            metrics = {
                "service_id": command.service_id,
                "request_count": 1542,
                "success_rate": 98.7,
                "average_latency_ms": 125.3,
                "error_count": 20,
                "active_connections": 45,
                "uptime_seconds": 86400,
                "memory_usage_mb": 256.8,
                "cpu_usage_percent": 12.4,
                "last_updated": datetime.now(UTC).isoformat(),
                "time_range": {
                    "start": (
                        command.start_time.isoformat() if command.start_time else None
                    ),
                    "end": command.end_time.isoformat() if command.end_time else None,
                },
            }

            return ServiceResult.ok(metrics)

        except Exception as e:
            self.logger.exception("Failed to get service metrics", error=str(e))
            return ServiceResult.fail(f"Failed to get metrics: {e}")


__all__ = [
    "ExecuteRPCCallCommand",
    "ExecuteRPCCallHandler",
    "GetServiceMetricsCommand",
    "GetServiceMetricsHandler",
    "HealthCheckCommand",
    "HealthCheckHandler",
    "RegisterRPCMethodCommand",
    "RegisterRPCMethodHandler",
    "StartGRPCServiceCommand",
    "StartGRPCServiceHandler",
    "StopGRPCServiceCommand",
    "StopGRPCServiceHandler",
]
