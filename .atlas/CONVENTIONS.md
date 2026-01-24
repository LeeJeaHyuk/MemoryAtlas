# CONVENTIONS

## Boundaries

### Always
- Keep REQ/RULE/CQ as authority; do not auto-edit without intent.
- Record verification steps in RUN.

### Ask First
- Add or remove dependencies.
- Change storage layout under `.atlas/`.

### Never
- Hardcode secrets.
- Modify existing REQ/RULE/CQ silently.

## Roles (one-line)
- REQ: what the system must do.
- RULE: constraints that must always hold.
- CQ: questions the system must answer.
- BRIEF: intake summary.
- RUN: execution plan and evidence.

## Verification
- `python atlas.py doctor`
- (project tests as defined)
