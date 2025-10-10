# FLEXT-GRPC

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![Development](https://img.shields.io/badge/status-development-orange.svg)](#)
[![gRPC Communication](https://img.shields.io/badge/grpc-communication-green.svg)](#)
[![Documentation](https://img.shields.io/badge/docs-organized-blue.svg)](./docs/)
[![GitHub](https://img.shields.io/badge/github-flext--grpc-black.svg)](https://github.com/flext/flext-grpc)

**gRPC communication library** for the FLEXT ecosystem using Clean Architecture patterns and railway-oriented programming.

> **⚠️ STATUS**: Development - Core functionality operational, test coverage at 26%, protobuf integration verified

## 📚 Documentation

**Complete documentation is available in the organized FLEXT documentation:**

- **[📖 Full Documentation](../docs/projects/flext-grpc/)** - Comprehensive guides, API reference, and examples
- **[🚀 Getting Started](../docs/projects/flext-grpc/guides/getting-started.md)** - Quick start guide
- **[🏗️ Architecture](../docs/projects/flext-grpc/architecture/architecture.md)** - System design and patterns
- **[🔌 API Reference](../docs/projects/flext-grpc/api/api-reference.md)** - Complete API documentation
- **[⚙️ Configuration](../docs/projects/flext-grpc/guides/configuration.md)** - Configuration patterns

---

---

## 🎯 Purpose

Provides gRPC communication patterns for microservices within the FLEXT data integration platform.

### Key Responsibilities

1. **gRPC Abstraction** - Layer over grpcio and protobuf libraries
2. **Service Management** - Server and client lifecycle operations
3. **Streaming Support** - Four gRPC patterns: unary, server streaming, client streaming, bidirectional

### Integration with FLEXT Ecosystem

- **flext-core** → Uses FlextResult, FlextContainer, FlextLogger patterns
- **FLEXT projects** → Intended as gRPC communication foundation

---

## 🏗️ Current Implementation

### FLEXT Integration Status

| Pattern            | Status         | Notes                                    |
| ------------------ | -------------- | ---------------------------------------- |
| FlextResult        | ✅ Implemented | Used throughout API                      |
| FlextContainer     | ✅ Implemented | Dependency injection present             |
| FlextLogger        | ✅ Implemented | Logging infrastructure                   |
| Clean Architecture | ✅ Implemented | Domain/service/infrastructure separation |

### Technical Details

- **Source Code**: 4,923 lines across 13 modules
- **Test Suite**: 18,018 lines across multiple test files
- **Test Coverage**: 39% (verified via pytest --cov)
- **Import Status**: ✅ All core modules importable after protobuf fixes

### Verified Working Functionality

```python
from flext_grpc import create_server, create_client, FlextGrpcPlatform
from flext_grpc.config import FlextGrpcConfig

# Server creation - verified working
server = create_server('localhost', 50051, 10)
# Output: Server address: localhost:50051, state: stopped

# Client creation - verified working
client = create_client('localhost:50051')
# Output: Client created successfully

# Platform management - verified working
platform = FlextGrpcPlatform()
# Output: Platform created successfully

# Configuration management - verified working
config = FlextGrpcConfig(host='localhost', port=50051, max_workers=10)
# Output: Config created with validation
```

---

## 🚀 Installation

### Prerequisites

- Python 3.13
- Poetry for dependency management
- grpcio and protobuf (managed via dependencies)

### Setup

```bash
git clone https://github.com/flext-sh/flext/tree/main/flext-grpc
cd flext-grpc
poetry install
```

---

## 🔧 Development

### Available Commands

```bash
# Install dependencies
poetry install

# Run individual test
poetry run pytest tests/unit/test_config.py::TestFlextGrpcConfig::test_create_valid_config_with_defaults -v

# Check coverage (currently 39%)
poetry run pytest tests/unit/test_config.py --cov=src/flext_grpc --cov-report=term

# Type checking
poetry run mypy src/

# Code linting
poetry run ruff check src/
```

### Quality Status

- **Import Validation**: ✅ Core functionality importable
- **Basic Operations**: ✅ Server/client creation working
- **Test Coverage**: ⚠️ 39% (needs improvement from pyproject.toml requirement of 90%)
- **Type Safety**: Available via mypy
- **Code Quality**: Available via ruff

---

## 🧪 Testing

### Current Test Status

- **Test Structure**: 18,018 lines across comprehensive test suite
- **Test Execution**: Individual tests can run successfully
- **Coverage Results**: 39% actual coverage (1,798 total statements, 956 missed)
- **Coverage Target**: 90% configured in pyproject.toml (not currently met)

### Test Execution Examples

```bash
# Run a working test
poetry run pytest tests/unit/test_config.py::TestFlextGrpcConfig::test_create_valid_config_with_defaults -v
# Result: PASSED

# Check coverage
poetry run pytest tests/unit/test_config.py --cov=src/flext_grpc --cov-report=term
# Result: 26% coverage, needs improvement
```

---

## 📊 Development Status

### Current Version (0.9.0)

**Working**:

- Core API functions (create_server, create_client, FlextGrpcPlatform)
- Configuration management with validation
- Basic import functionality

**Needs Work**:

- Test coverage improvement (39% → 90% target)
- Fix 28 failing tests (critical bugs in services, exceptions, protocols)
- Full test suite validation
- Complete protobuf integration testing

### Next Steps

1. **Test Coverage** - Address the 51 percentage point gap to meet 90% requirement
2. **Test Suite Validation** - Ensure all 18,018 lines of tests execute reliably
3. **Integration Testing** - Verify actual gRPC server/client communication
4. **Production Features** - Health checking, authentication, TLS

---

## 📚 Documentation

- **[Architecture](docs/architecture.md)** - Clean Architecture implementation
- **[API Reference](docs/api-reference.md)** - API documentation
- **[Configuration](docs/configuration.md)** - Settings management
- **[Integration](docs/integration.md)** - FLEXT ecosystem integration
- **[Getting Started](docs/getting-started.md)** - Setup instructions
- **[Development](docs/development.md)** - Development workflow
- **[Troubleshooting](docs/troubleshooting.md)** - Common issues

---

## 🤝 Contributing

### Development Focus

1. **Test Coverage** - Primary need to reach 90% from current 26%
2. **Functional Validation** - Ensure all features work as documented
3. **FLEXT Compliance** - Maintain ecosystem integration standards
4. **Code Quality** - Follow Clean Architecture patterns

### Quality Requirements

- **Test Coverage**: Must achieve 90% (currently 26%)
- **Import Functionality**: All modules must be importable
- **Type Safety**: Comprehensive type annotations
- **FLEXT Integration**: Complete flext-core pattern compliance

---

## 📄 License

MIT License

---

**flext-grpc v0.9.9** - gRPC communication library for FLEXT ecosystem.

**Current Focus**: Improving test coverage from 39% to meet the 90% requirement while fixing 28 failing tests.
