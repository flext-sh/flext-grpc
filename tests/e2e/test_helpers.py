"""FLEXT gRPC E2E Test Helpers - Comprehensive utilities for end-to-end testing.

This module provides comprehensive helper functions and utilities for FLEXT gRPC
end-to-end testing, implementing DRY principles with reusable test components,
data generation, and validation utilities for enterprise testing scenarios.

Helper Categories:
    The module provides essential E2E testing utilities:
    - Entity Creation: Pre-configured entities for realistic testing scenarios
    - Workflow Helpers: Common workflow patterns and test sequences
    - Validation Utilities: Comprehensive validation and assertion helpers
    - Data Generation: Realistic test data creation for various scenarios
    - Performance Helpers: Timing and performance measurement utilities

Testing Utilities:
    Helper functions follow enterprise testing patterns:
    - DRY Principle: Reusable components to eliminate code duplication
    - Configuration Management: Standard configurations for testing scenarios
    - Validation Patterns: Consistent validation and assertion utilities
    - Data Management: Realistic test data generation and management
    - Performance Testing: Timing and throughput measurement utilities

Key Features:
    - Entity Factory Functions: Create realistic entities for testing
    - Workflow Validation: Common workflow pattern validation
    - Performance Measurement: Timing and throughput validation utilities
    - Error Simulation: Realistic error scenario generation
    - Integration Helpers: Cross-component integration testing utilities

Example:
    Standard helper function usage pattern:

    >>> # Create realistic test entities
    >>> server = create_test_server_with_services()
    >>> client = create_test_client_with_options()
    >>> # Validate complete workflows
    >>> workflow_result = validate_complete_workflow(server, client)
    >>> assert workflow_result.success

Integration:
    - Provides utilities for all FLEXT gRPC E2E testing scenarios
    - Integrates with entity creation patterns from flext_grpc.entities
    - Uses flext-core patterns for consistent result handling
    - Supports realistic testing scenarios and performance validation

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Mapping

    from flext_grpc.entities import FlextGrpcClient, FlextGrpcServer, FlextGrpcService


def assert_server_from_setup(
    setup_result: Mapping[str, object],
    key: str = "server",
) -> FlextGrpcServer:
    """Type-safe server extraction from setup results - DRY pattern."""
    from flext_grpc.entities import FlextGrpcServer

    server_entity = setup_result[key]
    if not isinstance(server_entity, FlextGrpcServer):
        raise TypeError(f"Expected FlextGrpcServer, got {type(server_entity)}")
    return server_entity


def assert_client_from_setup(
    setup_result: Mapping[str, object],
    key: str = "client",
) -> FlextGrpcClient:
    """Type-safe client extraction from setup results - DRY pattern."""
    from flext_grpc.entities import FlextGrpcClient

    client_entity = setup_result[key]
    if not isinstance(client_entity, FlextGrpcClient):
        raise TypeError(f"Expected FlextGrpcClient, got {type(client_entity)}")
    return client_entity


def assert_service_from_setup(
    setup_result: Mapping[str, object],
    key: str = "service",
) -> FlextGrpcService:
    """Type-safe service extraction from setup results - DRY pattern."""
    from flext_grpc.entities import FlextGrpcService

    service_entity = setup_result[key]
    if not isinstance(service_entity, FlextGrpcService):
        raise TypeError(f"Expected FlextGrpcService, got {type(service_entity)}")
    return service_entity


def assert_dict_from_result(result_data: object) -> dict[str, object]:
    """Type-safe dict extraction from FlextResult data - DRY pattern."""
    if result_data is None:
        msg = "Result data cannot be None"
        raise ValueError(msg)
    if not isinstance(result_data, dict):
        raise TypeError(f"Expected dict, got {type(result_data)}")
    return result_data


def assert_client_from_result(result_data: object) -> FlextGrpcClient:
    """Type-safe client extraction from FlextResult data - DRY pattern."""
    from flext_grpc.entities import FlextGrpcClient

    if result_data is None:
        msg = "Result data cannot be None"
        raise ValueError(msg)
    if not isinstance(result_data, FlextGrpcClient):
        raise TypeError(f"Expected FlextGrpcClient, got {type(result_data)}")
    return result_data


def assert_server_from_result(result_data: object) -> FlextGrpcServer:
    """Type-safe server extraction from FlextResult data - DRY pattern."""
    from flext_grpc.entities import FlextGrpcServer

    if result_data is None:
        msg = "Result data cannot be None"
        raise ValueError(msg)
    if not isinstance(result_data, FlextGrpcServer):
        raise TypeError(f"Expected FlextGrpcServer, got {type(result_data)}")
    return result_data
