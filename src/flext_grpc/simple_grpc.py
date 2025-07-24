"""Simple gRPC Helpers."""

from __future__ import annotations

from typing import Any

# 🚨 ARCHITECTURAL COMPLIANCE: Using DI container for flext-core imports
from flext_grpc.infrastructure.di_container import get_service_result

ServiceResult = get_service_result()


def create_server_config(host: str = "localhost", port: int = 50051) -> dict[str, Any]:
    """Create simple server config."""
    return {"host": host, "port": port, "address": f"{host}:{port}"}


def create_client_config(address: str) -> ServiceResult[dict[str, Any]]:
    """Create simple client config."""
    try:
        config = {"address": address, "timeout": 30, "retry": True}
        return ServiceResult.ok(config)
    except Exception as e:
        return ServiceResult.fail(f"Client config failed: {e}")


def format_grpc_error(error: Exception) -> str:
    """Format gRPC error for logging."""
    return f"gRPC Error: {type(error).__name__}: {error}"


def validate_address(address: str) -> ServiceResult[bool]:
    """Validate gRPC address format."""
    try:
        if not address:
            return ServiceResult.fail("Address cannot be empty")

        if ":" not in address:
            return ServiceResult.fail("Address must include port (host:port)")

        return ServiceResult.ok(True)
    except Exception as e:
        return ServiceResult.fail(f"Address validation failed: {e}")
