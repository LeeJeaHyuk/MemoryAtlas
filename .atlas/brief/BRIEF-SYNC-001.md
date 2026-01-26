# [BRIEF-SYNC-001] 상태 동기화 도구 구현

> **ID**: BRIEF-SYNC-001
> **Domain**: SYNC
> **Status**: Completed
> **Date**: 2026-01-26
> **Implements**: [REQ-SYNC-001](../req/REQ-SYNC-001.md)

---

## 1. User Request
- RUN 문서 완료 시 BRIEF/REQ 문서의 체크박스와 Status를 자동 동기화하는 도구 필요
- REQ는 권위 문서로 자동 수정 금지, Patch만 생성
- CLI 중심 + Git Hook 보조 구조

## 2. Intent Summary
- **Goal**: `atlas sync` / `atlas finish` CLI 명령어 구현
- **Problem**: 현재 RUN 완료 후 BRIEF/REQ 상태를 수동으로 업데이트해야 함

## 3. Affected Artifacts

| Action | Path | Description |
|--------|------|-------------|
| Create | `.atlas/.system/src/sync.py` | sync 명령어 핵심 로직 |
| Create | `.atlas/.system/src/finish.py` | finish 명령어 (sync 래퍼) |
| Create | `.atlas/patch/` | REQ Patch 파일 저장 폴더 |
| Modify | `.atlas/.system/src/atlas_cli.py` | CLI 진입점에 명령어 추가 |
| Read | `.atlas/runs/`, `.atlas/brief/`, `.atlas/req/` | 동기화 대상 문서 |

## 4. Proposed Changes

### Step 1: 문서 파싱 모듈
- [ ] RUN/BRIEF/REQ 문서의 체크박스 파싱
- [ ] Status 필드 추출
- [ ] Traceability 링크 파싱 (연결된 문서 탐색)

### Step 2: sync 명령어 구현
- [ ] dry-run 기본 동작 (diff 출력)
- [ ] `--apply-brief` 옵션
- [ ] `--write-req-patch` 옵션
- [ ] `--apply-req` 옵션 (경고 포함)

### Step 3: finish 명령어 구현
- [ ] sync 호출 래퍼
- [ ] `--success` 플래그로 Status 결정
- [ ] Git 연동 옵션

### Step 4: 통합 및 테스트
- [ ] atlas_cli.py에 명령어 등록
- [ ] 실제 문서로 동기화 테스트

## 5. Verification Criteria
- [ ] `atlas sync <RUN-ID>` 실행 시 dry-run diff 출력
- [ ] `--apply-brief`로 BRIEF 문서 수정 확인
- [ ] `--write-req-patch`로 Patch 파일 생성 확인
- [ ] Traceability 링크 따라 연결 문서 탐색 확인

---

## Traceability
- **Implements**: [REQ-SYNC-001](../req/REQ-SYNC-001.md)
- **Answers**: [CQ-SYNC-001](../cq/CQ-SYNC-001.md)
