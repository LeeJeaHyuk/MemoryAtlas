# [REQ-MCP-001] MCP Execution Automation (REQ -> RUN)

> **ID**: REQ-MCP-001
> **Domain**: MCP
> **Status**: Active
> **Last Updated**: 2026-01-22
> **Must-Read**: RULE-ID-001, RULE-META-001, RULE-VALID-001, RULE-MUST-001, RULE-DIR-001
> **Template-Version**: 2.4

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
- `context` (dict): Failure context used to generate DISC drafts.

---

## Output

 - Updated or new documents:
   - `00_SYSTEM/mcp/README.md` (auto-generated MCP definitions)
  - `03_TECH_SPECS/*` (conditional)
  - `04_TASK_LOGS/active/RUN-...` (always)
  - `02_REQUIREMENTS/discussions/DISC-...` (on failure)
- Execution report: stage, status, and next action.

---

## MCP Functions (MVP)

- `apply_req(req_id, dry_run=false, create_spec=true)`: Orchestrates the pipeline end-to-end.
- `validate(scope)`: Runs `--lint`, `--req`, `--links`, or `--doctor`.
- `create_run(req_id)`: Creates a RUN document in `04_TASK_LOGS/active/`.
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

---

## Acceptance Criteria

- [ ] `Status=Active` is the only execution confirmation signal.
- [ ] `apply_req()` runs validation gates and stops on failure.
- [ ] `create_run()` always creates a RUN with required sections and metadata.
- [ ] 03 specs are created only when trigger conditions match.
- [ ] `create_disc_from_failure()` produces a structured DISC draft.
- [ ] `finalize_run()` archives only after `--doctor` passes.
- [ ] All automation writes are logged in the RUN output.

---

## Validation

```bash
# Orchestrated dry run
apply_req(REQ-XXX-001, dry_run=true)

# Full execution gate checks
validate("lint")
validate("req")
validate("links")
```
