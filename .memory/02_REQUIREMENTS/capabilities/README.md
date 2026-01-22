# Capabilities (REQ-*)

> **Template-Version**: 3.1
>
> **"시스템은 ~해야 한다"** 형태의 기능/행동을 정의합니다.
> 논의/대안 검토는 `../discussions/`에 작성하세요.

## REQ 판정 기준

- ✅ "시스템은 ~~해야 한다"로 시작 가능 (동작 중심)
- ✅ Input / Output / Acceptance Criteria 필수
- ❌ 규칙/형식/제약은 본문에 쓰지 말고 Must-Read로 RULE 참조

## Template

```markdown
# [REQ-XXX-001] Capability Name

> **ID**: REQ-XXX-001
> **Domain**: (도메인)
> **Status**: [Draft | Active | Deprecated]
> **Last Updated**: YYYY-MM-DD
> **Must-Read**: RULE-XXX-001, ADR-XXX
> **Template-Version**: 3.1

---

## Decision (최종 결정)

(기능에 대한 명확한 결정. 짧고 단단하게.)

## Input

- `param1` (type): description

## Output

- `result` (type): description

## Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2

## In/Out of Scope (Optional)

### In Scope
- (이 기능에 포함되는 것)

### Out of Scope
- (이 기능에 포함되지 않는 것)

## Related

- Discussion: [DISC-XXX-001](../discussions/DISC-XXX-001.md)
- Tech Spec: [API Spec](../../03_TECH_SPECS/api_specs/)
```

## Rules

1. **동작만 적는다**: 규칙/제약은 invariants/에
2. **짧게 유지**: 한 REQ = 하나의 명확한 기능
3. **Must-Read 필수**: RULE/ADR ID만, 링크 텍스트는 ID
4. **ID 일치**: 파일명 = **ID**: = 헤더 [ID]
5. **AC 필수**: Acceptance Criteria 없으면 REQ가 아님
