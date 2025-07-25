"""Simple gRPC Helpers."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

# 🚨 ARCHITECTURAL COMPLIANCE: Using DI container for flext-core imports
from flext_grpc.infrastructure.di_container import get_service_result

if TYPE_CHECKING:
    FlextResult = get_service_result()
else:
    FlextResult = get_service_result()


def create_server_config(host: str = "localhost", port: int = 50051) -> dict[str, Any]:
    """Create simple server config."""
    return {"host": host, "port": port, "address": f"{host}:{port}"}


def create_client_config(address: str) -> Any:
    """Create simple client config."""
    try:
        config = {"address": address, "timeout": 30, "retry": True}
        return FlextResult.ok(config)
    except Exception as e:
        return FlextResult.fail(f"Client config failed: {e}")


def format_grpc_error(error: Exception) -> str:
    """Format gRPC error for logging."""
    return f"gRPC Error: {type(error).__name__}: {error}"


def validate_address(address: str) -> FlextResult[bool]:
    """Validate gRPC address format."""
    try:
        if not address:
            return FlextResult.fail("Address cannot be empty")

        if ":" not in address:
            return FlextResult.fail("Address must include port (host:port)")

        return FlextResult.ok(True)
    except (ValueError, TypeError, OSError) as e:
        return FlextResult.fail(f"Address validation failed: {e}")
