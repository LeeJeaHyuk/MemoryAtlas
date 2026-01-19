import argparse
import os
import re
import shutil

CURRENT_VERSION = "2.0.0"
ROOT_DIR = ".memory"

# ============================================================================
# NEW STRUCTURE (v2.0)
# ============================================================================
# .memory/
# ├── 00_SYSTEM/                  # 시스템 관리 (건드리지 않음)
# ├── 01_PROJECT_CONTEXT/         # [프로젝트 헌법]
# │   ├── 00_GOALS.md
# │   └── 01_CONVENTIONS.md
# ├── 02_REQUIREMENTS/            # [WHAT: 사용자의 영역]
# │   ├── features/
# │   └── business_rules/
# ├── 03_TECH_SPECS/              # [HOW: 개발자의 영역]
# │   ├── architecture/
# │   ├── api_specs/
# │   └── decisions/
# ├── 04_TASK_LOGS/               # [HISTORY: 관리자의 영역]
# │   ├── active/
# │   └── archive/
# └── 98_KNOWLEDGE/               # [ASSET: 배운 점]
#     └── troubleshooting/
# ============================================================================

DIRS = [
    "00_SYSTEM/scripts",
    "01_PROJECT_CONTEXT",
    "02_REQUIREMENTS/features",
    "02_REQUIREMENTS/business_rules",
    "03_TECH_SPECS/architecture",
    "03_TECH_SPECS/api_specs",
    "03_TECH_SPECS/decisions",
    "04_TASK_LOGS/active",
    "04_TASK_LOGS/archive",
    "98_KNOWLEDGE/troubleshooting",
    "99_ARCHIVE",
]

DOC_TEMPLATES = {
    # =========================================================================
    # ROOT INDEX
    # =========================================================================
    "00_INDEX.md": """# Project Memory Index

> Entry point for Memory-Driven Development in this repo.
> **Version**: 2.0 (What-How-Log + Knowledge)

## Quick Navigation

| Folder | Purpose | When to Use |
|--------|---------|-------------|
| `01_PROJECT_CONTEXT/` | 프로젝트 헌법 (목표, 컨벤션) | 프로젝트 시작 시 한 번 정의 |
| `02_REQUIREMENTS/` | 기능 명세 & 비즈니스 규칙 | 새 기능 정의 시 |
| `03_TECH_SPECS/` | 기술 설계 & 의사결정 | 구현 방법 설계 시 |
| `04_TASK_LOGS/` | 작업 기록 (진행/완료) | 작업 추적 시 |
| `98_KNOWLEDGE/` | 배운 점, 트러블슈팅 | 지식 축적 시 |

## Start Here (For AI Agents)
1. Read `01_PROJECT_CONTEXT/00_GOALS.md` to understand project purpose.
2. Check `01_PROJECT_CONTEXT/01_CONVENTIONS.md` for coding rules.
3. Review `04_TASK_LOGS/active/` for current work.
4. Consult `98_KNOWLEDGE/` before implementing complex features.

## Document Map

### 01_PROJECT_CONTEXT (프로젝트 헌법)
- [00_GOALS.md](01_PROJECT_CONTEXT/00_GOALS.md) - 프로젝트 목표, 타겟 유저
- [01_CONVENTIONS.md](01_PROJECT_CONTEXT/01_CONVENTIONS.md) - 코딩 컨벤션, 네이밍 규칙

### 02_REQUIREMENTS (요구사항 - WHAT)
- [features/](02_REQUIREMENTS/features/) - 개별 기능 정의서
- [business_rules/](02_REQUIREMENTS/business_rules/) - 비즈니스 로직/공식

### 03_TECH_SPECS (기술 설계 - HOW)
- [architecture/](03_TECH_SPECS/architecture/) - DB 스키마, 전체 구조도
- [api_specs/](03_TECH_SPECS/api_specs/) - 모듈별 입출력 명세
- [decisions/](03_TECH_SPECS/decisions/) - 기술적 의사결정 (ADR)

### 04_TASK_LOGS (작업 기록 - HISTORY)
- [active/](04_TASK_LOGS/active/) - 현재 작업 중
- [archive/](04_TASK_LOGS/archive/) - 완료된 작업

### 98_KNOWLEDGE (지식 저장소 - ASSET)
- [troubleshooting/](98_KNOWLEDGE/troubleshooting/) - 해결된 난제들, 라이브러리 팁
""",

    # =========================================================================
    # 01_PROJECT_CONTEXT - 프로젝트 헌법
    # =========================================================================
    "01_PROJECT_CONTEXT/00_GOALS.md": """# Project Goals

> **ID**: CTX-GOALS-001
> **Last Updated**: (TBD)

---

## 1. Project Identity

### Name
(프로젝트 이름)

### One-Line Summary
(프로젝트를 한 문장으로 설명)

### Core Value
(이 시스템이 존재하는 이유, 어떤 가치를 제공하는가?)

---

## 2. Target Users
(누구를 위한 프로젝트인가?)

- **Primary**: (주요 사용자)
- **Secondary**: (부가 사용자)

---

## 3. Success Criteria
(프로젝트 성공의 기준은 무엇인가?)

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

---

## 4. Scope

### In-Scope
- (포함되는 기능/범위)

### Out-of-Scope
- (명시적으로 제외되는 것들)

---

## 5. Milestones

| Phase | Description | Target Date | Status |
|-------|-------------|-------------|--------|
| Phase 1 | MVP | TBD | ⬜ Not Started |
| Phase 2 | Core Features | TBD | ⬜ Not Started |
| Phase 3 | Hardening | TBD | ⬜ Not Started |
""",

    "01_PROJECT_CONTEXT/01_CONVENTIONS.md": """# Coding Conventions & Rules

> **ID**: CTX-CONV-001
> **Last Updated**: (TBD)

---

## 1. Naming Conventions

### Variables & Functions
- Style: `snake_case`
- Example: `user_name`, `get_user_data()`

### Classes
- Style: `PascalCase`
- Example: `UserManager`, `DataProcessor`

### Constants
- Style: `UPPER_SNAKE_CASE`
- Example: `MAX_RETRY_COUNT`, `DEFAULT_TIMEOUT`

### Files & Directories
- Style: `lowercase_with_underscores`
- Example: `user_service.py`, `data_models/`

---

## 2. Code Style

### Language-Specific Rules

#### Python
- Formatter: `black`
- Linter: `ruff` or `flake8`
- Type hints: Required for public functions
- Docstrings: Google style

#### JavaScript/TypeScript
- Formatter: `prettier`
- Linter: `eslint`

---

## 3. Git Conventions

### Branch Naming
- Feature: `feature/short-description`
- Bugfix: `fix/issue-description`
- Hotfix: `hotfix/critical-fix`

### Commit Messages
```
<type>(<scope>): <subject>

<body>
```
- Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`

---

## 4. Universal Constraints

### Performance
- (예: 응답 시간은 1초 이내)

### Data
- (예: 모든 시간은 UTC로 저장)

### Security
- (예: 비밀번호는 bcrypt로 해싱)

---

## 5. Documentation Rules

### Required for Every Feature
- [ ] Description in `02_REQUIREMENTS/features/`
- [ ] API spec in `03_TECH_SPECS/api_specs/`
- [ ] Test coverage

### AI Agent Instructions
- **Before coding**: Read `01_CONVENTIONS.md` first
- **After coding**: Update relevant docs in `02_REQUIREMENTS/`
""",

    # =========================================================================
    # 02_REQUIREMENTS - 요구사항 (WHAT)
    # =========================================================================
    "02_REQUIREMENTS/README.md": """# Requirements (WHAT)

> 이 폴더는 **"무엇을 만들 것인가?"**를 정의합니다.
> 기능(Feature)과 비즈니스 규칙(Business Rule)을 분리하여 관리합니다.

## Structure

```
02_REQUIREMENTS/
├── features/           # 개별 기능 명세
│   └── REQ-XXX-*.md    # 기능별 문서
└── business_rules/     # 비즈니스 로직/공식
    └── RULE-XXX-*.md   # 규칙별 문서
```

## Why Separate?
- **Features**: "뉴스를 크롤링한다", "DB에 저장한다" 같은 동작
- **Business Rules**: "응답 속도는 1초 이내", "모든 시간은 UTC" 같은 제약

AI가 기능 구현에 집중하다가 규칙을 놓치지 않도록 분리합니다.

## Naming Convention
- Features: `REQ-[DOMAIN]-[NUMBER].md` (예: `REQ-AUTH-001.md`)
- Rules: `RULE-[DOMAIN]-[NUMBER].md` (예: `RULE-DATA-001.md`)
""",

    "02_REQUIREMENTS/features/README.md": """# Feature Requirements

> 개별 기능 명세를 이곳에 저장합니다.

## Template
```markdown
# [REQ-XXX-001] Feature Name

> **ID**: REQ-XXX-001
> **Domain**: (도메인)
> **Status**: [Draft | Active | Deprecated]
> **Last Updated**: YYYY-MM-DD

---

## Description
(기능에 대한 명확한 설명)

## Input
- `param1` (type): description

## Output
- `result` (type): description

## Logic/Rules
1. First rule
2. Second rule

## Acceptance Criteria
- [ ] Feature implemented
- [ ] Edge cases handled
- [ ] Tests passing

## Related Documents
- [Architecture](../../03_TECH_SPECS/architecture/)
- [API Spec](../../03_TECH_SPECS/api_specs/)
```
""",

    "02_REQUIREMENTS/business_rules/README.md": """# Business Rules

> 비즈니스 로직, 공식, 변하지 않는 규칙을 이곳에 저장합니다.
> 모든 기능 구현 시 이 규칙들을 **반드시** 준수해야 합니다.

## Template
```markdown
# [RULE-XXX-001] Rule Name

> **ID**: RULE-XXX-001
> **Domain**: (도메인)
> **Priority**: [Critical | High | Medium | Low]
> **Last Updated**: YYYY-MM-DD

---

## Rule Statement
(규칙을 명확하게 한 문장으로)

## Rationale
(왜 이 규칙이 필요한가?)

## Examples
### ✅ Correct
(올바른 예시)

### ❌ Incorrect
(잘못된 예시)

## Exceptions
(예외 상황이 있다면)
```

## Common Categories
- **DATA**: 데이터 형식, 저장 규칙
- **PERF**: 성능 제약
- **SEC**: 보안 규칙
- **UX**: 사용자 경험 규칙
""",

    # =========================================================================
    # 03_TECH_SPECS - 기술 설계 (HOW)
    # =========================================================================
    "03_TECH_SPECS/README.md": """# Technical Specifications (HOW)

> 이 폴더는 **"어떻게 만들 것인가?"**를 정의합니다.
> 구조(Architecture), 인터페이스(API), 의사결정(Decisions)을 분리합니다.

## Structure

```
03_TECH_SPECS/
├── architecture/       # 구조도, DB 스키마 (비교적 덜 변함)
├── api_specs/          # 입출력 명세 (자주 변함)
└── decisions/          # 기술적 의사결정 기록 (ADR)
```

## Why This Structure?
- **Architecture**: 전체 그림. 자주 바뀌지 않음.
- **API Specs**: 구현 세부사항. 자주 바뀜.
- **Decisions**: "왜 이렇게 했는가?" 기록. 나중에 후회하지 않기 위해.
""",

    "03_TECH_SPECS/architecture/README.md": """# Architecture Documents

> 시스템 구조도, DB 스키마(ERD), 데이터 흐름도를 이곳에 저장합니다.

## Template: System Architecture
```markdown
# System Architecture

> **Last Updated**: YYYY-MM-DD

---

## High-Level Diagram
(ASCII 다이어그램 또는 이미지 링크)

## Components
| Component | Responsibility | Technology |
|-----------|---------------|------------|
| Frontend | UI | React |
| Backend | API | FastAPI |
| Database | Storage | PostgreSQL |

## Data Flow
1. User → Frontend
2. Frontend → Backend API
3. Backend → Database
```

## Template: Database Schema
```markdown
# Database Schema

> **Last Updated**: YYYY-MM-DD

---

## ERD
(ERD 다이어그램)

## Tables

### users
| Column | Type | Constraints |
|--------|------|-------------|
| id | UUID | PK |
| email | VARCHAR(255) | UNIQUE, NOT NULL |
| created_at | TIMESTAMP | NOT NULL |

### 다른 테이블...
```
""",

    "03_TECH_SPECS/api_specs/README.md": """# API Specifications

> 모듈별 입출력 명세를 이곳에 저장합니다.

## Template
```markdown
# [Module Name] API Specification

> **Module**: (모듈명)
> **Last Updated**: YYYY-MM-DD

---

## Endpoints / Functions

### `GET /api/users/{id}`
- **Description**: 사용자 정보 조회
- **Path Parameters**:
  - `id` (UUID): 사용자 ID
- **Response**:
```json
{
  "id": "uuid",
  "email": "string",
  "created_at": "datetime"
}
```
- **Error Codes**:
  - `404`: User not found
  - `500`: Internal server error

### `function_name(param1, param2) -> ReturnType`
- **Description**: 함수 설명
- **Parameters**:
  - `param1` (Type): 설명
  - `param2` (Type): 설명
- **Returns**: ReturnType 설명
- **Raises**: 예외 상황
```
""",

    "03_TECH_SPECS/decisions/README.md": """# Architecture Decision Records (ADR)

> 기술적 의사결정을 기록합니다.
> "왜 MongoDB 대신 PostgreSQL을 썼는가?"에 대한 답을 남깁니다.

## Why ADR?
구조를 뒤집을 때, 이 기록을 보지 않으면 **같은 실수를 반복**합니다.

## Template
```markdown
# ADR-001: [Decision Title]

> **Status**: [Proposed | Accepted | Deprecated | Superseded]
> **Date**: YYYY-MM-DD
> **Deciders**: (결정자)

---

## Context
(문제 상황을 설명)

## Decision
(무엇을 결정했는가?)

## Alternatives Considered
### Option A: (대안 1)
- Pros: ...
- Cons: ...

### Option B: (대안 2)
- Pros: ...
- Cons: ...

## Consequences
### Positive
- ...

### Negative
- ...

## Related
- [Link to related ADR or doc]
```

## Naming Convention
- `ADR-[NUMBER]-[short-title].md`
- Example: `ADR-001-database-choice.md`
""",

    # =========================================================================
    # 04_TASK_LOGS - 작업 기록 (HISTORY)
    # =========================================================================
    "04_TASK_LOGS/README.md": """# Task Logs (HISTORY)

> 작업 기록을 관리합니다.
> 진행 중(active)과 완료(archive)를 분리합니다.

## Structure

```
04_TASK_LOGS/
├── active/             # 현재 작업 중
│   └── YYYY-MM-DD_TYPE_Description.md
└── archive/            # 완료된 작업
    └── YYYY-MM/        # 월별 정리
        └── *.md
```

## Workflow
1. **Create**: 새 작업은 `active/`에 생성
2. **Execute**: 작업 중 상태 업데이트
3. **Archive**: 완료 시 `archive/YYYY-MM/`로 이동

## Naming Convention (MANDATORY)
`[YYYY-MM-DD]_[Type]_[ShortDescription].md`

### Types
| Type | Description |
|------|-------------|
| `FEAT` | 새 기능 |
| `FIX` | 버그 수정 |
| `DOCS` | 문서화 |
| `REFACTOR` | 코드 정리 |
| `MAINT` | 유지보수 |

### Examples
- `2024-01-16_FEAT_UserLogin.md`
- `2024-01-17_FIX_MemoryLeak.md`
""",

    "04_TASK_LOGS/active/README.md": """# Active Tasks

> 현재 진행 중인 작업을 이곳에 저장합니다.

## Template
```markdown
# [Task Title]

> **Status**: [Active | OnHold | Blocked]
> **Type**: [FEAT | FIX | DOCS | REFACTOR | MAINT]
> **Owner**: (담당자)
> **Started**: YYYY-MM-DD

---

## Objective
(이 작업의 목표)

## Progress Log
### YYYY-MM-DD
- [ ] Step 1
- [ ] Step 2

## Blockers
(막힌 부분이 있다면)

## Related
- [Requirement](../../02_REQUIREMENTS/features/)
- [Tech Spec](../../03_TECH_SPECS/)
```
""",

    "04_TASK_LOGS/archive/README.md": """# Archived Tasks

> 완료된 작업을 이곳에 저장합니다.
> 월별로 정리합니다: `YYYY-MM/`

## Structure
```
archive/
├── 2024-01/
│   ├── 2024-01-15_FEAT_Login.md
│   └── 2024-01-20_FIX_Auth.md
├── 2024-02/
│   └── ...
```

## Completed Task Template
```markdown
# [Task Title]

> **Status**: [x] Completed
> **Type**: [FEAT | FIX | DOCS | REFACTOR | MAINT]
> **Owner**: (담당자)
> **Started**: YYYY-MM-DD
> **Completed**: YYYY-MM-DD

---

## Summary
(무엇을 완료했는가?)

## Key Learnings
(배운 점이 있다면 → 98_KNOWLEDGE로 추출 고려)

## Related Commits
- `abc1234`: commit message
```
""",

    # =========================================================================
    # 98_KNOWLEDGE - 지식 저장소 (ASSET)
    # =========================================================================
    "98_KNOWLEDGE/README.md": """# Knowledge Base (ASSET)

> 프로젝트를 진행하면서 배운 **"일반적인 지식"**을 저장합니다.
> Task Log에 있는 지식을 추출하여 재사용 가능하게 만듭니다.

## Why This Folder?
- Task Log에 "파이썬 asyncio 에러 해결법"을 적어두면, 나중에 로그가 쌓여서 **검색이 안 됩니다**.
- 배운 점을 별도로 저장해야 **과거의 실수를 반복하지 않습니다**.

## Structure
```
98_KNOWLEDGE/
├── troubleshooting/    # 해결된 난제들
│   └── [topic]/        # 주제별 분류
└── [other_topics]/     # 필요에 따라 추가
```

## Usage for AI Agents
"KNOWLEDGE 폴더를 참고해서 코드를 짜"라고 하면,
과거의 경험을 바탕으로 더 나은 코드를 작성합니다.
""",

    "98_KNOWLEDGE/troubleshooting/README.md": """# Troubleshooting Guide

> 해결된 난제들, 라이브러리 사용 팁을 이곳에 저장합니다.

## Template
```markdown
# [Issue Title]

> **Category**: [Python | JavaScript | Database | DevOps | ...]
> **Date Discovered**: YYYY-MM-DD
> **Related Task**: [Link to original task log]

---

## Problem
(문제 상황 설명)

## Root Cause
(원인 분석)

## Solution
(해결 방법)

```code
# 해결 코드 예시
```

## Prevention
(다시 발생하지 않으려면?)

## References
- [Link to documentation]
- [Link to Stack Overflow]
```

## Folder Structure Example
```
troubleshooting/
├── python/
│   ├── asyncio_pitfalls.md
│   └── import_errors.md
├── database/
│   └── connection_pool.md
└── devops/
    └── docker_networking.md
```
""",

    # =========================================================================
    # 00_SYSTEM - 시스템 관리
    # =========================================================================
    "00_SYSTEM/README.md": """# System Management

> [!WARNING] **DO NOT MODIFY**
> 이 폴더는 MemoryAtlas 시스템 파일입니다.
> `memory_manager.py`에 의해 관리됩니다.

## Contents
- `AGENT_RULES.md`: AI 에이전트 행동 규칙
- `scripts/`: 시스템 스크립트
""",
}

# ============================================================================
# SYSTEM TEMPLATES (Managed by memory_manager.py)
# ============================================================================
AGENT_RULES_TEMPLATE = """# MemoryAtlas Agent Rules (v2.0)

> **SYSTEM FILE**: This file is managed by `memory_manager.py`.
> **DO NOT EDIT**: Changes made here will be overwritten by the system update.

This document defines the **STRICT BEHAVIORAL PROTOCOLS** for any AI Agent working on this project.

---

## 1. Core Philosophy
You are an intelligent operator of the **MemoryAtlas v2.0** documentation system.
Your goal is to keep the documentation (`.memory/`) in perfect sync with the codebase.

**Structure Overview**:
- `01_PROJECT_CONTEXT/`: 프로젝트 헌법 (목표, 규칙)
- `02_REQUIREMENTS/`: 요구사항 (WHAT)
- `03_TECH_SPECS/`: 기술 설계 (HOW)
- `04_TASK_LOGS/`: 작업 기록 (HISTORY)
- `98_KNOWLEDGE/`: 지식 저장소 (ASSET)

---

## 2. Universal Constraints
<constraints>
    <rule id="NO_SYSTEM_MODIFICATION">
        You must NEVER modify files in `.memory/00_SYSTEM/`.
        These are system-locked files.
    </rule>

    <rule id="CONTEXT_FIRST_APPROACH">
        Before generating any code, you MUST read:
        1. `.memory/00_INDEX.md` - 전체 구조 파악
        2. `.memory/01_PROJECT_CONTEXT/01_CONVENTIONS.md` - 코딩 규칙 확인
        3. `.memory/02_REQUIREMENTS/business_rules/` - 비즈니스 규칙 확인
    </rule>

    <rule id="KNOWLEDGE_FIRST">
        Before implementing complex features, check `.memory/98_KNOWLEDGE/` 
        for past solutions and pitfalls.
    </rule>

    <rule id="DOCUMENTATION_SYNCHRONIZATION">
        <trigger>Any modification to business logic or functional code</trigger>
        <action>
            Immediately update the corresponding requirement file in `.memory/02_REQUIREMENTS/`.
            If the file does not exist, create it following the standard template.
        </action>
    </rule>
</constraints>

---

## 3. Directory Authority Protocol
<directory_protocol>
    <dir path=".memory/00_SYSTEM">
        <access>READ_ONLY</access>
        <description>System files. Never modify.</description>
    </dir>
    <dir path=".memory/01_PROJECT_CONTEXT">
        <access>READ_MOSTLY</access>
        <description>Project constitution. Modify only for major changes.</description>
    </dir>
    <dir path=".memory/02_REQUIREMENTS">
        <access>READ_WRITE</access>
        <description>Living requirements. Update aggressively.</description>
    </dir>
    <dir path=".memory/03_TECH_SPECS">
        <access>READ_WRITE</access>
        <description>Technical specs. Keep in sync with code.</description>
    </dir>
    <dir path=".memory/04_TASK_LOGS">
        <access>READ_WRITE</access>
        <description>Task tracking. Create/update/archive tasks.</description>
    </dir>
    <dir path=".memory/98_KNOWLEDGE">
        <access>READ_WRITE</access>
        <description>Knowledge base. Extract learnings from completed tasks.</description>
    </dir>
</directory_protocol>

---

## 4. Standard Workflows

### Protocol A: Starting a New Task
**User Command**: "Check memory, plan [Feature], and execute."
**Agent Steps**:
1. **Context Check**: Read `00_INDEX.md`, `01_CONVENTIONS.md`, `business_rules/`
2. **Knowledge Check**: Scan `98_KNOWLEDGE/` for related past solutions
3. **Doc Update**: Create/update requirements in `02_REQUIREMENTS/features/`
4. **Task Creation**: Create task in `04_TASK_LOGS/active/`
5. **Execution**: Write code and tests
6. **Closure**: Move task to `archive/` and update `03_TECH_SPECS/` if needed

### Protocol B: Completing a Task
**Agent Steps**:
1. Move task file from `active/` to `archive/YYYY-MM/`
2. If valuable learnings exist, extract to `98_KNOWLEDGE/`
3. Update any changed APIs in `03_TECH_SPECS/api_specs/`

### Protocol C: Debugging
**Agent Steps**:
1. First check `98_KNOWLEDGE/troubleshooting/` for similar issues
2. If solved, document the solution in `98_KNOWLEDGE/troubleshooting/`
3. Link the troubleshooting doc in the task log

---

## 5. Interaction Style
- **When starting**: "I have loaded MemoryAtlas v2.0. Checking conventions and active tasks..."
- **When blocked**: "The requirement in `02_REQUIREMENTS/...` conflicts with the code. Which one is correct?"
- **When learning**: "I'll document this solution in `98_KNOWLEDGE/troubleshooting/` for future reference."
"""

SYSTEM_TEMPLATES = {
    "00_SYSTEM/AGENT_RULES.md": AGENT_RULES_TEMPLATE,
}

# ============================================================================
# MIGRATION: Old Structure → New Structure
# ============================================================================
MIGRATION_MAP = {
    # Old path → New path (or None to archive)
    "01_PROJECT_CONTEXT/00_IDENTITY.md": None,  # Content merged into 00_GOALS.md
    "01_PROJECT_CONTEXT/01_OVERVIEW.md": None,  # Content merged into 00_GOALS.md
    "01_PROJECT_CONTEXT/02_ARCHITECTURE.md": "03_TECH_SPECS/architecture/SYSTEM_ARCHITECTURE.md",
    "01_PROJECT_CONTEXT/03_DATA_MODEL.md": "03_TECH_SPECS/architecture/DATA_MODEL.md",
    "01_PROJECT_CONTEXT/04_AGENT_GUIDE.md": None,  # Replaced by AGENT_RULES.md
    "02_SERVICES": "02_REQUIREMENTS/features",  # Directory migration
    "03_MANAGEMENT/STATUS.md": "04_TASK_LOGS/STATUS.md",
    "03_MANAGEMENT/CHANGELOG.md": "04_TASK_LOGS/CHANGELOG.md",
    "03_MANAGEMENT/WORKLOG.md": None,  # Archive
    "03_MANAGEMENT/COMPONENTS.md": None,  # Archive
    "03_MANAGEMENT/MISSING_COMPONENTS.md": None,  # Archive
    "03_MANAGEMENT/tasks/active": "04_TASK_LOGS/active",
    "03_MANAGEMENT/tasks/archive": "04_TASK_LOGS/archive",
    "90_TOOLING/AGENT_RULES.md": "00_SYSTEM/AGENT_RULES.md",
    "90_TOOLING/scripts": "00_SYSTEM/scripts",
}

LEGACY_DIRS_TO_ARCHIVE = [
    "02_SERVICES",
    "03_MANAGEMENT",
    "90_TOOLING",
]

# ============================================================================
# LINT / CHECK CONFIGURATION
# ============================================================================
LINT_DIRS = ["01_PROJECT_CONTEXT", "02_REQUIREMENTS/features"]
LINK_SCAN_DIRS = ["01_PROJECT_CONTEXT", "02_REQUIREMENTS", "03_TECH_SPECS", "04_TASK_LOGS"]
REQ_SCAN_DIRS = ["02_REQUIREMENTS/features"]
LINT_SKIP_FILES = {"README.md", "00_INDEX.md"}
HEADER_FIELDS = ["**ID**", "**Last Updated**"]

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
REQ_HEADER_RE = re.compile(r"^###?\s+\[(REQ-[A-Za-z0-9_-]+)\]", re.M)
CHECKBOX_RE = re.compile(r"^\s*-\s*\[[ xX]\]", re.M)
FIELD_PATTERNS = {
    "Description": re.compile(r"^\s*-?\s*\*?\*?Description\*?\*?:", re.M | re.I),
}

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def write_file(path: str, content: str, dry_run: bool = False) -> None:
    if dry_run:
        return
    os.makedirs(os.path.dirname(path), exist_ok=True)
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
            print(f"  - Would create doc: {rel_path}")
            continue
        os.makedirs(os.path.dirname(path), exist_ok=True)
        write_file(path, content)
        print(f"  + Created doc: {rel_path}")


def update_system_templates(root: str, dry_run: bool = False) -> None:
    for rel_path, content in SYSTEM_TEMPLATES.items():
        path = os.path.join(root, rel_path)
        if dry_run:
            print(f"  - Would update system file: {rel_path}")
            continue
        os.makedirs(os.path.dirname(path), exist_ok=True)
        write_file(path, content)
        print(f"  * Updated system file: {rel_path}")


def migrate_v1_to_v2(root: str, dry_run: bool = False) -> None:
    """Migrate from v1.x structure to v2.0 structure."""
    archive_dir = os.path.join(root, "99_ARCHIVE", "v1_migration")
    
    print("\n=== Migrating v1.x → v2.0 ===")
    
    # 1. Migrate individual files
    for old_rel, new_rel in MIGRATION_MAP.items():
        old_path = os.path.join(root, old_rel)
        
        if not os.path.exists(old_path):
            continue
            
        if new_rel is None:
            # Archive the file
            archive_path = os.path.join(archive_dir, old_rel)
            if dry_run:
                print(f"  - Would archive: {old_rel}")
            else:
                os.makedirs(os.path.dirname(archive_path), exist_ok=True)
                if os.path.isdir(old_path):
                    if os.path.exists(archive_path):
                        shutil.rmtree(archive_path)
                    shutil.copytree(old_path, archive_path)
                else:
                    shutil.copy2(old_path, archive_path)
                print(f"  * Archived: {old_rel}")
        else:
            # Move to new location
            new_path = os.path.join(root, new_rel)
            if dry_run:
                print(f"  - Would move: {old_rel} → {new_rel}")
            else:
                os.makedirs(os.path.dirname(new_path), exist_ok=True)
                if os.path.isdir(old_path):
                    if not os.path.exists(new_path):
                        shutil.copytree(old_path, new_path)
                elif not os.path.exists(new_path):
                    shutil.copy2(old_path, new_path)
                print(f"  * Moved: {old_rel} → {new_rel}")
    
    # 2. Archive and remove legacy directories
    for legacy_dir in LEGACY_DIRS_TO_ARCHIVE:
        legacy_path = os.path.join(root, legacy_dir)
        if os.path.isdir(legacy_path):
            archive_path = os.path.join(archive_dir, legacy_dir)
            if dry_run:
                print(f"  - Would archive directory: {legacy_dir}")
            else:
                if not os.path.exists(archive_path):
                    shutil.copytree(legacy_path, archive_path)
                shutil.rmtree(legacy_path)
                print(f"  * Archived and removed: {legacy_dir}")


def update_tooling(root: str, dry_run: bool = False) -> None:
    src = os.path.abspath(__file__)
    dest = os.path.join(root, "00_SYSTEM", "scripts", "memory_manager.py")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    if os.path.abspath(src) != os.path.abspath(dest):
        if dry_run:
            print(f"  - Would update tool: {dest}")
            return
        shutil.copyfile(src, dest)
        print(f"  * Updated tool: 00_SYSTEM/scripts/memory_manager.py")


def read_version(root: str) -> str:
    version_file = os.path.join(root, "VERSION")
    if not os.path.exists(version_file):
        return "0.0.0"
    with open(version_file, "r", encoding="utf-8") as f:
        return f.read().strip()


def write_version(root: str, dry_run: bool = False) -> None:
    version_file = os.path.join(root, "VERSION")
    if dry_run:
        print(f"  - Would update version to: {CURRENT_VERSION}")
        return
    write_file(version_file, CURRENT_VERSION)


def is_v1_structure(root: str) -> bool:
    """Check if the current structure is v1.x"""
    v1_markers = [
        os.path.join(root, "02_SERVICES"),
        os.path.join(root, "03_MANAGEMENT"),
        os.path.join(root, "90_TOOLING"),
    ]
    return any(os.path.exists(m) for m in v1_markers)


def init_or_update(dry_run: bool = False, force_migrate: bool = False) -> None:
    installed_version = read_version(ROOT_DIR)
    print(
        f"Checking Memory System: Installed({installed_version}) "
        f"vs Current({CURRENT_VERSION})"
    )
    
    # Check if migration is needed
    needs_migration = force_migrate or (
        installed_version.startswith("1.") and is_v1_structure(ROOT_DIR)
    )
    
    if needs_migration:
        print("\n[!] Detected v1.x structure. Migration required.")
        migrate_v1_to_v2(ROOT_DIR, dry_run=dry_run)
    
    ensure_structure(ROOT_DIR)
    create_missing_docs(ROOT_DIR, dry_run=dry_run)
    update_system_templates(ROOT_DIR, dry_run=dry_run)
    update_tooling(ROOT_DIR, dry_run=dry_run)

    if installed_version != CURRENT_VERSION:
        write_version(ROOT_DIR, dry_run=dry_run)
        if dry_run:
            print(f"\nWould update to v{CURRENT_VERSION}")
        else:
            print(f"\n[OK] Updated to v{CURRENT_VERSION}")
    else:
        print("\n[OK] Already up to date.")


# ============================================================================
# VALIDATION FUNCTIONS
# ============================================================================

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
            print(f"! Missing directory: {folder}")
            issues += 1

    required_files = set(DOC_TEMPLATES.keys())
    required_files.add("VERSION")
    required_files.update(SYSTEM_TEMPLATES.keys())

    for rel_path in sorted(required_files):
        path = os.path.join(root, rel_path)
        if not os.path.exists(path):
            print(f"! Missing file: {rel_path}")
            issues += 1

    installed_version = read_version(root)
    if installed_version != CURRENT_VERSION:
        print(
            f"! Version mismatch: installed {installed_version} "
            f"vs current {CURRENT_VERSION}"
        )
        issues += 1

    print(f"\nStructure check: {issues} issue(s)")
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


def check_requirements(root: str) -> int:
    issues = 0
    seen = {}
    for path in iter_md_files(root, REQ_SCAN_DIRS):
        text = read_text(path)
        for match in REQ_HEADER_RE.finditer(text):
            req_id = match.group(1)
            rel_path = os.path.relpath(path, root)
            if req_id in seen:
                print(
                    f"! Duplicate requirement ID {req_id} in {rel_path} "
                    f"(also in {seen[req_id]})"
                )
                issues += 1
            else:
                seen[req_id] = rel_path
    print(f"Requirement check: {issues} issue(s)")
    return issues


def status_report(root: str) -> int:
    """Report on active tasks and knowledge base."""
    print("\n=== Status Report ===")
    
    # Count active tasks
    active_dir = os.path.join(root, "04_TASK_LOGS", "active")
    active_count = 0
    if os.path.isdir(active_dir):
        for f in os.listdir(active_dir):
            if f.endswith(".md") and f != "README.md":
                active_count += 1
    
    # Count archived tasks
    archive_dir = os.path.join(root, "04_TASK_LOGS", "archive")
    archive_count = 0
    if os.path.isdir(archive_dir):
        for root_dir, dirs, files in os.walk(archive_dir):
            for f in files:
                if f.endswith(".md") and f != "README.md":
                    archive_count += 1
    
    # Count knowledge articles
    knowledge_dir = os.path.join(root, "98_KNOWLEDGE")
    knowledge_count = 0
    if os.path.isdir(knowledge_dir):
        for root_dir, dirs, files in os.walk(knowledge_dir):
            for f in files:
                if f.endswith(".md") and f != "README.md":
                    knowledge_count += 1
    
    # Count requirements
    req_dir = os.path.join(root, "02_REQUIREMENTS", "features")
    req_count = 0
    if os.path.isdir(req_dir):
        for f in os.listdir(req_dir):
            if f.endswith(".md") and f != "README.md":
                req_count += 1
    
    print(f"  [Active Tasks]: {active_count}")
    print(f"  [Archived Tasks]: {archive_count}")
    print(f"  [Requirements]: {req_count}")
    print(f"  [Knowledge Articles]: {knowledge_count}")
    
    return 0


# ============================================================================
# MAIN
# ============================================================================

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="MemoryAtlas v2.0 - Memory-Driven Development Tool"
    )
    parser.add_argument(
        "--migrate",
        action="store_true",
        help="Force migration from v1.x to v2.0 structure.",
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
        help="Validate requirement blocks in 02_REQUIREMENTS.",
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Show status report of tasks and knowledge.",
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
        init_or_update(dry_run=args.dry_run, force_migrate=args.migrate)

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
