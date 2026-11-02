# Browser Use: rejected navigation still sent a request

**Status:** behavior defect reproduced; exploitable SSRF not established.

Browser Use operates Chrome through tools. In a local check, the navigation tool rejected an excluded destination, but the owned HTTP server still recorded its GET request.

- **Expected:** reject the navigation before contacting the destination.
- **Observed:** policy error and network request both occurred.
- **Impact:** a tool error did not prove prevention of the network side effect.
- **Limit:** trusted test code called the tool directly; no malicious-page → LLM → protected-resource chain was demonstrated.
- **Fix:** no upstream fix was verified.

Three other failed assertions were answer-format failures, not confirmed prompt injection.

## Evidence and details

[Boundary matrix](matrices/boundaries.json) · [Flow](FLOW.md) · [Case study](CASE-STUDY.md) · [Failure records](evidence/failures.json)

Snapshot: Browser Use 0.13.13, `aa093a8`. [Source pins](evidence/source-pins.json) · [File map](READING-GUIDE.md) · [Package check](VERIFY.md) · [Attribution / AI assistance](NOTICE.md).

Historical results; no new target execution in this documentation edit.
