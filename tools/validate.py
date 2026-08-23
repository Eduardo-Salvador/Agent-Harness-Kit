#!/usr/bin/env python3
"""Dependency-free structural validator for Agent Harness Kit."""

from __future__ import annotations

import json
import argparse
import copy
import hashlib
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_PARTS = {"work", "outputs", ".git", "__pycache__"}
READY_STATES = {"ready", "active"}
NODE_FIELDS = {
    "id", "goal", "depends_on", "status", "assignee", "reviewer",
    "write_set", "checkpoint", "task_brief", "assurance_status", "assurance_requires",
}
NODE_CONTEXT_FIELDS = {"workstream", "agent_role", "execution_context", "thread_policy", "thread_ref"}

REQUIRED_FILES = [
    "README.md", "README.pt-BR.md", "AGENTS.md", "CLAUDE.md", "LICENSE", "media/agent-harness-kit-overview-en.mp3", "media/agent-harness-kit-overview-pt-BR.mp3", "media/agent-harness-kit-overview-en.mp4", "media/agent-harness-kit-overview-pt-BR.mp4",
    "media/overview-script-en.txt", "media/overview-script-pt-BR.txt", "media/overview-audio-manifest.json",
    "OPEN-DECISIONS.md", "docs/PRODUCT.md", "docs/ARCHITECTURE.md",
    "docs/CORE-VS-LEARNING.md", "docs/DISCOVERY-INTERVIEW.md",
    "docs/PORTABILITY.md", "docs/VALIDATION.md", "docs/MODEL-ROUTING.md", "docs/EXECUTION-BUDGET.md", "docs/REVIEW-ROUNDS.md", "docs/CHANGE-INTEGRATION.md", "docs/CONTEXT-ROUTING.md", "docs/STATUS-AND-COMPLETION.md", "docs/EMBEDDED-INSTALLATION.md",
    "docs/contracts/REVIEW.md", "docs/contracts/PENDING.md", "docs/contracts/STATUS.md", "docs/contracts/EXECUTION-BUDGET.md",
    "adapters/README.md", "adapters/generic.md", "adapters/codex.md", "adapters/claude.md",
    "harness/roles/README.md", "harness/roles/discovery-interviewer.md",
    "harness/roles/orchestrator-po.md", "harness/roles/task-decomposer.md",
    "harness/roles/generic-specialist.md", "harness/roles/reviewer-integrator.md",
    "harness/roles/learning-assessor.md", "harness/roles/learning-debriefer-publisher.md",
    "harness/playbooks/README.md", "harness/playbooks/first-run.md", "harness/playbooks/status-resume.md",
    "harness/playbooks/discovery-to-graph.md", "harness/playbooks/task-dispatch.md",
    "harness/playbooks/contract-changes.md", "harness/playbooks/parallel-execution.md",
    "harness/playbooks/review-integration.md", "harness/playbooks/task-closeout.md", "harness/playbooks/model-routing.md", "harness/playbooks/context-routing.md", "harness/playbooks/frontend-screen.md", "harness/playbooks/learning-capture-publication.md",
    "harness/templates/README.md", "harness/templates/PROJECT-CONTEXT.md",
    "harness/templates/PENDING.md", "harness/templates/TASK-GRAPH.md", "harness/templates/TASK.md", "harness/templates/EXECUTION-BUDGET.md",
    "harness/templates/HANDOFF.md", "harness/templates/REVIEW.md", "harness/templates/STATUS.md",
    "harness/templates/DECISION.md", "harness/templates/LEARNING-PROFILE.md",
    "harness/templates/LEARNING-QUEUE.md", "harness/templates/MODEL-ROUTING.md",
    "harness/templates/ROOT-AGENTS-BRIDGE.md", "harness/templates/ROOT-CLAUDE-BRIDGE.md",
    "examples/development-only/README.md",
    "examples/development-plus-project-learning/README.md",
    "learning-pack/README.md", "learning-pack/01-HARNESS-BOUNDARIES.md",
    "learning-pack/02-SEVEN-COMPONENTS.md", "learning-pack/03-AGENT-LOOPS.md",
    "learning-pack/04-MEMORY.md", "learning-pack/05-CONTEXT-ENGINEERING.md",
    "learning-pack/06-ISOLATION.md", "learning-pack/07-ASSURANCE.md",
    "learning-pack/08-ORCHESTRATION.md",
    "validation/fixtures/valid/task-graph.json",
    "validation/fixtures/invalid/cycle.json",
    "validation/fixtures/invalid/missing-dependency.json",
    "validation/fixtures/invalid/write-collision.json",
    "validation/fixtures/invalid/assurance-gate.json",
    "validation/fixtures/invalid/reviewer-self-review.json",
    "validation/fixtures/invalid/path-traversal.json",
    "validation/fixtures/invalid/context-collision.json",
    "validation/status-fixtures/valid.json",
    "validation/status-fixtures/invalid/missing-progress.json",
    "validation/status-fixtures/invalid/path-traversal.json",
    "validation/status-fixtures/invalid/missing-workstreams.json",
    "validation/status-fixtures/invalid/missing-automatic-actions.json",
    "validation/status-fixtures/invalid/missing-macro-pending.json",
    "validation/status-fixtures/invalid/missing-graph-snapshot.json",
    "validation/status-fixtures/invalid/technical-transition-without-graph-update.json",
    "validation/review-fixtures/round-two-valid.json",
    "validation/review-fixtures/invalid/missing-correction-delta.json",
    "validation/budget-fixtures/valid.json",
    "validation/budget-fixtures/invalid/attempt-ceiling-bypass.json",
    "validation/budget-fixtures/invalid/no-progress-ceiling-bypass.json",
    "validation/budget-fixtures/invalid/context-ceiling-bypass.json",
    "validation/budget-fixtures/invalid/counter-rollback.json",
    "validation/budget-fixtures/invalid/lineage-reset.json",
    "validation/budget-fixtures/invalid/task-only-scope.json",
    "validation/budget-fixtures/invalid/path-traversal.json",
    "VERSION", "docs/DISTRIBUTION.md", "docs/PUBLICATION-READINESS.md", "tools/package.py", "tools/install.py", "validation/test_install.py",
    "distribution/project.json", "distribution/profiles/core.json", "distribution/profiles/core-learning.json", "distribution/profiles/full.json",
    "docs/contracts/MIGRATION-MANIFEST.md", "docs/contracts/COEXISTENCE.md", "docs/contracts/ADAPTER-BINDING.md",
    "harness/templates/MIGRATION-MANIFEST.md", "harness/templates/COEXISTENCE.md", "harness/templates/ADAPTER-BINDING.md",
    "harness/playbooks/mature-harness-adoption.md",
    "validation/host-fixtures/mature-existing/harness-adoption/MIGRATION-MANIFEST.md",
    "validation/fixtures/host-invalid/missing-backlink.json", "validation/fixtures/host-invalid/stale-snapshot.json",
    "validation/fixtures/host-invalid/silent-omission.json", "validation/fixtures/host-invalid/cutover-without-semantic-review.json",
    "docs/contracts/CAPABILITY-MANIFEST.md", "docs/contracts/RULES-MAP.md",
    "harness/templates/CAPABILITY-MANIFEST.md", "harness/templates/RULES-MAP.md",
    "validation/native-integration.json",
    ".agents/skills/first-run-discovery/SKILL.md", ".agents/skills/graph-execution/SKILL.md",
    ".agents/skills/governed-review/SKILL.md", ".agents/skills/frontend-screen/SKILL.md", ".agents/skills/project-learning/SKILL.md",
    ".claude/skills/first-run-discovery/SKILL.md", ".claude/skills/graph-execution/SKILL.md",
    ".claude/skills/governed-review/SKILL.md", ".claude/skills/frontend-screen/SKILL.md", ".claude/skills/project-learning/SKILL.md",
    ".claude/agents/discovery-interviewer.md", ".claude/agents/task-specialist.md",
    ".claude/agents/independent-reviewer.md", ".claude/agents/learning-assessor.md",
]

TEMPLATE_RULES = {
    "PROJECT-CONTEXT.md": (
        {"schema", "id", "revision", "status", "mode", "updated_at", "approved_by", "supersedes", "discovery_snapshot", "source_references", "capability_manifest", "rules_map", "pending_authority"},
        {"Project state", "Intent", "Scope", "Success measures", "Constraints", "Rules and capabilities", "Assumptions and unknowns", "Verification environment", "References"},
    ),
    "TASK-GRAPH.md": (
        {"schema", "id", "revision", "status", "project_context", "updated_at", "updated_by", "discovery_snapshot", "source_references"},
        {"Transition log"},
    ),
    "PENDING.md": (
        {"schema", "id", "revision", "status", "updated_at", "updated_by"},
        {"Human action required", "Project completion overview", "Recently resolved"},
    ),
    "TASK.md": (
        {"schema", "id", "graph", "revision", "status", "assigned_to", "reviewer", "workstream", "agent_role", "execution_context", "thread_policy", "thread_ref", "ownership_lease", "isolation", "updated_at", "capability_manifest", "rules_map", "model_tier", "model_reason", "execution_budget", "review_profile", "max_review_rounds", "assurance_gate"},
        {"Outcome", "Context to load", "Owned paths", "Constraints", "Rules to load", "Required capabilities", "Acceptance criteria", "Verification", "Exit"},
    ),
    "HANDOFF.md": (
        {"schema", "id", "task", "attempt", "status", "author", "workstream", "agent_role", "execution_context", "thread_ref", "created_at", "model_tier_used", "model_route_changes", "execution_budget"},
        {"Result", "Changes", "Change unit and authority", "Acceptance evidence", "Verification run", "Execution budget", "Discoveries and risks", "Routing and authority", "Review request", "User-facing closeout"},
    ),
    "REVIEW.md": (
        {"schema", "id", "task", "handoff", "revision", "round", "scope", "prior_review", "blocking_findings", "correction_delta", "regression_scope", "status", "reviewer", "verdict", "created_at"},
        {"Independence", "Review profile and scope", "Criterion verdicts", "Findings", "Integration recommendation", "Verification", "Next review boundary"},
    ),
    "STATUS.md": (
        {"schema", "id", "revision", "generated_at", "generated_by", "project_context", "pending_authority", "task_graph"},
        {"State revisions and synchronization", "Stage and progress", "Continuing without your action", "Human action required", "Macro pending from PENDING.md", "Technical graph from TASK-GRAPH.md", "Workstream status", "Blockers", "Next action", "Inspectable paths"},
    ),
    "DECISION.md": (
        {"schema", "id", "revision", "status", "consequence", "decided_by", "decided_at", "supersedes", "source_references"},
        {"Context", "Decision", "Options considered", "Consequences", "Affected artifacts", "Provenance"},
    ),
    "LEARNING-PROFILE.md": (
        {"schema", "id", "revision", "status", "owner", "consent_updated_at", "retention", "publication", "source_references"},
        {"Goals", "Observation consent", "Evidence by skill", "Learning queue", "Destination preferences", "Latest debrief"},
    ),
    "LEARNING-QUEUE.md": (
        {"schema", "id", "revision", "status", "profile", "updated_at", "updated_by"},
        {"Non-interference record", "Publication status"},
    ),
    "MIGRATION-MANIFEST.md": (
        {"schema", "id", "revision", "status", "source_root", "snapshot_revision", "snapshot_created_at", "semantic_review", "cutover_authorized_by"},
        {"Coverage statement", "Semantic review"},
    ),
    "COEXISTENCE.md": (
        {"schema", "id", "revision", "status", "updated_at", "approved_by"},
        {"Existing authorities", "Namespaced kit placement", "Precedence and conflicts", "Exclusions and sensitive paths", "Cutover gate", "Source references"},
    ),
    "ADAPTER-BINDING.md": (
        {"schema", "id", "revision", "adapter", "status", "reviewer"},
        {"Existing source reference", "Neutral mapping", "Precedence and permissions", "Degradation", "Provenance backlinks"},
    ),
    "CAPABILITY-MANIFEST.md": (
        {"schema", "id", "revision", "status", "updated_at", "approved_by"},
        {"Inventory notes", "Change gate"},
    ),
    "RULES-MAP.md": (
        {"schema", "id", "revision", "status", "updated_at", "approved_by"},
        {"Progressive disclosure", "Temporary context boundary", "Mature-adoption provenance"},
    ),
    "MODEL-ROUTING.md": (
        {"schema", "id", "revision", "status", "default_tier", "updated_at", "approved_by", "decision"},
        {"Tiers", "Escalation triggers", "Adapter mappings", "Dispatch record", "Context efficiency", "Authority boundary"},
    ),
    "EXECUTION-BUDGET.md": (
        {"schema", "id", "revision", "status", "updated_at", "updated_by"},
        {"Transition log"},
    ),
}

PORTUGUESE_MARKERS = re.compile(
    r"\b(pendências|decisões|usuários|aprendizado|entrega|arquitetura|"
    r"próxima fase|nome provisório|estado atual|o que é|princípios|"
    r"decisão|verificação|contexto aprovado)\b",
    re.IGNORECASE,
)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def markdown_files() -> list[Path]:
    return sorted(
        p for p in ROOT.rglob("*.md")
        if not any(part in EXCLUDED_PARTS for part in p.relative_to(ROOT).parts)
    )


def frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}
    result: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip()
    return result


def headings(text: str) -> set[str]:
    return {m.group(1).strip() for m in re.finditer(r"^#{1,6}\s+(.+?)\s*$", text, re.MULTILINE)}


def slug(value: str) -> str:
    value = re.sub(r"[^\w\- ]", "", value.lower(), flags=re.UNICODE)
    return re.sub(r"\s+", "-", value.strip())


def validate_markdown(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    if len(re.findall(r"^```", text, re.MULTILINE)) % 2:
        errors.append(f"markdown.fence: {rel(path)} has unbalanced fenced-code markers")
    for match in re.finditer(r"\[[^\]]+\]\(([^)]+)\)", text):
        target = unquote(match.group(1).strip())
        if re.match(r"^(https?://|mailto:)", target):
            continue
        path_part, _, fragment = target.partition("#")
        resolved = path if not path_part else (path.parent / path_part).resolve()
        try:
            resolved.relative_to(ROOT)
        except ValueError:
            errors.append(f"markdown.link-scope: {rel(path)} -> {target}")
            continue
        if not resolved.exists():
            errors.append(f"markdown.broken-link: {rel(path)} -> {target}")
            continue
        if fragment and resolved.suffix.lower() == ".md":
            target_headings = {slug(h) for h in headings(resolved.read_text(encoding="utf-8"))}
            if fragment.lower() not in target_headings:
                errors.append(f"markdown.missing-fragment: {rel(path)} -> {target}")
    if path.name != "README.pt-BR.md":
        scrubbed = text.replace("[Português (Brasil)](README.pt-BR.md)", "")
        marker = PORTUGUESE_MARKERS.search(scrubbed)
        if marker:
            errors.append(f"language.portuguese-marker: {rel(path)} contains '{marker.group(0)}'")
    return errors


def extract_graph(text: str) -> dict | None:
    match = re.search(r"```json\s*\n(.*?)\n```", text, re.DOTALL)
    if not match:
        return None
    return json.loads(match.group(1))


def normalize_owned_path(raw: str) -> tuple[str | None, str | None]:
    value = raw.replace("\\", "/").strip()
    if value.endswith("/**"):
        value = value[:-3]
    if not value or value.startswith("/") or re.match(r"^[A-Za-z]:", value):
        return None, "absolute-or-empty"
    parts = PurePosixPath(value).parts
    if ".." in parts:
        return None, "parent-segment"
    wildcard_at = next((i for i, part in enumerate(parts) if "*" in part or "?" in part), None)
    if wildcard_at is not None:
        parts = parts[:wildcard_at]
    normalized = "/".join(part for part in parts if part not in {"", "."}).casefold().rstrip("/")
    return normalized or None, None if normalized else "empty-prefix"


def paths_collide(left: str, right: str) -> bool:
    return left == right or left.startswith(right + "/") or right.startswith(left + "/")


def validate_graph(data: dict, source: str) -> list[str]:
    errors: list[str] = []
    nodes = data.get("nodes")
    if not isinstance(nodes, list):
        return [f"graph.shape: {source} has no nodes array"]
    by_id: dict[str, dict] = {}
    for index, node in enumerate(nodes):
        if not isinstance(node, dict):
            errors.append(f"graph.node-shape: {source} node {index} is not an object")
            continue
        missing = NODE_FIELDS - set(node)
        if missing:
            errors.append(f"graph.node-fields: {source} {node.get('id', index)} missing {sorted(missing)}")
        node_id = node.get("id")
        if not isinstance(node_id, str) or not node_id:
            errors.append(f"graph.node-id: {source} node {index} has invalid id")
        elif node_id in by_id:
            errors.append(f"graph.duplicate-id: {source} repeats {node_id}")
        else:
            by_id[node_id] = node
        present_context = NODE_CONTEXT_FIELDS & set(node)
        if present_context and present_context != NODE_CONTEXT_FIELDS:
            errors.append(f"graph.context-fields: {source} {node.get('id', index)} missing {sorted(NODE_CONTEXT_FIELDS - set(node))}")
    for node_id, node in by_id.items():
        dependencies = node.get("depends_on", [])
        if not isinstance(dependencies, list):
            errors.append(f"graph.dependencies-shape: {source} {node_id}")
            continue
        for dependency in dependencies:
            if dependency not in by_id:
                errors.append(f"graph.missing-dependency: {source} {node_id} -> {dependency}")
        write_set = node.get("write_set", [])
        if not isinstance(write_set, list) or not write_set:
            errors.append(f"graph.write-set: {source} {node_id} must own at least one path")
        for owned in write_set if isinstance(write_set, list) else []:
            normalized, reason = normalize_owned_path(str(owned))
            if reason:
                errors.append(f"graph.invalid-path: {source} {node_id} {owned!r} ({reason})")
        if node.get("assignee") not in {None, "unassigned"} and node.get("assignee") == node.get("reviewer"):
            errors.append(f"graph.reviewer-independence: {source} {node_id}")
        if NODE_CONTEXT_FIELDS <= set(node):
            if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", str(node.get("workstream", ""))):
                errors.append(f"graph.workstream: {source} {node_id}")
            if not str(node.get("agent_role", "")).strip():
                errors.append(f"graph.agent-role: {source} {node_id}")
            if node.get("execution_context") not in {"isolated", "shared-integration", "sequential-fallback"}:
                errors.append(f"graph.execution-context: {source} {node_id}")
            if node.get("thread_policy") not in {"create-per-task", "reuse-workstream", "manual", "sequential-fallback"}:
                errors.append(f"graph.thread-policy: {source} {node_id}")
            if not str(node.get("thread_ref", "")).strip():
                errors.append(f"graph.thread-ref: {source} {node_id}")
        assurance_status = node.get("assurance_status")
        if assurance_status not in {"not-required", "pending", "accepted", "changes-requested", "blocked"}:
            errors.append(f"graph.assurance-status: {source} {node_id}")
        assurance_requires = node.get("assurance_requires")
        if not isinstance(assurance_requires, list):
            errors.append(f"graph.assurance-requires-shape: {source} {node_id}")
        else:
            for required_id in assurance_requires:
                if required_id not in by_id:
                    errors.append(f"graph.assurance-missing: {source} {node_id} -> {required_id}")

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node_id: str) -> bool:
        if node_id in visiting:
            return True
        if node_id in visited:
            return False
        visiting.add(node_id)
        for dependency in by_id[node_id].get("depends_on", []):
            if dependency in by_id and visit(dependency):
                return True
        visiting.remove(node_id)
        visited.add(node_id)
        return False

    if any(visit(node_id) for node_id in by_id if node_id not in visited):
        errors.append(f"graph.cycle: {source}")

    for node_id, node in by_id.items():
        if node.get("status") in READY_STATES:
            for required_id in node.get("assurance_requires", []):
                required = by_id.get(required_id)
                if required and required.get("assurance_status") != "accepted":
                    errors.append(f"graph.assurance-gate: {source} {node_id} waits for accepted assurance of {required_id}")

    concurrent = [node for node in by_id.values() if node.get("status") in READY_STATES]
    for index, left in enumerate(concurrent):
        left_paths = [normalize_owned_path(str(p))[0] for p in left.get("write_set", [])]
        for right in concurrent[index + 1:]:
            right_paths = [normalize_owned_path(str(p))[0] for p in right.get("write_set", [])]
            if any(a and b and paths_collide(a, b) for a in left_paths for b in right_paths):
                errors.append(f"graph.write-collision: {source} {left['id']} <> {right['id']}")
            left_ref, right_ref = left.get("thread_ref"), right.get("thread_ref")
            if (left_ref not in {None, "pending", "manual", "sequential"} and left_ref == right_ref
                    and left.get("workstream") != right.get("workstream")):
                errors.append(f"graph.context-collision: {source} {left['id']} <> {right['id']}")
    return errors


def validate_templates() -> list[str]:
    errors: list[str] = []
    template_root = ROOT / "harness" / "templates"
    for name, (required_header, required_sections) in TEMPLATE_RULES.items():
        path = template_root / name
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        missing_header = required_header - set(frontmatter(text))
        missing_sections = required_sections - headings(text)
        if missing_header:
            errors.append(f"template.header: {rel(path)} missing {sorted(missing_header)}")
        if missing_sections:
            errors.append(f"template.section: {rel(path)} missing {sorted(missing_sections)}")
    return errors


def validate_fixtures() -> list[str]:
    errors: list[str] = []
    fixture_root = ROOT / "validation" / "fixtures"
    for path in sorted(fixture_root.rglob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        actual = validate_graph(data, rel(path))
        actual_codes = {item.split(":", 1)[0] for item in actual}
        expected = set(data.get("expected_errors", []))
        if path.parent.name == "valid" and actual:
            errors.append(f"fixture.valid-failed: {rel(path)} -> {actual}")
        elif path.parent.name == "invalid" and not expected:
            errors.append(f"fixture.no-expectation: {rel(path)}")
        elif path.parent.name == "invalid" and not expected.issubset(actual_codes):
            errors.append(f"fixture.expected-error: {rel(path)} expected {sorted(expected)}, got {sorted(actual_codes)}")
    return errors


STATUS_FIELDS = {"stage", "progress", "automatic_actions", "blockers", "next_action", "inspectable_paths", "human_pending", "macro_pending", "state_revisions", "technical_transition", "graph_snapshot", "workstreams"}


def validate_status_payload(data: dict, source: str) -> list[str]:
    """Validate the machine-readable payload behind a user-facing status update."""
    errors: list[str] = []
    if not isinstance(data, dict):
        return [f"status.shape: {source}"]
    for field in sorted(STATUS_FIELDS):
        if field not in data or data[field] is None or data[field] == "":
            errors.append(f"status.missing-field: {source} {field}")
    blockers = data.get("blockers")
    if not isinstance(blockers, list):
        errors.append(f"status.blockers-shape: {source}")
    paths = data.get("inspectable_paths")
    if not isinstance(paths, list) or not paths:
        errors.append(f"status.inspectable-path: {source}")
    else:
        for value in paths:
            normalized, reason = normalize_owned_path(str(value))
            if reason or not normalized:
                errors.append(f"status.inspectable-path: {source} {value!r}")
    human_pending = data.get("human_pending")
    if not isinstance(human_pending, list):
        errors.append(f"status.human-pending-shape: {source}")
    else:
        for index, item in enumerate(human_pending):
            if not isinstance(item, dict) or not item.get("action") or not item.get("source"):
                errors.append(f"status.human-source: {source} item {index}")
    if not isinstance(data.get("automatic_actions"), list):
        errors.append(f"status.automatic-actions-shape: {source}")
    if not isinstance(data.get("macro_pending"), list):
        errors.append(f"status.macro-pending-shape: {source}")
    graph_snapshot = data.get("graph_snapshot")
    graph_fields = {"active_nodes", "ready_nodes", "blocked_nodes"}
    if not isinstance(graph_snapshot, dict) or graph_fields - set(graph_snapshot):
        errors.append(f"status.graph-snapshot-fields: {source}")
    elif any(not isinstance(graph_snapshot[field], list) for field in graph_fields):
        errors.append(f"status.graph-snapshot-shape: {source}")
    state_revisions = data.get("state_revisions")
    if not isinstance(state_revisions, dict) or not state_revisions.get("pending") or not state_revisions.get("task_graph"):
        errors.append(f"status.state-revisions: {source}")
    transition = data.get("technical_transition")
    transition_fields = {"occurred", "graph_updated", "graph_revision", "node_changes"}
    if not isinstance(transition, dict) or transition_fields - set(transition):
        errors.append(f"status.graph-transition-shape: {source}")
    elif transition.get("occurred") is True and (
        transition.get("graph_updated") is not True
        or not isinstance(transition.get("node_changes"), list)
        or not transition.get("node_changes")
        or not isinstance(state_revisions, dict)
        or transition.get("graph_revision") != state_revisions.get("task_graph")
    ):
        errors.append(f"status.graph-transition: {source}")
    workstreams = data.get("workstreams")
    if not isinstance(workstreams, list) or not workstreams:
        errors.append(f"status.workstreams-shape: {source}")
    else:
        required = {"area", "progress", "human_pending", "technical_pending", "active_context", "blockers", "next_action"}
        for index, item in enumerate(workstreams):
            if not isinstance(item, dict) or required - set(item):
                errors.append(f"status.workstream-fields: {source} item {index}")
    return errors


def validate_status_fixtures() -> list[str]:
    """Execute hostile mutations against one known-good status payload."""
    errors: list[str] = []
    root = ROOT / "validation" / "status-fixtures"
    try:
        baseline = json.loads((root / "valid.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"status.fixture-baseline: {exc}"]
    baseline_errors = validate_status_payload(baseline, "validation/status-fixtures/valid.json")
    if baseline_errors:
        errors.append(f"status.fixture-valid-failed: {baseline_errors}")
    for path in sorted((root / "invalid").glob("*.json")):
        scenario = json.loads(path.read_text(encoding="utf-8"))
        candidate = copy.deepcopy(baseline)
        mutation = scenario.get("mutation", {})
        field = mutation.get("field")
        if mutation.get("action") == "remove":
            candidate.pop(field, None)
        elif mutation.get("action") == "set":
            candidate[field] = mutation.get("value")
        else:
            errors.append(f"status.fixture-mutation: {rel(path)}")
            continue
        actual_codes = {item.split(":", 1)[0] for item in validate_status_payload(candidate, rel(path))}
        expected = set(scenario.get("expected_errors", []))
        if not expected or not expected.issubset(actual_codes):
            errors.append(f"status.fixture-expected-error: {rel(path)} expected {sorted(expected)}, got {sorted(actual_codes)}")
    return errors


def validate_round_two_payload(data: dict, source: str) -> list[str]:
    errors: list[str] = []
    if data.get("round") != 2 or data.get("scope") != "focused-rereview":
        errors.append(f"review.fixture-scope: {source}")
    for field in ("prior_review", "blocking_findings", "correction_delta", "regression_scope"):
        value = data.get(field)
        if value is None or value == "" or value == "none":
            errors.append(f"review.focused-evidence: {source} {field}")
    return errors


def validate_review_fixtures() -> list[str]:
    """Prove that hostile removal of a round-two audit boundary is rejected."""
    errors: list[str] = []
    root = ROOT / "validation" / "review-fixtures"
    try:
        baseline = json.loads((root / "round-two-valid.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"review.fixture-baseline: {exc}"]
    if actual := validate_round_two_payload(baseline, "validation/review-fixtures/round-two-valid.json"):
        errors.append(f"review.fixture-valid-failed: {actual}")
    for path in sorted((root / "invalid").glob("*.json")):
        scenario = json.loads(path.read_text(encoding="utf-8"))
        candidate = copy.deepcopy(baseline)
        mutation = scenario.get("mutation", {})
        if mutation.get("action") == "remove":
            candidate.pop(mutation.get("field"), None)
        else:
            errors.append(f"review.fixture-mutation: {rel(path)}")
            continue
        actual_codes = {item.split(":", 1)[0] for item in validate_round_two_payload(candidate, rel(path))}
        expected = set(scenario.get("expected_errors", []))
        if not expected or not expected.issubset(actual_codes):
            errors.append(f"review.fixture-expected-error: {rel(path)} expected {sorted(expected)}, got {sorted(actual_codes)}")
    return errors


BUDGET_COUNTERS = {
    "implementation_attempts": "max_implementation_attempts",
    "consecutive_no_progress_cycles": "max_consecutive_no_progress_cycles",
    "context_expansions": "max_context_expansions",
}


def validate_budget_payload(data: dict, source: str) -> list[str]:
    """Validate one executable goal-lineage budget state."""
    errors: list[str] = []
    if not isinstance(data, dict) or data.get("schema") != "harness.execution-budget/v1":
        return [f"budget.shape: {source}"]
    for field in ("task", "goal_lineage", "reason"):
        if not isinstance(data.get(field), str) or not data[field].strip():
            errors.append(f"budget.missing-field: {source} {field}")
    if data.get("counter_scope") != "goal-lineage":
        errors.append(f"budget.counter-scope: {source}")
    previous_lineage = data.get("previous_goal_lineage")
    if data.get("decision") not in {"continue", "stop-and-replan"}:
        errors.append(f"budget.decision: {source}")
    if data.get("token_measurement") not in {"unavailable", "advisory", "host-reported"}:
        errors.append(f"budget.token-measurement: {source}")

    limits = data.get("limits")
    usage = data.get("usage")
    previous = data.get("previous_usage")
    if not isinstance(limits, dict) or not isinstance(usage, dict):
        errors.append(f"budget.counter-shape: {source}")
        return errors
    if previous is not None and not isinstance(previous, dict):
        errors.append(f"budget.counter-shape: {source} previous_usage")
        previous = None
    if isinstance(previous, dict) and previous_lineage != data.get("goal_lineage"):
        errors.append(f"budget.lineage-reset: {source}")
    elif previous is None and previous_lineage is not None:
        errors.append(f"budget.lineage-shape: {source}")

    ceiling_reached = False
    for usage_field, limit_field in BUDGET_COUNTERS.items():
        limit = limits.get(limit_field)
        current = usage.get(usage_field)
        if not isinstance(limit, int) or isinstance(limit, bool) or limit <= 0:
            errors.append(f"budget.limit: {source} {limit_field}")
            continue
        if not isinstance(current, int) or isinstance(current, bool) or current < 0:
            errors.append(f"budget.usage: {source} {usage_field}")
            continue
        if isinstance(previous, dict):
            prior = previous.get(usage_field)
            if not isinstance(prior, int) or isinstance(prior, bool) or prior < 0:
                errors.append(f"budget.usage: {source} previous_usage.{usage_field}")
            elif current < prior:
                errors.append(f"budget.counter-rollback: {source} {usage_field}")
        if current >= limit:
            ceiling_reached = True
    if ceiling_reached and data.get("decision") != "stop-and-replan":
        errors.append(f"budget.ceiling-bypass: {source}")

    paths = data.get("evidence_paths")
    if not isinstance(paths, list) or not paths:
        errors.append(f"budget.evidence-path: {source}")
    else:
        for value in paths:
            normalized, reason = normalize_owned_path(str(value))
            if reason or not normalized:
                errors.append(f"budget.evidence-path: {source} {value!r}")
    return errors


def set_nested_value(data: dict, dotted_path: str, value: object) -> bool:
    parts = dotted_path.split(".")
    target = data
    for part in parts[:-1]:
        candidate = target.get(part)
        if not isinstance(candidate, dict):
            return False
        target = candidate
    target[parts[-1]] = value
    return True


def validate_budget_fixtures() -> list[str]:
    """Execute hostile budget mutations against one known-good state."""
    errors: list[str] = []
    root = ROOT / "validation" / "budget-fixtures"
    try:
        baseline = json.loads((root / "valid.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"budget.fixture-baseline: {exc}"]
    if actual := validate_budget_payload(baseline, "validation/budget-fixtures/valid.json"):
        errors.append(f"budget.fixture-valid-failed: {actual}")
    template_path = ROOT / "harness" / "templates" / "EXECUTION-BUDGET.md"
    if template_path.is_file():
        try:
            template_payload = extract_graph(template_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"budget.template-json: {exc}")
        else:
            if template_payload is None:
                errors.append("budget.template-json: missing executable JSON block")
            elif actual := validate_budget_payload(template_payload, rel(template_path)):
                errors.append(f"budget.template-invalid: {actual}")
    for path in sorted((root / "invalid").glob("*.json")):
        scenario = json.loads(path.read_text(encoding="utf-8"))
        candidate = copy.deepcopy(baseline)
        mutation = scenario.get("mutation", {})
        if mutation.get("action") != "set" or not set_nested_value(
            candidate, str(mutation.get("path", "")), mutation.get("value")
        ):
            errors.append(f"budget.fixture-mutation: {rel(path)}")
            continue
        actual_codes = {item.split(":", 1)[0] for item in validate_budget_payload(candidate, rel(path))}
        expected = set(scenario.get("expected_errors", []))
        if not expected or not expected.issubset(actual_codes):
            errors.append(f"budget.fixture-expected-error: {rel(path)} expected {sorted(expected)}, got {sorted(actual_codes)}")
    return errors


def validate_runtime_budgets() -> list[str]:
    """Validate discovered runtime budget artifacts in root or embedded host state."""
    errors: list[str] = []
    roots = [ROOT / "harness-state"]
    if (ROOT / "PACKAGE-MANIFEST.json").is_file():
        roots.append(ROOT.parent / "harness-state")
    seen: set[Path] = set()
    for state_root in roots:
        if not state_root.is_dir():
            continue
        for path in sorted(state_root.rglob("*.md")):
            resolved = path.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            text = path.read_text(encoding="utf-8")
            if frontmatter(text).get("schema") != "harness.execution-budget/v1":
                continue
            try:
                payload = extract_graph(text)
            except json.JSONDecodeError as exc:
                errors.append(f"budget.runtime-json: {path}: {exc}")
                continue
            if payload is None:
                errors.append(f"budget.runtime-json: {path}: missing executable JSON block")
            else:
                errors.extend(validate_budget_payload(payload, str(path)))
    return errors


MIGRATION_CLASSIFICATIONS = {
    "migrated", "retained-as-authoritative-reference",
    "intentionally-duplicated-during-transition", "unresolved",
}
MATERIAL_TYPES = {
    "rule", "decision", "constraint", "pending-item", "role-responsibility",
    "learning-reference", "verification-source", "generated-source-exclusion",
    "secret-boundary",
}


def safe_host_path(host_root: Path, relative: str) -> Path | None:
    candidate = (host_root / relative).resolve()
    try:
        candidate.relative_to(host_root.resolve())
    except ValueError:
        return None
    return candidate


def file_identity(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def validate_migration_data(host_root: Path, header: dict[str, str], data: dict, source: str) -> list[str]:
    errors: list[str] = []
    required_header = {
        "schema", "id", "revision", "status", "source_root", "snapshot_revision",
        "snapshot_created_at", "semantic_review", "cutover_authorized_by",
    }
    if header.get("schema") != "harness.migration-manifest/v1":
        errors.append(f"migration.schema: {source}")
    missing_header = required_header - set(header)
    if missing_header:
        errors.append(f"migration.header: {source} missing {sorted(missing_header)}")
    selectors = data.get("source_selectors")
    items = data.get("items")
    if not isinstance(selectors, list) or not isinstance(items, list):
        return errors + [f"migration.shape: {source}"]

    covered_sources: set[str] = set()
    item_ids: set[str] = set()
    for item in items:
        if not isinstance(item, dict):
            errors.append(f"migration.item-shape: {source}")
            continue
        required = {
            "material_id", "material_type", "source", "source_identity", "classification",
            "destinations", "backlinks", "unresolved_owner", "unresolved_checkpoint",
            "semantic_review", "reviewed_by",
        }
        missing = required - set(item)
        if missing:
            errors.append(f"migration.item-fields: {source} missing {sorted(missing)}")
            continue
        material_id = item["material_id"]
        if material_id in item_ids:
            errors.append(f"migration.duplicate-id: {source} {material_id}")
        item_ids.add(material_id)
        if item["material_type"] not in MATERIAL_TYPES:
            errors.append(f"migration.material-type: {source} {material_id}")
        if item["classification"] not in MIGRATION_CLASSIFICATIONS:
            errors.append(f"migration.classification: {source} {material_id}")
        if item["classification"] == "unresolved" and (not item["unresolved_owner"] or not item["unresolved_checkpoint"]):
            errors.append(f"migration.unresolved-gate: {source} {material_id}")
        source_path = safe_host_path(host_root, str(item["source"]))
        if source_path is None:
            errors.append(f"migration.path-scope: {source} {material_id}")
            continue
        covered_sources.add(Path(item["source"]).as_posix())
        if not source_path.is_file():
            errors.append(f"migration.source-missing: {source} {material_id}")
        elif file_identity(source_path) != item["source_identity"]:
            errors.append(f"migration.source-drift: {source} {material_id}")
        for destination in item["destinations"]:
            destination_path = safe_host_path(host_root, str(destination))
            if destination_path is None or not destination_path.is_file():
                errors.append(f"migration.destination-missing: {source} {material_id} -> {destination}")
        for backlink in item["backlinks"]:
            backlink_path = safe_host_path(host_root, str(backlink))
            if backlink_path is None or not backlink_path.is_file():
                errors.append(f"migration.backlink-missing: {source} {material_id} -> {backlink}")
            elif str(item["source"]) not in backlink_path.read_text(encoding="utf-8"):
                errors.append(f"migration.backlink-content: {source} {material_id} -> {backlink}")
        if not item["destinations"] or not item["backlinks"]:
            errors.append(f"migration.provenance: {source} {material_id}")
        if item["semantic_review"] == "approved" and not str(item["reviewed_by"] or "").startswith("human:"):
            errors.append(f"migration.semantic-reviewer: {source} {material_id}")

    expanded_all: set[str] = set()
    for selector in selectors:
        if not isinstance(selector, dict) or set(selector) < {"selector", "expanded_sources"}:
            errors.append(f"migration.selector-shape: {source}")
            continue
        pattern = str(selector["selector"])
        actual = sorted(
            path.relative_to(host_root).as_posix()
            for path in host_root.glob(pattern) if path.is_file()
        )
        expected = sorted(str(path).replace("\\", "/") for path in selector["expanded_sources"])
        if actual != expected:
            errors.append(f"migration.selector-drift: {source} {pattern}")
        expanded_all.update(expected)
    omitted = expanded_all - covered_sources
    if omitted:
        errors.append(f"migration.silent-omission: {source} {sorted(omitted)}")

    if header.get("status") == "cutover-approved":
        if not str(header.get("cutover_authorized_by", "")).startswith("human:"):
            errors.append(f"migration.cutover-authority: {source}")
        for item in items:
            if item.get("classification") in {"retained-as-authoritative-reference", "intentionally-duplicated-during-transition"}:
                if item.get("semantic_review") != "approved" or not str(item.get("reviewed_by") or "").startswith("human:"):
                    errors.append(f"migration.cutover-semantic-review: {source} {item.get('material_id')}")
    return errors


def load_migration_manifest(path: Path) -> tuple[dict[str, str], dict]:
    text = path.read_text(encoding="utf-8")
    data = extract_graph(text)
    if data is None:
        raise ValueError("missing JSON block")
    return frontmatter(text), data


def validate_host_integration(host_root: Path, manifest_path: Path) -> list[str]:
    if not host_root.is_dir():
        return [f"migration.host-root: not a directory: {host_root}"]
    if not manifest_path.is_absolute():
        manifest_path = host_root / manifest_path
    if not manifest_path.is_file():
        return [f"migration.manifest-missing: {manifest_path}"]
    try:
        header, data = load_migration_manifest(manifest_path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return [f"migration.manifest-read: {exc}"]
    errors = validate_migration_data(host_root.resolve(), header, data, str(manifest_path))
    context_path = host_root / "harness-state" / "PROJECT-CONTEXT.md"
    if context_path.is_file():
        context_header = frontmatter(context_path.read_text(encoding="utf-8"))
        if context_header.get("status") == "approved":
            if context_header.get("discovery_snapshot") != header.get("snapshot_revision"):
                errors.append("migration.context-snapshot: approved context does not pin the current discovery snapshot")
            expected_reference = f"{header.get('id')}@{header.get('revision')}"
            if context_header.get("source_references") != expected_reference:
                errors.append("migration.context-provenance: approved context does not pin the migration manifest")
            if any(error.startswith(("migration.source-drift:", "migration.selector-drift:")) for error in errors):
                errors.append("migration.approval-stale: approved context rests on a stale discovery snapshot")
    return errors


def validate_host_fixtures() -> list[str]:
    errors: list[str] = []
    host_root = ROOT / "validation" / "host-fixtures" / "mature-existing"
    manifest_path = host_root / "harness-adoption" / "MIGRATION-MANIFEST.md"
    valid_errors = validate_host_integration(host_root, manifest_path)
    if valid_errors:
        errors.append(f"fixture.host-valid-failed: {valid_errors}")
        return errors
    header, base_data = load_migration_manifest(manifest_path)
    for scenario_path in sorted((ROOT / "validation" / "fixtures" / "host-invalid").glob("*.json")):
        scenario = json.loads(scenario_path.read_text(encoding="utf-8"))
        mutated = copy.deepcopy(base_data)
        mutated_header = dict(header)
        if "header_mutation" in scenario:
            mutated_header.update(scenario["header_mutation"])
        if "mutation" in scenario:
            mutation = scenario["mutation"]
            if mutation.get("action") == "remove":
                mutated["items"] = [item for item in mutated["items"] if item["material_id"] != mutation["material_id"]]
            else:
                target = next(item for item in mutated["items"] if item["material_id"] == mutation["material_id"])
                target[mutation["field"]] = mutation["value"]
        actual = validate_migration_data(host_root, mutated_header, mutated, rel(scenario_path))
        codes = {item.split(":", 1)[0] for item in actual}
        expected = set(scenario["expected_errors"])
        if not expected.issubset(codes):
            errors.append(f"fixture.host-invalid: {rel(scenario_path)} expected {sorted(expected)}, got {sorted(codes)}")
    return errors


def validate_native_integration() -> list[str]:
    errors: list[str] = []
    fixture_path = ROOT / "validation" / "native-integration.json"
    try:
        fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"native.fixture: {exc}"]
    if fixture.get("schema") != "agent-harness-kit.native-integration/v1":
        errors.append("native.fixture-schema: validation/native-integration.json")

    codex = fixture.get("codex", {})
    claude = fixture.get("claude", {})
    package_profile = None
    package_path = ROOT / "PACKAGE-MANIFEST.json"
    if package_path.is_file():
        try:
            package_profile = json.loads(package_path.read_text(encoding="utf-8")).get("profile")
        except (OSError, json.JSONDecodeError):
            pass
    learning_declared = [] if package_profile == "core" else [
        codex.get("learning_extension"), claude.get("learning_extension"), claude.get("learning_agent")
    ]
    declared = [
        codex.get("entrypoint"), codex.get("adapter"),
        claude.get("entrypoint"), claude.get("adapter"),
        *learning_declared, *codex.get("core_skills", []),
        *claude.get("core_skills", []), *claude.get("core_agents", []),
    ]
    for item in declared:
        if not isinstance(item, str) or not (ROOT / item).is_file():
            errors.append(f"native.required-file: {item!r}")

    agents_path = ROOT / "AGENTS.md"
    claude_path = ROOT / "CLAUDE.md"
    if agents_path.is_file() and claude_path.is_file():
        agents_text = agents_path.read_text(encoding="utf-8")
        claude_text = claude_path.read_text(encoding="utf-8")
        if not claude_text.startswith("@AGENTS.md\n"):
            errors.append("native.claude-import: CLAUDE.md must start with @AGENTS.md")
        if len(claude_text) > 1600 or len(claude_text) > len(agents_text) * 0.65:
            errors.append("native.context-duplication: CLAUDE.md must remain a thin compatibility entry")
        shared = str(fixture.get("shared_context", ""))
        if shared not in agents_text or shared not in (ROOT / "adapters" / "claude.md").read_text(encoding="utf-8"):
            errors.append("native.shared-core: both routes must name the neutral project-context path")
        if ".agents/skills/" not in agents_text or "adapters/codex.md" not in agents_text:
            errors.append("native.codex-routing: AGENTS.md does not route Codex")
        if ".claude/skills/" not in claude_text or "adapters/claude.md" not in claude_text:
            errors.append("native.claude-routing: CLAUDE.md does not route Claude Code")

        if "frontend-screen" not in agents_text or "harness/playbooks/frontend-screen.md" not in agents_text:
            errors.append("native.frontend-routing: AGENTS.md must route screen requests through the frontend workflow")
        learning_tokens = ("delivery+learning", "learning-profile", "destination")
        if any(token not in agents_text.lower() for token in learning_tokens):
            errors.append("native.learning-activation-routing: AGENTS.md must recognize learning requests and collect a note destination")

    frontend_playbook = ROOT / "harness" / "playbooks" / "frontend-screen.md"
    if frontend_playbook.is_file():
        frontend_text = frontend_playbook.read_text(encoding="utf-8")
        for capability in ("design-taste-frontend", "imagegen-frontend-web", "imagegen", "image-to-code"):
            if capability not in frontend_text:
                errors.append(f"native.frontend-capability: frontend playbook does not name {capability}")
        frontend_lower = frontend_text.lower()
        for token in ("approved-screen implementation route", "primary coding skill", "desktop and mobile", "temporary photographs", "never frontend code"):
            if token not in frontend_lower:
                errors.append(f"native.frontend-approved-screen-route: frontend playbook lacks {token!r}")
    for item in (".agents/skills/frontend-screen/SKILL.md", ".claude/skills/frontend-screen/SKILL.md"):
        path = ROOT / item
        if path.is_file():
            skill_text = path.read_text(encoding="utf-8")
            if "harness/playbooks/frontend-screen.md" not in skill_text:
                errors.append(f"native.frontend-playbook-routing: {item}")
            for token in ("image-to-code` the primary coding skill", "frontend-screen` responsible for desktop/mobile", "imagegen` only for temporary photographs"):
                if token not in skill_text:
                    errors.append(f"native.frontend-approved-screen-skill: {item} lacks {token!r}")

    learning_playbook = ROOT / "harness" / "playbooks" / "learning-capture-publication.md"
    if learning_playbook.is_file():
        learning_text = learning_playbook.read_text(encoding="utf-8").lower()
        for token in ("obsidian", "notion", "local", "capability manifest", "destination preferences"):
            if token not in learning_text:
                errors.append(f"native.learning-destination-routing: learning playbook does not cover {token}")
        for token in ("hard activation and write gate", "do not create a note", "do not infer `docs/`", "which connector/mcp", "explicit approved fallback destination"):
            if token not in learning_text:
                errors.append(f"native.learning-destination-gate: learning playbook lacks {token!r}")
    for item in (".agents/skills/project-learning/SKILL.md", ".claude/skills/project-learning/SKILL.md"):
        path = ROOT / item
        if path.is_file():
            skill_text = path.read_text(encoding="utf-8").lower()
            for token in ("destination confirmation is mandatory", "do not create files/folders", "which connector/mcp", "exact page/database"):
                if token not in skill_text:
                    errors.append(f"native.learning-skill-destination-gate: {item} lacks {token!r}")

    first_run_playbook = ROOT / "harness" / "playbooks" / "first-run.md"
    if first_run_playbook.is_file():
        first_run_text = first_run_playbook.read_text(encoding="utf-8").lower()
        for token in ("first-response handshake", "agent harness kit is active", "organizes project context, pending work, and verifiable execution", "highest-leverage unanswered", "empty or effectively empty", "do not propose a product", "localize the wording"):
            if token not in first_run_text:
                errors.append(f"native.first-run-handshake: first-run playbook lacks {token!r}")
    for item in (".agents/skills/first-run-discovery/SKILL.md", ".claude/skills/first-run-discovery/SKILL.md"):
        path = ROOT / item
        if path.is_file():
            skill_text = path.read_text(encoding="utf-8").lower()
            for token in ("agent harness kit is active", "highest-leverage unanswered", "empty", "do not propose"):
                if token not in skill_text:
                    errors.append(f"native.first-run-handshake-skill: {item} lacks {token!r}")

    context_playbook = ROOT / "harness" / "playbooks" / "context-routing.md"
    context_doc = ROOT / "docs" / "CONTEXT-ROUTING.md"
    if context_playbook.is_file() and context_doc.is_file():
        context_text = context_playbook.read_text(encoding="utf-8") + context_doc.read_text(encoding="utf-8")
        for token in ("workstream", "create_thread", "spawn_subagent", "thread_ref", "sequential-fallback"):
            if token not in context_text:
                errors.append(f"native.context-routing: context policy does not cover {token}")
        for adapter_name in ("generic.md", "codex.md", "claude.md"):
            adapter_text = (ROOT / "adapters" / adapter_name).read_text(encoding="utf-8")
            if "create_thread" not in adapter_text and "thread lifecycle" not in adapter_text.lower():
                errors.append(f"native.context-adapter: adapters/{adapter_name} lacks thread capability mapping")

    bounded_review_surfaces = (
        "AGENTS.md",
        "CLAUDE.md",
        "adapters/codex.md",
        "adapters/claude.md",
        ".agents/skills/graph-execution/SKILL.md",
        ".claude/skills/graph-execution/SKILL.md",
        ".agents/skills/governed-review/SKILL.md",
        ".claude/skills/governed-review/SKILL.md",
        ".claude/agents/independent-reviewer.md",
        "harness/roles/orchestrator-po.md",
        "harness/roles/reviewer-integrator.md",
    )
    for item in bounded_review_surfaces:
        path = ROOT / item
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            if "REVIEW-ROUNDS.md" not in text and "max_review_rounds" not in text and "two-round review budget" not in text and "bounded review profile" not in text:
                errors.append(f"native.bounded-review-routing: {item} does not route to the shared review budget")

    status_completion_surfaces = (
        "AGENTS.md",
        "CLAUDE.md",
        "adapters/codex.md",
        "adapters/claude.md",
        ".agents/skills/graph-execution/SKILL.md",
        ".claude/skills/graph-execution/SKILL.md",
    )
    for item in status_completion_surfaces:
        path = ROOT / item
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        required = ("PENDING.md", "TASK-GRAPH.md", "STATUS-AND-COMPLETION.md")
        if any(token not in text for token in required):
            errors.append(f"native.state-authority-routing: {item} must route pending, graph, and completion policy")
        lowered = text.lower()
        if "completed" not in lowered or "non-block" not in lowered:
            errors.append(f"native.nonblocking-closeout: {item} must complete passing tasks and keep assurance non-blocking")

    graph_sync_surfaces = (
        "AGENTS.md", "adapters/codex.md", "adapters/claude.md",
        ".agents/skills/graph-execution/SKILL.md", ".claude/skills/graph-execution/SKILL.md",
        "harness/playbooks/task-dispatch.md", "harness/playbooks/task-closeout.md",
        "harness/roles/orchestrator-po.md",
    )
    for item in graph_sync_surfaces:
        path = ROOT / item
        if path.is_file():
            sync_text = path.read_text(encoding="utf-8").lower()
            if "task-graph.md" not in sync_text or "pending.md" not in sync_text or "technical" not in sync_text:
                errors.append(f"native.graph-sync-routing: {item} must persist technical events in the graph, not pending")

    skill_paths = [ROOT / item for item in declared if isinstance(item, str) and item.endswith("/SKILL.md")]
    for path in skill_paths:
        if not path.is_file():
            continue
        header = frontmatter(path.read_text(encoding="utf-8"))
        expected_name = path.parent.name
        if header.get("name") != expected_name or not header.get("description"):
            errors.append(f"native.skill-frontmatter: {rel(path)}")

    allowed_claude_tools = {"Read", "Grep", "Glob", "Edit", "Write"}
    for item in claude.get("core_agents", []) + [claude.get("learning_agent")]:
        if not isinstance(item, str) or not (ROOT / item).is_file():
            continue
        path = ROOT / item
        header = frontmatter(path.read_text(encoding="utf-8"))
        if header.get("name") != path.stem or not header.get("description") or not header.get("tools"):
            errors.append(f"native.claude-agent-frontmatter: {rel(path)}")
            continue
        tools = {tool.strip() for tool in header["tools"].split(",")}
        if not tools <= allowed_claude_tools:
            errors.append(f"native.unsafe-agent-tools: {rel(path)} has {sorted(tools - allowed_claude_tools)}")

    for item in fixture.get("forbidden_live_configuration", []):
        if (ROOT / item).exists():
            errors.append(f"native.unsafe-live-config: {item}")
    for adapter in (ROOT / "adapters" / "codex.md", ROOT / "adapters" / "claude.md"):
        if adapter.is_file() and re.search(r"\bstub\b", adapter.read_text(encoding="utf-8"), re.IGNORECASE):
            errors.append(f"native.adapter-stub: {rel(adapter)}")
    return errors


def validate_repository() -> list[str]:
    errors: list[str] = []
    project_metadata_path = ROOT / "distribution" / "project.json"
    project_metadata = {}
    if project_metadata_path.exists():
        try:
            project_metadata = json.loads(project_metadata_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            errors.append(f"identity.metadata: {exc}")
        else:
            expected_identity = {
                "name": "Agent Harness Kit",
                "slug": "agent-harness-kit",
                "version_file": "VERSION",
                "license": "MIT",
                "copyright": "2026 Agent Harness Kit contributors",
            }
            for key, value in expected_identity.items():
                if project_metadata.get(key) != value:
                    errors.append(f"identity.metadata: {key} must be {value!r}")
    package_manifest_path = ROOT / "PACKAGE-MANIFEST.json"
    package_manifest = None
    if package_manifest_path.exists():
        try:
            package_manifest = json.loads(package_manifest_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            errors.append(f"distribution.manifest: {exc}")
        else:
            if package_manifest.get("name") != "Agent Harness Kit" or package_manifest.get("slug") != "agent-harness-kit":
                errors.append("distribution.manifest-identity: wrong name or slug")
            if package_manifest.get("project_learning_activation") != "not-activated":
                errors.append("distribution.learning-activation: package selection must not activate learning")
    required_files = REQUIRED_FILES
    if package_manifest:
        required_files = [
            "README.md", "README.pt-BR.md", "AGENTS.md", "CLAUDE.md", "LICENSE", "VERSION",
            "media/agent-harness-kit-overview-pt-BR.mp3",
            "media/agent-harness-kit-overview-en.mp3",
            "media/agent-harness-kit-overview-pt-BR.mp4",
            "media/agent-harness-kit-overview-en.mp4",
            "media/overview-script-en.txt", "media/overview-script-pt-BR.txt", "media/overview-audio-manifest.json",
            "docs/PRODUCT.md", "docs/ARCHITECTURE.md", "docs/VALIDATION.md", "docs/DISTRIBUTION.md",
            "docs/MODEL-ROUTING.md", "docs/EXECUTION-BUDGET.md", "docs/REVIEW-ROUNDS.md", "docs/CHANGE-INTEGRATION.md", "docs/CONTEXT-ROUTING.md", "docs/STATUS-AND-COMPLETION.md", "docs/EMBEDDED-INSTALLATION.md", "docs/contracts/REVIEW.md", "docs/contracts/PENDING.md", "docs/contracts/STATUS.md", "docs/contracts/EXECUTION-BUDGET.md",
            "harness/playbooks/first-run.md", "harness/playbooks/status-resume.md", "harness/playbooks/task-closeout.md", "harness/playbooks/model-routing.md", "harness/playbooks/context-routing.md", "harness/playbooks/frontend-screen.md", "harness/templates/PROJECT-CONTEXT.md",
            "harness/templates/PENDING.md", "harness/templates/TASK-GRAPH.md", "harness/templates/STATUS.md", "harness/templates/MODEL-ROUTING.md", "harness/templates/EXECUTION-BUDGET.md", "harness/templates/ROOT-AGENTS-BRIDGE.md", "harness/templates/ROOT-CLAUDE-BRIDGE.md", "tools/validate.py", "tools/package.py", "tools/install.py", "validation/test_install.py", "validation/budget-fixtures/valid.json",
            ".agents/skills/first-run-discovery/SKILL.md",
            ".agents/skills/graph-execution/SKILL.md",
            ".agents/skills/governed-review/SKILL.md",
            ".agents/skills/frontend-screen/SKILL.md",
            ".claude/skills/first-run-discovery/SKILL.md",
            ".claude/skills/graph-execution/SKILL.md",
            ".claude/skills/governed-review/SKILL.md",
            ".claude/skills/frontend-screen/SKILL.md",
            ".claude/agents/discovery-interviewer.md",
            ".claude/agents/task-specialist.md",
            ".claude/agents/independent-reviewer.md",
            "validation/native-integration.json",
        ]
        for entry in package_manifest.get("files", []):
            path = entry.get("path") if isinstance(entry, dict) else None
            if not path or not (ROOT / path).is_file():
                errors.append(f"distribution.manifest-file: missing {path!r}")
    for required in required_files:
        if not (ROOT / required).is_file():
            errors.append(f"repository.required-file: missing {required}")
    if (ROOT / "PENDENCIAS.md").exists():
        errors.append("language.filename: PENDENCIAS.md must remain OPEN-DECISIONS.md")
    license_path = ROOT / "LICENSE"
    if license_path.exists():
        license_text = license_path.read_text(encoding="utf-8")
        required_license_text = (
            "MIT License",
            "Copyright (c) 2026 Agent Harness Kit contributors",
            "Permission is hereby granted, free of charge",
            'THE SOFTWARE IS PROVIDED "AS IS"',
        )
        for phrase in required_license_text:
            if phrase not in license_text:
                errors.append(f"license.content: LICENSE missing {phrase!r}")
    for audio_name in ("agent-harness-kit-overview-en.mp3", "agent-harness-kit-overview-pt-BR.mp3"):
        audio_path = ROOT / "media" / audio_name
        if audio_path.exists():
            audio_bytes = audio_path.read_bytes()
            if len(audio_bytes) < 1024 or not (audio_bytes.startswith(b"ID3") or audio_bytes[:1] == b"\xff"):
                errors.append(f"media.audio: {audio_name} is empty or not recognizable as MP3")
    for player_name in ("agent-harness-kit-overview-en.mp4", "agent-harness-kit-overview-pt-BR.mp4"):
        player_path = ROOT / "media" / player_name
        if player_path.exists():
            player_bytes = player_path.read_bytes()
            if len(player_bytes) < 1024 or b"ftyp" not in player_bytes[:64]:
                errors.append(f"media.player: {player_name} is empty or not recognizable as MP4")
    audio_manifest_path = ROOT / "media" / "overview-audio-manifest.json"
    audio_manifest: dict = {}
    if audio_manifest_path.is_file():
        try:
            audio_manifest = json.loads(audio_manifest_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            errors.append(f"media.manifest: {exc}")
        else:
            if audio_manifest.get("schema") != "agent-harness-kit.overview-audio/v1":
                errors.append("media.manifest-schema: overview-audio-manifest.json")
            tracks = audio_manifest.get("tracks", [])
            if not isinstance(tracks, list) or {track.get("language") for track in tracks if isinstance(track, dict)} != {"en", "pt-BR"}:
                errors.append("media.manifest-languages: expected en and pt-BR")
            for track in tracks if isinstance(tracks, list) else []:
                if not isinstance(track, dict):
                    errors.append("media.manifest-track: track must be an object")
                    continue
                language = track.get("language", "unknown")
                if track.get("status") not in {"candidate-awaiting-audition", "approved", "refresh-required"}:
                    errors.append(f"media.manifest-status: {language}")
                attachment = track.get("github_attachment", "")
                if not re.fullmatch(r"https://github\.com/user-attachments/assets/[0-9a-f-]{36}", attachment):
                    errors.append(f"media.manifest-attachment: {language}")
                for field in ("audio", "script", "github_player"):
                    value = track.get(field)
                    path = (ROOT / str(value)).resolve() if value else None
                    try:
                        if path is None:
                            raise ValueError
                        path.relative_to(ROOT)
                    except ValueError:
                        errors.append(f"media.manifest-path: {language} {field}")
                        continue
                    if not path.is_file():
                        errors.append(f"media.manifest-missing: {language} {field}")
                        continue
                    expected = track.get(f"{field}_sha256")
                    actual = hashlib.sha256(path.read_bytes()).hexdigest()
                    if expected != actual:
                        errors.append(f"media.manifest-hash: {language} {field}")
                if track.get("status") in {"candidate-awaiting-audition", "approved"} and track.get("script_synced") is not True:
                    errors.append(f"media.manifest-script-sync: {language}")
    for path in markdown_files():
        errors.extend(validate_markdown(path))
        text = path.read_text(encoding="utf-8")
        header = frontmatter(text)
        if header.get("schema") == "harness.task/v1":
            if header.get("review_profile") not in {"light", "standard", "critical"}:
                errors.append(f"review.profile: {rel(path)}")
            if header.get("max_review_rounds") not in {"1", "2"}:
                errors.append(f"review.round-budget: {rel(path)} must be 1 or 2")
            if header.get("assurance_gate") not in {"none", "affected-actions"}:
                errors.append(f"review.assurance-gate: {rel(path)}")
            if header.get("review_profile") == "critical" and header.get("assurance_gate") != "affected-actions":
                errors.append(f"review.critical-gate: {rel(path)} critical work must gate affected actions")
        if header.get("schema") == "harness.review/v1":
            round_value = header.get("round")
            scope = header.get("scope")
            if round_value not in {"1", "2"}:
                errors.append(f"review.round: {rel(path)}")
            if (round_value == "1" and scope != "initial") or (round_value == "2" and scope != "focused-rereview"):
                errors.append(f"review.scope: {rel(path)}")
            if round_value == "2" and header.get("prior_review") in {None, "", "none"}:
                errors.append(f"review.lineage: {rel(path)}")
            focused_fields = ("blocking_findings", "correction_delta", "regression_scope")
            if round_value == "2" and any(header.get(field) in {None, "", "none"} for field in focused_fields):
                errors.append(f"review.focused-evidence: {rel(path)} round 2 must pin blockers, correction delta, and regression scope")
        if header.get("schema") == "harness.handoff/v1":
            if header.get("status") not in {"completed", "blocked", "failed"}:
                errors.append(f"handoff.status: {rel(path)} must be completed, blocked, or failed")
            closeout = re.search(r"^## User-facing closeout\s*$([\s\S]*?)(?=^## |\Z)", text, re.MULTILINE)
            required_labels = ("Stage:", "Progress:", "Blockers:", "Next action:", "Inspectable paths:", "Human action required:")
            if not closeout or any(label not in closeout.group(1) for label in required_labels):
                errors.append(f"handoff.closeout-fields: {rel(path)}")
        if header.get("schema") == "harness.pending/v1":
            required_pending_sections = {"Human action required", "Project completion overview", "Recently resolved"}
            if not required_pending_sections <= headings(text):
                errors.append(f"pending.sections: {rel(path)}")
            if "Agent and project work" in headings(text):
                errors.append(f"pending.technical-leak: {rel(path)} must keep technical execution in TASK-GRAPH.md")
        if header.get("schema") == "harness.task-graph/v1":
            try:
                graph = extract_graph(text)
            except json.JSONDecodeError as exc:
                errors.append(f"graph.json: {rel(path)} {exc}")
            else:
                if graph is None:
                    errors.append(f"graph.missing-json: {rel(path)}")
                else:
                    errors.extend(validate_graph(graph, rel(path)))
            transition_revisions = [int(value) for value in re.findall(r"^- r(\d+):", text, re.MULTILINE)]
            if transition_revisions:
                try:
                    declared_revision = int(header.get("revision", ""))
                except ValueError:
                    errors.append(f"graph.revision-number: {rel(path)}")
                else:
                    if declared_revision != max(transition_revisions):
                        errors.append(f"graph.revision-log: {rel(path)} declares r{declared_revision} but log reaches r{max(transition_revisions)}")
    for readme in (ROOT / "README.md", ROOT / "README.pt-BR.md"):
        if readme.exists() and len(re.findall(r"^```mermaid$", readme.read_text(encoding="utf-8"), re.MULTILINE)) != 1:
            errors.append(f"markdown.mermaid: {rel(readme)} must contain exactly one Mermaid block")
        if readme.exists():
            readme_text = readme.read_text(encoding="utf-8")
            attachment_urls = re.findall(r"^https://github\.com/user-attachments/assets/[0-9a-f-]{36}$", readme_text, re.MULTILINE)
            is_portuguese = readme.name == "README.pt-BR.md"
            language = "pt-BR" if is_portuguese else "en"
            manifest_tracks = {
                track.get("language"): track for track in audio_manifest.get("tracks", [])
                if isinstance(track, dict)
            }
            expected_attachment = manifest_tracks.get(language, {}).get("github_attachment", "")
            expected_audio = "media/agent-harness-kit-overview-pt-BR.mp3" if is_portuguese else "media/agent-harness-kit-overview-en.mp3"
            expected_script = "media/overview-script-pt-BR.txt" if is_portuguese else "media/overview-script-en.txt"
            other_audio = "media/agent-harness-kit-overview-en.mp3" if is_portuguese else "media/agent-harness-kit-overview-pt-BR.mp3"
            other_script = "media/overview-script-en.txt" if is_portuguese else "media/overview-script-pt-BR.txt"
            if attachment_urls != [expected_attachment]:
                errors.append(f"media.readme-player: {rel(readme)} must contain only its language-specific GitHub attachment player")
            if f"]({expected_audio})" not in readme_text or f"]({expected_script})" not in readme_text:
                errors.append(f"media.readme-language-assets: {rel(readme)} missing its language-specific MP3 or script")
            if other_audio in readme_text or other_script in readme_text:
                errors.append(f"media.readme-cross-language: {rel(readme)} must not mix overview media languages")
            if "<audio" in readme_text or "<video" in readme_text:
                errors.append(f"media.readme-unsupported-html: {rel(readme)}")
            if "agent-harness-kit/" not in readme_text or "EMBEDDED-INSTALLATION.md" not in readme_text:
                errors.append(f"embedded.readme-route: {rel(readme)}")
    embedded_doc = ROOT / "docs" / "EMBEDDED-INSTALLATION.md"
    agents_bridge = ROOT / "harness" / "templates" / "ROOT-AGENTS-BRIDGE.md"
    claude_bridge = ROOT / "harness" / "templates" / "ROOT-CLAUDE-BRIDGE.md"
    for bridge in (agents_bridge, claude_bridge):
        if bridge.is_file():
            bridge_text = bridge.read_text(encoding="utf-8")
            if bridge_text.count("<!-- agent-harness-kit:begin -->") != 1 or bridge_text.count("<!-- agent-harness-kit:end -->") != 1:
                errors.append(f"embedded.bridge-markers: {rel(bridge)}")
    if agents_bridge.is_file() and "agent-harness-kit/AGENTS.md" not in agents_bridge.read_text(encoding="utf-8"):
        errors.append("embedded.agents-route: root bridge must name agent-harness-kit/AGENTS.md")
    if claude_bridge.is_file() and "@agent-harness-kit/CLAUDE.md" not in claude_bridge.read_text(encoding="utf-8"):
        errors.append("embedded.claude-route: root bridge must import agent-harness-kit/CLAUDE.md")
    for bridge in (agents_bridge, claude_bridge):
        if bridge.is_file():
            bridge_text = bridge.read_text(encoding="utf-8")
            if "first-response" not in bridge_text or "first-run discovery interview automatically" not in bridge_text:
                errors.append(f"embedded.first-run-route: {rel(bridge)} must trigger automatic discovery from the root entrypoint")
            bridge_lower = bridge_text.lower()
            for token in ("mandatory first-response gate", "before any scan", "stop", "substantive project request", "exactly one", "prior conversations", "agent harness kit is active", "registered mentally", "path/revision"):
                if token not in bridge_lower:
                    errors.append(f"embedded.first-response-salience: {rel(bridge)} lacks {token!r}")
    if embedded_doc.is_file():
        embedded_text = embedded_doc.read_text(encoding="utf-8").lower()
        for phrase in ("harness-state/", "preserve", "degraded", "agent-harness-kit/"):
            if phrase not in embedded_text:
                errors.append(f"embedded.installation-policy: missing {phrase!r}")
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8").lower() if (ROOT / "AGENTS.md").exists() else ""
    for phrase in ("harness-state/PROJECT-CONTEXT.md", "harness-state/PENDING.md", "harness-state/TASK-GRAPH.md", "State authority split", "Session-start, resume, and status gate", "before planning implementation", "must not load `learning-pack/`"):
        if phrase.lower() not in agents:
            errors.append(f"policy.root-map: AGENTS.md missing {phrase!r}")
    for readme in (ROOT / "README.md", ROOT / "README.pt-BR.md"):
        if readme.exists() and not readme.read_text(encoding="utf-8").startswith("# Agent Harness Kit\n"):
            errors.append(f"identity.readme-title: {rel(readme)}")
    errors.extend(validate_templates())
    errors.extend(validate_fixtures())
    errors.extend(validate_status_fixtures())
    errors.extend(validate_review_fixtures())
    errors.extend(validate_budget_fixtures())
    errors.extend(validate_runtime_budgets())
    errors.extend(validate_host_fixtures())
    errors.extend(validate_native_integration())
    profiles = (package_manifest.get("profile"),) if package_manifest else ("core", "core-learning", "full")
    for profile in profiles:
        result = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "package.py"), "--profile", profile, "--output", str(ROOT.parent), "--check"],
            cwd=ROOT, capture_output=True, text=True, check=False,
        )
        if result.returncode:
            errors.append(f"distribution.profile: {profile}: {(result.stderr or result.stdout).strip()}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Agent Harness Kit source or a namespaced host adoption")
    parser.add_argument("--host-root", type=Path)
    parser.add_argument("--migration-manifest", type=Path)
    args = parser.parse_args()
    if bool(args.host_root) != bool(args.migration_manifest):
        parser.error("--host-root and --migration-manifest must be provided together")
    if args.host_root:
        host_errors = validate_host_integration(args.host_root.resolve(), args.migration_manifest)
        if host_errors:
            print(f"HOST INTEGRATION VALIDATION FAILED ({len(host_errors)} error(s))")
            for error in host_errors:
                print(f"- {error}")
            return 1
        print("HOST INTEGRATION VALIDATION PASSED: migration coverage, backlinks, snapshot identities, and cutover gates")
        return 0
    errors = validate_repository()
    if errors:
        print(f"VALIDATION FAILED ({len(errors)} error(s))")
        for error in errors:
            print(f"- {error}")
        return 1
    required_count = 17 if (ROOT / "PACKAGE-MANIFEST.json").exists() else len(REQUIRED_FILES)
    print(f"VALIDATION PASSED: {len(markdown_files())} Markdown files, {required_count} required files")
    print("Graph fixtures: valid, missing dependency, cycle, write/context collision, self-review, and path traversal")
    print("Status mutation fixtures: required fields, human-source provenance, and safe inspectable paths")
    print("Review mutation fixtures: focused round-two blocker, correction-delta, and regression boundaries")
    print("Execution budget fixtures: attempt, no-progress, context-expansion, lineage, and path ceilings")
    print("Host fixtures: namespaced adoption, missing backlink, silent omission, stale snapshot, and premature cutover")
    print("Native integration: Codex and Claude Code entrypoints, frontend/learning/context routing, safe defaults, and profile boundaries")
    print("Language boundary: README.pt-BR.md is the only Portuguese-content exception")
    return 0


if __name__ == "__main__":
    sys.exit(main())
