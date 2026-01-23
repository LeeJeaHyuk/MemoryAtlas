# Change Briefs

This folder contains **Change Brief** documents that capture intake requests before they become formal requirements and execution plans.

## Purpose

Change Briefs serve as the **single snapshot** that consolidates:
- User intent and natural language requests
- Affected artifacts (REQ, RULE, ADR, etc.)
- Proposed changes summary
- Verification criteria

## Naming Convention

```
BRIEF-[DOMAIN]-[YYYYMMDD]-[SEQ].md
```

**Examples:**
- `BRIEF-CORE-20260123-01.md`
- `BRIEF-MCP-20260123-01.md`
- `BRIEF-VALID-20260124-02.md`

## Lifecycle

1. **Created**: Via `intake()` MCP function (creates the BRIEF)
2. **Reviewed**: User approves or requests changes
3. **Consumed**: `plan_from_brief()` creates RUN document
4. **Archived**: Brief remains as historical record

If MCP is unavailable, do not proceed with intake; inform the user and fix MCP first.

## Template Structure

```markdown
# [BRIEF-DOMAIN-YYYYMMDD-SEQ] Title

## 1. Intent Summary
(What the user wants to achieve)

## 2. Affected Artifacts
- Modify: 02_REQUIREMENTS/capabilities/REQ-XXX-001.md
- Create: 02_REQUIREMENTS/invariants/RULE-YYY-001.md

## 3. Proposed Changes
(Bullet points of specific changes)

## 4. Verification Criteria
- [ ] Criterion 1
- [ ] Criterion 2
```

Affected Artifacts must use full paths or markdown links. REQ files live under `02_REQUIREMENTS/capabilities/`.

## Related Rules

- [RULE-FLOW-002](../../invariants/RULE-FLOW-002.md) - Brief Policy
- [RULE-ID-001](../../invariants/RULE-ID-001.md) - ID Naming Convention
