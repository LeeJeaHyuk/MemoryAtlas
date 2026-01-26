# [RUN-BRIEF-SYNC-001-step-01] sync 명령어 구현

> **ID**: RUN-BRIEF-SYNC-001-step-01
> **Brief**: BRIEF-SYNC-001
> **Status**: Completed
> **Started**: 2026-01-26
> **Git**: -
> **Completed**: -

## Input
- [BRIEF-SYNC-001](../brief/BRIEF-SYNC-001.md)
- [REQ-SYNC-001](../req/REQ-SYNC-001.md)
- [src/atlas_cli.py](../../src/atlas_cli.py) (기존 CLI 구조)

## Steps

### Phase 1: 문서 파싱 유틸리티
- [x] 체크박스 파싱 함수 (`parse_checkboxes`)
- [x] Traceability 링크 파싱 함수 (`parse_traceability`)
- [x] RUN → BRIEF → REQ 연결 탐색 함수

### Phase 2: sync 명령어 핵심 로직
- [x] `sync_command` 함수 구현
- [x] dry-run 기본 동작 (diff 출력)
- [x] `--apply-brief` 옵션 구현
- [x] `--write-req-patch` 옵션 구현
- [x] `--apply-req` 옵션 구현 (경고 포함)

### Phase 3: CLI 통합
- [x] `build_parser()`에 sync 명령어 추가
- [x] `main()`에 sync 분기 추가

### Phase 4: 빌드 및 테스트
- [x] `python build.py`로 atlas.py 재빌드
- [x] 실제 RUN 문서로 테스트

## Verification
- [x] `atlas sync RUN-BRIEF-SYNC-001-step-01` dry-run 동작
- [x] `--apply-brief`로 BRIEF 수정 확인
- [x] `--write-req-patch`로 Patch 파일 생성 확인
- [x] `atlas doctor` 통과

## Output
- src/atlas_cli.py (수정)
- atlas.py (재빌드)
- .atlas/patch/ (폴더 생성)
