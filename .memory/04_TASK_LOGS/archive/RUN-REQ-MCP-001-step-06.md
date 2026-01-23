# [RUN-REQ-MCP-001-step-06] Phase 5: Templates & Bootstrap

> **ID**: RUN-REQ-MCP-001-step-06
> **Input**: src/core/config.py, src/core/bootstrap_mcp.py
> **Verification**: `python memory_manager.py --bootstrap-mcp` generates updated templates.
> **Last Updated**: 2026-01-23

---

## 1. Objective

Update system templates and definitions to include the new Brief-driven workflow tools (`intake`, `plan_from_brief`) and ensure the MCP bootstrap process produces correct configuration files for clients.

## 2. Requirements

### A. Config Updates (`src/core/config.py`)
1.  Add `DOC_TEMPLATES["briefs"]`: New template for `BRIEF-*.md`.
    - Should match the structure used in `automation.py`.
2.  Add `MCP_DEFINITIONS` entries for `intake` and `plan_from_brief`.
    - Mark `apply_req` variants as "deprecated".

### B. Bootstrap Updates (`src/core/bootstrap_mcp.py`)
1.  Ensure `_render_prompt` includes the new tool definitions (it iterates `MCP_DEFINITIONS`, so config update might be sufficient).
2.  Update `_render_mcp_template` if necessary (usually robust).

## 3. Scope

### In Scope
- `src/core/config.py`
- `src/core/bootstrap_mcp.py` (if needed)

### Out of Scope
- Client-side configuration (user responsibility, but we provide the JSON).

## 4. Verification
- [x] Config updated with `briefs` template and new MCP definitions.
- [x] `memory_manager.py` rebuilt.
- [x] `python memory_manager.py --bootstrap-mcp` creates prompt with correct tool list (`intake`, `plan_from_brief`).

## 5. Evidence
- `BOOTSTRAP_MCP_PROMPT_claude_code_windows.md` contains `intake` and `plan_from_brief`.
- `apply_req` marked as deprecated in tool list.

## Output
- `src/core/config.py` updated.
- MCP bootstrap artifacts regenerated.

