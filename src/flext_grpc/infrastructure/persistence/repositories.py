"""Repository implementations for FLEXT-GRPC.

REFACTORED: Uses flext-core Repository pattern - NO duplication.
"""

from __future__ import annotations

from uuid import UUID

from flext_core.domain.core import Repository, RepositoryError
from flext_core.domain.types import ServiceResult
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from flext_grpc.domain.entities import GRPCService, RPCCall, RPCMethod
from flext_grpc.infrastructure.persistence.models import (
    GRPCServiceModel,
    RPCCallModel,
    RPCMethodModel,
)


class BaseRepositoryMixin:
    """Base repository mixin with common functionality.

    Extending flext-core patterns.
    """

    def __init__(self, database_url: str) -> None:
        """Initialize repository with database URL.

        Args:
            database_url: Database connection URL

        """
        self.engine = create_async_engine(database_url)
        self.session_factory = async_sessionmaker(
            self.engine,
            expire_on_commit=False,
        )

    async def get_session(self) -> AsyncSession:
        """Get a new database session.

        Returns:
            New async database session.

        """
        return self.session_factory()

    async def close(self) -> None:
        """Close the database engine and clean up resources."""
        await self.engine.dispose()


class PostgreSQLGRPCServiceRepository(
    BaseRepositoryMixin,
    Repository[GRPCService, UUID],
):
    """PostgreSQL implementation of GRPCServiceRepository."""

    async def save(self, service: GRPCService) -> GRPCService:
        """Save a gRPC service to the database.

        Args:
            service: The gRPC service to save.

        Returns:
            GRPCService: The saved service.

        Raises:
            RepositoryError: If save operation fails.

        """
        try:
            async with await self.get_session() as session:
                # Check if service exists:
                existing = await session.get(GRPCServiceModel, service.id)

                if existing:
                    # Update existing service
                    for key, value in service.model_dump().items():
                        setattr(existing, key, value)
                    model = existing
                else:
                    # Create new service
                    model = GRPCServiceModel(**service.model_dump())
                    session.add(model)

                await session.commit()
                await session.refresh(model)

                # Convert back to domain entity
                return GRPCService(**model.to_dict())
        except Exception as e:
            msg = f"Error in operation: {e}"
            raise RepositoryError(msg) from e

    async def get_by_id(self, service_id: UUID) -> GRPCService | None:
        """Get gRPC service by ID - Repository interface method."""
        return await self._get_by_id_internal(service_id)

    async def _get_by_id_internal(self, service_id: UUID) -> GRPCService | None:
        """Get a gRPC service by its ID.

        Args:
            service_id: Unique identifier of the service.

        Returns:
            The service or None if not found.

        """
        try:
            async with await self.get_session() as session:
                stmt = select(GRPCServiceModel).where(GRPCServiceModel.id == service_id)
                result = await session.execute(stmt)
                model = result.scalar_one_or_none()

                if model is None:
                    return None

                return GRPCService(**model.to_dict())

        except Exception as e:
            msg = f"Failed to get service: {e!s}"
            raise RepositoryError(msg) from e

    async def get_by_name(self, name: str) -> ServiceResult[GRPCService | None]:
        """Get a gRPC service by its name.

        Args:
            name: Name of the service to retrieve.

        Returns:
            ServiceResult containing the service or None if not found.

        """
        try:
            async with await self.get_session() as session:
                stmt = select(GRPCServiceModel).where(GRPCServiceModel.name == name)
                result = await session.execute(stmt)
                model = result.scalar_one_or_none()

                if model is None:
                    return ServiceResult.ok(None)

                domain_service = GRPCService(**model.to_dict())
                return ServiceResult.ok(domain_service)

        except Exception as e:
            return ServiceResult.fail(f"Failed to get service by name: {e!s}")

    async def list_all(self) -> ServiceResult[list[GRPCService]]:
        """List all gRPC services.

        Returns:
            ServiceResult containing list of all services.

        """
        try:
            async with await self.get_session() as session:
                stmt = select(GRPCServiceModel)
                result = await session.execute(stmt)
                models = result.scalars().all()

                services = [GRPCService(**model.to_dict()) for model in models]
                return ServiceResult.ok(services)

        except Exception as e:
            return ServiceResult.fail(f"Failed to list services: {e!s}")

    async def delete(self, service_id: UUID) -> bool:
        """Delete a gRPC service by its ID.

        Args:
            service_id: Unique identifier of the service to delete.

        Returns:
            True if deleted, False if not found.

        Raises:
            RepositoryError: If delete operation fails.

        """
        try:
            async with await self.get_session() as session:
                stmt = delete(GRPCServiceModel).where(GRPCServiceModel.id == service_id)
                result = await session.execute(stmt)
                await session.commit()

                return result.rowcount > 0
        except Exception as e:
            msg = f"Error in operation: {e}"
            raise RepositoryError(msg) from e


class PostgreSQLRPCMethodRepository(BaseRepositoryMixin, Repository[RPCMethod, UUID]):
    """PostgreSQL implementation of RPCMethodRepository."""

    async def save(self, method: RPCMethod) -> RPCMethod:
        """Save an RPC method to the database.

        Args:
            method: The RPC method to save.

        Returns:
            RPCMethod: The saved method.

        Raises:
            RepositoryError: If save operation fails.

        """
        try:
            async with await self.get_session() as session:
                # Check if method exists:
                existing = await session.get(RPCMethodModel, method.id)

                if existing:
                    # Update existing method
                    for key, value in method.model_dump().items():
                        setattr(existing, key, value)
                    model = existing
                else:
                    # Create new method
                    model = RPCMethodModel(**method.model_dump())
                    session.add(model)

                await session.commit()
                await session.refresh(model)

                # Convert back to domain entity
                return RPCMethod(**model.to_dict())
        except Exception as e:
            msg = f"Error in operation: {e}"
            raise RepositoryError(msg) from e

    async def get(self, method_id: UUID) -> RPCMethod | None:
        """Get RPC method by ID - Repository interface method."""
        return await self.get_by_id(method_id)

    async def get_by_id(self, method_id: UUID) -> RPCMethod | None:
        """Get an RPC method by its ID.

        Args:
            method_id: Unique identifier of the method.

        Returns:
            The method or None if not found.

        """
        try:
            async with await self.get_session() as session:
                stmt = select(RPCMethodModel).where(RPCMethodModel.id == method_id)
                result = await session.execute(stmt)
                model = result.scalar_one_or_none()

                if model is None:
                    return None

                return RPCMethod(**model.to_dict())

        except Exception as e:
            msg = f"Failed to get method: {e!s}"
            raise RepositoryError(msg) from e

    async def get_by_service_id(
        self,
        service_id: UUID,
    ) -> ServiceResult[list[RPCMethod]]:
        """Get all RPC methods for a specific service.

        Args:
            service_id: Unique identifier of the service.

        Returns:
            ServiceResult containing list of methods for the service.

        """
        try:
            async with await self.get_session() as session:
                stmt = select(RPCMethodModel).where(
                    RPCMethodModel.service_id == service_id,
                )
                result = await session.execute(stmt)
                models = result.scalars().all()

                methods = [RPCMethod(**model.to_dict()) for model in models]
                return ServiceResult.ok(methods)

        except Exception as e:
            return ServiceResult.fail(f"Failed to get methods by service: {e!s}")

    async def get_by_name(
        self,
        service_id: UUID,
        name: str,
    ) -> ServiceResult[RPCMethod | None]:
        """Get an RPC method by service ID and method name.

        Args:
            service_id: Unique identifier of the service.
            name: Name of the method to retrieve.

        Returns:
            ServiceResult containing the method or None if not found.

        """
        try:
            async with await self.get_session() as session:
                stmt = select(RPCMethodModel).where(
                    RPCMethodModel.service_id == service_id,
                    RPCMethodModel.name == name,
                )
                result = await session.execute(stmt)
                model = result.scalar_one_or_none()

                if model is None:
                    return ServiceResult.ok(None)

                domain_method = RPCMethod(**model.to_dict())
                return ServiceResult.ok(domain_method)

        except Exception as e:
            return ServiceResult.fail(f"Failed to get method by name: {e!s}")

    async def delete(self, method_id: UUID) -> bool:
        """Delete an RPC method by its ID.

        Args:
            method_id: Unique identifier of the method to delete.

        Returns:
            True if deleted, False if not found.

        Raises:
            RepositoryError: If delete operation fails.

        """
        try:
            async with await self.get_session() as session:
                stmt = delete(RPCMethodModel).where(RPCMethodModel.id == method_id)
                result = await session.execute(stmt)
                await session.commit()

                return result.rowcount > 0
        except Exception as e:
            msg = f"Error in operation: {e}"
            raise RepositoryError(msg) from e

    async def find_all(self) -> list[RPCMethod]:
        """Find all RPC methods.

        Returns:
            List of all RPC methods.

        Raises:
            RepositoryError: If find operation fails.

        """
        try:
            async with await self.get_session() as session:
                stmt = select(RPCMethodModel)
                result = await session.execute(stmt)
                models = result.scalars().all()

                return [RPCMethod(**model.to_dict()) for model in models]
        except Exception as e:
            msg = f"Error in operation: {e}"
            raise RepositoryError(msg) from e


class PostgreSQLRPCCallRepository(BaseRepositoryMixin, Repository[RPCCall, UUID]):
    """PostgreSQL implementation of RPCCallRepository."""

    async def save(self, call: RPCCall) -> RPCCall:
        """Save an RPC call to the database.

        Args:
            call: The RPC call to save.

        Returns:
            RPCCall: The saved call.

        Raises:
            RepositoryError: If save operation fails.

        """
        try:
            async with await self.get_session() as session:
                # Check if call exists:
                existing = await session.get(RPCCallModel, call.id)

                if existing:
                    # Update existing call
                    for key, value in call.model_dump().items():
                        setattr(existing, key, value)
                    model = existing
                else:
                    # Create new call
                    model = RPCCallModel(**call.model_dump())
                    session.add(model)

                await session.commit()
                await session.refresh(model)

                # Convert back to domain entity
                return RPCCall(**model.to_dict())
        except Exception as e:
            msg = f"Error in operation: {e}"
            raise RepositoryError(msg) from e

    async def get(self, call_id: UUID) -> RPCCall | None:
        """Get RPC call by ID - Repository interface method."""
        return await self.get_by_id(call_id)

    async def get_by_id(self, call_id: UUID) -> RPCCall | None:
        """Get an RPC call by its ID.

        Args:
            call_id: Unique identifier of the call.

        Returns:
            The call or None if not found.

        """
        try:
            async with await self.get_session() as session:
                stmt = select(RPCCallModel).where(RPCCallModel.id == call_id)
                result = await session.execute(stmt)
                model = result.scalar_one_or_none()

                if model is None:
                    return None

                return RPCCall(**model.to_dict())

        except Exception as e:
            msg = f"Error in operation: {e}"
            raise RepositoryError(msg) from e

    async def get_by_method_id(
        self,
        method_id: UUID,
        limit: int = 100,
    ) -> ServiceResult[list[RPCCall]]:
        """Get RPC calls for a specific method with optional limit.

        Args:
            method_id: Unique identifier of the method.
            limit: Maximum number of calls to return.

        Returns:
            ServiceResult containing list of calls for the method.

        """
        try:
            async with await self.get_session() as session:
                stmt = (
                    select(RPCCallModel)
                    .where(RPCCallModel.method_id == method_id)
                    .limit(limit)
                    .order_by(RPCCallModel.created_at.desc())
                )
                result = await session.execute(stmt)
                models = result.scalars().all()

                calls = [RPCCall(**model.to_dict()) for model in models]
                return ServiceResult.ok(calls)

        except Exception as e:
            msg = f"Error in operation: {e}"
            raise RepositoryError(msg) from e

    async def get_active_calls(self) -> ServiceResult[list[RPCCall]]:
        """Get all currently active RPC calls.

        Returns:
            ServiceResult containing list of active calls.

        """
        try:
            async with await self.get_session() as session:
                stmt = select(RPCCallModel).where(RPCCallModel.completed_at.is_(None))
                result = await session.execute(stmt)
                models = result.scalars().all()

                calls = [RPCCall(**model.to_dict()) for model in models]
                return ServiceResult.ok(calls)

        except Exception as e:
            msg = f"Error in operation: {e}"
            raise RepositoryError(msg) from e

    async def delete(self, call_id: UUID) -> bool:
        """Delete an RPC call by its ID.

        Args:
            call_id: Unique identifier of the call to delete.

        Returns:
            True if deleted, False if not found.

        Raises:
            RepositoryError: If delete operation fails.

        """
        try:
            async with await self.get_session() as session:
                stmt = delete(RPCCallModel).where(RPCCallModel.id == call_id)
                result = await session.execute(stmt)
                await session.commit()

                return result.rowcount > 0
        except Exception as e:
            msg = f"Error in operation: {e}"
            raise RepositoryError(msg) from e

    async def find_all(self) -> list[RPCCall]:
        """Find all RPC calls.

        Returns:
            List of all RPC calls.

        Raises:
                RepositoryError: If find operation fails.

        """
        try:
            async with await self.get_session() as session:
                stmt = select(RPCCallModel)
                result = await session.execute(stmt)
                models = result.scalars().all()

                return [RPCCall(**model.to_dict()) for model in models]
        except Exception as e:
            msg = f"Error in operation: {e}"
            raise RepositoryError(msg) from e
