# Views (VIEW)

Views are non-SSOT docs that reorganize SSOT for humans (guides, perspective maps, understanding checks).

## Naming Convention
- **File**: `VIEW-{slug}.md` (slug is free-form; SSOT ID not required)
- **ID Pattern**: `^VIEW-(.*)$`

## Required Metadata
- `Refs`: List of SSOT IDs this view centers on (one or more).
- Allowed IDs: `REQ-*`, `RULE-*`, `ADR-*`.

## Structure Rules
- Must include `## References (SSOT index)` section.
- List **all** SSOT IDs mentioned in the body (REQ/RULE/ADR) in that index.
- If you use normative keywords (MUST/SHOULD/MAY/반드시/해야/불가/금지/항상), the sentence must include an inline SSOT anchor like `(@REQ-... / @RULE-... / @ADR-...)`.

## Usage
- Guides/onboarding
- Perspective maps (ops/security/data/UX)
- Understanding checks with SSOT anchors
