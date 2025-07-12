"""Unified gRPC client base for FLEXT Meltano Enterprise - ZERO DUPLICATION.

This module provides the canonical gRPC client implementation that eliminates
duplication between CLI and Web interfaces while maintaining specialized functionality.

Features:
    - Unified configuration through domain_config.py
    - SSL/TLS security with enterprise-grade certificates
    - Connection pooling and resource management
    - Error handling with ServiceResult patterns
    - Python 3.13 type system throughout
    - Strategic TYPE_CHECKING for optimal imports
"""

from __future__ import annotations

import functools
import logging
from typing import TYPE_CHECKING
from typing import Any

import grpc

# Unified configuration management
from flext_core.domain.types import ServiceResult
from flext_core.domain.types import ServiceError
from flext_core.config.domain_config import get_config
from flext_observability.logging import get_logger

logger = get_logger(__name__)

if TYPE_CHECKING:
            from flext_grpc.proto import flext_pb2_grpc
else:
            # Real imports at runtime - NO LAZY LOADING VIOLATIONS
    from flext_grpc.proto import flext_pb2_grpc

# Python 3.13 type aliases for gRPC domain
GrpcConfig = dict[str, Any]
ChannelOptions = list[tuple[str, Any]]
GrpcResponse = dict[str, Any]
DashboardStats = dict[str, int | float]
HealthStatus = dict[str, bool | dict[str, Any]]
ExecutionData = dict[str, str | None]


def get_grpc_channel_target() -> str:
    """Get the gRPC channel target from configuration.
    
    Returns:
        Target string in format "host:port"
    """
    config = get_config()
    grpc_config = config.get_service_config("grpc")
    host = grpc_config.get("host", "localhost")
    port = grpc_config.get("port", 50051)
    return f"{host}:{port}"


def _create_ssl_credentials(cert_file: str | None = None, 
                          key_file: str | None = None,
                          ca_file: str | None = None) -> grpc.ChannelCredentials:
    """Create SSL channel credentials for secure gRPC connections.
    
    Args:
        cert_file: Path to client certificate file
        key_file: Path to client private key file  
        ca_file: Path to CA certificate file
        
    Returns:
        gRPC channel credentials for SSL/TLS
    """
    root_certificates = None
    private_key = None
    certificate_chain = None
    
    if ca_file:
        with open(ca_file, 'rb') as f:
            root_certificates = f.read()
            
    if key_file and cert_file:
        with open(key_file, 'rb') as f:
            private_key = f.read()
        with open(cert_file, 'rb') as f:
            certificate_chain = f.read()
            
    return grpc.ssl_channel_credentials(
        root_certificates=root_certificates,
        private_key=private_key,
        certificate_chain=certificate_chain
    )


class FlextGrpcClientBase:
    """Base gRPC client with unified configuration and connection management.

    This is the CANONICAL implementation that eliminates duplication between
    CLI and Web gRPC clients while providing shared functionality.

    Features:
        - Unified domain configuration
        - Enterprise SSL/TLS security
        - Connection pooling
        - Error handling patterns
        - Resource management
    """

    def __init__(self) -> None:
        self._config = get_config()
        self._grpc_config = self._config.get_service_config("grpc")
        self._logger = logger.bind(component="grpc_client")

    def _get_grpc_message_size(self) -> int:
        return self._config.business.GRPC_DEFAULT_MAX_MESSAGE_SIZE_MB * 1024 * 1024

    def _get_channel_options(self) -> ChannelOptions:
        return [
            (
                "grpc.max_send_message_length",
                self._grpc_config.get(
                    "max_message_length",
                    self._get_grpc_message_size(),
                ),
            ),
            (
                "grpc.max_receive_message_length",
                self._grpc_config.get(
                    "max_message_length",
                    self._get_grpc_message_size(),
                ),
            ),
            # ZERO TOLERANCE: Use unified domain configuration for gRPC keepalive
            ("grpc.keepalive_time_ms", self._config.network.grpc_keepalive_time_ms),
            (
                "grpc.keepalive_timeout_ms",
                self._config.network.grpc_keepalive_timeout_ms,
            ),
            (
                "grpc.keepalive_permit_without_calls",
                self._config.network.grpc_keepalive_permit_without_calls,
            ),
        ]

    def _create_channel(self) -> grpc.Channel:
        target = get_grpc_channel_target()
        options = self._get_channel_options()

        if self._config.network.enable_ssl:
            credentials = _create_ssl_credentials(
                cert_file=self._config.network.ssl_cert_file,
                key_file=self._config.network.ssl_key_file,
                ca_file=self._config.network.ssl_ca_file,
            )
            return grpc.secure_channel(target, credentials, options=options)
        return grpc.insecure_channel(target, options=options)

    def _handle_grpc_error(self, error: grpc.RpcError, operation: str) -> ServiceResult[Any]:
        try:
            error_details = error.details()
        except AttributeError:
            error_details = str(error)

        try:
            error_code = error.code()
        except AttributeError:
            error_code = None

        self._logger.error(
            "gRPC operation failed",
            operation=operation,
            error=error_details,
            code=error_code,
        )

        service_error = ServiceError(
            code=f"GRPC_{error_code.name}" if error_code else "GRPC_ERROR",
            message=f"gRPC {operation} failed: {error_details}",
        )
        return ServiceResult.fail(service_error)

    def _create_stub(self, channel: grpc.Channel) -> flext_pb2_grpc.FlextServiceStub:
        return flext_pb2_grpc.FlextServiceStub(channel)


@functools.lru_cache(maxsize=1)
def get_grpc_client_base() -> FlextGrpcClientBase:
        return FlextGrpcClientBase()
