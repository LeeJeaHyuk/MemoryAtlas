# [CQ-SYNC-001] 상태 추적 도구

> **ID**: CQ-SYNC-001
> **Domain**: SYNC
> **Status**: Draft
> **Last Updated**: 2026-01-26

---

## Question
- run 문서가 완료되었을 때, 관련된 brief/req 문서의 체크박스(x 표시)와 status를 어떻게 자동 동기화할 것인가?

## Expected Answer (Criteria)
1. run 문서 업데이트 시 완료된 항목에 자동으로 `[x]` 표시 생성
2. 해당 run 문서와 연결된 brief 문서의 체크박스/status 동기화
3. 해당 run 문서와 연결된 req 문서의 체크박스/status 동기화
4. status 필드가 존재하는 경우 상태값 자동 업데이트

> Note: 단일 파일 배포 요구사항은 [CQ-DIST-001](CQ-DIST-001.md)로 분리됨

## Traceability
- **Source**: [요구사항.md](../idea/요구사항.md)
- **Solved by**: [REQ-SYNC-001](../req/REQ-SYNC-001.md)
- **Constrained by**: (RULE 문서 작성 시 연결)
