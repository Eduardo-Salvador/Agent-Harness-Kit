# Playbook: Project-learning activation, capture, and destinations

## Activation request

Treat plain-language requests such as “study mode,” “help me learn while we build,” “track what I am learning,” or “save my study notes” as requests to configure `delivery+learning`. Do not require the user to know the internal mode name.

1. Inspect the current project context, `harness-state/LEARNING-PROFILE.md` when present, and the capability manifest. Do not repeat current approved answers.
2. If the installed profile lacks the native project-learning extension, explain the exact limitation and offer a bounded installation/profile change. Do not claim activation.
3. Ask one compact question covering only missing configuration:
   - learning goal or topic;
   - evidence the learning observer may read and anything excluded;
   - where notes should live: repository-local Markdown, another local folder/file, an Obsidian vault/folder, a Notion page/database, or another named destination;
   - preferred structure or naming only when it affects the output.
4. Treat destination selection as a hard activation and write gate. Until the user answers and confirms an exact target, do not create a note, a notes folder, an active learning profile, or any durable learning artifact; do not infer `docs/`, repository-local Markdown, the desktop, Obsidian, Notion, or another fallback. A request for study mode approves configuration only, not a destination.
5. Resolve the destination precisely and record it under `Destination preferences`: destination type, exact project-relative path or user-approved external locator, format, adapter/capability status, retention, and write/publication policy. Store no credentials or access tokens. For Notion or another remote system, ask which connector/MCP to use and which exact page/database is the target; never choose either implicitly.
6. Update the capability manifest with evidence. Local and Obsidian destinations require verified filesystem access to the exact approved path. Notion requires a verified connector/MCP, authentication, and target page/database. Missing access is `unavailable`, `degraded`, or `approval-required`, never assumed.
7. Present the concise profile delta and obtain the one activation consent that covers goals, observation, retention, and the private note destination. Set the project context to `delivery+learning` and the learning profile to `active` only after approval.

## Learning cycle

1. Confirm mode is `delivery+learning` and the active profile permits every proposed input and output.
2. Learning assessor reads only consented delivery evidence and user-authored reasoning.
3. Draft skill-specific assessment and queue changes; record that delivery nodes changed: none.
4. Offer bounded practice off the critical delivery path. Unanswered practice never blocks delivery.
5. Debriefer writes the summary only to the approved note destination with evidence, uncertainty, and next practice. If that destination is temporarily unavailable, report the degradation and do not write elsewhere unless the active profile already names an explicit approved fallback destination.
6. A private destination write already covered by the active profile follows its recorded write policy. Public sharing, a new destination, broader visibility, or a consequential retention change requires a fresh preview and human approval.
7. The destination adapter writes or returns failure/denial evidence. Delivery remains unchanged in all cases.

Disabling learning stops observation immediately and requires no delivery migration. Changing destination or observation scope updates the profile and consent timestamp before later capture.
