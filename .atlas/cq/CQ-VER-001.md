# [CQ-VER-001] 버전 업데이트 감지 및 변경사항 알림

> **ID**: CQ-VER-001
> **Domain**: VER
> **Status**: Draft
> **Last Updated**: 2026-01-26

---

## Question
- `atlas.py`가 실행되었을 때, 버전이 변경(업데이트)되었다면 이를 감지하고 **변경사항(Changelog)을 참조하여** 추가된 기능을 항상 출력할 수 있는가?

## Expected Answer (Criteria)
1. 실행 시 현재 설치된 버전(`.atlas/.system/VERSION`)과 실행되는 `atlas.py`의 내부 버전을 비교한다.
2. 버전이 변경된 경우(업데이트), 사용자에게 버전 변경 사실을 알린다 (예: `Upgrading Atlas: 0.1.0 -> 0.2.0`).
3. **업데이트된 버전의 변경사항(Changelog)을 참조하여** 추가되거나 변경된 주요 기능을 항상 출력한다.

## Traceability
- **Source**: User Request
- **Solved by**: [REQ-VER-001](../req/REQ-VER-001.md)
