# MCP Definitions

System-generated. Do not edit directly.

Each section below documents an MCP function exposed by MemoryAtlas.

## apply_req

### Signature
`apply_req(req_id, dry_run=False) (Deprecated)`

### Summary
(Deprecated) Use plan() instead.

### Inputs
- `req_id` (str)
- `dry_run` (bool)

### Outputs
- Report dict

### Behavior
- Triggers deprecation warning.

## apply_req_full

### Signature
`apply_req_full(req_id) (Deprecated)`

### Summary
(Deprecated) One-shot orchestration.

### Inputs
- `req_id` (str)

### Outputs
- State dict

### Behavior
- See plan().

## continue_req

### Signature
`continue_req(req_id, implementation_done=false)`

### Summary
Advance the REQ state machine after implementation or verification.

### Inputs
- `req_id` (str): Target REQ ID.
- `implementation_done` (bool): Set true when implementation is complete.

### Outputs
- State-aware report with next action and any validation errors.

### Behavior
- Transitions RUN_CREATED → IMPLEMENTING.
- Transitions IMPLEMENTING → VERIFYING/READY_TO_FINALIZE based on checks.
- Re-runs validation gates when requested.

## create_disc_from_failure

### Signature
`create_disc_from_failure(context)`

### Summary
Generate a DISC draft for a failed stage.

### Inputs
- `context` (dict): stage, errors, files, rules, logs, req_id/target_id.

### Outputs
- DISC draft created in `02_REQUIREMENTS/discussions/`.

### Behavior
- Includes summary, evidence, hypotheses, fix options, next steps.
- One DISC per failure event.

## create_run

### Signature
`create_run(req_id)`

### Summary
Create a RUN document from template for a REQ.

### Inputs
- `req_id` (str): Target REQ ID.

### Outputs
- RUN document created in `04_TASK_LOGS/active/`.

### Behavior
- Includes Objective/Scope/Plan, Design Summary, Validation Gates, Exit Criteria.
- Keeps required RUN metadata fields.

## finalize_run

### Signature
`finalize_run(run_id, success=True, git_hash='')`

### Summary
(Alias) See finish().

### Inputs
- `run_id` (str)
- `success` (bool)
- `git_hash` (str)

### Outputs
- Same as finish().

### Behavior
- Alias for finish() - kept for backward compatibility.

## finish

### Signature
`finish(run_id, success=True, git_hash='')`

### Summary
Mark a RUN as completed with Git evidence.

### Inputs
- `run_id` (str): RUN ID.
- `success` (bool): Whether the run succeeded.
- `git_hash` (str): Git commit hash as evidence.

### Outputs
- RUN updated in `04_TASK_LOGS/active/` (no archive move).

### Behavior
- Updates Status to Completed/Failed.
- Records Git hash as evidence.
- RUN stays in active/ (v3.4+ policy).

## intake

### Signature
`intake(description, domain='GEN')`

### Summary
Intake a new user request and create a BRIEF document.

### Inputs
- `description` (str): User request logic/features.
- `domain` (str): Domain code (default 'GEN').

### Outputs
- BRIEF document path (key: `brief_path`).

### Behavior
- Creates a new BRIEF in active logs.
- Use this to start a new feature or task.

## plan

### Signature
`plan(brief_id)`

### Summary
Create a RUN document from an existing BRIEF.

### Inputs
- `brief_id` (str): Target Brief ID.

### Outputs
- RUN ID (key: `run_id`).
- RUN document path (key: `run_path`).

### Behavior
- Creates a RUN document linked to the Brief.
- Auto-creates/updates REQ documents.
- Moves workflow from Intake to Execution.

## plan_from_brief

### Signature
`plan_from_brief(brief_id)`

### Summary
(Alias) See plan().

### Inputs
- `brief_id` (str)

### Outputs
- Same as plan().

### Behavior
- Alias for plan() - kept for backward compatibility.

## req_status

### Signature
`req_status(req_id)`

### Summary
Inspect REQ readiness without executing pipeline.

### Inputs
- `req_id` (str): Target REQ ID.

### Outputs
- `status`: metadata status value.
- `metadata`: parsed REQ metadata.
- `readiness`: true/false.
- `blocking_issues`: list of reasons.

### Behavior
- Does not write any files.
- Useful for preflight checks in UIs.

## run_report

### Signature
`run_report(run_id)`

### Summary
Return a structured summary of a RUN document.

### Inputs
- `run_id` (str): RUN ID.

### Outputs
- `objective`, `scope`, `status`, `validation_state`, `artifacts`.

### Behavior
- Read-only; does not move or update RUN files.

## validate

### Signature
`validate(scope)`

### Summary
Run a single validation check and return issue count.

### Inputs
- `scope` (str): lint | req | links | doctor.

### Outputs
- Issue count and console report.

### Behavior
- Uses the same checks as `memory_manager.py`.

## Connection Guide

### Entry Points
- STDIO: `python .memory/00_SYSTEM/mcp/mcp_server.py --stdio`
- HTTP: `python .memory/00_SYSTEM/mcp/mcp_server.py --http --host 127.0.0.1 --port 8765`
- Module: `python -m memoryatlas_mcp --stdio`

### Auto-Launch Behavior
- STDIO clients can auto-spawn the server process on demand using the configured command.
- This means the server does not need to be manually running in the background.
- HTTP mode still requires a long-running server process.

### One-Shot Flow (apply_req_full)
- Call `apply_req_full(req_id)` to create the RUN and receive instructions.
- Implement changes, then call `apply_req_full(req_id)` again to verify and finalize.

### Spec Auto-Trigger
- Set REQ metadata `> **Requires-Spec**: true` to auto-create 03 specs.

### DISC Context Example
- `create_disc_from_failure({"req_id":"REQ-MCP-001","stage":"validate","errors":[{"type":"links","message":"3 link issues"}],"files":["02_REQUIREMENTS/README.md"],"rules":["RULE-LINK-001"],"logs":"..."})`

### Client Config Templates
- `claude_code.mcp.json` (STDIO)
- `codex.mcp.json` (STDIO)
- `gemini_cli.mcp.json` (STDIO)
- Bootstrap templates: `00_SYSTEM/mcp/templates/<target>.mcp.json` (from --bootstrap-mcp)

### Notes
- Clients usually require one-time server registration.
- HTTP mode may require authentication and is optional.
