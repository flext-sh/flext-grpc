# flext-grpc Development Guide
## Table of Contents

- [flext-grpc Development Guide](#flext-grpc-development-guide)
  - [Development Setup](#development-setup)
    - [Prerequisites](#prerequisites)
    - [Initial Setup](#initial-setup)
- [Clone the repository](#clone-the-repository)
- [Complete development setup](#complete-development-setup)
- [Verify setup](#verify-setup)
    - [Development Environment](#development-environment)
  - [Development Workflow](#development-workflow)
    - [Essential Commands](#essential-commands)
- [Development lifecycle](#development-lifecycle)
- [Code quality](#code-quality)
- [Testing](#testing)
- [Development utilities](#development-utilities)
    - [Quality Gates](#quality-gates)
- [MANDATORY before any commit](#mandatory-before-any-commit)
- [Individual checks](#individual-checks)
  - [Code Standards](#code-standards)
    - [FLEXT-Core Compliance](#flext-core-compliance)
- [✅ CORRECT - Railway-oriented programming](#-correct---railway-oriented-programming)
- [❌ FORBIDDEN - Exception-based error handling](#-forbidden---exception-based-error-handling)
    - [Type Annotations](#type-annotations)
- [Protocol for dependency injection](#protocol-for-dependency-injection)
- [Generic service class](#generic-service-class)
    - [Domain Patterns](#domain-patterns)
  - [Testing Standards](#testing-standards)
    - [Test Structure](#test-structure)
    - [Test Writing Guidelines](#test-writing-guidelines)
    - [Test Markers](#test-markers)
- [Run specific test categories](#run-specific-test-categories)
- [pytest -m unit              # Unit tests only](#pytest--m-unit---------------unit-tests-only)
- [pytest -m "not slow"        # Exclude slow tests](#pytest--m-not-slow---------exclude-slow-tests)
- [pytest -m "integration"     # Integration tests only](#pytest--m-integration------integration-tests-only)
  - [Architecture Guidelines](#architecture-guidelines)
    - [Layer Separation](#layer-separation)
- [Domain Layer - No dependencies on other layers](#domain-layer---no-dependencies-on-other-layers)
- [Service Layer - Depends only on Domain](#service-layer---depends-only-on-domain)
- [Infrastructure Layer - Depends on Domain + Service](#infrastructure-layer---depends-on-domain--service)
    - [Dependency Injection](#dependency-injection)
  - [Documentation Standards](#documentation-standards)
    - [Docstring Requirements](#docstring-requirements)
    - [Code Comments](#code-comments)
  - [Contributing Process](#contributing-process)
    - [Development Workflow](#development-workflow)
    - [Code Review Guidelines](#code-review-guidelines)
    - [Commit Message Standards](#commit-message-standards)
- [Feature additions](#feature-additions)
- [Bug fixes](#bug-fixes)
- [Documentation](#documentation)
- [Refactoring](#refactoring)
- [Tests](#tests)
  - [Current Development Priorities](#current-development-priorities)
    - [Critical Issues](#critical-issues)
    - [Short-term Enhancements](#short-term-enhancements)
    - [Medium-term Features](#medium-term-features)
  - [Troubleshooting Development Issues](#troubleshooting-development-issues)
    - [Common Issues](#common-issues)
- [Current blocker - protobuf version mismatch](#current-blocker---protobuf-version-mismatch)
- [Error: Detected mismatched Protobuf versions](#error-detected-mismatched-protobuf-versions)
- [Check type annotations](#check-type-annotations)
- [Common fixes:](#common-fixes)
- [- Add missing return type annotations](#--add-missing-return-type-annotations)
- [- Import proper types from typing module](#--import-proper-types-from-typing-module)
- [- Use FlextResult for all fallible operations](#--use-flextresult-for-all-fallible-operations)
- [Run specific test file](#run-specific-test-file)
- [Debug test with print statements](#debug-test-with-print-statements)
    - [Development Tools](#development-tools)
- [Auto-format code](#auto-format-code)
- [Check specific file](#check-specific-file)
- [Python debugger](#python-debugger)
- [REPL with project loaded](#repl-with-project-loaded)


**Version**: 0.9.9 RC | **Updated**: September 17, 2025

Development workflow, contributing guidelines, and standards for flext-grpc.

## Development Setup

### Prerequisites

- **Python**: 3.13+ (required for advanced type annotations)
- **Poetry**: Latest version for dependency management
- **Make**: GNU Make for development commands
- **Git**: For version control and pre-commit hooks

### Initial Setup

```bash
# Clone the repository
git clone https://github.com/flext-sh/flext/tree/main/flext-grpc
cd flext-grpc

# Complete development setup
make setup

# Verify setup
make doctor
```

### Development Environment

The `make setup` command configures:

- Virtual environment with Poetry
- Pre-commit hooks for quality gates
- Development dependencies
- IDE integration files

## Development Workflow

### Essential Commands

```bash
# Development lifecycle
make setup                  # Initial environment setup
make validate              # Complete validation pipeline
make check                 # Quick validation (lint + type)
make clean                 # Clean build artifacts

# Code quality
make lint                  # Ruff linting with comprehensive rules
make type-check            # MyPy strict type checking
make format                # Auto-format code (black + ruff)
make security              # Security scanning (bandit + pip-audit)

# Testing
make test                  # Full test suite (28 failures need fixing)
make test-unit             # Unit tests only
make test-integration      # Integration tests
make test-e2e              # End-to-end tests

# Development utilities
make shell                 # Python REPL with project loaded
make docs                  # Build documentation
make build                 # Build package for distribution
```

### Quality Gates

All contributions must pass these quality gates:

```bash
# MANDATORY before any commit
make validate

# Individual checks
make lint                  # Zero Ruff violations
make type-check            # Zero MyPy errors (strict mode)
make security              # Zero critical security issues
make test                  # All tests pass (currently 28 failing, needs bug fixes)
```

## Code Standards

### FLEXT-Core Compliance

All code must follow flext-core architectural patterns:

```python
# ✅ CORRECT - Railway-oriented programming
from flext_core import FlextBus
from flext_core import FlextConfig
from flext_core import FlextConstants
from flext_core import FlextContainer
from flext_core import FlextContext
from flext_core import FlextDecorators
from flext_core import FlextDispatcher
from flext_core import FlextExceptions
from flext_core import FlextHandlers
from flext_core import FlextLogger
from flext_core import FlextMixins
from flext_core import FlextModels
from flext_core import FlextProcessors
from flext_core import FlextProtocols
from flext_core import FlextRegistry
from flext_core import FlextResult
from flext_core import FlextRuntime
from flext_core import FlextService
from flext_core import FlextTypes
from flext_core import FlextUtilities
from flext_grpc import FlextGrpcConfig

def create_validated_config(host: str, port: int) -> FlextResult[FlextGrpcConfig]:
    """Create and validate gRPC configuration."""

    return (
        validate_host(host)
        .flat_map(lambda _: validate_port(port))
        .flat_map(lambda _: create_config(host, port))
    )

# ❌ FORBIDDEN - Exception-based error handling
def create_config_bad(host: str, port: int) -> FlextGrpcConfig:
    try:
        if not host:
            raise ValueError("Host required")
        return FlextGrpcConfig(host=host, port=port)
    except Exception:
        return None  # Loses error information
```

### Type Annotations

Complete type annotations are mandatory:

```python
from typing import Protocol, TypeVar, Generic
from flext_core import FlextBus
from flext_core import FlextConfig
from flext_core import FlextConstants
from flext_core import FlextContainer
from flext_core import FlextContext
from flext_core import FlextDecorators
from flext_core import FlextDispatcher
from flext_core import FlextExceptions
from flext_core import FlextHandlers
from flext_core import FlextLogger
from flext_core import FlextMixins
from flext_core import FlextModels
from flext_core import FlextProcessors
from flext_core import FlextProtocols
from flext_core import FlextRegistry
from flext_core import FlextResult
from flext_core import FlextRuntime
from flext_core import FlextService
from flext_core import FlextTypes
from flext_core import FlextUtilities
from flext_grpc import FlextGrpcServer

T = TypeVar('T')

# Protocol for dependency injection
class GrpcServerProtocol(Protocol):
    def start(self) -> FlextResult[FlextGrpcServer]: ...
    def stop(self) -> FlextResult[FlextGrpcServer]: ...

# Generic service class
class GrpcService(Generic[T]):
    def __init__(self, config: T) -> None:
        self._config = config

    def process(self, data: dict) -> FlextResult[FlextTypes.Dict]:
        # Implementation with proper typing
        return FlextResult.ok({"processed": data})
```

### Domain Patterns

Follow Domain-Driven Design patterns:

```python
from flext_core import FlextBus
from flext_core import FlextConfig
from flext_core import FlextConstants
from flext_core import FlextContainer
from flext_core import FlextContext
from flext_core import FlextDecorators
from flext_core import FlextDispatcher
from flext_core import FlextExceptions
from flext_core import FlextHandlers
from flext_core import FlextLogger
from flext_core import FlextMixins
from flext_core import FlextModels
from flext_core import FlextProcessors
from flext_core import FlextProtocols
from flext_core import FlextRegistry
from flext_core import FlextResult
from flext_core import FlextRuntime
from flext_core import FlextService
from flext_core import FlextTypes
from flext_core import FlextUtilities
from flext_grpc.typings import TGrpcServerState

class FlextGrpcServer(FlextModels.Entity):
    """Domain entity with business logic."""

    host: str
    port: int
    state: TGrpcServerState = "stopped"

    def start(self) -> FlextResult[FlextGrpcServer]:
        """State transition with business rules validation."""

        if self.state != "stopped":
            return FlextResult.fail(f"Cannot start from state: {self.state}")

        # State transition
        return FlextResult.ok(self.copy_with(state="starting"))

    def validate_business_rules(self) -> FlextResult[None]:
        """Domain validation rules."""

        if not self.host:
            return FlextResult.fail("Host cannot be empty")

        if self.port < 1024 or self.port > 65535:
            return FlextResult.fail(f"Invalid port: {self.port}")

        return FlextResult.ok(None)
```

## Testing Standards

### Test Structure

``` javascript
tests/
├── unit/                   # Unit tests (isolated components)
│   ├── test_entities.py    # Domain entity testing
│   ├── test_services.py    # Service layer testing
│   ├── test_config.py      # Configuration testing
│   └── test_api.py         # API function testing
├── integration/            # Integration tests (component interaction)
│   ├── test_platform.py   # Platform integration
│   └── test_ecosystem.py   # FLEXT ecosystem integration
├── e2e/                    # End-to-end tests (complete workflows)
│   ├── test_grpc.py        # Complete gRPC workflows
│   └── test_streaming.py   # Streaming operations
└── conftest.py             # Shared fixtures and utilities
```

### Test Writing Guidelines

```python
import pytest
from flext_core import FlextBus
from flext_core import FlextConfig
from flext_core import FlextConstants
from flext_core import FlextContainer
from flext_core import FlextContext
from flext_core import FlextDecorators
from flext_core import FlextDispatcher
from flext_core import FlextExceptions
from flext_core import FlextHandlers
from flext_core import FlextLogger
from flext_core import FlextMixins
from flext_core import FlextModels
from flext_core import FlextProcessors
from flext_core import FlextProtocols
from flext_core import FlextRegistry
from flext_core import FlextResult
from flext_core import FlextRuntime
from flext_core import FlextService
from flext_core import FlextTypes
from flext_core import FlextUtilities
from flext_grpc import FlextGrpcConfig, create_server

class TestGrpcServer:
    """Test gRPC server functionality."""

    def test_server_creation_success(self):
        """Test successful server creation."""

        # Arrange
        config = FlextGrpcConfig(host="localhost", port=50051)

        # Act
        result = create_server(config)

        # Assert
        assert result.success
        server = result.unwrap()
        assert server.host == "localhost"
        assert server.port == 50051

    def test_server_creation_invalid_config(self):
        """Test server creation with invalid configuration."""

        # Arrange
        config = FlextGrpcConfig(host="", port=-1)  # Invalid

        # Act
        result = create_server(config)

        # Assert
        assert result.is_failure
        assert "Invalid configuration" in result.error

    @pytest.mark.parametrize("host,port,expected_error", [
        ("", 50051, "Host cannot be empty"),
        ("localhost", -1, "Invalid port"),
        ("localhost", 99999, "Invalid port"),
    ])
    def test_validation_errors(self, host, port, expected_error):
        """Test configuration validation errors."""

        config = FlextGrpcConfig(host=host, port=port)
        validation = config.validate()

        assert validation.is_failure
        assert expected_error in validation.error
```

### Test Markers

Use pytest markers for test categorization:

```python
import pytest

@pytest.mark.unit
def test_entity_creation():
    """Unit test for entity creation."""
    pass

@pytest.mark.integration
def test_service_integration():
    """Integration test for services."""
    pass

@pytest.mark.e2e
def test_complete_workflow():
    """End-to-end workflow test."""
    pass

@pytest.mark.slow
def test_performance_benchmark():
    """Slow performance test."""
    pass

# Run specific test categories
# pytest -m unit              # Unit tests only
# pytest -m "not slow"        # Exclude slow tests
# pytest -m "integration"     # Integration tests only
```

## Architecture Guidelines

### Layer Separation

Maintain strict layer boundaries:

```python
# Domain Layer - No dependencies on other layers
class FlextGrpcServer(FlextModels.Entity):
    # Pure business logic, no infrastructure concerns
    pass

# Service Layer - Depends only on Domain
class FlextGrpcServerService:
    def __init__(self, server: FlextGrpcServer):
        self._server = server  # Domain dependency only

# Infrastructure Layer - Depends on Domain + Service
from flext_grpc.entities import FlextGrpcServer
from flext_grpc.services import FlextGrpcServerService

def create_server(config: FlextGrpcConfig) -> FlextResult[FlextGrpcServer]:
    # Infrastructure function using domain and service layers
    pass
```

### Dependency Injection

Use FlextContainer for all dependencies:

```python
from flext_core import FlextBus
from flext_core import FlextConfig
from flext_core import FlextConstants
from flext_core import FlextContainer
from flext_core import FlextContext
from flext_core import FlextDecorators
from flext_core import FlextDispatcher
from flext_core import FlextExceptions
from flext_core import FlextHandlers
from flext_core import FlextLogger
from flext_core import FlextMixins
from flext_core import FlextModels
from flext_core import FlextProcessors
from flext_core import FlextProtocols
from flext_core import FlextRegistry
from flext_core import FlextResult
from flext_core import FlextRuntime
from flext_core import FlextService
from flext_core import FlextTypes
from flext_core import FlextUtilities
from flext_grpc import FlextGrpcPlatform

class GrpcServiceManager:
    """Service manager using dependency injection."""

    def __init__(self) -> None:
        self._container = FlextContainer.get_global()
        self.logger = FlextLogger(__name__)

    def initialize(self) -> FlextResult[None]:
        """Initialize with dependency injection."""

        # Register services
        platform = FlextGrpcPlatform()
        self._container.register("grpc_platform", platform)

        return FlextResult.ok(None)

    def get_platform(self) -> FlextResult[FlextGrpcPlatform]:
        """Retrieve platform from container."""

        platform_result = self._container.get("grpc_platform")
        if platform_result.success:
            return FlextResult.ok(platform_result.unwrap())

        return FlextResult.fail("Platform not initialized")
```

## Documentation Standards

### Docstring Requirements

All public APIs require comprehensive docstrings:

```python
from flext_core import FlextBus
from flext_core import FlextConfig
from flext_core import FlextConstants
from flext_core import FlextContainer
from flext_core import FlextContext
from flext_core import FlextDecorators
from flext_core import FlextDispatcher
from flext_core import FlextExceptions
from flext_core import FlextHandlers
from flext_core import FlextLogger
from flext_core import FlextMixins
from flext_core import FlextModels
from flext_core import FlextProcessors
from flext_core import FlextProtocols
from flext_core import FlextRegistry
from flext_core import FlextResult
from flext_core import FlextRuntime
from flext_core import FlextService
from flext_core import FlextTypes
from flext_core import FlextUtilities
from flext_grpc import FlextGrpcConfig, FlextGrpcServer

def create_server(config: FlextGrpcConfig) -> FlextResult[FlextGrpcServer]:
    """Create a gRPC server with the specified configuration.

    Creates and validates a gRPC server instance using Clean Architecture
    patterns with comprehensive error handling through FlextResult.

    Args:
        config: gRPC server configuration with validation rules

    Returns:
        FlextResult[FlextGrpcServer]: Success with server instance, or
            failure with detailed error message

    Example:
        >>> config = FlextGrpcConfig(host="localhost", port=50051)
        >>> result = create_server(config)
        >>> if result.success:
        ...     server = result.unwrap()
        ...     print(f"Server: {server.host}:{server.port}")

    Integration:
        Integrates with FlextContainer for dependency injection and
        follows FLEXT ecosystem patterns for consistency.

    Raises:
        No exceptions - all errors returned via FlextResult pattern.
    """
    # Implementation
    pass
```

### Code Comments

Use comments sparingly for complex business logic:

```python
def validate_server_state(self, new_state: TGrpcServerState) -> FlextResult[None]:
    """Validate server state transition."""

    # State machine validation - only specific transitions allowed
    valid_transitions = {
        "stopped": ["starting"],
        "starting": ["running", "stopped"],  # Can fail to start
        "running": ["stopping"],
        "stopping": ["stopped"]
    }

    if new_state not in valid_transitions.get(self.state, []):
        return FlextResult.fail(
            f"Invalid state transition: {self.state} → {new_state}"
        )

    return FlextResult.ok(None)
```

## Contributing Process

### Development Workflow

1. **Issue Creation**
   - Create GitHub issue describing the problem/feature
   - Use appropriate labels (bug, feature, documentation)
   - Reference related issues or PRs

2. **Branch Creation**

   ```bash
   git checkout -b feature/add-health-checking
   git checkout -b fix/protobuf-version-conflict
   git checkout -b docs/update-api-reference
   ```

3. **Development**

   ```bash
   # Make changes following standards
   make validate          # Run quality gates
   make test             # Run tests (when available)
   git add .
   git commit -m "Add health checking implementation"
   ```

4. **Pull Request**
   - Create PR with descriptive title and body
   - Link to related issues
   - Ensure all CI checks pass
   - Request code review

### Code Review Guidelines

**For Authors:**

- Ensure all quality gates pass before requesting review
- Provide clear PR description with context
- Include working code examples in comments
- Update documentation for API changes

**For Reviewers:**

- Check FLEXT-core pattern compliance
- Verify comprehensive type annotations
- Ensure tests cover new functionality
- Validate documentation accuracy

### Commit Message Standards

Use conventional commit format:

```bash
# Feature additions
git commit -m "feat: add health checking service implementation"

# Bug fixes
git commit -m "fix: resolve protobuf version compatibility issue"

# Documentation
git commit -m "docs: update API reference for new methods"

# Refactoring
git commit -m "refactor: simplify server state machine logic"

# Tests
git commit -m "test: add comprehensive streaming operation tests"
```

## Current Development Priorities

### Critical Issues

1. **Fix Protobuf Version Conflict**
   - Regenerate protobuf files to match runtime version
   - Update CI/CD to prevent version mismatches
   - Enable test suite execution

2. **Test Suite Validation**
   - Execute available test functions
   - Verify actual functionality coverage
   - Fix any failing tests

### Short-term Enhancements

1. **Health Checking Implementation**
   - Implement grpc.health.v1.Health service
   - Add health monitoring endpoints
   - Integration with flext-observability

2. **Interceptor Framework**
   - Authentication interceptors
   - Logging interceptors
   - Metrics collection interceptors

### Medium-term Features

1. **OpenTelemetry Integration**
   - Distributed tracing
   - Metrics export
   - Request correlation

2. **Production Features**
   - Service discovery
   - Load balancing
   - Circuit breaker patterns

## Troubleshooting Development Issues

### Common Issues

**Import Errors**

```bash
# Current blocker - protobuf version mismatch
python -c "from flext_grpc import FlextGrpcConfig"
# Error: Detected mismatched Protobuf versions
```

**Type Checking Issues**

```bash
# Check type annotations
make type-check

# Common fixes:
# - Add missing return type annotations
# - Import proper types from typing module
# - Use FlextResult for all fallible operations
```

**Test Failures**

```bash
# Run specific test file
pytest tests/unit/test_config.py -v

# Debug test with print statements
pytest tests/unit/test_config.py::test_validation -s
```

### Development Tools

**Code Quality**

```bash
# Auto-format code
make format

# Check specific file
ruff check src/flext_grpc/config.py
mypy src/flext_grpc/config.py --strict
```

**Debugging**

```bash
# Python debugger
import pdb; pdb.set_trace()

# REPL with project loaded
make shell
>>> from flext_grpc import FlextGrpcConfig
>>> config = FlextGrpcConfig()
```

---

This development guide provides comprehensive standards and workflows for contributing to flext-grpc while maintaining high quality and FLEXT ecosystem integration.
