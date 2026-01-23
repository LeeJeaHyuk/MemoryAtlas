# [RUN-REQ-MCP-001-step-05] Phase 4: MCP Server (mcp_server.py)

> **ID**: RUN-REQ-MCP-001-step-05
> **Input**: src/mcp_server.py
> **Verification**: `python memory_manager.py --mcp` then testing intake/plan tools via mock or manual invocation.
> **Last Updated**: 2026-01-23

---

## 1. Objective

Expose the new automation logic (`intake`, `plan_from_brief`) as MCP tools in `src/mcp_server.py`. This provides the client interface for the Brief-driven workflow.

## 2. Requirements

### A. New Tools
1.  `intake(description: str, domain: str = "GEN") -> Dict`:
    - Wraps `Automator.intake`.
    - Returns `brief_path`.
2.  `plan_from_brief(brief_id: str) -> Dict`:
    - Wraps `Automator.plan_from_brief`.
    - Returns `run_path`.

### B. Updates
1.  `apply_req` (and `kick_off` if present): Mark as deprecated in docstring and print warning.
2.  `finalize_run`: Update `req_id` extraction logic to simpler regex or split, since Brief-based RUN IDs (`RUN-BRIEF-GEN-001-step-01`) might differ from REQ-based IDs.
    - If `req_id` cannot be extracted (because it's a Brief), skip state machine update or handle gracefully without crashing.

## 3. Scope

### In Scope
- `src/mcp_server.py`

### Out of Scope
- Config changes (Phase 1 verified).
- Automation logic (Phase 3 verified).

## 4. Verification
- [x] `mcp_server.py` updated and rebuilt.
- [x] `python memory_manager.py --mcp` runs (despite existing MCP setup warnings, the server logic is loaded).
- [x] `apply_req` deprecation warning added.

## 5. Evidence
- Source code shows `intake` and `plan_from_brief` decorated with `@mcp.tool()`.

## Output
- `src/mcp_server.py` updated.
- `memory_manager.py` rebuilt.

