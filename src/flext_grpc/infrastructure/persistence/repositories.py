"""Repository implementations for FLEXT-GRPC.

Using flext-core patterns - NO duplication.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import delete
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from flext_core.domain.pydantic_base import ServiceResult
from flext_grpc.domain.entities import GRPCService
from flext_grpc.domain.entities import RPCCall
from flext_grpc.domain.entities import RPCMethod
from flext_grpc.domain.ports import GRPCServiceRepository
from flext_grpc.domain.ports import RPCCallRepository
from flext_grpc.domain.ports import RPCMethodRepository
from flext_grpc.infrastructure.persistence.models import GRPCServiceModel
from flext_grpc.infrastructure.persistence.models import RPCCallModel
from flext_grpc.infrastructure.persistence.models import RPCMethodModel

if TYPE_CHECKING:
    from uuid import UUID


class BaseRepository:
    """Base repository with common functionality."""

    def __init__(self, database_url: str) -> None:
        """Initialize repository with database URL.

        Args:
            database_url: Database connection URL

        """
        self.engine = create_async_engine(database_url)
        self.session_factory = sessionmaker(
            self.engine,
            class_=AsyncSession,
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


class PostgreSQLGRPCServiceRepository(BaseRepository, GRPCServiceRepository):
    """PostgreSQL implementation of GRPCServiceRepository."""

    async def save(self, service: GRPCService) -> ServiceResult[GRPCService]:
        """Save a gRPC service to the database.

        Args:
            service: The gRPC service to save.

        Returns:
            ServiceResult[GRPCService]: Result containing the saved service.

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
                domain_service = GRPCService(**model.to_dict())
                return ServiceResult.ok(domain_service)

        except Exception as e:
            return ServiceResult.fail(f"Failed to save service: {e!s}")

    async def get_by_id(self, service_id: UUID) -> ServiceResult[GRPCService | None]:
        """Get a gRPC service by its ID.

        Args:
            service_id: Unique identifier of the service.

        Returns:
            ServiceResult containing the service or None if not found.

        """
        try:
            async with await self.get_session() as session:
                stmt = select(GRPCServiceModel).where(GRPCServiceModel.id == service_id)
                result = await session.execute(stmt)
                model = result.scalar_one_or_none()

                if model is None:
                    return ServiceResult.ok(None)

                domain_service = GRPCService(**model.to_dict())
                return ServiceResult.ok(domain_service)

        except Exception as e:
            return ServiceResult.fail(f"Failed to get service: {e!s}")

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

    async def delete(self, service_id: UUID) -> ServiceResult[bool]:
        """Delete a gRPC service by its ID.

        Args:
            service_id: Unique identifier of the service to delete.

        Returns:
            ServiceResult containing True if deleted, False if not found.

        """
        try:
            async with await self.get_session() as session:
                stmt = delete(GRPCServiceModel).where(GRPCServiceModel.id == service_id)
                result = await session.execute(stmt)
                await session.commit()

                return ServiceResult.ok(result.rowcount > 0)

        except Exception as e:
            return ServiceResult.fail(f"Failed to delete service: {e!s}")


class PostgreSQLRPCMethodRepository(BaseRepository, RPCMethodRepository):
    """PostgreSQL implementation of RPCMethodRepository."""

    async def save(self, method: RPCMethod) -> ServiceResult[RPCMethod]:
        """Save an RPC method to the database.

        Args:
            method: The RPC method to save.

        Returns:
            ServiceResult containing the saved method.

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
                domain_method = RPCMethod(**model.to_dict())
                return ServiceResult.ok(domain_method)

        except Exception as e:
            return ServiceResult.fail(f"Failed to save method: {e!s}")

    async def get_by_id(self, method_id: UUID) -> ServiceResult[RPCMethod | None]:
        """Get an RPC method by its ID.

        Args:
            method_id: Unique identifier of the method.

        Returns:
            ServiceResult containing the method or None if not found.

        """
        try:
            async with await self.get_session() as session:
                stmt = select(RPCMethodModel).where(RPCMethodModel.id == method_id)
                result = await session.execute(stmt)
                model = result.scalar_one_or_none()

                if model is None:
                    return ServiceResult.ok(None)

                domain_method = RPCMethod(**model.to_dict())
                return ServiceResult.ok(domain_method)

        except Exception as e:
            return ServiceResult.fail(f"Failed to get method: {e!s}")

    async def get_by_service_id(
        self, service_id: UUID,
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
        self, service_id: UUID, name: str,
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

    async def delete(self, method_id: UUID) -> ServiceResult[bool]:
        """Delete an RPC method by its ID.

        Args:
            method_id: Unique identifier of the method to delete.

        Returns:
            ServiceResult containing True if deleted, False if not found.

        """
        try:
            async with await self.get_session() as session:
                stmt = delete(RPCMethodModel).where(RPCMethodModel.id == method_id)
                result = await session.execute(stmt)
                await session.commit()

                return ServiceResult.ok(result.rowcount > 0)

        except Exception as e:
            return ServiceResult.fail(f"Failed to delete method: {e!s}")


class PostgreSQLRPCCallRepository(BaseRepository, RPCCallRepository):
    """PostgreSQL implementation of RPCCallRepository."""

    async def save(self, call: RPCCall) -> ServiceResult[RPCCall]:
        """Save an RPC call to the database.

        Args:
            call: The RPC call to save.

        Returns:
            ServiceResult containing the saved call.

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
                domain_call = RPCCall(**model.to_dict())
                return ServiceResult.ok(domain_call)

        except Exception as e:
            return ServiceResult.fail(f"Failed to save call: {e!s}")

    async def get_by_id(self, call_id: UUID) -> ServiceResult[RPCCall | None]:
        """Get an RPC call by its ID.

        Args:
            call_id: Unique identifier of the call.

        Returns:
            ServiceResult containing the call or None if not found.

        """
        try:
            async with await self.get_session() as session:
                stmt = select(RPCCallModel).where(RPCCallModel.id == call_id)
                result = await session.execute(stmt)
                model = result.scalar_one_or_none()

                if model is None:
                    return ServiceResult.ok(None)

                domain_call = RPCCall(**model.to_dict())
                return ServiceResult.ok(domain_call)

        except Exception as e:
            return ServiceResult.fail(f"Failed to get call: {e!s}")

    async def get_by_method_id(
        self, method_id: UUID, limit: int = 100,
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
            return ServiceResult.fail(f"Failed to get calls by method: {e!s}")

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
            return ServiceResult.fail(f"Failed to get active calls: {e!s}")

    async def delete(self, call_id: UUID) -> ServiceResult[bool]:
        """Delete an RPC call by its ID.

        Args:
            call_id: Unique identifier of the call to delete.

        Returns:
            ServiceResult containing True if deleted, False if not found.

        """
        try:
            async with await self.get_session() as session:
                stmt = delete(RPCCallModel).where(RPCCallModel.id == call_id)
                result = await session.execute(stmt)
                await session.commit()

                return ServiceResult.ok(result.rowcount > 0)

        except Exception as e:
            return ServiceResult.fail(f"Failed to delete call: {e!s}")
