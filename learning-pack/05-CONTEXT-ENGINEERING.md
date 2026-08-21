# Context engineering and progressive disclosure

Context engineering selects the smallest trustworthy working set for the current decision. More context is not automatically better: irrelevant files can obscure authority, stale revisions, and acceptance criteria.

This harness loads context progressively:

1. root policy and the assigned role;
2. approved project context and relevant decisions;
3. the task and its dependency/ownership neighborhood;
4. task-local source, checks, and prior evidence;
5. the selected adapter's actual capability notes.

Project-specific learning context is withheld from delivery agents by default. The Harness Engineering Learning Pack is also excluded unless the user explicitly asks to study it.

Inspect [the architecture's context order](../docs/ARCHITECTURE.md#progressive-context) and the `Context to load` section in [the task template](../harness/templates/TASK.md). A useful exercise is to explain why each referenced artifact is necessary and what risk appears if its revision is stale.
