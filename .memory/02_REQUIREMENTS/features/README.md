# Feature Requirements (DECISION)

> **Template-Version**: 2.4
>
> 이곳에는 **최종 결정**만 저장합니다.
> 논의/대안 검토는 `../discussions/`에 작성하세요.

## Template

```markdown
# [REQ-XXX-001] Feature Name

> **ID**: REQ-XXX-001
> **Domain**: (도메인)
> **Status**: [Draft | Active | Deprecated]
> **Last Updated**: YYYY-MM-DD
> **Must-Read**: RULE-XXX-001, ADR-XXX
> **Template-Version**: 2.4

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

## Constraints & Boundaries (Optional)

> 이 기능 구현 시 적용되는 특별한 제약.
> 프로젝트 전역 Boundaries(`01_CONVENTIONS.md`)를 넘어서는 경우만 작성.

### ⚠️ Ask First
- (이 기능에서 사람 승인이 필요한 것)

### 🚫 Never
- (이 기능에서 절대 금지)

## Related

- Discussion: [DISC-XXX-001](../discussions/DISC-XXX-001.md)
- Tech Spec: [API Spec](../../03_TECH_SPECS/api_specs/)
```

## Rules

1. **결정만 적는다**: 논의/대안은 discussions/에
2. **짧게 유지**: 한 REQ = 하나의 명확한 결정
3. **Must-Read 필수**: RULE/ADR ID만, 링크 텍스트는 ID
4. **ID 일치**: 파일명 = **ID**: = 헤더 [ID]
5. **Boundaries 선택적**: 프로젝트 전역 규칙 외 추가 제약 시만 작성
