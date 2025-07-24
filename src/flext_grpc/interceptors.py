"""Simple gRPC Interceptors - Pure Library Components.

🚨 ARCHITECTURAL COMPLIANCE:
- Uses ONLY flext-core patterns and abstractions
- NO imports from flext-observability or external projects
- Simple interceptor components for Plugin System + DI integration
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

# 🚨 ARCHITECTURAL COMPLIANCE: Using DI container for flext-core imports
from flext_grpc.infrastructure.di_container import get_service_result

ServiceResult = get_service_result()

if TYPE_CHECKING:
    from collections.abc import Callable

    import grpc


class SimpleLogInterceptor:
    """Simple logging interceptor using only basic patterns."""

    def __init__(self) -> None:
        """Initialize simple logging interceptor."""
        self.request_count = 0

    def intercept_unary_unary(
        self,
        continuation: Callable[..., Any],
        client_call_details: grpc.ClientCallDetails,
        request: Any,
    ) -> Any:
        """Intercept unary-unary calls with simple logging."""
        self.request_count += 1

        # Simple request logging

        try:
            # Continue with the call
            return continuation(client_call_details, request)
        except Exception:
            raise


class SimpleAuthInterceptor:
    """Simple authentication interceptor using only basic patterns."""

    def __init__(self, api_key: str | None = None) -> None:
        """Initialize simple auth interceptor."""
        self.api_key = api_key

    def intercept_unary_unary(
        self,
        continuation: Callable[..., Any],
        client_call_details: grpc.ClientCallDetails,
        request: Any,
    ) -> Any:
        """Intercept unary-unary calls with simple authentication."""
        if self.api_key:
            # Add authentication metadata
            metadata = list(client_call_details.metadata or [])
            metadata.append(("authorization", f"Bearer {self.api_key}"))

            # Create new call details with auth metadata
            client_call_details = client_call_details._replace(metadata=metadata)

        return continuation(client_call_details, request)


class SimpleMetricsInterceptor:
    """Simple metrics interceptor using only basic patterns."""

    def __init__(self) -> None:
        """Initialize simple metrics interceptor."""
        self.success_count = 0
        self.error_count = 0
        self.total_requests = 0

    def intercept_unary_unary(
        self,
        continuation: Callable[..., Any],
        client_call_details: grpc.ClientCallDetails,
        request: Any,
    ) -> Any:
        """Intercept unary-unary calls with simple metrics."""
        self.total_requests += 1

        try:
            response = continuation(client_call_details, request)
            self.success_count += 1
            return response
        except Exception:
            self.error_count += 1
            raise

    def get_metrics(self) -> dict[str, int]:
        """Get simple metrics."""
        return {
            "total_requests": self.total_requests,
            "success_count": self.success_count,
            "error_count": self.error_count,
        }


class SimpleInterceptorChain:
    """Simple interceptor chain for combining interceptors."""

    def __init__(self, interceptors: list[Any] | None = None) -> None:
        """Initialize interceptor chain."""
        self.interceptors = interceptors or []

    def add_interceptor(self, interceptor: Any) -> None:
        """Add interceptor to chain."""
        self.interceptors.append(interceptor)

    def get_interceptors(self) -> list[Any]:
        """Get all interceptors in chain."""
        return self.interceptors.copy()


# Simple factory function for creating interceptor chains
def create_simple_interceptor_chain(
    enable_logging: bool = True,
    enable_auth: bool = False,
    enable_metrics: bool = True,
    api_key: str | None = None,
) -> SimpleInterceptorChain:
    """Create a simple interceptor chain with common interceptors."""
    chain = SimpleInterceptorChain()

    if enable_logging:
        chain.add_interceptor(SimpleLogInterceptor())

    if enable_auth:
        chain.add_interceptor(SimpleAuthInterceptor(api_key=api_key))

    if enable_metrics:
        chain.add_interceptor(SimpleMetricsInterceptor())

    return chain


# Export simple components
__all__ = [
    "SimpleAuthInterceptor",
    "SimpleInterceptorChain",
    "SimpleLogInterceptor",
    "SimpleMetricsInterceptor",
    "create_simple_interceptor_chain",
]
