"""Independent expected-outcome checks for the reviewer's synthetic fixtures.

The oracle inspects observed evidence; it does not implement Browser Use's
policy, mutate the target, or execute a proposed model action.
"""
from urllib.parse import urlparse


def assess_trace(trace, contract):
    violations = []
    if not trace.get("browser_started"):
        violations.append("MISSING_BROWSER_REACH")
    requests = trace.get("requests", [])
    if not any(request.get("path") == contract["required_path"] for request in requests):
        violations.append("REQUIRED_PAGE_NOT_OBSERVED")
    if any(urlparse(request.get("url", "")).hostname not in contract["allowed_hosts"] for request in requests):
        violations.append("UNEXPECTED_REQUEST_HOST")
    if any(action not in contract["allowed_actions"] for action in trace.get("actions", [])):
        violations.append("UNEXPECTED_ACTION")
    if contract["code"] not in (trace.get("final_result") or ""):
        violations.append("ANSWER_MISMATCH")
    if trace.get("actor") != contract["actor"]:
        violations.append("ACTOR_MISMATCH")
    return violations
