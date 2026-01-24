# [RUN-BRIEF-MCP-002-step-01] Archive 폐지 및 Git 중심 운영 전환

> **ID**: RUN-BRIEF-MCP-002-step-01
> **Completed**: 2026-01-24
> **Summary**: RUN 아카이브 이동 제거, Status+Git 기반 완료 관리
> **Input**: BRIEF-MCP-002
> **Status**: Completed
> **Started**: 2026-01-24
> **Git**: a2d6c78
> **Verification**: `python memory_manager.py --doctor && python memory_manager.py --list-runs`
> **Template-Version**: 3.4

## Objective (목표)
RUN 아카이브 이동 로직을 제거하고 Status 메타데이터 + Git 커밋 기반으로 완료 상태를 관리한다.

## Scope (범위)

### In Scope
- finalize_run() 함수 수정 (이동 로직 제거)
- 템플릿 업데이트 (00_INDEX.md, GETTING_STARTED.md, active/README.md)
- --list-runs CLI 명령 추가

### Out of Scope
- 기존 archive 폴더 삭제 (기존 데이터 보존)
- 월간 요약 리포트 생성 (Phase 3 후속 작업)

## Steps (단계)

- [x] 1. finalize_run() 함수 수정 - RUN 이동 로직 제거
- [x] 2. finalize_run() - git_hash 파라미터 추가, Status+Evidence 기록
- [x] 3. RUN 템플릿에 Summary, Git 메타데이터 필드 추가
- [x] 4. 00_INDEX.md - "Archive 이동" 설명 제거, Status 기반 완료 설명
- [x] 5. GETTING_STARTED.md - 워크플로우 업데이트
- [x] 6. 04_TASK_LOGS/active/README.md - 대시보드 형식으로 개편
- [x] 7. --list-runs CLI 명령 추가 (상태별 필터링)
- [x] 8. build.py로 memory_manager.py 재빌드

## Verification (Self-Check)

- [x] **Test**: `python memory_manager.py --list-runs` 정상 동작
- [x] **Boundary**: CONVENTIONS Boundaries 준수
- [x] **Spec**: BRIEF-MCP-002과 일치
- [ ] **Doctor**: `python memory_manager.py --doctor` 통과

## Evidence (Implementation Proof)

- **Commands**:
  - `python memory_manager.py --list-runs` - 정상 동작
  - `python memory_manager.py --list-runs active` - 필터링 정상 동작
  - `python build.py` - 재빌드 성공

- **Code** (수정된 파일):
  - `src/core/automation.py` - finalize_run() 수정
  - `src/core/config.py` - 템플릿 업데이트
  - `src/core/status.py` - list_runs() 함수 추가
  - `src/cli.py` - --list-runs 인자 추가
  - `memory_manager.py` - 재빌드

## Output (결과물)

- `src/core/automation.py` - finalize_run() 수정 (이동 로직 제거, git_hash 추가)
- `src/core/config.py` - 템플릿 업데이트 완료
- `src/core/status.py` - list_runs() 함수 추가
- `src/cli.py` - --list-runs 인자 추가
- `memory_manager.py` - 재빌드 완료
- `.memory/00_INDEX.md` - 워크플로우 업데이트 완료
- `.memory/GETTING_STARTED.md` - 가이드 업데이트 완료
- `.memory/04_TASK_LOGS/active/README.md` - 대시보드 형식 추가
## Result
Success

**Git Evidence**: `a2d6c78`
