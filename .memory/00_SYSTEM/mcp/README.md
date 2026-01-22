# MCP Definitions

System-generated. Do not edit directly.

Each section below documents an MCP function exposed by MemoryAtlas.

## apply_req

### Signature
`apply_req(req_id, dry_run=false, create_spec="auto")`

### Summary
Orchestrate the REQ -> RUN pipeline with validation gates.

### Inputs
- `req_id` (str): Target REQ ID.
- `dry_run` (bool): Preview only.
- `create_spec` (bool | "auto"): Create spec draft when true or auto-triggered.

### Outputs
- RUN document created/updated in `04_TASK_LOGS/active/`.
- DISC draft path on failure.
- Stage/result report.

### Behavior
- Requires REQ `Status=Active`.
- Runs `validate(lint)`, `validate(req)`, `validate(links)` gates.
- Creates 03 specs when `create_spec` is true or auto-triggered.
- Does not edit code by default.

## apply_req_full

### Signature
`apply_req_full(req_id, dry_run=false)`

### Summary
One-shot orchestration that drives the state machine and returns follow-up hints.

### Inputs
- `req_id` (str): Target REQ ID.
- `dry_run` (bool): Preview only.

### Outputs
- State-aware report (`state`, `run_id`, `next_action`).
- `instructions` plus `continue_with` / `continue_args` for client-driven steps.
- DISC draft path on failure.

### Behavior
- Runs lint/req/links validation on the first pass.
- Creates RUN when validation passes.
- Returns implementation instructions; code edits are performed by the client/agent.
- Runs `--doctor` and finalizes when state is ready.

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
`finalize_run(run_id)`

### Summary
Mark a RUN as completed and archive it.

### Inputs
- `run_id` (str): RUN ID.

### Outputs
- RUN moved to `04_TASK_LOGS/archive/` after validation.

### Behavior
- Requires `--doctor` pass before completion.

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
