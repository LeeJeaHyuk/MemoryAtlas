# [RULE-SYS-005] SSOT Addition Scope Limit

> **ID**: RULE-SYS-005
> **Domain**: SYS
> **Priority**: Medium
> **Last Updated**: 2026-02-06
> **Must-Read**: RULE-SYS-002

---

## Rule Statement
- SSOT 신규 작성/보강은 **검증 가능(Verifiable)** 하고 **불변 제약(Invariant Constraint)** 인 내용만 허용한다.
- 설명, 배경, 맥락은 View에 작성하고 SSOT에는 포함하지 않는다.
- SSOT는 작고(Small), 참조 가능(Referencable), 검토 가능(Reviewable)해야 한다.

## Scope
- REQ, RULE, ADR 문서 신규 작성 및 수정 시.

## Violation
- SSOT에 설명/배경/맥락을 장황하게 작성하는 경우.
- 검증 불가능한 주관적 내용을 SSOT에 포함하는 경우.
- 변경 가능한 구현 세부사항을 SSOT에 고정하는 경우.

## Examples

### Correct (검증 가능/불변 제약)
- "sync 명령어는 dry-run이 기본이다." (검증 가능)
- "REQ 문서는 자동 수정하지 않고 Patch만 생성한다." (불변 제약)

### Incorrect (SSOT에 부적합)
- "sync 명령어가 유용한 이유는..." (설명/배경)
- "나중에 기능이 추가될 수 있다." (변경 가능)
- "사용자 경험이 좋아야 한다." (검증 불가)
