---
schema: harness.migration-manifest/v1
id: fixture-migration
revision: 1
status: coexistence
source_root: .
snapshot_revision: fixture-snapshot-001
snapshot_created_at: 2026-08-20T12:00:00Z
semantic_review: pending
cutover_authorized_by: none
---

# Sanitized migration manifest

```json
{
  "source_selectors": [
    {"selector": "AGENTS.md", "expanded_sources": ["AGENTS.md"]},
    {"selector": "CLAUDE.md", "expanded_sources": ["CLAUDE.md"]},
    {"selector": "PENDING.md", "expanded_sources": ["PENDING.md"]},
    {"selector": "DECISIONS.md", "expanded_sources": ["DECISIONS.md"]},
    {"selector": ".env.example", "expanded_sources": [".env.example"]},
    {"selector": ".claude/roles/*.md", "expanded_sources": [".claude/roles/builder.md"]},
    {"selector": ".claude/knowledge/*.md", "expanded_sources": [".claude/knowledge/testing.md"]},
    {"selector": ".claude/worktrees/**/*.md", "expanded_sources": [".claude/worktrees/generated-context.md"]},
    {"selector": "tests/verification-source.txt", "expanded_sources": ["tests/verification-source.txt"]}
  ],
  "items": [
    {"material_id":"MAT-ROOT-AGENTS","material_type":"rule","source":"AGENTS.md","source_identity":"sha256:35417a29f1b22c02da74b1e8a8048a5b1bcae5828ff9054cc34accfb95bffdcd","classification":"retained-as-authoritative-reference","destinations":["harness-adoption/COEXISTENCE.md"],"backlinks":["harness-adoption/COEXISTENCE.md"],"unresolved_owner":null,"unresolved_checkpoint":null,"semantic_review":"pending","reviewed_by":null},
    {"material_id":"MAT-ROOT-CLAUDE","material_type":"rule","source":"CLAUDE.md","source_identity":"sha256:5104c4b69b71cc9f2fcf05dbd6419e40e9ac8898d534c9f0d6275fd67d22e026","classification":"retained-as-authoritative-reference","destinations":["harness-adoption/COEXISTENCE.md"],"backlinks":["harness-adoption/COEXISTENCE.md"],"unresolved_owner":null,"unresolved_checkpoint":null,"semantic_review":"pending","reviewed_by":null},
    {"material_id":"MAT-PENDING","material_type":"pending-item","source":"PENDING.md","source_identity":"sha256:b9418eb40c3fe83a4a83e6e4301a6900236b8ab82dd7daee83119c3a66a5a84e","classification":"unresolved","destinations":["harness-adoption/COEXISTENCE.md"],"backlinks":["harness-adoption/COEXISTENCE.md"],"unresolved_owner":"human:product-owner","unresolved_checkpoint":"before context approval","semantic_review":"pending","reviewed_by":null},
    {"material_id":"MAT-DECISIONS","material_type":"decision","source":"DECISIONS.md","source_identity":"sha256:9d75d912f24c46cb9e7f0365eeeed22640d7c642fcb8609b740d9980201617c8","classification":"retained-as-authoritative-reference","destinations":["harness-adoption/COEXISTENCE.md"],"backlinks":["harness-adoption/COEXISTENCE.md"],"unresolved_owner":null,"unresolved_checkpoint":null,"semantic_review":"pending","reviewed_by":null},
    {"material_id":"MAT-SECRET","material_type":"secret-boundary","source":".env.example","source_identity":"sha256:eab0d826100161459aae7344586d842c959c8be664ca2d45c05e63c5439035c0","classification":"migrated","destinations":["harness-adoption/COEXISTENCE.md"],"backlinks":["harness-adoption/COEXISTENCE.md"],"unresolved_owner":null,"unresolved_checkpoint":null,"semantic_review":"approved","reviewed_by":"human:security-reviewer"},
    {"material_id":"MAT-ROLE","material_type":"role-responsibility","source":".claude/roles/builder.md","source_identity":"sha256:69e1b4d523e852dcfe3ec693231dd556cffa3e52abc5883e58da27fb9196b122","classification":"retained-as-authoritative-reference","destinations":["harness-adoption/COEXISTENCE.md"],"backlinks":["harness-adoption/COEXISTENCE.md"],"unresolved_owner":null,"unresolved_checkpoint":null,"semantic_review":"pending","reviewed_by":null},
    {"material_id":"MAT-LEARNING","material_type":"learning-reference","source":".claude/knowledge/testing.md","source_identity":"sha256:337f5d082cb0aa606f4044a3b87f43a5aebb5f80633fb8a5ea4efb27efba389d","classification":"retained-as-authoritative-reference","destinations":["harness-adoption/COEXISTENCE.md"],"backlinks":["harness-adoption/COEXISTENCE.md"],"unresolved_owner":null,"unresolved_checkpoint":null,"semantic_review":"pending","reviewed_by":null},
    {"material_id":"MAT-WORKTREE","material_type":"generated-source-exclusion","source":".claude/worktrees/generated-context.md","source_identity":"sha256:22b152219dacea78f904207bf2c89a582b1605b1a0ee29009b375ba1502539f6","classification":"migrated","destinations":["harness-adoption/COEXISTENCE.md"],"backlinks":["harness-adoption/COEXISTENCE.md"],"unresolved_owner":null,"unresolved_checkpoint":null,"semantic_review":"approved","reviewed_by":"human:existing-harness-maintainer"},
    {"material_id":"MAT-VERIFY","material_type":"verification-source","source":"tests/verification-source.txt","source_identity":"sha256:2787bd7186ede4a95555c06937db791ae4d1188d092b3d9bc7228160ee58a646","classification":"retained-as-authoritative-reference","destinations":["harness-adoption/COEXISTENCE.md"],"backlinks":["harness-adoption/COEXISTENCE.md"],"unresolved_owner":null,"unresolved_checkpoint":null,"semantic_review":"pending","reviewed_by":null}
  ]
}
```

## Coverage statement

Every sanitized discovered source is classified. Secret values are not present, generated worktree state is excluded, and retained narrative decisions remain authoritative.

## Semantic review

Structural coverage is testable. Human equivalence/cutover remain pending.
