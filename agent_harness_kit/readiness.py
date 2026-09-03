"""Graph-local readiness evaluation shared by scheduling and validation."""

from __future__ import annotations

from collections.abc import Mapping


def _text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _positive(value: object) -> bool:
    return type(value) is int and value > 0


def product_approved(node: dict) -> bool:
    """Check recorded approval, not the authenticity of the human decision."""
    review = node.get("product_review")
    if not isinstance(review, dict):
        return False
    identity = review.get("approved_by")
    evidence = review.get("evidence")
    return (
        node.get("status") == "completed"
        and _positive(node.get("acceptance_revision"))
        and type(review.get("reviewed_revision")) is int
        and review["reviewed_revision"] == node["acceptance_revision"]
        and review.get("status") == "approved"
        and isinstance(identity, str) and identity.startswith("human:")
        and bool(identity[6:].strip())
        and _text(review.get("decision_ref"))
        and isinstance(evidence, list) and bool(evidence) and all(_text(ref) for ref in evidence)
    )


def acceptance_declaration_blocker(node: dict) -> str | None:
    if "acceptance_criteria" not in node:
        return None
    criteria = node["acceptance_criteria"]
    if not isinstance(criteria, list) or not criteria:
        return "completion-evidence:acceptance-criteria"
    seen: set[str] = set()
    for criterion in criteria:
        if (not isinstance(criterion, dict) or not _text(criterion.get("id"))
                or not _text(criterion.get("condition")) or criterion["id"] in seen):
            return "completion-evidence:acceptance-criteria"
        seen.add(criterion["id"])
    return None


def completion_blocker(node: dict) -> str | None:
    """Validate declared, revision-pinned evidence without inventing execution."""
    if "scope_status" in node and node["scope_status"] != "approved":
        return "completion-evidence:scope"
    if "test_strategy" in node and node["test_strategy"] not in ("tdd", "focused", "characterization", "verification-only", "not-applicable"):
        return "completion-evidence:test-strategy"
    if "runtime_smoke_required" in node and type(node["runtime_smoke_required"]) is not bool:
        return "completion-evidence:smoke-requirement"
    tdd_required = node.get("test_strategy") == "tdd"
    smoke_required = node.get("runtime_smoke_required") is True
    criteria_required = "acceptance_criteria" in node
    if blocker := acceptance_declaration_blocker(node):
        return blocker
    if not tdd_required and not smoke_required and not criteria_required:
        return None
    verification = node.get("verification")
    if (not isinstance(verification, dict)
            or not _positive(node.get("acceptance_revision"))
            or type(verification.get("spec_revision")) is not int
            or verification["spec_revision"] != node["acceptance_revision"]):
        return "completion-evidence:revision"
    if criteria_required:
        checks = verification.get("acceptance")
        if not isinstance(checks, list):
            return "completion-evidence:acceptance"
        by_id = {}
        for check in checks:
            if (not isinstance(check, dict) or not _text(check.get("criterion"))
                    or check["criterion"] in by_id):
                return "completion-evidence:acceptance"
            by_id[check["criterion"]] = check
        if set(by_id) != {criterion["id"] for criterion in node["acceptance_criteria"]}:
            return "completion-evidence:acceptance"
        for check in by_id.values():
            if (check.get("result") != "passed" or not _text(check.get("observed"))
                    or not _text(check.get("evidence"))):
                return "completion-evidence:acceptance"
    if tdd_required:
        tdd = verification.get("tdd")
        if not isinstance(tdd, dict):
            return "completion-evidence:tdd"
        red, green = tdd.get("red"), tdd.get("green")
        if not isinstance(red, dict) or not isinstance(green, dict):
            return "completion-evidence:tdd"
        if (not _text(red.get("command")) or red.get("command") != green.get("command")
                or type(red.get("exit_code")) is not int or red["exit_code"] == 0
                or red.get("failure_kind") != "behavior"
                or type(green.get("exit_code")) is not int or green["exit_code"] != 0
                or not _text(red.get("evidence")) or not _text(green.get("evidence"))):
            return "completion-evidence:tdd"
        sequence = (red.get("sequence"), tdd.get("implementation_sequence"), green.get("sequence"))
        if not all(_positive(value) for value in sequence) or not sequence[0] < sequence[1] < sequence[2]:
            return "completion-evidence:tdd-order"
    if smoke_required:
        smoke = verification.get("runtime_smoke")
        if (not isinstance(smoke, dict)
                or type(smoke.get("exit_code")) is not int or smoke["exit_code"] != 0
                or not all(_text(smoke.get(key)) for key in ("command", "evidence", "expected", "observed"))):
            return "completion-evidence:runtime-smoke"
    return None


def readiness_blocker(node: dict, nodes_by_id: Mapping[str, dict]) -> str | None:
    """Return the first unmet graph-local readiness gate for *node*, if any."""
    if "scope_status" in node and node["scope_status"] != "approved":
        return "scope:needs-discovery"
    if blocker := acceptance_declaration_blocker(node):
        return blocker
    for dependency in node.get("depends_on", []):
        dependency_id = str(dependency)
        if dependency_id not in nodes_by_id or nodes_by_id[dependency_id].get("status") != "completed":
            return f"dependency:{dependency_id}"
        if completion_blocker(nodes_by_id[dependency_id]):
            return f"completion-evidence:{dependency_id}"
    product_requires = node.get("product_requires", [])
    if not isinstance(product_requires, list):
        return "product-review:invalid-requirements"
    for required in product_requires:
        if (not _text(required) or required not in node.get("depends_on", [])
                or required not in nodes_by_id or not product_approved(nodes_by_id[required])):
            return f"product-review:{required}"
    for required in node.get("assurance_requires", []):
        required_id = str(required)
        if required_id not in nodes_by_id or nodes_by_id[required_id].get("assurance_status") != "accepted":
            return f"assurance:{required_id}"
    if node.get("checkpoint") is not None and node.get("checkpoint") != "":
        return "checkpoint"
    return None
