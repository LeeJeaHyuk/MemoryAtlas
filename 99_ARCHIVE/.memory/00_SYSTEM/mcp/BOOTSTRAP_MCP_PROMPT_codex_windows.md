# MCP Bootstrap Prompt

Goal: Configure MCP so the client can auto-spawn the MemoryAtlas server on demand.
Target client: codex
OS: windows
Python strategy: default to .venv unless specified otherwise.

Constraints:
- Do NOT edit anything under 02_REQUIREMENTS automatically.
- Use STDIO mode for MCP server execution.

Project context:
- Repo root contains .memory/ and memory_manager.py
- MCP entrypoint: .memory/00_SYSTEM/mcp/mcp_server.py

MCP tool definitions:
- apply_req(req_id, dry_run=False) (Deprecated): (Deprecated) Use plan_from_brief instead.
- apply_req_full(req_id) (Deprecated): (Deprecated) One-shot orchestration.
- continue_req(req_id, implementation_done=false): Advance the REQ state machine after implementation or verification.
- create_disc_from_failure(context): Generate a DISC draft for a failed stage.
- create_run(req_id): Create a RUN document from template for a REQ.
- finalize_run(run_id): Mark a RUN as completed and archive it.
- intake(description, domain='GEN'): Intake a new user request and create a BRIEF document.
- plan_from_brief(brief_id): Create a RUN document from an existing BRIEF.
- req_status(req_id): Inspect REQ readiness without executing pipeline.
- run_report(run_id): Return a structured summary of a RUN document.
- validate(scope): Run a single validation check and return issue count.

Required outputs (fixed format):
1) List of files to create or update (with paths).
2) Full contents of each file or a unified diff patch.
3) Installation / connection steps (3-5 steps).
4) Verification steps (commands to run).

Must include:
- apply_req_full two-call flow in MCP README.
- Requires-Spec metadata example in MCP README.
- create_disc_from_failure(context) example in MCP README.

Default file targets:
- .memory/00_SYSTEM/mcp/templates/codex.mcp.json
- .memory/00_SYSTEM/scripts/run_mcp_server.ps1
- .memory/00_SYSTEM/scripts/run_mcp_server.sh

Validation commands:
- python memory_manager.py --doctor
- python memory_manager.py --mcp-check --target codex
