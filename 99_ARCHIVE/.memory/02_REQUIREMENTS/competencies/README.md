# Competencies (CQ-*)

> **Template-Version**: 3.4
>
> 시스템이 반드시 답해야 하는 질문(검증 시나리오)을 정의합니다.
> CQ는 REQ/RULE의 완결성을 확인하는 테스트 케이스 역할입니다.

## CQ 판정 기준

- ✅ "시스템은 ~~에 답할 수 있는가?" 형태 (검증 중심)
- ✅ Question / Expected Answer / Traceability 필수
- ✅ REQ/RULE과 링크로 추적성 확보

## Template

```markdown
# [CQ-XXX-001] Competency Question Title

> **ID**: CQ-XXX-001
> **Domain**: (도메인)
> **Status**: [Draft | Active | Deprecated]
> **Last Updated**: YYYY-MM-DD
> **Template-Version**: 3.4

---

## Question
(검증 질문)

## Expected Answer (Criteria)
1. ...
2. ...

## Traceability
- **Solves by**: [REQ-XXX-001](../capabilities/REQ-XXX-001.md)
- **Constrained by**: [RULE-XXX-001](../invariants/RULE-XXX-001.md)
```

## Rules

1. **질문 중심**: 구현 방법이 아니라 답변 가능성에 집중
2. **추적성 필수**: 최소 1개 REQ/RULE 링크
3. **ID 일치**: 파일명 = **ID**: = 헤더 [ID]
