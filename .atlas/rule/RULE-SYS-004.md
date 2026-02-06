# [RULE-SYS-004] RUN Document Structure

> **ID**: RULE-SYS-004
> **Domain**: SYS
> **Priority**: High
> **Last Updated**: 2026-02-06
> **Must-Read**: RULE-SYS-002

---

## Rule Statement
- RUN 문서는 SSOT(REQ/RULE/ADR)를 직접 참조해야 한다.
- RUN 내용은 **행동(Action), 검증(Verification), 산출물(Output)** 중심으로 작성한다.
- View만 참조하는 RUN은 검증 기준이 모호해지므로 금지한다.

## Scope
- `.atlas/runs/` 하위의 모든 RUN 문서.

## Violation
- RUN이 SSOT 없이 View만 참조하는 경우.
- RUN에 행동/검증/산출물 섹션이 누락된 경우.
- 검증 기준이 SSOT에 근거하지 않는 경우.

## Examples

### Correct
```markdown
## Steps
- [ ] REQ-SYNC-001 기반 sync 명령어 구현

## Verification
- [ ] REQ-SYNC-001#Acceptance-Criteria 충족 확인
```

### Incorrect
```markdown
## Steps
- [ ] sync 명령어 구현 (View 참조)

## Verification
- [ ] 잘 동작하는지 확인
```
