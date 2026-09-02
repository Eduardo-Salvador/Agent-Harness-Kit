"""Dependency-free deterministic request preflight routing."""

from __future__ import annotations

import re
from typing import Final


LANES: Final[tuple[str, ...]] = ("direct-trivial", "vibe", "graph-only", "full-harness")
ASSURANCE_LEVELS: Final[tuple[str, ...]] = ("none", "light", "full")
HARNESS_SHAPES: Final[tuple[str, ...]] = ("none", "compact", "complete")
PROMOTION_TRIGGERS: Final[tuple[str, ...]] = (
    "multi-agent-execution", "human-in-loop", "audit-required",
    "weak-model", "ambiguity-unresolved", "explicit-full",
)

_EXPLICIT_FULL = re.compile(
    r"\b(?:full[ -]harness|use (?:the )?harness|full workflow|harness completo|use o harness|fluxo completo)\b", re.I,
)
_EXPLICIT_VIBE = re.compile(r"\b(?:vibe(?: mode)?|modo vibe|modo r[aá]pido|faz r[aá]pido)\b", re.I)

# Risk signals raise assurance; they do not independently select a route.
_RISK_SIGNALS: Final[tuple[tuple[str, re.Pattern[str]], ...]] = (
    ("authentication", re.compile(
        r"\b(?:auth(?:entication|orization)?|login|sign[ -]in|sign[ -]?up|user registration|registration flow|"
        r"register (?:a )?user|autentica[cç][aã]o|autoriza[cç][aã]o|cadastro (?:de )?usu[aá]ri[oa]|"
        r"cadastrar (?:um )?usu[aá]ri[oa])\b", re.I)),
    ("security-or-privacy", re.compile(
        r"\b(?:security|privacy|permission|access control|secret|seguran[cç]a|privacidade|permiss[aã]o|controle de acesso|segredo)\b", re.I)),
    ("data-schema-or-api-contract", re.compile(
        r"\b(?:data schema|database schema|schema change|api(?: contract| change)?|public api|esquema de dados|esquema do banco|contrato da api|api p[uú]blica)\b", re.I)),
    ("dependency", re.compile(
        r"\b(?:dependenc(?:y|ies)(?: change| update)?|(?:add|install|upgrade|replace) (?:a |the )?dependenc(?:y|ies)|(?:adicionar|instalar|atualizar|substituir) (?:uma? )?depend[eê]ncia)\b", re.I)),
    ("migration", re.compile(r"\b(?:migrat(?:e|es|ed|ing|ion|ions)|migra[cç][aã]o|migrar)\b", re.I)),
    ("accessibility", re.compile(r"\b(?:accessibility|a11y|acessibilidade)\b", re.I)),
    ("external-side-effect", re.compile(
        r"\b(?:external side[ -]effect|send (?:an? )?(?:email|message)|invite (?:a |the )?users? by (?:e-?mail|message)|"
        r"(?:e-?mail|message) notification|charge|payment|publish|deploy|delete external|"
        r"enviar (?:um )?(?:email|e-mail|mensagem)|convid\w* usu[aá]ri[oa]s? por (?:e-?mail|mensagem)|"
        r"convite por (?:e-?mail|mensagem)|notifica[cç][aã]o por (?:e-?mail|mensagem)|"
        r"cobrar|pagamento|publicar|implantar|deletar extern)\w*\b", re.I)),
    ("integration", re.compile(r"\b(?:integration|integrate with|webhook|third[ -]party|integra[cç][aã]o|integrar com|terceiro)\b", re.I)),
    ("destructive-action", re.compile(r"\b(?:destructive|irreversible|destrutiv[oa]|irrevers[ií]vel)\b", re.I)),
)
_MULTIPLE_WORKSTREAMS = re.compile(
    r"\b(?:multiple workstreams|cross[ -]workstream|frontend and backend|backend and frontend|m[uú]ltiplas frentes|frontend e backend|backend e frontend)\b", re.I,
)
_STATIC_REQUEST = re.compile(
    r"\b(?:typo|static copy|copy text|copywriting|static (?:text|label|content)|button label|spacing|padding|margin|font size|"
    r"text color|background color|rename (?:a |the )?(?:label|heading)|replace (?:a |the )?static)\b"
    r"|\b(?:erro de digita[cç][aã]o|texto est[aá]tico|r[oó]tulo (?:do )?bot[aã]o|espa[cç]amento|"
    r"margem|tamanho da fonte|cor do texto|cor de fundo|renomear (?:o )?(?:r[oó]tulo|t[ií]tulo))\b", re.I,
)

_ARTIFACTS: Final[dict[str, list[str]]] = {
    "none": [],
    "compact": ["task-graph-transition"],
    "complete": ["project-context", "pending-work", "task-graph", "task-spec", "verification-evidence", "independent-review"],
}


def _default_assurance(route: str) -> str:
    return {"direct-trivial": "none", "vibe": "none", "graph-only": "light", "full-harness": "full"}[route]


def _default_shape(route: str) -> str:
    return {"direct-trivial": "none", "vibe": "none", "graph-only": "compact", "full-harness": "complete"}[route]


def _decision(
    route: str, *, reasons: list[str], risk_signals: tuple[str, ...] = (),
    coordination_signals: tuple[str, ...] = (),
    needs_ai: bool = False, classification: str = "deterministic", user_override: str = "none",
    assurance: str = "auto", harness_shape: str = "auto", assurance_floor: str = "none",
) -> dict[str, object]:
    selected_assurance = _default_assurance(route) if assurance == "auto" else assurance
    mandatory_risks = {"authentication", "security-or-privacy", "destructive-action"}
    mandatory_full = bool(mandatory_risks.intersection(risk_signals)) or assurance_floor == "full"
    warnings: list[str] = []
    if assurance == "auto" and risk_signals:
        if selected_assurance != "full":
            reasons.append("assurance-raised-by-risk")
        selected_assurance = "full"
    elif mandatory_full and selected_assurance != "full":
        reasons.append("assurance-raised-by-mandatory-policy")
        selected_assurance = "full"
    elif risk_signals and selected_assurance != "full":
        warnings.append("explicit-assurance-below-risk-recommendation")
    selected_shape = _default_shape(route) if harness_shape == "auto" else harness_shape
    verification = {
        "direct-trivial": "smallest-useful-check", "vibe": "focused-check",
        "graph-only": "declared-graph-check", "full-harness": "full-harness-verification",
    }[route]
    artifacts = list(_ARTIFACTS[selected_shape])
    matched_signals = risk_signals + coordination_signals
    return {
        "schema": "harness.request-route/v1", "route": route,
        "assurance": selected_assurance, "selected_assurance": selected_assurance,
        "harness_shape": selected_shape, "shape": selected_shape, "selected_shape": selected_shape,
        "needs_ai": needs_ai, "classification": classification, "user_override": user_override,
        "lanes": LANES, "reason": reasons[0], "reasons": reasons,
        # Compatibility aliases for v0.6 consumers.
        "hard_triggers": list(matched_signals), "matched_triggers": matched_signals,
        "risk_signals": list(risk_signals), "verification": verification,
        "durable_artifacts": artifacts, "minimal_artifacts": artifacts,
        "artifact_expectations": artifacts,
        "warnings": warnings,
        "promotion_trigger": "reclassify-before-further-edits-on-any-promotion-trigger",
        "promotion_triggers": PROMOTION_TRIGGERS,
    }


def classify_request(
    request: str, *, graph_bound: bool = False, graph_only_eligible: bool = False,
    explicit_mode: str = "auto", workstream_count: int = 1, assurance: str = "auto",
    harness_shape: str = "auto", agent_count: int = 1, human_in_loop: bool = False,
    audit_required: bool = False, model_capability: str = "normal",
) -> dict[str, object]:
    """Select route, assurance, and artifact shape as independent axes."""
    if not isinstance(request, str):
        raise TypeError("request must be a string")
    normalized_mode = {"full": "full-harness"}.get(explicit_mode, explicit_mode)
    if normalized_mode not in {"auto", *LANES}:
        raise ValueError("explicit_mode must be auto, direct-trivial, vibe, graph-only, or full")
    if assurance not in {"auto", *ASSURANCE_LEVELS}:
        raise ValueError("assurance must be auto, none, light, or full")
    if harness_shape not in {"auto", *HARNESS_SHAPES}:
        raise ValueError("harness_shape must be auto, none, compact, or complete")
    if model_capability not in {"strong", "normal", "weak"}:
        raise ValueError("model_capability must be strong, normal, or weak")
    for name, value in (("workstream_count", workstream_count), ("agent_count", agent_count)):
        if not isinstance(value, int) or isinstance(value, bool) or value < 1:
            raise ValueError(f"{name} must be a positive integer")

    text = " ".join(request.split())
    user_override = "none" if normalized_mode == "auto" else normalized_mode
    risk_signals = tuple(name for name, pattern in _RISK_SIGNALS if pattern.search(text))
    multiple_workstreams = workstream_count > 1 or bool(_MULTIPLE_WORKSTREAMS.search(text))
    coordination_signals = (("multiple-workstreams",) if multiple_workstreams else ())

    full_reasons: list[str] = []
    if normalized_mode == "full-harness" or _EXPLICIT_FULL.search(text):
        full_reasons.append("explicit-full")
    if agent_count >= 2:
        full_reasons.append("multi-agent-execution")
    if human_in_loop:
        full_reasons.append("human-in-loop")
    if audit_required:
        full_reasons.append("audit-required")
    if model_capability == "weak":
        full_reasons.append("weak-model")
    if full_reasons:
        selected_full_shape = harness_shape
        if selected_full_shape == "auto":
            complete_reasons = {"explicit-full", "multi-agent-execution", "human-in-loop", "audit-required"}
            selected_full_shape = "complete" if complete_reasons.intersection(full_reasons) else "compact"
        return _decision(
            "full-harness", reasons=full_reasons, risk_signals=risk_signals,
            coordination_signals=coordination_signals, user_override=user_override,
            assurance=assurance, harness_shape=selected_full_shape,
            assurance_floor="full" if audit_required or model_capability == "weak" else "none",
        )

    if normalized_mode != "auto":
        return _decision(
            normalized_mode, reasons=[f"explicit-{normalized_mode}"], risk_signals=risk_signals,
            coordination_signals=coordination_signals,
            user_override=user_override, assurance=assurance, harness_shape=harness_shape,
        )
    if _EXPLICIT_VIBE.search(text):
        return _decision(
            "vibe", reasons=["explicit-vibe"], risk_signals=risk_signals,
            coordination_signals=coordination_signals, user_override="vibe",
            assurance=assurance, harness_shape=harness_shape,
        )
    if multiple_workstreams:
        return _decision(
            "graph-only", reasons=["multiple-workstreams-single-agent"], risk_signals=risk_signals,
            coordination_signals=coordination_signals,
            assurance=assurance, harness_shape=harness_shape,
        )
    if graph_bound:
        reason = "eligible-graph-bound-work" if graph_only_eligible else "graph-bound-work"
        return _decision(
            "graph-only", reasons=[reason], risk_signals=risk_signals,
            coordination_signals=coordination_signals,
            assurance=assurance, harness_shape=harness_shape,
        )
    if risk_signals:
        return _decision(
            "graph-only", reasons=["risk-managed-graph-work"], risk_signals=risk_signals,
            assurance=assurance, harness_shape=harness_shape,
        )
    if _STATIC_REQUEST.search(text):
        return _decision(
            "direct-trivial", reasons=["obvious-static-request"],
            assurance=assurance, harness_shape=harness_shape,
        )
    return _decision(
        "full-harness", reasons=["ambiguity-unresolved"], needs_ai=True, classification="fallback",
        assurance=assurance, harness_shape=harness_shape,
    )
