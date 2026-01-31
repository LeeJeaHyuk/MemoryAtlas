# [VIEW-SSOT] SSOT과 View의 관계

> **Refs**: RULE-SYS-002, RULE-SYS-003
> **Last Updated**: 2026-01-31

## Summary
- SSOT는 프로젝트의 권위 문서 집합이다. (@RULE-SYS-002#Rule-Statement) <!-- ATLAS:OK -->
- 변경이 생기면 SSOT가 먼저 바뀌고, 코드/테스트/뷰가 이를 따른다. (@RULE-SYS-002#Rule-Statement) <!-- ATLAS:OK -->
- VIEW는 SSOT를 특정 목적에 맞게 재구성한 읽기 레이어다. (@RULE-SYS-003#Rule-Statement) <!-- ATLAS:OK -->
- VIEW는 SSOT를 대체하지 않고, 근거는 SSOT 앵커로 연결된다. (@RULE-SYS-003#Rule-Statement) <!-- ATLAS:OK -->
- (설명/배경/예시: 규범 문장 금지) SSOT는 REQ/RULE/ADR로 구성되며 최소 단위로 관리된다.
  <!-- ATLAS:NOTE
  규범 키워드(MUST/SHOULD/MAY/반드시/해야/불가/금지/항상)가 들어가면 아래 형식의 근거 토큰이 필요:
  (@RULE-SYS-002#Rule-Statement)
  -->

## Notes
SSOT는 중복 없이 “무엇이 참이어야 하는가(REQ/RULE)”와 “왜 이렇게 하기로 했는가(ADR의 결정)”를 기록한다.

SSOT는 가능한 한 작게 쪼개진 최소 단위로 관리되어, 참조/검증/리뷰가 쉽다.

## References (SSOT index)
- RULE-SYS-002
- RULE-SYS-003
