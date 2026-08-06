# AGENTS.md — flext-grpc

> **Parent workspace law** lives in [`../AGENTS.md`](../AGENTS.md) — read it first.
> Universal engineering core: `~/.agents/UNIVERSAL_CORE.md`. Composition: global skills + parent/root `AGENTS.md` + this scope delta. Do not re-embed universal law.
>
> **Standalone / independent mode:** when `../AGENTS.md` does not resolve, pin the parent raw `AGENTS.md` URL to the same branch/release as this package (never `main`).

<!-- AIHUB-AGENTS-SCOPE-LOCAL-BEGIN -->
**Package:** `flext_grpc` · deps: `flext-cli`, `flext-core`

## Overview

High-performance gRPC services layer.

## Structure

```text
src/flext_grpc/
├── api.py            # FlextGrpc facade (thin — no RPC behavior here)
├── base.py errors.py
├── proto/            # protobuf definitions + generated stubs
├── services/
├── constants.py typings.py protocols.py models.py utilities.py   # AUTO-GENERATED facets
└── _config.py _utilities/
```

## Code Map

| Symbol | Kind | Location | Role |
|--------|------|----------|------|
| `FlextGrpc` | class | `api.py` | thin package facade |

## Conventions (specific to this package)

- **Protobuf contracts (`proto/`) are the source of transport shape** — avoid placing RPC-specific behavior directly in `api.py`.
- Config/settings canonical pattern: ADR-012.
- Codemod governance (ast-grep + make mod): ADR-014.

## Anti-Patterns / Gotchas

- Generated protobuf stubs are excluded from Ruff/type gates via per-file ignores — regenerate through the build, never hand-edit.

## Commands

```bash
make check PROJECT=flext-grpc
make test  PROJECT=flext-grpc       # tests/unit
```
<!-- AIHUB-AGENTS-SCOPE-LOCAL-END -->
