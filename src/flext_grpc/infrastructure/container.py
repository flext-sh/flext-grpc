"""Dependency injection container for FLEXT-GRPC.

REFACTORED:
            Uses flext-core dependency injection patterns.
"""

from __future__ import annotations

from flext_core.config import get_container, singleton

from flext_grpc.infrastructure.config import GRPCConfig, get_grpc_config


@singleton
class GRPCContainerConfig:
    """gRPC container configuration using flext-core patterns."""

    def __init__(self, config: GRPCConfig) -> None:
        """Initialize the container with gRPC configuration."""
        self.config = config

    def configure_dependencies(self) -> None:
        """Configure dependency injection container with gRPC services."""
        container = get_container()

        # Register configuration
        container.register(GRPCConfig, self.config)

        # Register this config instance
        container.register(GRPCContainerConfig, self)


def setup_grpc_container(config: GRPCConfig | None = None) -> GRPCContainerConfig:
    if config is None:
        config = get_grpc_config()

    container_config = GRPCContainerConfig(config)
    container_config.configure_dependencies()

    return container_config


def get_grpc_container() -> GRPCContainerConfig:
    container = get_container()
    return container.resolve(GRPCContainerConfig)
