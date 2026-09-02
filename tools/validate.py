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
from typing import NamedTuple, Sequence
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent_harness_kit.readiness import readiness_blocker


EXCLUDED_PARTS = {"work", "outputs", ".git", "__pycache__"}
READY_STATES = {"ready", "active"}
ACTIVE_STATES = {"active"}
FOUNDATIONAL_SCOPE_PATHS = {
    "AGENTS.md",
    "CLAUDE.md",
    "PACKAGE-MANIFEST.json",
    "pyproject.toml",
    "tools/package.py",
    "tools/validate.py",
    "agent_harness_kit/__main__.py",
    "agent_harness_kit/cli.py",
}
NODE_FIELDS = {
    "id", "goal", "depends_on", "status", "assignee", "reviewer",
    "write_set", "checkpoint", "task_brief", "evidence_profile", "assurance_status", "assurance_requires",
}
NODE_CONTEXT_FIELDS = {"workstream", "agent_role", "execution_context", "thread_policy", "thread_ref"}
NODE_ENRICHMENT_FIELDS = {"read_set", "impact_set", "context_provenance"}


class ScopeError(RuntimeError):
    """Raised when a requested validation scope cannot be resolved safely."""


class ScopeSelection(NamedTuple):
    requested_scope: str
    effective_scope: str
    paths: set[str] | None
    escalated: bool = False


def content_sha256(data: bytes, *, normalize_text: bool = False) -> str:
    if normalize_text:
        text = data.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")
        data = text.encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def audio_attachment_errors(track: dict) -> list[str]:
    """Require a GitHub attachment only after a regenerated track is approved."""
    language = track.get("language", "unknown")
    attachment = track.get("github_attachment")
    if not attachment:
        return [f"media.manifest-attachment: {language}"] if track.get("status") == "approved" else []
    if not isinstance(attachment, str) or not re.fullmatch(
        r"https://github\.com/user-attachments/assets/[0-9a-f-]{36}", attachment
    ):
        return [f"media.manifest-attachment: {language}"]
    return []


def validate_task_evidence_profile(header: dict[str, str], source: str) -> list[str]:
    """Validate the bounded no-artifact closeout profile for task briefs."""
    errors: list[str] = []
    evidence_profile = header.get("evidence_profile")
    if evidence_profile not in {"handoff-review", "graph-only"}:
        return [f"task.evidence-profile: {source}"]
    if evidence_profile == "graph-only":
        if header.get("planning_mode") != "inline-simple" or header.get("test_strategy") != "verification-only":
            errors.append(f"task.graph-only-scope: {source} must be inline-simple and verification-only")
        if header.get("reviewer") != "not-required" or header.get("review_profile") != "none":
            errors.append(f"task.graph-only-review: {source} must use reviewer not-required and review profile none")
        if header.get("max_review_rounds") != "0" or header.get("assurance_gate") != "none":
            errors.append(f"task.graph-only-assurance: {source} must use zero review rounds and no assurance gate")
    elif header.get("reviewer") == "not-required":
        errors.append(f"task.handoff-review-reviewer: {source} must assign or reserve an independent reviewer")
    return errors

REQUIRED_FILES = [
    "README.md", "README.pt-BR.md", "AGENTS.md", "CLAUDE.md", "LICENSE", "docs/assets/agent-harness-kit-banner.svg", "docs/assets/harness-demo-flow.svg", "media/agent-harness-kit-overview-en.mp3", "media/agent-harness-kit-overview-pt-BR.mp3", "media/agent-harness-kit-overview-en.mp4", "media/agent-harness-kit-overview-pt-BR.mp4",
    "media/overview-script-en.txt", "media/overview-script-pt-BR.txt", "media/overview-audio-manifest.json",
    "OPEN-DECISIONS.md", "docs/PRODUCT.md", "docs/ARCHITECTURE.md", "docs/PYPI-README.md",
    "docs/CORE-VS-LEARNING.md", "docs/DISCOVERY-INTERVIEW.md",
    "docs/PORTABILITY.md", "docs/VALIDATION.md", "docs/ADAPTIVE-EXECUTION.md", "docs/RUNTIME-STATE.md", "docs/TDD.md", "docs/MODEL-ROUTING.md", "docs/EXECUTION-BUDGET.md", "docs/REVIEW-ROUNDS.md", "docs/CHANGE-INTEGRATION.md", "docs/CONTEXT-ROUTING.md", "docs/HACKATHON-MODE.md", "docs/STATUS-AND-COMPLETION.md", "docs/EMBEDDED-INSTALLATION.md",
    "docs/contracts/REQUEST-ROUTE.md", "docs/contracts/FEATURE-BRIEF.md", "docs/contracts/IMPLEMENTATION-PLAN.md", "docs/contracts/MODEL-DISPATCH.md", "docs/contracts/CODEX-AGENT-DISPATCH.md", "docs/contracts/PARALLEL-DISPATCH.md", "docs/contracts/REVIEW.md", "docs/contracts/PENDING.md", "docs/contracts/STATUS.md", "docs/contracts/EXECUTION-BUDGET.md",
    "adapters/README.md", "adapters/generic.md", "adapters/codex.md", "adapters/claude.md",
    "harness/roles/README.md", "harness/roles/discovery-interviewer.md",
    "harness/roles/orchestrator-po.md", "harness/roles/task-decomposer.md",
    "harness/roles/generic-specialist.md", "harness/roles/reviewer-integrator.md",
    "harness/roles/learning-assessor.md", "harness/roles/learning-debriefer-publisher.md",
    "harness/playbooks/README.md", "harness/playbooks/request-routing.md", "harness/playbooks/first-run.md", "harness/playbooks/feature-discovery.md", "harness/playbooks/writing-plans.md", "harness/playbooks/test-driven-execution.md", "harness/playbooks/hackathon-delivery.md", "harness/playbooks/status-resume.md",
    "harness/playbooks/discovery-to-graph.md", "harness/playbooks/task-dispatch.md",
    "harness/playbooks/contract-changes.md", "harness/playbooks/parallel-execution.md",
    "harness/playbooks/review-integration.md", "harness/playbooks/task-closeout.md", "harness/playbooks/model-routing.md", "harness/playbooks/context-routing.md", "harness/playbooks/frontend-screen.md", "harness/playbooks/learning-capture-publication.md",
    "harness/templates/README.md", "harness/templates/REQUEST-ROUTE.md", "harness/templates/PROJECT-CONTEXT.md", "harness/templates/FEATURE-BRIEF.md", "harness/templates/IMPLEMENTATION-PLAN.md",
    "harness/templates/PENDING.md", "harness/templates/TASK-GRAPH.md", "harness/templates/TASK.md", "harness/templates/EXECUTION-BUDGET.md",
    "harness/templates/HANDOFF.md", "harness/templates/MODEL-DISPATCH.md", "harness/templates/CODEX-AGENT-DISPATCH.md", "harness/templates/PARALLEL-DISPATCH.md", "harness/templates/REVIEW.md", "harness/templates/STATUS.md",
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
    "validation/model-dispatch-fixtures/valid.json",
    "validation/model-dispatch-fixtures/invalid/recorded-tier-only.json",
    "validation/model-dispatch-fixtures/invalid/silent-host-default.json",
    "validation/model-dispatch-fixtures/invalid/same-context-autoswitch.json",
    "validation/test_model_dispatch.py", "validation/test_media_manifest.py",
    "validation/test_scheduler.py", "validation/test_parallel_dispatch.py", "validation/test_codex_dispatch.py", "validation/test_codex_agent_dispatch_validation.py",
    "validation/parallel-dispatch-fixtures/valid.json",
    "validation/parallel-dispatch-fixtures/invalid/recorded-without-runtime.json",
    "validation/parallel-dispatch-fixtures/invalid/over-capacity.json",
    "validation/parallel-dispatch-fixtures/invalid/duplicate-context.json",
    "validation/codex-agent-dispatch-fixtures/valid.json",
    "validation/codex-agent-dispatch-fixtures/invalid/same-review-context.json",
    "validation/codex-agent-dispatch-fixtures/invalid/missing-response.json",
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
    "validation/review-fixtures/invalid/missing-spec-authority.json",
    "validation/review-fixtures/invalid/prompt-memory-source.json",
    "validation/review-fixtures/invalid/same-context.json",
    "validation/budget-fixtures/valid.json",
    "validation/budget-fixtures/invalid/attempt-ceiling-bypass.json",
    "validation/budget-fixtures/invalid/no-progress-ceiling-bypass.json",
    "validation/budget-fixtures/invalid/context-ceiling-bypass.json",
    "validation/budget-fixtures/invalid/counter-rollback.json",
    "validation/budget-fixtures/invalid/lineage-reset.json",
    "validation/budget-fixtures/invalid/task-only-scope.json",
    "validation/budget-fixtures/invalid/path-traversal.json",
    "VERSION", "docs/DISTRIBUTION.md", "docs/PUBLICATION-READINESS.md", "pyproject.toml", "agent_harness_kit/__init__.py", "agent_harness_kit/__main__.py", "agent_harness_kit/cli.py", "agent_harness_kit/preflight.py", "agent_harness_kit/state_runtime.py", "agent_harness_kit/scheduler.py", "tools/package.py", "tools/install.py", "validation/test_install.py", "validation/test_cli.py", "validation/test_installed_host_smoke.py", "validation/test_validate_cli.py", "validation/test_preflight.py", "validation/test_state_runtime.py", "benchmarks/fullstack/scripts/run_pilot.py", "benchmarks/fullstack/tests/test_run_pilot.py",
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
    ".agents/skills/request-router/SKILL.md", ".agents/skills/first-run-discovery/SKILL.md", ".agents/skills/feature-discovery/SKILL.md", ".agents/skills/writing-plans/SKILL.md", ".agents/skills/test-driven-task/SKILL.md", ".agents/skills/graph-execution/SKILL.md",
    ".agents/skills/governed-review/SKILL.md", ".agents/skills/codex-agent-dispatch/SKILL.md", ".agents/skills/parallel-dispatch/SKILL.md", ".agents/skills/frontend-screen/SKILL.md", ".agents/skills/project-learning/SKILL.md",
    ".claude/skills/request-router/SKILL.md", ".claude/skills/first-run-discovery/SKILL.md", ".claude/skills/feature-discovery/SKILL.md", ".claude/skills/writing-plans/SKILL.md", ".claude/skills/test-driven-task/SKILL.md", ".claude/skills/graph-execution/SKILL.md",
    ".claude/skills/governed-review/SKILL.md", ".claude/skills/parallel-dispatch/SKILL.md", ".claude/skills/frontend-screen/SKILL.md", ".claude/skills/project-learning/SKILL.md",
    ".claude/agents/discovery-interviewer.md", ".claude/agents/task-specialist.md",
    ".claude/agents/independent-reviewer.md", ".claude/agents/learning-assessor.md",
]

TEMPLATE_RULES = {
    "IMPLEMENTATION-PLAN.md": (
        {"schema", "id", "revision", "status", "project_context", "feature_brief", "updated_at", "updated_by", "source_references"},
        {"Outcome and authority", "Planning classification", "Scoped context and constraints", "Task units", "Integration and verification", "Replan triggers"},
    ),
    "FEATURE-BRIEF.md": (
        {"schema", "id", "revision", "status", "project_context", "owner", "updated_at", "approved_by", "supersedes", "source_references"},
        {"Problem and user", "Actors, access, and permissions", "Current behavior and evidence", "Desired outcome and success", "Options explored", "Selected direction", "Scope", "Non-goals", "User journey", "Alternate, failure, and recovery paths", "Data and integrations", "Constraints and risks", "Deferred cases", "Acceptance criteria", "Open questions", "Graph handoff"},
    ),
    "PROJECT-CONTEXT.md": (
        {"schema", "id", "revision", "status", "mode", "updated_at", "approved_by", "supersedes", "discovery_snapshot", "source_references", "capability_manifest", "rules_map", "pending_authority"},
        {"Project state", "Intent", "Scope", "Success measures", "Delivery shape", "Constraints", "Rules and capabilities", "Assumptions and unknowns", "Verification environment", "References"},
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
        {"schema", "id", "graph", "revision", "status", "planning_mode", "implementation_plan", "plan_step", "target_minutes", "test_strategy", "tdd_exception", "evidence_profile", "assurance", "artifact_policy", "handoff_consumer", "test_ladder", "assigned_to", "reviewer", "workstream", "agent_role", "execution_context", "thread_policy", "thread_ref", "ownership_lease", "isolation", "updated_at", "capability_manifest", "rules_map", "model_tier", "model_reason", "model_dispatch", "execution_budget", "review_profile", "max_review_rounds", "assurance_gate"},
        {"Outcome", "Executable spec", "Context to load", "Owned paths", "Constraints", "Non-goals", "Rules to load", "Required capabilities", "Acceptance criteria", "Test-first cycle", "Verification", "Stop and replan", "Exit"},
    ),
    "HANDOFF.md": (
        {"schema", "id", "task", "attempt", "status", "consumer", "author", "workstream", "agent_role", "execution_context", "thread_ref", "created_at", "model_tier_used", "model_id_used", "reasoning_effort_used", "model_dispatch", "model_route_changes", "execution_budget"},
        {"Result", "Changes", "Change unit and authority", "Acceptance evidence", "Verification run", "Test-first evidence", "Execution budget", "Discoveries and risks", "Routing and authority", "Review request", "User-facing closeout"},
    ),
    "MODEL-DISPATCH.md": (
        {"schema", "id", "revision", "task", "status", "tier", "tier_reason", "adapter", "capability_evidence", "available_models", "selected_model", "reasoning_effort", "dispatch_surface", "override_requested", "override_confirmed", "execution_context_ref", "dispatch_evidence", "created_at", "created_by"},
        {"Resolution", "Dispatch evidence", "Degradation and recovery"},
    ),
    "PARALLEL-DISPATCH.md": (
        {"schema", "id", "revision", "status", "graph", "capacity", "active_before", "capability_evidence", "scheduler_plan", "created_at", "created_by"},
        {"Selection", "Reservation transaction", "Adapter dispatch evidence", "Refill and fan-in", "Recovery"},
    ),
    "CODEX-AGENT-DISPATCH.md": (
        {"schema", "id", "revision", "status", "task", "purpose", "agent_identity", "role", "execution_context_ref", "model_dispatch", "adapter_operation", "adapter_response_identity", "created_at", "created_by"},
        {"Role resolution", "Minimal context packet", "Native call", "Dispatch evidence", "Separation and fallback"},
    ),
    "REVIEW.md": (
        {"schema", "id", "task", "handoff", "spec_authority", "review_packet", "review_context", "review_context_ref", "prompt_source", "revision", "round", "scope", "prior_review", "blocking_findings", "correction_delta", "regression_scope", "status", "reviewer", "verdict", "findings", "evidence", "commands", "duration_ms", "tokens", "created_at"},
        {"Independence", "Spec authority", "Fresh-context evidence", "Independent reconstruction", "Review profile and scope", "Criterion verdicts", "Findings", "Integration recommendation", "Verification", "Next review boundary"},
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


def normalize_scope_path(path: str | Path) -> str:
    return str(path).replace("\\", "/").removeprefix("./").strip("/")


def git_changed_paths() -> set[str]:
    """Return tracked and untracked worktree changes as repository-relative paths."""
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError as exc:
        raise ScopeError(f"changed scope requires Git: {exc}") from exc
    if result.returncode:
        detail = (result.stderr or result.stdout).strip()
        suffix = f": {detail}" if detail else ""
        raise ScopeError(f"changed scope requires Git and a readable repository{suffix}")

    entries = result.stdout.split("\0")
    changed: set[str] = set()
    index = 0
    while index < len(entries):
        entry = entries[index]
        index += 1
        if not entry:
            continue
        if len(entry) < 4 or entry[2] != " ":
            continue
        status = entry[:2]
        changed.add(normalize_scope_path(entry[3:]))
        if "R" in status or "C" in status:
            if index < len(entries) and entries[index]:
                changed.add(normalize_scope_path(entries[index]))
            index += 1  # porcelain -z appends the rename/copy source as a second field
    return changed


def foundational_scope_change(paths: set[str]) -> bool:
    return any(
        path in FOUNDATIONAL_SCOPE_PATHS or path.startswith("distribution/profiles/")
        for path in paths
    )


def task_scope_paths(task_path: Path) -> set[str]:
    path = task_path if task_path.is_absolute() else ROOT / task_path
    path = path.resolve()
    try:
        task_relative = path.relative_to(ROOT.resolve()).as_posix()
    except ValueError as exc:
        raise ScopeError(f"task path must be inside the repository: {task_path}") from exc
    if not path.is_file():
        raise ScopeError(f"task path does not exist or is not a file: {task_path}")

    text = path.read_text(encoding="utf-8")
    owned_match = re.search(r"^## Owned paths\s*$([\s\S]*?)(?=^## |\Z)", text, re.MULTILINE)
    paths = {task_relative}
    if not owned_match:
        return paths
    for raw in re.findall(r"^-\s+`([^`]+)`\s*$", owned_match.group(1), re.MULTILINE):
        normalized, reason = normalize_owned_path(raw)
        if reason or not normalized:
            raise ScopeError(f"task contains an invalid owned path {raw!r}: {reason}")
        candidate = ROOT / normalized
        if "*" in raw or "?" in raw:
            matches = sorted(item for item in ROOT.glob(raw.replace("\\", "/")) if item.is_file())
            if matches:
                paths.update(rel(item) for item in matches)
            else:
                paths.add(normalized)
        elif candidate.is_dir():
            paths.update(rel(item) for item in sorted(candidate.rglob("*")) if item.is_file())
        else:
            paths.add(normalized)
    return paths


def resolve_scope(scope: str, task_path: Path | None) -> ScopeSelection:
    if scope == "repository":
        return ScopeSelection(scope, scope, None)
    if scope == "task":
        if task_path is None:
            raise ScopeError("--scope task requires --task PATH")
        return ScopeSelection(scope, scope, task_scope_paths(task_path))
    paths = git_changed_paths()
    if foundational_scope_change(paths):
        return ScopeSelection(scope, "repository", None, True)
    return ScopeSelection(scope, scope, paths)


def error_in_scope(error: str, selected_paths: set[str]) -> bool:
    detail = error.replace("\\", "/")
    for path in selected_paths:
        normalized = normalize_scope_path(path)
        if normalized and normalized in detail:
            return True
    return False


def scoped_errors(errors: Sequence[str], selected_paths: set[str] | None) -> list[str]:
    if selected_paths is None:
        return list(errors)
    return [error for error in errors if error_in_scope(error, selected_paths)]


def summarize_error_categories(errors: Sequence[str]) -> str:
    counts: dict[str, int] = {}
    for error in errors:
        code = error.split(":", 1)[0]
        category = code.split(".", 1)[0]
        counts[category] = counts.get(category, 0) + 1
    return ", ".join(f"{category}={counts[category]}" for category in sorted(counts))


def load_package_manifest() -> dict | None:
    path = ROOT / "PACKAGE-MANIFEST.json"
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return data if isinstance(data, dict) else None


def selected_required_count(package_manifest: dict | None, selected_paths: set[str] | None) -> int:
    if package_manifest:
        required = {
            normalize_scope_path(entry["path"])
            for entry in package_manifest.get("files", [])
            if isinstance(entry, dict) and isinstance(entry.get("path"), str)
        }
    else:
        required = set(REQUIRED_FILES)
    if selected_paths is None:
        return len(required)
    return len(required & {normalize_scope_path(path) for path in selected_paths})


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
        present_enrichment = NODE_ENRICHMENT_FIELDS & set(node)
        if present_enrichment and present_enrichment != NODE_ENRICHMENT_FIELDS:
            errors.append(f"graph.enrichment-fields: {source} {node.get('id', index)} missing {sorted(NODE_ENRICHMENT_FIELDS - set(node))}")
    for node_id, node in by_id.items():
        evidence_profile = node.get("evidence_profile")
        if evidence_profile not in {"handoff-review", "graph-only"}:
            errors.append(f"graph.evidence-profile: {source} {node_id}")
        elif evidence_profile == "graph-only":
            if node.get("reviewer") != "not-required":
                errors.append(f"graph.graph-only-reviewer: {source} {node_id}")
            if node.get("assurance_status") != "not-required" or node.get("assurance_requires") != []:
                errors.append(f"graph.graph-only-assurance: {source} {node_id}")
        elif node.get("reviewer") == "not-required":
            errors.append(f"graph.handoff-review-reviewer: {source} {node_id}")
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
        if NODE_ENRICHMENT_FIELDS <= set(node):
            for field in ("read_set", "impact_set"):
                scoped_paths = node.get(field)
                if not isinstance(scoped_paths, list):
                    errors.append(f"graph.{field.replace('_', '-')}-shape: {source} {node_id}")
                    continue
                for scoped in scoped_paths:
                    normalized, reason = normalize_owned_path(str(scoped))
                    if reason:
                        errors.append(f"graph.invalid-path: {source} {node_id} {scoped!r} ({reason})")
            if not isinstance(node.get("context_provenance"), str) or not node["context_provenance"].strip():
                errors.append(f"graph.context-provenance: {source} {node_id}")
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
        if node.get("status") not in READY_STATES:
            continue
        blocker = readiness_blocker(node, by_id)
        if blocker is None:
            continue
        gate, _, required_id = blocker.partition(":")
        if gate == "dependency":
            errors.append(f"graph.dependency-gate: {source} {node_id} waits for completed dependency {required_id}")
        elif gate == "assurance":
            errors.append(f"graph.assurance-gate: {source} {node_id} waits for accepted assurance of {required_id}")
        else:
            errors.append(f"graph.checkpoint-gate: {source} {node_id} has an unresolved checkpoint")

    concurrent = [node for node in by_id.values() if node.get("status") in ACTIVE_STATES]
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


PARALLEL_DISPATCH_FIELDS = {
    "schema", "id", "graph", "status", "capacity", "active_before",
    "capability_evidence", "selected", "dispatches",
}


def validate_parallel_dispatch_payload(data: dict, source: str) -> list[str]:
    """Require runtime evidence for every task claimed as parallel-dispatched."""
    errors: list[str] = []
    if not isinstance(data, dict):
        return [f"parallel-dispatch.shape: {source}"]
    if missing := PARALLEL_DISPATCH_FIELDS - set(data):
        errors.append(f"parallel-dispatch.missing-field: {source} {sorted(missing)}")
    if data.get("schema") != "harness.parallel-dispatch/v1":
        errors.append(f"parallel-dispatch.schema: {source}")
    if data.get("status") not in {"completed", "partial", "blocked"}:
        errors.append(f"parallel-dispatch.status: {source}")
    capacity = data.get("capacity")
    active_before = data.get("active_before")
    if not isinstance(capacity, int) or isinstance(capacity, bool) or capacity < 1:
        errors.append(f"parallel-dispatch.capacity: {source}")
        capacity = 0
    if not isinstance(active_before, int) or isinstance(active_before, bool) or active_before < 0:
        errors.append(f"parallel-dispatch.active-count: {source}")
        active_before = 0
    selected = data.get("selected")
    dispatches = data.get("dispatches")
    if not isinstance(selected, list):
        errors.append(f"parallel-dispatch.selected-shape: {source}")
        selected = []
    if not isinstance(dispatches, list):
        errors.append(f"parallel-dispatch.dispatch-shape: {source}")
        dispatches = []
    if active_before + len(dispatches) > capacity:
        errors.append(f"parallel-dispatch.capacity: {source}")

    selected_ids: list[str] = []
    selected_paths: list[tuple[str, list[str]]] = []
    for item in selected:
        if not isinstance(item, dict) or not item.get("task") or not isinstance(item.get("write_set"), list):
            errors.append(f"parallel-dispatch.selected-shape: {source}")
            continue
        task_id = str(item["task"])
        if task_id in selected_ids:
            errors.append(f"parallel-dispatch.duplicate-task: {source} {task_id}")
        selected_ids.append(task_id)
        normalized: list[str] = []
        for raw in item["write_set"]:
            path, reason = normalize_owned_path(str(raw))
            if reason or not path:
                errors.append(f"parallel-dispatch.invalid-path: {source} {task_id} {raw!r}")
            else:
                normalized.append(path)
        for owner_id, owner_paths in selected_paths:
            if any(paths_collide(left, right) for left in normalized for right in owner_paths):
                errors.append(f"parallel-dispatch.write-collision: {source} {owner_id} <> {task_id}")
        selected_paths.append((task_id, normalized))

    dispatch_ids: list[str] = []
    context_refs: list[str] = []
    lease_refs: list[str] = []
    placeholders = {"", "none", "pending", "unknown", "unavailable", "self-asserted"}
    for item in dispatches:
        if not isinstance(item, dict):
            errors.append(f"parallel-dispatch.dispatch-shape: {source}")
            continue
        task_id = str(item.get("task", ""))
        dispatch_ids.append(task_id)
        context_ref = str(item.get("context_ref", "")).strip()
        lease_ref = str(item.get("lease_ref", "")).strip()
        evidence = str(item.get("adapter_evidence", "")).strip()
        model_dispatch = str(item.get("model_dispatch", "")).strip()
        if any(value.lower() in placeholders for value in (context_ref, lease_ref, evidence, model_dispatch)):
            errors.append(f"parallel-dispatch.missing-evidence: {source} {task_id}")
        if context_ref in context_refs:
            errors.append(f"parallel-dispatch.duplicate-context: {source} {context_ref}")
        if lease_ref in lease_refs:
            errors.append(f"parallel-dispatch.duplicate-lease: {source} {lease_ref}")
        context_refs.append(context_ref)
        lease_refs.append(lease_ref)
    if data.get("status") == "completed" and sorted(selected_ids) != sorted(dispatch_ids):
        errors.append(f"parallel-dispatch.incomplete-batch: {source}")
    return errors


def validate_parallel_dispatch_fixtures() -> list[str]:
    errors: list[str] = []
    root = ROOT / "validation" / "parallel-dispatch-fixtures"
    valid_path = root / "valid.json"
    try:
        valid = json.loads(valid_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"parallel-dispatch.fixture-baseline: {exc}"]
    if actual := validate_parallel_dispatch_payload(valid, rel(valid_path)):
        errors.append(f"parallel-dispatch.fixture-valid-failed: {actual}")
    for path in sorted((root / "invalid").glob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        actual = validate_parallel_dispatch_payload(payload, rel(path))
        actual_codes = {item.split(":", 1)[0] for item in actual}
        expected = set(payload.get("expected_errors", []))
        if not expected:
            errors.append(f"parallel-dispatch.fixture-no-expectation: {rel(path)}")
        elif not expected.issubset(actual_codes):
            errors.append(
                f"parallel-dispatch.fixture-expected-error: {rel(path)} "
                f"expected {sorted(expected)}, got {sorted(actual_codes)}"
            )
    return errors


MODEL_DISPATCH_FIELDS = {
    "schema", "id", "revision", "task", "status", "tier", "tier_reason",
    "adapter", "capability_evidence", "available_models", "selected_model",
    "reasoning_effort", "dispatch_surface", "override_requested",
    "override_confirmed", "execution_context_ref", "dispatch_evidence",
}
MODEL_OVERRIDE_SURFACES = {"create_thread", "send_message_to_thread", "spawn_subagent", "manual-selection"}
MODEL_PLACEHOLDERS = {"", "none", "pending", "unknown", "default", "host-default", "unavailable"}
MODEL_EVIDENCE_PLACEHOLDERS = MODEL_PLACEHOLDERS | {"self-asserted"}


def validate_model_dispatch_payload(data: dict, source: str) -> list[str]:
    """Reject routing records that describe a tier without proving the runtime override."""
    errors: list[str] = []
    if not isinstance(data, dict):
        return [f"model-dispatch.shape: {source}"]
    missing = MODEL_DISPATCH_FIELDS - set(data)
    if missing:
        errors.append(f"model-dispatch.missing-field: {source} {sorted(missing)}")
    if data.get("schema") != "harness.model-dispatch/v1":
        errors.append(f"model-dispatch.schema: {source}")
    if data.get("status") not in {"resolved", "manual-required", "blocked"}:
        errors.append(f"model-dispatch.status: {source}")
    if data.get("tier") not in {"economical", "balanced", "frontier"}:
        errors.append(f"model-dispatch.tier: {source}")
    if not str(data.get("tier_reason", "")).strip():
        errors.append(f"model-dispatch.tier-reason: {source}")
    available = data.get("available_models")
    if not isinstance(available, list) or not available:
        errors.append(f"model-dispatch.catalog: {source}")
        available = []
    selected = str(data.get("selected_model", "")).strip()
    if data.get("status") == "resolved" and (
        selected.lower() in MODEL_PLACEHOLDERS or selected not in available
    ):
        errors.append(f"model-dispatch.unresolved-model: {source}")
    reasoning = str(data.get("reasoning_effort", "")).strip().lower()
    if data.get("status") == "resolved" and reasoning in MODEL_PLACEHOLDERS:
        errors.append(f"model-dispatch.unresolved-reasoning: {source}")
    surface = data.get("dispatch_surface")
    if data.get("status") == "resolved" and surface not in MODEL_OVERRIDE_SURFACES:
        errors.append(f"model-dispatch.same-context-claim: {source}")
    if data.get("status") == "resolved" and (
        data.get("override_requested") is not True or data.get("override_confirmed") is not True
    ):
        errors.append(f"model-dispatch.override-not-confirmed: {source}")
    evidence = str(data.get("dispatch_evidence", "")).strip().lower()
    context_ref = str(data.get("execution_context_ref", "")).strip().lower()
    if data.get("status") == "resolved" and (
        evidence in MODEL_EVIDENCE_PLACEHOLDERS or context_ref in MODEL_PLACEHOLDERS
    ):
        errors.append(f"model-dispatch.missing-evidence: {source}")
    return errors


def validate_model_dispatch_fixtures() -> list[str]:
    errors: list[str] = []
    root = ROOT / "validation" / "model-dispatch-fixtures"
    valid_path = root / "valid.json"
    try:
        valid = json.loads(valid_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"model-dispatch.fixture-baseline: {exc}"]
    if actual := validate_model_dispatch_payload(valid, rel(valid_path)):
        errors.append(f"model-dispatch.fixture-valid-failed: {actual}")
    for path in sorted((root / "invalid").glob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        actual = validate_model_dispatch_payload(payload, rel(path))
        actual_codes = {item.split(":", 1)[0] for item in actual}
        expected = set(payload.get("expected_errors", []))
        if not expected:
            errors.append(f"model-dispatch.fixture-no-expectation: {rel(path)}")
        elif not expected.issubset(actual_codes):
            errors.append(
                f"model-dispatch.fixture-expected-error: {rel(path)} "
                f"expected {sorted(expected)}, got {sorted(actual_codes)}"
            )
    return errors


CODEX_DISPATCH_FIELDS = {
    "schema", "status", "task", "purpose", "agent_identity", "role",
    "context_packet", "execution_context_ref", "model", "adapter_operation",
    "adapter_response_identity", "adapter_response", "separation",
}
CODEX_CONTEXT_FORBIDDEN = {"conversation", "conversation_history", "prompt_history", "implementation_plan"}


def validate_codex_agent_dispatch_payload(data: dict, source: str) -> list[str]:
    """Validate adapter-owned proof that a native Codex agent was actually dispatched."""
    errors: list[str] = []
    if not isinstance(data, dict):
        return [f"codex-dispatch.shape: {source}"]
    missing = CODEX_DISPATCH_FIELDS - set(data)
    if missing:
        errors.append(f"codex-dispatch.missing-field: {source} {sorted(missing)}")
    if data.get("schema") != "harness.codex-agent-dispatch/v1":
        errors.append(f"codex-dispatch.schema: {source}")
    if data.get("status") != "dispatched":
        errors.append(f"codex-dispatch.status: {source}")
    if data.get("purpose") not in {"implementation", "review"}:
        errors.append(f"codex-dispatch.purpose: {source}")

    role = data.get("role")
    if not isinstance(role, dict) or any(not str(role.get(key, "")).strip() for key in ("requested", "executor", "role_file")):
        errors.append(f"codex-dispatch.role: {source}")
    context_packet = data.get("context_packet")
    if not isinstance(context_packet, dict) or not str(context_packet.get("task_spec", "")).strip():
        errors.append(f"codex-dispatch.context-packet: {source}")
    elif CODEX_CONTEXT_FORBIDDEN & set(context_packet):
        errors.append(f"codex-dispatch.context-leak: {source}")

    response = data.get("adapter_response")
    response_identity = str(data.get("adapter_response_identity", "")).strip().lower()
    context_ref = str(data.get("execution_context_ref", "")).strip().lower()
    if (
        not isinstance(response, dict)
        or not response
        or response_identity in MODEL_EVIDENCE_PLACEHOLDERS
        or context_ref in MODEL_PLACEHOLDERS
        or not (response.get("agent_id") or response.get("context_ref"))
    ):
        errors.append(f"codex-dispatch.missing-response: {source}")

    model = data.get("model")
    if not isinstance(model, dict):
        errors.append(f"codex-dispatch.model: {source}")
    else:
        if model.get("requested") != model.get("accepted") or str(model.get("accepted", "")).lower() in MODEL_PLACEHOLDERS:
            errors.append(f"codex-dispatch.model-mismatch: {source}")
        if (
            model.get("reasoning_effort_requested") != model.get("reasoning_effort_accepted")
            or str(model.get("reasoning_effort_accepted", "")).lower() in MODEL_PLACEHOLDERS
        ):
            errors.append(f"codex-dispatch.reasoning-mismatch: {source}")

    separation = data.get("separation")
    if not isinstance(separation, dict):
        errors.append(f"codex-dispatch.separation: {source}")
    elif data.get("purpose") == "review":
        if data.get("agent_identity") == separation.get("implementer_identity"):
            errors.append(f"codex-dispatch.reviewer-identity: {source}")
        if data.get("execution_context_ref") == separation.get("implementer_context_ref"):
            errors.append(f"codex-dispatch.reviewer-context: {source}")
        if separation.get("fresh_context_required") is not True:
            errors.append(f"codex-dispatch.reviewer-freshness: {source}")
        if isinstance(role, dict) and role.get("executor") != "role:reviewer-integrator":
            errors.append(f"codex-dispatch.reviewer-role: {source}")
    return errors


def validate_codex_agent_dispatch_fixtures() -> list[str]:
    errors: list[str] = []
    root = ROOT / "validation" / "codex-agent-dispatch-fixtures"
    valid_path = root / "valid.json"
    try:
        valid = json.loads(valid_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"codex-dispatch.fixture-baseline: {exc}"]
    if actual := validate_codex_agent_dispatch_payload(valid, rel(valid_path)):
        errors.append(f"codex-dispatch.fixture-valid-failed: {actual}")
    for path in sorted((root / "invalid").glob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        actual = validate_codex_agent_dispatch_payload(payload, rel(path))
        actual_codes = {item.split(":", 1)[0] for item in actual}
        expected = set(payload.get("expected_errors", []))
        if not expected:
            errors.append(f"codex-dispatch.fixture-no-expectation: {rel(path)}")
        elif not expected.issubset(actual_codes):
            errors.append(
                f"codex-dispatch.fixture-expected-error: {rel(path)} "
                f"expected {sorted(expected)}, got {sorted(actual_codes)}"
            )
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
    if not data.get("spec_authority"):
        errors.append(f"review.spec-authority: {source}")
    if not data.get("review_packet") or not data.get("review_context_ref"):
        errors.append(f"review.context-evidence: {source}")
    if data.get("review_context") != "isolated-fresh":
        errors.append(f"review.fresh-context: {source}")
    if data.get("prompt_source") != "task-spec-only":
        errors.append(f"review.prompt-source: {source}")
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
        elif mutation.get("action") == "set":
            candidate[mutation.get("field")] = mutation.get("value")
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
    data = path.read_bytes()
    try:
        digest = content_sha256(data, normalize_text=True)
    except UnicodeDecodeError:
        digest = content_sha256(data)
    return "sha256:" + digest


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
        if len(claude_text) > 4000 or len(claude_text) > len(agents_text) * 0.35:
            errors.append("native.context-duplication: CLAUDE.md must remain a thin compatibility entry")
        shared = str(fixture.get("shared_context", ""))
        if shared not in agents_text or shared not in (ROOT / "adapters" / "claude.md").read_text(encoding="utf-8"):
            errors.append("native.shared-core: both routes must name the neutral project-context path")
        if ".agents/skills/" not in agents_text or "adapters/codex.md" not in agents_text:
            errors.append("native.codex-routing: AGENTS.md does not route Codex")
        if ".claude/skills/" not in claude_text or "adapters/claude.md" not in claude_text:
            errors.append("native.claude-routing: CLAUDE.md does not route Claude Code")

        router_tokens = ("request-routing gate", "before all harness ceremony", ".agents/skills/request-router/skill.md", "direct-trivial", "vibe", "graph-only", "full-harness", "deterministically first", "explicit `full-harness` always wins", "orthogonal assurance", "15–30")
        if any(token not in agents_text.lower() for token in router_tokens):
            errors.append("native.request-router-root: AGENTS.md must route all requests before Harness ceremony")

        if "frontend-screen" not in agents_text or "harness/playbooks/frontend-screen.md" not in agents_text:
            errors.append("native.frontend-routing: AGENTS.md must route screen requests through the frontend workflow")
        learning_tokens = ("delivery+learning", "learning-profile", "destination")
        if any(token not in agents_text.lower() for token in learning_tokens):
            errors.append("native.learning-activation-routing: AGENTS.md must recognize learning requests and collect a note destination")
        hackathon_tokens = ("hackathon", "time-boxed mvp", "demo-first", "harness/playbooks/hackathon-delivery.md")
        if any(token not in agents_text.lower() for token in hackathon_tokens):
            errors.append("native.hackathon-routing: AGENTS.md must route time-boxed MVP and demo-first requests")
        feature_tokens = ("feature-discovery", "never needs to know its name", "highest-leverage unanswered question", "access/authentication", "failure/recovery paths", "harness-state/features/feature-<id>.md")
        if any(token not in agents_text.lower() for token in feature_tokens):
            errors.append("native.feature-discovery-routing: AGENTS.md must automatically route unresolved new feature requests")
        plan_tokens = ("writing-plans", "15–30 minutes", "compact inline spec", "scope", "human decision")
        if any(token not in agents_text.lower() for token in plan_tokens):
            errors.append("native.writing-plans-routing: AGENTS.md must require optimized spec-driven planning before implementation")
        tdd_tokens = ("test-driven-task", "meaningful red", "green", "focused", "workspace", "delivery")
        if any(token not in agents_text.lower() for token in tdd_tokens):
            errors.append("native.tdd-routing: AGENTS.md must require RED-GREEN evidence for behavior-changing code tasks")
        direct_tokens = ("direct-trivial fast path", "few minutes", "no product behavior", "smallest useful check", "no harness artifacts")
        if any(token not in agents_text.lower() for token in direct_tokens):
            errors.append("native.direct-trivial-routing: AGENTS.md must bypass SDD only for bounded mechanical edits")
        model_dispatch_tokens = ("human-approved routing artifact", "actual task, message, or subagent dispatch", "harness.model-dispatch/v1", "same-context mid-turn switch", "manual-required")
        if any(token not in agents_text.lower() for token in model_dispatch_tokens):
            errors.append("native.model-dispatch-routing: AGENTS.md must require confirmed runtime model overrides")
        parallel_tokens = ("parallel-dispatch", "two or more collision-free", "numeric parallel capacity", "active worker count", "refill capacity")
        if any(token not in agents_text.lower() for token in parallel_tokens):
            errors.append("native.parallel-dispatch-routing: AGENTS.md must automatically fan out and refill safe ready work")
        codex_agent_tokens = ("codex-agent-dispatch", "minimal request", "fork_turns: none", "harness.codex-agent-dispatch/v1", "implementer and reviewer", "manual context")
        if any(token not in agents_text.lower() for token in codex_agent_tokens):
            errors.append("native.codex-agent-dispatch-routing: AGENTS.md must create and evidence native Codex agents")

    codex_adapter = ROOT / "adapters" / "codex.md"
    if codex_adapter.is_file():
        codex_text = codex_adapter.read_text(encoding="utf-8").lower()
        for token in ("effective codex app model dispatch", "create_thread", "send_message_to_thread", "spawn_subagent", "model` and `thinking", "adapter-owned evidence", "cannot claim that it changed its own model"):
            if token not in codex_text:
                errors.append(f"native.codex-model-dispatch: adapters/codex.md lacks {token!r}")
        for token in ("effective codex app parallel dispatch", "agent-harness schedule", "without waiting", "first-completion", "refill", "sequential"):
            if token not in codex_text:
                errors.append(f"native.codex-parallel-dispatch: adapters/codex.md lacks {token!r}")
        for token in ("effective codex app agent dispatch", "agent-harness codex-dispatch", "fork_turns", "adapter response", "reviewer-integrator", "fresh manual context"):
            if token not in codex_text:
                errors.append(f"native.codex-agent-dispatch: adapters/codex.md lacks {token!r}")
    dispatch_contract = ROOT / "docs" / "contracts" / "MODEL-DISPATCH.md"
    if dispatch_contract.is_file():
        dispatch_text = dispatch_contract.read_text(encoding="utf-8").lower()
        for token in ("override_confirmed", "adapter evidence", "already-running context", "never silently accept the host default", "selected_model"):
            if token not in dispatch_text:
                errors.append(f"native.model-dispatch-contract: MODEL-DISPATCH.md lacks {token!r}")

    request_contract = ROOT / "docs" / "contracts" / "REQUEST-ROUTE.md"
    request_playbook = ROOT / "harness" / "playbooks" / "request-routing.md"
    request_template = ROOT / "harness" / "templates" / "REQUEST-ROUTE.md"
    request_surfaces = (request_contract, request_playbook, request_template)
    for surface in request_surfaces:
        if not surface.is_file():
            errors.append(f"native.request-router-surface: missing {rel(surface)}")
    if all(surface.is_file() for surface in request_surfaces):
        combined = "\n".join(surface.read_text(encoding="utf-8").lower() for surface in request_surfaces)
        for token in ("harness.request-route/v1", "direct-trivial", "vibe", "graph-only", "full-harness", "deterministic", "assurance", "compact", "complete", "explicit full", "focused", "reclass"):
            if token not in combined:
                errors.append(f"native.request-router-contract: neutral surfaces lack {token!r}")
        template_header = frontmatter(request_template.read_text(encoding="utf-8"))
        required_route_fields = {"schema", "route", "assurance", "harness_shape", "classification", "user_override", "risk_signals", "coordination_signals", "warnings", "reason", "verification", "promotion_trigger"}
        if template_header.get("schema") != "harness.request-route/v1" or not required_route_fields <= set(template_header):
            errors.append("native.request-router-template: invalid request-route header")
    for item in (".agents/skills/request-router/SKILL.md", ".claude/skills/request-router/SKILL.md"):
        path = ROOT / item
        if not path.is_file():
            errors.append(f"native.request-router-skill: missing {item}")
            continue
        skill_text = path.read_text(encoding="utf-8").lower()
        for token in ("automatically classify every request", "before mutating work", "deterministically first", "ai classifier only", "direct-trivial", "vibe", "graph-only", "full-harness", "explicit full wins", "focused deterministic check", "promote"):
            if token not in skill_text:
                errors.append(f"native.request-router-skill: {item} lacks {token!r}")

    feature_playbook = ROOT / "harness" / "playbooks" / "feature-discovery.md"
    if feature_playbook.is_file():
        feature_text = feature_playbook.read_text(encoding="utf-8").lower()
        for token in ("activate automatically", "feature-completeness analysis", "people and access", "failure and recovery", "forgotten-password recovery", "two to four credible directions", "explicitly approved", "at most two cohesive feature questions", "do not activate for bug fixes"):
            if token not in feature_text:
                errors.append(f"native.feature-discovery-contract: feature workflow lacks {token!r}")
    for item in (".agents/skills/feature-discovery/SKILL.md", ".claude/skills/feature-discovery/SKILL.md"):
        path = ROOT / item
        if path.is_file():
            skill_text = path.read_text(encoding="utf-8").lower()
            for token in ("automatically use", "first-run-discovery", "exactly one highest-leverage", "forgotten-password recovery", "failure, recovery path", "two to four credible directions", "do not mutate `pending.md` or `task-graph.md`"):
                if token not in skill_text:
                    errors.append(f"native.feature-discovery-skill: {item} lacks {token!r}")

    first_run_playbook = ROOT / "harness" / "playbooks" / "first-run.md"
    if first_run_playbook.is_file():
        first_run_text = first_run_playbook.read_text(encoding="utf-8").lower()
        for token in ("harness-state/model-routing.md", "automatic model routing enabled/disabled", "consolidated context approval", "advisory/manual"):
            if token not in first_run_text:
                errors.append(f"native.first-run-model-routing: first-run.md lacks {token!r}")

    if claude_path.is_file():
        claude_text = claude_path.read_text(encoding="utf-8").lower()
        for token in ("request-router", "before mutating work", "four public lanes", "full-harness", "assurance"):
            if token not in claude_text:
                errors.append(f"native.claude-request-routing: CLAUDE.md lacks {token!r}")
        for token in (".claude/skills/feature-discovery/skill.md", "automatically load", "need not name it", "failure/recovery", "before pending or graph changes"):
            if token not in claude_text:
                errors.append(f"native.claude-feature-discovery-routing: CLAUDE.md lacks {token!r}")
        for token in ("writing-plans", "15–30", "inline spec"):
            if token not in claude_text:
                errors.append(f"native.claude-writing-plans-routing: CLAUDE.md lacks {token!r}")
        for token in ("test-driven-task", "test ladder", "behavior/bugs"):
            if token not in claude_text:
                errors.append(f"native.claude-tdd-routing: CLAUDE.md lacks {token!r}")

    plan_playbook = ROOT / "harness" / "playbooks" / "writing-plans.md"
    if plan_playbook.is_file():
        plan_text = plan_playbook.read_text(encoding="utf-8").lower()
        for token in ("compact inline spec", "15–30 minutes", "separate context", "stop/replan", "actual separate consumer", "no ceremonial human approval"):
            if token not in plan_text:
                errors.append(f"native.writing-plans-contract: writing plans lacks {token!r}")
        for token in ("direct-trivial gate", "no sdd", "one color", "no product behavior", "do not create a feature brief", "no spec", "promote"):
            if token not in plan_text:
                errors.append(f"native.direct-trivial-contract: writing plans lacks {token!r}")
    for item in (".agents/skills/writing-plans/SKILL.md", ".claude/skills/writing-plans/SKILL.md"):
        path = ROOT / item
        if path.is_file():
            skill_text = path.read_text(encoding="utf-8").lower()
            for token in ("automatically use", "compact inline spec", "15–30 minutes", "self-contained `task.md`", "separate executor", "request spec revision"):
                if token not in skill_text:
                    errors.append(f"native.writing-plans-skill: {item} lacks {token!r}")
            for token in ("direct-trivial", "without loading planning artifacts", "spec/task", "tdd", "review"):
                if token not in skill_text:
                    errors.append(f"native.direct-trivial-planning-skill: {item} lacks {token!r}")

    tdd_playbook = ROOT / "harness" / "playbooks" / "test-driven-execution.md"
    if tdd_playbook.is_file():
        tdd_text = tdd_playbook.read_text(encoding="utf-8").lower()
        for token in ("red → green → refactor", "meaningful failure", "identical focused command", "not valid red", "needs-replan", "inside one task", "test ladder"):
            if token not in tdd_text:
                errors.append(f"native.tdd-contract: TDD workflow lacks {token!r}")
    for item in (".agents/skills/test-driven-task/SKILL.md", ".claude/skills/test-driven-task/SKILL.md"):
        path = ROOT / item
        if path.is_file():
            skill_text = path.read_text(encoding="utf-8").lower()
            for token in ("automatically use", "before observing red", "fails for the wrong reason", "minimum behavior required for green", "same small task", "record red", "simplicity, deadline, hackathon mode"):
                if token not in skill_text:
                    errors.append(f"native.tdd-skill: {item} lacks {token!r}")
            for token in ("direct-trivial", "vibe", "focused deterministic check", "promote", "full-harness"):
                if token not in skill_text:
                    errors.append(f"native.fast-route-tdd-skill: {item} lacks {token!r}")

    status_doc = ROOT / "docs" / "STATUS-AND-COMPLETION.md"
    if status_doc.is_file():
        status_text = status_doc.read_text(encoding="utf-8").lower()
        for token in ("fast-route exception", "direct-trivial", "vibe", "never becomes a task or graph event", "do not emit an intermediate status update", "concise closeout", "passing focused deterministic check", "promotion"):
            if token not in status_text:
                errors.append(f"native.fast-route-status: status policy lacks {token!r}")
    for adapter_name in ("generic.md", "codex.md", "claude.md"):
        adapter_text = (ROOT / "adapters" / adapter_name).read_text(encoding="utf-8").lower()
        if "direct-trivial" not in adapter_text or "no" not in adapter_text:
            errors.append(f"native.direct-trivial-adapter: adapters/{adapter_name}")

    hackathon_playbook = ROOT / "harness" / "playbooks" / "hackathon-delivery.md"
    hackathon_doc = ROOT / "docs" / "HACKATHON-MODE.md"
    if hackathon_playbook.is_file() and hackathon_doc.is_file():
        hackathon_text = (hackathon_playbook.read_text(encoding="utf-8") + hackathon_doc.read_text(encoding="utf-8")).lower()
        for token in ("at most two", "vertical slice", "demo-rehearsal", "frontend", "backend", "write_set", "light independent review", "no third loop", "post-mvp"):
            if token not in hackathon_text:
                errors.append(f"native.hackathon-contract: hackathon workflow lacks {token!r}")
    for item in (".agents/skills/first-run-discovery/SKILL.md", ".claude/skills/first-run-discovery/SKILL.md"):
        path = ROOT / item
        if path.is_file():
            skill_text = path.read_text(encoding="utf-8").lower()
            for token in ("hackathon", "at most two", "demo-first graph", "workstream/agent/context"):
                if token not in skill_text:
                    errors.append(f"native.hackathon-discovery-skill: {item} lacks {token!r}")

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
        for token in ("first-response handshake", "agent harness kit is active", "organizes project context, pending work, and verifiable execution", "standard delivery", "hackathon mode", "time-boxed mvp/demo", "highest-leverage unanswered", "empty or effectively empty", "do not propose a product", "localize the wording"):
            if token not in first_run_text:
                errors.append(f"native.first-run-handshake: first-run playbook lacks {token!r}")
    for item in (".agents/skills/first-run-discovery/SKILL.md", ".claude/skills/first-run-discovery/SKILL.md"):
        path = ROOT / item
        if path.is_file():
            skill_text = path.read_text(encoding="utf-8").lower()
            for token in ("agent harness kit is active", "standard delivery", "hackathon mode", "time-boxed mvp/demo", "highest-leverage unanswered", "empty", "do not propose"):
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

    spec_review_surfaces = (
        "AGENTS.md",
        "CLAUDE.md",
        "adapters/codex.md",
        "adapters/claude.md",
        ".agents/skills/governed-review/SKILL.md",
        ".claude/skills/governed-review/SKILL.md",
        ".claude/agents/independent-reviewer.md",
        "harness/playbooks/review-integration.md",
        "harness/roles/reviewer-integrator.md",
    )
    for item in spec_review_surfaces:
        path = ROOT / item
        if not path.is_file():
            continue
        review_text = path.read_text(encoding="utf-8").lower()
        if "fresh" not in review_text or "spec" not in review_text:
            errors.append(f"native.spec-review-routing: {item} must require fresh-context SPEC-led review")
        if "prompt" not in review_text and "conversation" not in review_text:
            errors.append(f"native.review-memory-boundary: {item} must reject prompt/conversation memory as review authority")
    review_playbook = ROOT / "harness" / "playbooks" / "review-integration.md"
    if review_playbook.is_file():
        review_text = review_playbook.read_text(encoding="utf-8").lower()
        for token in ("spawn_subagent", "same-context", "minimal immutable review packet", "before inspecting implementation", "original user prompt", "another fresh, focused review context"):
            if token not in review_text:
                errors.append(f"native.spec-review-contract: review integration lacks {token!r}")

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
        if not any(token in lowered for token in ("complete", "completed")) or "non-block" not in lowered:
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
            "docs/PRODUCT.md", "docs/ARCHITECTURE.md", "docs/VALIDATION.md", "docs/ADAPTIVE-EXECUTION.md", "docs/RUNTIME-STATE.md", "docs/DISTRIBUTION.md",
            "docs/TDD.md", "docs/MODEL-ROUTING.md", "docs/EXECUTION-BUDGET.md", "docs/REVIEW-ROUNDS.md", "docs/CHANGE-INTEGRATION.md", "docs/CONTEXT-ROUTING.md", "docs/STATUS-AND-COMPLETION.md", "docs/EMBEDDED-INSTALLATION.md", "docs/contracts/REQUEST-ROUTE.md", "docs/contracts/FEATURE-BRIEF.md", "docs/contracts/IMPLEMENTATION-PLAN.md", "docs/contracts/MODEL-DISPATCH.md", "docs/contracts/CODEX-AGENT-DISPATCH.md", "docs/contracts/PARALLEL-DISPATCH.md", "docs/contracts/REVIEW.md", "docs/contracts/PENDING.md", "docs/contracts/STATUS.md", "docs/contracts/EXECUTION-BUDGET.md",
            "harness/playbooks/request-routing.md", "harness/playbooks/first-run.md", "harness/playbooks/feature-discovery.md", "harness/playbooks/writing-plans.md", "harness/playbooks/test-driven-execution.md", "harness/playbooks/status-resume.md", "harness/playbooks/task-closeout.md", "harness/playbooks/model-routing.md", "harness/playbooks/context-routing.md", "harness/playbooks/frontend-screen.md", "harness/templates/REQUEST-ROUTE.md", "harness/templates/PROJECT-CONTEXT.md", "harness/templates/FEATURE-BRIEF.md", "harness/templates/IMPLEMENTATION-PLAN.md",
            "harness/templates/PENDING.md", "harness/templates/TASK-GRAPH.md", "harness/templates/STATUS.md", "harness/templates/MODEL-ROUTING.md", "harness/templates/MODEL-DISPATCH.md", "harness/templates/CODEX-AGENT-DISPATCH.md", "harness/templates/PARALLEL-DISPATCH.md", "harness/templates/EXECUTION-BUDGET.md", "harness/templates/ROOT-AGENTS-BRIDGE.md", "harness/templates/ROOT-CLAUDE-BRIDGE.md", "agent_harness_kit/preflight.py", "agent_harness_kit/state_runtime.py", "agent_harness_kit/scheduler.py", "tools/validate.py", "tools/package.py", "tools/install.py", "validation/test_install.py", "validation/test_installed_host_smoke.py", "validation/test_validate_cli.py", "validation/test_preflight.py", "validation/test_state_runtime.py", "validation/test_model_dispatch.py", "validation/test_scheduler.py", "validation/test_parallel_dispatch.py", "validation/test_codex_dispatch.py", "validation/test_codex_agent_dispatch_validation.py", "validation/budget-fixtures/valid.json", "validation/model-dispatch-fixtures/valid.json", "validation/parallel-dispatch-fixtures/valid.json", "validation/codex-agent-dispatch-fixtures/valid.json", "benchmarks/fullstack/scripts/run_pilot.py", "benchmarks/fullstack/tests/test_run_pilot.py",
            ".agents/skills/request-router/SKILL.md",
            ".agents/skills/first-run-discovery/SKILL.md",
            ".agents/skills/feature-discovery/SKILL.md",
            ".agents/skills/writing-plans/SKILL.md",
            ".agents/skills/test-driven-task/SKILL.md",
            ".agents/skills/graph-execution/SKILL.md",
            ".agents/skills/governed-review/SKILL.md",
            ".agents/skills/codex-agent-dispatch/SKILL.md",
            ".agents/skills/parallel-dispatch/SKILL.md",
            ".agents/skills/frontend-screen/SKILL.md",
            ".claude/skills/request-router/SKILL.md",
            ".claude/skills/first-run-discovery/SKILL.md",
            ".claude/skills/feature-discovery/SKILL.md",
            ".claude/skills/writing-plans/SKILL.md",
            ".claude/skills/test-driven-task/SKILL.md",
            ".claude/skills/graph-execution/SKILL.md",
            ".claude/skills/governed-review/SKILL.md",
            ".claude/skills/parallel-dispatch/SKILL.md",
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
                errors.extend(audio_attachment_errors(track))
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
                    actual = content_sha256(path.read_bytes(), normalize_text=field == "script")
                    if expected != actual:
                        errors.append(f"media.manifest-hash: {language} {field}")
                if track.get("status") in {"candidate-awaiting-audition", "approved"} and track.get("script_synced") is not True:
                    errors.append(f"media.manifest-script-sync: {language}")
    for path in markdown_files():
        errors.extend(validate_markdown(path))
        text = path.read_text(encoding="utf-8")
        header = frontmatter(text)
        if header.get("schema") == "harness.project-context/v1":
            mode = header.get("mode")
            if mode not in {"delivery", "delivery+learning", "hackathon", "hackathon+learning"}:
                errors.append(f"project-context.mode: {rel(path)}")
            if mode in {"hackathon", "hackathon+learning"}:
                delivery_shape = re.search(r"^## Delivery shape\s*$([\s\S]*?)(?=^## |\Z)", text, re.MULTILINE)
                required_hackathon = ("deadline/timebox", "primary demo path", "demo audience/environment", "acceptable shortcuts", "post-mvp")
                if not delivery_shape or any(token not in delivery_shape.group(1).lower() for token in required_hackathon):
                    errors.append(f"project-context.hackathon-shape: {rel(path)}")
        if header.get("schema") == "harness.task/v1":
            required_planning = {"planning_mode", "implementation_plan", "plan_step", "target_minutes"}
            if missing := required_planning - set(header):
                errors.append(f"task.spec-planning-fields: {rel(path)} missing {sorted(missing)}")
            planning_mode = header.get("planning_mode")
            try:
                target_minutes = int(header.get("target_minutes", "0"))
            except ValueError:
                target_minutes = 0
            if planning_mode == "planned":
                if header.get("implementation_plan") in {None, "", "none"} or header.get("plan_step") in {None, "", "inline"}:
                    errors.append(f"task.plan-provenance: {rel(path)} planned work must pin plan revision and step")
                if not 15 <= target_minutes <= 30:
                    errors.append(f"task.plan-duration: {rel(path)} planned unit must target 15-30 active minutes")
            elif planning_mode == "inline-simple":
                if header.get("implementation_plan") != "none" or header.get("plan_step") != "inline":
                    errors.append(f"task.simple-provenance: {rel(path)} inline-simple must use none/inline provenance")
                if not 1 <= target_minutes <= 5:
                    errors.append(f"task.simple-duration: {rel(path)} inline-simple unit must target at most 5 active minutes")
            else:
                errors.append(f"task.planning-mode: {rel(path)}")
            required_spec_sections = {"Executable spec", "Non-goals", "Stop and replan", "Acceptance criteria", "Verification"}
            if not required_spec_sections <= headings(text):
                errors.append(f"task.executable-spec: {rel(path)} lacks complete executable spec sections")
            test_strategy = header.get("test_strategy")
            tdd_exception = header.get("tdd_exception")
            if test_strategy not in {"tdd", "characterization", "verification-only"}:
                errors.append(f"task.test-strategy: {rel(path)}")
            if test_strategy == "tdd" and tdd_exception != "none":
                errors.append(f"task.tdd-exception: {rel(path)} TDD must use exception none")
            if test_strategy in {"characterization", "verification-only"} and tdd_exception in {None, "", "none"}:
                errors.append(f"task.tdd-exception: {rel(path)} non-TDD strategy requires an exact reason")
            if "Test-first cycle" not in headings(text):
                errors.append(f"task.test-first-cycle: {rel(path)}")
            if test_strategy == "tdd":
                test_first = re.search(r"^## Test-first cycle\s*$([\s\S]*?)(?=^## |\Z)", text, re.MULTILINE)
                required_tdd = ("red test/path:", "red command:", "expected red:", "green change:", "green command:", "refactor boundary:", "proportional regression:")
                if not test_first or any(token not in test_first.group(1).lower() for token in required_tdd):
                    errors.append(f"task.tdd-spec: {rel(path)} lacks RED/GREEN/refactor/regression specification")
            evidence_profile = header.get("evidence_profile")
            errors.extend(validate_task_evidence_profile(header, rel(path)))
            if header.get("assurance") not in {"none", "light", "full"}:
                errors.append(f"task.assurance: {rel(path)}")
            if header.get("artifact_policy") not in {"inline", "transfer"}:
                errors.append(f"task.artifact-policy: {rel(path)}")
            if header.get("handoff_consumer") not in {"none", "reviewer", "human"}:
                errors.append(f"task.handoff-consumer: {rel(path)}")
            if header.get("artifact_policy") == "inline" and header.get("handoff_consumer") != "none":
                errors.append(f"task.inline-consumer: {rel(path)} inline work cannot create a transfer consumer")
            if header.get("test_ladder") not in {"focused-edit", "focused-unit", "workspace", "integration", "global-checkpoint", "release-full"}:
                errors.append(f"task.test-ladder: {rel(path)}")
            if evidence_profile != "graph-only" and header.get("review_profile") not in {"light", "standard", "critical"}:
                errors.append(f"review.profile: {rel(path)}")
            if evidence_profile != "graph-only" and header.get("max_review_rounds") not in {"1", "2"}:
                errors.append(f"review.round-budget: {rel(path)} must be 1 or 2")
            if header.get("assurance_gate") not in {"none", "affected-actions"}:
                errors.append(f"review.assurance-gate: {rel(path)}")
            if header.get("review_profile") == "critical" and header.get("assurance_gate") != "affected-actions":
                errors.append(f"review.critical-gate: {rel(path)} critical work must gate affected actions")
            if header.get("status") == "active" and header.get("model_dispatch") in {None, "", "none", "pending", "unknown", "host-default"}:
                errors.append(f"task.model-dispatch: {rel(path)} active task must pin resolved dispatch evidence")
        if header.get("schema") == "harness.implementation-plan/v1":
            if header.get("status") not in {"draft", "ready", "superseded"}:
                errors.append(f"plan.status: {rel(path)}")
            plan_text = text.lower()
            for token in ("target active work: 15–30 minutes", "exact change:", "write set:", "acceptance:", "verification:", "stop/replan if:"):
                if token not in plan_text:
                    errors.append(f"plan.unit-spec: {rel(path)} lacks {token!r}")
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
            if header.get("spec_authority") != header.get("task"):
                errors.append(f"review.spec-authority: {rel(path)} must equal the pinned task revision")
            if header.get("review_context") != "isolated-fresh":
                errors.append(f"review.fresh-context: {rel(path)}")
            if header.get("prompt_source") != "task-spec-only":
                errors.append(f"review.prompt-source: {rel(path)}")
            if any(header.get(field) in {None, "", "none"} for field in ("review_packet", "review_context_ref")):
                errors.append(f"review.context-evidence: {rel(path)}")
            if header.get("verdict") not in {"accept", "changes-requested", "rejected", "needs-replan"}:
                errors.append(f"review.verdict: {rel(path)} must use the normalized v0.7 verdict enum")
            for field in ("findings", "evidence", "commands", "duration_ms", "tokens"):
                if field not in header:
                    errors.append(f"review.metrics-field: {rel(path)} missing {field}")
        if header.get("schema") == "harness.handoff/v1":
            if header.get("status") not in {"completed", "blocked", "failed"}:
                errors.append(f"handoff.status: {rel(path)} must be completed, blocked, or failed")
            closeout = re.search(r"^## User-facing closeout\s*$([\s\S]*?)(?=^## |\Z)", text, re.MULTILINE)
            required_labels = ("Stage:", "Progress:", "Blockers:", "Next action:", "Inspectable paths:", "Human action required:")
            if not closeout or any(label not in closeout.group(1) for label in required_labels):
                errors.append(f"handoff.closeout-fields: {rel(path)}")
            if "Test-first evidence" not in headings(text):
                errors.append(f"handoff.test-first-evidence: {rel(path)}")
            if header.get("consumer") not in {"reviewer", "human"}:
                errors.append(f"handoff.consumer: {rel(path)} must name a real separate consumer")
            for field in ("model_id_used", "reasoning_effort_used", "model_dispatch"):
                if header.get(field) in {None, "", "none", "pending", "unknown", "host-default"}:
                    errors.append(f"handoff.model-dispatch: {rel(path)} missing {field}")
        if header.get("schema") == "harness.model-dispatch/v1" and "harness/templates" not in rel(path):
            required = MODEL_DISPATCH_FIELDS | {"created_at", "created_by"}
            if missing := required - set(header):
                errors.append(f"model-dispatch.markdown-fields: {rel(path)} missing {sorted(missing)}")
            if header.get("status") == "resolved":
                for field in ("selected_model", "reasoning_effort", "execution_context_ref", "dispatch_evidence"):
                    if str(header.get(field, "")).strip().lower() in MODEL_EVIDENCE_PLACEHOLDERS:
                        errors.append(f"model-dispatch.markdown-evidence: {rel(path)} unresolved {field}")
                if header.get("dispatch_surface") not in MODEL_OVERRIDE_SURFACES:
                    errors.append(f"model-dispatch.markdown-surface: {rel(path)}")
                if header.get("override_requested") != "true" or header.get("override_confirmed") != "true":
                    errors.append(f"model-dispatch.markdown-confirmation: {rel(path)}")
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
        if readme.exists():
            readme_text = readme.read_text(encoding="utf-8")
            attachment_urls = re.findall(r"^https://github\.com/user-attachments/assets/[0-9a-f-]{36}$", readme_text, re.MULTILINE)
            is_portuguese = readme.name == "README.pt-BR.md"
            language = "pt-BR" if is_portuguese else "en"
            manifest_tracks = {
                track.get("language"): track for track in audio_manifest.get("tracks", [])
                if isinstance(track, dict)
            }
            expected_attachment = manifest_tracks.get(language, {}).get("github_attachment")
            expected_audio = "media/agent-harness-kit-overview-pt-BR.mp3" if is_portuguese else "media/agent-harness-kit-overview-en.mp3"
            expected_player = "media/agent-harness-kit-overview-pt-BR.mp4" if is_portuguese else "media/agent-harness-kit-overview-en.mp4"
            expected_script = "media/overview-script-pt-BR.txt" if is_portuguese else "media/overview-script-en.txt"
            other_audio = "media/agent-harness-kit-overview-en.mp3" if is_portuguese else "media/agent-harness-kit-overview-pt-BR.mp3"
            other_script = "media/overview-script-en.txt" if is_portuguese else "media/overview-script-pt-BR.txt"
            expected_urls = [expected_attachment] if expected_attachment else []
            if attachment_urls != expected_urls:
                errors.append(f"media.readme-player: {rel(readme)} has a stale or mismatched GitHub attachment player")
            if any(f"]({asset})" not in readme_text for asset in (expected_audio, expected_player, expected_script)):
                errors.append(f"media.readme-language-assets: {rel(readme)} missing its language-specific MP3, MP4, or script")
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
            if "first-run discovery interview automatically" not in bridge_text:
                errors.append(f"embedded.first-run-route: {rel(bridge)} must trigger automatic discovery from the root entrypoint")
            bridge_lower = bridge_text.lower()
            for token in ("mandatory context-routing gate", "before any scan", "status: approved", "do not emit the first-run welcome", "status/resume", "stop", "substantive project request", "exactly one", "prior conversations", "agent harness kit is active", "standard delivery", "hackathon mode", "time-boxed mvp/demo", "registered mentally", "path/revision"):
                if token not in bridge_lower:
                    errors.append(f"embedded.first-response-salience: {rel(bridge)} lacks {token!r}")
            if bridge_lower.find("status: approved") > bridge_lower.find("first-run discovery interview automatically"):
                errors.append(f"embedded.approved-resume-priority: {rel(bridge)} must route approved context before first-run discovery")
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
    errors.extend(validate_parallel_dispatch_fixtures())
    errors.extend(validate_model_dispatch_fixtures())
    errors.extend(validate_codex_agent_dispatch_fixtures())
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


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate Agent Harness Kit source or a namespaced host adoption")
    parser.add_argument("--host-root", type=Path)
    parser.add_argument("--migration-manifest", type=Path)
    parser.add_argument("--scope", choices=("repository", "changed", "task"), default="repository")
    parser.add_argument("--task", type=Path)
    args = parser.parse_args(argv)
    if bool(args.host_root) != bool(args.migration_manifest):
        parser.error("--host-root and --migration-manifest must be provided together")
    if args.scope == "task" and args.task is None:
        parser.error("--scope task requires --task PATH")
    if args.task is not None and args.scope != "task":
        parser.error("--task PATH requires --scope task")
    if args.host_root:
        host_errors = validate_host_integration(args.host_root.resolve(), args.migration_manifest)
        if host_errors:
            print(f"HOST INTEGRATION VALIDATION FAILED ({len(host_errors)} error(s))")
            print(f"ERROR CATEGORIES: {summarize_error_categories(host_errors)}")
            for error in host_errors:
                print(f"- {error}")
            return 1
        print("HOST INTEGRATION VALIDATION PASSED: migration coverage, backlinks, snapshot identities, and cutover gates")
        return 0
    try:
        selection = resolve_scope(args.scope, args.task)
    except ScopeError as exc:
        print(f"VALIDATION SCOPE ERROR: {exc}")
        return 2
    if selection.escalated:
        print("VALIDATION SCOPE: changed -> repository (foundational validator/profile/entrypoint change)")
    errors = scoped_errors(validate_repository(), selection.paths)
    if errors:
        print(f"VALIDATION FAILED ({len(errors)} error(s))")
        print(f"ERROR CATEGORIES: {summarize_error_categories(errors)}")
        for error in errors:
            print(f"- {error}")
        return 1
    selected_markdown = markdown_files()
    if selection.paths is not None:
        selected_markdown = [path for path in selected_markdown if rel(path) in selection.paths]
    required_count = selected_required_count(load_package_manifest(), selection.paths)
    print(f"VALIDATION PASSED: {len(selected_markdown)} Markdown files, {required_count} required files")
    if selection.effective_scope != "repository":
        print(f"Validation scope: {selection.effective_scope}, {len(selection.paths or set())} selected path(s)")
    print("Graph fixtures: valid, missing dependency, cycle, write/context collision, self-review, and path traversal")
    print("Parallel dispatch fixtures: capacity, runtime evidence, distinct contexts, and collision-safe batches")
    print("Model dispatch fixtures: resolved override evidence, recorded-tier-only, silent default, and same-context claim")
    print("Codex agent dispatch fixtures: minimal context, runtime response, resolved model, and reviewer separation")
    print("Status mutation fixtures: required fields, human-source provenance, and safe inspectable paths")
    print("Review mutation fixtures: SPEC authority, fresh context, prompt-memory exclusion, and focused round-two boundaries")
    print("Execution budget fixtures: attempt, no-progress, context-expansion, lineage, and path ceilings")
    print("Host fixtures: namespaced adoption, missing backlink, silent omission, stale snapshot, and premature cutover")
    print("Native integration: pre-ceremony four-lane request routing plus Codex/Claude dispatch, feature/planning/TDD/SPEC-led review/frontend/learning/context routing, safe defaults, and profile boundaries")
    print("Language boundary: README.pt-BR.md is the only Portuguese-content exception")
    return 0


if __name__ == "__main__":
    sys.exit(main())
