# Contract: Learning profile

Optional, user-controlled learning state. It is never required by `delivery` mode and contains no credentials.

```yaml
---
schema: harness.learning-profile/v1
id: learning-profile
revision: 2
status: active                    # draft | awaiting-consent | active | paused | withdrawn
owner: human:owner
consent_updated_at: 2026-08-20T15:10:00Z
retention: repository-local
publication: approval-required
source_references: migration-main@1
---
```

```markdown
# Learning profile

## Goals
- Explain dependency-aware graph design through current project work.

## Observation consent
- May read: task briefs, user-authored reasoning, review summaries.
- Must not read/export: secrets, customer data, raw private logs.

## Evidence by skill
| Skill | Self-assessment | Demonstrated evidence | Confidence |
| --- | --- | --- | --- |
| Task decomposition | developing | Drafted TASK-001 breakdown | medium |

## Learning queue
| ID | Topic | Why now | Prerequisites | State |
| --- | --- | --- | --- | --- |
| LEARN-003 | Ownership overlap | Relevant to TASK-001 review | Path basics | proposed |

## Destination preferences
- Local Markdown draft; external publication requires per-item approval.

## Latest debrief
- Improved: distinguished node loops from graph orchestration.
- Next: design a failure-recovery example.
```

## Invariants

- The owner explicitly controls consent, visibility, retention, and publication.
- Skill/seniority feedback is evidence-linked, scoped by skill, and uncertainty-calibrated; no unsupported global rank.
- Queue items cannot be delivery dependencies or mutate delivery priority/status.
- External publication always requires the declared human approval; destination credentials never appear here.
- `paused` or `withdrawn` stops observation and publication without changing delivery artifacts.
- Deleting or omitting this artifact leaves all core contracts valid.
- Installing/selecting `core-learning` does not create consent, activate observation, set retention, or approve publication.
- Migrated learning references retain source identities/backlinks and remain inactive until explicit consent.
