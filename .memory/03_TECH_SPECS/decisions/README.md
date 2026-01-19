# Architecture Decision Records (ADR)

> 기술적 의사결정을 기록합니다.
> "왜 MongoDB 대신 PostgreSQL을 썼는가?"에 대한 답을 남깁니다.

## Why ADR?
구조를 뒤집을 때, 이 기록을 보지 않으면 **같은 실수를 반복**합니다.

## Template
```markdown
# ADR-001: [Decision Title]

> **Status**: [Proposed | Accepted | Deprecated | Superseded]
> **Date**: YYYY-MM-DD
> **Deciders**: (결정자)

---

## Context
(문제 상황을 설명)

## Decision
(무엇을 결정했는가?)

## Alternatives Considered
### Option A: (대안 1)
- Pros: ...
- Cons: ...

### Option B: (대안 2)
- Pros: ...
- Cons: ...

## Consequences
### Positive
- ...

### Negative
- ...

## Related
- [Link to related ADR or doc]
```

## Naming Convention
- `ADR-[NUMBER]-[short-title].md`
- Example: `ADR-001-database-choice.md`
