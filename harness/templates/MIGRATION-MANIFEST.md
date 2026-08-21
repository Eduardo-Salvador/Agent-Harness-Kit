---
schema: harness.migration-manifest/v1
id: migration-main
revision: 1
status: coexistence
source_root: .
snapshot_revision: discovery-001
snapshot_created_at: 2000-01-01T00:00:00Z
semantic_review: pending
cutover_authorized_by: none
---

# Migration manifest

```json
{
  "source_selectors": [
    {"selector": "existing/instructions.md", "expanded_sources": ["existing/instructions.md"]}
  ],
  "items": [
    {
      "material_id": "MAT-001",
      "material_type": "rule",
      "source": "existing/instructions.md",
      "source_identity": "sha256:<replace>",
      "classification": "unresolved",
      "destinations": ["harness-adoption/COEXISTENCE.md"],
      "backlinks": ["harness-adoption/COEXISTENCE.md"],
      "unresolved_owner": "human:owner",
      "unresolved_checkpoint": "before project-context approval",
      "semantic_review": "pending",
      "reviewed_by": null
    }
  ]
}
```

## Coverage statement

- Every discovered material item is classified; silent omission is prohibited.

## Semantic review

- Structural validation: pending.
- Human equivalence review: pending.
- Cutover authorization: not requested.
