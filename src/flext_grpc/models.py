"""Compatibility models module mapping to grpc_models.

Re-exports domain models for tests that import flext_grpc.models directly.
"""
from __future__ import annotations

from flext_grpc.grpc_models import *  # noqa: F401,F403
