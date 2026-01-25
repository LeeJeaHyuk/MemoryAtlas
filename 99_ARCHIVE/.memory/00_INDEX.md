# Project Memory Index

> Entry point for Memory-Driven Development in this repo.
> **Version**: 3.4.1 (Smart Spec Edition)
> **Template Version**: 3.4

## Capabilities, Invariants & Competencies Model (v3.1)

```
02_REQUIREMENTS/ 구조:
  capabilities/   - REQ-* (기능/행동) "시스템은 ~해야 한다"
  invariants/     - RULE-* (불변 규칙) "항상 ~이다 / ~는 금지"
  competencies/  - CQ-* (역량 질문) "시스템은 ~에 답할 수 있는가?"
  discussions/    - DISC-* (조율 기록) LLM 기본 무시

REQ vs RULE vs CQ 판정:
  REQ  = Input/Output/Acceptance Criteria 필수 (동작 중심)
  RULE = Scope/Violation/Examples 필수 (불변 중심)
  CQ   = Question/Expected Answer/Traceability 필수 (검증 중심)
```

## Quick Navigation

| Folder | Purpose | Authority Level |
|--------|---------|-----------------|
| `01_PROJECT_CONTEXT/` | 프로젝트 헌법 + **Boundaries** | Constitution |
| `02_REQUIREMENTS/capabilities/` | 기능 **결정** (REQ-*) | Authority |
| `02_REQUIREMENTS/invariants/` | 불변 규칙 **결정** (RULE-*) | Authority |
| `02_REQUIREMENTS/competencies/` | 역량 질문 **검증** (CQ-*) | Authority |
| `02_REQUIREMENTS/discussions/` | 조율 기록 (DISC-*) | Reference |
| `03_TECH_SPECS/` | 기술 설계 & ADR | Implementation |
| `04_TASK_LOGS/` | 실행 기록 (RUN-*) | Execution |
| `98_KNOWLEDGE/` | 배운 점 | Asset |

## Start Here (For AI Agents)

### Reading Priority (P0 = Must Read)
1. **P0**: `01_PROJECT_CONTEXT/01_CONVENTIONS.md` - **특히 Boundaries 섹션** ⭐
2. **P0**: Target REQ's `**Must-Read**` field
3. **P1**: `02_REQUIREMENTS/invariants/` (all active)
4. **P1.5**: `02_REQUIREMENTS/competencies/` (referenced CQs only)
5. **P2**: `98_KNOWLEDGE/` (if complex feature)

## 3-Step Workflow (Intake → Plan → Finish)

1. **Intake**: 생각/메모 → BRIEF 생성 (`02_REQUIREMENTS/discussions/briefs/`)
2. **Plan**: BRIEF → RUN 생성 (`04_TASK_LOGS/active/`)
3. **Finish**: 구현 완료 → Status 업데이트 + Git 증거

> MCP 도구: `intake()` → `plan()` → `finish()`

### Execution Checklist
1. [ ] **Intake**: BRIEF 생성 및 검토
2. [ ] **Plan**: RUN 문서 생성 및 검토
3. [ ] 구현 → 테스트 → Git 커밋
4. [ ] **Finish**: Self-Check 통과 후 finish() 호출 (Status → Completed)

## Quick Start (MCP 도구 사용법)

### 1. "Intake 해줘"
```python
intake("사용자 요청 내용", domain="GEN")
```
→ 반환: BRIEF 파일 경로 (예: `BRIEF-GEN-001`)

### 2. "Plan 만들어줘"
```python
plan("BRIEF-GEN-001")
```
→ 반환: RUN ID (예: `RUN-BRIEF-GEN-001-step-01`)

### 3. "작업 완료"
1. RUN 문서의 Steps 실행
2. Self-Check 확인
3. Git 커밋 생성
4. 완료 후:
```python
finish("RUN-BRIEF-GEN-001-step-01", git_hash="abc123")
```
→ Status가 Completed로 변경 + Git 증거 기록

### 예시 대화
```
User: "로그인 기능 추가해줘. intake 해"
LLM:  intake("로그인 기능 추가", domain="AUTH") 호출
LLM:  BRIEF 생성 → 사용자 검토 요청
User: "plan 만들어"
LLM:  plan("BRIEF-AUTH-001") 호출
LLM:  RUN 생성 → 사용자 검토 요청
User: "run 해"
LLM:  RUN Steps 실행 → Self-Check → finish()
```

## Manual Fallback (MCP 없이)

MCP 도구 사용이 불가능하거나 원하지 않는 경우, 동일한 워크플로우를 수동으로 수행할 수 있습니다.

### 1. BRIEF 직접 작성
- **템플릿**: `02_REQUIREMENTS/discussions/briefs/README.md` 참조
- **위치**: `02_REQUIREMENTS/discussions/briefs/BRIEF-DOMAIN-001.md`
- **필수 섹션**: User Request, Intent Summary, Affected Artifacts, Proposed Changes, Verification Criteria

### 2. REQ/RUN 직접 작성
- **REQ 템플릿**: `02_REQUIREMENTS/capabilities/README.md` 참조
- **REQ 위치**: `02_REQUIREMENTS/capabilities/REQ-DOMAIN-001.md`
- **RUN 템플릿**: `04_TASK_LOGS/active/README.md` 참조
- **RUN 위치**: `04_TASK_LOGS/active/RUN-BRIEF-DOMAIN-001-step-01.md`

### 3. 완료 처리 (수동)
- RUN 문서의 Status를 `Completed` 또는 `Failed`로 변경
- Git 커밋 해시를 Evidence에 기록
- RUN은 `active/`에 유지 (이동 없음)

> ⚠️ MCP 도구 사용이 권장됩니다. 수동 프로세스는 동일한 결과를 만들지만 더 많은 작업이 필요합니다.

## Direct Execute (간단한 작업)

다음 조건을 **모두** 만족하면 BRIEF/RUN 없이 바로 실행 가능:

### Skip 가능 조건
- 단일 파일 수정
- 아키텍처 영향 없음
- 명백한 변경 (typo 수정, 단순 버그 픽스)
- 새 의존성 없음
- 검증이 자명함 (에러 해결 = 성공)

### 예시
| 작업 | 경로 |
|------|------|
| README 오타 수정 | ✅ Direct Execute |
| 로그 메시지 추가 | ✅ Direct Execute |
| 단순 import 수정 | ✅ Direct Execute |
| 새 API 엔드포인트 | ❌ 3-Phase 필요 |
| 인증 로직 변경 | ❌ 3-Phase 필요 |
| 다중 파일 리팩토링 | ❌ 3-Phase 필요 |

### 주의사항
- Skip 시에도 **커밋 메시지에 변경 이유 명시**
- 불확실하면 → Intake 진행 권장

### What NOT to Read by Default
- `02_REQUIREMENTS/discussions/` - Only when explicitly referenced
- `04_TASK_LOGS/archive/` - Only for historical context
- `99_ARCHIVE/` - Deprecated content

## Document Map

### 01_PROJECT_CONTEXT (프로젝트 헌법)
- [00_GOALS.md](01_PROJECT_CONTEXT/00_GOALS.md) - 프로젝트 목표
- [01_CONVENTIONS.md](01_PROJECT_CONTEXT/01_CONVENTIONS.md) - 코딩 규칙 + **Boundaries** ⭐

### 02_REQUIREMENTS (요구사항)
- [capabilities/](02_REQUIREMENTS/capabilities/) - 기능 **결정** (REQ-*)
- [invariants/](02_REQUIREMENTS/invariants/) - 불변 규칙 **결정** (RULE-*)
- [competencies/](02_REQUIREMENTS/competencies/) - 역량 질문 **검증** (CQ-*)
- [discussions/](02_REQUIREMENTS/discussions/) - 조율 기록 (DISC-*)

### 03_TECH_SPECS (기술 설계)
- [architecture/](03_TECH_SPECS/architecture/) - 구조도, DB 스키마
- [api_specs/](03_TECH_SPECS/api_specs/) - API 명세
- [decisions/](03_TECH_SPECS/decisions/) - ADR (RATIONALE)

### 04_TASK_LOGS (작업 기록)
- [active/](04_TASK_LOGS/active/) - 실행 중 (RUN-*) + **Self-Check**
- [archive/](04_TASK_LOGS/archive/) - 완료된 작업

### 98_KNOWLEDGE (지식 저장소)
- [troubleshooting/](98_KNOWLEDGE/troubleshooting/) - 해결된 난제들
