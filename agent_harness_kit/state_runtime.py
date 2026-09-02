"""Durable runtime-state primitives for Agent Harness Kit.

The module deliberately uses only the standard library.  Graph mutations are
serialized per resolved path and committed by replacing a fully flushed
temporary file in the same directory.  JSONL ledgers are append-only and are
flushed to stable storage before returning.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
import threading
import uuid
from collections import Counter, defaultdict
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping


EVENT_SCHEMA = "harness.runtime-event/v1"
METRIC_SCHEMA = "harness.runtime-metric/v1"


class StateRuntimeError(RuntimeError):
    """Base class for runtime-state failures."""


class RevisionConflictError(StateRuntimeError):
    """The graph changed after the caller read it."""


class IllegalTransitionError(StateRuntimeError):
    """A requested task lifecycle transition is not permitted."""


class CorruptLedgerError(StateRuntimeError):
    """A JSONL ledger is torn, malformed, or has an invalid hash chain."""


class DuplicateEventError(StateRuntimeError):
    """An event ID was reused with different content."""


_LOCKS_GUARD = threading.Lock()
_PATH_LOCKS: dict[str, threading.RLock] = {}
_LEGAL_TRANSITIONS = {
    "pending": {"ready", "blocked"},
    "ready": {"active", "blocked"},
    "active": {"completed", "blocked"},
    "blocked": {"pending", "ready"},
    "completed": set(),
}
_RELEASE_FIELDS = (
    "lease", "lease_id", "context", "agent_context", "execution_context",
    "thread_ref", "assigned_to", "agent",
)
_VALID_REVIEW_VERDICTS = {
    None, "accept", "changes-requested", "rejected", "needs-replan", "not-required", "pending",
}


def _path_lock(path: Path) -> threading.RLock:
    key = os.path.normcase(str(path.resolve()))
    with _LOCKS_GUARD:
        return _PATH_LOCKS.setdefault(key, threading.RLock())


@contextmanager
def _interprocess_lock(path: Path):
    """Serialize writers across real agent processes using a sibling lock file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    lock_path = path.with_name(f".{path.name}.lock")
    with lock_path.open("a+b") as stream:
        stream.seek(0, os.SEEK_END)
        if stream.tell() == 0:
            stream.write(b"\0")
            stream.flush()
        stream.seek(0)
        if os.name == "nt":
            import msvcrt

            msvcrt.locking(stream.fileno(), msvcrt.LK_LOCK, 1)
            try:
                yield
            finally:
                stream.seek(0)
                msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
        else:
            import fcntl

            fcntl.flock(stream.fileno(), fcntl.LOCK_EX)
            try:
                yield
            finally:
                fcntl.flock(stream.fileno(), fcntl.LOCK_UN)


def _utc_timestamp(value: str | datetime | None = None) -> str:
    if value is None:
        value = datetime.now(timezone.utc)
    if isinstance(value, str):
        return value
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _canonical_json(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
    ).encode("utf-8")


def _sha256(value: Any) -> str:
    return hashlib.sha256(_canonical_json(value)).hexdigest()


def _atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", newline="", dir=path.parent,
            prefix=f".{path.name}.", suffix=".tmp", delete=False,
        ) as stream:
            temp_name = stream.name
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp_name, path)
        temp_name = None
        if os.name != "nt":
            directory_fd = os.open(path.parent, os.O_RDONLY)
            try:
                os.fsync(directory_fd)
            finally:
                os.close(directory_fd)
    finally:
        if temp_name is not None:
            try:
                os.unlink(temp_name)
            except FileNotFoundError:
                pass


def _validate_transition(current: str, requested: str) -> None:
    if current not in _LEGAL_TRANSITIONS:
        raise IllegalTransitionError(f"unknown current lifecycle state: {current!r}")
    if requested not in _LEGAL_TRANSITIONS[current]:
        raise IllegalTransitionError(f"illegal lifecycle transition: {current} -> {requested}")


def _task_from_json(graph: dict[str, Any], task_id: str) -> dict[str, Any]:
    collection = graph.get("tasks", graph.get("nodes"))
    if isinstance(collection, dict):
        task = collection.get(task_id)
        if isinstance(task, dict):
            return task
    elif isinstance(collection, list):
        for candidate in collection:
            if isinstance(candidate, dict) and candidate.get("id", candidate.get("task_id")) == task_id:
                return candidate
    raise KeyError(f"task not found: {task_id}")


def _release_ownership(task: dict[str, Any]) -> None:
    for field in _RELEASE_FIELDS:
        if field in task:
            task[field] = None


def _transition_entry(
    task_id: str, previous: str, requested: str, revision: int,
    actor: str, context: str, timestamp: str, reason: str | None,
) -> dict[str, Any]:
    entry = {
        "revision": revision,
        "task": task_id,
        "from": previous,
        "to": requested,
        "actor": actor,
        "context": context,
        "timestamp": timestamp,
    }
    if reason is not None:
        entry["reason"] = reason
    return entry


def _transition_json(
    content: str, task_id: str, requested: str, expected_revision: int,
    actor: str, context: str, timestamp: str, reason: str | None,
) -> tuple[str, dict[str, Any]]:
    try:
        graph = json.loads(content)
    except (TypeError, json.JSONDecodeError) as exc:
        raise StateRuntimeError("TASK-GRAPH JSON is malformed") from exc
    if not isinstance(graph, dict):
        raise StateRuntimeError("TASK-GRAPH JSON root must be an object")
    current_revision = graph.get("revision")
    if current_revision != expected_revision:
        raise RevisionConflictError(
            f"expected graph revision {expected_revision}, found {current_revision}"
        )
    task = _task_from_json(graph, task_id)
    previous = task.get("status")
    _validate_transition(previous, requested)
    resulting_revision = expected_revision + 1
    task["status"] = requested
    if requested in {"completed", "blocked"}:
        _release_ownership(task)
    graph["revision"] = resulting_revision
    graph["updated_at"] = timestamp
    graph["updated_by"] = actor
    log_key = "transitions" if "transitions" in graph else "transition_log"
    log = graph.setdefault(log_key, [])
    if not isinstance(log, list):
        raise StateRuntimeError(f"{log_key} must be a list")
    log.append(_transition_entry(
        task_id, previous, requested, resulting_revision, actor, context,
        timestamp, reason,
    ))
    return json.dumps(graph, indent=2, ensure_ascii=False) + "\n", graph


def _frontmatter_revision(lines: list[str]) -> tuple[int, int]:
    if not lines or lines[0].strip() != "---":
        raise StateRuntimeError("TASK-GRAPH Markdown needs YAML frontmatter")
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            break
        match = re.match(r"^(\s*revision\s*:\s*)(\d+)(\s*)$", lines[index])
        if match:
            return index, int(match.group(2))
    raise StateRuntimeError("TASK-GRAPH Markdown frontmatter has no numeric revision")


def _replace_frontmatter_value(lines: list[str], key: str, value: str) -> None:
    end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if end is None:
        raise StateRuntimeError("unterminated TASK-GRAPH Markdown frontmatter")
    pattern = re.compile(rf"^(\s*{re.escape(key)}\s*:\s*).*$")
    for index in range(1, end):
        match = pattern.match(lines[index])
        if match:
            lines[index] = match.group(1) + value
            return
    lines.insert(end, f"{key}: {value}")


def _transition_markdown(
    content: str, task_id: str, requested: str, expected_revision: int,
    actor: str, context: str, timestamp: str, reason: str | None,
) -> tuple[str, dict[str, Any]]:
    lines = content.splitlines()
    revision_line, current_revision = _frontmatter_revision(lines)
    if current_revision != expected_revision:
        raise RevisionConflictError(
            f"expected graph revision {expected_revision}, found {current_revision}"
        )

    previous = None
    json_block = re.search(r"```json\s*\n(.*?)\n```", content, re.DOTALL)
    if json_block:
        try:
            executable = json.loads(json_block.group(1))
        except json.JSONDecodeError as exc:
            raise StateRuntimeError("TASK-GRAPH Markdown executable JSON is malformed") from exc
        if not isinstance(executable, dict):
            raise StateRuntimeError("TASK-GRAPH Markdown executable JSON root must be an object")
        task = _task_from_json(executable, task_id)
        previous = task.get("status")
        _validate_transition(previous, requested)
        task["status"] = requested
        if requested in {"completed", "blocked"}:
            _release_ownership(task)
        replacement = "```json\n" + json.dumps(executable, indent=2, ensure_ascii=False) + "\n```"
        content = content[:json_block.start()] + replacement + content[json_block.end():]
        lines = content.splitlines()
        revision_line, _ = _frontmatter_revision(lines)
    else:
        header_index = None
        id_column = status_column = agent_column = None
        for index, line in enumerate(lines):
            if not line.lstrip().startswith("|"):
                continue
            cells = [cell.strip().lower() for cell in line.strip().strip("|").split("|")]
            if "id" in cells and "status" in cells:
                header_index = index
                id_column, status_column = cells.index("id"), cells.index("status")
                agent_column = cells.index("agent/context") if "agent/context" in cells else None
                break
        if header_index is None or id_column is None or status_column is None:
            raise StateRuntimeError("TASK-GRAPH Markdown executable JSON block or task table was not found")
        task_line = None
        for index in range(header_index + 2, len(lines)):
            line = lines[index]
            if not line.lstrip().startswith("|"):
                break
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if id_column < len(cells) and cells[id_column] == task_id:
                if status_column >= len(cells):
                    raise StateRuntimeError(f"task row has no status cell: {task_id}")
                task_line, previous = index, cells[status_column]
                _validate_transition(previous, requested)
                cells[status_column] = requested
                if requested in {"completed", "blocked"} and agent_column is not None and agent_column < len(cells):
                    cells[agent_column] = "unassigned / released"
                lines[index] = "| " + " | ".join(cells) + " |"
                break
        if task_line is None or previous is None:
            raise KeyError(f"task not found: {task_id}")

    resulting_revision = expected_revision + 1
    prefix_match = re.match(r"^(\s*revision\s*:\s*)", lines[revision_line])
    lines[revision_line] = (prefix_match.group(1) if prefix_match else "revision: ") + str(resulting_revision)
    _replace_frontmatter_value(lines, "updated_at", timestamp)
    _replace_frontmatter_value(lines, "updated_by", actor)

    heading = next(
        (i for i, line in enumerate(lines) if re.match(r"^##\s+Transition log\s*$", line, re.I)),
        None,
    )
    if heading is None:
        lines.extend(["", "## Transition log"])
        heading = len(lines) - 1
    reason_text = f"; {reason}" if reason else ""
    entry_text = (
        f"- r{resulting_revision}: {task_id} {previous} → {requested}; "
        f"actor `{actor}`; context `{context}`; {timestamp}{reason_text}"
    )
    insert_at = heading + 1
    while insert_at < len(lines) and (not lines[insert_at].startswith("## ")):
        insert_at += 1
    lines.insert(insert_at, entry_text)
    result = _transition_entry(
        task_id, previous, requested, resulting_revision, actor, context,
        timestamp, reason,
    )
    return "\n".join(lines) + "\n", {"revision": resulting_revision, "transition": result}


def transition_task_graph(
    path: str | os.PathLike[str], task: str, to_status: str,
    expected_revision: int, actor: str, context: str, *,
    reason: str | None = None, timestamp: str | datetime | None = None,
) -> dict[str, Any]:
    """CAS-transition one task in a JSON or Markdown TASK-GRAPH atomically."""
    graph_path = Path(path)
    requested = to_status.strip().lower()
    stamp = _utc_timestamp(timestamp)
    with _path_lock(graph_path):
        with _interprocess_lock(graph_path):
            content = graph_path.read_text(encoding="utf-8")
            if graph_path.suffix.lower() == ".json":
                updated, result = _transition_json(
                    content, task, requested, expected_revision, actor, context,
                    stamp, reason,
                )
            elif graph_path.suffix.lower() in {".md", ".markdown"}:
                updated, result = _transition_markdown(
                    content, task, requested, expected_revision, actor, context,
                    stamp, reason,
                )
            else:
                raise ValueError("TASK-GRAPH path must use .json, .md, or .markdown")
            _atomic_write(graph_path, updated)
            return result


def _read_jsonl(path: Path, *, schema: str | None = None) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    raw = path.read_bytes()
    if raw and not raw.endswith(b"\n"):
        raise CorruptLedgerError(f"torn JSONL record in {path}")
    records: list[dict[str, Any]] = []
    for line_number, raw_line in enumerate(raw.splitlines(), 1):
        try:
            record = json.loads(raw_line.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise CorruptLedgerError(f"invalid JSONL record at line {line_number}") from exc
        if not isinstance(record, dict):
            raise CorruptLedgerError(f"JSONL record {line_number} is not an object")
        if schema is not None and record.get("schema") != schema:
            raise CorruptLedgerError(f"unexpected schema at line {line_number}")
        records.append(record)
    return records


def _event_identity(record: Mapping[str, Any]) -> dict[str, Any]:
    return {
        key: value for key, value in record.items()
        if key not in {"previous_hash", "event_hash", "timestamp"}
    }


def _verify_event_chain_unlocked(ledger_path: Path) -> dict[str, Any]:
    records = _read_jsonl(ledger_path, schema=EVENT_SCHEMA)
    previous_hash: str | None = None
    seen_ids: set[str] = set()
    for index, record in enumerate(records, 1):
        event_id = record.get("event_id")
        if not isinstance(event_id, str) or not event_id or event_id in seen_ids:
            raise CorruptLedgerError(f"invalid or duplicate event_id at line {index}")
        seen_ids.add(event_id)
        if record.get("previous_hash") != previous_hash:
            raise CorruptLedgerError(f"broken previous_hash at line {index}")
        if record.get("payload_hash") != _sha256(record.get("payload")):
            raise CorruptLedgerError(f"payload hash mismatch at line {index}")
        claimed_hash = record.get("event_hash")
        material = {key: value for key, value in record.items() if key != "event_hash"}
        if claimed_hash != _sha256(material):
            raise CorruptLedgerError(f"event hash mismatch at line {index}")
        previous_hash = claimed_hash
    return {"valid": True, "event_count": len(records), "head_hash": previous_hash}


def verify_event_chain(path: str | os.PathLike[str]) -> dict[str, Any]:
    """Verify syntax, payload hashes, event hashes, and previous-hash links."""
    ledger_path = Path(path)
    with _path_lock(ledger_path):
        with _interprocess_lock(ledger_path):
            return _verify_event_chain_unlocked(ledger_path)


def append_runtime_event(
    path: str | os.PathLike[str], *, event_id: str, transaction_id: str,
    expected_revision: int, resulting_revision: int, task: str, actor: str,
    context: str, payload: Any, timestamp: str | datetime | None = None,
) -> dict[str, Any]:
    """Append a hash-chained event, treating an identical event ID as idempotent."""
    ledger_path = Path(path)
    stamp = _utc_timestamp(timestamp)
    base = {
        "schema": EVENT_SCHEMA,
        "event_id": event_id,
        "transaction_id": transaction_id,
        "expected_revision": expected_revision,
        "resulting_revision": resulting_revision,
        "task": task,
        "actor": actor,
        "context": context,
        "timestamp": stamp,
        "payload": payload,
        "payload_hash": _sha256(payload),
    }
    with _path_lock(ledger_path):
        with _interprocess_lock(ledger_path):
            report = _verify_event_chain_unlocked(ledger_path)
            records = _read_jsonl(ledger_path, schema=EVENT_SCHEMA)
            for existing in records:
                if existing.get("event_id") == event_id:
                    if _event_identity(existing) == _event_identity(base):
                        return existing
                    raise DuplicateEventError(f"event_id {event_id!r} has different content")
            event = dict(base)
            event["previous_hash"] = report["head_hash"]
            event["event_hash"] = _sha256(event)
            ledger_path.parent.mkdir(parents=True, exist_ok=True)
            with ledger_path.open("a", encoding="utf-8", newline="") as stream:
                stream.write(json.dumps(event, sort_keys=True, ensure_ascii=False) + "\n")
                stream.flush()
                os.fsync(stream.fileno())
            return event


def record_metric(
    path: str | os.PathLike[str], *, lane: str, assurance: str,
    harness_shape: str, artifacts_created: int, ceremony_ms: int,
    implementation_ms: int, human_approvals: int, gate_hits: Iterable[str],
    target_minutes: float, actual_minutes: float,
    host_input_tokens: int | None = None, host_output_tokens: int | None = None,
    host_total_tokens: int | None = None, timestamp: str | datetime | None = None,
    metric_id: str | None = None, **dimensions: Any,
) -> dict[str, Any]:
    """Append one runtime metric record with explicit token availability."""
    metric_path = Path(path)
    token_values = (host_input_tokens, host_output_tokens, host_total_tokens)
    tokens: dict[str, Any]
    if all(value is None for value in token_values):
        tokens = {"status": "unavailable"}
    else:
        tokens = {
            "status": "reported", "input": host_input_tokens,
            "output": host_output_tokens, "total": host_total_tokens,
        }
    record = {
        "schema": METRIC_SCHEMA,
        "metric_id": metric_id or str(uuid.uuid4()),
        "timestamp": _utc_timestamp(timestamp),
        "lane": lane,
        "assurance": assurance,
        "harness_shape": harness_shape,
        "artifacts_created": int(artifacts_created),
        "ceremony_ms": int(ceremony_ms),
        "implementation_ms": int(implementation_ms),
        "human_approvals": int(human_approvals),
        "gate_hits": list(gate_hits),
        "target_minutes": float(target_minutes),
        "actual_minutes": float(actual_minutes),
        "host_tokens": tokens,
        "host_tokens_status": tokens["status"],
        "host_input_tokens": host_input_tokens,
        "host_output_tokens": host_output_tokens,
        "host_total_tokens": host_total_tokens,
        **dimensions,
    }
    with _path_lock(metric_path):
        with _interprocess_lock(metric_path):
            _read_jsonl(metric_path, schema=METRIC_SCHEMA)
            metric_path.parent.mkdir(parents=True, exist_ok=True)
            with metric_path.open("a", encoding="utf-8", newline="") as stream:
                stream.write(json.dumps(record, sort_keys=True, ensure_ascii=False) + "\n")
                stream.flush()
                os.fsync(stream.fileno())
    return record


def summarize_metrics(
    path: str | os.PathLike[str], *, no_gate_threshold: int = 3,
) -> dict[str, Any]:
    """Aggregate runtime metrics into governance and execution signals."""
    if no_gate_threshold < 1:
        raise ValueError("no_gate_threshold must be at least 1")
    metric_path = Path(path)
    with _path_lock(metric_path):
        with _interprocess_lock(metric_path):
            records = _read_jsonl(metric_path, schema=METRIC_SCHEMA)
    count = len(records)
    first_pass_known = [r for r in records if "first_pass_accepted" in r]
    first_pass_accepted = sum(bool(r["first_pass_accepted"]) for r in first_pass_known)
    ceremony = sum(max(0, int(r.get("ceremony_ms", 0))) for r in records)
    implementation = sum(max(0, int(r.get("implementation_ms", 0))) for r in records)
    regression_counts: Counter[str] = Counter()
    for record in records:
        regression_counts.update(str(item) for item in record.get("global_regressions", []))
    repeated = {name: hits for name, hits in regression_counts.items() if hits > 1}
    remediation_count = sum(bool(r.get("remediation")) for r in records)
    revisions_by_task: defaultdict[str, int] = defaultdict(int)
    for record in records:
        if record.get("task") is not None:
            revisions_by_task[str(record["task"])] += int(record.get("graph_revisions", 0))
    overrun_records = [
        r for r in records
        if float(r.get("actual_minutes", 0)) > float(r.get("target_minutes", 0))
    ]
    invalid_verdicts = sum(
        r.get("review_verdict") not in _VALID_REVIEW_VERDICTS for r in records
    )
    gate_counts: Counter[str] = Counter()
    for record in records:
        gate_counts.update(str(item) for item in record.get("gate_hits", []))
    no_gate_streak = 0
    for record in reversed(records):
        if record.get("gate_hits"):
            break
        no_gate_streak += 1
    suggested_lane = None
    if no_gate_streak >= no_gate_threshold and records:
        current = records[-1].get("lane")
        suggested_lane = {
            "full-harness": "graph-only", "graph-only": "vibe", "vibe": "direct-trivial",
        }.get(current)
    total_work = ceremony + implementation
    revision_values = list(revisions_by_task.values())
    return {
        "runs": count,
        "first_pass_acceptance": {
            "accepted": first_pass_accepted,
            "observed": len(first_pass_known),
            "rate": first_pass_accepted / len(first_pass_known) if first_pass_known else None,
        },
        "first_pass_acceptance_inputs": {
            "accepted": first_pass_accepted,
            "rejected": len(first_pass_known) - first_pass_accepted,
            "observed": len(first_pass_known),
            "missing": count - len(first_pass_known),
        },
        "governance_product_ratio": ceremony / implementation if implementation else None,
        "governance_share": ceremony / total_work if total_work else None,
        "time_inputs_ms": {"governance": ceremony, "product": implementation},
        "lane_counts": dict(Counter(str(r.get("lane")) for r in records)),
        "assurance_counts": dict(Counter(str(r.get("assurance")) for r in records)),
        "harness_shape_counts": dict(Counter(str(r.get("harness_shape")) for r in records)),
        "artifacts_created": sum(int(r.get("artifacts_created", 0)) for r in records),
        "human_approvals": sum(int(r.get("human_approvals", 0)) for r in records),
        "gate_hit_counts": dict(sorted(gate_counts.items())),
        "repeated_global_regressions": dict(sorted(repeated.items())),
        "remediation_ratio": remediation_count / count if count else None,
        "graph_revisions_per_task": {
            "by_task": dict(sorted(revisions_by_task.items())),
            "average": sum(revision_values) / len(revision_values) if revision_values else None,
        },
        "invalid_review_verdict_count": invalid_verdicts,
        "target_overrun": {
            "count": len(overrun_records),
            "ratio": len(overrun_records) / count if count else None,
            "minutes": sum(
                float(r.get("actual_minutes", 0)) - float(r.get("target_minutes", 0))
                for r in overrun_records
            ),
        },
        "minutes": {
            "target": sum(float(r.get("target_minutes", 0)) for r in records),
            "actual": sum(float(r.get("actual_minutes", 0)) for r in records),
        },
        "no_gate_streak": no_gate_streak,
        "suggested_lane": suggested_lane,
    }


def evaluate_inactivity(
    last_progress_at: str | datetime, *, now: str | datetime | None = None,
    consecutive_occurrences: int = 0, warning_after_seconds: float = 60,
    declared_long_running_tool_wait: bool = False,
) -> dict[str, Any]:
    """Return continue, warn/checkpoint, or interrupt/reassign policy action."""
    if not 60 <= warning_after_seconds <= 90:
        raise ValueError("warning_after_seconds must be between 60 and 90")

    def parse(value: str | datetime | None) -> datetime:
        if value is None:
            return datetime.now(timezone.utc)
        if isinstance(value, str):
            value = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)

    elapsed = max(0.0, (parse(now) - parse(last_progress_at)).total_seconds())
    if declared_long_running_tool_wait:
        return {"action": "exempt", "elapsed_seconds": elapsed, "occurrences": consecutive_occurrences}
    if elapsed < warning_after_seconds:
        return {"action": "continue", "elapsed_seconds": elapsed, "occurrences": 0}
    occurrences = max(0, int(consecutive_occurrences)) + 1
    action = "interrupt-reassign" if occurrences >= 2 else "warn-checkpoint"
    return {"action": action, "elapsed_seconds": elapsed, "occurrences": occurrences}


__all__ = [
    "CorruptLedgerError", "DuplicateEventError", "EVENT_SCHEMA",
    "IllegalTransitionError", "METRIC_SCHEMA", "RevisionConflictError",
    "StateRuntimeError", "append_runtime_event", "evaluate_inactivity",
    "record_metric", "summarize_metrics", "transition_task_graph",
    "verify_event_chain",
]
