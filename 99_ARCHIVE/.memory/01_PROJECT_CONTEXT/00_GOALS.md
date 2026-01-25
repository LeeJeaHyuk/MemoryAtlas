# Project Goals

> **ID**: CTX-GOALS-001
> **Last Updated**: 2026-01-20
> **Template-Version**: 2.4

---

## 1. Project Identity

### Name
MemoryAtlas

### One-Line Summary
LLM과 협업하며 프로젝트 문서-코드 일관성을 유지하는 메모리 기반 개발 시스템

### Core Value
프로젝트가 점점 커졌을 때 문서가 자동으로 정리되면서 해당 문서에 맞게 프로젝트가 구현되도록 유지하는 것. 누구나(사람/AI)가 문서를 읽고 즉시 프로젝트를 이해하고 일관된 구현을 유지할 수 있도록 한다.

---

## 2. Target Users

- **Primary**: 프로젝트를 Memory-Driven Development 방식으로 관리하고 싶은 개발자
- **Secondary**: AI 에이전트 (Claude, GPT 등)가 프로젝트 문서를 읽고 즉시 작업할 수 있도록

### Use Case
- 혼자 또는 팀으로 개발할 때, 프로젝트 규칙과 문서-코드 일관성을 자동으로 유지하고 싶을 때
- AI와 협업하며 일관된 품질의 코드를 생산하고 싶을 때
- 특정 User 또는 AI가 프로젝트에 바로 투입되어도 문서만 보고 전체 구조를 이해할 수 있어야 할 때

---

## 3. Success Criteria

- [x] 문서 구조가 체계적으로 관리되고 자동 검증이 가능함 (--doctor)
- [x] REQ/RULE/RUN 문서 간 참조 무결성이 보장됨
- [x] 단일 실행 파일 배포로 손쉬운 설치 (memory_manager.py)
- [ ] 프로젝트 문서와 코드 간 일관성 자동 검증
- [ ] 협업 시 문서-코드 동기화 자동화

---

## 4. Scope

### In-Scope
- Memory-Driven Development를 위한 문서 템플릿 관리
- REQ(요구사항), RULE(규칙), ADR(결정), RUN(실행) 문서의 검증 및 관리
- 문서 ID 3-way 일치성 검증 (파일명=헤더=메타데이터)
- 링크 무결성 검증 및 Must-Read 추적
- Context Bootstrapping (AI 기반 프로젝트 초기화)

### Out-of-Scope
- 코드 자동 생성 (AI가 문서를 보고 직접 생성)
- IDE 플러그인 (현재는 CLI 도구로만 제공)
- 실시간 문서-코드 동기화 (수동 검증 방식 유지)

---

## 5. Milestones

| Phase | Description | Target Date | Status |
|-------|-------------|-------------|--------|
| v2.0 | Memory-Driven Structure 확립 | 2024 Q4 | ✅ Done |
| v2.2 | Authority Model & Execution Unit | 2025 Q1 | ✅ Done |
| v2.3 | Smart Spec & Boundaries | 2025 Q2 | ✅ Done |
| v2.4 | Context Bootstrapping | 2026 Q1 | ✅ Done |
| v3.0 | 코드-문서 자동 동기화 | 2026 Q3 | 🔄 Planning |
