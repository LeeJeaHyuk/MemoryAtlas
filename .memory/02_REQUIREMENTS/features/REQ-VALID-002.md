# [REQ-VALID-002] Metadata Header Validation

> **ID**: REQ-VALID-002
> **Domain**: VALID
> **Status**: Active
> **Last Updated**: 2026-01-20
> **Must-Read**: RULE-META-001
> **Template-Version**: 2.4

---

## Decision (최종 결정)

문서 타입별로 정해진 메타데이터 필드가 문서 상단에 존재하는지 검증한다.

**Source**: `src/core/checks.py:lint_metadata()`

---

## Input

- `root` (str): `.memory` 디렉토리 경로
- Document scanned: `LINT_DIRS`에 정의된 디렉토리

---

## Output

- `issues` (int): 누락된 필드 개수
- Console output: 누락된 필드 목록

---

## Logic

1. `LINT_DIRS`의 모든 마크다운 파일 순회
2. `README.md`, `00_INDEX.md` 스킵
3. 문서 타입 감지 (`get_doc_type()`)
4. `HEADER_FIELDS_BY_TYPE`에서 필수 필드 조회
5. 문서 상위 40줄에 해당 필드 존재 확인
6. 누락 시 오류 보고

---

## Acceptance Criteria

- [x] 문서 타입별 필수 필드 정의 (features, business_rules, decisions, discussions, runs)
- [x] 코드 블록 제외하고 메타데이터 영역만 검사
- [x] 누락된 필드마다 `! Missing header fields in {file}: {fields}` 출력
- [x] 총 문제 개수 반환

---

## Validation

```bash
python memory_manager.py --lint
```

**실패 예시**:
```
! Missing header fields in 02_REQUIREMENTS/features/REQ-AUTH-001.md: **Domain**, **Must-Read**
Metadata lint: 1 issue(s)
```
