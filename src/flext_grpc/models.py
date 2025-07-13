"""gRPC models using flext-core patterns.

Domain models for gRPC service implementation.
Zero tolerance for primitive types - using domain value objects.
"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from typing import Any

from pydantic import Field

from flext_core import DomainEntity
from flext_core import DomainValueObject


class PipelineModel(DomainEntity):
    """Pipeline entity for gRPC service using flext-core patterns."""

    id: str = Field(..., description="Pipeline unique identifier")
    name: str = Field(..., min_length=1, max_length=255, description="Pipeline name")
    description: str = Field(default="", description="Pipeline description")
    extractor: str = Field(..., min_length=1, description="Extractor plugin name")
    loader: str = Field(..., min_length=1, description="Loader plugin name")
    transform: str | None = Field(None, description="Transform plugin name")
    is_active: bool = Field(default=True, description="Pipeline active status")
    created_by: str = Field(default="grpc-system", description="Pipeline creator")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    config: dict[str, Any] = Field(
        default_factory=dict, description="Pipeline configuration",
    )


class ExecutionModel(DomainEntity):
    """Pipeline execution entity for gRPC service."""

    id: str = Field(..., description="Execution unique identifier")
    pipeline_id: str = Field(..., description="Associated pipeline ID")
    status: str = Field(..., description="Execution status")
    started_at: datetime | None = Field(None, description="Execution start time")
    finished_at: datetime | None = Field(None, description="Execution finish time")
    triggered_by: str | None = Field(None, description="Who triggered the execution")
    error_message: str | None = Field(None, description="Error message if failed")
    records_processed: int | None = Field(
        None, description="Number of records processed",
    )
    metadata: dict[str, str] = Field(
        default_factory=dict, description="Execution metadata",
    )

    @property
    def duration_seconds(self) -> float:
        """Calculate execution duration in seconds."""
        if self.started_at and self.finished_at:
            return (self.finished_at - self.started_at).total_seconds()
        return 0.0

    @property
    def is_running(self) -> bool:
        """Check if execution is currently running."""
        return self.status in {"running", "started"} and self.finished_at is None


class ScheduleModel(DomainEntity):
    """Schedule entity for pipeline automation."""

    id: str = Field(..., description="Schedule unique identifier")
    pipeline_id: str = Field(..., description="Associated pipeline ID")
    cron_expression: str = Field(..., description="Cron expression for scheduling")
    timezone: str = Field(default="UTC", description="Timezone for scheduling")
    is_active: bool = Field(default=True, description="Schedule active status")
    created_by: str = Field(default="grpc-system", description="Schedule creator")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    last_run: datetime | None = Field(None, description="Last execution time")
    next_run: datetime | None = Field(None, description="Next scheduled execution")


class PluginModel(DomainEntity):
    """Plugin entity for plugin management."""

    name: str = Field(..., min_length=1, description="Plugin name")
    plugin_type: str = Field(..., description="Plugin type (tap, target, transform)")
    version: str = Field(..., description="Plugin version")
    description: str = Field(default="", description="Plugin description")
    config_schema: dict[str, Any] = Field(
        default_factory=dict, description="Configuration schema",
    )
    is_installed: bool = Field(default=False, description="Installation status")
    install_path: str | None = Field(None, description="Installation path")
    dependencies: list[str] = Field(
        default_factory=list, description="Plugin dependencies",
    )


class SystemMetrics(DomainValueObject):
    """System metrics for health monitoring."""

    cpu_usage: float = Field(..., ge=0, le=100, description="CPU usage percentage")
    memory_usage: float = Field(
        ..., ge=0, le=100, description="Memory usage percentage",
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
    "ExecutionModel",
    "PipelineModel",
    "PluginModel",
    "ScheduleModel",
    "SystemMetrics",
]
