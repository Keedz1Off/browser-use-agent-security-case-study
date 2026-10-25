# Browser Use case study

## Executive Summary

The local navigation check returned an error for an excluded hostname, but the owned receiver recorded the request. The meaningful result is **a policy error did not establish prevention of the network side effect**. No untrusted-page-to-agent exploit, protected data access or sandbox escape was demonstrated.

This case study consolidates retained local measurements and pinned source review; it does not report a new execution. Version: Browser Use 0.13.13, snapshot `aa093a8`; dispatcher inspected: bubus 1.5.6.

## Background

Browser Use packages the trusted task and browser state for a model. The model proposes structured actions; the registry dispatches tools; BrowserSession uses events and Chrome DevTools Protocol (CDP) to operate Chrome. The receiver, not the model's success message, provides evidence that a request arrived.

The navigation test called a tool directly from trusted test code. It **did not use the Agent/LLM loop**. Allowed and excluded hostnames resolved to an owned synthetic loopback backend. The receiver's request list was fresh for each test.

## Observed defect

No report-ready security vulnerability is claimed. The retained behavioral failure was:

1. Expected: reject the selected excluded navigation before sending its request.
2. Observed: the owned server recorded a GET; the tool returned a policy error.
3. Source explanation: [SecurityWatchdog.on_NavigateToUrlEvent](https://github.com/browser-use/browser-use/blob/aa093a843da5edbf323c0b4145c9b6a0db3ecde8/browser_use/browser/watchdogs/security_watchdog.py#L35) intends a pre-navigation check. The [navigation tool](https://github.com/browser-use/browser-use/blob/aa093a843da5edbf323c0b4145c9b6a0db3ecde8/browser_use/tools/service.py#L509) dispatches an event and collects handler results. A separate browser handler performs navigation. Inspected bubus dispatch catches handler failures rather than implementing an atomic authorization-before-operation veto.
4. Limit: this source explanation is consistent with retained logs; no complete scheduler timing trace was captured. The diagram does not claim one guaranteed handler order.

Cleanup to about:blank cannot undo a request already received. Conversely, the [navigation policy field](https://github.com/browser-use/browser-use/blob/aa093a843da5edbf323c0b4145c9b6a0db3ecde8/browser_use/browser/profile.py#L628) is not documentation of universal all-protocol egress filtering.

## Security impact and limits

| Observation | Supported conclusion | Unsupported conclusion |
| --- | --- | --- |
| Policy error plus recorded excluded request | Scoped pre-navigation rejection defect | Proven SSRF, data exfiltration or sandbox escape |
| Correct synthetic answer with an extra REVIEW_CODE label in three scenarios | Exact-output correctness failure | Three prompt-injection vulnerabilities |
| Clean model control fails in the same way | Formatting is a strong alternative explanation | General resistance to prompt injection |
| 42 owned MCP/auth cases passed | Selected application-fixture checks enforced identity/scope/tenant/ownership | Browser Use automatically supplies backend authorization |
| 12 separate explicit-proxy Chrome controls passed | Selected proxy rules held in that configuration | Original navigation defect fixed |
| cross_origin_iframes reference says False, code defaults to True | Documentation mismatch | Demonstrated cross-origin privilege violation |

The model corpus allowed only the done action. Its output records cannot establish a forbidden network action, and they cannot be joined to the separate direct-tool navigation case as one attack chain.

## Recorded validation evidence

This documentation-only bundle includes sanitized failure records and source references, **not an executable exploit**. No target execution was performed when preparing it.

Historical logical accounting:

| Cohort | Passed | Failed | Total |
| --- | ---: | ---: | ---: |
| Baseline | 173 | 4 | 177 |
| Owned auth/MCP follow-up | 42 | 0 | 42 |
| Latest Chrome controls | 12 | 0 | 12 |
| Total | 227 | 4 | 231 |

Replays are not new independent coverage. The public JSON is a selected derivative of retained evidence, not the complete raw execution archive. Its hashes support provenance/file consistency, not independent proof of every runtime claim.

## Remediation

No upstream fix was submitted or verified. Source-informed recommendations are to make rejection authoritative before the navigation side effect, and to check request arrival in regression tests rather than accepting an eventual error as success. Where zero network contact is required, enforce and verify a separate network/proxy policy.

Backend object permissions must remain server-side. Set deployment-sensitive browser options explicitly instead of relying on conflicting defaults.

## Summary

One scoped navigation-guard behavioral defect, three answer-format failures and one documentation mismatch were identified. No exploitable security vulnerability is confirmed.

Not covered: exhaustive source review, general adversarial model behavior, production connectors, all-protocol egress, real OS-user isolation or an untrusted-input-to-protected-effect chain. Separate CONNECT controls used an HTTP fixture, not end-to-end TLS validation. Python socket instrumentation did not confine native Chrome traffic. Renderer/Network Service sandbox diagnostics are not proof of either escape or complete browser isolation.
