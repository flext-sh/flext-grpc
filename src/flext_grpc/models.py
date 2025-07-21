"""gRPC models using flext-core patterns.

Domain models for gRPC service implementation.
Zero tolerance for duplication - using flext-core domain models.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.domain.pipeline import Pipeline, PipelineExecution
from flext_core.domain.pydantic_base import DomainEntity, DomainValueObject
from flext_core.domain.shared_models import (
    PluginMetadata,  # Use flext-core PluginMetadata
    PluginType,  # Use flext-core PluginType
)
from pydantic import Field

if TYPE_CHECKING:
    from datetime import datetime
    from uuid import UUID

# Export flext-core entities for gRPC usage - NO DUPLICATION
PipelineModel = Pipeline  # Use flext-core Pipeline aggregate
ExecutionModel = PipelineExecution  # Use flext-core PipelineExecution
PluginModel = PluginMetadata  # Use flext-core PluginMetadata


class ScheduleModel(DomainEntity):
    """Schedule entity for pipeline automation."""

    id: UUID = Field(..., description="Schedule unique identifier")
    name: str = Field(..., description="Schedule name")
    pipeline_id: str = Field(..., description="Associated pipeline ID")
    cron_expression: str = Field(..., description="Cron expression for scheduling")
    timezone: str = Field(default="UTC", description="Timezone for scheduling")
    is_active: bool = Field(default=True, description="Schedule active status")
    created_by: str = Field(default="grpc-system", description="Schedule creator")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    last_run: datetime | None = Field(None, description="Last execution time")
    next_run: datetime | None = Field(None, description="Next scheduled execution")


# PluginModel removed - using flext-core PluginMetadata instead


class SystemMetrics(DomainValueObject):
    """System metrics for health monitoring."""

    cpu_usage: float = Field(..., ge=0, le=100, description="CPU usage percentage")
    memory_usage: float = Field(
        ...,
        ge=0,
        le=100,
        description="Memory usage percentage",
    )
    disk_usage: float = Field(..., ge=0, le=100, description="Disk usage percentage")
    active_pipelines: int = Field(..., ge=0, description="Number of active pipelines")
    total_executions: int = Field(..., ge=0, description="Total executions count")
    failed_executions: int = Field(..., ge=0, description="Failed executions count")
    timestamp: datetime = Field(..., description="Metrics collection timestamp")

    @property
    def success_rate(self) -> float:
        """Calculate success rate percentage."""
        if self.total_executions == 0:
            return 100.0
        return (
            (self.total_executions - self.failed_executions) / self.total_executions
        ) * 100.0

    @property
    def is_healthy(self) -> bool:
        """Check if system is healthy based on metrics."""
        max_usage_threshold = 90.0
        min_success_rate = 95.0

        return (
            self.cpu_usage < max_usage_threshold
            and self.memory_usage < max_usage_threshold
            and self.disk_usage < max_usage_threshold
            and self.success_rate >= min_success_rate
        )


__all__ = [
    "ExecutionModel",  # = flext_core.domain.pipeline.PipelineExecution
    # flext-core entities (aliases for backward compatibility)
    "PipelineModel",  # = flext_core.domain.pipeline.Pipeline
    "PluginModel",  # = flext_core.domain.shared_models.PluginMetadata
    "PluginType",  # = flext_core.domain.shared_models.PluginType
    # gRPC-specific models
    "ScheduleModel",
    "SystemMetrics",
]
