# [RULE-SYS-002] SSOT Authority and Change Order

> **ID**: RULE-SYS-002
> **Domain**: SYS
> **Priority**: High
> **Last Updated**: 2026-01-31
> **Must-Read**: None

---

## Rule Statement
- SSOT (REQ/RULE/ADR) is the authoritative source of truth for the project.
- When changes occur, SSOT is updated first; code/tests/views follow.
- Keep SSOT small, referencable, and reviewable.

## Scope
- All project documentation and implementation artifacts.

## Violation
- Updating code/tests/views without corresponding SSOT changes.
- Duplicating SSOT content without explicit references.

## Examples

### Correct
- Update REQ first, then adjust code and view docs.
- Link view summaries to the specific SSOT section they derive from.

### Incorrect
- Change code behavior without updating the related REQ/RULE/ADR.
- Copy a rule into a view without referencing its SSOT ID.
