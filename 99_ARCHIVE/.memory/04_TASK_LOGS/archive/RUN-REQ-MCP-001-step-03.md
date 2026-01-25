# [RUN-REQ-MCP-001-step-03] Phase 2: Verification Logic (checks.py)

> **ID**: RUN-REQ-MCP-001-step-03
> **Input**: REQ-MCP-001, src/core/checks.py
> **Verification**: `python memory_manager.py --doctor` passes with new validation logic.
> **Last Updated**: 2026-01-23

---

## 1. Objective

Implement `Brief` document validation logic in `src/core/checks.py` to support `BRIEF-XXX-001` document types as defined in Phase 1 config updates.

## 2. Requirements

### A. New Functions
- `check_briefs(root)`: Implement 3-way consistency check for Brief documents.
    - **ID**: metadata
    - Filename matches `BRIEF_ID_PATTERN`
    - Header matches `BRIEF_HEADER_RE`
    - Date field existence (from `HEADER_FIELDS_BY_TYPE`)

### B. Integration
- Update `extract_id_from_filename` to support `BRIEF_ID_PATTERN`.
- Update `get_doc_type` to identify `briefs`.
- Update `doctor` function to include Step [7/7] Brief Validation.
    - *Note*: Step number will increase from 6 to 7.

## 3. Scope

### In Scope
- `src/core/checks.py` modification.

### Out of Scope
- Creating actual `BRIEF` documents (this is verification logic only).

## 4. Verification
- [x] `check_briefs` detects missing IDs or mismatched filenames.
- [x] `doctor` runs all 7 steps.
- [x] `python memory_manager.py --doctor` returns success (0 issues if no briefs exist, currently passing Phase 2 checks).

## 5. Evidence
- Output of `--doctor` showing "[7/7] Brief Validation".
- `memory_manager.py` rebuilt successfully with restored functions.

## Output
- `src/core/checks.py` updated.
- `memory_manager.py` rebuilt.
