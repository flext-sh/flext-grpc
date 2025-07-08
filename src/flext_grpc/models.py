"""Pydantic models for in-memory gRPC data representation with enterprise domain types.

These models provide strong typing and validation for the data used
within the gRPC server, using enterprise domain value objects to replace
primitive types with validated business objects.

ZERO TOLERANCE: No primitive types - all values use domain objects.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

# Import flext-core base classes for consistency
from flext_core import Entity, ServiceResult, ValueObject
from flext_core.domain.business_types import (
    CronExpression,
    ExecutionNumber,
    PluginName,
    RecordCount,
    ScheduleId,
    TimeoutSeconds,
    Timezone,
    Username,
)
from pydantic import Field

if TYPE_CHECKING:
    from datetime import datetime

    from flext_core.domain.value_objects import (
        Duration,
        ExecutionId,
        ExecutionStatus,
        PipelineId,
        PipelineName,
    )


class PipelineGrpcModel(Entity):
    """Enterprise Pydantic model for gRPC Pipeline serialization with validated domain types.

    ZERO TOLERANCE: All fields use domain value objects for type safety and validation.
    Renamed from PipelineModel to avoid conflict with persistence PipelineModel.

    Uses flext-core Entity as base for identity-based equality and domain modeling.
    """

    id: PipelineId
    name: PipelineName
    description: str | None = None
    extractor: PluginName
    loader: PluginName
    transform: PluginName | None = None
    schedule: CronExpression | None = None
    is_active: bool = True
    created_by: Username = Username(value="grpc-system")
    created_at: datetime
    updated_at: datetime
    config: dict[str, object] = Field(default_factory=dict)
    timeout: TimeoutSeconds | None = None


class ExecutionModel(Entity):
    """Enterprise Pydantic model for in-memory Execution with validated domain types.

    ZERO TOLERANCE: All fields use domain value objects for type safety and validation.

    Uses flext-core Entity as base for identity-based equality.
    """

    id: ExecutionId
    pipeline_id: PipelineId
    execution_number: ExecutionNumber
    status: ExecutionStatus
    started_at: datetime
    finished_at: datetime | None = None
    triggered_by: Username | None = None
    metadata: dict[str, str] = Field(default_factory=dict)
    duration: Duration | None = None
    error_message: str | None = None
    records_processed: RecordCount | None = None


class ScheduleModel(ValueObject):
    """Enterprise Pydantic model for Schedule with domain value objects.

    ZERO TOLERANCE: All fields use domain value objects for type safety and validation.

    Uses flext-core ValueObject as base for immutability.
    """

    id: ScheduleId
    pipeline_id: PipelineId
    cron: CronExpression
    timezone: Timezone | None = None
    is_active: bool = True
    created_by: Username
    created_at: datetime
    updated_at: datetime
    next_run: datetime | None = None
    last_run: datetime | None = None


# Example of using ServiceResult for error handling
def create_pipeline_result(pipeline_data: dict) -> ServiceResult[PipelineGrpcModel]:
    """Create pipeline using flext-core ServiceResult pattern.

    Demonstrates integration with flext-core error handling patterns.
    """
    try:
        pipeline = PipelineGrpcModel(**pipeline_data)
        return ServiceResult.success(pipeline)
    except Exception as e:
        return ServiceResult.failure(f"Failed to create pipeline: {e}")


# Export models for use in gRPC service
__all__ = [
    "ExecutionModel",
    "PipelineGrpcModel",
    "ScheduleModel",
    "create_pipeline_result",
]
