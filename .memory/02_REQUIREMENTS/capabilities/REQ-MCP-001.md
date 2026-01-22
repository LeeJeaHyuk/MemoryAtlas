# [REQ-MCP-001] MCP Execution Automation (REQ -> RUN)

> **ID**: REQ-MCP-001
> **Domain**: MCP
> **Status**: Active
> **Last Updated**: 2026-01-22
> **Must-Read**: RULE-ID-001, RULE-META-001, RULE-VALID-001, RULE-MUST-001, RULE-DIR-001
> **Template-Version**: 3.3

---

## Decision

Provide MCP-based automation that converts a confirmed REQ into a RUN plan,
runs required validations, and records failures as DISC drafts. The only
execution confirmation signal is `Status=Active` on the REQ.

---

## Input

- `req_id` (str): Target REQ ID to execute.
- `dry_run` (bool): If true, generate previews only.
- `scope` (str): Validation scope for `validate()` (lint/req/links/doctor).
- `create_spec` (bool | "auto"): When "auto", create spec only if `Requires-Spec: true`.
- `context` (dict): Failure context used to generate DISC drafts.
- `target` (str): MCP bootstrap client target (claude_code, claude_desktop, codex, gemini_cli, ci).
- `os` (str): MCP bootstrap OS target (windows, unix).

---

## Output

 - Updated or new documents:
   - `00_SYSTEM/mcp/README.md` (auto-generated MCP definitions)
  - `03_TECH_SPECS/*` (conditional)
  - `04_TASK_LOGS/active/RUN-...` (always)
  - `02_REQUIREMENTS/discussions/DISC-...` (on failure)
- Execution report: stage, status, and next action.
- One-shot reports include `instructions`, `continue_with`, and `continue_args`.

---

## MCP Functions (MVP)

- `apply_req(req_id, dry_run=false, create_spec=true)`: Orchestrates the pipeline end-to-end.
- `apply_req_full(req_id, dry_run=false)`: One-shot orchestrator with follow-up hints.
- `validate(scope)`: Runs `--lint`, `--req`, `--links`, or `--doctor`.
- `create_run(req_id)`: Creates a RUN document in `04_TASK_LOGS/active/`.
- `continue_req(req_id, implementation_done=false)`: Advances state after implementation.
- `finalize_run(run_id)`: Marks RUN completed and moves it to archive.
- `create_disc_from_failure(context)`: Generates a DISC draft for failure analysis.
- `req_status(req_id)`: Returns readiness and blocking issues without execution.
- `run_report(run_id)`: Returns a structured summary of a RUN.

---

## Logic

### 0. Confirmation Signal (REQ)
- Only `Status=Active` is treated as "confirmed".
- Allowed state transitions: `Draft` -> `Active` -> `Deprecated/Archived`.
- Do not use separate READY flags to avoid dual-source drift.

### 1. Gate (REQ Validation)
- Run `validate(lint)`, `validate(req)`, `validate(links)`.
- If any gate fails, stop and create a DISC draft classified as "requirement failure".

### 2. 03_TECH_SPECS Policy
- Default: skip 03.
- Use RUN "Design Summary" when the change is small or localized.
- Create/update `03_TECH_SPECS` (ADR or Spec) when any trigger holds:
  - Public API/CLI/input-output format change.
  - Module boundaries or folder structure changes.
  - Data schema changes (tables/fields/triples).
  - Performance, security, or compatibility-impacting decisions.
- MVP trigger: REQ metadata `Requires-Spec: true`.

### 3. RUN Creation
- Generate a RUN doc from template in `04_TASK_LOGS/active/`.
- Minimum sections:
  - Objective / Scope / Plan (Phases)
  - Design Summary (required when no 03)
  - Validation Gates (commands to pass)
  - Exit Criteria (definition of done)
- Preserve required RUN metadata (`Input`, `Verification`, `Output`).

### 4. Execution Boundary
- MCP does not edit code by default.
- Code changes are performed by a human or a separate coding agent.
- Before/after verification uses `--doctor` and tests.

### 5. Finalization
- If `--doctor` passes, mark RUN as completed and archive it.
- Record all auto-generated files and reasons in the RUN output.

### 6. Failure Handling (Any Stage)
- Generate one DISC draft with:
  - Summary, Stage, Evidence (rules/files/log excerpt)
  - Hypotheses (2-3)
  - Fix Options (minimum two)
  - Next Steps (checklist + restart point)
- Leave existing RUN in progress with failure notes.
- Retry only after user review.

### 7. One-Shot Orchestration (apply_req_full)
- Runs validation gates, creates RUN, then returns implementation instructions.
- The client/agent performs code changes and resumes the flow using `continue_with`.
- When verification passes, the flow finalizes the RUN and archives it.

### 8. MCP Bootstrap Command
- CLI: `python memory_manager.py --bootstrap-mcp --target <client> --os <windows|unix>`
- Generates bootstrap prompt + checklist, templates, and run scripts.
- Validation: `python memory_manager.py --doctor` and `python memory_manager.py --mcp-check --target <client>`.

---

## Acceptance Criteria

- [ ] `Status=Active` is the only execution confirmation signal.
- [ ] `apply_req()` runs validation gates and stops on failure.
- [ ] `apply_req()` runs `lint/req/links` gates before RUN creation.
- [ ] `apply_req_full()` returns `instructions` and `continue_with` for client-driven execution.
- [ ] `create_run()` always creates a RUN with required sections and metadata.
- [ ] 03 specs are created only when trigger conditions match.
- [ ] `create_disc_from_failure()` produces a structured DISC draft.
- [ ] `finalize_run()` archives only after `--doctor` passes.
- [ ] `--bootstrap-mcp` generates prompt + templates and passes `--mcp-check`.
- [ ] All automation writes are logged in the RUN output.

---

## Validation

```bash
# Orchestrated dry run
apply_req(REQ-XXX-001, dry_run=true)

# One-shot flow
apply_req_full(REQ-XXX-001)

# Full execution gate checks
validate("lint")
validate("req")
validate("links")
```
