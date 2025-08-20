"""FLEXT gRPC Error Handling Patterns - Comprehensive error management and recovery.

This module demonstrates comprehensive error handling patterns and recovery strategies
for the FLEXT gRPC communication platform, showcasing robust error management,
validation error handling, and enterprise-grade error recovery patterns following
Clean Architecture and Domain-Driven Design principles.

Error Handling Categories:
    The module provides comprehensive examples of FLEXT gRPC error handling:
    - Validation Errors: Entity validation failures and field-specific error handling
    - Configuration Errors: Configuration validation and setup error management
    - Connection Errors: Network and communication error handling patterns
    - Service Errors: Service operation failures and recovery strategies
    - FlextResult Patterns: Comprehensive success/failure pattern usage

Error Management Patterns:
    - FlextResult Pattern: Railway-oriented programming for error handling
    - Error Context: Detailed error information with context and recovery guidance
    - Error Recovery: Strategies for handling and recovering from various error types
    - Validation Patterns: Domain rule validation and error reporting
    - Enterprise Logging: Error logging and monitoring integration patterns

Key Features Demonstrated:
    - Comprehensive Error Types: All FLEXT gRPC error classes with examples
    - Context Information: Error-specific context and debugging information
    - Recovery Strategies: Error recovery and fallback mechanisms
    - Validation Patterns: Domain validation error handling
    - Monitoring Integration: Error reporting and monitoring patterns

Example:
    Comprehensive error handling pattern:

    >>> from flext_grpc import create_server, FlextGrpcConfig
    >>> from flext_grpc import (
    ...     FlextGrpcValidationError,
    ...     FlextGrpcConfigurationError,
    ... )
    >>>
    >>> try:
    ...     # Attempt configuration with invalid values
    ...     config = FlextGrpcConfig(port=-1, max_workers=0)
    ... except FlextGrpcConfigurationError as e:
    ...     print(f"Configuration error: {e}")
    ...     print(f"Invalid field: {e.config_key}")
    ...     print(f"Invalid value: {e.config_value}")
    ...     # Implement recovery strategy
    ...     config = FlextGrpcConfig()  # Use defaults

Current Implementation Status:
    - ✅ Error Classes: Complete error hierarchy with contextual information
    - ✅ FlextResult Integration: Comprehensive result pattern usage
    - ✅ Validation Errors: Domain validation error handling examples
    - ✅ Recovery Strategies: Error recovery and fallback implementations
    - ✅ Enterprise Patterns: Production-ready error handling patterns

Usage:
    Run this example to see FLEXT gRPC error handling patterns:

    >>> poetry run python examples/03_error_handling_patterns.py

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from typing import Any, NoReturn

# Add src directory to Python path for development
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from flext_core import FlextResult, get_logger

from flext_grpc import (
    FlextGrpcConfigurationError,
    FlextGrpcConnectionError,
    FlextGrpcError,
    FlextGrpcTimeoutError,
    FlextGrpcValidationError,
    create_config,
)

# Setup logging
logger = get_logger(__name__)


def validate_user_input(username: str, email: str) -> FlextResult[dict[str, str]]:
    """Validate user input with FlextGrpcValidationError."""

    def _raise_username_error() -> NoReturn:
        msg = "Username cannot be empty"
        raise FlextGrpcValidationError(msg, field_name="username")

    def _raise_email_error() -> NoReturn:
        msg = "Invalid email format"
        raise FlextGrpcValidationError(msg, field_name="email")

    try:
        if not username:
            _raise_username_error()

        if not email or "@" not in email:
            _raise_email_error()

        return FlextResult[dict[str, str]].ok({"username": username, "email": email})

    except FlextGrpcValidationError as e:
        logger.exception("Validation failed", field=e.field_name, error=str(e))
        return FlextResult[dict[str, str]].fail(f"Validation error: {e}")


def create_server_config(port: int, workers: int) -> FlextResult[Any]:
    """Create server configuration with proper error handling."""

    def _raise_port_error() -> NoReturn:
        msg = "Port must be between 1 and 65535"
        raise FlextGrpcConfigurationError(msg, config_key="port", config_value=port)

    def _raise_workers_error() -> NoReturn:
        msg = "Workers must be positive"
        raise FlextGrpcConfigurationError(
            msg,
            config_key="max_workers",
            config_value=workers,
        )

    def _raise_config_error(error_msg: str) -> NoReturn:
        msg: str = f"Failed to create config: {error_msg}"
        raise FlextGrpcConfigurationError(msg)

    try:
        max_port = 65535
        if port < 1 or port > max_port:
            _raise_port_error()

        if workers < 1:
            _raise_workers_error()

        try:
            config = create_config(host="localhost", port=port, max_workers=workers)
            return FlextResult[Any].ok(config)
        except Exception as e:
            return FlextResult[Any].fail(str(e))

    except FlextGrpcConfigurationError as e:
        logger.exception(
            "Configuration error",
            key=e.config_key,
            value=e.config_value,
            error=str(e),
        )
        return FlextResult[Any].fail(f"Configuration error: {e}")


def simulate_connection_error() -> FlextResult[str]:
    """Simulate a connection error scenario."""

    def _raise_connection_error() -> NoReturn:
        msg = "Failed to connect to gRPC server"
        raise FlextGrpcConnectionError(msg)

    try:
        # Simulate connection failure
        _raise_connection_error()

    except FlextGrpcConnectionError as e:
        logger.exception("Connection failed", error=str(e))
        return FlextResult[str].fail(f"Connection error: {e}")


def simulate_timeout_error() -> FlextResult[str]:
    """Simulate a timeout error scenario."""

    def _raise_timeout_error() -> NoReturn:
        msg = "Request timed out after 30 seconds"
        raise FlextGrpcTimeoutError(msg)

    try:
        # Simulate timeout
        _raise_timeout_error()

    except FlextGrpcTimeoutError as e:
        logger.exception("Request timed out", error=str(e))
        return FlextResult[str].fail(f"Timeout error: {e}")


def handle_generic_grpc_error() -> FlextResult[str]:
    """Handle generic gRPC errors."""

    def _raise_generic_error() -> NoReturn:
        msg = "Unknown gRPC error occurred"
        raise FlextGrpcError(msg)

    try:
        # Simulate generic error
        _raise_generic_error()

    except FlextGrpcError as e:
        logger.exception("Generic gRPC error", error=str(e))
        return FlextResult[str].fail(f"gRPC error: {e}")


def comprehensive_error_handling_pipeline() -> FlextResult[str]:
    """Demonstrate comprehensive error handling in a realistic pipeline."""
    logger.info("Starting comprehensive error handling pipeline")

    # Step 1: Validate user input
    validation_result = validate_user_input("john_doe", "john@example.com")
    if validation_result.is_failure:
        return FlextResult[str].fail(
            f"Pipeline failed at validation: {validation_result.error}",
        )

    logger.info("✅ User input validation passed")

    # Step 2: Create server configuration
    config_result = create_server_config(50051, 4)
    if config_result.is_failure:
        return FlextResult[str].fail(
            f"Pipeline failed at configuration: {config_result.error}",
        )

    logger.info("✅ Server configuration created")

    # Step 3: Test different error scenarios (all will fail, but gracefully)
    scenarios = [
        ("connection", simulate_connection_error),
        ("timeout", simulate_timeout_error),
        ("generic", handle_generic_grpc_error),
    ]

    for scenario_name, scenario_func in scenarios:
        result = scenario_func()
        if result.is_failure:
            logger.warning(
                f"⚠️ {scenario_name} scenario failed as expected: {result.error}",
            )

    return FlextResult[str].ok("Pipeline completed with graceful error handling")


def error_recovery_patterns() -> FlextResult[str]:
    """Demonstrate error recovery patterns."""
    logger.info("Testing error recovery patterns")

    # Pattern 1: Retry with backoff
    for attempt in range(3):
        connection_result = simulate_connection_error()
        if connection_result.success:
            logger.info(f"✅ Connection succeeded on attempt {attempt + 1}")
            break

        logger.warning(f"⚠️ Connection attempt {attempt + 1} failed, retrying...")

        last_attempt = 2
        if attempt == last_attempt:  # Last attempt
            logger.error("❌ All connection attempts failed")
            return FlextResult[str].fail("Connection recovery failed after 3 attempts")

    # Pattern 2: Fallback configuration
    primary_config_result = create_server_config(-1, 4)  # Invalid port
    if primary_config_result.is_failure:
        logger.warning("Primary config failed, trying fallback")

        fallback_config_result = create_server_config(8080, 2)  # Fallback
        if fallback_config_result.success:
            logger.info("✅ Fallback configuration successful")
            return FlextResult[str].ok("Recovery successful with fallback config")

    return FlextResult[str].fail("All recovery attempts failed")


def demonstrate_error_context() -> None:
    """Demonstrate how error context helps with debugging."""
    logger.info("Demonstrating error context for debugging")

    # Create errors with rich context
    validation_error = FlextGrpcValidationError(
        "Email format is invalid - missing @ symbol",
        field_name="user_email",
    )

    config_error = FlextGrpcConfigurationError(
        "Invalid port configuration for production environment",
        config_key="server_port",
        config_value=0,
    )

    # Log errors with context
    logger.error(
        "Validation error with field context",
        error_type=type(validation_error).__name__,
        error_message=str(validation_error),
        field_name=validation_error.field_name,
        error_category="validation",
    )

    logger.error(
        "Configuration error with config context",
        error_type=type(config_error).__name__,
        error_message=str(config_error),
        config_key=config_error.config_key,
        config_value=config_error.config_value,
        error_category="configuration",
    )


async def async_error_handling() -> FlextResult[str]:
    """Demonstrate error handling in async contexts."""
    logger.info("Testing async error handling patterns")

    def _raise_async_timeout() -> NoReturn:
        msg = "Async operation timed out"
        raise FlextGrpcTimeoutError(msg)

    try:
        # Simulate async operation that might fail
        await asyncio.sleep(0.1)  # Simulate work

        # Check for error condition
        error_condition = True  # Simulate error condition
        if error_condition:
            _raise_async_timeout()

        # This would only execute if error_condition is False
        return FlextResult[str].ok("Async operation completed")

    except FlextGrpcTimeoutError as e:
        logger.exception("Async timeout occurred", error=str(e))
        return FlextResult[str].fail(f"Async error: {e}")
    except Exception as e:
        logger.exception("Unexpected async error", error=str(e))
        return FlextResult[str].fail(f"Unexpected async error: {e}")


def main() -> None:
    """Main function demonstrating all error handling patterns."""
    logger.info("🚀 Starting FLEXT gRPC Error Handling Examples")

    # Basic error scenarios
    logger.info("\n📋 1. Basic Error Scenarios")
    demonstrate_error_context()

    # Comprehensive pipeline
    logger.info("\n🔄 2. Comprehensive Error Handling Pipeline")
    pipeline_result = comprehensive_error_handling_pipeline()
    if pipeline_result.success:
        logger.info(f"✅ Pipeline result: {pipeline_result.data}")
    else:
        logger.error(f"❌ Pipeline failed: {pipeline_result.error}")

    # Error recovery patterns
    logger.info("\n🔧 3. Error Recovery Patterns")
    recovery_result = error_recovery_patterns()
    if recovery_result.success:
        logger.info(f"✅ Recovery result: {recovery_result.data}")
    else:
        logger.error(f"❌ Recovery failed: {recovery_result.error}")

    # Async error handling
    logger.info("\n⚡ 4. Async Error Handling")
    try:
        async_result = asyncio.run(async_error_handling())
        if async_result.success:
            logger.info(f"✅ Async result: {async_result.data}")
        else:
            logger.error(f"❌ Async failed: {async_result.error}")
    except Exception:
        logger.exception("❌ Async exception occurred")

    logger.info("\n🎉 Error handling examples completed!")
    logger.info("Key takeaways:")
    logger.info("  • Use specific error types for better debugging")
    logger.info("  • Always use FlextResult for error handling")
    logger.info("  • Include context (field names, config keys) in errors")
    logger.info("  • Implement retry and fallback patterns")
    logger.info("  • Log errors with structured context")


if __name__ == "__main__":
    main()
