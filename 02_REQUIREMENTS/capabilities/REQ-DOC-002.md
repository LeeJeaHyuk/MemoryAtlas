# [REQ-DOC-002] Template Sync with 3-Phase Workflow

> **ID**: REQ-DOC-002
> **Domain**: DOC
> **Status**: Active
> **Last Updated**: 2026-01-23
> **Must-Read**: RULE-ID-001, RULE-META-001
> **Template-Version**: 3.3

---

## Decision (최종 결정)

`config.py`의 `DOC_TEMPLATES`를 수정하여 시스템이 생성하는 문서 템플릿이 최신 워크플로우(Intake -> Plan -> Execute)와 일치하도록 한다.

## Input

- **Requests**: 
  - 3-Phase Workflow 명시 (00_INDEX)
  - Execution Checklist 갱신 (01_CONVENTIONS)
  - 구식 문서 참조 제거 (04_AGENT_GUIDE)
  - 템플릿 오류 수정 (04_TASK_LOGS/active/README)
  - Briefs README 추가

## Output

- 수정된 `src/core/config.py`
  - `DOC_TEMPLATES` 딕셔너리 업데이트

## Acceptance Criteria

- [ ] `00_INDEX.md` 템플릿에 "3-Phase Workflow" 섹션이 존재해야 한다.
- [ ] `01_CONVENTIONS.md` 템플릿의 체크리스트가 Intake/Plan 단계를 포함해야 한다.
- [ ] `04_AGENT_GUIDE.md` 템플릿에서 `02_SERVICES` 참조가 사라져야 한다.
- [ ] `04_TASK_LOGS/active/README.md` 템플릿의 한글 깨짐(???)이 수정되어야 한다.
- [ ] `02_REQUIREMENTS/discussions/briefs/README.md` 템플릿이 신규 추가되어야 한다.

## In/Out of Scope (Optional)

### In Scope
- `config.py` 내의 템플릿 문자열 수정

### Out of Scope
- 기존에 생성된 문서 파일 수정 (새로 생성될 문서에만 적용됨)
