# [RUN-REQ-MCP-001-step-08] Fix Brief Directory Mismatch

> **ID**: RUN-REQ-MCP-001-step-08
> **Input**: src/core/config.py, src/core/automation.py, src/core/checks.py
> **Verification**: `test_e2e.py` creates Brief in `02_REQUIREMENTS/discussions/briefs/`.
> **Last Updated**: 2026-01-23

---

## 1. Objective

Align implementation with authority documents (`REQ-MCP-001`). Move `Brief` document location from `04_TASK_LOGS/active` to `02_REQUIREMENTS/discussions/briefs`.

## 2. Requirements

### A. Config Update
1.  Add `02_REQUIREMENTS/discussions/briefs` to directory structure.
2.  Update `BRIEF_SCAN_DIRS` to point to the new location.

### B. Automation Update
1.  Update `Automator.intake` to save Briefs to `02_REQUIREMENTS/discussions/briefs`.
2.  Update `Automator.plan_from_brief` and `_generate_brief_id` to read from the new location.

## 3. Scope

### In Scope
- `src/core/config.py`
- `src/core/automation.py`
- `src/core/checks.py` (if scan dirs are used)

### Out of Scope
- Modifying `REQ-MCP-001` (Authority document is correct).

## 4. Verification
- Manual verification script `test_brief_location.py`.
- `memory_manager.py --doctor` check.

## 5. Output
- Implementation aligned with REQ.
