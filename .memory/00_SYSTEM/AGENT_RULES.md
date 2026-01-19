# MemoryAtlas Agent Rules (v2.2.1)

> **SYSTEM FILE**: Managed by `memory_manager.py`. DO NOT EDIT.
> **For custom rules**: Use `01_PROJECT_CONTEXT/01_CONVENTIONS.md`.

---

## 1. Authority Model

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

## 2. Reading Priority

### P0 (Always Read)
1. `01_PROJECT_CONTEXT/01_CONVENTIONS.md`
2. Target REQ's `**Must-Read**` field
3. All referenced RULE-* documents

### P1 (Read for Context)
- `02_REQUIREMENTS/business_rules/` (all active)
- Referenced ADR-* documents

### Default Skip
- `02_REQUIREMENTS/discussions/` - Only when explicitly referenced
- `04_TASK_LOGS/archive/` - Only for historical context
- `99_ARCHIVE/` - Deprecated content

---

## 3. Writing Rules

### REQ/RULE Documents (Authority)
- **결정만 적는다**: 논의/대안은 discussions/에
- **짧게 유지**: 한 REQ = 하나의 명확한 결정
- **Must-Read ??**: RULE/ADR ID?, ?? ???? ID

### RUN Documents (Execution)
- **1 RUN = 1 목적**: 여러 목적을 섞지 않음
- **Input 명시**: 읽어야 할 문서 ID 목록
- **Verification 명시**: 성공 조건
- **Output 기록**: 생성/수정 파일 목록

---

## 4. Validation Requirements

### Three-Way ID Consistency
- `**ID**:` metadata (Authority)
- Filename
- Header `[ID]`

All three must match.

### Must-Read Validation
- Must-Read allows only RULE/ADR IDs (CTX is P0 and excluded)
- Link text must be the ID if markdown links are used
- All documents in `**Must-Read**` must exist
- All must be read before implementation

---

## 5. Workflow

### Starting a Task
1. Read P0 documents
2. Read target REQ and its Must-Read
3. Create RUN-* document in `04_TASK_LOGS/active/`
4. Implement in small steps

### Completing a Step
1. Mark RUN as Done
2. Move to `04_TASK_LOGS/archive/YYYY-MM/`
3. Create next step if needed

### When Discussion Needed
1. Create DISC-* in `02_REQUIREMENTS/discussions/`
2. Reference from REQ's `Related` section
3. Update REQ with final decision
