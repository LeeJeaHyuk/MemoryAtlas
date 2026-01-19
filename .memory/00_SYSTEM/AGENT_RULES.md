# MemoryAtlas Agent Rules (v2.0)

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
