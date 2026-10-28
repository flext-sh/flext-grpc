"""Base models for flext-grpc.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)

from flext_grpc.config_models import FlextGrpcModelsConfigNamespace


class FlextGrpcModelsBase(FlextGrpcModelsConfigNamespace):
    """Base models for flext-grpc."""


__all__: list[str] = ["FlextGrpcModelsBase"]
