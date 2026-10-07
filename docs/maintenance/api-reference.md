# Documentation maintenance API reference

<!-- TOC START -->

<!-- TOC END -->

FLEXT-gRPC does not expose a Python documentation-maintenance API. The
`DocumentationAuditor`, `LinkValidator`, `StyleValidator`, and related classes
previously described here are not part of this package. Do not import them from `docs`
or build integrations around them.

Documentation validation is performed through the canonical `make docs` verb at the
active workspace root. The package's docs CI invokes the same verb. A failed invocation
is a documentation failure; fix its source and rerun the verb.

For the actual gRPC package API, see [the public surface summary](../index.md) and the
[`FlextGrpc` facade](../../src/flext_grpc/api.py). The package root publishes the facade
and its typed `c`, `t`, `p`, `m`, and `u` contracts; those contracts concern gRPC
behavior, not documentation maintenance.
