# [BRIEF-MCP-002] Request: 
📘 MCP 실행/아카이브 구조 전환 방향성 계획서

## 핵심 요청
아카이브 폐지 + G...

> **ID**: BRIEF-MCP-002
> **Date**: 2026-01-24
> **Status**: Active
> **Template-Version**: 3.4

## 1. User Request (원본 요청)
> 
📘 MCP 실행/아카이브 구조 전환 방향성 계획서

## 핵심 요청
아카이브 폐지 + Git 중심 운영으로 전환

## 주요 변경사항
1. RUN 문서는 모두 active에 유지 (이동 없음)
2. 완료/실패 여부는 Status 메타데이터로만 표현
3. 변경 증거(Evidence)는 Git 커밋 기준으로 관리
4. finalize_run() 의존 제거

## 영향 범위
- finalize_run() 함수 수정/제거
- 00_INDEX.md, GETTING_STARTED.md 등 템플릿 업데이트
- 04_TASK_LOGS/archive 폴더 역할 변경
- RUN 문서 메타데이터 표준 변경 (Summary, Git, Status 필수)

## 검증 기준
- RUN 이동 없이 Status만으로 완료 판단 가능
- Git 커밋 해시가 Evidence로 기록됨
- active/README.md 대시보드 자동 생성


## 2. Intent Summary (의도 요약)

- **주요 목표**: RUN 아카이브 이동 제거 → Status 메타데이터 + Git 커밋 기반 완료 관리
- **해결할 문제**:
  - finalize_run() 아카이브 이동 실패 문제
  - 아카이브 폴더의 실질적 미사용 (Git이 이미 증거 역할)
  - 완료 판단 기준 불명확
- **접근 방식**: 역할 분리 - 증거(Git) / 맥락(RUN) / 가독성(View)

## 3. Affected Artifacts (영향받는 문서)

- **Modify**: [REQ-MCP-002](02_REQUIREMENTS/capabilities/REQ-MCP-002.md)
- **Read**: [아카이브 폐지계획](.memory/02_REQUIREMENTS/discussions/아카이브 폐지계획.md)

## 4. Proposed Changes (변경 제안)

### Phase 1: finalize_run() 수정
1. `finalize_run()` - RUN 이동 로직 제거
2. `finalize_run()` - Status 업데이트 + Git Evidence 기록만 수행
3. RUN 템플릿에 필수 메타데이터 추가: Summary, Git, Status

### Phase 2: 템플릿 업데이트
4. `00_INDEX.md` - "Archive 이동" 설명 제거, Status 기반 완료 설명
5. `GETTING_STARTED.md` - 워크플로우 업데이트
6. `04_TASK_LOGS/active/README.md` - 대시보드 형식으로 개편

### Phase 3: View 기능
7. CLI `--runs` 명령 - 상태별 필터링 추가
8. active/README.md 자동 갱신 로직

## 5. Verification Criteria (검증 기준)

- [ ] finalize_run() 호출 시 RUN 이동 없이 Status만 업데이트됨
- [ ] RUN 문서에 Git 커밋 해시가 Evidence로 기록됨
- [ ] 04_TASK_LOGS/archive 폴더로 이동하는 코드 없음
- [ ] 템플릿(00_INDEX.md, GETTING_STARTED.md)에서 "Archive 이동" 설명 제거됨
- [ ] `--runs` 명령으로 상태별 필터링 가능
