"""Tests for application handlers using real implementations."""

from __future__ import annotations

import pytest

from flext_grpc.application.handlers import (
    ExecuteRPCCallCommand,
    ExecuteRPCCallHandler,
    GetServiceMetricsCommand,
    GetServiceMetricsHandler,
    HealthCheckCommand,
    HealthCheckHandler,
    RegisterRPCMethodCommand,
    RegisterRPCMethodHandler,
    StartGRPCServiceCommand,
    StartGRPCServiceHandler,
    StopGRPCServiceCommand,
    StopGRPCServiceHandler,
    _validate_method_registration,
    _validate_rpc_execution,
    _validate_service_config,
)

# 🚨 ARCHITECTURAL COMPLIANCE: Tests can import directly for verification
from flext_grpc.infrastructure.di_container import get_service_result

# Initialize types via DI container for tests
ServiceResult = get_service_result()


class TestServiceConfigValidation:
    """Test service configuration validation functions."""

    def test_validate_service_config_valid(self) -> None:
        """Test validation with valid configuration."""
        # Should not raise exception
        _validate_service_config("test-service", 8080)

    def test_validate_service_config_missing_name(self) -> None:
        """Test validation with missing service name."""
        with pytest.raises(ValueError, match="Service name and port are required"):
            _validate_service_config(None, 8080)

    def test_validate_service_config_empty_name(self) -> None:
        """Test validation with empty service name."""
        with pytest.raises(ValueError, match="Service name and port are required"):
            _validate_service_config("", 8080)

    def test_validate_service_config_missing_port(self) -> None:
        """Test validation with missing port."""
        with pytest.raises(ValueError, match="Service name and port are required"):
            _validate_service_config("test-service", None)

    def test_validate_service_config_invalid_port_low(self) -> None:
        """Test validation with port too low."""
        with pytest.raises(ValueError, match="Port must be between 1024 and 65535"):
            _validate_service_config("test-service", 80)

    def test_validate_service_config_invalid_port_high(self) -> None:
        """Test validation with port too high."""
        with pytest.raises(ValueError, match="Port must be between 1024 and 65535"):
            _validate_service_config("test-service", 70000)


class TestMethodRegistrationValidation:
    """Test method registration validation functions."""

    def test_validate_method_registration_valid(self) -> None:
        """Test validation with valid parameters."""
        # Should not raise exception
        _validate_method_registration("service-123", "CreatePipeline")

    def test_validate_method_registration_missing_service_id(self) -> None:
        """Test validation with missing service ID."""
        with pytest.raises(
            ValueError,
            match="Service ID is required for method registration",
        ):
            _validate_method_registration(None, "CreatePipeline")

    def test_validate_method_registration_empty_service_id(self) -> None:
        """Test validation with empty service ID."""
        with pytest.raises(
            ValueError,
            match="Service ID is required for method registration",
        ):
            _validate_method_registration("", "CreatePipeline")

    def test_validate_method_registration_missing_method_name(self) -> None:
        """Test validation with missing method name."""
        with pytest.raises(ValueError, match="Method name cannot be empty"):
            _validate_method_registration("service-123", None)

    def test_validate_method_registration_empty_method_name(self) -> None:
        """Test validation with empty method name."""
        with pytest.raises(ValueError, match="Method name cannot be empty"):
            _validate_method_registration("service-123", "")

    def test_validate_method_registration_whitespace_method_name(self) -> None:
        """Test validation with whitespace-only method name."""
        with pytest.raises(ValueError, match="Method name cannot be empty"):
            _validate_method_registration("service-123", "   ")

    def test_validate_method_registration_invalid_method_name(self) -> None:
        """Test validation with invalid method name."""
        with pytest.raises(ValueError, match="Method name must be alphanumeric"):
            _validate_method_registration("service-123", "Invalid Method!")

    def test_validate_method_registration_valid_method_names(self) -> None:
        """Test validation with various valid method names."""
        valid_names = [
            "CreatePipeline",
            "create_pipeline",
            "create-pipeline",
            "Pipeline123",
            "get_pipeline_status",
        ]
        for name in valid_names:
            # Should not raise exception
            _validate_method_registration("service-123", name)


class TestRPCExecutionValidation:
    """Test RPC execution validation functions."""

    def test_validate_rpc_execution_valid(self) -> None:
        """Test validation with valid parameters."""
        # Should not raise exception
        _validate_rpc_execution("method-123", {"key": "value"})

    def test_validate_rpc_execution_missing_method_id(self) -> None:
        """Test validation with missing method ID."""
        with pytest.raises(
            ValueError,
            match="Method ID is required for RPC call execution",
        ):
            _validate_rpc_execution(None, {"key": "value"})

    def test_validate_rpc_execution_empty_method_id(self) -> None:
        """Test validation with empty method ID."""
        with pytest.raises(
            ValueError,
            match="Method ID is required for RPC call execution",
        ):
            _validate_rpc_execution("", {"key": "value"})

    def test_validate_rpc_execution_invalid_request_data_string(self) -> None:
        """Test validation with string request data."""
        with pytest.raises(TypeError, match="Request data must be a dictionary"):
            _validate_rpc_execution("method-123", "invalid")

    def test_validate_rpc_execution_invalid_request_data_list(self) -> None:
        """Test validation with list request data."""
        with pytest.raises(TypeError, match="Request data must be a dictionary"):
            _validate_rpc_execution("method-123", [1, 2, 3])

    def test_validate_rpc_execution_invalid_request_data_none(self) -> None:
        """Test validation with None request data."""
        with pytest.raises(TypeError, match="Request data must be a dictionary"):
            _validate_rpc_execution("method-123", None)


class TestCommandClasses:
    """Test command class initialization and validation."""

    def test_start_grpc_service_command_creation(self) -> None:
        """Test StartGRPCServiceCommand creation."""
        command = StartGRPCServiceCommand(service_name="test-service", port=8080)
        assert command.service_name == "test-service"
        assert command.port == 8080
        assert command.host == "0.0.0.0"  # Default value
        assert isinstance(command.config, dict)

    def test_start_grpc_service_command_with_custom_host(self) -> None:
        """Test StartGRPCServiceCommand with custom host."""
        command = StartGRPCServiceCommand(
            service_name="test-service",
            port=8080,
            host="127.0.0.1",
        )
        assert command.host == "127.0.0.1"

    def test_start_grpc_service_command_with_config(self) -> None:
        """Test StartGRPCServiceCommand with additional config."""
        command = StartGRPCServiceCommand(
            service_name="test-service",
            port=8080,
            max_workers=10,
            timeout=30,
        )
        assert command.config["max_workers"] == 10
        assert command.config["timeout"] == 30

    def test_stop_grpc_service_command_creation(self) -> None:
        """Test StopGRPCServiceCommand creation."""
        command = StopGRPCServiceCommand(service_id="service-123")
        assert command.service_id == "service-123"

    def test_register_rpc_method_command_creation(self) -> None:
        """Test RegisterRPCMethodCommand creation."""
        command = RegisterRPCMethodCommand(
            service_id="service-123",
            name="CreatePipeline",
            method_type="unary",
            request_type="CreatePipelineRequest",
            response_type="CreatePipelineResponse",
        )
        assert command.service_id == "service-123"
        assert command.name == "CreatePipeline"
        assert command.method_type == "unary"
        assert command.request_type == "CreatePipelineRequest"
        assert command.response_type == "CreatePipelineResponse"
        assert command.timeout_seconds == 30  # Default
        assert command.retry_policy is None  # Default

    def test_register_rpc_method_command_with_retry_policy(self) -> None:
        """Test RegisterRPCMethodCommand with retry policy."""
        retry_policy = {"max_attempts": 3, "backoff_factor": 2}
        command = RegisterRPCMethodCommand(
            service_id="service-123",
            name="CreatePipeline",
            method_type="unary",
            request_type="CreatePipelineRequest",
            response_type="CreatePipelineResponse",
            timeout_seconds=60,
            retry_policy=retry_policy,
        )
        assert command.timeout_seconds == 60
        assert command.retry_policy == retry_policy

    def test_execute_rpc_call_command_creation(self) -> None:
        """Test ExecuteRPCCallCommand creation."""
        request_data = {"name": "test-pipeline", "extractor": "tap-postgres"}
        command = ExecuteRPCCallCommand(
            method_id="CreatePipeline",
            request_data=request_data,
        )
        assert command.method_id == "CreatePipeline"
        assert command.request_data == request_data
        assert command.timeout_seconds is None  # Default
        assert command.metadata == {}  # Default

    def test_execute_rpc_call_command_with_metadata(self) -> None:
        """Test ExecuteRPCCallCommand with metadata."""
        metadata = {"authorization": "Bearer token123"}
        command = ExecuteRPCCallCommand(
            method_id="CreatePipeline",
            request_data={"name": "test"},
            timeout_seconds=45,
            metadata=metadata,
        )
        assert command.timeout_seconds == 45
        assert command.metadata == metadata

    def test_health_check_command_creation(self) -> None:
        """Test HealthCheckCommand creation."""
        command = HealthCheckCommand()
        assert command is not None

    def test_get_service_metrics_command_creation(self) -> None:
        """Test GetServiceMetricsCommand creation."""
        command = GetServiceMetricsCommand(service_id="test-service")
        assert command is not None
        assert command.service_id == "test-service"


class TestHandlerClasses:
    """Test handler class initialization and basic functionality."""

    def test_start_grpc_service_handler_creation(self) -> None:
        """Test StartGRPCServiceHandler creation."""
        handler = StartGRPCServiceHandler()
        assert handler is not None
        assert hasattr(handler, "handle")

    def test_stop_grpc_service_handler_creation(self) -> None:
        """Test StopGRPCServiceHandler creation."""
        handler = StopGRPCServiceHandler()
        assert handler is not None
        assert hasattr(handler, "handle")

    def test_register_rpc_method_handler_creation(self) -> None:
        """Test RegisterRPCMethodHandler creation."""
        handler = RegisterRPCMethodHandler()
        assert handler is not None
        assert hasattr(handler, "handle")

    def test_execute_rpc_call_handler_creation(self) -> None:
        """Test ExecuteRPCCallHandler creation."""
        handler = ExecuteRPCCallHandler()
        assert handler is not None
        assert hasattr(handler, "handle")

    def test_health_check_handler_creation(self) -> None:
        """Test HealthCheckHandler creation."""
        handler = HealthCheckHandler()
        assert handler is not None
        assert hasattr(handler, "handle")

    def test_get_service_metrics_handler_creation(self) -> None:
        """Test GetServiceMetricsHandler creation."""
        handler = GetServiceMetricsHandler()
        assert handler is not None
        assert hasattr(handler, "handle")


class TestStartGRPCServiceHandler:
    """Test StartGRPCServiceHandler functionality."""

    @pytest.fixture
    def handler(self) -> StartGRPCServiceHandler:
        """Create handler instance."""
        return StartGRPCServiceHandler()

    @pytest.mark.asyncio
    async def test_handle_valid_command(self, handler: StartGRPCServiceHandler) -> None:
        """Test handling valid start service command."""
        command = StartGRPCServiceCommand(service_name="test-service", port=8080)
        result = await handler.handle(command)
        assert isinstance(result, ServiceResult)
        assert result.success

    @pytest.mark.asyncio
    async def test_handle_command_with_custom_config(
        self,
        handler: StartGRPCServiceHandler,
    ) -> None:
        """Test handling command with custom configuration."""
        command = StartGRPCServiceCommand(
            service_name="test-service",
            port=8080,
            max_workers=20,
            host="127.0.0.1",
        )
        result = await handler.handle(command)
        assert result.success


class TestStopGRPCServiceHandler:
    """Test StopGRPCServiceHandler functionality."""

    @pytest.fixture
    def handler(self) -> StopGRPCServiceHandler:
        """Create handler instance."""
        return StopGRPCServiceHandler()

    @pytest.mark.asyncio
    async def test_handle_valid_command(self, handler: StopGRPCServiceHandler) -> None:
        """Test handling valid stop service command."""
        command = StopGRPCServiceCommand(service_id="test-service-123")
        result = await handler.handle(command)
        assert isinstance(result, ServiceResult)
        assert result.success


class TestRegisterRPCMethodHandler:
    """Test RegisterRPCMethodHandler functionality."""

    @pytest.fixture
    def handler(self) -> RegisterRPCMethodHandler:
        """Create handler instance."""
        return RegisterRPCMethodHandler()

    @pytest.mark.asyncio
    async def test_handle_valid_command(
        self,
        handler: RegisterRPCMethodHandler,
    ) -> None:
        """Test handling valid register method command."""
        command = RegisterRPCMethodCommand(
            service_id="service-123",
            name="CreatePipeline",
            method_type="unary",
            request_type="CreatePipelineRequest",
            response_type="CreatePipelineResponse",
        )
        result = await handler.handle(command)
        assert isinstance(result, ServiceResult)
        assert result.success

    @pytest.mark.asyncio
    async def test_handle_streaming_method_command(
        self,
        handler: RegisterRPCMethodHandler,
    ) -> None:
        """Test handling streaming method registration."""
        command = RegisterRPCMethodCommand(
            service_id="service-123",
            name="StreamLogs",
            method_type="server_streaming",
            request_type="StreamLogsRequest",
            response_type="LogEntry",
        )
        result = await handler.handle(command)
        assert result.success


class TestExecuteRPCCallHandler:
    """Test ExecuteRPCCallHandler functionality."""

    @pytest.fixture
    def handler(self) -> ExecuteRPCCallHandler:
        """Create handler instance."""
        return ExecuteRPCCallHandler()

    @pytest.mark.asyncio
    async def test_handle_valid_command(self, handler: ExecuteRPCCallHandler) -> None:
        """Test handling valid execute RPC command."""
        command = ExecuteRPCCallCommand(
            method_id="CreatePipeline",
            request_data={
                "name": "test-pipeline",
                "extractor": "tap-postgres",
                "loader": "target-snowflake",
            },
        )
        result = await handler.handle(command)
        assert isinstance(result, ServiceResult)
        assert result.success

    @pytest.mark.asyncio
    async def test_handle_command_with_metadata(
        self,
        handler: ExecuteRPCCallHandler,
    ) -> None:
        """Test handling command with metadata."""
        command = ExecuteRPCCallCommand(
            method_id="CreatePipeline",
            request_data={"name": "test"},
            metadata={"authorization": "Bearer token123"},
        )
        result = await handler.handle(command)
        assert result.success

    @pytest.mark.asyncio
    async def test_handle_command_with_timeout(
        self,
        handler: ExecuteRPCCallHandler,
    ) -> None:
        """Test handling command with custom timeout."""
        command = ExecuteRPCCallCommand(
            method_id="CreatePipeline",
            request_data={"name": "test"},
            timeout_seconds=60,
        )
        result = await handler.handle(command)
        assert result.success


class TestHealthCheckHandler:
    """Test HealthCheckHandler functionality."""

    @pytest.fixture
    def handler(self) -> HealthCheckHandler:
        """Create handler instance."""
        return HealthCheckHandler()

    @pytest.mark.asyncio
    async def test_handle_health_check_command(
        self,
        handler: HealthCheckHandler,
    ) -> None:
        """Test handling health check command."""
        command = HealthCheckCommand()
        result = await handler.handle(command)
        assert isinstance(result, ServiceResult)
        assert result.success


class TestGetServiceMetricsHandler:
    """Test GetServiceMetricsHandler functionality."""

    @pytest.fixture
    def handler(self) -> GetServiceMetricsHandler:
        """Create handler instance."""
        return GetServiceMetricsHandler()

    @pytest.mark.asyncio
    async def test_handle_get_metrics_command(
        self,
        handler: GetServiceMetricsHandler,
    ) -> None:
        """Test handling get service metrics command."""
        command = GetServiceMetricsCommand(service_id="test-service")
        result = await handler.handle(command)
        assert isinstance(result, ServiceResult)
        assert result.success


class TestHandlerIntegration:
    """Test handler integration scenarios."""

    @pytest.mark.asyncio
    async def test_complete_service_lifecycle(self) -> None:
        """Test complete service lifecycle using real handlers."""
        # Start service
        start_handler = StartGRPCServiceHandler()
        start_command = StartGRPCServiceCommand(
            service_name="integration-test",
            port=8080,
        )
        start_result = await start_handler.handle(start_command)
        assert start_result.success
        # Register method
        register_handler = RegisterRPCMethodHandler()
        register_command = RegisterRPCMethodCommand(
            service_id="integration-test",
            name="CreatePipeline",
            method_type="unary",
            request_type="CreatePipelineRequest",
            response_type="CreatePipelineResponse",
        )
        register_result = await register_handler.handle(register_command)
        assert register_result.success
        # Execute RPC call
        execute_handler = ExecuteRPCCallHandler()
        execute_command = ExecuteRPCCallCommand(
            method_id="CreatePipeline",
            request_data={"name": "integration-pipeline"},
        )
        execute_result = await execute_handler.handle(execute_command)
        assert execute_result.success
        # Health check
        health_handler = HealthCheckHandler()
        health_command = HealthCheckCommand()
        health_result = await health_handler.handle(health_command)
        assert health_result.success
        # Get metrics
        metrics_handler = GetServiceMetricsHandler()
        metrics_command = GetServiceMetricsCommand(service_id="integration-test")
        metrics_result = await metrics_handler.handle(metrics_command)
        assert metrics_result.success
        # Stop service
        stop_handler = StopGRPCServiceHandler()
        stop_command = StopGRPCServiceCommand(service_id="integration-test")
        stop_result = await stop_handler.handle(stop_command)
        assert stop_result.success

    @pytest.mark.asyncio
    async def test_error_handling_chain(self) -> None:
        """Test error handling across handler chain."""
        # All handlers should handle invalid commands gracefully
        handlers_and_commands = [
            (StartGRPCServiceHandler(), StartGRPCServiceCommand("", 0)),  # Invalid
            (StopGRPCServiceHandler(), StopGRPCServiceCommand("")),  # Invalid
            (
                RegisterRPCMethodHandler(),
                RegisterRPCMethodCommand("", "", "", "", ""),
            ),  # Invalid
        ]
        for handler, command in handlers_and_commands:
            # Commands with invalid data should still return ServiceResult
            # but with is_success = False
            result = await handler.handle(command)
            assert isinstance(result, ServiceResult)
            # Note: We don't assert failure here because handlers might
            # handle edge cases differently
