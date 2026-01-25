# [RULE-DIR-001] Memory Directory Structure

> **ID**: RULE-DIR-001
> **Domain**: STRUCTURE
> **Priority**: Critical
> **Last Updated**: 2026-01-22
> **Must-Read**: RULE-ID-001
> **Template-Version**: 3.3

---

## Rule Statement (최종 결정)

`.memory/` 폴더는 정해진 16개의 필수 하위 디렉토리를 포함해야 하며, 이 구조는 MemoryAtlas 시스템이 정상 작동하기 위한 최소 요구사항이다.

---

## Rationale

**Source**: `src/core/config.py:31-45`

```python
DIRS = [
    "00_SYSTEM/scripts",
    "00_SYSTEM/mcp",
    "00_SYSTEM/mcp/templates",
    "00_SYSTEM/state",
    "01_PROJECT_CONTEXT",
    "02_REQUIREMENTS/capabilities",
    "02_REQUIREMENTS/invariants",
    "02_REQUIREMENTS/discussions",
    "03_TECH_SPECS/architecture",
    "03_TECH_SPECS/api_specs",
    "03_TECH_SPECS/decisions",
    "04_TASK_LOGS/active",
    "04_TASK_LOGS/archive",
    "98_KNOWLEDGE/troubleshooting",
    "99_ARCHIVE",
    "99_ARCHIVE/discussions",
]
```

이 구조는 **Authority Model**(WHAT → HOW → LOG)을 강제하며, 문서 자동 검증(`--doctor`)의 기반이 된다.

---

## Required Directory Structure

```
.memory/
  00_SYSTEM/
    scripts/              # System scripts (memory_manager.py copy)
    mcp/                  # MCP definitions (auto-generated)
      templates/          # Client config templates
    state/                # MCP state snapshots
  01_PROJECT_CONTEXT/     # Project goals and conventions
  02_REQUIREMENTS/        # Requirements (Authority Layer)
    capabilities/         # REQ-* (capabilities)
    invariants/           # RULE-* (invariants)
    discussions/          # DISC-* (discussions)
  03_TECH_SPECS/          # Technical specs (HOW Layer)
    architecture/         # Architecture and data models
    api_specs/            # API specs
    decisions/            # ADR-* (decisions)
  04_TASK_LOGS/           # Execution logs
    active/               # RUN-* (active)
    archive/              # Completed runs (YYYY-MM/)
  98_KNOWLEDGE/           # Knowledge base
    troubleshooting/      # Troubleshooting notes
  99_ARCHIVE/             # Deprecated content
    discussions/          # Archived discussions
```

---

## Examples

### ✅ Correct Structure

```bash
$ python memory_manager.py --check
Structure check: 0 issue(s)
```

모든 15개 디렉토리가 존재하면 통과.

### ❌ Incorrect

```
Missing directory: 02_REQUIREMENTS/features
Missing directory: 04_TASK_LOGS/active
Structure check: 2 issue(s)
```

---

## Automatic Creation

`python memory_manager.py --update` 실행 시 누락된 디렉토리를 자동 생성한다.

---

## Exceptions

없음. 모든 15개 디렉토리는 필수. 

**참고**: 프로젝트에서 사용하지 않는 폴더라도 빈 폴더로 존재해야 검증을 통과한다.

---

## Validation

```bash
# 구조 검증
python memory_manager.py --check

# 누락된 폴더 자동 생성
python memory_manager.py --update
```
