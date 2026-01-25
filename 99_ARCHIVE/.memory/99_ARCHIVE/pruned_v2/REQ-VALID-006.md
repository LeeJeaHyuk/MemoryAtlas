# [REQ-VALID-006] Discussion Document Validation

> **ID**: REQ-VALID-006
> **Domain**: VALID
> **Status**: Active
> **Last Updated**: 2026-01-20
> **Must-Read**: RULE-ID-001, RULE-VALID-001, RULE-META-001
> **Template-Version**: 2.4

---

## Decision (최종 결정)

DISC 문서(논의 기록)의 3-way ID 일치성을 검증한다.

**Source**: `src/core/checks.py:check_discussions()`

---

## Input

- `root` (str): `.memory` 디렉토리 경로
- Scanned dirs: `02_REQUIREMENTS/discussions/`

---

## Output

- `issues` (int): 발견된 문제 개수
- Console output: 상세 오류 메시지

---

## Logic

1. `discussions/` 폴더의 모든 DISC 문서 순회
2. 파일명 패턴 검증: `DISC-[DOMAIN]-[NNN].md`
3. **3-way ID 일치**: 파일명 = `**ID**:` = `# [ID]`

---

## Acceptance Criteria

- [x] 파일명이 `DISC_ID_PATTERN` 패턴 준수
- [x] `**ID**:` 메타데이터 필수
- [x] `# [DISC-...]` 헤더 필수
- [x] 3개 ID 정확히 일치
- [x] README.md 스킵

---

## Validation

```bash
python memory_manager.py --doctor
```

4/6 단계에서 DISC 검증 포함됨.

**실패 예시**:
```
! Invalid DISC filename format in DISC-AUTH-1.md
! Missing **ID**: metadata in DISC-AUTH-001.md
! Header does not match **ID**: in DISC-AUTH-001.md
  -> **ID**: DISC-AUTH-001
  -> Header: DISC-AUTH-002
Discussion check: 3 issue(s)
```
