"""🚨 ARCHITECTURAL COMPLIANCE: ELIMINATED DUPLICATE DI Container.

REFATORADO COMPLETO:
- REMOVIDA TODAS as duplicações de FlextContainer/DIContainer
- USA APENAS FlextContainer oficial do flext-core
- Mantém apenas utilitários flext_grpc-específicos
- SEM fallback, backward compatibility ou código duplicado

Copyright (c) 2025 Flext. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Any

# 🚨 ARCHITECTURAL COMPLIANCE: Use ONLY official flext-core FlextContainer
from flext_core import FlextContainer, get_logger

logger = get_logger(__name__)


# ==================== FLEXT_GRPC-SPECIFIC DI UTILITIES ====================

_flext_grpc_container_instance: FlextContainer | None = None


def get_flext_grpc_container() -> FlextContainer:
    """Get FLEXT_GRPC-specific DI container instance.

    Returns:
        FlextContainer: Official container from flext-core.

    """
    global _flext_grpc_container_instance
    if _flext_grpc_container_instance is None:
        _flext_grpc_container_instance = FlextContainer()
    return _flext_grpc_container_instance


def configure_flext_grpc_dependencies() -> None:
    """Configure FLEXT_GRPC dependencies using official FlextContainer."""
    get_flext_grpc_container()

    try:
        # Register module-specific dependencies
        # TODO: Add module-specific service registrations here

        logger.info("FLEXT_GRPC dependencies configured successfully")

    except ImportError as e:
        logger.exception(f"Failed to configure FLEXT_GRPC dependencies: {e}")


def get_flext_grpc_service(service_name: str) -> Any:
    """Get flext_grpc service from container.

    Args:
        service_name: Name of service to retrieve.

    Returns:
        Service instance or None if not found.

    """
    container = get_flext_grpc_container()
    result = container.get(service_name)

    if result.success:
        return result.data

    logger.warning(f"FLEXT_GRPC service '{service_name}' not found: {result.error}")
    return None


def get_domain_types() -> dict[str, Any]:
    """Get domain types for gRPC services.

    Returns:
        Dictionary of domain types available for gRPC services

    """
    return {
        "BaseGrpcService": "flext_grpc.infrastructure.grpc_base.BaseGrpcService",
        "converters": "flext_grpc.converters",
        "grpc_container": get_flext_grpc_container,
    }


def get_service_result() -> type:
    """Get FlextResult class for tests.

    Returns:
        FlextResult class from flext-core

    """
    from flext_core import FlextResult
    return FlextResult


# Initialize flext_grpc dependencies on module import
configure_flext_grpc_dependencies()
