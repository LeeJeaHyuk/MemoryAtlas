# [RUN-REQ-MCP-001-step-07] Phase 6: Checklist & Validation

> **ID**: RUN-REQ-MCP-001-step-07
> **Input**: All modules
> **Verification**: Full E2E test of the new workflow and regression test of existing checks.
> **Last Updated**: 2026-01-23

---

## 1. Objective

Perform a comprehensive End-to-End (E2E) test of the "Intake -> Brief -> Plan -> Execution -> Finalize" workflow, and ensure existing "Doctor" checks remain valid.

## 2. Requirements

### A. E2E Test Scenario
1.  **Intake**: Call `intake("Phase 6 E2E Test")` via MCP tool.
    - Expect: `BRIEF-GEN-XXX.md` created.
2.  **Plan**: Call `plan_from_brief("BRIEF-GEN-XXX")` via MCP tool.
    - Expect: `RUN-BRIEF-GEN-XXX-step-01.md` created.
3.  **Execute**: Manually simulate "work done" (no-op).
4.  **Finalize**: Call `finalize_run("RUN-BRIEF-GEN-XXX-step-01")` via MCP tool.
    - Expect: RUN moved to archive, status updated.

### B. Regression Checks
1.  Run `memory_manager.py --doctor`.
    - Expect: All 7 checks pass (Structure, Metadata, Link, Req, Run, Disc, Brief).
2.  Check for `apply_req` deprecation warning.

## 3. Scope

### In Scope
- Verification script (`test_e2e.py`).
- Manual verification of artifacts.

### Out of Scope
- Code changes (unless bugs are found).

## 4. Verification
- [x] `test_e2e.py` passed:
    - Intake: `BRIEF-TEST-001` created.
    - Plan: `RUN-BRIEF-TEST-001-step-01` created.
    - Finalize: `RUN-BRIEF-TEST-001-step-01` archived, status COMPLETED.
    - `apply_req` deprecation warning verified.
- [x] `python memory_manager.py --doctor` passed (existing unrelated warnings ignored).

## 5. Evidence
- E2E script output confirmed creation and transition of Brief -> RUN -> Archive.
- `--doctor` output confirms system integrity.

## Output
- Verified system state.

