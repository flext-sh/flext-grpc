"""Domain ports (interfaces) for FLEXT-GRPC.

Using flext-core patterns - NO duplication.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from uuid import UUID

    from flext_core.domain.pydantic_base import ServiceResult
    from flext_grpc.domain.entities import GRPCService
    from flext_grpc.domain.entities import RPCCall
    from flext_grpc.domain.entities import RPCMethod


class GRPCServiceRepository(ABC):
    """Repository interface for gRPC services."""

    @abstractmethod
    async def save(self, service: GRPCService) -> ServiceResult[GRPCService]:
        """Save a gRPC service.

        Args:
            service: The gRPC service to save.

        Returns:
            ServiceResult[GRPCService]: Result containing the saved service.

        """
        ...

    @abstractmethod
    async def get_by_id(self, service_id: UUID) -> ServiceResult[GRPCService | None]:
        """Get a gRPC service by its ID.

        Args:
            service_id: The unique identifier of the service.

        Returns:
            ServiceResult[GRPCService | None]: Result containing the service or None if not found.

        """
        ...

    @abstractmethod
    async def get_by_name(self, name: str) -> ServiceResult[GRPCService | None]:
        """Get a gRPC service by its name.

        Args:
            name: The name of the service.

        Returns:
            ServiceResult[GRPCService | None]: Result containing the service or None if not found.

        """
        ...

    @abstractmethod
    async def list_all(self) -> ServiceResult[list[GRPCService]]:
        """List all gRPC services.

        Returns:
            ServiceResult[list[GRPCService]]: Result containing list of all services.

        """
        ...

    @abstractmethod
    async def delete(self, service_id: UUID) -> ServiceResult[bool]:
        """Delete a gRPC service by its ID.

        Args:
            service_id: The unique identifier of the service to delete.

        Returns:
            ServiceResult[bool]: Result containing True if deleted successfully.

        """
        ...


class RPCMethodRepository(ABC):
    """Repository interface for RPC methods."""

    @abstractmethod
    async def save(self, method: RPCMethod) -> ServiceResult[RPCMethod]:
        """Save an RPC method.

        Args:
            method: The RPC method to save.

        Returns:
            ServiceResult[RPCMethod]: Result containing the saved method.

        """
        ...

    @abstractmethod
    async def get_by_id(self, method_id: UUID) -> ServiceResult[RPCMethod | None]:
        """Get an RPC method by its ID.

        Args:
            method_id: The unique identifier of the method.

        Returns:
            ServiceResult[RPCMethod | None]: Result containing the method or None if not found.

        """
        ...

    @abstractmethod
    async def get_by_service_id(
        self,
        service_id: UUID,
    ) -> ServiceResult[list[RPCMethod]]:
        """Get all RPC methods for a specific service.

        Args:
            service_id: The unique identifier of the service.

        Returns:
            ServiceResult[list[RPCMethod]]: Result containing list of methods for the service.

        """
        ...

    @abstractmethod
    async def get_by_name(
        self,
        service_id: UUID,
        name: str,
    ) -> ServiceResult[RPCMethod | None]:
        """Get an RPC method by service ID and method name.

        Args:
            service_id: The unique identifier of the service.
            name: The name of the method.

        Returns:
            ServiceResult[RPCMethod | None]: Result containing the method or None if not found.

        """
        ...

    @abstractmethod
    async def delete(self, method_id: UUID) -> ServiceResult[bool]:
        """Delete an RPC method by its ID.

        Args:
            method_id: The unique identifier of the method to delete.

        Returns:
            ServiceResult[bool]: Result containing True if deleted successfully.

        """
        ...


class RPCCallRepository(ABC):
    """Repository interface for RPC calls."""

    @abstractmethod
    async def save(self, call: RPCCall) -> ServiceResult[RPCCall]:
        """Save an RPC call.

        Args:
            call: The RPC call to save.

        Returns:
            ServiceResult[RPCCall]: Result containing the saved call.

        """
        ...

    @abstractmethod
    async def get_by_id(self, call_id: UUID) -> ServiceResult[RPCCall | None]:
        """Get an RPC call by its ID.

        Args:
            call_id: The unique identifier of the call.

        Returns:
            ServiceResult[RPCCall | None]: Result containing the call or None if not found.

        """
        ...

    @abstractmethod
    async def get_by_method_id(
        self,
        method_id: UUID,
        limit: int = 100,
    ) -> ServiceResult[list[RPCCall]]:
        """Get RPC calls for a specific method.

        Args:
            method_id: The unique identifier of the method.
            limit: Maximum number of calls to return.

        Returns:
            ServiceResult[list[RPCCall]]: Result containing list of calls for the method.

        """
        ...

    @abstractmethod
    async def get_active_calls(self) -> ServiceResult[list[RPCCall]]:
        """Get all currently active RPC calls.

        Returns:
            ServiceResult[list[RPCCall]]: Result containing list of active calls.

        """
        ...

    @abstractmethod
    async def delete(self, call_id: UUID) -> ServiceResult[bool]:
        """Delete an RPC call by its ID.

        Args:
            call_id: The unique identifier of the call to delete.

        Returns:
            ServiceResult[bool]: Result containing True if deleted successfully.

        """
        ...


class GRPCServerPort(ABC):
    """Port interface for gRPC server operations."""

    @abstractmethod
    async def start_service(self, service: GRPCService) -> ServiceResult[None]:
        """Start a gRPC service.

        Args:
            service: The gRPC service to start.

        Returns:
            ServiceResult[None]: Result indicating success or failure.

        """
        ...

    @abstractmethod
    async def stop_service(self, service_id: UUID) -> ServiceResult[None]:
        """Stop a gRPC service.

        Args:
            service_id: The unique identifier of the service to stop.

        Returns:
            ServiceResult[None]: Result indicating success or failure.

        """
        ...

    @abstractmethod
    async def get_service_health(self, service_id: UUID) -> ServiceResult[bool]:
        """Get the health status of a gRPC service.

        Args:
            service_id: The unique identifier of the service.

        Returns:
            ServiceResult[bool]: Result containing True if service is healthy.

        """
        ...

    @abstractmethod
    async def get_service_metrics(
        self,
        service_id: UUID,
    ) -> ServiceResult[dict[str, float]]:
        """Get metrics for a gRPC service.

        Args:
            service_id: The unique identifier of the service.

        Returns:
            ServiceResult[dict[str, float]]: Result containing service metrics.

        """
        ...


class GRPCClientPort(ABC):
    """Port interface for gRPC client operations."""

    @abstractmethod
    async def create_client(self, service: GRPCService) -> ServiceResult[None]:
        """Create a gRPC client for a service.

        Args:
            service: The gRPC service to create a client for.

        Returns:
            ServiceResult[None]: Result indicating success or failure.

        """
        ...

    @abstractmethod
    async def call_method(self, call: RPCCall) -> ServiceResult[RPCCall]:
        """Execute an RPC method call.

        Args:
            call: The RPC call to execute.

        Returns:
            ServiceResult[RPCCall]: Result containing the completed call with response.

        """
        ...

    @abstractmethod
    async def close_client(self, service_id: UUID) -> ServiceResult[None]:
        """Close a gRPC client for a service.

        Args:
            service_id: The unique identifier of the service.

        Returns:
            ServiceResult[None]: Result indicating success or failure.

        """
        ...


class MetricsPort(ABC):
    """Port interface for metrics collection."""

    @abstractmethod
    async def record_call_metrics(self, call: RPCCall) -> ServiceResult[None]:
        """Record metrics for an RPC call.

        Args:
            call: The RPC call to record metrics for.

        Returns:
            ServiceResult[None]: Result indicating success or failure.

        """
        ...

    @abstractmethod
    async def get_service_metrics(
        self,
        service_id: UUID,
    ) -> ServiceResult[dict[str, float]]:
        """Get metrics for a service.

        Args:
            service_id: The unique identifier of the service.

        Returns:
            ServiceResult[dict[str, float]]: Result containing service metrics.

        """
        ...

    @abstractmethod
    async def get_method_metrics(
        self,
        method_id: UUID,
    ) -> ServiceResult[dict[str, float]]:
        """Get metrics for an RPC method.

        Args:
            method_id: The unique identifier of the method.

        Returns:
            ServiceResult[dict[str, float]]: Result containing method metrics.

        """
        ...
