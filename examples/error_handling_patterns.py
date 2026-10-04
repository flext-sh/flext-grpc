"""FLEXT gRPC Error Handling Patterns - Comprehensive error management and recovery.

This module demonstrates comprehensive error handling patterns and recovery strategies
for the FLEXT gRPC communication platform, showcasing robust error management,
validation error handling, and enterprise-grade error recovery patterns following
Clean Architecture and Domain-Driven Design principles.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import time
from typing import NoReturn

from flext_grpc import FlextGrpcConstants, p, r, t, u
from flext_grpc.errors import FlextGrpcErrors

logger = u.fetch_logger(__name__)


def validate_user_input(username: str, email: str) -> p.Result[t.Grpc.Headers]:
    """Validate user input with FlextGrpcErrors.ValidationError."""

    def _raise_username_error() -> NoReturn:
        msg = "Username cannot be empty"
        raise FlextGrpcErrors.ValidationError(msg, field="username")

    def _raise_email_error() -> NoReturn:
        msg = "Invalid email format"
        raise FlextGrpcErrors.ValidationError(msg, field="email")

    try:
        if not username:
            _raise_username_error()
        if not email or "@" not in email:
            _raise_email_error()
        return r[t.Grpc.Headers].ok({"username": username, "email": email})
    except FlextGrpcErrors.ValidationError as e:
        logger.exception("Validation failed", field=e.field or "", error=str(e))
        return r[t.Grpc.Headers].fail(f"Validation error: {e}")


def create_server_config(port: int, workers: int) -> p.Result[t.Grpc.ConfigDict]:
    """Create server configuration with proper error handling."""

    def _raise_port_error() -> NoReturn:
        msg = "Port must be between 1 and 65535"
        raise FlextGrpcErrors.ConfigurationError(msg, config_key="port")

    def _raise_workers_error() -> NoReturn:
        msg = "Workers must be positive"
        raise FlextGrpcErrors.ConfigurationError(msg, config_key="max_workers")

    def _validate_config() -> None:
        max_port = 65535
        if port < 1 or port > max_port:
            _raise_port_error()
        if workers < 1:
            _raise_workers_error()

    try:
        _validate_config()
        settings: t.Grpc.ConfigDict = {
            "host": FlextGrpcConstants.Grpc.NETWORK_DEFAULT_HOST,
            "port": port,
            "max_workers": workers,
        }
        return r[t.Grpc.ConfigDict].ok(settings)
    except FlextGrpcErrors.ConfigurationError as e:
        logger.exception("Configuration error", key=e.config_key or "", error=str(e))
        return r[t.Grpc.ConfigDict].fail(f"Configuration error: {e}")


def simulate_connection_error() -> p.Result[str]:
    """Simulate a connection error scenario."""

    def _raise_connection_error() -> NoReturn:
        msg = "Failed to connect to gRPC server"
        raise FlextGrpcErrors.GrpcConnectionError(msg)

    try:
        _raise_connection_error()
    except FlextGrpcErrors.GrpcConnectionError as e:
        logger.exception("Connection failed", error=str(e))
        return r[str].fail(f"Connection error: {e}")


def simulate_timeout_error() -> p.Result[str]:
    """Simulate a timeout error scenario."""

    def _raise_timeout_error() -> NoReturn:
        msg = "Request timed out after 30 seconds"
        raise FlextGrpcErrors.GrpcTimeoutError(msg)

    try:
        _raise_timeout_error()
    except FlextGrpcErrors.GrpcTimeoutError as e:
        logger.exception("Request timed out", error=str(e))
        return r[str].fail(f"Timeout error: {e}")


def handle_generic_grpc_error() -> p.Result[str]:
    """Handle generic gRPC errors."""

    def _raise_generic_error() -> NoReturn:
        msg = "Unknown gRPC error occurred"
        raise FlextGrpcErrors.Error(msg)

    try:
        _raise_generic_error()
    except FlextGrpcErrors.Error as e:
        logger.exception("Generic gRPC error", error=str(e))
        return r[str].fail(f"gRPC error: {e}")


def comprehensive_error_handling_pipeline() -> p.Result[str]:
    """Demonstrate comprehensive error handling in a realistic pipeline."""
    logger.info("Starting comprehensive error handling pipeline")
    validation_result = validate_user_input("john_doe", "john@example.com")
    if validation_result.failure:
        return r[str].fail(f"Pipeline failed at validation: {validation_result.error}")
    logger.info("✅ User input validation passed")
    config_result = create_server_config(
        FlextGrpcConstants.Grpc.NETWORK_DEFAULT_GRPC_PORT, 4
    )
    if config_result.failure:
        return r[str].fail(f"Pipeline failed at configuration: {config_result.error}")
    logger.info("✅ Server configuration created")
    scenarios = [
        ("connection", simulate_connection_error),
        ("timeout", simulate_timeout_error),
        ("generic", handle_generic_grpc_error),
    ]
    for scenario_name, scenario_func in scenarios:
        result = scenario_func()
        if result.failure:
            logger.warning(
                f"⚠️ {scenario_name} scenario failed as expected: {result.error}"
            )
    return r[str].ok("Pipeline completed with graceful error handling")


def error_recovery_patterns() -> p.Result[str]:
    """Demonstrate error recovery patterns."""
    logger.info("Testing error recovery patterns")
    for attempt in range(3):
        connection_result = simulate_connection_error()
        if connection_result.success:
            logger.info(f"✅ Connection succeeded on attempt {attempt + 1}")
            break
        logger.warning(f"⚠️ Connection attempt {attempt + 1} failed, retrying...")
        last_attempt = 2
        if attempt == last_attempt:
            logger.error("❌ All connection attempts failed")
            return r[str].fail("Connection recovery failed after 3 attempts")
    primary_config_result = create_server_config(-1, 4)
    if primary_config_result.failure:
        logger.warning("Invalid primary settings rejected; trying corrected settings")
        corrected_config_result = create_server_config(
            FlextGrpcConstants.Grpc.NETWORK_DEFAULT_GRPC_PORT, 2
        )
        if corrected_config_result.success:
            logger.info("✅ Corrected configuration successful")
            return r[str].ok("Recovery successful with corrected settings")
    return r[str].fail("All recovery attempts failed")


def demonstrate_error_context() -> None:
    """Demonstrate how error context helps with debugging."""
    logger.info("Demonstrating error context for debugging")
    validation_error = FlextGrpcErrors.ValidationError(
        "Email format is invalid - missing @ symbol", field="user_email"
    )
    config_error = FlextGrpcErrors.ConfigurationError(
        "Invalid port configuration for production environment",
        config_key="server_port",
    )
    logger.error(
        "Validation error with field context",
        error_type=type(validation_error).__name__,
        error_message=str(validation_error),
        field_name=validation_error.field or "",
        error_category="validation",
    )
    logger.error(
        "Configuration error with settings context",
        error_type=type(config_error).__name__,
        error_message=str(config_error),
        config_key=config_error.config_key or "",
        error_category="configuration",
    )


def error_handling() -> p.Result[str]:
    """Demonstrate error handling in contexts."""
    logger.info("Testing error handling patterns")

    def _raise_timeout() -> NoReturn:
        msg = "operation timed out"
        raise FlextGrpcErrors.GrpcTimeoutError(msg)

    try:
        time.sleep(0.1)
        error_condition = True
        if error_condition:
            _raise_timeout()
        return r[str].ok("operation completed")
    except FlextGrpcErrors.GrpcTimeoutError as e:
        logger.exception("timeout occurred", error=str(e))
        return r[str].fail(f"error: {e}")


def main() -> None:
    """Demonstrate all error handling patterns."""
    logger.info("🚀 Starting FLEXT gRPC Error Handling Examples")
    logger.info("\n📋 1. Basic Error Scenarios")
    demonstrate_error_context()
    logger.info("\n🔄 2. Comprehensive Error Handling Pipeline")
    pipeline_result = comprehensive_error_handling_pipeline()
    if pipeline_result.success:
        logger.info(f"✅ Pipeline result: {pipeline_result.value}")
    else:
        logger.error(f"❌ Pipeline failed: {pipeline_result.error}")
    logger.info("\n🔧 3. Error Recovery Patterns")
    recovery_result = error_recovery_patterns()
    if recovery_result.success:
        logger.info(f"✅ Recovery result: {recovery_result.value}")
    else:
        logger.error(f"❌ Recovery failed: {recovery_result.error}")
    logger.info("\n⚡ 4. Error Handling")
    try:
        result = error_handling()
        if result.success:
            logger.info(f"✅ result: {result.value}")
        else:
            logger.error(f"❌ failed: {result.error}")
    except (ValueError, RuntimeError, OSError):
        logger.exception("❌ exception occurred")
    logger.info("\n🎉 Error handling examples completed!")
    logger.info("Key takeaways:")
    logger.info("  • Use specific error types for better debugging")
    logger.info("  • Always use r for error handling")
    logger.info("  • Include context (field names, settings keys) in errors")
    logger.info("  • Implement retry and correction patterns")
    logger.info("  • Log errors with structured context")


if __name__ == "__main__":
    main()
