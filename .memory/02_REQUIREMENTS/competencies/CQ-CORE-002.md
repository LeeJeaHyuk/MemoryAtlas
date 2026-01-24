# [CQ-CORE-002] 경계 시행 (Boundary Enforcement)

> **ID**: CQ-CORE-002
> **Domain**: CORE
> **Status**: Active
> **Last Updated**: 2026-01-24
> **Template-Version**: 3.4

---

## Question
시스템은 Core Constitution(CQs)에 부합하지 않는 요구사항이나 코드 변경을 거부하는가?

## Expected Answer (Criteria)
1. `intake` 프로세스는 활성 CQ에 부합하지 않는 아이디어를 걸러내야 한다.
2. `plan` 프로세스는 구현 단계를 유효한 REQ/CQ에 명시적으로 연결해야 한다.
3. 무분별한 기능 추가(Feature Creep)는 차단되어야 한다.

## Traceability
- **Solves by**: [REQ-AUTO-001](../capabilities/REQ-AUTO-001.md)
- **Constrained by**: [RULE-MUST-001](../invariants/RULE-MUST-001.md), [RULE-LINK-001](../invariants/RULE-LINK-001.md), [RULE-ID-001](../invariants/RULE-ID-001.md)
