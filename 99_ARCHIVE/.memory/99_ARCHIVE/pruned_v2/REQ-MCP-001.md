# [REQ-MCP-001] MCP Workflow Evolution (Intake-Plan-Execute)

> **ID**: REQ-MCP-001
> **Domain**: MCP
> **Status**: Active
> **Last Updated**: 2026-01-23
> **Must-Read**: RULE-ID-001, RULE-VALID-001, RULE-FLOW-002
> **Template-Version**: 5.0

---

## 1. Decision (결정 사항)

기존의 "Kick-off(즉시 실행)" 모델은 복잡한 프로젝트에서 맥락 소실(Context Loss)을 유발한다.
따라서 **Intake → Plan → Execute**의 3단계 워크플로우를 도입하고,
모든 변경 사항을 **Change Brief(변경 브리프)**라는 단일 스냅샷 문서로 관리한다.

이 변경을 통해 에이전트는 여러 문서를 뒤질 필요 없이 Brief와 RUN만 보고 작업을 수행할 수 있다.

---

## 2. New Workflow (3-Phase Model)

### Phase 1: Intake (요구 수집)
Intake includes creating the BRIEF document (not just collecting intent).
When a user asks for intake, you must call the MCP intake tool; if MCP is unavailable, inform the user and fix MCP first.


**목표**: 흩어진 요구사항과 논의를 하나의 Change Brief로 압축한다.

**입력**: 사용자 자연어, 기존 DISC, 채팅 로그.

**행동**:
1. 사용자 의도(Intent) 파악
2. 영향 받는 문서(REQ, RULE, ADR) 식별
3. `BRIEF-[DOMAIN]-[YYYYMMDD]-[SEQ].md` 작성

**산출물**: `02_REQUIREMENTS/discussions/briefs/BRIEF-*.md`
Affected Artifacts must use full paths or markdown links (e.g., 02_REQUIREMENTS/capabilities/REQ-*.md).

### Phase 2: Plan (계획 고정)
REQ location: `02_REQUIREMENTS/capabilities/REQ-*.md` (plan_from_brief creates/updates here).

**목표**: 확정된 Brief를 기반으로 **실행 단위(RUN)**를 고정한다.

**입력**: 확정된 Brief ID.

**행동**:
1. REQ 문서 생성/수정 (Draft → Active)
2. `04_TASK_LOGS/active/RUN-*.md` 생성
3. RUN 헤더에 Brief 링크 연결 (맥락 보존)

**산출물**: `RUN-*.md` (Status: Active)

### Phase 3: Execute (실행 및 종료)

**목표**: RUN 계획에 따라 구현하고, 검증 후 아카이브한다.

**입력**: "Run" 명령 (코드 구현은 에이전트 수행).

**행동**:
1. 에이전트가 코드를 구현
2. 구현 완료 시 `finalize_run` 자동 호출
3. `--doctor` 검증 후 아카이브 이동

**산출물**: `04_TASK_LOGS/archive/RUN-*.md`

---

## 3. MCP Functions (도구 정의)

### 🌟 Primary Tools (핵심 도구)

#### `intake(description, ref_docs=[])`

**역할**: [Phase 1] 자연어 요구사항을 받아 Change Brief를 생성합니다.

**Args**:
- `description`: 변경 요청 내용 요약
- `ref_docs`: 참고할 문서 ID 리스트 (선택)

**트리거**: "이거 바꾸고 싶어", "새 기능 제안", "Intake 시작해"

#### `plan_from_brief(brief_id)`

**역할**: [Phase 2] 승인된 Brief를 기반으로 RUN 문서를 생성하고 실행을 확정합니다.

**Args**: `brief_id` (Target Brief ID)
**Output**: run_id (use the returned run_id for finalize_run; do not construct IDs).

**트리거**: "브리프 승인", "계획 확정해", "이대로 진행시켜"

#### `finalize_run(run_id)`

**역할**: [Phase 3] 구현이 끝난 작업을 검증하고 종료합니다.

**Args**: `run_id`

**트리거**: "구현 완료", "Run 완료" (코딩 후 자동 호출)

### 🛠️ Auxiliary Tools (보조 도구)

- `validate(scope)`: 수동 검증 (lint/links/doctor)
- `req_status(req_id)`: 특정 REQ 상태 조회
- `create_disc_from_failure(context)`: 자동화 실패 시 분석 문서 생성

---

## 4. Artifact Specs (산출물 명세)

### A. Change Brief (`BRIEF-*.md`)

**위치**: `02_REQUIREMENTS/discussions/briefs/`

```markdown
# [BRIEF-CORE-20260123-01] Switch to 3-Phase Workflow

## 1. Intent Summary
MCP 워크플로우를 기존 2단계에서 Intake-Plan-Execute 3단계로 변경하여 맥락 유지를 강화함.

## 2. Affected Artifacts
- Modify: 02_REQUIREMENTS/capabilities/REQ-MCP-001.md
- Create: 02_REQUIREMENTS/invariants/RULE-FLOW-002.md

## 3. Proposed Changes
- `kick_off` 도구 삭제 및 `intake` 도구 신설
- `briefs` 폴더 구조 생성

## 4. Verification Criteria
- [ ] `intake` 호출 시 BRIEF 파일 생성 확인
- [ ] `plan_from_brief` 호출 시 RUN 파일 생성 확인
```

### B. RUN Document (`RUN-*.md`)

**위치**: `04_TASK_LOGS/active/`

**Must-Read**: 반드시 원본 `BRIEF-ID`를 링크해야 함.

- **Objective**: Brief의 Intent Summary를 복사
- **Verification**: Brief의 Criteria를 계승

---

## 5. Deprecated Functions (삭제 예정)

다음 함수들은 3-Phase 워크플로우 도입으로 더 이상 사용되지 않습니다:

- ~~`kick_off()`~~: `intake()` + `plan_from_brief()`로 대체
- ~~`apply_req()`~~: `plan_from_brief()`로 대체
- ~~`apply_req_full()`~~: `intake()` → `plan_from_brief()` → `finalize_run()` 시퀀스로 대체
- ~~`continue_req()`~~: `finalize_run()`으로 통합

---

## 6. Acceptance Criteria (완료 조건)

- [ ] **Intake**: `intake()` 함수가 `02_.../briefs/` 폴더에 올바른 포맷의 문서를 생성하는가?
- [ ] **Intake-Process**: Intake must run via MCP (intake tool); if MCP is unavailable, notify the user and fix MCP first.
- [ ] **Plan**: `plan_from_brief()`가 Brief의 내용을 읽어 RUN 문서를 생성하고, 관련 REQ를 업데이트하는가?
- [ ] **Execute**: `finalize_run()`이 `--doctor` 통과 시에만 아카이브로 이동하는가?
- [ ] **Env**: MCP server runs with a dedicated virtualenv (e.g., `.venv-mcp`) instead of base/system Python.
- [ ] **Deprecation**: 기존 `kick_off`, `apply_req` 함수가 제거되었는가?
- [ ] **Linking**: 생성된 RUN 문서가 원본 BRIEF 문서를 Must-Read로 참조하고 있는가?

---

## 7. Validation

```bash
# Phase 1: Intake
intake("워크플로우를 3단계로 변경하고 싶습니다", ref_docs=["REQ-MCP-001"])

# Phase 2: Plan (Brief 승인 후)
run_id = plan_from_brief("BRIEF-MCP-20260123-01")

# Phase 3: Execute (구현 완료 후)
finalize_run("<run_id returned by plan_from_brief>")

# 보조 검증
validate("lint")
validate("links")
validate("doctor")
```