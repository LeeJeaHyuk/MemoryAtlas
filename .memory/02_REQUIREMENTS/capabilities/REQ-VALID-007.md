# [REQ-VALID-007] Full System Check (Doctor)

> **ID**: REQ-VALID-007
> **Domain**: VALID
> **Status**: Active
> **Last Updated**: 2026-01-20
> **Must-Read**: RULE-DIR-001, RULE-META-001, RULE-LINK-001, RULE-ID-001, RULE-VALID-001, RULE-MUST-001
> **Template-Version**: 2.4

---

## Decision (최종 결정)

모든 검증 기능을 통합 실행하여 `.memory/` 시스템의 무결성을 종합 검사한다.

**Source**: `src/core/checks.py:doctor()`

---

## Input

- `root` (str): `.memory` 디렉토리 경로
- `allow_absolute_links` (bool, optional): 절대 경로 링크 허용 여부

---

## Output

- `total_issues` (int): 전체 문제 개수
- Console output: 6단계 검증 결과 리포트

---

## Execution Flow

```
[1/6] Structure Check        → REQ-VALID-001
[2/6] Metadata Lint           → REQ-VALID-002
[3/6] Link Validation         → REQ-VALID-003
[4/6] Requirement Validation  → REQ-VALID-004
[5/6] RUN Document Validation → REQ-VALID-005
[6/6] Discussion Validation   → REQ-VALID-006
```

각 단계별 `issues` 누적 → `total_issues` 반환.

---

## Acceptance Criteria

- [x] 6가지 검증을 순차 실행
- [x] 각 단계별 결과 출력
- [x] 전체 문제 개수 누적
- [x] 최종 OK/FAIL 상태 표시
- [x] 문제 0개면 "All checks passed!" 출력

---

## Validation

```bash
python memory_manager.py --doctor
```

**성공 출력**:
```
============================================================
  MemoryAtlas Doctor - Full System Check
============================================================

[1/6] Structure Check
----------------------------------------
Structure check: 0 issue(s)

[2/6] Metadata Lint
----------------------------------------
Metadata lint: 0 issue(s)

[3/6] Link Validation
----------------------------------------
Link check: 0 issue(s)

[4/6] Requirement Validation (Authority)
----------------------------------------
Requirement check: 0 issue(s)

[5/6] RUN Document Validation (Execution)
----------------------------------------
RUN document check: 0 issue(s)

[6/6] Discussion Validation (Reference)
----------------------------------------
Discussion check: 0 issue(s)

============================================================
  [OK] All checks passed!
============================================================
```
