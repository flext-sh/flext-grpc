"""REAL gRPC context management with user propagation using Python 3.13.

This module implements secure user context propagation through gRPC calls,
eliminating the security vulnerability of missing user context.
"""

from __future__ import annotations

import contextvars
from collections.abc import Awaitable
from collections.abc import Callable
from functools import wraps
from typing import TYPE_CHECKING

import grpc
from flext_auth.repositories import InMemoryRoleRepository

from flext_core.domain.pydantic_base import DomainBaseModel
from flext_core.domain.pydantic_base import Field

if TYPE_CHECKING:
    from uuid import UUID

    from flext_auth.models import User
    from flext_auth.repositories import RoleRepositoryInterface

    # Simple type alias replacement
    MetadataDict = dict[str, str]

# Python 3.13 type aliases - with strict validation
ContextValue = str | int | bool | float | None
GrpcMetadata = dict[str, str]
GrpcMethod = Callable[..., Awaitable]  # Generic simplified for Pydantic compatibility
GrpcMethodDecorator = Callable[[GrpcMethod], GrpcMethod]

# Context variables for thread-safe user propagation
current_user: contextvars.ContextVar[User | None] = contextvars.ContextVar(
    "current_user",
    default=None,
)

current_request_id: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "current_request_id",
    default=None,
)

current_trace_id: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "current_trace_id",
    default=None,
)


class GrpcRequestContext(DomainBaseModel):
    """Complete gRPC request context with user information."""

    user: User | None = Field(
        default=None,
        description="Authenticated user for this request",
    )
    request_id: str | None = Field(
        default=None,
        description="Unique request identifier for tracing",
    )
    trace_id: str | None = Field(
        default=None,
        description="Distributed trace identifier",
    )
    method: str | None = Field(default=None, description="gRPC method being called")
    peer: str | None = Field(default=None, description="Client peer address")
    metadata: MetadataDict = Field(
        default_factory=dict,
        description="Additional request metadata",
    )

    @property
    def is_authenticated(self) -> bool:
        """Check if the request context has an authenticated user.

        Returns:
            bool: True if user is authenticated, False otherwise.

        """
        return self.user is not None

    @property
    def user_id(self) -> UUID | None:
        """Get the user ID from the authenticated user.

        Returns:
            UUID | None: User ID if authenticated, None otherwise.

        """
        return self.user.user_id if self.user else None

    @property
    def username(self) -> str | None:
        """Get the username from the authenticated user.

        Returns:
            str | None: Username if authenticated, None otherwise.

        """
        return self.user.username if self.user else None

    def to_dict(self) -> MetadataDict:
        """Convert the request context to a dictionary.

        Returns:
            MetadataDict: Dictionary representation of the context.

        """
        return {
            "user_id": str(self.user_id) if self.user_id else None,
            "username": self.username,
            "request_id": self.request_id,
            "trace_id": self.trace_id,
            "method": self.method,
            "peer": self.peer,
            "is_authenticated": self.is_authenticated,
        }


class GrpcContextManager:
    """Manages gRPC context propagation and access."""

    @staticmethod
    def set_user(user: User) -> None:
        """Set the current user in the context.

        Args:
            user: The authenticated user to set in context.

        """
        current_user.set(user)

    @staticmethod
    def get_user() -> User | None:
        """Get the current user from the context.

        Returns:
            User | None: The current user if set, None otherwise.

        """
        return current_user.get()

    @staticmethod
    def set_request_id(request_id: str) -> None:
        """Set the current request ID in the context.

        Args:
            request_id: The request ID to set in context.

        """
        current_request_id.set(request_id)

    @staticmethod
    def get_request_id() -> str | None:
        """Get the current request ID from the context.

        Returns:
            str | None: The current request ID if set, None otherwise.

        """
        return current_request_id.get()

    @staticmethod
    def set_trace_id(trace_id: str) -> None:
        """Set the current trace ID in the context.

        Args:
            trace_id: The trace ID to set in context.

        """
        current_trace_id.set(trace_id)

    @staticmethod
    def get_trace_id() -> str | None:
        """Get the current trace ID from the context.

        Returns:
            str | None: The current trace ID if set, None otherwise.

        """
        return current_trace_id.get()

    @staticmethod
    def get_context() -> GrpcRequestContext:
        """Get the complete request context.

        Returns:
            GrpcRequestContext: Complete context with user, request ID, and trace ID.

        """
        return GrpcRequestContext(
            user=current_user.get(),
            request_id=current_request_id.get(),
            trace_id=current_trace_id.get(),
        )

    @staticmethod
    def clear_context() -> None:
        """Clear all context variables.

        This resets user, request ID, and trace ID to None.
        """
        current_user.set(None)
        current_request_id.set(None)
        current_trace_id.set(None)


class AuthenticatedServicer:
    def require_authentication(self) -> User:
        """Require user authentication for the current request.

        Returns:
            User: The authenticated user.

        Raises:
            grpc.RpcError: If user is not authenticated.

        """
        user = GrpcContextManager.get_user()
        if not user:
            raise grpc.RpcError(
                grpc.StatusCode.UNAUTHENTICATED,
                "Authentication required",
            )
        return user

    def get_context(self) -> GrpcRequestContext:
        """Get the complete request context.

        Returns:
            GrpcRequestContext: Complete context with user, request ID, and trace ID.

        """
        return GrpcContextManager.get_context()

    def check_permission(self, permission: str) -> bool:
        """Check if the current user has the specified permission.

        Args:
            permission: The permission string to check.

        Returns:
            bool: True if user has permission, False otherwise.

        """
        # This method is largely obsolete now that the decorator handles
        # this logic asynchronously. This is a simplified, synchronous
        # version for any legacy non-async uses.
        user = self.require_authentication()
        if permission == "special:legacy":
            return "REDACTED_LDAP_BIND_PASSWORD" in user.roles
        return False

    def require_permission(self, permission: str) -> None:
        """Require the current user to have the specified permission.

        Args:
            permission: The permission string to require.

        Raises:
            grpc.RpcError: If user does not have the required permission.

        """
        if not self.check_permission(permission):
            raise grpc.RpcError(
                grpc.StatusCode.PERMISSION_DENIED,
                f"Permission required: {permission}",
            )


def get_current_user() -> User | None:
    """Get current user from context."""
    return GrpcContextManager.get_user()


def require_current_user() -> User:
    """Get current user from context, raising error if not authenticated."""
    user = GrpcContextManager.get_user()
    if not user:
        raise grpc.RpcError(
            grpc.StatusCode.UNAUTHENTICATED,
            "Authentication required",
        )
    return user


def get_request_context() -> GrpcRequestContext:
    """Get complete request context."""
    return GrpcContextManager.get_context()


class Authenticator:
    """Decorator class for authentication and permission checks."""

    def __init__(self, permission: str | None = None) -> None:
        """Initialize the decorator with optional permission requirement."""
        self.permission = permission
        self.role_repo: RoleRepositoryInterface = InMemoryRoleRepository()

    def __call__(self, func: GrpcMethod) -> GrpcMethod:
        """Apply authentication and permission checking to a gRPC method.

        Args:
            func: The gRPC method to decorate.

        Returns:
            GrpcMethod: The decorated method with authentication and permission checks.

        """

        @wraps(func)
        async def wrapper(*args: object, **kwargs: object) -> object:
            # First argument is always the servicer instance
            servicer_instance = args[0]
            if not isinstance(servicer_instance, AuthenticatedServicer):
                msg = "This decorator must be used on methods of a class that inherits from AuthenticatedServicer."
                raise TypeError(msg)

            user = servicer_instance.require_authentication()

            if self.permission:
                # Use the repository to get full Role objects
                user_roles = await self.role_repo.find_by_names(user.roles)

                # Check permissions across all roles
                has_permission = any(
                    self.permission in role.permissions for role in user_roles
                )

                if not has_permission:
                    # If permission is not found, deny access
                    raise grpc.RpcError(
                        grpc.StatusCode.PERMISSION_DENIED,
                        f"Permission required: {self.permission}",
                    )
            # If all checks pass, proceed with the original RPC method
            return await func(*args, **kwargs)

        return wrapper


# Re-alias for backward compatibility
requires_auth = Authenticator
requires_permission = Authenticator
