# [CQ-CORE-003] 추적성 (Traceability)

> **ID**: CQ-CORE-003
> **Domain**: CORE
> **Status**: Active
> **Last Updated**: 2026-01-24
> **Template-Version**: 3.4

---

## Question
시스템은 구현된 모든 기능을 특정 Authority Document(REQ/CQ)로 추적할 수 있는가?

## Expected Answer (Criteria)
1. 모든 `RUN` 문서는 `BRIEF` 또는 `REQ`를 참조해야 한다.
2. 모든 `REQ`는 최소 하나의 `CQ`(해결) 또는 `RULE`(제약)을 참조해야 한다.
3. 고아 코드(연결된 요구사항이 없는 코드)는 제거 대상으로 식별되어야 한다.

## Traceability
- **Solves by**: [REQ-AUTO-001](../capabilities/REQ-AUTO-001.md)
- **Constrained by**: [RULE-VALID-001](../invariants/RULE-VALID-001.md), [RULE-META-001](../invariants/RULE-META-001.md)
