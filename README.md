# Browser Use navigation policy

In a controlled local test, the navigation tool returned a policy error, yet the owned test server recorded a request. This showed a gap between the tool's response and its network behavior.

The observation covers a direct tool call in a local setup. It establishes the request side effect under those conditions. The three other failed assertions concerned answer formatting.

## Evidence

- [Recorded observations](evidence/failures.json) · [Coverage](evidence/coverage.json)
- [Boundary matrix index](matrices/boundaries.json)
- [Navigation](matrices/NAVIGATION.json) · [Model output](matrices/MODEL-OUTPUT.json) · [App authorization](matrices/MCP-AUTH.json) · [Proxy controls](matrices/PROXY.json)

## Run the checks

[Open Case study checks in GitHub Actions](https://github.com/Keedz1Off/browser-use-agent-security-case-study/actions/workflows/checks.yml) and select **Run workflow**. CI runs four offline tests on the evidence and the trace checker’s synthetic inputs.

The run saves `check-results`. Select **CD demo** to also package the passing log, commit SHA and checksum as `verified-delivery`.

Run locally with Python 3.10 or later:

```sh
python -B -m unittest discover -s tests -v
```
