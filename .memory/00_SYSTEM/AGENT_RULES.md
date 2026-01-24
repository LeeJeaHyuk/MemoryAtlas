# MemoryAtlas Agent Rules (v3.4.1) - Smart Spec Edition

> **SYSTEM FILE**: Managed by `memory_manager.py`. DO NOT EDIT.
> **For custom rules**: Use `01_PROJECT_CONTEXT/01_CONVENTIONS.md`.

---

## 1. Smart Spec Model

```
6 Core Sections in CONVENTIONS:
  1. Commands: Test, Lint, Run 명령어
  2. Project Structure: 디렉토리 구조
  3. Code Style: 포맷팅, 네이밍 규칙
  4. Testing Strategy: 테스트 요구사항
  5. Git Workflow: 브랜치/커밋 규칙
  6. Boundaries: Always / Ask First / Never 규칙

Boundaries (STRICT):
  ✅ Always: AI가 항상 수행해야 하는 행동
  ⚠️ Ask First: 사람 승인 후 진행
  🚫 Never: AI가 절대 수행하면 안 되는 행동
```

---

## 2. Authority Model

```
권위의 흐름 (Authority Flow):
  REQ (Authority) → TECH_SPEC → CODE → RUN/LOG

문서 등급:
  - DECISION: 최종 결정 (REQ-*, RULE-*) - MUST READ
  - DISCUSSION: 조율 기록 (DISC-*) - DEFAULT SKIP
  - RATIONALE: 결정 근거 (ADR-*) - READ IF REFERENCED
  - EXECUTION: 작업 단위 (RUN-*) - CREATE/UPDATE
```

---

## 3. Reading Priority

### P0 (Always Read)
1. `01_PROJECT_CONTEXT/01_CONVENTIONS.md` - **특히 Boundaries 섹션**
2. Target REQ's `**Must-Read**` field
3. All referenced RULE-* documents

### P1 (Read for Context)
- `02_REQUIREMENTS/invariants/` (all active)
- `02_REQUIREMENTS/competencies/` (referenced CQs only)
- Referenced ADR-* documents

### Default Skip
- `02_REQUIREMENTS/discussions/` - Only when explicitly referenced
- `04_TASK_LOGS/archive/` - Only for historical context
- `99_ARCHIVE/` - Deprecated content

---

## 4. Boundaries Compliance (STRICT)

### ✅ Always (항상 수행)
- RUN 문서 종료 전 **테스트 통과** 확인
- 모든 퍼블릭 함수에 **Type Hint** 추가
- 기존 코드 수정 시 **기존 테스트 통과** 확인
- 새 기능 추가 시 **REQ 문서 참조** 확인

### ⚠️ Ask First (사전 승인 필요)
- `requirements.txt` 등 **의존성 추가/삭제**
- `.memory/00_SYSTEM/` 내부 파일 수정
- **DB 스키마 변경** (migration 등)
- **API 엔드포인트 삭제/변경**
- 설정 파일 구조 변경

### 🚫 Never (절대 금지)
- **Secret 커밋 금지**: API Key, Password, Token 등
- **하드코딩 금지**: 프로덕션 데이터, mock 데이터
- **물리적 삭제 금지**: Soft Delete 사용
- **Force Push 금지**: main/master 브랜치
- **테스트 스킵 금지**: @skip으로 무시하지 않음

---

## 5. Writing Rules

### REQ/RULE Documents (Authority)
- **결정만 적는다**: 논의/대안은 discussions/에
- **짧게 유지**: 한 REQ = 하나의 명확한 결정
- **Must-Read 필수**: RULE/ADR ID만, 링크 텍스트는 ID
- **Constraints 선택적**: 기능별 추가 제약 시만 작성

### RUN Documents (Execution)
- **1 RUN = 1 목적**: 여러 목적을 섞지 않음
- **Input 명시**: 읽어야 할 문서 ID 목록
- **Verification 명시**: 성공 조건 + Self-Check
- **Output 기록**: 생성/수정 파일 목록

---

## 6. Validation Requirements

### Three-Way ID Consistency
- `**ID**:` metadata (Authority)
- Filename
- Header `[ID]`

All three must match.

### Must-Read Validation
- Must-Read allows only RULE/ADR IDs (CTX is P0 and excluded)
- Link text must be the ID if markdown links are used
- All documents in `**Must-Read**` must exist

---

## 7. 3-Step Workflow (Intake → Plan → Finish)

### MCP 도구 (핵심)

| 트리거 | MCP 도구 | 결과 |
|--------|----------|------|
| "intake 해줘" | `intake(description)` | BRIEF 생성 |
| "plan 만들어" | `plan(brief_id)` | RUN 생성 |
| "작업 완료" | `finish(run_id, git_hash)` | Status 완료 |

### Step 1: Intake
- 사용자가 "~해줘", "intake 해줘" 요청 시
- `intake("요청 내용")` 호출 → BRIEF 생성
- BRIEF 검토 요청

### Step 2: Plan
- 사용자가 "plan 만들어", "계획 확정" 요청 시
- `plan("BRIEF-ID")` 호출 → RUN 생성
- RUN 검토 요청

### Step 3: Finish
- 구현 완료 후
- Git 커밋 생성
- `finish("RUN-ID", git_hash="...")` 호출
- RUN은 active/에 유지 (Archive 이동 없음)

### Self-Check (완료 전 필수)
- [ ] **Test**: 테스트 통과?
- [ ] **Boundary**: CONVENTIONS Boundaries 준수?
- [ ] **Spec**: REQ/BRIEF와 일치?

### When Discussion Needed
1. Create DISC-* in `02_REQUIREMENTS/discussions/`
2. Reference from REQ's `Related` section
3. Update REQ with final decision

---

## 8. 하위 호환 별칭

- `plan_from_brief()` → `plan()` (v3.4 이전 호환)
- `finalize_run()` → `finish()` (v3.4 이전 호환)
