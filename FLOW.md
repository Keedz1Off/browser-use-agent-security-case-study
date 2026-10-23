# Architecture and flows

This describes the pinned open-source/local path, not Browser Use Cloud. Arrows show component communication, not an automatic grant of authority.

## 1. Normal agent loop

```mermaid
flowchart TD
    H["Trusted task and host configuration"] --> A["Agent and message manager"]
    W["Page DOM and screenshots: untrusted data"] --> A
    A --> L["LLM proposes structured action"]
    L --> R["Tool registry and schema validation"]
    R --> T["Tool execution"]
    T --> E["BrowserSession event bus"]
    E --> C["Navigation handler and CDP"]
    C --> B["Chrome and destination"]
    B --> W
    E --> S["SecurityWatchdog policy handler"]
    S --> X["Policy result or error"]
```

Schema validation answers whether an action has valid fields; it does not prove that its side effect is authorized. A policy-handler error is not automatically a transaction-wide cancellation.

## 2. Recorded navigation failure

```mermaid
flowchart TD
    I["Trusted local test invokes navigation tool"] --> E["Navigation event"]
    E --> P["Policy handler reports rejection"]
    E --> N["Browser handler performs navigation"]
    N --> D["Owned receiver records GET"]
    P --> O["Caller eventually receives policy error"]
```

Observed: error **and** received request. The source supports separate handlers; this is not a precise measured ordering diagram. No LLM or malicious-page chain was part of this case.

## 3. Separate answer and authorization checks

```text
Owned page text → browser state → restricted model → done
                                      ↓
                       compare exact answer with known value

Synthetic principal → MCP client → STDIO MCP server
                                   ↓
                         application authorization
                                   ↓
                         instrumented data accessor
```

The answer checks exposed an extra label, not task replacement. The auth checks belong to the owned application fixture, not an automatic Browser Use permission system.

## 4. Assessment workflow

```text
Pin source → identify boundary and expected invariant
           → positive and negative controls
           → compare tool/model output with receiver/accessor records
           → inspect alternative explanations
           → classify defect, rejected hypothesis or remaining gap
```

Sources: browser_use/agent/service.py, tools/service.py, browser/session.py, browser/watchdogs/security_watchdog.py; exact provenance in [source-pins.json](evidence/source-pins.json). Diagrams simplify components and do not claim exhaustive coverage.
