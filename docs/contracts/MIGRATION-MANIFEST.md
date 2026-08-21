# Contract: Migration manifest

`harness.migration-manifest/v1` proves structural coverage when Agent Harness Kit is adopted into a repository with a mature existing harness. It never proves semantic equivalence by itself.

```yaml
---
schema: harness.migration-manifest/v1
id: migration-main
revision: 1
status: coexistence
source_root: .
snapshot_revision: discovery-001
snapshot_created_at: 2026-08-20T12:00:00Z
semantic_review: pending
cutover_authorized_by: none
---
```

The executable JSON block contains selectors and classified material:

```json
{
  "source_selectors": [
    {"selector": "legacy/roles/*.md", "expanded_sources": ["legacy/roles/builder.md"]}
  ],
  "items": [
    {
      "material_id": "MAT-001",
      "material_type": "role-responsibility",
      "source": "legacy/roles/builder.md",
      "source_identity": "sha256:<hex>",
      "classification": "retained-as-authoritative-reference",
      "destinations": ["harness-adoption/COEXISTENCE.md"],
      "backlinks": ["harness-adoption/COEXISTENCE.md"],
      "unresolved_owner": null,
      "unresolved_checkpoint": null,
      "semantic_review": "pending",
      "reviewed_by": null
    }
  ]
}
```

## Classifications

Every discovered material rule, decision, constraint, pending item, role responsibility, learning reference, verification source, generated-source exclusion, and secret boundary must be exactly one of:

- `migrated`
- `retained-as-authoritative-reference`
- `intentionally-duplicated-during-transition`
- `unresolved`

Silent omission is invalid. `unresolved` requires an owner and checkpoint. Selectors must record their exact expanded source paths at the discovery snapshot, and every expanded path must have at least one classified item with a content identity.

## Invariants

- Source paths are repository-relative and cannot escape the host root.
- `source_identity` is a SHA-256 identity checked before approval; selector expansion and hashes detect drift/stale snapshots.
- Destinations and backlinks exist. Each backlink contains the source path so provenance can be followed in both directions.
- Narrative decisions may remain authoritative references; they must not be lossily split without semantic review.
- Selecting `coexistence` preserves originals. `cutover-approved` requires every retained/duplicated item to have human semantic-equivalence approval and a separate human `cutover_authorized_by`.
- Structural validation never authorizes deletion. Missing originals during coexistence fail validation.
