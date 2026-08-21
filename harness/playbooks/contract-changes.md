# Playbook: Contract changes

Use this for a schema or invariant change, not for an ordinary artifact revision.

1. Propose the problem, compatibility impact, alternatives, and migration in a decision artifact.
2. Require human approval when authority, lifecycle, security, portability, or learning boundaries change.
3. Update the contract document, operational template, validator, valid/invalid fixtures, examples, and adapter conformance notes together.
4. Increment the schema version for incompatible meaning; never reinterpret an existing version silently.
5. Validate old supported fixtures and the new version. Record unsupported migrations explicitly.

No adapter may ship a private contract dialect as canonical core state.
