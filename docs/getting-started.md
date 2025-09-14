# Getting Started with flext-grpc

**Version**: 0.9.0 | **Updated**: September 17, 2025

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

```python
from flext_grpc import create_server

# Create gRPC server
server = create_server('localhost', 50051, 10)
print(f"Server address: {server.address}")
print(f"Server state: {server.state}")
```

### Client Creation

```python
from flext_grpc import create_client

# Create gRPC client
client = create_client('localhost:50051')
print(f"Client created: {type(client).__name__}")
```

### Platform Management

```python
from flext_grpc import FlextGrpcPlatform

# Create platform for advanced operations
platform = FlextGrpcPlatform()
print(f"Platform ready: {type(platform).__name__}")
```

### Configuration

```python
from flext_grpc.config import FlextGrpcConfig

# Create configuration with validation
config = FlextGrpcConfig(
    host='localhost',
    port=50051,
    max_workers=10,
    timeout=30.0
)
print(f"Config: {config.host}:{config.port}")
```

## Development Setup

### Development Commands

```bash
# Run a basic test
poetry run pytest tests/unit/test_config.py::TestFlextGrpcConfig::test_create_valid_config_with_defaults -v

# Check test coverage (currently 26%)
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
from flext_grpc.config import FlextGrpcConfig
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

- **Current**: 26% coverage (902 of 1,322 statements missed)
- **Target**: 90% (configured in pyproject.toml)
- **Gap**: 64 percentage points to address

### Known Issues

- Some test protobuf files may need regeneration if version mismatches occur
- Test suite validation in progress (18,018 test lines available)

## Next Steps

1. **Explore API Reference** - See [API Reference](api-reference.md) for complete function documentation
2. **Development Workflow** - See [Development](development.md) for contribution guidelines
3. **Integration Patterns** - See [Integration](integration.md) for FLEXT ecosystem usage
4. **Configuration** - See [Configuration](configuration.md) for advanced settings

---

For troubleshooting common issues, see [Troubleshooting](troubleshooting.md).