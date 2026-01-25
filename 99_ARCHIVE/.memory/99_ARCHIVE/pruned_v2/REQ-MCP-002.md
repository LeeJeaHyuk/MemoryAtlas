# [REQ-MCP-002] Archive 폐지 및 Git 중심 운영 전환

> **ID**: REQ-MCP-002
> **Last Updated**: 2026-01-24
> **Status**: Active
> **Created**: 2026-01-24
> **Template-Version**: 3.4

## Summary
RUN 아카이브 이동 로직을 제거하고 Status 메타데이터 + Git 커밋 기반으로 완료 상태를 관리한다.

## Input
- BRIEF-MCP-002 (아카이브 폐지 계획)
- 기존 finalize_run() 함수

## Output
- 수정된 finalize_run() 함수 (이동 로직 제거)
- 업데이트된 템플릿 (00_INDEX.md, GETTING_STARTED.md)
- RUN 대시보드 (04_TASK_LOGS/active/README.md)

## Acceptance Criteria
- [ ] finalize_run() 호출 시 RUN 이동 없이 Status만 업데이트됨
- [ ] RUN 문서에 Git 커밋 해시가 Evidence로 기록됨
- [ ] 템플릿에서 "Archive 이동" 설명이 제거됨
- [ ] --runs 명령으로 상태별 필터링 가능

## Must-Read
- `.memory/02_REQUIREMENTS/discussions/아카이브 폐지계획.md`
- `src/core/automation.py` (finalize_run 함수)