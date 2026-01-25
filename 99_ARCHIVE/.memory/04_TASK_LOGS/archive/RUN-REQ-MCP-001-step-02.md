# [RUN-REQ-MCP-001-step-02] Phase 1: Core Configuration (config.py)

> **ID**: RUN-REQ-MCP-001-step-02
> **Input**: REQ-MCP-001
> **Verification**: `python memory_manager.py --doctor` passes with new config
> **Last Updated**: 2026-01-23

---

## 1. Objective

Update `src/core/config.py` to support `BRIEF` document type and update system versions. This is Phase 1 of the MCP validation logic updates.

## 2. Requirements

### A. Pattern Updates
- **BRIEF_ID_PATTERN**: `^BRIEF-([A-Z]+)-(\d{3})$`
- **BRIEF_HEADER_RE**: `^#{1,3}\s+\[(BRIEF-[A-Z]+-\d{3})\]`
- **BRIEF_SCAN_DIRS**: Define directory for BRIEF documents (if applicable, e.g., `01_PROJECT_CONTEXT/briefs` or check user intent. **Decision**: Add placeholder or existing scan dir if generic).
- **HEADER_FIELDS_BY_TYPE**: Add "briefs" entry (e.g., `["**ID**", "**Date**"]` or similar).

### B. Version Updates
- Update `CURRENT_VERSION` (target: check 3.3.1 or 3.4.0)
- Update `TEMPLATE_VERSION` (if templates change)

## 3. Plan

1.  **Modify `src/core/config.py`**:
    - Add regex patterns.
    - Update `HEADER_FIELDS_BY_TYPE`.
    - Update Versions.
2.  **Verify**:
    - Run `python memory_manager.py --doctor` to check for syntax errors and configuration load.

### Output
- Updated `src/core/config.py`

## 4. Verification
- [x] `python memory_manager.py --doctor` returns success (Structure check passed; version synced to 3.4.0).

## Evidence
- `src/core/config.py`: Updated BRIEF patterns and version 3.4.0.
- `memory_manager.py`: Rebuilt using `python build.py`.
- `.memory/VERSION`: Updated to 3.4.0.
- Doctor: Structure check 0 issues. Remaining issue in REQ-MCP-001 refs (unrelated to config).
