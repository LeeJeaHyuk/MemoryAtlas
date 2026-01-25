# MemoryAtlas

> Document-Driven Development with Atlas CLI

[English](README.en.md) | [한국어](README.md)

## 3-Step Workflow

Atlas runs on **Intake → Plan → Finish**.

```
[idea] → Intake → [BRIEF] → Plan → [RUN] → Implementation → Finish
```

### Step 0: Init (first time)

```bash
python atlas.py init
```

- Creates the `.atlas/` structure and default docs/templates.
- Onboarding prompt: `.atlas/.system/prompts/onboarding.md`

### Step 1: Intake

```bash
python atlas.py intake "Add user authentication" --domain GEN
```

- Creates `.atlas/brief/BRIEF-GEN-001.md`

### Step 2: Plan

```bash
python atlas.py plan BRIEF-GEN-001
```

- Creates `.atlas/runs/RUN-BRIEF-GEN-001-step-01.md`
- Generates REQ stubs if REQ IDs are referenced in the brief

### Step 3: Finish

```bash
python atlas.py finish RUN-BRIEF-GEN-001-step-01 --git abc1234 --success true
```

- Updates RUN metadata (Status/Git/Completed)

### Doctor (validation)

```bash
python atlas.py doctor
```

- Checks structure, links, and required docs

## Core structure

| Path | Role |
|---|---|
| `.atlas/FRONT.md` | Project overview / quick usage |
| `.atlas/BOARD.md` | Current work status |
| `.atlas/CONVENTIONS.md` | Working rules |
| `.atlas/GOALS.md` | Goals & scope |
| `.atlas/req/` | REQ documents |
| `.atlas/rule/` | RULE documents |
| `.atlas/cq/` | CQ documents |
| `.atlas/brief/` | BRIEF documents |
| `.atlas/runs/` | RUN documents |
| `.atlas/idea/` | Unstructured notes |
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
