# [REQ-VALID-004] Requirement Document Validation

> **ID**: REQ-VALID-004
> **Domain**: VALID
> **Status**: Active
> **Last Updated**: 2026-01-20
> **Must-Read**: RULE-ID-001, RULE-VALID-001, RULE-MUST-001
> **Template-Version**: 2.4

---

## Decision (최종 결정)

REQ/RULE 문서의 3-way ID 일치성, Must-Read 필드, 링크 무결성을 검증한다 (Authority Model 구현).

**Source**: `src/core/checks.py:check_requirements()`

---

## Input

- `root` (str): `.memory` 디렉토리 경로
- Scanned dirs: `REQ_SCAN_DIRS` (features/, business_rules/)

---

## Output

- `issues` (int): 발견된 문제 개수
- Console output: 상세 오류 메시지

---

## Logic

**Phase 1**: 모든 문서 ID 수집 (REQ, RULE, DISC, ADR)

**Phase 2**: 각 문서 검증
1. **3-way ID 일치**: 파일명 = `**ID**:` = `# [ID]`
2. **Must-Read 필드 존재**: 필수
3. **Must-Read 제약**: RULE/ADR만 허용, 최소 1개
4. **Must-Read 참조 존재**: 모든 참조 ID 실제 존재
5. **중복 ID 없음**

---

## Acceptance Criteria

- [x] 파일명 패턴 검증 (`REQ_ID_PATTERN`, `RULE_ID_PATTERN`)
- [x] `**ID**:` 메타데이터 필수
- [x] `# [ID]` 헤더 필수
- [x] 3개 ID 정확히 일치
- [x] `**Must-Read**:` 필드 필수
- [x] Must-Read에 REQ/RULE/ADR 외 ID 금지
- [x] 빈 Must-Read 금지
- [x] 참조 문서 존재 확인
- [x] 중복 ID 감지

---

## Validation

```bash
python memory_manager.py --req
```

**실패 예시**:
```
! Invalid filename format in 02_REQUIREMENTS/features/req-auth-001.md
! Filename does not match **ID**: in REQ-AUTH-001.md
  -> **ID**: REQ-AUTH-002
  -> Filename: REQ-AUTH-001
! Must-Read allows only RULE/ADR IDs in REQ-DATA-001.md: REQ-AUTH-001
! Empty **Must-Read**: list in RULE-SEC-001.md
Requirement check: 4 issue(s)
```
