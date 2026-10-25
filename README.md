# Browser Use: trust-boundary assessment

**Question:** do navigation errors, model answers and tool metadata correspond to enforced security boundaries?

**Result:** an owned destination received a request even though the navigation tool returned a policy error. This is a demonstrated behavioral defect in pre-navigation rejection, **not a confirmed exploitable vulnerability**. Three other failed assertions were answer-format failures, not demonstrated prompt-injection success.

Assessed: Browser Use **0.13.13**; snapshot `aa093a8`; inspected dispatcher bubus **1.5.6**. Assessment records predate this documentation update on 25 October 2026.

## Work performed

- Mapped the user-task → model → tool → event bus → browser path.
- Compared intended navigation rejection with receiver-side request records.
- Reviewed selected browser/proxy/profile controls, restricted model-answer scenarios and owned MCP authorization fixtures.
- Calibrated the result judge with one GREEN and six deliberately defective RED records; these were classifier controls, not six successful attacks.
- Separated product behavior, fixture limitations, documentation inconsistencies and unconfirmed security impact.

**Recorded coverage:** 231 logical records across historical executions: 227 passed, four failed. This is neither a fresh 231-test run nor full repository coverage.

## Read in order

1. [Reading guide and file map](READING-GUIDE.md)
2. [Architecture and observed flows](FLOW.md)
3. [Case study and classifications](CASE-STUDY.md)
4. [Measured evidence](evidence/coverage.json) and [four failure records](evidence/failures.json)
5. [Source pins](evidence/source-pins.json) · [offline verification](VERIFY.md)

Independent, AI-assisted assessment. No vendor affiliation, accepted bounty, CVE, complete-audit claim or general prompt-injection-resistance claim. No product tests were executed during this packaging update.
