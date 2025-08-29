# flext-grpc

**Type**: Infrastructure Library | **Status**: Active Development | **Dependencies**: flext-core

gRPC communication library for the FLEXT ecosystem with Clean Architecture patterns.

> ⚠️ Development Status: Core domain entities working; Protocol Buffer integration incomplete; ~76% test coverage.

## Quick Start

```bash
# Install dependencies
poetry install

# Test basic functionality
python -c "from flext_grpc import FlextGrpcPlatform; platform = FlextGrpcPlatform(); print('✅ Working')"

# Run development setup
make setup
```

## Current Reality

**What Actually Works:**

- Domain entities (Server, Client, Channel, Service, Stream) with state management
- Service layer with business logic following DDD patterns
- FlextResult pattern integration for error handling
- Configuration management with Pydantic

**What Needs Work:**

- Protocol Buffer implementation for Go/Python interoperability
- Service discovery integration (currently manual host/port)
- Test coverage improvement (76% → 90% target)
- Cross-language testing with Go services

## Architecture Role in FLEXT Ecosystem

### **Infrastructure Component**

FLEXT gRPC provides communication layer between distributed services:

```
┌─────────────────────────────────────────────────────────────────┐
│                    FLEXT ECOSYSTEM (32 Projects)                 │
├─────────────────────────────────────────────────────────────────┤
│ Services: FlexCore(Go) | FLEXT Service(Go/Python) | Clients     │
├─────────────────────────────────────────────────────────────────┤
│ Applications: API | Auth | Web | CLI | Quality | Observability  │
├═════════════════════════════════════════════════════════════════┤
│ Infrastructure: Oracle | LDAP | LDIF | [FLEXT-GRPC] | WMS      │
├─────────────────────────────────────────────────────────────────┤
│ Singer Ecosystem: Taps(5) | Targets(5) | DBT(4) | Extensions(1) │
├─────────────────────────────────────────────────────────────────┤
│ Foundation: FLEXT-CORE (FlextResult | DI | Domain Patterns)     │
└─────────────────────────────────────────────────────────────────┘
```

### **Core Responsibilities**

1. **Service Communication**: gRPC client/server management for FlexCore ↔ FLEXT Service
2. **Protocol Buffers**: Shared definitions for type-safe Go/Python communication
3. **Clean Architecture**: Domain entities with state management and validation

## Key Features

### **Current Capabilities**

- **Domain Entities**: gRPC Server, Client, Channel, Service, Stream with state management
- **Clean Architecture**: Domain/service/platform layer separation
- **FlextResult Pattern**: Type-safe error handling throughout
- **Configuration Management**: Environment-aware gRPC settings

### **FLEXT Core Integration**

- **FlextResult Pattern**: Railway-oriented programming for error handling
- **FlextModels.Entity**: Domain entities with validation and state transitions
- **Dependency Injection**: Global container integration (via flext-core)

## Installation & Usage

### Installation

```bash
# Clone and install
cd /path/to/flext-grpc
poetry install

# Development setup
make setup
```

### Basic Usage

```python
from flext_grpc import FlextGrpcPlatform, FlextGrpcServer
from datetime import datetime, timezone

# Create server entity
server = FlextGrpcServer(
    id="main-server",
    host="localhost",
    port=50051,
    max_workers=10,
    created_at=datetime.now(timezone.utc)
)

# Validate domain rules
validation = server.validate_domain_rules()
if validation.is_failure:
    print(f"Configuration error: {validation.error}")
    exit(1)

# Use platform for operations
platform = FlextGrpcPlatform()
result = platform.service.execute("create_server", server)
if result.success:
    print(f"Server created: {result.data.state}")
else:
    print(f"Error: {result.error}")
```

## Architecture

### Clean Architecture + DDD Structure

```
src/flext_grpc/
├── entities.py           # Domain entities (Server, Client, Channel, Service, Stream)
├── services.py           # Domain services (business logic)
├── platform.py           # Application service (unified facade)
├── config.py             # Configuration management
├── types.py              # Type definitions and validation
├── errors.py             # Domain-specific errors
├── constants.py          # Domain constants
└── api.py                # Public API functions
```

### Key Architectural Patterns

- **Entity Pattern**: Immutable domain entities with `copy_with()` methods
- **Service Pattern**: Domain services for business operations
- **Result Pattern**: `FlextResult` for error handling without exceptions
- **Dependency Injection**: Global container integration via flext-core
- **State Machines**: Clear state transitions for all gRPC entities

### Domain Entities

#### FlextGrpcServer

Server lifecycle management with states: `stopped` → `starting` → `running` → `stopping`

#### FlextGrpcClient

Client connection management with host, port, and SSL configuration

#### FlextGrpcChannel

gRPC channel abstraction with connection state tracking

#### FlextGrpcService

Service definition with method registration and metadata

#### FlextGrpcStream

Streaming operations support (unary, server streaming, client streaming, bidirectional)

## Development

### Development Setup

```bash
# Complete development environment
make setup                    # Install dependencies + pre-commit hooks

# Quality gates (must pass before commits)
make validate                 # Complete validation pipeline
make check                    # Quick health check
make test                     # Run tests with coverage
```

### Quality Standards

- **Test Coverage**: Minimum 90% (currently 86% - [improvement needed](docs/TODO.md))
- **Type Safety**: Strict MyPy validation (currently failing - [fixes needed](docs/TODO.md))
- **Code Quality**: Ruff linting with ALL rules enabled
- **Security**: Bandit + pip-audit scanning

### Testing

```bash
# Test categories
make test-unit                # Unit tests (isolated components)
make test-integration         # Integration tests (component interaction)
make test-grpc                # gRPC-specific functionality
make test-fast                # Quick feedback without coverage

# Coverage analysis
make coverage-html            # Generate HTML coverage report
```

## Quality Standards

### **Quality Targets**

- **Coverage**: 90% target (currently ~76%)
- **Type Safety**: MyPy strict mode adoption in progress
- **Linting**: Ruff with comprehensive rules (continuous improvement)
- **Security**: Bandit + pip-audit scanning

## Integration with FLEXT Ecosystem

### **FLEXT Core Patterns**

```python
# FlextResult for all operations
def create_server(config) -> FlextResult[FlextGrpcServer]:
    try:
        server = FlextGrpcServer(**config)
        validation = server.validate_domain_rules()
        if validation.is_failure:
            return FlextResult[None].fail(validation.error)
        return FlextResult[None].ok(server)
    except Exception as e:
        return FlextResult[None].fail(f"Server creation failed: {e}")
```

### **Service Integration**

- **FlexCore (Go)**: Runtime service gRPC communication (port 8080)
- **FLEXT Service**: Data platform gRPC integration (port 8081)
- **Cross-language**: Protocol Buffer definitions for Go/Python interop

## Current Status

**Version**: 0.9.0 (Development)

**Completed**:

- ✅ Domain entities with state management
- ✅ Clean Architecture implementation
- ✅ FlextResult error handling

**In Progress**:

- 🔄 Protocol Buffer integration
- 🔄 Test coverage improvement (76% → 90%)
- 🔄 Service discovery

**Planned**:

- 📋 Go service integration
- 📋 Performance benchmarking
- 📋 Advanced streaming features

## Contributing

### Development Standards

- **FLEXT Core Integration**: Use established patterns
- **Type Safety**: All code must pass MyPy
- **Testing**: Maintain coverage and ensure tests pass
- **Code Quality**: Follow linting rules

### Development Workflow

```bash
# Setup and validate
make setup
make validate
make test
```

## License

MIT License - See [LICENSE](LICENSE) file for details.

## Links

- **[flext-core](../flext-core)**: Foundation library
- **[CLAUDE.md](CLAUDE.md)**: Development guidance
- **[Documentation](docs/)**: Complete documentation

---
