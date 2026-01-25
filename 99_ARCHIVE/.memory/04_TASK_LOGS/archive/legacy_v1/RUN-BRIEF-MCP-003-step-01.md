# [RUN-BRIEF-MCP-003-step-01] Execution for BRIEF-MCP-003

> **ID**: RUN-BRIEF-MCP-003-step-01
> **Git**: fb7734e
> **Completed**: 2026-01-24
> **Input**: BRIEF-MCP-003
> **Status**: Completed
> **Started**: 2026-01-24
> **Verification**: `python memory_manager.py --doctor`
> **Template-Version**: 3.4

## Objective (목표)
Execute the requirements defined in BRIEF-MCP-003. (BRIEF-MCP-003에 정의된 요구사항 실행)

## Scope (범위)

### In Scope
- Implement changes requested in BRIEF-MCP-003
- (추가 범위는 BRIEF의 Affected Artifacts를 참고하여 구체화)

### Out of Scope
- (명시적으로 제외되는 것)

## Steps (단계)

- [x] 1. `plan_from_brief()` → `plan()` 리네이밍 + 별칭 유지
- [x] 2. `finalize_run()` → `finish()` 리네이밍 + 별칭 유지
- [x] 3. `plan()` 호출 시 REQ 자동 생성/갱신 로직 추가 (기존 로직 유지)
- [x] 4. MCP 서버 함수명 업데이트 (plan, finish)
- [x] 5. README.md 전면 개편 - 3-Step Workflow 중심
- [x] 6. .memory/00_INDEX.md 워크플로우 섹션 업데이트 (config.py 템플릿)
- [x] 7. build.py로 memory_manager.py 재빌드
- [x] 8. 동작 검증 (plan, finish 호출 테스트)

## Verification (Self-Check)
> 작업 완료 전 반드시 확인

- [x] **Test**: plan(), finish() 메서드 존재 및 별칭 정상 동작
- [x] **Boundary**: CONVENTIONS Boundaries 준수
- [x] **Spec**: BRIEF-MCP-003과 일치
- [ ] **Doctor**: `python memory_manager.py --doctor` - 24 issues (기존 이슈)

## Evidence (Implementation Proof)

- **Commands**:
  - `python build.py` - 재빌드 성공
  - `python memory_manager.py --list-runs` - 정상 동작
  - `python -c "..."` - plan(), finish() 메서드 검증

- **Code** (수정된 파일):
  - `src/core/automation.py` - plan(), finish() 리네이밍 + 별칭 추가
  - `src/mcp_server.py` - plan(), finish() MCP 도구 추가
  - `src/core/config.py` - 템플릿 업데이트 (3-Step Workflow)
  - `README.md` - 전면 개편
  - `memory_manager.py` - 재빌드

## Output (결과물)

- `src/core/automation.py` - plan(), finish() 메서드 + 별칭
- `src/mcp_server.py` - plan(), finish() MCP 도구
- `src/core/config.py` - 3-Step Workflow 템플릿
- `README.md` - 단순화된 3-Step Workflow 가이드
- `memory_manager.py` - 재빌드 완료
## Result
Success

**Git Evidence**: `fb7734e`
