# Reading guide

Start with [README](README.md). It explains the behavior and its security limits.

| Next question | File |
| --- | --- |
| How does the request reach Chrome? | [FLOW.md](FLOW.md) |
| Why can an error coexist with a request? | [CASE-STUDY.md](CASE-STUDY.md) |
| Which boundaries and scenarios were checked? | [Boundary matrix](matrices/boundaries.json) |
| What actually failed? | [failures.json](evidence/failures.json) |
| What do the coverage totals mean? | [coverage.json](evidence/coverage.json) |
| Which code was inspected? | [source-pins.json](evidence/source-pins.json) |
| How do I check file integrity? | [VERIFY.md](VERIFY.md) |

The matrix indexes retained evidence. It is not an executable test suite. The package verifier checks files and links, not Browser Use behavior.
