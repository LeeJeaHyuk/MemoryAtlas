# [RULE-SYS-001] No Hardcoded Defaults for Atlas Docs

> **ID**: RULE-SYS-001
> **Domain**: SYS
> **Priority**: High
> **Last Updated**: 2026-01-31
> **Must-Read**: None

---

## Rule Statement
- Atlas default docs (top docs, templates, prompts, dir READMEs) must be sourced from `src/.system_defaults/`.
- Do not hardcode default document contents inside `src/atlas_cli.py`.
- Build output (`atlas.py`) may embed defaults for distribution, but the source of truth remains `src/.system_defaults/`.
- When adding or changing a default document, update the corresponding file in `src/.system_defaults/`.

## Scope
- `src/atlas_cli.py` and any build/init flow that generates `.atlas` system documents.

## Violation
- Embedding default document bodies as string literals in `src/atlas_cli.py`.
- Generating `.atlas` docs without source files under `src/.system_defaults/`.

## Examples

### Correct
- Add `src/.system_defaults/templates/NEW.md` and load it at runtime.
- Update `src/.system_defaults/top_docs/CONVENTIONS.md` and rebuild.

### Incorrect
- Add a new default doc by inserting a multiline string in `src/atlas_cli.py`.
