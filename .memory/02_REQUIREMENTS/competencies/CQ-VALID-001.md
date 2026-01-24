# [CQ-VALID-001] 문서 무결성 (Document Integrity)

> **ID**: CQ-VALID-001
> **Domain**: VALIDATION
> **Status**: Active
> **Last Updated**: 2026-01-24
> **Template-Version**: 3.4

---

## Question
시스템은 깨진 링크, 잘못된 메타데이터, 형식이 어긋난 문서를 스스로 감지하고 리포트할 수 있는가?

## Expected Answer (Criteria)
1. 시스템은 모든 오프라인 문서 내의 상대 링크 유효성을 검증할 수 있어야 한다.
2. 시스템은 문서 타입별 필수 메타데이터 필드 누락을 감지해야 한다.
3. 시스템은 3-Way Consistency(파일명-ID-헤더) 불일치를 식별해야 한다.

## Traceability
- **Solves by**: [REQ-AUTO-001](../capabilities/REQ-AUTO-001.md)
- **Constrained by**: [RULE-VALID-001](../invariants/RULE-VALID-001.md), [RULE-LINK-001](../invariants/RULE-LINK-001.md), [RULE-META-001](../invariants/RULE-META-001.md)
