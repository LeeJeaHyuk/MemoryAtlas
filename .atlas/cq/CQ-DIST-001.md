# [CQ-DIST-001] 단일 파일 배포

> **ID**: CQ-DIST-001
> **Domain**: DIST
> **Status**: Draft
> **Last Updated**: 2026-01-26

---

## Question
- `atlas.py` 단일 파일만으로 다른 프로젝트에 배포했을 때, `init` 명령어로 모든 구조(templates, prompts, src 등)가 생성되어야 하는가?

## Expected Answer (Criteria)
1. `atlas.py` 파일 하나만 복사하여 배포 가능
2. `python atlas.py init` 실행 시 완전한 `.atlas/` 구조 생성
3. `.atlas/.system/src/atlas_cli.py`에 **원본 소스 코드** 생성 (stickytape wrapper 없음)
4. 외부 의존성 없이 독립 실행 가능
5. `atlas.py`는 배포 산출물이므로 **절대 직접 수정하지 않고**, 항상 빌드 프로세스를 통해 생성되어야 한다.

## Traceability
- **Source**: CQ-SYNC-001 5번 항목에서 분리
- **Solved by**: [REQ-DIST-001](../req/REQ-DIST-001.md)
