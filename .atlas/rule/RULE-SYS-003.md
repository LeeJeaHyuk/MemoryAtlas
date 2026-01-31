# [RULE-SYS-003] Views as Non-SSOT Reference Layer

> **ID**: RULE-SYS-003
> **Domain**: SYS
> **Priority**: High
> **Last Updated**: 2026-01-31
> **Must-Read**: None

---

## Rule Statement
- Views are non-SSOT documents and must not replace SSOT.
- Views reorganize SSOT for specific audiences and purposes.
- View statements that use normative keywords must include inline SSOT anchors.
- Views should link back to their source SSOT IDs for traceability.

## Scope
- All documents under `.atlas/views/`.

## Violation
- Treating a view as authoritative without SSOT linkage.
- Using MUST/SHOULD/MAY/반드시/해야/불가/금지/항상 in a view without SSOT anchors.

## Examples

### Correct
- “VIEW는 비권위 문서다. (@RULE-SYS-003#Rule-Statement)”
- A summary bullet that includes `(@REQ-XXX-001#Decision)`.

### Incorrect
- “항상 SSOT를 참조한다.” (no anchor)
- View text that introduces new requirements without REQ/RULE/ADR references.
