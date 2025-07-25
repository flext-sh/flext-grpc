"""gRPC server implementation for FLEXT.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

gRPC server with FLEXT integration and service management.
"""

from __future__ import annotations

import logging
from concurrent.futures import ThreadPoolExecutor
from typing import TYPE_CHECKING

import grpc
from flext_core import FlextResult

if TYPE_CHECKING:
    from flext_grpc.infrastructure.grpc_base import BaseGrpcService


class FlextGrpcServer:
    """FLEXT gRPC server with service management."""

    def __init__(self, host: str = "localhost", port: int = 50051) -> None:
        """Initialize the gRPC server.

        Args:
            host: Server host address
            port: Server port number

        """
        self.host = host
        self.port = port
        self.server: grpc.Server | None = None
        self.services: list[BaseGrpcService] = []
        self.logger = logging.getLogger("flext.grpc.server")

    def add_service(self, service: BaseGrpcService) -> FlextResult[bool]:
        """Add a gRPC service to the server.

        Args:
            service: gRPC service to add

        Returns:
            FlextResult indicating success

        """
        try:
            self.services.append(service)
            self.logger.info(f"Added service: {service.service_name}")
            return FlextResult.ok(True)
        except Exception as e:
            return FlextResult.fail(f"Failed to add service: {e}")

    def start(self) -> FlextResult[bool]:
        """Start the gRPC server.

        Returns:
            FlextResult indicating success

        """
        try:
            executor = ThreadPoolExecutor(max_workers=10)
            self.server = grpc.server(executor)

            # Add services to server
            for service in self.services:
                self.logger.info(f"Registering service: {service.service_name}")

            # Start server
            listen_addr = f"{self.host}:{self.port}"
            self.server.add_insecure_port(listen_addr)
            self.server.start()

            self.logger.info(f"gRPC server started on {listen_addr}")
            return FlextResult.ok(True)

        except Exception as e:
            return FlextResult.fail(f"Failed to start server: {e}")

    def stop(self, grace_period: float = 5.0) -> FlextResult[bool]:
        """Stop the gRPC server.

        Args:
            grace_period: Grace period for shutdown

        Returns:
            FlextResult indicating success

        """
        try:
            if self.server:
                self.server.stop(grace_period)
                self.logger.info("gRPC server stopped")
            return FlextResult.ok(True)
        except Exception as e:
            return FlextResult.fail(f"Failed to stop server: {e}")

    async def wait_for_termination(self) -> None:
        """Wait for server termination."""
        if self.server:
            await self.server.wait_for_termination()
