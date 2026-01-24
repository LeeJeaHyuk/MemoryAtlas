# [REQ-MCP-003] 3-Step Workflow 단순화

> **ID**: REQ-MCP-003
> **Last Updated**: 2026-01-24
> **Status**: Active
> **Created**: 2026-01-24
> **Template-Version**: 3.4

## Summary
MCP/수동 이중 경로를 단일 3-Step Workflow(Intake→Plan→Finish)로 통합하고 함수명을 직관적으로 변경한다.

## Input
- BRIEF-MCP-003 (3-Step Workflow 단순화 계획)
- 현재 automation.py (plan_from_brief, finalize_run)

## Output
- 리네이밍된 함수: plan(), finish()
- REQ 자동관리 로직
- 개편된 README.md

## Acceptance Criteria
- [ ] plan() 호출 시 REQ 자동 생성/갱신 + RUN 생성
- [ ] finish() 호출 시 Status 완료 + Git Evidence 기록
- [ ] 기존 함수명 별칭으로 동작 (하위호환)
- [ ] README.md에 3-Step Workflow 설명

## Must-Read
- `.memory/02_REQUIREMENTS/discussions/briefs/BRIEF-MCP-003.md`
- `src/core/automation.py`
