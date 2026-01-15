import argparse
import os
import re
import shutil

CURRENT_VERSION = "1.3.0"
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

AGENT_RULES_TEMPLATE = """# MemoryAtlas Agent Rules

> **SYSTEM FILE**: This file is managed by `memory_manager.py`.
> **DO NOT EDIT**: Changes made here will be overwritten by the system update.

This document defines the **STRICT BEHAVIORAL PROTOCOLS** for any AI Agent working on this project.

---

## 1. Core Philosophy
You are an intelligent operator of the **MemoryAtlas** documentation system.
Your goal is to keep the documentation (`.memory/`) in perfect sync with the codebase.

## 2. Universal Constraints
<constraints>
    <rule id="NO_SYSTEM_MODIFICATION">
        You must NEVER modify files in `.memory/90_TOOLING/` or the `memory_manager.py` script.
        These are system-locked files. If a user asks to change them, explain that they must update the central repository.
    </rule>

    <rule id="CONTEXT_FIRST_APPROACH">
        Before generating any code, you MUST read `.memory/00_INDEX.md` to understand the project map.
        Do not guess the architecture; look it up in `01_PROJECT_CONTEXT/`.
    </rule>

    <rule id="DOCUMENTATION_SYNCHRONIZATION">
        <trigger>Any modification to business logic or functional code</trigger>
        <action>
            Immediately update the corresponding requirement file in `.memory/02_SERVICES/`.
            If the file does not exist, create it following the standard template.
        </action>
    </rule>
</constraints>

## 3. Directory Authority Protocol
<directory_protocol>
    <dir path=".memory/01_PROJECT_CONTEXT">
        <access>READ_ONLY</access>
        <description>Architecture & Global Context. Do not modify unless instructed for architectural refactoring.</description>
    </dir>
    <dir path=".memory/02_SERVICES">
        <access>READ_WRITE</access>
        <description>Living requirements. You own this folder. Update it aggressively.</description>
    </dir>
    <dir path=".memory/03_MANAGEMENT">
        <access>READ_WRITE</access>
        <description>Task tracking. Check `STATUS.md` before starting work.</description>
    </dir>
</directory_protocol>

## 4. Interaction Style
- **When starting**: "I have loaded the MemoryAtlas context. Checking `STATUS.md`..."
- **When blocked**: "The requirement in `02_SERVICES/...` conflicts with the code. Which one is correct?"
"""

LEGACY_FILES = [
    "03_REQUIREMENTS.md",
    "01_ARCH_DECISIONS.md",
]

SYSTEM_TEMPLATES = {
    "90_TOOLING/AGENT_RULES.md": AGENT_RULES_TEMPLATE,
}

MIGRATE_TEMPLATES = {
    "00_INDEX.md": DOC_TEMPLATES["00_INDEX.md"],
}

REQUIRED_SYSTEM_FILES = [
    "VERSION",
    "90_TOOLING/AGENT_RULES.md",
    "90_TOOLING/scripts/memory_manager.py",
]

LINT_DIRS = ["01_PROJECT_CONTEXT", "02_SERVICES"]
LINK_SCAN_DIRS = ["01_PROJECT_CONTEXT", "02_SERVICES", "03_MANAGEMENT"]
REQ_SCAN_DIRS = ["02_SERVICES"]
LINT_SKIP_FILES = {"README.md", "00_INDEX.md", "04_AGENT_GUIDE.md"}
HEADER_FIELDS = ["**ID**", "**Service**", "**Scope**", "**Last Updated**"]

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
REQ_HEADER_RE = re.compile(r"^###\s+\[(REQ-[A-Za-z0-9_-]+)\]", re.M)
CHECKBOX_RE = re.compile(r"^\s*-\s*\[[ xX]\]", re.M)
FIELD_PATTERNS = {
    "Description": re.compile(r"^\s*-\s*\*\*Description\*\*:", re.M | re.I),
    "Input": re.compile(r"^\s*-\s*\*\*Input\*\*:", re.M | re.I),
    "Output": re.compile(r"^\s*-\s*\*\*Output\*\*:", re.M | re.I),
    "Acceptance Criteria": re.compile(
        r"^\s*-\s*\*\*Acceptance Criteria\*\*:", re.M | re.I
    ),
}


def write_file(path: str, content: str, dry_run: bool = False) -> None:
    if dry_run:
        return
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def ensure_structure(root: str) -> None:
    for folder in DIRS:
        os.makedirs(os.path.join(root, folder), exist_ok=True)


def create_missing_docs(root: str, dry_run: bool = False) -> None:
    for rel_path, content in DOC_TEMPLATES.items():
        path = os.path.join(root, rel_path)
        if os.path.exists(path):
            continue
        if dry_run:
            print(f"  - Would create doc: {path}")
            continue
        write_file(path, content)
        print(f"  + Created doc: {path}")


def update_system_templates(root: str, dry_run: bool = False) -> None:
    for rel_path, content in SYSTEM_TEMPLATES.items():
        path = os.path.join(root, rel_path)
        if dry_run:
            print(f"  - Would update system file: {rel_path}")
            continue
        write_file(path, content)
        print(f"  * Updated system file: {rel_path}")


def smart_merge(root: str, dry_run: bool = False) -> None:
    archive_dir = os.path.join(root, "99_ARCHIVE")
    os.makedirs(archive_dir, exist_ok=True)

    for rel_path in LEGACY_FILES:
        legacy_path = os.path.join(root, rel_path)
        if not os.path.exists(legacy_path):
            continue
        dest_path = os.path.join(archive_dir, rel_path)
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        if dry_run:
            print(f"  - Would archive legacy file: {rel_path}")
            continue
        shutil.move(legacy_path, dest_path)
        print(f"  * Archived legacy file: {rel_path}")

    for rel_path, content in MIGRATE_TEMPLATES.items():
        path = os.path.join(root, rel_path)
        if dry_run:
            print(f"  - Would update system file: {rel_path}")
            continue
        write_file(path, content)
        print(f"  * Updated system file: {rel_path}")


def update_tooling(root: str, dry_run: bool = False) -> None:
    src = os.path.abspath(__file__)
    dest = os.path.join(root, "90_TOOLING", "scripts", "memory_manager.py")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    if os.path.abspath(src) != os.path.abspath(dest):
        if dry_run:
            print(f"  - Would update tool: {dest}")
            return
        shutil.copyfile(src, dest)
        print(f"  * Updated tool: {dest}")


def read_version(root: str) -> str:
    version_file = os.path.join(root, "VERSION")
    if not os.path.exists(version_file):
        return "0.0.0"
    with open(version_file, "r", encoding="utf-8") as f:
        return f.read().strip()


def write_version(root: str, dry_run: bool = False) -> None:
    version_file = os.path.join(root, "VERSION")
    if dry_run:
        print(f"  - Would update version: {version_file}")
        return
    write_file(version_file, CURRENT_VERSION)


def init_or_update(dry_run: bool = False) -> None:
    installed_version = read_version(ROOT_DIR)
    print(
        f"Checking Memory System: Installed({installed_version}) "
        f"vs Current({CURRENT_VERSION})"
    )

    ensure_structure(ROOT_DIR)
    create_missing_docs(ROOT_DIR, dry_run=dry_run)
    update_system_templates(ROOT_DIR, dry_run=dry_run)
    update_tooling(ROOT_DIR, dry_run=dry_run)

    if installed_version != CURRENT_VERSION:
        write_version(ROOT_DIR, dry_run=dry_run)
        if dry_run:
            print(f"Would update to v{CURRENT_VERSION}")
        else:
            print(f"Updated to v{CURRENT_VERSION}")
    else:
        print("Already up to date.")

def iter_md_files(root: str, dirs) -> list:
    files = []
    for base in dirs:
        base_path = os.path.join(root, base)
        if not os.path.isdir(base_path):
            continue
        for dirpath, _, filenames in os.walk(base_path):
            for name in filenames:
                if name.lower().endswith(".md"):
                    files.append(os.path.join(dirpath, name))
    return files


def check_structure(root: str) -> int:
    issues = 0
    if not os.path.isdir(root):
        print(f"! Missing root directory: {root}")
        return 1

    for folder in DIRS:
        path = os.path.join(root, folder)
        if not os.path.isdir(path):
            print(f"! Missing directory: {path}")
            issues += 1

    required_files = set(DOC_TEMPLATES.keys())
    required_files.update(REQUIRED_SYSTEM_FILES)
    required_files.update(SYSTEM_TEMPLATES.keys())

    for rel_path in sorted(required_files):
        path = os.path.join(root, rel_path)
        if not os.path.exists(path):
            print(f"! Missing file: {path}")
            issues += 1

    installed_version = read_version(root)
    if installed_version != CURRENT_VERSION:
        print(
            f"! Version mismatch: installed {installed_version} "
            f"vs current {CURRENT_VERSION}"
        )
        issues += 1

    print(f"Structure check: {issues} issue(s)")
    return issues


def lint_metadata(root: str) -> int:
    issues = 0
    for path in iter_md_files(root, LINT_DIRS):
        name = os.path.basename(path)
        if name in LINT_SKIP_FILES:
            continue
        text = read_text(path)
        head = "\n".join(text.splitlines()[:40])
        missing = [field for field in HEADER_FIELDS if field not in head]
        if missing:
            rel_path = os.path.relpath(path, root)
            print(f"! Missing header fields in {rel_path}: {', '.join(missing)}")
            issues += 1
    print(f"Metadata lint: {issues} issue(s)")
    return issues


def iter_links(text: str) -> list:
    links = []
    in_code = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        for match in LINK_RE.finditer(line):
            links.append(match.group(1).strip())
    return links


def check_links(root: str) -> int:
    issues = 0
    for path in iter_md_files(root, LINK_SCAN_DIRS):
        text = read_text(path)
        for target in iter_links(text):
            if not target:
                continue
            if target.startswith("#"):
                continue
            if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target):
                continue
            clean = target.split("#", 1)[0].split("?", 1)[0].strip()
            if not clean:
                continue
            if clean.startswith("<") and clean.endswith(">"):
                clean = clean[1:-1].strip()
            if os.path.isabs(clean) or re.match(r"^[A-Za-z]:", clean):
                if not os.path.exists(clean):
                    rel_path = os.path.relpath(path, root)
                    print(f"! Broken absolute link in {rel_path}: {target}")
                    issues += 1
                continue
            resolved = os.path.normpath(os.path.join(os.path.dirname(path), clean))
            if not os.path.exists(resolved):
                rel_path = os.path.relpath(path, root)
                print(f"! Broken link in {rel_path}: {target}")
                issues += 1
    print(f"Link check: {issues} issue(s)")
    return issues


def parse_requirement_blocks(text: str) -> list:
    blocks = []
    current = None
    for line in text.splitlines():
        header = REQ_HEADER_RE.match(line)
        if header:
            if current:
                blocks.append(current)
            current = {"id": header.group(1), "lines": []}
            continue
        if current is not None:
            current["lines"].append(line)
    if current:
        blocks.append(current)
    return blocks


def check_requirements(root: str) -> int:
    issues = 0
    seen = {}
    for path in iter_md_files(root, REQ_SCAN_DIRS):
        text = read_text(path)
        blocks = parse_requirement_blocks(text)
        for block in blocks:
            req_id = block["id"]
            rel_path = os.path.relpath(path, root)
            if req_id in seen:
                print(
                    f"! Duplicate requirement ID {req_id} in {rel_path} "
                    f"(also in {seen[req_id]})"
                )
                issues += 1
            else:
                seen[req_id] = rel_path
            block_text = "\n".join(block["lines"])
            missing_fields = [
                name
                for name, pattern in FIELD_PATTERNS.items()
                if not pattern.search(block_text)
            ]
            if missing_fields:
                print(
                    f"! Missing fields for {req_id} in {rel_path}: "
                    f"{', '.join(missing_fields)}"
                )
                issues += 1
            if FIELD_PATTERNS["Acceptance Criteria"].search(block_text):
                if not CHECKBOX_RE.search(block_text):
                    print(
                        f"! Acceptance Criteria has no checkboxes for {req_id} "
                        f"in {rel_path}"
                    )
                    issues += 1
    print(f"Requirement check: {issues} issue(s)")
    return issues


def status_report(root: str) -> int:
    issues = 0
    components_path = os.path.join(root, "03_MANAGEMENT", "COMPONENTS.md")
    status_path = os.path.join(root, "03_MANAGEMENT", "STATUS.md")
    tasks_dir = os.path.join(root, "03_MANAGEMENT", "tasks")

    sections = {}
    if os.path.exists(components_path):
        current_section = None
        for line in read_text(components_path).splitlines():
            if line.startswith("## "):
                current_section = line[3:].strip()
                continue
            if line.startswith("- ") and current_section:
                item = line[2:].strip()
                if item and item != "(none)":
                    sections.setdefault(current_section, []).append(item)
    else:
        print(f"! Missing components file: {components_path}")
        issues += 1

    seen = {}
    for section, items in sections.items():
        for item in items:
            if item in seen:
                print(
                    f"! Component listed in multiple sections: {item} "
                    f"({seen[item]} and {section})"
                )
                issues += 1
            else:
                seen[item] = section

    if os.path.exists(status_path):
        status_text = read_text(status_path)
        if not re.search(r"^\s*-\s*\[[ xX]\]", status_text, re.M):
            print(f"! No checkboxes found in {status_path}")
            issues += 1
    else:
        print(f"! Missing status file: {status_path}")
        issues += 1

    task_count = 0
    if os.path.isdir(tasks_dir):
        for name in os.listdir(tasks_dir):
            if name.lower().endswith(".md") and name.lower() != "readme.md":
                task_count += 1

    print(
        "Status report: "
        f"{sum(len(items) for items in sections.values())} component(s), "
        f"{task_count} task file(s)"
    )
    return issues


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="MemoryAtlas init/update tool.")
    parser.add_argument(
        "--migrate",
        action="store_true",
        help="Archive legacy files and refresh system templates.",
    )
    parser.add_argument(
        "--update",
        action="store_true",
        help="Run init/update even when using checks.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate structure and required files.",
    )
    parser.add_argument(
        "--lint",
        action="store_true",
        help="Check metadata headers in key documents.",
    )
    parser.add_argument(
        "--links",
        action="store_true",
        help="Validate relative links in .memory docs.",
    )
    parser.add_argument(
        "--req",
        action="store_true",
        help="Validate requirement blocks in 02_SERVICES.",
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Summarize status files and detect duplicates.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without writing.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run_checks = any([args.check, args.lint, args.links, args.req, args.status])
    run_update = args.update or args.migrate or not run_checks

    if run_update:
        init_or_update(dry_run=args.dry_run)
        if args.migrate:
            smart_merge(ROOT_DIR, dry_run=args.dry_run)

    if args.check:
        check_structure(ROOT_DIR)
    if args.lint:
        lint_metadata(ROOT_DIR)
    if args.links:
        check_links(ROOT_DIR)
    if args.req:
        check_requirements(ROOT_DIR)
    if args.status:
        status_report(ROOT_DIR)
