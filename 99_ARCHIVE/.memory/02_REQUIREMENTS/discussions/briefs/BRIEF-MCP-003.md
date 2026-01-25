# [BRIEF-MCP-003] Request: 
# 3-Step Workflow 단순화 (Intake → Plan → Finish)

#...

> **ID**: BRIEF-MCP-003
> **Date**: 2026-01-24
> **Status**: Active
> **Template-Version**: 3.4

## 1. User Request (원본 요청)
> 
# 3-Step Workflow 단순화 (Intake → Plan → Finish)

## 핵심 요청
MCP/수동 이중 경로를 단일 경로로 통합하고 함수명을 직관적으로 변경

## 주요 변경사항
1. 함수 리네이밍
   - plan_from_brief() → plan()
   - finalize_run() → finish()
   
2. REQ 관리 주체 변경
   - 이전: 사용자가 REQ 직접 작성
   - 이후: plan() 단계에서 시스템이 자동 갱신
   
3. 수동 Intake 공식 지원
   - briefs/ 폴더에 파일 직접 생성 = Intake 완료로 간주

4. README.md 전면 개편
   - 3-Step Workflow 중심으로 단순화
   - 복잡한 R&R 내용 제거

## 영향 범위
- src/core/automation.py - 함수 리네이밍 + plan() 로직 추가
- src/cli.py - CLI 도움말 업데이트
- src/core/config.py - 템플릿 업데이트
- README.md - 전면 개편
- .memory/00_INDEX.md - 워크플로우 업데이트

## 검증 기준
- plan() 호출 시 REQ 자동 갱신 + RUN 생성
- finish() 호출 시 Status 완료 + Git Evidence 기록
- 수동으로 Brief 생성 후 plan() 정상 동작


## 2. Intent Summary (의도 요약)

- **주요 목표**: MCP/수동 이중 경로를 단일 3-Step Workflow(Intake→Plan→Finish)로 통합
- **해결할 문제**:
  - 함수명 비직관적 (plan_from_brief, finalize_run)
  - REQ 수동 작성의 번거로움
  - MCP/Manual 이중 문서화로 인한 복잡성
- **접근 방식**: 함수 리네이밍 + REQ 자동관리 + README 단순화

## 3. Affected Artifacts (영향받는 문서)

- **Modify**: [REQ-MCP-003](02_REQUIREMENTS/capabilities/REQ-MCP-003.md)
- **Read**:
  - `src/core/automation.py` (현재 plan_from_brief, finalize_run)
  - `README.md` (현재 문서 구조)

## 4. Proposed Changes (변경 제안)

### Phase 1: 함수 리네이밍
1. `plan_from_brief()` → `plan()` 리네이밍
2. `finalize_run()` → `finish()` 리네이밍
3. 기존 함수명은 별칭(alias)으로 유지 (하위호환)

### Phase 2: REQ 자동관리
4. `plan()` 호출 시 REQ 자동 생성/갱신 로직 추가
5. REQ 템플릿 간소화 (시스템 자동생성용)

### Phase 3: 문서 업데이트
6. `README.md` 전면 개편 - 3-Step Workflow 중심
7. `.memory/00_INDEX.md` 워크플로우 섹션 업데이트
8. CLI 도움말 메시지 업데이트

## 5. Verification Criteria (검증 기준)

- [ ] `plan("BRIEF-XXX")` 호출 시 RUN 정상 생성
- [ ] `plan()` 호출 시 REQ 자동 생성/갱신
- [ ] `finish("RUN-XXX")` 호출 시 Status 완료 + Git Evidence 기록
- [ ] 기존 함수명(plan_from_brief, finalize_run) 별칭으로 동작
- [ ] README.md에 3-Step Workflow 명확히 설명
