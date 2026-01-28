# MemoryAtlas (Refactored)

> SSOT-First Development with Atlas CLI

[English] | [한국어](README.md)

## Core Philosophy
- SSOT: source of truth for machines and systems (REQ, RULE, ADR)
- Views: human-readable context (views/)
- Execution: plans, results, and git evidence (RUN)

## 3-Step Workflow
Atlas runs on Capture -> Run -> Finish.

### Step 0: Init (first time)
```bash
python atlas.py init
```
- Creates the `.atlas/` structure and default templates.

### Step 1: Capture
Capture updates SSOT (REQ) and Views directly.
```bash
python atlas.py capture "Add user authentication" --domain GEN
```
Result:
- `.atlas/req/REQ-GEN-001.md` created/updated
- `.atlas/views/REQ-GEN-001.md` created/updated

Compatibility option:
```bash
python atlas.py capture "..." --domain GEN --to brief
```
- `.atlas/drafts/brief/BRIEF-GEN-001.md` created

### Step 2: Run
Create a RUN document for a target REQ.
```bash
python atlas.py run REQ-GEN-001
```
Result:
- `.atlas/runs/RUN-REQ-GEN-001-step-01.md` created
- Plan/Verification included in RUN

### Step 3: Finish
Record git evidence when implementation is done.
```bash
python atlas.py finish RUN-REQ-GEN-001-step-01 --git a1b2c3d --success true
```
Result:
- RUN status updated to Completed
- REQ header updated with Implemented-Git / Linked-RUN

### Doctor (validation)
```bash
python atlas.py doctor
```
- Validates view links to REQ files
- Warns if Implemented REQ lacks git evidence

## Core structure

| Path | Role |
|---|---|
| `.atlas/FRONT.md` | Project overview / quick usage |
| `.atlas/BOARD.md` | Current work status |
| `.atlas/CONVENTIONS.md` | Working rules |
| `.atlas/GOALS.md` | Goals & scope |
| `.atlas/req/` | REQ documents (SSOT) |
| `.atlas/rule/` | RULE documents (SSOT) |
| `.atlas/adr/` | ADR documents (SSOT) |
| `.atlas/cq/` | CQ documents |
| `.atlas/views/` | View documents |
| `.atlas/drafts/brief/` | BRIEF drafts (optional) |
| `.atlas/runs/` | RUN documents |
| `.atlas/inbox/` | External input / idea buffer |
| `.atlas/archive/` | Archived artifacts |
| `.atlas/.system/templates/` | Templates used by Atlas |
| `src/.system_defaults/` | Default templates/docs/prompts |

## Refreshing defaults
- To reapply defaults:
  ```bash
  python atlas.py init --overwrite
  ```

## Dev build
- After editing `src/`, rebuild the single-file CLI:
  ```bash
  python build.py
  ```
