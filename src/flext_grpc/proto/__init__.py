"""Protocol buffer definitions for FLEXT gRPC services.

CRITICAL: Uses REAL Protocol Buffers only - NO mock or fallback implementations.
Zero tolerance for mock/fake code in production.
"""

from __future__ import annotations

# Import REAL protobuf modules only - NO fallbacks, NO mock classes
from flext_grpc.proto import flext_pb2, flext_pb2_grpc

__all__ = ["flext_pb2", "flext_pb2_grpc"]
