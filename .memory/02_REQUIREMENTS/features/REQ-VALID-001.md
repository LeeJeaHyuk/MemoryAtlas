# [REQ-VALID-001] Directory Structure Validation

> **ID**: REQ-VALID-001
> **Domain**: VALID
> **Status**: Active
> **Last Updated**: 2026-01-20
> **Must-Read**: RULE-DIR-001
> **Template-Version**: 2.4

---

## Decision (최종 결정)

`.memory/` 폴더의 14개 필수 디렉토리가 모두 존재하는지 검증하고, 누락된 경우 오류를 보고한다.

**Source**: `src/core/checks.py:check_structure()`

---

## Input

- `root` (str): `.memory` 디렉토리 경로

---

## Output

- `issues` (int): 발견된 문제 개수
- Console output: 누락된 디렉토리 목록

---

## Acceptance Criteria

- [x] 14개 필수 디렉토리 목록을 `DIRS` 상수에서 읽음
- [x] 각 디렉토리 존재 여부 확인
- [x] 누락된 디렉토리마다 `! Missing directory: {folder}` 출력
- [x] VERSION 파일 존재 여부 확인
- [x] 시스템 템플릿 파일(AGENT_RULES.md 등) 존재 확인
- [x] 총 문제 개수 반환

---

## Validation

```bash
python memory_manager.py --check
```

**성공 예시**:
```
Structure check: 0 issue(s)
```

**실패 예시**:
```
! Missing directory: 04_TASK_LOGS/active
! Missing file: VERSION
Structure check: 2 issue(s)
```
