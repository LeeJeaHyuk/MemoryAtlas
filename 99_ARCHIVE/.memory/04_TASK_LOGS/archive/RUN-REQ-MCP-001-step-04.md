# [RUN-REQ-MCP-001-step-04] Phase 3: Automation Logic (automation.py)

> **ID**: RUN-REQ-MCP-001-step-04
> **Input**: src/core/automation.py
> **Verification**: `intake()` creates BRIEF-GEN-001, `plan_from_brief()` creates RUN from BRIEF.
> **Last Updated**: 2026-01-23

---

## 1. Objective

Implement the core automation logic for the new Brief-driven workflow in `src/core/automation.py`. This enables the "Intake -> Brief -> Plan -> RUN" pipeline.

## 2. Requirements

### A. New Methods
1.  `intake(description: str) -> Path`:
    - Generate a `BRIEF-[DOMAIN]-[NNN].md` file in `BRIEF_SCAN_DIRS`.
    - ID generation: increment generic counter or parse implicit domain.
    - Content: Fill template with `description` as "User Request".
2.  `plan_from_brief(brief_id: str) -> Path`:
    - Read `BRIEF-XXX-NNN`.
    - Create `RUN-REQ-[DOMAIN]-[NNN]-step-01.md`.
    - Link RUN to BRIEF (Input field).

### B. Updates
1.  `apply_req()`: Add generic deprecation warning (or soft deprecation).
2.  `finalize_run()`: Ensure it can handle RUNs driven by Briefs (not just REQs).
    - Current logic mostly generic, but ensure `Objective`/`Scope` extraction works if format varies.

## 3. Scope

### In Scope
- `src/core/automation.py`

### Out of Scope
- Modifying `memory_manager.py` (CLI commands) - this is Phase 4.

## 4. Verification
- [x] Manual script `test_automation.py` verified:
    - `intake("Test...")` -> Created `BRIEF-TEST-001`.
    - `plan_from_brief("BRIEF-TEST-001")` -> Created `RUN-BRIEF-TEST-001-step-01`.
- [x] `apply_req` deprecation warning added.

## 5. Evidence
- Test output showing successful creation of BRIEF and RUN files using the new automation logic.

## Output
- `src/core/automation.py` updated with `intake` and `plan_from_brief`.

