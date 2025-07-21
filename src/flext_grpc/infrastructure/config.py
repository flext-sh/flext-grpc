"""Configuration redirects to unified configuration.

DEPRECATED: This file should redirect to unified configuration patterns.
For backward compatibility, re-export the existing configuration with minimal changes.

TODO: Consolidate into flext-core unified configuration patterns when available.
"""

from __future__ import annotations

# Import the existing configuration - will be unified with flext-core patterns later
from flext_grpc.config import (
    GRPCSettings as GRPCConfig,
    get_grpc_settings as get_grpc_config,
)

# Re-export for backward compatibility
__all__ = ["GRPCConfig", "get_grpc_config"]
