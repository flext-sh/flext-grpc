"""FLEXT gRPC Constants - Minimal configuration constants.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

# =============================================================================
# MINIMAL GRPC CONSTANTS - No duplication with flext-core
# =============================================================================

# Network Constants
FLEXT_GRPC_DEFAULT_HOST = "localhost"
FLEXT_GRPC_DEFAULT_PORT = 50051
FLEXT_GRPC_MIN_PORT = 1
FLEXT_GRPC_MAX_PORT = 65535

# Service Constants
FLEXT_GRPC_DEFAULT_TIMEOUT = 30.0
FLEXT_GRPC_DEFAULT_MAX_WORKERS = 10
FLEXT_GRPC_MIN_WORKERS = 1
FLEXT_GRPC_MAX_WORKERS = 100

# Validation Constants
FLEXT_GRPC_MAX_SERVICE_NAME_LENGTH = 100
FLEXT_GRPC_MAX_METHOD_NAME_LENGTH = 200
FLEXT_GRPC_MIN_TIMEOUT_SECONDS = 0.1
FLEXT_GRPC_MAX_TIMEOUT_SECONDS = 600.0

# Host Name Pattern
FLEXT_GRPC_HOST_NAME_PATTERN = r"^[a-zA-Z0-9.-]+$"

# =============================================================================
# DEFAULT CONFIGURATION
# =============================================================================

FLEXT_GRPC_DEFAULT_CONFIG = {
    "host": FLEXT_GRPC_DEFAULT_HOST,
    "port": FLEXT_GRPC_DEFAULT_PORT,
    "timeout": FLEXT_GRPC_DEFAULT_TIMEOUT,
    "max_workers": FLEXT_GRPC_DEFAULT_MAX_WORKERS,
}

# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    # Configuration
    "FLEXT_GRPC_DEFAULT_CONFIG",
    # Network
    "FLEXT_GRPC_DEFAULT_HOST",
    "FLEXT_GRPC_DEFAULT_MAX_WORKERS",
    "FLEXT_GRPC_DEFAULT_PORT",
    # Service
    "FLEXT_GRPC_DEFAULT_TIMEOUT",
    "FLEXT_GRPC_HOST_NAME_PATTERN",
    "FLEXT_GRPC_MAX_METHOD_NAME_LENGTH",
    "FLEXT_GRPC_MAX_PORT",
    # Validation
    "FLEXT_GRPC_MAX_SERVICE_NAME_LENGTH",
    "FLEXT_GRPC_MAX_TIMEOUT_SECONDS",
    "FLEXT_GRPC_MAX_WORKERS",
    "FLEXT_GRPC_MIN_PORT",
    "FLEXT_GRPC_MIN_TIMEOUT_SECONDS",
    "FLEXT_GRPC_MIN_WORKERS",
]
