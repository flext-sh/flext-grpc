# FLEXT gRPC Source Code

<!-- TOC START -->

- [Module Structure](#module-structure)
  - [Core Implementation](#core-implementation)
- [Architecture Layers](#architecture-layers)
  - [Domain Layer (Core Business Logic)](#domain-layer-core-business-logic)
  - [Application Layer (Business Process Orchestration)](#application-layer-business-process-orchestration)
  - [Infrastructure Layer (External System Integration)](#infrastructure-layer-external-system-integration)
- [Code Organization Principles](#code-organization-principles)
  - [Clean Architecture Compliance](#clean-architecture-compliance)
  - [Domain-Driven Design Patterns](#domain-driven-design-patterns)
  - [Enterprise Patterns](#enterprise-patterns)
- [Implementation Standards](#implementation-standards)
  - [Code Quality Standards](#code-quality-standards)
  - [Testing Integration](#testing-integration)
- [Integration Points](#integration-points)
  - [FLEXT Ecosystem Integration](#flext-ecosystem-integration)
  - [External Dependencies](#external-dependencies)
- [Development Workflow](#development-workflow)
  - [Code Modification Guidelines](#code-modification-guidelines)
  - [Quality Gates](#quality-gates)
  - [File Organization](#file-organization)
- [Current Status](#current-status)
  - [Implementation Completeness](#implementation-completeness)
- [Contributing](#contributing)
  - [Code Contribution Guidelines](#code-contribution-guidelines)
  - [Review Checklist](#review-checklist)

<!-- TOC END -->

Source code implementation for the FLEXT gRPC communication platform following Clean Architecture and Domain-Driven Design principles.

## Module Structure

### Core Implementation

```
src/flext_grpc/
├── __init__.py              # Public API and module exports
├── entities.py              # Domain entities (Server, Client, Channel, Service, Stream)
├── services.py              # Domain services (business logic layer)
├── platform.py              # Application service (unified facade)
├── api.py                   # Public API functions and utilities
├── config.py                # Configuration management and validation
├── types.py
├── errors.py                # Domain-specific error classes
└── constants.py             # Domain constants and enumerations
```

## Architecture Layers

### Domain Layer (Core Business Logic)

**Files**: `entities.py`, `types.py`, `constants.py`\
**Purpose**: Core business entities and domain logic\
**Dependencies**: None (pure domain logic)

**Key Components**:

- **FlextGrpcServer**: Server lifecycle and state management
- **FlextGrpcClient**: Client connection management with SSL support
- **FlextGrpcChannel**: gRPC channel abstraction and state tracking
- **FlextGrpcService**: Service definition and method registration
- **FlextGrpcStream**: Streaming operations for all gRPC stream types

### Application Layer (Business Process Orchestration)

**Files**: `services.py`, `platform.py`\
**Purpose**: Business process orchestration and use case implementation\
**Dependencies**: Domain layer only

**Key Components**:

- **FlextGrpcServerService**: Server operation orchestration
- **FlextGrpcClientService**: Client operation orchestration
- **FlextGrpcStreamService**: Stream operation orchestration
- **FlextGrpcPlatform**: Unified facade for high-level operations

### Infrastructure Layer (External System Integration)

**Files**: `api.py`, `config.py`, `errors.py`\
**Purpose**: External system integration and technical concerns\
**Dependencies**: Application and domain layers

**Key Components**:

- **FlextGrpcSettings**: Configuration management with Pydantic validation
- **API Functions**: Factory functions and utility operations
- **Error Classes**: Domain-specific exception hierarchy
- **Type Validators**: Input validation and type checking

## Code Organization Principles

### Clean Architecture Compliance

**Dependency Direction**: External layers depend on inner layers, never the reverse

- Infrastructure → Application → Domain
- No circular dependencies between layers
- Domain layer is completely independent

**Separation of Concerns**: Each layer has distinct responsibilities

- Domain: Business logic and entities
- Application: Use case orchestration
- Infrastructure: External system integration

### Domain-Driven Design Patterns

**Rich Domain Model**: Entities contain business behavior, not just data

- Domain validation through `validate_domain_rules()`
- State transitions with business rule enforcement
- Immutable entities with `copy_with()` methods

**Ubiquitous Language**: Consistent terminology throughout codebase

- gRPC domain concepts clearly expressed in code
- Business terminology used consistently
- Clear naming conventions for all components

### Enterprise Patterns

**Result Pattern**: Railway-oriented programming for error handling

- All operations return `FlextResult<T>` for explicit error handling
- No exceptions for business logic failures
- Composable operations with map/flat_map support

**Entity Pattern**: Immutable domain entities with rich behavior

- Entities implement business logic methods
- State changes through immutable operations
- Comprehensive domain validation

**Service Pattern**: Domain services for complex business operations

- Stateless services implementing business workflows
- Clear separation between entity and service responsibilities
- Dependency injection for external service access

## Implementation Standards

### Code Quality Standards

**Type Safety**: MyPy strict mode adoption; aiming for full coverage

- All parameters and return types explicitly typed
- Union types for optional parameters
- Generic types for container operations

**Documentation**: Enterprise-grade docstrings following FLEXT standards

- Module-level comprehensive documentation
- Class and method documentation with examples
- Integration notes and architectural positioning

**Error Handling**: Comprehensive error handling with FlextResult pattern

- No uncaught exceptions in business logic
- Clear error messages with actionable information
- Error propagation through result chains

### Testing Integration

**Testability**: Code designed for comprehensive testing

- Dependency injection for external dependencies
- Pure functions for core business logic
- Clear separation of concerns for isolated testing

**Coverage**: Target 90% code coverage with quality tests

- Unit tests for all business logic
- Integration tests for component interaction
- E2E tests for complete workflows

## Integration Points

### FLEXT Ecosystem Integration

**flext-core Foundation**: Built on established FLEXT patterns

- FlextModels.Entity base class for all domain entities
- FlextResult for consistent error handling
- Global dependency injection container

**flext-observability**: Monitoring and observability integration

- Health check endpoints for all services
- Performance metrics for gRPC operations
- Distributed tracing for cross-service calls

### External Dependencies

**gRPC Framework**: Core gRPC functionality

- grpcio for Python gRPC implementation
- grpcio-tools for protocol buffer compilation
- protobuf for message serialization

**Configuration Management**: Type-safe configuration

- Pydantic for configuration validation
- Environment variable support
- Development vs production configuration

## Development Workflow

### Code Modification Guidelines

1. **Domain Changes**: Start with domain entities and validation
1. **Service Implementation**: Add business logic in service classes
1. **Platform Integration**: Expose operations through platform facade
1. **API Updates**: Update public API functions as needed
1. **Documentation**: Update docstrings and examples

### Quality Gates

**Before Committing**:

```bash
make validate    # Complete validation pipeline
make check       # Quick health check
make test        # Run tests with coverage
```

**Code Standards**:

- Ruff linting with ALL rules enabled (zero tolerance)
- MyPy strict type checking (zero errors)
- 90% test coverage minimum
- Comprehensive docstrings

### File Organization

**Import Order**: Consistent import organization

1. Standard library imports
1. Third-party imports
1. flext-core imports
1. Local module imports

**Code Structure**: Consistent within-file organization

1. Module docstring
1. Imports
1. Type definitions
1. Constants
1. Classes and functions
1. Module-level code

## Current Status

### Implementation Completeness

**Completed**:

- ✅ Domain entity implementation with validation
- ✅ Service layer with business logic
- ✅ Platform facade for unified operations
- ✅ Configuration management
- ✅ Type definitions and validation
- ✅ Error handling framework

**In Progress**:

- 🚧 Protocol Buffer implementation
- 🚧 Cross-language integration patterns
- 🚧 Performance optimization

**Planned**:

- ⏳ Advanced streaming capabilities
- ⏳ Security features (TLS/mTLS)
- ⏳ Service discovery integration

For detailed status and development priorities, see [../docs/TODO.md](../docs/TODO.md).

## Contributing

### Code Contribution Guidelines

1. **Follow Architecture**: Respect Clean Architecture and DDD principles
1. **Maintain Quality**: All quality gates must pass
1. **Write Tests**: Minimum 90% coverage for new code
1. **Document Thoroughly**: Enterprise-grade documentation required
1. **Use Patterns**: Follow established FLEXT patterns

### Review Checklist

- [ ] Code follows Clean Architecture principles
- [ ] Domain validation implemented for entities
- [ ] FlextResult pattern used for error handling
- [ ] Comprehensive docstrings with examples
- [ ] Type annotations for all parameters/returns
- [ ] Unit tests with 90%+ coverage
- [ ] Integration with existing patterns
- [ ] No circular dependencies introduced

For detailed development guidance, see [../AGENTS.md](../AGENTS.md).
