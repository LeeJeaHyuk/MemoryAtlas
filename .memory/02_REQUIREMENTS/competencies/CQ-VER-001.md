# [CQ-VER-001] 버전 호환성 (Version Compatibility)

> **ID**: CQ-VER-001
> **Domain**: VERSION
> **Status**: Active
> **Last Updated**: 2026-01-24
> **Template-Version**: 3.4

---

## Question
시스템은 템플릿 버전(Template Version)과 코드 버전(Manager Version) 간의 호환성을 관리할 수 있는가?

## Expected Answer (Criteria)
1. 시스템은 코드 버전(`CURRENT_VERSION`)과 문서 템플릿 버전(`TEMPLATE_VERSION`)을 독립적으로 관리해야 한다.
2. 시스템은 업데이트 시 변경된 템플릿 버전이 기존 문서와 충돌하지 않는지(또는 마이그레이션이 필요한지) 판단해야 한다.
3. 시스템은 빌드 시 버전을 명시하여 배포 무결성을 보장해야 한다.

## Traceability
- **Solves by**: [REQ-AUTO-001](../capabilities/REQ-AUTO-001.md)
- **Constrained by**: [RULE-VER-001](../invariants/RULE-VER-001.md)
