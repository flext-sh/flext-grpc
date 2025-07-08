"""FLEXT GRPC - Enterprise gRPC Services with Zero Tolerance for Technical Debt.

Professional imports with proper package management.
"""

from __future__ import annotations

# Version
__version__ = "0.6.0"

# Professional imports from installed flext-core package
try:
    from flext_core import Entity, Pipeline, ServiceResult, ValueObject
    __all__ = ["Entity", "Pipeline", "ServiceResult", "ValueObject", "__version__"]
except ImportError as e:
    print(f"Warning: Could not import flext-core: {e}")
    __all__ = ["__version__"]
