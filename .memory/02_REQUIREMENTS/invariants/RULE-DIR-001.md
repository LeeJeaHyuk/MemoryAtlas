# [RULE-DIR-001] Memory Directory Structure

> **ID**: RULE-DIR-001
> **Domain**: STRUCTURE
> **Priority**: Critical
> **Last Updated**: 2026-01-20
> **Must-Read**: RULE-ID-001
> **Template-Version**: 2.4

---

## Rule Statement (최종 결정)

`.memory/` 폴더는 정해진 14개의 필수 하위 디렉토리를 포함해야 하며, 이 구조는 MemoryAtlas 시스템이 정상 작동하기 위한 최소 요구사항이다.

---

## Rationale

**Source**: `src/core/config.py:31-45`

```python
DIRS = [
    "00_SYSTEM/scripts",
    "01_PROJECT_CONTEXT",
    "02_REQUIREMENTS/features",
    "02_REQUIREMENTS/business_rules",
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
├── 00_SYSTEM/
│   └── scripts/              # 시스템 스크립트 (memory_manager.py 복사본)
├── 01_PROJECT_CONTEXT/       # 프로젝트 헌법 (GOALS, CONVENTIONS)
├── 02_REQUIREMENTS/          # 요구사항 (Authority Layer)
│   ├── features/             # REQ-* (기능 결정)
│   ├── business_rules/       # RULE-* (비즈니스 규칙)
│   └── discussions/          # DISC-* (조율 기록)
├── 03_TECH_SPECS/            # 기술 명세 (HOW Layer)
│   ├── architecture/         # 시스템 구조도, DB 스키마
│   ├── api_specs/            # API 명세서
│   └── decisions/            # ADR-* (기술 결정 근거)
├── 04_TASK_LOGS/             # 실행 로그 (Execution Layer)
│   ├── active/               # RUN-* (진행중 작업)
│   └── archive/              # 완료된 작업 (YYYY-MM/ 형식)
├── 98_KNOWLEDGE/             # 지식 베이스
│   └── troubleshooting/      # 해결된 문제들
└── 99_ARCHIVE/               # 더 이상 사용하지 않는 문서
    └── discussions/          # 구버전 논의 기록
```

---

## Examples

### ✅ Correct Structure

```bash
$ python memory_manager.py --check
Structure check: 0 issue(s)
```

모든 14개 디렉토리가 존재하면 통과.

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

없음. 모든 14개 디렉토리는 필수. 

**참고**: 프로젝트에서 사용하지 않는 폴더라도 빈 폴더로 존재해야 검증을 통과한다.

---

## Validation

```bash
# 구조 검증
python memory_manager.py --check

# 누락된 폴더 자동 생성
python memory_manager.py --update
```
