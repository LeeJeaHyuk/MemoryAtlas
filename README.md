# MemoryAtlas

MemoryAtlas is a memory-driven development toolkit that keeps project context,
requirements, and execution logs aligned for humans and LLMs.

## What this repo contains

- A CLI tool (`memory_manager.py`) built from `src/` via `build.py`.
- A `.memory/` workspace that stores the project knowledge base.
- An MCP automation server and client templates under `.memory/00_SYSTEM/mcp/`.
- A validation engine that enforces the MemoryAtlas authority model.

## Core capabilities (from `.memory/02_REQUIREMENTS/capabilities/`)

- Initialize or update the `.memory/` structure.
- Bootstrap project context for AI-assisted setup (`--bootstrap`).
- Validate structure, metadata, links, requirements, and RUN logs.
- Generate a status report for active tasks (`--status`).
- Reverse-engineer focused code areas into prompts (`--reverse`, draft).
- Build a single-file CLI with Stickytape (`build.py`).
- Automate REQ -> RUN creation via CLI and MCP tools.

## Non-negotiable invariants (from `.memory/02_REQUIREMENTS/invariants/`)

- Required `.memory/` directory layout (`RULE-DIR-001`).
- Three-way ID consistency: filename, header, metadata (`RULE-VALID-001`).
- Strict metadata header fields by document type (`RULE-META-001`).
- Must-Read field allows only RULE/ADR IDs (`RULE-MUST-001`).
- Link validation rules for documentation (`RULE-LINK-001`).
- Versioning policy for manager vs template (`RULE-VER-001`).

See the authoritative docs in `.memory/00_INDEX.md` and `.memory/02_REQUIREMENTS/`.

## Quick start

```bash
# Initialize or update .memory
python memory_manager.py

# Full system validation
python memory_manager.py --doctor

# Show active task summary
python memory_manager.py --status

# Create AI bootstrap prompts
python memory_manager.py --bootstrap

# Preview changes without writing
python memory_manager.py --dry-run

# Create a RUN from a REQ (optionally skip spec draft)
python memory_manager.py apply-req --id REQ-EXAMPLE-001
python memory_manager.py apply-req --id REQ-EXAMPLE-001 --dry-run --no-spec

# Generate MCP bootstrap prompt and templates
python memory_manager.py --bootstrap-mcp --target claude_code --os windows
```

## Reverse engineering (draft)

Generate a focused prompt for partial code analysis:

```bash
python memory_manager.py --reverse --focus src/core
```

This creates `.memory/00_REVERSE_PROMPT.md`.

## MCP automation

MCP tool definitions and client templates live in `.memory/00_SYSTEM/mcp/`.
See `.memory/00_SYSTEM/mcp/README.md` for the full list (apply_req, req_status, run_report, etc.).

```bash
# STDIO server (local)
python .memory/00_SYSTEM/mcp/mcp_server.py --stdio

# Module entrypoint
python -m memoryatlas_mcp --stdio
```

## .memory layout (v3 Capabilities & Invariants)

```
.memory/
  00_SYSTEM/                  # System-managed rules, scripts, and MCP entrypoints
  01_PROJECT_CONTEXT/         # Project goals and conventions
  02_REQUIREMENTS/
    capabilities/             # REQ-* (what the system must do)
    invariants/               # RULE-* (non-negotiable rules)
    discussions/              # DISC-* (reference-only discussions)
  03_TECH_SPECS/              # ADRs and technical specs (how)
  04_TASK_LOGS/
    active/                   # RUN-* execution steps
    archive/                  # Completed task logs
  98_KNOWLEDGE/               # Troubleshooting and shared knowledge
  99_ARCHIVE/                 # Deprecated or legacy content
```

## Common validation commands

```bash
python memory_manager.py --check     # Structure
python memory_manager.py --lint      # Metadata headers
python memory_manager.py --links     # Links
python memory_manager.py --req       # REQ/RULE validation
python memory_manager.py --runs      # RUN validation
python memory_manager.py --mcp-check # MCP bootstrap outputs
```

## Build and development

- Python 3.8+ is required.
- `build.py` bundles `src/` into `memory_manager.py`.
- Install Stickytape only when building:

```bash
pip install stickytape
python build.py
```

## Where to start

- `.memory/00_INDEX.md` for the documentation map and reading priority.
- `.memory/01_PROJECT_CONTEXT/00_GOALS.md` for project identity.
- `.memory/01_PROJECT_CONTEXT/01_CONVENTIONS.md` for working rules.
