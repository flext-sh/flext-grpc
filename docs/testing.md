# Testing flext-grpc

<!-- TOC START -->

- [Behavioral boundary](#behavioral-boundary)
- [Native gate](#native-gate)

<!-- TOC END -->

The public consumer contract and real runtime behavior determine acceptance. Tests
confirm those outcomes; an old coverage percentage or historical failure count is not a
current baseline. The canonical evidence is the native gate report for the exact commit
under review.

## Behavioral boundary

Construct the public `FlextGrpc` facade and call its public operations. `create_server`,
`create_client`, `create_stream`, and `create_service` return typed `p.Result` values
carrying `m.Grpc` models. Assert the result and observable model state. A constructed
server entity does not by itself prove that a socket is listening.

Runtime integration tests must start a real server, connect through the real client
boundary, exercise the transport, and stop it. Failures must retain their original
cause. Use bounded timeouts and clean up every listener and channel. Test fixtures may
assemble valid input; they must not replace the owner under test with canned responses
or mock internals. Do not skip a failing path or mask a warning.

Settings and config tests read the typed `settings.Grpc` and `config.Grpc` authorities
and validate invariants or round trips across valid values. They do not freeze a mutable
configured host, port, timeout, or worker count as the expected answer. Existing
public-boundary examples live in `tests/unit/test_api.py`,
`tests/unit/test_services.py`, and `tests/unit/test_config.py`.

## Native gate

Run from the active workspace root:

```bash
make setup
make check
make test
make docs
```

The root `make test` is the test entry point; do not invoke pytest directly or pass ad
hoc selectors to bare Make verbs. Preserve the command, exit code, test counts,
warnings, skips, and report path. A typed incremental testmon cache hit is recorded as a
cache hit, never described as tests passing. After the PR merges, run the gate again
against the exact integration SHA.
