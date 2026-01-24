# 🚀 MemoryAtlas 시작하기

> **Version**: 3.4.1 | **Template**: 3.4
>
> 이 문서는 MemoryAtlas를 처음 사용하는 사용자를 위한 설정 가이드입니다.

## Quick Start

```bash
# 1. 온보딩 시작 (대화형 설정)
python memory_manager.py --guide

# 2. 출력된 프롬프트를 LLM에게 전달
# 3. LLM의 질문에 답하며 설정 완료
```

## 설정 체크리스트

### Phase 1: 프로젝트 기본 정보
- [ ] 프로젝트 이름 설정 <!-- id:phase1.project_name -->
- [ ] 프로젝트 목표 정의 (`01_PROJECT_CONTEXT/00_GOALS.md`) <!-- id:phase1.project_goal -->
- [ ] 기술 스택 결정 <!-- id:phase1.tech_stack -->

### Phase 2: 개발 규칙 설정
- [ ] 코딩 컨벤션 정의 (`01_PROJECT_CONTEXT/01_CONVENTIONS.md`) <!-- id:phase2.coding_style -->
- [ ] Boundaries 설정 (금지 사항) <!-- id:phase2.boundaries -->
- [ ] 테스트 정책 결정 <!-- id:phase2.testing_policy -->

### Phase 3: MCP 연동 (선택)
- [ ] MCP 서버 설정 확인 <!-- id:phase3.mcp_server -->
- [ ] 클라이언트 연동 테스트 <!-- id:phase3.mcp_client -->
- [ ] `intake()`, `plan_from_brief()`, `finalize_run()` 동작 확인 <!-- id:phase3.mcp_tools -->

## 설정 완료 후

설정이 완료되면 다음 명령어를 사용할 수 있습니다:

| 명령어 | 설명 |
|--------|------|
| `intake("요청")` | 아이디어 → BRIEF 생성 |
| `plan_from_brief("BRIEF-ID")` | BRIEF → RUN 생성 |
| `finalize_run("RUN-ID", git_hash="...")` | Status 완료 + Git 증거 기록 |

## 도움이 필요하면

- 📖 [README.md](../README.md) - 전체 시스템 이해
- 📋 [00_INDEX.md](00_INDEX.md) - 문서 네비게이션
- 🔧 `python memory_manager.py --doctor` - 시스템 검증

## 온보딩 상태

> **Status**: Not Started
> **Last Updated**: 2026-01-23

## 사용자 메모
<!-- NOTES:BEGIN -->
(자유롭게 기록)
<!-- NOTES:END -->
