---
schema: harness.capability-manifest/v1
id: capability-manifest
revision: 1
status: draft
updated_at: 2000-01-01T00:00:00Z
approved_by: pending
---

# Capability manifest

| ID | Kind | Purpose | Provider/source | State | Scope | Auth/secret/network | Side effects | Evidence | Fallback | Approval |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CAP-001 | native-tool / MCP-connector / skill / script-command / hook / external-integration | Replace | Replace | unavailable | none | none known | none known | not detected | block | human:owner |

## Inventory notes

- Presence in instructions does not prove installation, authentication, secret access, network access, or authorization.
- For frontend-screen work, inventory `design-taste-frontend`, `imagegen-frontend-web`, `imagegen`, and `image-to-code` separately; the router must degrade visibly when any phase capability is absent. For approved screenshots, record `image-to-code` as the primary coding capability, `frontend-screen` as desktop/mobile orchestration and verification, and `imagegen` as temporary raster-asset generation only.
- For project-learning destinations, inventory exact filesystem access for local/Obsidian paths or the connector/MCP, authentication state, and target evidence for Notion/other systems. Never record credentials.
- For context routing, inventory `spawn_subagent`, `create_thread`, `resume_thread`, `message_thread`, `close_thread`, and `parallel_contexts` separately. Internal agents do not prove user-visible chat creation.

## Change gate

- Consequential expansion requires explicit human approval and validation before use.
