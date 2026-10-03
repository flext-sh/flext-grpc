# Documentation maintenance

<!-- TOC START -->

- No sections found

<!-- TOC END -->

Run documentation maintenance from the active `flext-grpc` worktree root:

```bash
make docs
```

This is the package's documentation lifecycle. It generates owned pages, applies the
formatter, validates links and examples, and audits the resulting content. Read the
reports under `.reports/docs/` when the command reports a finding. An audit finding
requires a source correction even if the command exits zero.

When a generator input changes, run `make gen` twice and require both runs to reach the
generator's fixed-point verification before running `make docs` again. Edit handwritten
source documents and generator inputs at their owners; generated pages are projections.

The package has no separate Python documentation-maintenance framework or API. See the
[API reference](api-reference.md) for that boundary and the
[documentation index](../index.md) for the published package guides.
