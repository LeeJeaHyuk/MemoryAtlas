# [CQ-CORE-001] 자가 업데이트 문서화 (Self-Updating Documentation)

> **ID**: CQ-CORE-001
> **Domain**: CORE
> **Status**: Active
> **Last Updated**: 2026-01-24
> **Template-Version**: 3.4

---

## Question
시스템은 사용자의 명시적인 수동 편집 없이도 자체 문서와 상태를 업데이트할 수 있는가?

## Expected Answer (Criteria)
1. 시스템은 Intake -> Plan -> Finish 단계 이동 시 `01_PROJECT_BOARD.md`를 자동으로 업데이트해야 한다.
2. 시스템은 완료된 `RUN` 문서를 자동으로 아카이브해야 한다.
3. 시스템은 도구 호출을 통해 `task.md`나 상태 추적기를 업데이트할 수 있어야 한다.

## Traceability
- **Solves by**: [REQ-AUTO-001](../capabilities/REQ-AUTO-001.md)
- **Constrained by**: [RULE-FLOW-002](../invariants/RULE-FLOW-002.md)
