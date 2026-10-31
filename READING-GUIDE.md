# Browser Use: reading guide

## Pick a reading depth

- **Two minutes:** README → the normal and observed diagrams in [FLOW.md](FLOW.md).
- **Technical review:** [CASE-STUDY.md](CASE-STUDY.md) → [failure records](evidence/failures.json) → [source pins](evidence/source-pins.json).
- **Package verification:** [VERIFY.md](VERIFY.md). This checks package integrity, not product behavior.

## Where to start

Read README.md for the summary, FLOW.md for the architecture, and CASE-STUDY.md for the expected behavior, observed result, and impact assessment. Use the evidence files to check the underlying measurements.

| File or directory | Purpose |
| --- | --- |
| [README.md](README.md) | Scope, headline result, version, and links into the study. |
| [FLOW.md](FLOW.md) | How the agent, tools, event bus, and browser connect. |
| [CASE-STUDY.md](CASE-STUDY.md) | Main analysis: expected behavior, observation, source explanation, limits, and recommendations. |
| [evidence/coverage.json](evidence/coverage.json) | Historical coverage accounting, not a new test run. |
| [evidence/failures.json](evidence/failures.json) | Four selected failed assertions and their classifications. |
| [evidence/source-pins.json](evidence/source-pins.json) | Exact source revisions and retained evidence fingerprints. |
| [VERIFY.md](VERIFY.md) | How to check this documentation package offline. |
| [verify_package.py](verify_package.py) | Checks hashes, sizes, and local Markdown links; does not run Browser Use. |
| [MANIFEST.json](MANIFEST.json) | Expected file sizes and SHA256 hashes used by the verifier. |
| [NOTICE.md](NOTICE.md) | Attribution, AI assistance, and assessment limits. |

## Short explanation of the case

This study asks whether an agent's errors and answers correspond to enforced boundaries. In a local navigation check, the tool returned a policy error, but the owned receiver recorded an HTTP request. The analysis connects receiver-side evidence to the event handlers and separates that behavior from unconfirmed exploitability.

The work was AI-assisted, not an entirely manual audit. The bundle contains selected historical evidence and source analysis, not a new target execution.

## Normal flow

A user task and page state reach the agent. The LLM proposes an action; the registry checks argument shape; the tool dispatches through BrowserSession and its event bus; CDP operates Chrome; page results return to the agent.

The LLM does not itself open the connection. Tool and browser code perform the action. Page text is untrusted data, not permission to act.

## What failed

The selected invariant was: reject excluded navigation before sending its request. An invariant is a condition expected to remain true.

One handler checks policy, while a separate handler performs navigation. An error in the former does not by itself establish cancellation of the latter. The retained test recorded both a tool error and a GET in the local receiver's fresh per-test request list. Moving to about:blank afterward cannot undo a request already received.

This source explanation is consistent with the logs. A complete measured schedule of every handler was not captured.

## Why this is not confirmed SSRF

Trusted stand code invoked the navigation tool directly. The study did not establish an untrusted page causing the agent to reach a protected resource. Secret disclosure, isolation escape, and interaction with someone else's server were not demonstrated.

Supported description: a scoped pre-navigation rejection defect. Unsupported description: proven SSRF through prompt injection.

## The other failed assertions

Three scenarios expected only a synthetic code. The model returned the correct code with an additional REVIEW_CODE prefix. The clean control without conflicting text failed in the same way. An exact-format assertion failed; successful task replacement through injection was not established. Only the done action was available, so these scenarios did not exercise arbitrary tool use.

The documented cross_origin_iframes default also differed from code. This is a documentation mismatch, not proof of cross-origin data access.

## Questions a reviewer may ask

**How do we know the request arrived?** The receiver recorded it; the conclusion does not rely on a model answer or tool status.

**Could the request be left over from a previous test?** The receiver's request list was separate for each test.

**Do the 12 passing Chrome controls fix the original failure?** No. They used a separately configured explicit proxy.

**Do the 42 passing authorization checks prove built-in Browser Use authorization?** No. They exercised server-side policy in an owned synthetic MCP application.

**What does 231 mean?** Historical logical accounting: 227 passed and four failed. It is not one fresh run or a vulnerability count.

**How should the work be presented?** As an independent, AI-assisted assessment of agent boundaries, navigation policy, and selected owned authorization fixtures, with false-positive analysis. It does not claim complete audit coverage, a successful exploit, a CVE, an accepted bounty, or general prompt-injection resistance.
