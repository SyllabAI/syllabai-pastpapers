# SyllabAI Past Papers — Multi-Agent Rules

The project-wide multi-agent operating system is canonical in `SyllabAI/syllabai` (`AGENT.md` + `.syllabai/`).

Past-paper data rules:

1. Treat manifests, SHA-256 identities, provenance and quarantine state as canonical data truth.
2. Never silently replace, pair, rename or infer ambiguous source/session identity.
3. Preserve QP/MS pairing evidence and quarantine conflicts such as `REVIEW_REQUIRED` cases.
4. Data mutations must be reproducible and durably reported; ephemeral workspace state is not canonical.
5. Record task ID/base commit and corpus commit for material changes.
6. Coordinate changes that affect ingestion contracts with parser/core owners.
7. Do not turn corpus acquisition or parser suggestions into learner-servable content; serving remains behind validation in core.
