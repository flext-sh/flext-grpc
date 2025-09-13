
"""Test helpers for end-to-end gRPC tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT.
"""

from __future__ import annotations

from collections.abc import Mapping

from flext_core import FlextTypes

from flext_grpc import FlextGrpcClient, FlextGrpcServer, FlextGrpcService


def assert_server_from_setup(
    setup_result: Mapping[str, object],
    key: str = "server",
) -> FlextGrpcServer:
    """Type-safe server extraction from setup results - DRY pattern."""
    server_entity = setup_result[key]
    if not isinstance(server_entity, FlextGrpcServer):
        raise TypeError(f"Expected FlextGrpcServer, got {type(server_entity)}")
    return server_entity


def assert_client_from_setup(
    setup_result: Mapping[str, object],
    key: str = "client",
) -> FlextGrpcClient:
    """Type-safe client extraction from setup results - DRY pattern."""
    client_entity = setup_result[key]
    if not isinstance(client_entity, FlextGrpcClient):
        raise TypeError(f"Expected FlextGrpcClient, got {type(client_entity)}")
    return client_entity


def assert_service_from_setup(
    setup_result: Mapping[str, object],
    key: str = "service",
) -> FlextGrpcService:
    """Type-safe service extraction from setup results - DRY pattern."""
    service_entity = setup_result[key]
    if not isinstance(service_entity, FlextGrpcService):
        raise TypeError(f"Expected FlextGrpcService, got {type(service_entity)}")
    return service_entity


def assert_dict_from_result(result_data: object) -> FlextTypes.Core.Dict:
    """Type-safe dict extraction from FlextResult data - DRY pattern."""
    if result_data is None:
        msg = "Result data cannot be None"
        raise ValueError(msg)
    if not isinstance(result_data, dict):
        raise TypeError(f"Expected dict, got {type(result_data)}")
    return result_data


def assert_client_from_result(result_data: object) -> FlextGrpcClient:
    """Type-safe client extraction from FlextResult data - DRY pattern."""
    if result_data is None:
        msg = "Result data cannot be None"
        raise ValueError(msg)
    if not isinstance(result_data, FlextGrpcClient):
        raise TypeError(f"Expected FlextGrpcClient, got {type(result_data)}")
    return result_data


def assert_server_from_result(result_data: object) -> FlextGrpcServer:
    """Type-safe server extraction from FlextResult data - DRY pattern."""
    if result_data is None:
        msg = "Result data cannot be None"
        raise ValueError(msg)
    if not isinstance(result_data, FlextGrpcServer):
        raise TypeError(f"Expected FlextGrpcServer, got {type(result_data)}")
    return result_data
