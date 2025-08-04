# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FLEXT gRPC is a high-performance gRPC communication platform built with Python 3.13, following Clean Architecture and Domain-Driven Design (DDD) principles. The library provides a comprehensive solution for gRPC client/server management with enterprise-grade features including streaming, configuration management, and robust error handling.

## Architecture

### Core Patterns

- **Clean Architecture**: Clear separation between domain entities, services, and infrastructure
- **Domain-Driven Design (DDD)**: Rich domain entities with business logic and validation
- **Result Pattern**: Using `FlextResult` for robust error handling throughout the codebase
- **Entity Pattern**: Immutable entities with `copy_with()` methods for state transitions
- **Dependency Injection**: Global container management via `flext-core`

### Key Components

#### Domain Entities (`src/flext_grpc/entities.py`)

- **FlextGrpcServer**: Server lifecycle management with state transitions (stopped → starting → running → stopping)
- **FlextGrpcClient**: Client connection management with channel state tracking
- **FlextGrpcChannel**: gRPC channel with connection states (idle → connecting → ready → shutdown)
- **FlextGrpcService**: Service definition with method management
- **FlextGrpcStream**: Streaming operations support (unary, server_streaming, client_streaming, bidirectional)

#### Domain Services (`src/flext_grpc/services.py`)

- **FlextGrpcServerService**: Server operations (start, stop, add_service, status)
- **FlextGrpcClientService**: Client operations (connect, disconnect, call, status)
- **FlextGrpcStreamService**: Stream operations (create, send, close)

#### Platform Layer (`src/flext_grpc/platform.py`)

- **FlextGrpcPlatform**: Unified facade providing high-level gRPC operations
- Integrates with global container for service management
- Convenience methods for common operations

#### Configuration (`src/flext_grpc/config.py`)

- **FlextGrpcConfig**: Settings management using `FlextBaseSettings`
- Validation for host, port, workers, and timeout
- Environment variable support

## Development Commands

### Essential Commands

```bash
# Development setup
make setup                    # Complete development environment setup
make install                  # Install dependencies with Poetry
make install-dev              # Install with development extras

# Quality Gates (run before committing)
make validate                # Complete validation (lint + type + security + test) - MUST PASS
make check                   # Essential checks (lint + type + test)
make lint                    # Ruff linting with ALL rules enabled
make type-check              # MyPy strict type checking (zero errors tolerated)
make security                # Security scans (bandit + pip-audit)

# Testing
make test                    # Run tests with 90% coverage minimum
make test-unit               # Unit tests only
make test-integration        # Integration tests only
make test-grpc               # gRPC-specific tests
make test-fast               # Run tests without coverage for quick feedback
make coverage-html           # Generate HTML coverage report

# Code Formatting
make format                  # Format code with ruff
make format-check            # Check formatting without fixing
make fix                     # Auto-fix all issues
```

### Protocol Buffers

```bash
make proto-gen               # Generate protobuf code from .proto files
# Note: Proto files are located in proto/ directory when available
```

### gRPC Server Operations

```bash
make dev-server              # Start development gRPC server (port 50051)
# Server operations are handled through the FlextGrpcPlatform API
```

### Build and Distribution

```bash
make build                   # Build distribution packages
make build-clean             # Clean and build
make clean                   # Remove all artifacts
make clean-all               # Deep clean including virtual environment
make reset                   # Reset project (clean-all + setup)
```

### Diagnostics and Utilities

```bash
make diagnose                # Show Python, Poetry, and gRPC versions
make doctor                  # Health check (diagnose + check)
make shell                   # Open Poetry Python shell
make pre-commit              # Run pre-commit hooks manually
make deps-update             # Update all dependencies
make deps-show               # Show dependency tree
make deps-audit              # Security audit of dependencies

# Convenient aliases for common commands
make t                       # test
make l                       # lint
make f                       # format
make tc                      # type-check
make c                       # clean
make i                       # install
make v                       # validate
```

## Testing Strategy

### Test Structure

- **Unit Tests** (`tests/unit/`): Test individual components in isolation
- **Integration Tests** (`tests/integration/`): Test component interactions
- **E2E Tests** (`tests/e2e/`): Test complete workflows

### Coverage Requirements

- **Minimum 90% coverage** enforced by `make test`
- Focus on domain entities and services in `src/flext_grpc/`
- Use `make coverage-html` to identify gaps

### Test Configuration

- Uses pytest with comprehensive plugins
- Auto-cleanup of global container between tests
- Fixtures for common test data and configurations

## Key Development Patterns

### Entity Creation and Validation

```python
# Create entities using direct instantiation
server = FlextGrpcServer(
    id="server-1",
    host="localhost",
    port=50051,
    max_workers=10,
    created_at=datetime.now(UTC)
)

# Always validate domain rules
validation = server.validate_domain_rules()
if validation.is_failure:
    return FlextResult.fail(validation.error)
```

### State Transitions

```python
# Use copy_with() for immutable state changes
start_result = server.start()  # stopped → starting
if start_result.success:
    running_server = start_result.data.mark_running()  # starting → running
```

### Service Operations

```python
# Use domain services for business logic
server_service = FlextGrpcServerService()
result = server_service.execute("start", server)
if result.success:
    started_server = result.data
```

### Result Pattern Usage

```python
# Always use FlextResult for operations that can fail
def risky_operation() -> FlextResult[str]:
    if error_condition:
        return FlextResult.fail("Operation failed")
    return FlextResult.ok("Success")

# Handle results properly
result = risky_operation()
if result.success:
    process_data(result.data)
else:
    log_error(result.error)
```

## Configuration Management

### Environment Variables

```bash
# gRPC settings
export FLEXT_GRPC_HOST=localhost
export FLEXT_GRPC_PORT=50051
export FLEXT_GRPC_MAX_WORKERS=10
export FLEXT_GRPC_DEV_MODE=true

# Protocol Buffers
export PROTOBUF_PYTHON_IMPLEMENTATION=python
```

### Configuration Classes

```python
# Use FlextGrpcConfig for settings
config = FlextGrpcConfig(
    host="localhost",
    port=50051,
    max_workers=10,
    timeout=30.0
)
```

## Dependencies

### Core Dependencies

- **flext-core**: Foundation library providing base patterns, entities, and container
- **flext-observability**: Monitoring, metrics, and health checks
- **grpcio (>=1.50.0)**: Core gRPC functionality
- **grpcio-tools (==1.71.2)**: Protocol buffer compilation
- **pydantic (>=2.11.7)**: Data validation and settings
- **protobuf (>=4)**: Protocol buffer support

### Development Tools

- **pytest**: Testing framework with comprehensive plugins
- **ruff**: Linting and formatting (ALL rules enabled)
- **mypy**: Strict type checking
- **bandit**: Security scanning
- **pre-commit**: Git hooks for quality gates

## Common Issues and Solutions

### Quality Gate Failures

```bash
# If lint fails
make fix                     # Auto-fix issues
make format                  # Format code

# If type check fails
mypy src/ tests/ --show-error-codes  # See specific errors

# If tests fail
pytest tests/ -v -x          # Stop on first failure
pytest tests/ --lf           # Run only last failed
```

### Protocol Buffer Issues

```bash
# Regenerate protobuf files (if proto/ directory exists)
make proto-gen

# Check protobuf dependencies
poetry run python -c "import grpc; print(f'gRPC version: {grpc.__version__}')"
```

### Container and Service Issues

```bash
# Debug service registration with flext-core
poetry run python -c "from flext_core import get_flext_container; print(get_flext_container().list_services())"

# Check gRPC functionality
poetry run python -c "import grpc; print('gRPC imported successfully')"

# Test entity creation
poetry run python -c "from flext_grpc.entities import FlextGrpcServer; print('Entities working')"
```

### Development Environment Issues

```bash
# Full project health check
make doctor                  # Runs diagnose + check

# Reset development environment completely
make reset                   # clean-all + setup

# Check Python and Poetry versions
make diagnose

# Update and audit dependencies
make deps-update && make deps-audit
```

## Integration with FLEXT Ecosystem

This library is part of the larger FLEXT ecosystem and follows established patterns:

- Uses `flext-core` for foundational patterns
- Integrates with `flext-observability` for monitoring
- Provides gRPC communication layer for other FLEXT services
- Follows workspace-wide quality standards and conventions

## TODO: GAPS DE ARQUITETURA IDENTIFICADOS - PRIORIDADE ALTA

### 🚨 GAP 1: Go Integration Missing

**Status**: ALTO - gRPC bridge com FlexCore (Go) não especificado
**Problema**:

- FlexCore (Go) usa gRPC mas integração com flext-grpc não documentada
- Protocol buffers não compartilhados entre Go e Python services
- Type safety não garantida entre Go e Python gRPC calls

**TODO**:

- [ ] Criar shared Protocol Buffer definitions para Go/Python integration
- [ ] Documentar gRPC client patterns para Go services
- [ ] Implementar type-safe serialization entre Go/Python
- [ ] Criar integration testing com FlexCore service

### 🚨 GAP 2: Service Discovery Integration Gap

**Status**: ALTO - Service discovery não integrado com ecosystem
**Problema**:

- gRPC clients precisam conhecer hosts/ports manualmente
- Não integra com service registry do ecosystem
- Load balancing entre services não implementado

**TODO**:

- [ ] Implementar service discovery integration
- [ ] Criar client-side load balancing patterns
- [ ] Integrar com ecosystem service registry
- [ ] Documentar service discovery patterns para deployment

### 🚨 GAP 3: Coverage de Testes Baixa (76%)

**Status**: ALTO - Cobertura abaixo do mínimo ecosystem (90%)
**Problema**:

- Coverage atual 76% vs 90% mínimo exigido pelo ecosystem
- Domain entities e services não completamente testados
- Integration tests insuficientes

**TODO**:

- [ ] Aumentar coverage para 90%+ seguindo padrões ecosystem
- [ ] Criar comprehensive integration tests
- [ ] Implementar property-based testing para entities
- [ ] Adicionar performance benchmarks para gRPC operations

## Examples

See `examples/` directory for comprehensive usage examples:

- `basic_usage.py`: Core functionality and entity usage
- `advanced_usage.py`: Complex scenarios with streaming and service management
