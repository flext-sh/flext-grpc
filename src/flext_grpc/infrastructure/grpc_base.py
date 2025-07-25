"""Base gRPC service implementation.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Base classes and utilities for gRPC services with error handling.
"""

from __future__ import annotations

import logging
from typing import Any

import grpc
from flext_core import FlextResult


class BaseGrpcService:
    """Base class for gRPC services with error handling."""

    def __init__(self, service_name: str) -> None:
        """Initialize the base gRPC service.

        Args:
            service_name: Name of the gRPC service

        """
        self.service_name = service_name
        self.logger = logging.getLogger(f"flext.grpc.{service_name}")

    def handle_error(self, error: Exception, context: grpc.ServicerContext) -> FlextResult[Any]:
        """Handle gRPC service errors.

        Args:
            error: Exception that occurred
            context: gRPC servicer context

        Returns:
            FlextResult with error information

        """
        self.logger.error(f"Error in {self.service_name}: {error}")

        if isinstance(error, grpc.RpcError):
            context.set_code(error.code())
            context.set_details(str(error))
        else:
            context.set_code(internal.invalid)
            context.set_details("Internal server error")

        return FlextResult.fail(str(error))

    def validate_request(self, request: Any) -> FlextResult[bool]:
        """Validate gRPC request.

        Args:
            request: gRPC request object

        Returns:
            FlextResult indicating validation success

        """
        if request is None:
            return FlextResult.fail("Request cannot be None")
        return FlextResult.ok(True)
