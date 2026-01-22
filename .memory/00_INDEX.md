# Project Memory Index

> Entry point for Memory-Driven Development in this repo.
> **Version**: 3.3.0 (Smart Spec Edition)
> **Template Version**: 3.3

## Capabilities & Invariants Model (v3.0)

```
02_REQUIREMENTS/ 구조:
  capabilities/  - REQ-* (기능/행동) "시스템은 ~해야 한다"
  invariants/    - RULE-* (불변 규칙) "항상 ~이다 / ~는 금지"
  discussions/   - DISC-* (조율 기록) LLM 기본 무시

REQ vs RULE 판정:
  REQ  = Input/Output/Acceptance Criteria 필수 (동작 중심)
  RULE = Scope/Violation/Examples 필수 (불변 중심)
```

## Quick Navigation

| Folder | Purpose | Authority Level |
|--------|---------|-----------------|
| `01_PROJECT_CONTEXT/` | 프로젝트 헌법 + **Boundaries** | Constitution |
| `02_REQUIREMENTS/capabilities/` | 기능 **결정** (REQ-*) | Authority |
| `02_REQUIREMENTS/invariants/` | 불변 규칙 **결정** (RULE-*) | Authority |
| `02_REQUIREMENTS/discussions/` | 조율 기록 (DISC-*) | Reference |
| `03_TECH_SPECS/` | 기술 설계 & ADR | Implementation |
| `04_TASK_LOGS/` | 실행 기록 (RUN-*) | Execution |
| `98_KNOWLEDGE/` | 배운 점 | Asset |

## Start Here (For AI Agents)

### Reading Priority (P0 = Must Read)
1. **P0**: `01_PROJECT_CONTEXT/01_CONVENTIONS.md` - **특히 Boundaries 섹션** ⭐
2. **P0**: Target REQ's `**Must-Read**` field
3. **P1**: `02_REQUIREMENTS/invariants/` (all active)
4. **P2**: `98_KNOWLEDGE/` (if complex feature)

### Execution Checklist
1. [ ] CONVENTIONS의 **Boundaries** 확인
2. [ ] Target REQ 읽기
3. [ ] Must-Read 문서 읽기
4. [ ] RUN 문서 작성 (Self-Check 포함)
5. [ ] 구현 → 테스트 → 검증
6. [ ] Self-Check 통과 후 RUN 완료 처리

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
