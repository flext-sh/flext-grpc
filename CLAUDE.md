# flext-grpc - FLEXT Infrastructure

**Hierarchy**: PROJECT
**Parent**: [../CLAUDE.md](../CLAUDE.md) - Workspace standards
**Last Update**: 2025-12-07

---

## Project Overview

**FLEXT-gRPC** is the enterprise gRPC communication library for the FLEXT ecosystem, providing gRPC client and server functionality with protobuf integration.

**Version**: 0.9.0  
**Status**: Development - Core functionality operational  
**Python**: 3.13+  
**Coverage**: 39% (target: 75%+)

---

## Essential Commands

```bash
# Setup and validation
make setup                    # Complete development environment setup
make validate                 # Complete validation (lint + type + security + test)
make check                    # Quick check (lint + type)

# Quality gates
make lint                     # Ruff linting
make type-check               # Pyrefly type checking
make security                 # Bandit security scan
make test                     # Run tests
```

---

## Key Patterns

### gRPC Service Implementation

```python
from flext_core import FlextResult
from flext_grpc import FlextGrpcService

service = FlextGrpcService()

# Handle gRPC request
result = service.handle_request(request)
if result.is_success:
    response = result.unwrap()
```

---

## Critical Development Rules

### ZERO TOLERANCE Policies

**ABSOLUTELY FORBIDDEN**:
- ❌ Exception-based error handling (use FlextResult)
- ❌ Type ignores or `Any` types
- ❌ Mockpatch in tests

**MANDATORY**:
- ✅ Use `FlextResult[T]` for all operations
- ✅ Complete type annotations
- ✅ Zero Ruff violations
- ✅ 75%+ test coverage

---

**See Also**:
- [Workspace Standards](../CLAUDE.md)
- [flext-core Patterns](../flext-core/CLAUDE.md)
- [flext-api Patterns](../flext-api/CLAUDE.md)
