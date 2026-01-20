# [REQ-MGT-002] Context Bootstrapping

> **ID**: REQ-MGT-002
> **Domain**: MGT
> **Status**: Active
> **Last Updated**: 2026-01-20
> **Must-Read**: RULE-DIR-001
> **Template-Version**: 2.4

---

## Decision (최종 결정)

AI 주도로 프로젝트 컨텍스트(GOALS, CONVENTIONS)를 초기화하기 위한 부트스트래핑 파일을 생성한다.

**Source**: `src/core/bootstrap.py:bootstrap_init()`

---

## Input

- `root` (str): `.memory` 디렉토리 경로
- `dry_run` (bool): 변경 사항 미리보기 모드

---

## Output

- `BOOTSTRAP_PROMPT.md`: AI 인터뷰용 프롬프트
- `01_PROJECT_CONTEXT/GOALS.md`: (빈 템플릿)
- `01_PROJECT_CONTEXT/CONVENTIONS.md`: (빈 템플릿)

---

## Logic

1. `.memory/01_PROJECT_CONTEXT/` 폴더 생성
2. `BOOTSTRAP_PROMPT.md` 파일 생성 (AI 킥오프 미팅 아젠다 포함)
3. `GOALS.md`와 `CONVENTIONS.md` 템플릿 파일 생성
4. 사용자 가이드 출력

---

## Acceptance Criteria

- [x] `--bootstrap` 플래그로 실행
- [x] `BOOTSTRAP_PROMPT.md` 생성
- [x] `GOALS.md`, `CONVENTIONS.md`가 없으면 생성
- [x] 이미 존재하면 덮어쓰지 않고 SKIP
- [x] 다음 단계 가이드 출력

---

## Validation

```bash
python memory_manager.py --bootstrap
```
