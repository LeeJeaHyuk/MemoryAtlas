# Business Rules

> 비즈니스 로직, 공식, 변하지 않는 규칙을 이곳에 저장합니다.
> 모든 기능 구현 시 이 규칙들을 **반드시** 준수해야 합니다.

## Template
```markdown
# [RULE-XXX-001] Rule Name

> **ID**: RULE-XXX-001
> **Domain**: (도메인)
> **Priority**: [Critical | High | Medium | Low]
> **Last Updated**: YYYY-MM-DD

---

## Rule Statement
(규칙을 명확하게 한 문장으로)

## Rationale
(왜 이 규칙이 필요한가?)

## Examples
### ✅ Correct
(올바른 예시)

### ❌ Incorrect
(잘못된 예시)

## Exceptions
(예외 상황이 있다면)
```

## Common Categories
- **DATA**: 데이터 형식, 저장 규칙
- **PERF**: 성능 제약
- **SEC**: 보안 규칙
- **UX**: 사용자 경험 규칙
