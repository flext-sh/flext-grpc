# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Grpc. Models package.

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

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_grpc._models.base import FlextGrpcModelsBase
    from flext_grpc._models.channel_models import FlextGrpcModelsChannel
    from flext_grpc._models.config import FlextGrpcModelsConfig
    from flext_grpc._models.message_models import FlextGrpcModelsMessage
    from flext_grpc._models.runtime_models import FlextGrpcModelsRuntime


__all__: tuple[str, ...] = (
    "FlextGrpcModelsBase",
    "FlextGrpcModelsChannel",
    "FlextGrpcModelsConfig",
    "FlextGrpcModelsMessage",
    "FlextGrpcModelsRuntime",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextGrpcModelsConfig": ".config",
        "FlextGrpcModelsBase": ".base",
        "FlextGrpcModelsChannel": ".channel_models",
        "FlextGrpcModelsMessage": ".message_models",
        "FlextGrpcModelsRuntime": ".runtime_models",
    }),
    public_exports=__all__,
)
