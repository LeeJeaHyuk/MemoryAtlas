import os

TEMPLATES = {
    "00_INDEX.md": """# Project Memory Index\n\n> Entry point for Memory-Driven Development in this repo.\n\n## Start Here\n- Read 01_PROJECT_CONTEXT to understand goals and architecture.\n- Check 03_MANAGEMENT for current status and gaps.\n- Use 02_SERVICES for feature-level requirements and specs.\n\n## Context\n- 01_PROJECT_CONTEXT/01_OVERVIEW.md\n- 01_PROJECT_CONTEXT/02_ARCHITECTURE.md\n- 01_PROJECT_CONTEXT/03_DATA_MODEL.md\n- 01_PROJECT_CONTEXT/04_AGENT_GUIDE.md\n\n## Services\n- 02_SERVICES/README.md\n\n## Management\n- 03_MANAGEMENT/STATUS.md\n- 03_MANAGEMENT/COMPONENTS.md\n- 03_MANAGEMENT/MISSING_COMPONENTS.md\n- 03_MANAGEMENT/tasks/\n""",
    "01_PROJECT_CONTEXT/01_OVERVIEW.md": """# Project Overview\n\n## Goal\nDescribe the primary outcome and value delivered by this project.\n\n## Scope\nList the in-scope capabilities and explicit exclusions.\n\n## Stakeholders\nIdentify owners, users, and decision makers.\n""",
    "01_PROJECT_CONTEXT/02_ARCHITECTURE.md": """# System Architecture\n\n## High-Level Diagram\nDescribe components and data flow.\n\n## Key Decisions\nRecord architectural choices and trade-offs.\n""",
    "01_PROJECT_CONTEXT/03_DATA_MODEL.md": """# Data Model\n\n## Core Entities\nList the main entities and relationships.\n\n## Invariants\nDefine rules that must always hold.\n""",
    "01_PROJECT_CONTEXT/04_AGENT_GUIDE.md": """# Agent Guide\n\n## Source of Truth\n- Always start with 00_INDEX.md.\n- Prefer .memory documents over ad-hoc assumptions.\n\n## Update Rules\n- Update 02_SERVICES when requirements or specs change.\n- Update 01_PROJECT_CONTEXT when architecture or scope changes.\n- Update 03_MANAGEMENT after implementing or deferring work.\n""",
    "02_SERVICES/README.md": """# Services Index\n\nThis folder is intentionally project-specific.\nCreate subfolders for your domains (e.g., FRONTEND, BACKEND_API, INFRA).\nEach service should have a short spec and interfaces listed.\n""",
    "03_MANAGEMENT/STATUS.md": """# Implementation Status\n\n## Phases\n- [ ] Phase 1: Setup\n- [ ] Phase 2: Core Features\n- [ ] Phase 3: Hardening\n\n## Current Focus\nList the short-term targets and active milestones.\n""",
    "03_MANAGEMENT/COMPONENTS.md": """# Component Matrix\n\n## Implemented\n- (none)\n\n## In Progress\n- (none)\n\n## Not Started\n- (none)\n\n## Deprecated\n- (none)\n""",
    "03_MANAGEMENT/MISSING_COMPONENTS.md": """# Missing Components\n\nTrack gaps that block requirements or tests.\n- (none)\n""",
    "03_MANAGEMENT/tasks/README.md": """# Tasks\n\nUse one file per task or sprint. Keep tasks small and actionable.\n""",
}

FOLDERS = [
    "01_PROJECT_CONTEXT",
    "02_SERVICES",
    "03_MANAGEMENT/tasks",
    "90_TOOLING/scripts",
    "99_ARCHIVE",
]


def create_file(path: str, content: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def init_memory_structure(root: str = ".memory") -> None:
    print(f"Initializing memory structure in '{root}'...")

    for folder in FOLDERS:
        path = os.path.join(root, folder)
        os.makedirs(path, exist_ok=True)
        print(f"  + directory: {path}")

    for rel_path, content in TEMPLATES.items():
        path = os.path.join(root, rel_path)
        if os.path.exists(path):
            print(f"  - skipped (exists): {path}")
            continue
        create_file(path, content)
        print(f"  + file: {path}")

    print("Done. Update 02_SERVICES to match your project domain.")


if __name__ == "__main__":
    init_memory_structure()
