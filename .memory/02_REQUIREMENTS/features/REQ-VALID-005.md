# [REQ-VALID-005] RUN Document Validation

> **ID**: REQ-VALID-005
> **Domain**: VALID
> **Status**: Active
> **Last Updated**: 2026-01-20
> **Must-Read**: RULE-ID-001, RULE-VALID-001, RULE-META-001
> **Template-Version**: 2.4

---

## Decision (최종 결정)

RUN 문서(실행 로그)의 형식을 검증한다: 3-way ID 일치, 필수 필드(Input, Verification, Output 섹션).

**Source**: `src/core/checks.py:check_runs()`

---

## Input

- `root` (str): `.memory` 디렉토리 경로
- Scanned dirs: `RUN_SCAN_DIRS` (04_TASK_LOGS/active/)

---

## Output

- `issues` (int): 발견된 문제 개수
- Console output: 상세 오류 메시지

---

## Logic

1. `04_TASK_LOGS/active/`의 모든 RUN 문서 순회
2. 파일명 패턴 검증: `RUN-(REQ|RULE)-[DOMAIN]-[NNN]-step-[NN].md`
3. **3-way ID 일치**: 파일명 = `**ID**:` = `# [ID]`
4. 필수 필드 존재:
   - `> **Input**:` (읽을 문서 목록)
   - `> **Verification**:` (검증 조건)
   - `## Output` 또는 `### Output` 섹션

---

## Acceptance Criteria

- [x] 파일명이 `RUN_ID_PATTERN` 패턴 준수
- [x] `**ID**:` 메타데이터 필수
- [x] `# [RUN-...]` 헤더 필수
- [x] 3개 ID 정확히 일치
- [x] `**Input**:` 필드 필수
- [x] `**Verification**:` 필드 필수
- [x] `## Output` 또는 `### Output` 섹션 필수

---

## Validation

```bash
python memory_manager.py --runs
```

**실패 예시**:
```
! Invalid RUN filename format: RUN-AUTH-001.md
  -> Expected: RUN-REQ-[DOMAIN]-[NNN]-step-[NN].md
! Missing **Input**: field in RUN-REQ-AUTH-001-step-01.md
! Missing ## Output section in RUN-REQ-AUTH-001-step-02.md
RUN document check: 3 issue(s)
```
