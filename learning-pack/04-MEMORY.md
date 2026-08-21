# Memory as durable state

Agent systems may need several kinds of memory, but each deserves a clear owner and retention policy:

- **User memory:** stable preferences or consent, such as project-learning visibility and publication policy.
- **Episodic memory:** what happened in a particular attempt, captured by handoffs, reviews, and transition logs.
- **Semantic memory:** durable project facts and approved decisions.
- **Procedural memory:** how work is performed, captured by roles, contracts, playbooks, and adapter rules.

Chat history is a transport, not canonical memory. A message can announce that a handoff exists; the handoff file must contain the state needed after interruption.

Map the types in this repository: [learning profile](../harness/templates/LEARNING-PROFILE.md) for consented user state, [handoff](../harness/templates/HANDOFF.md) for an episode, [project context](../harness/templates/PROJECT-CONTEXT.md) and [decision](../harness/templates/DECISION.md) for semantic facts, and [playbooks](../harness/playbooks/README.md) for procedures. Retention and external storage remain explicit policy choices.
