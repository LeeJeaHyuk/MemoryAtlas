# Invariants (RULE-*)

> **Template-Version**: 3.0
>
> **"항상 ~이다 / ~는 금지"** 형태의 불변 규칙을 정의합니다.

## RULE 판정 기준

- ✅ "항상 ~~이다 / ~~는 금지 / ~~를 만족해야 한다"로 시작 가능 (불변 중심)
- ✅ Scope / Violation 판정 기준 / Examples 필수
- ✅ 단독으로 참/거짓 판정 가능 (테스트 가능한 문장)

## Template

```markdown
# [RULE-XXX-001] Invariant Name

> **ID**: RULE-XXX-001
> **Domain**: (도메인)
> **Priority**: [Critical | High | Medium | Low]
> **Last Updated**: YYYY-MM-DD
> **Must-Read**: RULE-XXX-001, ADR-XXX
> **Template-Version**: 3.0

---

## Rule Statement (최종 결정)

(규칙을 명확하게 한 문장으로. "항상 ~이다" 또는 "~는 금지")

## Scope

(이 규칙이 적용되는 범위)

## Violation (위반 판정 기준)

(어떤 경우 이 규칙을 위반한 것인가?)

## Examples

### Correct
(올바른 예시)

### Incorrect
(잘못된 예시)

## Exceptions

(예외 상황이 있다면)
```

## Common Domains

- **ID**: ID 명명 규칙
- **META**: 메타데이터 규칙
- **DATA**: 데이터 형식, 저장 규칙
- **SEC**: 보안 규칙
- **VER**: 버전 관리 규칙

## Rules

1. **불변만 적는다**: 기능/동작은 capabilities/에
2. **테스트 가능**: 단독으로 참/거짓 판정 가능해야 함
3. **Violation 필수**: 위반 기준 없으면 RULE이 아님
4. **ID 일치**: 파일명 = **ID**: = 헤더 [ID]
