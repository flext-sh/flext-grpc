"""Type stubs for protobuf classes to resolve MyPy issues.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    # Type aliases for protobuf classes to avoid import issues
    type HealthStatus = Any
    type ComponentHealth = Any
    type SystemStats = Any
    type Pipeline = Any
    type ListPipelinesResponse = Any
    type Execution = Any
    type ListPluginsResponse = Any
    type LogEntry = Any
    type CreatePipelineRequest = Any
    type GetPipelineRequest = Any
    type ListPipelinesRequest = Any
    type RunPipelineRequest = Any
    type ListPluginsRequest = Any
    type StreamLogsRequest = Any

    # Status constants
    STATUS_UNSPECIFIED: int
    STATUS_PENDING: int
    STATUS_RUNNING: int
    STATUS_SUCCESS: int
    STATUS_FAILED: int
    STATUS_CANCELLED: int

else:
    # Runtime fallbacks
    HealthStatus = Any
    ComponentHealth = Any
    SystemStats = Any
    Pipeline = Any
    ListPipelinesResponse = Any
    Execution = Any
    ListPluginsResponse = Any
    LogEntry = Any
    CreatePipelineRequest = Any
    GetPipelineRequest = Any
    ListPipelinesRequest = Any
    RunPipelineRequest = Any
    ListPluginsRequest = Any
    StreamLogsRequest = Any

    # Status constants (runtime values)
    STATUS_UNSPECIFIED = 0
    STATUS_PENDING = 1
    STATUS_RUNNING = 2
    STATUS_SUCCESS = 3
    STATUS_FAILED = 4
    STATUS_CANCELLED = 5
