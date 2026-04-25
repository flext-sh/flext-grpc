# FLEXT-gRPC Architecture


<!-- TOC START -->
- [Structure](#structure)
- [What To Read](#what-to-read)
- [Diagrams](#diagrams)
- [Validation](#validation)
- [Maintenance Rules](#maintenance-rules)
<!-- TOC END -->

Architecture docs for `flext-grpc` are organized by view type and kept aligned with the files that currently exist in this folder.

## Structure

```text
docs/architecture/
├── README.md
├── c4-model/
│   └── context.md
├── arc42/
│   └── 01_introduction.md
├── adrs/
│   ├── README.md
│   ├── adr-001-clean-architecture.md
│   └── adr-003-protobuf-generation.md
├── diagrams/
│   ├── context.puml
│   ├── containers.puml
│   ├── components.puml
│   ├── deployment.puml
│   ├── data-flow.puml
│   └── security.puml
└── tools/
    ├── generate-diagrams.sh
    └── validate_docs.py
```

## What To Read

- `c4-model/context.md`: system context and external boundaries.
- `arc42/01_introduction.md`: architecture goals and baseline constraints.
- `adrs/README.md`: ADR conventions for this package.
- `adrs/adr-001-clean-architecture.md`: core architecture style decision.
- `adrs/adr-003-protobuf-generation.md`: protobuf/codegen decision history.

## Diagrams

PlantUML sources live in `diagrams/`. Use the local helper script to render or refresh images when diagrams change.

```bash
cd flext-grpc/docs/architecture
./tools/generate-diagrams.sh
```

## Validation

Use the docs validator in this folder to check internal references and documentation structure.

```bash
cd flext-grpc/docs/architecture
python tools/validate_docs.py
```

## Maintenance Rules

- Keep this file as a factual index only; avoid speculative metrics or roadmap claims.
- When adding a new ADR, update both `adrs/README.md` and this index.
- When adding/removing architecture files, update the structure tree above in the same change.
