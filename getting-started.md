# Getting Started with flext-grpc

<!-- TOC START -->
- [Table of Contents](#table-of-contents)
- [Prerequisites](#prerequisites)
  - [System Requirements](#system-requirements)
  - [Dependencies](#dependencies)
- [Installation](#installation)
  - [1. Clone and Setup](#1-clone-and-setup)
  - [2. Verify Installation](#2-verify-installation)
- [Basic Usage](#basic-usage)
  - [Server Creation](#server-creation)
  - [Client Creation](#client-creation)
  - [Platform Management](#platform-management)
  - [Configuration](#configuration)
- [Development Setup](#development-setup)
  - [Development Commands](#development-commands)
  - [Quality Status Check](#quality-status-check)
- [Current Limitations](#current-limitations)
  - [Test Coverage](#test-coverage)
  - [Known Issues](#known-issues)
- [Next Steps](#next-steps)
- [Related Documentation](#related-documentation)
<!-- TOC END -->

## Table of Contents

- [Getting Started with flext-grpc](#getting-started-with-flext-grpc)
  - [Prerequisites](#prerequisites)
    - [System Requirements](#system-requirements)
    - [Dependencies](#dependencies)
  - [Installation](#installation)
    - [1. Clone and Setup](#1-clone-and-setup)
    - [2. Verify Installation](#2-verify-installation)
- [Test core imports](#test-core-imports)
- [Test functionality](#test-functionality)
  - [Basic Usage](#basic-usage)
    - [Server Creation](#server-creation)
- [Create gRPC server](#create-grpc-server)
  - [Client Creation](#client-creation)
- [Create gRPC client](#create-grpc-client)
  - [Platform Management](#platform-management)
- [Create platform for advanced operations](#create-platform-for-advanced-operations)
  - [Configuration](#configuration)
- [Create configuration with validation](#create-configuration-with-validation)
  - [Development Setup](#development-setup)
    - [Development Commands](#development-commands)
- [Run a basic test](#run-a-basic-test)
- [Check test coverage (currently 39%)](#check-test-coverage-currently-39)
- [Type checking](#type-checking)
- [Code linting](#code-linting)
  - [Quality Status Check](#quality-status-check)
- [Verify imports work](#verify-imports-work)
- [Test basic functionality](#test-basic-functionality)
  - [Current Limitations](#current-limitations)
    - [Test Coverage](#test-coverage)
    - [Known Issues](#known-issues)
  - [Next Steps](#next-steps)

**Version**: 0.12.0-dev | **Updated**: April 14, 2026

Setup guide for flext-grpc gRPC communication library.

## Prerequisites

### System Requirements

- **Python 3.13** (required)
- **Poetry** (dependency management)
- **FLEXT workspace** (for ecosystem integration)

### Dependencies

Managed via Poetry (no manual installation required):

- grpcio and grpcio-tools
- protobuf
- flext-core (FLEXT ecosystem integration)

## Installation

### 1. Clone and Setup

```bash
git clone https://github.com/flext-sh/flext/tree/main/flext-grpc
cd flext-grpc
poetry install
```

### 2. Verify Installation

```bash
# Test core imports
poetry run python -c "from flext_grpc import create_server, FlextGrpcPlatform; print('Import successful')"

# Test functionality
poetry run python -c "
from flext_grpc import create_server
server = create_server('localhost', 50051, 10)
print(f'Server: {server.address}, state: {server.state}')
"
```

## Basic Usage

### Server Creation

```python notest
from flext_grpc import create_server

# Create gRPC server
server = create_server("localhost", 50051, 10)
print(f"Server address: {server.address}")
print(f"Server state: {server.state}")
```

### Client Creation

```python notest
from flext_grpc import create_client

# Create gRPC client
client = create_client("localhost:50051")
print(f"Client created: {type(client).__name__}")
```

### Platform Management

```python notest
from flext_grpc import FlextGrpcPlatform

# Create platform for advanced operations
platform = FlextGrpcPlatform()
print(f"Platform ready: {type(platform).__name__}")
```

### Configuration

```python
from flext_grpc import FlextGrpcSettings

# Create configuration with validation
settings = FlextGrpcSettings.model_validate(
    {
        "Grpc": {
            "host": "localhost",
            "port": 50051,
            "max_workers": 10,
            "timeout": 30.0,
        }
    }
)
print(f"Config: {settings.Grpc.host}:{settings.Grpc.port}")
```

## Development Setup

### Development Commands

```bash
# Run a basic test
poetry run pytest tests/unit/test_config.py::TestFlextGrpcSettings::test_create_valid_config_with_defaults -v

# Check test coverage (currently 39%)
poetry run pytest tests/unit/test_config.py --cov=src/flext_grpc --cov-report=term

# Type checking
poetry run mypy src/

# Code linting
poetry run ruff check src/
```

### Quality Status Check

Current status verification:

```bash
# Verify imports work
poetry run python -c "
import sys
from flext_grpc import create_server, create_client, FlextGrpcPlatform
from flext_grpc import FlextGrpcSettings
print('✅ All imports successful')
"

# Test basic functionality
poetry run python -c "
from flext_grpc import create_server
server = create_server('localhost', 50051, 10)
print(f'✅ Server creation: {server.address}')
"
```

## Current Limitations

### Test Coverage

- **Current**: 39% coverage (956 of 1,798 statements missed)
- **Target**: 90% (configured in pyproject.toml)
- **Gap**: 64 percentage points to address

### Known Issues

- Some test protobuf files may need regeneration if version mismatches occur
- Test suite validation in progress (18,018 test lines available)

## Next Steps

1. **Explore API Reference** - See [API Reference](api-reference.md) for complete function documentation
1. **Development Workflow** - See [Development](development.md) for contribution guidelines
1. **Integration Patterns** - See [Integration](integration.md) for FLEXT ecosystem usage
1. **Configuration** - See [Configuration](configuration.md) for advanced settings

---

For troubleshooting common issues, see [Troubleshooting](troubleshooting.md).

## Related Documentation

**Within Project**:

- [Architecture](architecture.md) - Architecture and design patterns
- [API Reference](api-reference.md) - Complete API documentation
- [Development](development.md) - Development workflow
- [Integration](integration.md) - FLEXT ecosystem usage
- [Configuration](configuration.md) - Advanced settings
- [Troubleshooting](troubleshooting.md) - Common issues

**Across Projects**:

- [flext-core Foundation](https://github.com/organization/flext/tree/main/flext-core/docs/architecture/overview.md) - Clean architecture and CQRS patterns
- [flext-core Service Patterns](https://github.com/organization/flext/tree/main/flext-core/docs/guides/service-patterns.md) - Service patterns and dependency injection
- [flext-api HTTP Framework](https://github.com/organization/flext/tree/main/flext-api/AGENTS.md) - HTTP foundation patterns

**External Resources**:

- [PEP 257 - Docstring Conventions](https://peps.python.org/pep-0257/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
