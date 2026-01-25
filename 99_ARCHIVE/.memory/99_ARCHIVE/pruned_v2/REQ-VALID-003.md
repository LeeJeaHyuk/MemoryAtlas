# [REQ-VALID-003] Link Validation

> **ID**: REQ-VALID-003
> **Domain**: VALID
> **Status**: Active
> **Last Updated**: 2026-01-20
> **Must-Read**: RULE-LINK-001
> **Template-Version**: 2.4

---

## Decision (최종 결정)

문서 내 모든 마크다운 링크가 유효한 파일을 가리키는지 검증한다.

**Source**: `src/core/checks.py:check_links()`

---

## Input

- `root` (str): `.memory` 디렉토리 경로
- `allow_absolute` (bool, optional): 절대 경로 링크 허용 여부 (기본값: False)

---

## Output

- `issues` (int): 깨진 링크 개수
- Console output: 깨진 링크 목록

---

## Logic

1. `LINK_SCAN_DIRS`의 모든 마크다운 파일 순회
2. 코드 블록 제외하고 링크 추출 (`iter_links()`)
3. 각 링크에 대해:
   - 앵커(#)만 있으면 스킵
   - 외부 URL (`http://`, `https://`) 스킵
   - 절대 경로: `allow_absolute=false`면 오류
   - 상대 경로: 파일 존재 여부 확인
4. 존재하지 않는 파일 링크는 오류 보고

---

## Acceptance Criteria

- [x] `LINK_RE` 정규식으로 마크다운 링크 추출
- [x] 코드 블록(```) 내부 링크 제외
- [x] 상대 경로 링크 검증
- [x] 절대 경로 링크 선택적 허용
- [x] 깨진 링크마다 `! Broken link in {file}: {target}` 출력
- [x] 총 문제 개수 반환

---

## Validation

```bash
# 기본 검증 (절대 경로 금지)
python memory_manager.py --links

# 절대 경로 허용
python memory_manager.py --links --allow-absolute-links
```

**실패 예시**:
```
! Broken link in 02_REQUIREMENTS/README.md: ../business_rules/RULE-FAKE-999.md
Link check: 1 issue(s)
```
