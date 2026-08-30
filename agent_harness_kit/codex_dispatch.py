"""Build and record auditable native Codex subagent dispatches."""

from __future__ import annotations

import re
from typing import Any


class DispatchError(ValueError):
    """Raised when a safe native Codex dispatch cannot be prepared or recorded."""


KNOWN_ROLES = {
    "role:discovery-interviewer": "harness/roles/discovery-interviewer.md",
    "role:orchestrator-po": "harness/roles/orchestrator-po.md",
    "role:task-decomposer": "harness/roles/task-decomposer.md",
    "role:generic-specialist": "harness/roles/generic-specialist.md",
    "role:reviewer-integrator": "harness/roles/reviewer-integrator.md",
    "role:learning-assessor": "harness/roles/learning-assessor.md",
    "role:learning-debriefer-publisher": "harness/roles/learning-debriefer-publisher.md",
}
REASONING_EFFORTS = {"none", "minimal", "low", "medium", "high", "xhigh", "max", "ultra"}
RESPONSE_FIELDS = {
    "agent_id",
    "context_ref",
    "operation_id",
    "accepted_model",
    "accepted_reasoning_effort",
    "status",
    "host_id",
    "revision",
}


def _required_string(data: dict[str, Any], field: str, owner: str) -> str:
    value = data.get(field)
    if not isinstance(value, str) or not value.strip():
        raise DispatchError(f"{owner}.{field} must be a non-empty string")
    return value.strip()


def _string_list(data: dict[str, Any], field: str) -> list[str]:
    value = data.get(field, [])
    if not isinstance(value, list) or any(not isinstance(item, str) or not item.strip() for item in value):
        raise DispatchError(f"task.{field} must be a list of non-empty strings")
    return [item.strip() for item in value]


def _role_for(purpose: str, requested: str) -> dict[str, str]:
    if purpose == "review":
        executor = "role:reviewer-integrator"
    elif requested in KNOWN_ROLES:
        executor = requested
    elif requested.startswith("role:") and requested.endswith("-specialist"):
        executor = "role:generic-specialist"
    else:
        raise DispatchError(f"unsupported agent role: {requested}")
    return {
        "requested": requested,
        "executor": executor,
        "role_file": KNOWN_ROLES[executor],
    }


def _identity(task_id: str, purpose: str, attempt: int, review_round: int) -> str:
    if purpose == "review":
        return f"agent:reviewer:{task_id}:round-{review_round}"
    return f"agent:implementer:{task_id}:attempt-{attempt}"


def _task_name(identity: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "_", identity.casefold()).strip("_")
    return value[:64] or "codex_agent"


def build_dispatch(request: dict[str, Any]) -> dict[str, Any]:
    """Prepare one native Codex call without inheriting conversation history."""
    if not isinstance(request, dict):
        raise DispatchError("dispatch request must be an object")
    task = request.get("task")
    model = request.get("model_dispatch")
    capabilities = request.get("capabilities")
    if not isinstance(task, dict) or not isinstance(model, dict) or not isinstance(capabilities, dict):
        raise DispatchError("task, model_dispatch, and capabilities must be objects")

    purpose = request.get("purpose", "implementation")
    if purpose not in {"implementation", "review"}:
        raise DispatchError("purpose must be implementation or review")
    task_id = _required_string(task, "id", "task")
    task_spec = _required_string(task, "task_spec", "task")
    requested_role = _required_string(task, "agent_role", "task")
    role = _role_for(purpose, requested_role)

    if model.get("status") != "resolved" or model.get("override_confirmed") is not True:
        raise DispatchError("model dispatch must be resolved and override-confirmed")
    selected_model = _required_string(model, "selected_model", "model_dispatch")
    effort = _required_string(model, "reasoning_effort", "model_dispatch")
    if effort not in REASONING_EFFORTS:
        raise DispatchError(f"unsupported reasoning effort: {effort}")
    model_ref = _required_string(model, "id", "model_dispatch")

    try:
        attempt = int(request.get("attempt", 1))
        review_round = int(request.get("review_round", 1))
    except (TypeError, ValueError) as exc:
        raise DispatchError("attempt and review_round must be positive integers") from exc
    if attempt < 1 or review_round < 1:
        raise DispatchError("attempt and review_round must be positive integers")

    agent_identity = _identity(task_id, purpose, attempt, review_round)
    implementer_identity = str(request.get("implementer_identity", "unassigned"))
    implementer_context = str(request.get("implementer_context_ref", "unassigned"))
    if purpose == "review" and agent_identity == implementer_identity:
        raise DispatchError("reviewer identity must differ from implementer identity")

    packet = {
        "role": role,
        "task": f"{task_id}@{task.get('revision', 1)}",
        "task_spec": task_spec,
        "approved_authorities": _string_list(task, "approved_authorities"),
        "scoped_rules": _string_list(task, "scoped_rules"),
        "read_set": _string_list(task, "read_set"),
        "impact_set": _string_list(task, "impact_set"),
        "model_dispatch": model_ref,
    }
    message_lines = [
        f"Act as {agent_identity} using {role['executor']}.",
        f"Read the neutral role at {role['role_file']} and the executable task SPEC at {task_spec}.",
        "Load only the following approved context packet; do not use conversation history:",
    ]
    for field in ("approved_authorities", "scoped_rules", "read_set", "impact_set"):
        values = packet[field]
        message_lines.append(f"- {field}: {', '.join(values) if values else 'none'}")
    message_lines.append(f"Model dispatch authority: {model_ref}.")
    if purpose == "review":
        message_lines.append("Derive acceptance from the pinned SPEC and remain independent from the implementer.")

    spawn = capabilities.get("spawn_subagent")
    available = isinstance(spawn, dict) and spawn.get("available") is True
    operation = spawn.get("operation") if isinstance(spawn, dict) else None
    capability_evidence = spawn.get("evidence") if isinstance(spawn, dict) else None
    if available and operation not in {"spawn_agent", "spawn_subagent"}:
        raise DispatchError("available subagent capability needs a supported native operation")

    plan: dict[str, Any] = {
        "schema": "harness.codex-agent-dispatch-plan/v1",
        "task": packet["task"],
        "purpose": purpose,
        "agent_identity": agent_identity,
        "role": role,
        "context_packet": packet,
        "model": {"requested": selected_model, "reasoning_effort": effort, "dispatch_ref": model_ref},
        "capability_evidence": capability_evidence or "unavailable",
        "separation": {
            "implementer_identity": implementer_identity,
            "implementer_context_ref": implementer_context,
            "fresh_context_required": purpose == "review",
        },
    }
    if available:
        plan.update(
            {
                "status": "ready-to-dispatch",
                "native_call": {
                    "operation": operation,
                    "arguments": {
                        "task_name": _task_name(agent_identity),
                        "fork_turns": "none",
                        "message": "\n".join(message_lines),
                        "model": selected_model,
                        "reasoning_effort": effort,
                    },
                },
                "fallback": None,
            }
        )
    elif purpose == "review":
        plan.update(
            {
                "status": "manual-fresh-context-required",
                "native_call": None,
                "fallback": "open-new-review-context",
            }
        )
    else:
        plan.update(
            {
                "status": "sequential-fallback",
                "native_call": None,
                "fallback": "run-in-orchestrator-context",
            }
        )
    return plan


def record_dispatch(plan: dict[str, Any], adapter_response: dict[str, Any]) -> dict[str, Any]:
    """Convert an adapter-owned Codex response into durable dispatch evidence."""
    if plan.get("status") != "ready-to-dispatch" or not isinstance(plan.get("native_call"), dict):
        raise DispatchError("only a ready native dispatch can record a runtime response")
    if not isinstance(adapter_response, dict):
        raise DispatchError("adapter response must be an object")
    agent_id = adapter_response.get("agent_id")
    context_ref = adapter_response.get("context_ref")
    if not isinstance(agent_id, str) or not agent_id.strip():
        if not isinstance(context_ref, str) or not context_ref.strip():
            raise DispatchError("adapter response needs an agent or context reference")
        execution_context_ref = context_ref.strip()
    else:
        execution_context_ref = f"codex:{agent_id.strip()}"

    requested_model = plan["model"]["requested"]
    requested_effort = plan["model"]["reasoning_effort"]
    if adapter_response.get("accepted_model") != requested_model:
        raise DispatchError("adapter response did not confirm the requested model")
    if adapter_response.get("accepted_reasoning_effort") != requested_effort:
        raise DispatchError("adapter response did not confirm the requested reasoning effort")
    if plan.get("purpose") == "review":
        implementer_context = plan["separation"].get("implementer_context_ref")
        returned_context = adapter_response.get("context_ref")
        if execution_context_ref == implementer_context or returned_context == implementer_context:
            raise DispatchError("review dispatch reused the implementer context")

    sanitized_response = {key: adapter_response[key] for key in RESPONSE_FIELDS if key in adapter_response}
    evidence = sanitized_response.get("operation_id") or sanitized_response.get("context_ref") or sanitized_response.get("agent_id")
    if not isinstance(evidence, str) or not evidence.strip():
        raise DispatchError("adapter response needs an inspectable response identity")
    return {
        "schema": "harness.codex-agent-dispatch/v1",
        "status": "dispatched",
        "task": plan["task"],
        "purpose": plan["purpose"],
        "agent_identity": plan["agent_identity"],
        "role": plan["role"],
        "context_packet": plan["context_packet"],
        "execution_context_ref": execution_context_ref,
        "model": {
            "requested": requested_model,
            "accepted": adapter_response["accepted_model"],
            "reasoning_effort_requested": requested_effort,
            "reasoning_effort_accepted": adapter_response["accepted_reasoning_effort"],
            "dispatch_ref": plan["model"]["dispatch_ref"],
        },
        "adapter_operation": plan["native_call"]["operation"],
        "adapter_response_identity": evidence,
        "adapter_response": sanitized_response,
        "separation": plan["separation"],
    }
