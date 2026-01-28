# [VIEW-REQ-VER-001] SSOT과 View의 관계

> **Last Updated**: 2026-01-28
> **SSOT**: (@REQ-VER-001) (@REQ-SYNC-001) (@REQ-DIST-001)

## Summary
- SSOT는 REQ/RULE/ADR로 구성되며 시스템 기준을 제공한다. (@REQ-VER-001#Decision) <!-- ATLAS:OK -->
- View는 SSOT를 사람이 이해하기 쉬운 문맥으로 설명한다. (@REQ-SYNC-001#Decision) <!-- ATLAS:OK -->
- View는 SSOT를 대체하지 않으며, 항상 SSOT 참조를 포함해야 한다. (@REQ-SYNC-001#Decision) <!-- ATLAS:OK -->
- 예: View는 구현 상세가 아니라 의도와 맥락을 요약한다.
  <!-- ATLAS:NOTE
  규범 키워드(반드시/해야/불가/금지/항상)가 들어가면 아래 형식의 근거 토큰이 필요:
  (@REQ-XXX-001#<Section>)
  -->

## References (SSOT index)
- REQ-DIST-001
- REQ-SYNC-001
- REQ-VER-001
