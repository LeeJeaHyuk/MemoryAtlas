# [CQ-STRUCT-001] 구조 강제성 (Structure Enforcement)

> **ID**: CQ-STRUCT-001
> **Domain**: STRUCTURE
> **Status**: Active
> **Last Updated**: 2026-01-24
> **Template-Version**: 3.4

---

## Question
시스템은 정해진 15개 표준 디렉토리 구조를 강제로 유지하고, 누락 시 자동 생성할 수 있는가?

## Expected Answer (Criteria)
1. 시스템은 필수 디렉토리 목록(`DIRS`)을 기반으로 현재 구조를 검사해야 한다.
2. 시스템은 `--update` 명령 시 누락된 디렉토리 트리를 복구해야 한다.
3. 시스템은 임의의 최상위 폴더 생성을 경고하거나 관리할 수 있어야 한다.

## Traceability
- **Solves by**: [REQ-AUTO-001](../capabilities/REQ-AUTO-001.md)
- **Constrained by**: [RULE-DIR-001](../invariants/RULE-DIR-001.md)
