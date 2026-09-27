# Development

<!-- TOC START -->

- [Local cycle](#local-cycle)
- [Package boundaries](#package-boundaries)
- [Tests and review](#tests-and-review)

<!-- TOC END -->

Work from the active FLEXT workspace root. The root Makefile selects the package and
owns environment setup, generation, formatting, checks, tests, and builds. Follow the
current [workspace development contract](../AGENTS.md); use `make help` for the verbs
available on this branch.

## Local cycle

```bash
make setup
make gen
make fmt
make check
make test
make build
make docs
```

Run each command to completion and retain its exit status and report. A warning, skip,
missing tool or report, or empty collection is a failure to investigate. Do not call the
underlying Python tools directly or pass selectors to bare root verbs. Repeated
generation and formatting must leave no changes on an unchanged candidate.

## Package boundaries

The public entry point is `FlextGrpc` in `flext_grpc.api`, also exported by
`flext_grpc`. Its methods return `p.Result` containing package `m.Grpc` models. For
example, `create_server` returns a server model; starting a real server is a separate
lifecycle operation. A successful entity construction does not prove that a transport
listener is running.

```python
from flext_grpc import FlextGrpc

result = FlextGrpc().create_server()
if result.failure:
    raise RuntimeError(result.error)
server = result.value
```

The typed settings singleton is `settings.Grpc`; business rules are exposed under
`config.Grpc`. Change the canonical `config/*.yaml` owner or the settings model when
behavior must change. Never copy configured defaults into tests or documentation as
acceptance criteria. The generated `constants.py`, `models.py`, `protocols.py`,
`typings.py`, `utilities.py`, and package `__init__.py` are projections: change their
sources and regenerate.

The facade composes service implementations; declaration layers carry data and
contracts. Use `p.Grpc` for dependency contracts, `m.Grpc` for payloads, and `r`
outcomes for operational boundaries. Keep gRPC transport details behind the
implementation and depend on the facade from application code.

## Tests and review

Tests exercise public runtime behavior with real collaborators. The current examples are
in `tests/unit/test_api.py` and `tests/unit/test_services.py`. Assert a `p.Result`
outcome and the observable model state or transport effect. Do not assert private
construction details or replace a runtime owner with a test double. For network
behavior, validate the real listener and client interaction with bounded timeouts.

Review generated output, documentation, and the exact changed scope after `make gen`.
Run the native gates locally before publishing a PR; rerun at the integration SHA after
merging.
