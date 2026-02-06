# [VIEW-REQ-DIST-001] SSOT

> **Last Updated**: 2026-02-03
> **SSOT**: (@REQ-DIST-001) (@REQ-SYNC-001)

## Summary
- `.atlas/` 초기화 시 SSOT 문서를 보관하는 `req/`, `rule/`, `adr/` 디렉터리가 생성된다. (@REQ-DIST-001#Decision) <!-- ATLAS:OK -->
- `atlas sync`는 REQ 변경을 기본적으로 patch로 분리하며, REQ 직접 적용은 명시적 옵션에서만 수행된다. (@REQ-SYNC-001#Decision) <!-- ATLAS:OK -->
- 이 View는 SSOT의 저장 위치와 변경 경로만 요약하고, 상세 규칙은 각 REQ에 위임한다.
  <!-- ATLAS:NOTE
  규범 키워드(반드시/해야/불가/금지/항상)가 들어가면 아래 형식의 근거 토큰이 필요:
  (@REQ-XXX-001#<Section>)
  -->

## References (SSOT index)
- REQ-DIST-001
- REQ-SYNC-001
