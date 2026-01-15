# MemoryAtlas Agent Rules

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
