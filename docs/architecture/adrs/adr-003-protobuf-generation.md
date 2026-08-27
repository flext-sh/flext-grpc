# ADR-003: Protocol Buffer Generation Strategy

<!-- TOC START -->
- [Table of Contents](#table-of-contents)
- [Status](#status)
- [Context](#context)
- [Decision](#decision)
  - [Version Management](#version-management)
  - [Generation Process](#generation-process)
  - [Code Organization](#code-organization)
  - [Maintenance Strategy](#maintenance-strategy)
- [Consequences](#consequences)
  - [Positive Consequences](#positive-consequences)
  - [Negative Consequences](#negative-consequences)
- [Alternatives Considered](#alternatives-considered)
  - [Dynamic Version Resolution](#dynamic-version-resolution)
  - [Manual Code Generation](#manual-code-generation)
  - [Monorepo with Shared Versions](#monorepo-with-shared-versions)
  - [Protobuf as Separate Package](#protobuf-as-separate-package)
- [Implementation Plan](#implementation-plan)
  - [Phase 1: Immediate Fix (Current)](#phase-1-immediate-fix-current)
  - [Phase 2: Automation (Next Sprint)](#phase-2-automation-next-sprint)
  - [Phase 3: Optimization (Future)](#phase-3-optimization-future)
- [Technical Details](#technical-details)
  - [Version Pinning Strategy](#version-pinning-strategy)
  - [Docker Generation Environment](#docker-generation-environment)
  - [CI/CD Integration](#cicd-integration)
- [Risks and Mitigations](#risks-and-mitigations)
  - [Version Lock-in Risk](#version-lock-in-risk)
  - [Docker Complexity Risk](#docker-complexity-risk)
  - [Ecosystem Compatibility Risk](#ecosystem-compatibility-risk)
- [Success Criteria](#success-criteria)
  - [Technical Success](#technical-success)
  - [Quality Success](#quality-success)
  - [Process Success](#process-success)
- [References](#references)
- [Notes](#notes)
<!-- TOC END -->

## Table of Contents

- [ADR-003: Protocol Buffer Generation Strategy](#adr-003-protocol-buffer-generation-strategy)
  - [Status](#status)
  - [Context](#context)
  - [Decision](#decision)
    - [Version Management](#version-management)
    - [Generation Process](#generation-process)
    - [Code Organization](#code-organization)
    - [Maintenance Strategy](#maintenance-strategy)
  - [Consequences](#consequences)
    - [Positive Consequences](#positive-consequences)
    - [Negative Consequences](#negative-consequences)
  - [Alternatives Considered](#alternatives-considered)
    - [Dynamic Version Resolution](#dynamic-version-resolution)
    - [Manual Code Generation](#manual-code-generation)
    - [Monorepo with Shared Versions](#monorepo-with-shared-versions)
    - [Protobuf as Separate Package](#protobuf-as-separate-package)
  - [Implementation Plan](#implementation-plan)
    - [Phase 1: Immediate Fix (Current)](#phase-1-immediate-fix-current)
    - [Phase 2: Automation (Next Sprint)](#phase-2-automation-next-sprint)
    - [Phase 3: Optimization (Future)](#phase-3-optimization-future)
  - [Technical Details](#technical-details)
    - [Version Pinning Strategy](#version-pinning-strategy)
  - [Docker Generation Environment](#docker-generation-environment)
  - [CI/CD Integration](#cicd-integration)
  - [Risks and Mitigations](#risks-and-mitigations)
    - [Version Lock-in Risk](#version-lock-in-risk)
    - [Docker Complexity Risk](#docker-complexity-risk)
    - [Ecosystem Compatibility Risk](#ecosystem-compatibility-risk)
  - [Success Criteria](#success-criteria)
    - [Technical Success](#technical-success)
    - [Quality Success](#quality-success)
    - [Process Success](#process-success)
  - [References](#references)
  - [Notes](#notes)

## Status

Blocked

## Context

FLEXT-gRPC needs to provide Protocol Buffer definitions for gRPC services,
but we're facing version compatibility issues between the generated protobuf files and the runtime dependencies.

The current situation:

- **grpcio version**: 1.75.1 (latest stable)
- **grpcio-tools version**: 1.75.1 (for code generation)
- **protobuf version**: 6.30.2 (latest)
- **Generated protobuf**: Uses protobuf 6.31.1 syntax/behavior

This creates import failures because:

1. Generated code expects protobuf 6.31.1 features
1. Runtime has protobuf 6.30.2
1. Version mismatch causes ImportError on module loading

The protobuf generation process involves:

1. Writing .proto files with service definitions
1. Running grpcio-tools to generate Python code
1. Generated code includes version-specific imports and behaviors

We need a strategy that:

- Ensures version compatibility between generation and runtime
- Provides reliable protobuf code generation
- Supports future updates and maintenance
- Works within the FLEXT ecosystem constraints

## Decision

Implement a **version-pinned protobuf generation strategy** with the following approach:

### Version Management

- **Lock versions**: Pin grpcio-tools and protobuf to exact compatible versions
- **Separate environments**: Use different environments for generation vs runtime if needed
- **Version validation**: Automated checks to ensure compatibility

### Generation Process

- **Docker-based generation**: Use Docker containers with pinned versions for reproducible builds
- **CI/CD integration**: Automated generation in CI pipeline with version validation
- **Fallback generation**: Local generation with version compatibility checks

### Code Organization

- **Separate proto/ directory**: Keep generated code isolated from hand-written code
- **Version metadata**: Include version information in generated code comments
- **Compatibility checks**: Runtime validation of protobuf versions

### Maintenance Strategy

- **Regular updates**: Quarterly review and update of protobuf versions
- **Compatibility testing**: Automated tests for version compatibility
- **Migration planning**: Clear process for version updates

## Consequences

### Positive Consequences

**Reliability**

- Eliminates import errors due to version mismatches
- Predictable code generation across environments
- Consistent behavior between development and production

**Maintainability**

- Clear process for updating protobuf versions
- Automated validation prevents compatibility issues
- Docker-based generation ensures reproducibility

**Developer Experience**

- Reliable local development environment
- Clear error messages for version issues
- Automated generation reduces manual steps

### Negative Consequences

**Complexity**

- Additional Docker layer for code generation
- Version management overhead
- CI/CD pipeline complexity

**Maintenance Burden**

- Regular version update reviews required
- Docker image maintenance needed
- Compatibility testing overhead

**Development Overhead**

- Local development requires Docker
- Additional steps for protobuf changes
- Learning curve for Docker-based workflow

## Alternatives Considered

### Dynamic Version Resolution

**Rejected because:**

- Unpredictable behavior across environments
- Difficult to reproduce issues
- No guarantee of compatibility

### Manual Code Generation

**Rejected because:**

- Error-prone and inconsistent
- Difficult to maintain across team
- No version tracking or validation

### Monorepo with Shared Versions

**Not feasible because:**

- FLEXT ecosystem has diverse version requirements
- Breaking changes in protobuf ecosystem
- Different teams have different update cadences

### Protobuf as Separate Package

**Rejected because:**

- Increases complexity of library distribution
- Version management becomes more complex
- Users need to manage additional dependencies

## Implementation Plan

### Phase 1: Immediate Fix (Current)

1. Pin compatible versions in pyproject.toml
1. Create Docker-based generation environment
1. Implement version validation checks
1. Fix current import errors

### Phase 2: Automation (Next Sprint)

1. CI/CD pipeline for automated generation
1. Version compatibility testing
1. Docker image maintenance automation
1. Local development workflow updates

### Phase 3: Optimization (Future)

1. Generation performance optimization
1. Advanced validation and error reporting
1. Integration with protobuf ecosystem updates
1. Alternative generation strategies evaluation

## Technical Details

### Version Pinning Strategy

```toml
# pyproject.toml
[tool.poetry.dependencies]
grpcio = "1.75.1"
grpcio-tools = "1.75.1"
protobuf = "6.30.2"

[tool.poetry.group.dev.dependencies]
# Separate dev dependencies if needed
```

### Docker Generation Environment

```dockerfile
# Dockerfile.protobuf
FROM python:3.13-slim

# Install specific versions
RUN pip install grpcio-tools==1.75.1 protobuf==6.30.2

# Copy proto files
COPY proto/ /proto/

# Generate code
RUN python -m grpc_tools.protoc \
    --proto_path=/proto \
    --python_out=/generated \
    --grpc_python_out=/generated \
    /proto/*.proto
```

### CI/CD Integration

```yaml
# .github/workflows/generate-proto.yml
name: Generate Protocol Buffers
on:
  push:
    paths:
      - "proto/*.proto"

jobs:
  generate:
    runs-on: ubuntu-latest
    container:
      image: flext-grpc-proto-generator:latest
    steps:
      - name: Generate Python code
        run: |
          python -m grpc_tools.protoc \
            --proto_path=proto \
            --python_out=src/flext_grpc/proto \
            --grpc_python_out=src/flext_grpc/proto \
            proto/*.proto
```

## Risks and Mitigations

### Version Lock-in Risk

**Risk**: Pinned versions may miss security updates or bug fixes
**Mitigation**:

- Regular security audits of pinned versions
- Quarterly review process for version updates
- Emergency update process for critical security issues

### Docker Complexity Risk

**Risk**: Docker-based generation adds complexity for developers
**Mitigation**:

- Clear documentation and setup scripts
- Fallback local generation option
- Team training on Docker workflow

### Ecosystem Compatibility Risk

**Risk**: Version conflicts with other FLEXT libraries
**Mitigation**:

- Regular compatibility testing across FLEXT ecosystem
- Clear communication of version requirements
- Coordination with other FLEXT teams

## Success Criteria

### Technical Success

- [ ] All protobuf imports work without version errors
- [ ] Docker-based generation produces consistent results
- [ ] CI/CD pipeline successfully generates and validates code
- [ ] Local development workflow supports protobuf changes

### Quality Success

- [ ] No import errors in test suite
- [ ] Generated code follows FLEXT coding standards
- [ ] Version compatibility validated across environments
- [ ] Documentation includes generation process

### Process Success

- [ ] Team can reliably modify protobuf definitions
- [ ] Generation process is automated and fast
- [ ] Version update process is clear and documented
- [ ] Emergency update process works when needed

## References

- [gRPC Python Generated Code](https://grpc.io/docs/languages/python/generated-code/)
- [Buffers Python](https://developers.google.com/protocol-buffers/docs/pythontutorial)
- [Docker for Development](https://docs.docker.com/develop/dev-best-practices/)
- [Semantic Versioning](https://semver.org/)

## Notes

This ADR is currently BLOCKED due to the immediate need to resolve import errors. The protobuf version mismatch is preventing the library from functioning,

```
 which blocks all other development work.
```

Once resolved,
this ADR will be marked as ACCEPTED and implementation will proceed according to the plan outlined above.

The Docker-based generation approach provides the most reliable solution for version compatibility while maintaining development workflow efficiency.
