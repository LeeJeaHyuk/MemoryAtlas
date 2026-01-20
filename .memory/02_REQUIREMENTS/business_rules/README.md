# Business Rules (DECISION)

> **Template-Version**: 2.4
>
> 비즈니스 로직, 공식, 변하지 않는 규칙의 **최종 결정**을 저장합니다.

## Template

```markdown
# [RULE-XXX-001] Rule Name

> **ID**: RULE-XXX-001
> **Domain**: (도메인)
> **Priority**: [Critical | High | Medium | Low]
> **Last Updated**: YYYY-MM-DD
> **Must-Read**: RULE-XXX-001, ADR-XXX
> **Template-Version**: 2.4

---

## Rule Statement (최종 결정)

(규칙을 명확하게 한 문장으로)

## Rationale

(왜 이 규칙이 필요한가? 간단히)

## Examples

### Correct
(올바른 예시)

### Incorrect
(잘못된 예시)

## Exceptions

(예외 상황이 있다면)
```

## Common Domains

- **DATA**: 데이터 형식, 저장 규칙
- **PERF**: 성능 제약
- **SEC**: 보안 규칙
- **UX**: 사용자 경험 규칙
