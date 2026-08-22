# Playbook: Frontend screen workflow

Use this playbook for a new screen, page, landing page, portfolio surface, responsive section, or material visual redesign. A small bug fix or deterministic style adjustment stays in the normal task loop.

## Capability gate

Before visual work, inspect the approved capability manifest for these skill capabilities:

1. `design-taste-frontend` — design read, visual system, interaction judgment, and final preflight.
2. `imagegen-frontend-web` — section-level visual direction across desktop, tablet, and mobile.
3. `imagegen` — temporary photographs, bitmap mockups, and visual-asset generation; never frontend code.
4. `image-to-code` — primary implementation capability when approved screenshots exist: interpret proportions, component boundaries, desktop/mobile relationships, and translate them faithfully into responsive code.

Presence of a name or file is not evidence of runtime availability. Record each capability as available, degraded, unavailable, or approval-required. If one is unavailable, announce the exact degradation and preserve the same phase boundary with available native tools; never pretend the named skill ran.

## Default sequence

1. Inspect the existing product, frontend stack, brand assets, responsive constraints, task acceptance, and owned paths. For a redesign, audit before proposing replacement.
2. Use `design-taste-frontend` to state one concise design read and set the visual direction. Preserve an established design system unless the task authorizes an overhaul.
3. Use `imagegen-frontend-web` to turn that direction into legible section proposals and responsive intent. Prefer separate section references over one unreadable full-page board.
4. Use `imagegen` to render the required mockups or raster assets. Generate distinct variants with distinct prompts, keep exact user copy, and persist project-bound outputs under an owned project path.
5. Obtain one consolidated visual approval before implementation only when the workflow introduced new visual judgment. Skip this gate when the user supplied an already-approved reference, explicitly requested direct code, or the task is deterministic.
6. After approval, use `image-to-code` to inspect the actual repository and implement the proposal in the existing stack. Do not replace real components, dependencies, brand assets, or accessibility behavior merely to resemble the image.
7. Verify the real result at representative desktop, tablet, and mobile widths. Check content hierarchy, overflow, interaction states, keyboard/accessibility basics, reduced-motion behavior when relevant, and fidelity to the approved proposal.
8. Use `design-taste-frontend` for the final design preflight. Fix acceptance failures inside the task budget, write the normal handoff, complete passing work, and continue through bounded independent assurance.

## Approved-screen implementation route

When the user supplies or points to approved desktop/mobile screens, `frontend-screen` remains the orchestration and cross-breakpoint verification skill, but skips new visual-direction generation unless a material gap requires user judgment.

1. Treat `image-to-code` as the primary coding skill. It inspects every approved screenshot, derives proportions and reusable components, maps desktop/mobile differences into responsive behavior, and implements in the real frontend stack.
2. Use `frontend-screen` to verify that all approved desktop and mobile references are paired, that no breakpoint or state is silently omitted, and that the implemented result remains coherent between those references.
3. Use `imagegen` only for missing temporary photographs or other raster assets requested by the approved design. It does not generate, replace, or validate frontend code and must not reinterpret approved layout.
4. Use `design-taste-frontend` only for a bounded fidelity/accessibility preflight. Use `imagegen-frontend-web` only if an approved breakpoint/section is genuinely missing and the user authorizes new visual judgment.

## Boundaries

- The visual phase does not grant implementation, package installation, network, publication, commit, or push authority.
- Do not block implementation on repeated aesthetic approvals. One consolidated approval is the maximum unless the user materially changes direction.
- Do not load all four skill bodies when a phase is not needed. Route progressively.
- Approved screenshots make `image-to-code` primary; do not rerun concept generation merely because image-generation capabilities exist.
- Do not spend delivery budget generating decorative variants that do not change an acceptance decision.
- When generation is unavailable, a code-native prototype may replace the mockup phase only after the degradation is visible; verification against task acceptance remains mandatory.
