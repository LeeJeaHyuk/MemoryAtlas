# [REQ-AUTO-001] Workflow Automation v2.0

> **ID**: REQ-AUTO-001
> **Domain**: AUTO
> **Status**: Active
> **Last Updated**: 2026-01-24
> **Must-Read**: CQ-CORE-001, CQ-CORE-002, CQ-CORE-003
> **Template-Version**: 3.4

---

## Decision
Implement a 3-step automation pipeline (`intake` -> `plan` -> `finish`) that enforces the "Authority-Based" workflow.
All state changes must be reflected in `01_PROJECT_BOARD.md`.

## Functions

### 1. `intake(description: str | list[str])`
- **Input**: User description string OR list of file paths in `00_INBOX`.
- **Logic**:
    1.  Create a `BRIEF` document in `02_REQUIREMENTS/discussions/briefs/`.
    2.  Read `01_PROJECT_BOARD.md`.
    3.  Append the new Brief ID and Summary to the `## Queue (Intake)` section.
    4.  Save `01_PROJECT_BOARD.md`.
- **Output**: Path to the created `BRIEF`.

### 2. `plan(brief_id: str)`
- **Input**: A valid `BRIEF` ID (e.g., `BRIEF-GEN-005`).
- **Logic**:
    1.  Validate that the Brief exists.
    2.  Create a `RUN` document in `04_TASK_LOGS/active/`.
    3.  Read `01_PROJECT_BOARD.md`.
    4.  **Move** the item from `## Queue` to `## Active`.
    5.  Save `01_PROJECT_BOARD.md`.
- **Output**: Path to the created `RUN`.

### 3. `finish(run_id: str)`
- **Input**: A valid `RUN` ID (e.g., `RUN-BRIEF-GEN-005-step-01`).
- **Logic**:
    1.  Validate that the RUN exists.
    2.  Run `doctor` (validation check).
    3.  If successful:
        a. Move the `RUN` file to `04_TASK_LOGS/archive/Legacy/` (or strictly `archive/YYYY-MM/` if implemented). *v2.0 simplified: move to `archive/`.*
        b. Read `01_PROJECT_BOARD.md`.
        c. **Move** the item from `## Active` to `## Completed`.
        d. Save `01_PROJECT_BOARD.md`.
- **Output**: Archives path.

## Acceptance Criteria
- [ ] `intake` adds item to Queue.
- [ ] `plan` moves item from Queue to Active.
- [ ] `finish` moves item from Active to Completed AND moves file to archive.
- [ ] Operations are idempotent (safe to run multiple times).
