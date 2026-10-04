# ADR-001: Clean Architecture Adoption

<!-- TOC START -->

- [Table of Contents](#table-of-contents)
- [Status](#status)
- [Context](#context)
- [Decision](#decision)
- [Consequences](#consequences)
  - [Positive Consequences](#positive-consequences)
  - [Negative Consequences](#negative-consequences)
- [Alternatives Considered](#alternatives-considered)
  - [Traditional Layered Architecture](#traditional-layered-architecture)
  - [Hexagonal Architecture](#hexagonal-architecture)
  - [Onion Architecture](#onion-architecture)
  - [Microservices Architecture](#microservices-architecture)
- [Implementation Details](#implementation-details)
  - [Layer Boundaries](#layer-boundaries)
  - [Dependency Rules](#dependency-rules)
  - [Interface Design](#interface-design)
- [References](#references)
- [Notes](#notes)

<!-- TOC END -->

## Table of Contents

- [ADR-001: Clean Architecture Adoption](#adr-001-clean-architecture-adoption)
  - [Status](#status)
  - [Context](#context)
  - [Decision](#decision)
  - [Consequences](#consequences)
    - [Positive Consequences](#positive-consequences)
    - [Negative Consequences](#negative-consequences)
  - [Alternatives Considered](#alternatives-considered)
    - [Traditional Layered Architecture](#traditional-layered-architecture)
    - [Hexagonal Architecture](#hexagonal-architecture)
    - [Onion Architecture](#onion-architecture)
    - [Microservices Architecture](#microservices-architecture)
  - [Implementation Details](#implementation-details)
    - [Layer Boundaries](#layer-boundaries)
    - [Dependency Rules](#dependency-rules)
    - [Interface Design](#interface-design)
      - Domain defines interfaces
      - Infrastructure implements interfaces
  - [References](#references)
  - [Notes](#notes)

## Status

Accepted

## Context

FLEXT-gRPC was initially developed with a traditional layered architecture, but as the
codebase grew to include domain entities, service coordination, infrastructure concerns,
and FLEXT ecosystem integration, the code became increasingly complex and difficult to
maintain.

The main issues we were facing:

- Mixed concerns across layers (business logic mixed with infrastructure)
- Difficult unit testing due to tight coupling
- Complex dependency management
- Hard to evolve and extend functionality
- Difficult to understand the codebase for new team members

We needed an architectural approach that would:

- Provide clear separation of concerns
- Enable behavioral testing through public boundaries
- Support clean dependency management
- Allow independent evolution of layers
- Make the codebase more maintainable and understandable

## Decision

Adopt Clean Architecture, using ports and adapters at transport boundaries, with the
following layer structure:

```text
┌─────────────────────────────────────────┐
│              FLEXT-gRPC                 │
├─────────────────────────────────────────┤
│ Domain Layer (entities.py)              │
│ ├── FlextGrpcServer (state machine)    │
│ ├── FlextGrpcClient (connection mgmt)  │
│ ├── FlextGrpcChannel (communication)   │
│ ├── FlextGrpcService (service def)     │
│ └── FlextGrpcStream (streaming ops)    │
├─────────────────────────────────────────┤
│ Application Layer (services.py)        │
│ ├── FlextGrpcServerService             │
│ ├── FlextGrpcClientService             │
│ ├── FlextGrpcStreamService             │
│ └── FlextGrpcPlatform (facade)         │
├─────────────────────────────────────────┤
│ Infrastructure Layer                    │
│ ├── Configuration (settings.py)          │
│ ├── API Functions (api.py)             │
│ ├── Exception Hierarchy (exceptions.py)│
│ └── Protocol Buffers (proto/)          │
└─────────────────────────────────────────┘
```

With the following principles:

- **Dependency Inversion**: Higher layers don't depend on lower layers
- **Domain Centrality**: Business logic is independent of frameworks
- **Interface Segregation**: Clear interfaces between layers
- **Single Responsibility**: Each class has one reason to change

## Consequences

### Positive Consequences

**Better Testability**

- Domain entities can be tested in isolation
- Dependencies can be supplied through explicit contracts
- Unit tests don't require infrastructure setup
- Faster test execution and better coverage

**Improved Maintainability**

- Clear responsibilities for each layer
- Easier to locate and modify code
- Reduced coupling between components
- Better code organization and navigation

**Enhanced Flexibility**

- Infrastructure can be swapped without affecting business logic
- New features can be added without breaking existing code
- Technology migrations are easier
- Framework upgrades don't affect core logic

**Better Developer Experience**

- Clear architectural boundaries
- Easier onboarding for new developers
- Consistent patterns throughout codebase
- Reduced cognitive load when working with code

### Negative Consequences

**Increased Complexity**

- More files and classes to manage
- Additional interfaces and abstractions
- Learning curve for new team members
- More boilerplate code

**Development Overhead**

- Longer initial development time
- More classes and interfaces to maintain
- Additional complexity in simple operations
- More decisions about layer placement

**Performance Considerations**

- Additional indirection through interfaces
- Potential performance overhead from abstraction layers
- Need to be careful about performance-critical paths

## Alternatives Considered

### Traditional Layered Architecture

**Rejected because:**

- Doesn't provide enough separation of concerns
- Business logic still coupled to infrastructure
- Difficult to test business rules in isolation
- Hard to swap implementations

### Hexagonal Architecture

**Not chosen because:**

- More complex than needed for our use case
- Additional complexity in ports and adapters
- Overkill for a library rather than a full application
- Team familiarity with Clean Architecture patterns

### Onion Architecture

**Not chosen because:**

- Similar to Clean Architecture but with more layers
- Additional complexity without clear benefits
- Team already familiar with Clean Architecture
- Simpler approach better suited for library development

### Microservices Architecture

**Not applicable because:**

- FLEXT-gRPC is a library, not a service
- Would be overkill for a communication library
- Clean Architecture provides better separation within a single codebase

## Implementation Details

### Layer Boundaries

**Domain Layer**

- Pure business logic, no external dependencies
- State machines and business rules
- Entity validation and business constraints
- Independent of frameworks and infrastructure

**Application Layer**

- Orchestrates domain objects
- Contains use cases and application logic
- Coordinates between domain and infrastructure
- Defines application-specific interfaces

**Infrastructure Layer**

- External concerns (grpcio, protobuf, networking)
- Framework and library integrations
- Configuration and environment concerns
- Data persistence and external APIs

### Dependency Rules

1. **Domain Layer**: No dependencies on other layers
1. **Application Layer**: Can depend on Domain, not Infrastructure
1. **Infrastructure Layer**: Can depend on all layers (implements interfaces)

### Interface Design

The package publishes transport contracts through `p.Grpc` and typed payloads through
`m.Grpc`. `FlextGrpc` composes the service implementations and exposes their operations
at the public boundary. Transport adapters depend on those contracts; consumers use the
facade and its `p.Result` outcomes. The source in `src/flext_grpc/protocols.py`,
`src/flext_grpc/models.py`, and `src/flext_grpc/api.py` is authoritative for the current
signatures.

## References

- [Clean Architecture Book by Robert C. Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [The Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/)
- [Dependency Inversion Principle](https://en.wikipedia.org/wiki/Dependency_inversion_principle)

## Notes

This ADR established the fundamental architectural approach for FLEXT-gRPC. All
subsequent development follows these Clean Architecture principles. The architecture has
proven effective for maintainability and testability.

The layer separation has been particularly valuable for:

- Unit testing (domain logic can be tested without grpcio)
- Framework independence (could swap grpcio for other protocols)
- Feature development (new features fit cleanly into layers)
- Code organization (developers know where to put new code)
