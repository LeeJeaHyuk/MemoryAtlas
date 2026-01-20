# Project Memory Index

> Entry point for Memory-Driven Development in this repo.
> **Version**: 2.4.0 (Smart Spec Edition)
> **Template Version**: 2.4

## Smart Spec Model (v2.3)

```
6 Core Sections in CONVENTIONS:
  1. Commands      - Test, Lint, Run 명령어
  2. Structure     - 프로젝트 디렉토리 구조
  3. Code Style    - 포맷팅, 네이밍 규칙
  4. Testing       - 테스트 전략
  5. Git Workflow  - 브랜치/커밋 규칙
  6. Boundaries    - Always / Ask First / Never 규칙 ⭐

Boundaries (STRICT):
  ✅ Always    - AI가 항상 수행해야 하는 행동
  ⚠️ Ask First - 사람 승인 후 진행
  🚫 Never     - AI가 절대 수행하면 안 되는 행동
```

## Quick Navigation

| Folder | Purpose | Authority Level |
|--------|---------|-----------------|
| `01_PROJECT_CONTEXT/` | 프로젝트 헌법 + **Boundaries** | Constitution |
| `02_REQUIREMENTS/features/` | 기능 **결정** (DECISION) | Authority |
| `02_REQUIREMENTS/business_rules/` | 규칙 **결정** (DECISION) | Authority |
| `02_REQUIREMENTS/discussions/` | 조율 기록 (DISCUSSION) | Reference |
| `03_TECH_SPECS/` | 기술 설계 & ADR | Implementation |
| `04_TASK_LOGS/` | 실행 기록 (RUN-*) | Execution |
| `98_KNOWLEDGE/` | 배운 점 | Asset |

## Start Here (For AI Agents)

### Reading Priority (P0 = Must Read)
1. **P0**: `01_PROJECT_CONTEXT/01_CONVENTIONS.md` - **특히 Boundaries 섹션** ⭐
2. **P0**: Target REQ's `**Must-Read**` field
3. **P1**: `02_REQUIREMENTS/business_rules/` (all active)
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
- [features/](02_REQUIREMENTS/features/) - 기능 **결정** (Authority)
- [business_rules/](02_REQUIREMENTS/business_rules/) - 규칙 **결정** (Authority)
- [discussions/](02_REQUIREMENTS/discussions/) - 조율 기록 (Reference)

### 03_TECH_SPECS (기술 설계)
- [architecture/](03_TECH_SPECS/architecture/) - 구조도, DB 스키마
- [api_specs/](03_TECH_SPECS/api_specs/) - API 명세
- [decisions/](03_TECH_SPECS/decisions/) - ADR (RATIONALE)

### 04_TASK_LOGS (작업 기록)
- [active/](04_TASK_LOGS/active/) - 실행 중 (RUN-*) + **Self-Check**
- [archive/](04_TASK_LOGS/archive/) - 완료된 작업

### 98_KNOWLEDGE (지식 저장소)
- [troubleshooting/](98_KNOWLEDGE/troubleshooting/) - 해결된 난제들
