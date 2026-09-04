# Runtime template catalog

Compact client installations keep templates in the hash-verified `resources/templates.zip` pack instead of copying every template as a separate file. The source repository and expanded `full` profile retain the readable canonical files under `harness/templates/`.

List available templates:

```text
agent-harness scaffold --list
```

Materialize only the template that has an actual consumer:

```text
agent-harness scaffold PROJECT-CONTEXT --output harness-state/PROJECT-CONTEXT.md
agent-harness scaffold FEATURE-BRIEF --output harness-state/features/FEATURE-001.md
agent-harness scaffold TASK --output harness-state/tasks/TASK-001.md
```

For a compact portable installation without the global CLI, replace `agent-harness` with:

```text
python agent-harness-kit/runtime.pyz scaffold
```

An expanded `full` installation already contains each canonical file under `agent-harness-kit/harness/templates/`; it does not need the compact scaffold command.

The scaffold command refuses to overwrite an existing file unless the operator explicitly supplies `--force`. Creating a template does not approve it, activate learning, or grant authority.
