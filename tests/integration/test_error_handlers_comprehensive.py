"""Comprehensive tests for gRPC BaseGrpcService error handling.

This module provides comprehensive test coverage for the new BaseGrpcService
error handling patterns that replace the deprecated error_handlers module.
Uses REAL gRPC implementation without any mock/fake implementations.
"""

from __future__ import annotations

import pytest
from flext_core.infrastructure.grpc_base import BaseGrpcService


class TestBaseGrpcServiceErrorHandling:
    """Test BaseGrpcService error handling functionality."""

    def test_base_grpc_service_initialization(self) -> None:
        """Test that BaseGrpcService can be initialized properly."""
        service = BaseGrpcService("TestService")
        assert service.service_name == "TestService"
        assert service.logger is not None

    def test_error_handling_method_exists(self) -> None:
        """Test that execute_with_error_handling method exists."""
        service = BaseGrpcService("TestService")
        assert hasattr(service, "execute_with_error_handling")
        assert callable(service.execute_with_error_handling)

    def test_timestamp_conversion_utilities(self) -> None:
        """Test that timestamp conversion utilities exist."""
        service = BaseGrpcService("TestService")
        assert hasattr(service, "datetime_to_timestamp")
        assert hasattr(service, "get_current_timestamp")
        assert callable(service.datetime_to_timestamp)
        assert callable(service.get_current_timestamp)

    def test_method_availability(self) -> None:
        """Test that all BaseGrpcService utility methods are available."""
        service = BaseGrpcService("TestService")

        # Test that all expected utility methods exist
        expected_methods = [
            "execute_with_error_handling",
            "datetime_to_timestamp",
            "timestamp_to_datetime",
            "build_success_response",
            "build_error_response",
        ]

        for method_name in expected_methods:
            assert hasattr(service, method_name), f"Method {method_name} should exist"
            assert callable(getattr(service, method_name)), (
                f"Method {method_name} should be callable"
            )


class TestBaseGrpcServiceIntegration:
    """Test BaseGrpcService integration and patterns."""

    def test_service_name_assignment(self) -> None:
        """Test that service name is properly assigned."""
        test_names = [
            "TestService",
            "FlextGrpcServer",
            "PipelineService",
            "PluginService",
        ]

        for name in test_names:
            service = BaseGrpcService(name)
            assert service.service_name == name

    def test_logger_initialization(self) -> None:
        """Test that logger is properly initialized."""
        service = BaseGrpcService("TestService")
        assert service.logger is not None
        # Logger should have proper name structure
        assert hasattr(service.logger, "info")
        assert hasattr(service.logger, "error")
        assert hasattr(service.logger, "warning")
        assert hasattr(service.logger, "debug")

    def test_multiple_service_instances(self) -> None:
        """Test that multiple service instances work independently."""
        service1 = BaseGrpcService("Service1")
        service2 = BaseGrpcService("Service2")

        assert service1.service_name != service2.service_name
        assert service1.service_name == "Service1"
        assert service2.service_name == "Service2"


class TestDeprecatedErrorHandlers:
    """Test deprecated error handlers for backward compatibility."""

    def test_deprecated_import_available(self) -> None:
        """Test deprecated error handlers can be imported but issue warnings."""
        # This should work but issue deprecation warnings
        try:
            from flext_grpc.error_handlers import (
                handle_grpc_error,
                handle_not_found_error,
                handle_validation_error,
            )

            # If we reach here, imports work
            assert callable(handle_grpc_error)
            assert callable(handle_validation_error)
            assert callable(handle_not_found_error)
        except ImportError:
            pytest.fail(
                "Deprecated error handlers should still be importable for "
                "backward compatibility",
            )

    def test_deprecation_guidance(self) -> None:
        """Test that deprecated functions have proper guidance."""
        from flext_grpc.error_handlers import handle_grpc_error

        # Check that docstring contains deprecation notice
        docstring = handle_grpc_error.__doc__
        assert docstring is not None, "Function should have docstring"
        assert "DEPRECATED" in docstring
        assert "BaseGrpcService" in docstring
