# [REQ-VER-001] 버전 업데이트 감지 및 변경사항 알림

> **ID**: REQ-VER-001
> **Domain**: VER
> **Status**: Implemented
> **Last Updated**: 2026-01-26
> **Answers**: [CQ-VER-001](../cq/CQ-VER-001.md)
> **Must-Read**: None

---

## Decision

### 1. 버전 감지 메커니즘
`atlas.py` 실행 시 다음 두 버전을 비교하여 업데이트 여부를 판단한다:
- **실행 버전 (`ATLAS_VERSION`)**: 실행 중인 `atlas.py` 코드 내에 정의된 상수 버전
- **설치 버전 (`.atlas/.system/VERSION`)**: 사용자 환경에 설치된 `.atlas` 시스템의 버전 파일 내용

### 2. 업데이트 시 동작
- **감지 조건**: `ATLAS_VERSION`이 `installation version`보다 높은 경우 (`>`)
- **알림**: 사용자에게 버전 업그레이드 사실을 알림 (예: `Upgrading Atlas: 0.1.0 -> 0.2.0`)
- **변경사항 출력**: `atlas.py` 내에 포함된 `CHANGELOG` 데이터를 참조하여, 업데이트 구간에 해당하는 변경 내역을 출력
- **상태 갱신**: `.atlas/.system/VERSION` 파일을 새로운 버전으로 덮어씀

### 3. Changelog 관리
- `atlas.py` 내부에 `CHANGELOG` 딕셔너리 상수를 두어 관리
- Key: 버전 문자열 (예: "0.2.0")
- Value: 변경사항 리스트 (예: `["Feature: ...", "Fix: ..."]`)

---

## Input
- `.atlas/.system/VERSION` (파일)
- `atlas.py` (내부 상수 `ATLAS_VERSION`, `CHANGELOG`)

## Output
- **Console**: 버전 업데이트 알림 및 변경사항 로그
- **File**: `.atlas/.system/VERSION` (최신 버전으로 갱신됨)

---

## Acceptance Criteria
- [x] 실행 시 현재 설치된 버전이 없거나, 실행 버전보다 낮을 경우 업데이트 루틴이 동작한다.
- [x] 업데이트 시 "Upgrading Atlas: X -> Y" 메시지가 출력된다.
- [x] 업데이트된 버전 범위에 해당하는 모든 Changelog 내역이 출력된다.
- [x] Changelog 출력 후 `.atlas/.system/VERSION` 파일이 최신 버전으로 업데이트된다.
- [x] 이미 최신 버전인 경우 업데이트 메시지나 변경사항이 출력되지 않는다.

---

## Traceability
- **Answers**: [CQ-VER-001](../cq/CQ-VER-001.md)
