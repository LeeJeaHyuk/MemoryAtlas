import argparse
import os
import shutil

CURRENT_VERSION = "1.1.0"
ROOT_DIR = ".memory"

DIRS = [
    "01_PROJECT_CONTEXT",
    "02_SERVICES",
    "03_MANAGEMENT/tasks",
    "90_TOOLING/scripts",
    "99_ARCHIVE",
]

DOC_TEMPLATES = {
    "00_INDEX.md": """# Project Memory Index

> Entry point for Memory-Driven Development in this repo.

## Start Here
- Read 01_PROJECT_CONTEXT to understand goals and architecture.
- Use 01_PROJECT_CONTEXT/04_AGENT_GUIDE.md for documentation rules and templates.
- Check 03_MANAGEMENT for current status and gaps.
- Use 02_SERVICES for feature-level requirements and specs.

## Context
- 01_PROJECT_CONTEXT/00_IDENTITY.md
- 01_PROJECT_CONTEXT/01_OVERVIEW.md
- 01_PROJECT_CONTEXT/02_ARCHITECTURE.md
- 01_PROJECT_CONTEXT/03_DATA_MODEL.md
- 01_PROJECT_CONTEXT/04_AGENT_GUIDE.md

## Services
- 02_SERVICES/README.md

## Management
- 03_MANAGEMENT/CHANGELOG.md
- 03_MANAGEMENT/WORKLOG.md
- 03_MANAGEMENT/STATUS.md
- 03_MANAGEMENT/COMPONENTS.md
- 03_MANAGEMENT/MISSING_COMPONENTS.md
- 03_MANAGEMENT/tasks/
""",
    "01_PROJECT_CONTEXT/00_IDENTITY.md": """# Project Identity

## Name
(TBD)

## One-Line Summary
Describe the project in a single sentence.

## Core Value
Explain why this system exists and what it unlocks.

## Audience
Who is this for? (humans, agents, both)
""",
    "01_PROJECT_CONTEXT/01_OVERVIEW.md": """# Project Overview

## Goal
Describe the primary outcome and value delivered by this project.

## Scope
List the in-scope capabilities and explicit exclusions.

## Stakeholders
Identify owners, users, and decision makers.
""",
    "01_PROJECT_CONTEXT/02_ARCHITECTURE.md": """# System Architecture

## High-Level Diagram
Describe components and data flow.

## Key Decisions
Record architectural choices and trade-offs.
""",
    "01_PROJECT_CONTEXT/03_DATA_MODEL.md": """# Data Model

## Core Entities
List the main entities and relationships.

## Invariants
Define rules that must always hold.
""",
    "01_PROJECT_CONTEXT/04_AGENT_GUIDE.md": """# Agent Guide

## Source of Truth
- Always start with 00_INDEX.md.
- Prefer .memory documents over ad-hoc assumptions.

## Update Rules
- Update 02_SERVICES when requirements or specs change.
- Update 01_PROJECT_CONTEXT when architecture or scope changes.
- Update 03_MANAGEMENT after implementing or deferring work.

## Documentation Standard: Structured Natural Language
Use the following 5 rules so humans and LLMs can both parse and act on documents reliably.

### Rule 1: Metadata Header (Context Injection)
Place a header at the very top to declare what the document is, who it is for, and its freshness.

```markdown
# Document Title (e.g., News Classification Service Requirements)

> **ID**: DOC-ING-001
> **Service**: Ingestion Service
> **Scope**: News article category classification and tagging logic
> **Last Updated**: 2026-01-15

---
```

### Rule 2: Atomic Requirements (ID-Scoped Blocks)
Write each requirement as its own block with an ID and explicit fields.

```markdown
### [REQ-CLS-001] Rule-Based Disclosure Classification

- **Description**: If the title contains certain keywords, classify immediately without an LLM.
- **Input**: `Article` (title, content)
- **Output**: `ClassificationResult` (category='CORP_EVENT', confidence=1.0)
- **Rules**:
  - If the title contains "[공시]" or "[IR]", classify as `CORP_EVENT`.
  - If the title contains "속보", increase weight.
```

### Rule 3: Checkbox State Tracking
Track implementation inside the requirement using checkboxes.

```markdown
- **Acceptance Criteria**:
  - [x] "[공시]" keyword handling implemented
  - [ ] "[IR]" keyword handling implemented
  - [ ] Unit tests written
```

### Rule 4: Explicit Schemas via Code Blocks
Define schemas and examples inside code blocks (json, python, etc.).

```markdown
**Output Format Example**:
```json
{
  "category": "MACRO",
  "confidence": 0.95,
  "reasoning": "Multiple mentions of rate hikes"
}
```
```

### Rule 5: Explicit Linking
Use relative links to related documents.

```markdown
## Related Documents
- **Data Model**: [../../01_PROJECT_CONTEXT/03_DATA_MODEL.md](../../01_PROJECT_CONTEXT/03_DATA_MODEL.md)
- **Architecture**: [../../01_PROJECT_CONTEXT/02_ARCHITECTURE.md](../../01_PROJECT_CONTEXT/02_ARCHITECTURE.md)
```

## Standard Template (Copy/Paste)
```markdown
# [Service Name] Requirements

> **Service**: [Service name, e.g., Ingestion]
> **Component**: [Component name, e.g., Classification Pipeline]
> **Status**: [Draft / Active / Deprecated]

---

## 1. Overview
Briefly describe what this document defines.

## 2. Requirements

### [REQ-AAA-001] [Feature Name]
- **Description**: Clear statement of what must be done.
- **Input**:
  - `text` (str): input description
- **Output**:
  - `result` (dict): output description
- **Logic/Rules**:
  1. First rule
  2. Second rule
- **Acceptance Criteria**:
  - [ ] Feature implemented
  - [ ] Edge cases handled
  - [ ] Tests passing

### [REQ-AAA-002] [Feature Name]
...

## 3. Data Structures
```python
# Pydantic-style or JSON example
class OutputDTO:
    id: str
    value: int
```

## 4. References
List related documents here.
```
""",
    "02_SERVICES/README.md": """# Services Index

This folder is intentionally project-specific.
Create subfolders for your domains (e.g., FRONTEND, BACKEND_API, INFRA).
Each service should have a short spec and interfaces listed.
""",
    "03_MANAGEMENT/STATUS.md": """# Implementation Status

## Phases
- [ ] Phase 1: Setup
- [ ] Phase 2: Core Features
- [ ] Phase 3: Hardening

## Current Focus
List the short-term targets and active milestones.
""",
    "03_MANAGEMENT/COMPONENTS.md": """# Component Matrix

## Implemented
- (none)

## In Progress
- (none)

## Not Started
- (none)

## Deprecated
- (none)
""",
    "03_MANAGEMENT/MISSING_COMPONENTS.md": """# Missing Components

Track gaps that block requirements or tests.
- (none)
""",
    "03_MANAGEMENT/CHANGELOG.md": """# Changelog

Track notable changes in the memory system.

## Unreleased
- (none)
""",
    "03_MANAGEMENT/WORKLOG.md": """# Work Log

Record work by date. Keep entries short and factual.

## YYYY-MM-DD
- (none)
""",
    "03_MANAGEMENT/tasks/README.md": """# Tasks

Use one file per task or sprint. Keep tasks small and actionable.
""",
}

LEGACY_FILES = [
    "03_REQUIREMENTS.md",
    "01_ARCH_DECISIONS.md",
]

SYSTEM_TEMPLATES = {
    "00_INDEX.md": DOC_TEMPLATES["00_INDEX.md"],
}


def write_file(path: str, content: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def ensure_structure(root: str) -> None:
    for folder in DIRS:
        os.makedirs(os.path.join(root, folder), exist_ok=True)


def create_missing_docs(root: str) -> None:
    for rel_path, content in DOC_TEMPLATES.items():
        path = os.path.join(root, rel_path)
        if os.path.exists(path):
            continue
        write_file(path, content)
        print(f"  + Created doc: {path}")


def smart_merge(root: str) -> None:
    archive_dir = os.path.join(root, "99_ARCHIVE")
    os.makedirs(archive_dir, exist_ok=True)

    for rel_path in LEGACY_FILES:
        legacy_path = os.path.join(root, rel_path)
        if not os.path.exists(legacy_path):
            continue
        dest_path = os.path.join(archive_dir, rel_path)
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        shutil.move(legacy_path, dest_path)
        print(f"  * Archived legacy file: {rel_path}")

    for rel_path, content in SYSTEM_TEMPLATES.items():
        path = os.path.join(root, rel_path)
        write_file(path, content)
        print(f"  * Updated system file: {rel_path}")


def update_tooling(root: str) -> None:
    src = os.path.abspath(__file__)
    dest = os.path.join(root, "90_TOOLING", "scripts", "memory_manager.py")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    if os.path.abspath(src) != os.path.abspath(dest):
        shutil.copyfile(src, dest)
        print(f"  * Updated tool: {dest}")


def read_version(root: str) -> str:
    version_file = os.path.join(root, "VERSION")
    if not os.path.exists(version_file):
        return "0.0.0"
    with open(version_file, "r", encoding="utf-8") as f:
        return f.read().strip()


def write_version(root: str) -> None:
    version_file = os.path.join(root, "VERSION")
    write_file(version_file, CURRENT_VERSION)


def init_or_update() -> None:
    installed_version = read_version(ROOT_DIR)
    print(
        f"Checking Memory System: Installed({installed_version}) "
        f"vs Current({CURRENT_VERSION})"
    )

    ensure_structure(ROOT_DIR)
    create_missing_docs(ROOT_DIR)
    update_tooling(ROOT_DIR)

    if installed_version != CURRENT_VERSION:
        write_version(ROOT_DIR)
        print(f"Updated to v{CURRENT_VERSION}")
    else:
        print("Already up to date.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="MemoryAtlas init/update tool.")
    parser.add_argument(
        "--migrate",
        action="store_true",
        help="Archive legacy files and refresh system templates.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    init_or_update()
    if args.migrate:
        smart_merge(ROOT_DIR)
