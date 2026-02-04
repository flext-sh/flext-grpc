"""Backward compatibility classes for flext-grpc public API.

Exception and model aliases with real inheritance for consumers
that import from package root.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextExceptions

from flext_grpc.models import FlextGrpcModels


class FlextGrpcError(FlextExceptions.BaseError):
    """FlextGrpcError - real inheritance from BaseError."""


class FlextGrpcSettingsurationError(FlextExceptions.ConfigurationError):
    """FlextGrpcSettingsurationError - real inheritance from ConfigurationError."""


class FlextGrpcConnectionError(FlextExceptions.ConnectionError):
    """FlextGrpcConnectionError - real inheritance from ConnectionError."""


class FlextGrpcTimeoutError(FlextExceptions.TimeoutError):
    """FlextGrpcTimeoutError - real inheritance from TimeoutError."""


class FlextGrpcValidationError(FlextExceptions.ValidationError):
    """FlextGrpcValidationError - real inheritance from ValidationError."""


class GrpcHealthCheck(FlextGrpcModels.Grpc.GrpcHealthCheck):
    """GrpcHealthCheck - real inheritance from Domain.GrpcHealthCheck."""


class GrpcRequest(FlextGrpcModels.Grpc.GrpcRequest):
    """GrpcRequest - real inheritance from Domain.GrpcRequest."""


class ServiceDefinition(FlextGrpcModels.Grpc.ServiceDefinition):
    """ServiceDefinition - real inheritance from ServiceDefinition."""


class ServiceMetrics(FlextGrpcModels.Grpc.ServiceMetrics):
    """ServiceMetrics - real inheritance from ServiceMetrics."""


class StreamInfo(FlextGrpcModels.Grpc.StreamInfo):
    """StreamInfo - real inheritance from Domain.StreamInfo."""


class StreamMetrics(FlextGrpcModels.Grpc.StreamMetrics):
    """StreamMetrics - real inheritance from Domain.StreamMetrics."""
