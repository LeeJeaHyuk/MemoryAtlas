# [BRIEF-DOC-001] Request: 
config.py의 DOC_TEMPLATES가 README의 원칙과 불일치함.
1. 00...

> **ID**: BRIEF-DOC-001
> **Date**: 2026-01-23
> **Status**: Active
> **Template-Version**: 3.3

## 1. User Request (원본 요청)
> 
config.py의 DOC_TEMPLATES가 README의 원칙과 불일치함.
1. 00_INDEX.md: 3-Phase Workflow (Intake->Plan->Execute) 추가.
2. 01_CONVENTIONS.md: Execution Checklist를 3-Phase Workflow로 수정.
3. 04_AGENT_GUIDE.md: 구식 참조(02_SERVICES) 제거 및 최신 Workflow 반영.
4. 04_TASK_LOGS/active/README.md: 깨진 한글 수정, Input에 BRIEF 참조 추가.
5. 02_REQUIREMENTS/discussions/briefs/README.md: 신규 템플릿 추가 필요.


## 2. Intent Summary (의도 요약)
> ⚠️ **LLM 작업**: 아래 원본 요청의 핵심 의도를 분석하세요.

- **주요 목표**: `src/core/config.py` 내 `DOC_TEMPLATES`를 최신 README 원칙(3-Phase Workflow) 및 구조에 맞게 동기화.
- **해결할 문제**: 생성되는 문서 템플릿이 실제 가이드라인과 달라 사용자/AI 혼란 유발.
- **CQ 형식 입력 허용**: 정리 안 된 생각/메모도 가능

## 3. Affected Artifacts (영향받는 문서)
> ⚠️ **반드시 구체적인 경로/링크로 작성** (REQ-XXX 금지)  
> 예: `02_REQUIREMENTS/capabilities/REQ-AUTH-001.md`

- **Create**: 02_REQUIREMENTS/capabilities/REQ-DOC-002.md

## 4. Proposed Changes (변경 제안)
> ⚠️ **LLM 작업**: 구체적인 변경사항을 나열하세요.

1. **00_INDEX.md 템플릿 수정**: 3-Phase Workflow (Intake -> Plan -> Execute) 섹션 추가.
2. **01_CONVENTIONS.md 템플릿 수정**: Execution Checklist를 3-Phase Workflow에 맞게 갱신 (Intake, Plan 단계 명시).
3. **04_AGENT_GUIDE.md 템플릿 수정**: `02_SERVICES` 등 구식 참조 제거, 문서 표준 최신화.
4. **04_TASK_LOGS/active/README.md 템플릿 수정**: 깨진 한글 수정, Input 필드 예시에 BRIEF 추가.
5. **Briefs README 추가**: `DOC_TEMPLATES`에 `02_REQUIREMENTS/discussions/briefs/README.md` 키와 템플릿 내용 추가.

## 5. Verification Criteria (검증 기준)
> ⚠️ **LLM 작업**: 검증 가능한 구체적 조건을 작성하세요.

- [ ] `src/core/config.py` 수정 후 Python 문법 오류 없음.
- [ ] `DOC_TEMPLATES`의 각 항목이 요구사항대로 변경되었는지 코드 레벨 확인.
- [ ] `00_INDEX.md`에 "3-Phase Workflow" 문자열 존재 확인.
- [ ] `01_CONVENTIONS.md`에 "Intake" 체크리스트 항목 존재 확인.
- [ ] `briefs/README.md` 템플릿 추가 확인.
