"""Dependency-free deterministic request preflight routing."""

from __future__ import annotations

import re
from typing import Final


LANES: Final[tuple[str, ...]] = (
    "direct-trivial",
    "vibe",
    "graph-only",
    "full-harness",
)

PROMOTION_TRIGGERS: Final[tuple[str, ...]] = (
    "scope-growth",
    "ambiguity-unresolved",
    "authentication",
    "security-or-privacy",
    "data-schema-or-api-contract",
    "dependency",
    "migration",
    "accessibility",
    "external-side-effect",
    "integration",
    "multiple-workstreams",
    "destructive-action",
    "failed-verification",
)

_EXPLICIT_FULL = re.compile(
    r"\b(?:full[ -]harness|use (?:the )?harness|full workflow|harness completo|use o harness|fluxo completo)\b",
    re.IGNORECASE,
)
_EXPLICIT_VIBE = re.compile(
    r"\b(?:vibe(?: mode)?|modo vibe|modo r[aá]pido|faz r[aá]pido)\b",
    re.IGNORECASE,
)

_HARD_TRIGGERS: Final[tuple[tuple[str, re.Pattern[str]], ...]] = (
    (
        "authentication",
        re.compile(
            r"\b(?:auth(?:entication|orization)?|login|sign[ -]in|sign[ -]?up|user registration|registration flow|"
            r"register (?:a )?user|autentica[cç][aã]o|autoriza[cç][aã]o|cadastro (?:de )?usu[aá]ri[oa]|"
            r"cadastrar (?:um )?usu[aá]ri[oa])\b",
            re.I,
        ),
    ),
    (
        "security-or-privacy",
        re.compile(
            r"\b(?:security|privacy|permission|access control|secret|seguran[cç]a|privacidade|permiss[aã]o|controle de acesso|segredo)\b",
            re.I,
        ),
    ),
    (
        "data-schema-or-api-contract",
        re.compile(
            r"\b(?:data schema|database schema|schema change|api contract|public api|esquema de dados|esquema do banco|contrato da api|api p[uú]blica)\b",
            re.I,
        ),
    ),
    (
        "dependency",
        re.compile(
            r"\b(?:(?:add|install|upgrade|replace) (?:a |the )?dependenc(?:y|ies)|(?:adicionar|instalar|atualizar|substituir) (?:uma? )?depend[eê]ncia)\b",
            re.I,
        ),
    ),
    ("migration", re.compile(r"\b(?:migrat(?:e|es|ed|ing|ion|ions)|migra[cç][aã]o|migrar)\b", re.I)),
    (
        "accessibility",
        re.compile(r"\b(?:accessibility|a11y|acessibilidade)\b", re.I),
    ),
    (
        "external-side-effect",
        re.compile(
            r"\b(?:send (?:an? )?(?:email|message)|invite (?:a |the )?users? by (?:e-?mail|message)|"
            r"(?:e-?mail|message) notification|charge|payment|publish|deploy|delete external|"
            r"enviar (?:um )?(?:email|e-mail|mensagem)|convid\w* usu[aá]ri[oa]s? por (?:e-?mail|mensagem)|"
            r"convite por (?:e-?mail|mensagem)|notifica[cç][aã]o por (?:e-?mail|mensagem)|"
            r"cobrar|pagamento|publicar|implantar|deletar extern)\w*\b",
            re.I,
        ),
    ),
    (
        "integration",
        re.compile(r"\b(?:integration|integrate with|webhook|third[ -]party|integra[cç][aã]o|integrar com|terceiro)\b", re.I),
    ),
    (
        "multiple-workstreams",
        re.compile(
            r"\b(?:multiple workstreams|cross[ -]workstream|frontend and backend|backend and frontend|m[uú]ltiplas frentes|frontend e backend|backend e frontend)\b",
            re.I,
        ),
    ),
    ("destructive-action", re.compile(r"\b(?:destructive|irreversible|destrutiv[oa]|irrevers[ií]vel)\b", re.I)),
)

_STATIC_REQUEST = re.compile(
    r"\b(?:typo|static copy|copy text|copywriting|static (?:text|label|content)|button label|spacing|padding|margin|font size|"
    r"text color|background color|rename (?:a |the )?(?:label|heading)|replace (?:a |the )?static)\b"
    r"|\b(?:erro de digita[cç][aã]o|texto est[aá]tico|r[oó]tulo (?:do )?bot[aã]o|espa[cç]amento|"
    r"margem|tamanho da fonte|cor do texto|cor de fundo|renomear (?:o )?(?:r[oó]tulo|t[ií]tulo))\b",
    re.IGNORECASE,
)


def _decision(
    route: str,
    *,
    reason: str,
    matched_triggers: tuple[str, ...] = (),
    needs_ai: bool = False,
    classification: str = "deterministic",
    user_override: str = "none",
) -> dict[str, object]:
    verification = {
        "direct-trivial": "smallest-useful-check",
        "vibe": "focused-check",
        "graph-only": "declared-graph-check",
        "full-harness": "full-harness-verification",
    }[route]
    artifacts: list[str]
    if route in {"direct-trivial", "vibe"}:
        artifacts = []
    elif route == "graph-only":
        artifacts = ["task-graph-transition"]
    else:
        artifacts = ["full-harness-artifacts"]
    return {
        "schema": "harness.request-route/v1",
        "route": route,
        "needs_ai": needs_ai,
        "classification": classification,
        "user_override": user_override,
        "lanes": LANES,
        "reason": reason,
        "hard_triggers": list(matched_triggers),
        "matched_triggers": matched_triggers,
        "verification": verification,
        "durable_artifacts": artifacts,
        "promotion_trigger": "reclassify-before-further-edits-on-any-promotion-trigger",
        "promotion_triggers": PROMOTION_TRIGGERS,
    }


def classify_request(
    request: str,
    *,
    graph_bound: bool = False,
    graph_only_eligible: bool = False,
    explicit_mode: str = "auto",
    workstream_count: int = 1,
) -> dict[str, object]:
    """Classify a request before workflow selection.

    Hard gates are deliberately evaluated before fast-lane hints. The function
    performs no I/O and delegates only genuinely ambiguous language to AI.
    """
    if not isinstance(request, str):
        raise TypeError("request must be a string")
    if explicit_mode not in {"auto", "vibe", "full"}:
        raise ValueError("explicit_mode must be auto, vibe, or full")
    if not isinstance(workstream_count, int) or isinstance(workstream_count, bool) or workstream_count < 1:
        raise ValueError("workstream_count must be a positive integer")

    text = " ".join(request.split())
    user_override = {"auto": "none", "vibe": "vibe", "full": "full-harness"}[explicit_mode]
    if explicit_mode == "full" or _EXPLICIT_FULL.search(text):
        return _decision("full-harness", reason="explicit-full", user_override=user_override)

    matched = tuple(name for name, pattern in _HARD_TRIGGERS if pattern.search(text))
    if workstream_count > 1 and "multiple-workstreams" not in matched:
        matched += ("multiple-workstreams",)
    if matched:
        return _decision(
            "full-harness",
            reason="hard-trigger",
            matched_triggers=matched,
            user_override=user_override,
        )

    if explicit_mode == "vibe" or _EXPLICIT_VIBE.search(text):
        return _decision("vibe", reason="explicit-vibe", user_override=user_override)

    if graph_bound:
        if graph_only_eligible:
            return _decision("graph-only", reason="eligible-graph-bound-work", user_override=user_override)
        return _decision("full-harness", reason="graph-bound-work-not-graph-only-eligible", user_override=user_override)

    if _STATIC_REQUEST.search(text):
        return _decision("direct-trivial", reason="obvious-static-request", user_override=user_override)

    return _decision(
        "full-harness",
        reason="ambiguous-request-needs-ai-or-safe-fallback",
        needs_ai=True,
        classification="fallback",
        user_override=user_override,
    )
