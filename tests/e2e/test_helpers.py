"""Helper functions for E2E tests - DRY principle implementation.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flext_grpc.entities import FlextGrpcClient, FlextGrpcServer, FlextGrpcService


def assert_server_from_setup(setup_result: Mapping[str, object], key: str = "server") -> FlextGrpcServer:
    """Type-safe server extraction from setup results - DRY pattern."""
    from flext_grpc.entities import FlextGrpcServer  # noqa: PLC0415
    server_entity = setup_result[key]
    if not isinstance(server_entity, FlextGrpcServer):
        raise TypeError(f"Expected FlextGrpcServer, got {type(server_entity)}")
    return server_entity


def assert_client_from_setup(setup_result: Mapping[str, object], key: str = "client") -> FlextGrpcClient:
    """Type-safe client extraction from setup results - DRY pattern."""
    from flext_grpc.entities import FlextGrpcClient  # noqa: PLC0415
    client_entity = setup_result[key]
    if not isinstance(client_entity, FlextGrpcClient):
        raise TypeError(f"Expected FlextGrpcClient, got {type(client_entity)}")
    return client_entity


def assert_service_from_setup(setup_result: Mapping[str, object], key: str = "service") -> FlextGrpcService:
    """Type-safe service extraction from setup results - DRY pattern."""
    from flext_grpc.entities import FlextGrpcService  # noqa: PLC0415
    service_entity = setup_result[key]
    if not isinstance(service_entity, FlextGrpcService):
        raise TypeError(f"Expected FlextGrpcService, got {type(service_entity)}")
    return service_entity


def assert_dict_from_result(result_data: object) -> dict[str, object]:
    """Type-safe dict extraction from FlextResult data - DRY pattern."""
    if result_data is None:
        raise ValueError("Result data cannot be None")
    if not isinstance(result_data, dict):
        raise TypeError(f"Expected dict, got {type(result_data)}")
    return result_data


def assert_client_from_result(result_data: object) -> FlextGrpcClient:
    """Type-safe client extraction from FlextResult data - DRY pattern."""
    from flext_grpc.entities import FlextGrpcClient  # noqa: PLC0415
    if result_data is None:
        raise ValueError("Result data cannot be None")
    if not isinstance(result_data, FlextGrpcClient):
        raise TypeError(f"Expected FlextGrpcClient, got {type(result_data)}")
    return result_data


def assert_server_from_result(result_data: object) -> FlextGrpcServer:
    """Type-safe server extraction from FlextResult data - DRY pattern."""
    from flext_grpc.entities import FlextGrpcServer  # noqa: PLC0415
    if result_data is None:
        raise ValueError("Result data cannot be None")
    if not isinstance(result_data, FlextGrpcServer):
        raise TypeError(f"Expected FlextGrpcServer, got {type(result_data)}")
    return result_data
