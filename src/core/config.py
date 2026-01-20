
import re

CURRENT_VERSION = "2.5.0"
ROOT_DIR = ".memory"
TEMPLATE_VERSION = "2.4"  # Template schema version (Context Bootstrapping)

# ============================================================================
# STRUCTURE (v2.3) - Smart Spec Edition
# ============================================================================
# .memory/
# ├── 00_SYSTEM/                  # 시스템 관리 (시스템만 수정)
# ├── 01_PROJECT_CONTEXT/         # [프로젝트 헌법]
# │   ├── 00_GOALS.md
# │   └── 01_CONVENTIONS.md
# ├── 02_REQUIREMENTS/            # [WHAT: Authority Layer]
# │   ├── features/               # REQ-* (DECISION only, 최종 결정)
# │   ├── business_rules/         # RULE-* (DECISION only)
# │   └── discussions/            # DISC-* (조율 기록, LLM 기본 무시)
# ├── 03_TECH_SPECS/              # [HOW: 개발자의 영역]
# │   ├── architecture/
# │   ├── api_specs/
# │   └── decisions/              # ADR-* (RATIONALE)
# ├── 04_TASK_LOGS/               # [HISTORY: Execution Layer]
# │   ├── active/                 # RUN-* (실행 단위)
# │   └── archive/
# └── 98_KNOWLEDGE/               # [ASSET: 배운 점]
#     └── troubleshooting/
# ============================================================================

DIRS = [
    "00_SYSTEM/scripts",
    "01_PROJECT_CONTEXT",
    "02_REQUIREMENTS/features",
    "02_REQUIREMENTS/business_rules",
    "02_REQUIREMENTS/discussions",  # NEW in v2.2
    "03_TECH_SPECS/architecture",
    "03_TECH_SPECS/api_specs",
    "03_TECH_SPECS/decisions",
    "04_TASK_LOGS/active",
    "04_TASK_LOGS/archive",
    "98_KNOWLEDGE/troubleshooting",
    "99_ARCHIVE",
    "99_ARCHIVE/discussions",  # For old discussion logs
]

# ============================================================================
# LINT / CHECK CONFIGURATION
# ============================================================================
# P1: Expanded to include discussions and RUN for format enforcement
LINT_DIRS = [
    "01_PROJECT_CONTEXT",
    "02_REQUIREMENTS/features",
    "02_REQUIREMENTS/business_rules",
    "02_REQUIREMENTS/discussions",  # v2.2.1: Even if "default skip", enforce format
    "04_TASK_LOGS/active",  # v2.2.1: RUN documents need format validation
]

LINK_SCAN_DIRS = [
    "01_PROJECT_CONTEXT",
    "02_REQUIREMENTS",
    "03_TECH_SPECS",
    "04_TASK_LOGS",
]

REQ_SCAN_DIRS = [
    "02_REQUIREMENTS/features",
    "02_REQUIREMENTS/business_rules",
]

RUN_SCAN_DIRS = [
    "04_TASK_LOGS/active",
]

LINT_SKIP_FILES = {"README.md", "00_INDEX.md"}

# Document type-specific header requirements
HEADER_FIELDS_BY_TYPE = {
    "default": ["**ID**", "**Last Updated**"],
    "features": ["**ID**", "**Domain**", "**Status**", "**Last Updated**", "**Must-Read**"],
    "business_rules": ["**ID**", "**Domain**", "**Priority**", "**Last Updated**", "**Must-Read**"],
    "decisions": ["**Status**", "**Date**"],
    "discussions": ["**ID**", "**Related-REQ**", "**Date**"],
    "runs": ["**ID**", "**Input**", "**Verification**"],
}

# ID patterns
REQ_ID_PATTERN = re.compile(r"^REQ-([A-Z]+)-(\d{3})$")
RULE_ID_PATTERN = re.compile(r"^RULE-([A-Z]+)-(\d{3})$")
ADR_ID_PATTERN = re.compile(r"^ADR-(\d{3})$")
DISC_ID_PATTERN = re.compile(r"^DISC-([A-Z]+)-(\d{3})$")
RUN_ID_PATTERN = re.compile(r"^RUN-(REQ|RULE)-([A-Z]+)-(\d{3})-step-(\d{2})$")

# Regex patterns
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")

# Authority source: **ID**: line in document metadata
# Fix A: Include ADR in META_ID_RE
META_ID_RE = re.compile(r"^\s*>\s*\*\*ID\*\*:\s*((?:REQ|RULE|DISC|RUN|ADR)-[A-Z0-9-]+(?:-step-\d{2})?)\s*$", re.M)

# Must-Read field (v2.2)
MUST_READ_RE = re.compile(r"^\s*>\s*\*\*Must-Read\*\*:\s*(.+)$", re.M)
MUST_READ_ANY_ID_RE = re.compile(r"(?:REQ|RULE|DISC|CTX)-[A-Z]+-\d{3}|ADR-\d{3}")
MUST_READ_ALLOWED_ID_RE = re.compile(r"(?:RULE)-[A-Z]+-\d{3}|ADR-\d{3}")
MUST_READ_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")

# Header patterns (v2.2.1: Support H1-H3, i.e. #, ##, ###)
# P0 fix: Templates use # [REQ-...] (H1), so regex must match #{1,3}
REQ_HEADER_RE = re.compile(r"^#{1,3}\s+\[(REQ-[A-Z]+-\d{3})\]", re.M)
RULE_HEADER_RE = re.compile(r"^#{1,3}\s+\[(RULE-[A-Z]+-\d{3})\]", re.M)
RUN_HEADER_RE = re.compile(r"^#{1,3}\s+\[(RUN-(?:REQ|RULE)-[A-Z]+-\d{3}-step-\d{2})\]", re.M)
DISC_HEADER_RE = re.compile(r"^#{1,3}\s+\[(DISC-[A-Z]+-\d{3})\]", re.M)

# RUN document sections (v2.2)
RUN_INPUT_RE = re.compile(r"^\s*>\s*\*\*Input\*\*:\s*(.+)$", re.M)
RUN_VERIFICATION_RE = re.compile(r"^\s*>\s*\*\*Verification\*\*:\s*(.+)$", re.M)
# Fix D: Support H3 Output (### Output)
RUN_OUTPUT_RE = re.compile(r"^#{2,3}\s*Output", re.M)

CHECKBOX_RE = re.compile(r"^\s*-\s*\[[ xX]\]", re.M)

# ============================================================================
# DOC TEMPLATES (v2.3) - Smart Spec Edition
# ============================================================================
DOC_TEMPLATES = {
    # =========================================================================
    # ROOT INDEX
    # =========================================================================
    "00_INDEX.md": f"""# Project Memory Index

> Entry point for Memory-Driven Development in this repo.
> **Version**: {CURRENT_VERSION} (Smart Spec Edition)
> **Template Version**: {TEMPLATE_VERSION}

## Smart Spec Model (v2.3)

```
6 Core Sections in CONVENTIONS:
  1. Commands      - Test, Lint, Run 명령어
  2. Structure     - 프로젝트 디렉토리 구조
  3. Code Style    - 포맷팅, 네이밍 규칙
  4. Testing       - 테스트 전략
  5. Git Workflow  - 브랜치/커밋 규칙
  6. Boundaries    - Always / Ask First / Never 규칙 ⭐

Boundaries (STRICT):
  ✅ Always    - AI가 항상 수행해야 하는 행동
  ⚠️ Ask First - 사람 승인 후 진행
  🚫 Never     - AI가 절대 수행하면 안 되는 행동
```

## Quick Navigation

| Folder | Purpose | Authority Level |
|--------|---------|-----------------|
| `01_PROJECT_CONTEXT/` | 프로젝트 헌법 + **Boundaries** | Constitution |
| `02_REQUIREMENTS/features/` | 기능 **결정** (DECISION) | Authority |
| `02_REQUIREMENTS/business_rules/` | 규칙 **결정** (DECISION) | Authority |
| `02_REQUIREMENTS/discussions/` | 조율 기록 (DISCUSSION) | Reference |
| `03_TECH_SPECS/` | 기술 설계 & ADR | Implementation |
| `04_TASK_LOGS/` | 실행 기록 (RUN-*) | Execution |
| `98_KNOWLEDGE/` | 배운 점 | Asset |

## Start Here (For AI Agents)

### Reading Priority (P0 = Must Read)
1. **P0**: `01_PROJECT_CONTEXT/01_CONVENTIONS.md` - **특히 Boundaries 섹션** ⭐
2. **P0**: Target REQ's `**Must-Read**` field
3. **P1**: `02_REQUIREMENTS/business_rules/` (all active)
4. **P2**: `98_KNOWLEDGE/` (if complex feature)

### Execution Checklist
1. [ ] CONVENTIONS의 **Boundaries** 확인
2. [ ] Target REQ 읽기
3. [ ] Must-Read 문서 읽기
4. [ ] RUN 문서 작성 (Self-Check 포함)
5. [ ] 구현 → 테스트 → 검증
6. [ ] Self-Check 통과 후 RUN 완료 처리

### What NOT to Read by Default
- `02_REQUIREMENTS/discussions/` - Only when explicitly referenced
- `04_TASK_LOGS/archive/` - Only for historical context
- `99_ARCHIVE/` - Deprecated content

## Document Map

### 01_PROJECT_CONTEXT (프로젝트 헌법)
- [00_GOALS.md](01_PROJECT_CONTEXT/00_GOALS.md) - 프로젝트 목표
- [01_CONVENTIONS.md](01_PROJECT_CONTEXT/01_CONVENTIONS.md) - 코딩 규칙 + **Boundaries** ⭐

### 02_REQUIREMENTS (요구사항)
- [features/](02_REQUIREMENTS/features/) - 기능 **결정** (Authority)
- [business_rules/](02_REQUIREMENTS/business_rules/) - 규칙 **결정** (Authority)
- [discussions/](02_REQUIREMENTS/discussions/) - 조율 기록 (Reference)

### 03_TECH_SPECS (기술 설계)
- [architecture/](03_TECH_SPECS/architecture/) - 구조도, DB 스키마
- [api_specs/](03_TECH_SPECS/api_specs/) - API 명세
- [decisions/](03_TECH_SPECS/decisions/) - ADR (RATIONALE)

### 04_TASK_LOGS (작업 기록)
- [active/](04_TASK_LOGS/active/) - 실행 중 (RUN-*) + **Self-Check**
- [archive/](04_TASK_LOGS/archive/) - 완료된 작업

### 98_KNOWLEDGE (지식 저장소)
- [troubleshooting/](98_KNOWLEDGE/troubleshooting/) - 해결된 난제들
""",

    # =========================================================================
    # 01_PROJECT_CONTEXT
    # =========================================================================
    "01_PROJECT_CONTEXT/00_GOALS.md": f"""# Project Goals

> **ID**: CTX-GOALS-001
> **Last Updated**: (TBD)
> **Template-Version**: {TEMPLATE_VERSION}

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

- **Primary**: (주요 사용자)
- **Secondary**: (부가 사용자)

---

## 3. Success Criteria

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
| Phase 1 | MVP | TBD | Not Started |
| Phase 2 | Core Features | TBD | Not Started |
| Phase 3 | Hardening | TBD | Not Started |
""",

    "01_PROJECT_CONTEXT/01_CONVENTIONS.md": f"""# Coding Conventions & Rules (Smart Spec)

> **ID**: CTX-CONV-001
> **Last Updated**: (TBD)
> **Template-Version**: {TEMPLATE_VERSION}

---

## 1. Commands (실행 명령어)

> AI가 테스트, 린트, 실행 시 사용할 명령어를 명시합니다.

| Action | Command | Description |
|--------|---------|-------------|
| **Test** | `pytest` | Run all unit tests |
| **Test (specific)** | `pytest tests/test_<name>.py` | Run specific test file |
| **Lint** | `ruff check .` | Check code style |
| **Format** | `ruff format .` | Auto-format code |
| **Run** | `python main.py` | Run the application |
| **Build** | `(TBD)` | Build for production |

---

## 2. Project Structure (프로젝트 구조)

```
project_root/
├── src/                    # 소스 코드 (비즈니스 로직)
│   ├── __init__.py
│   └── (modules)/
├── tests/                  # 테스트 코드 (src와 1:1 대응)
│   ├── __init__.py
│   └── test_*.py
├── .memory/                # 프로젝트 문서 (MemoryAtlas)
├── requirements.txt        # Python 의존성
└── README.md               # 프로젝트 소개
```

---

## 3. Code Style (코드 스타일)

### Python
- **Formatter**: `ruff format` (or `black`)
- **Linter**: `ruff check` (or `flake8`)
- **Type Hints**: Required for all public functions
- **Docstrings**: Google style (복잡한 함수만)

### Naming Conventions
| Type | Style | Example |
|------|-------|---------|
| Variables/Functions | `snake_case` | `user_name`, `get_data()` |
| Classes | `PascalCase` | `UserManager` |
| Constants | `UPPER_SNAKE_CASE` | `MAX_RETRY` |
| Files | `lowercase_underscores` | `user_service.py` |

### Comments
- 복잡한 로직에만 **"Why"**를 적는다
- 명백한 코드에 주석 금지
- TODO: `# TODO(author): description`

---

## 4. Testing Strategy (테스트 전략)

### Requirements
- 모든 기능(`REQ`)은 최소 1개의 테스트 파일을 가져야 함
- 테스트 파일명: `test_<module_name>.py`
- 테스트 함수명: `test_<behavior>_<expected_result>()`

### TDD Workflow (권장)
1. `RUN` 문서 작성 시 테스트 케이스 먼저 정의
2. 실패하는 테스트 작성
3. 테스트 통과하는 최소 코드 작성
4. 리팩토링

### Coverage
- 목표: (예: 80% 이상)
- 핵심 비즈니스 로직: 100%

---

## 5. Git Workflow (Git 규칙)

### Branch Naming
- Feature: `feat/REQ-ID-short-desc` (예: `feat/REQ-AUTH-001-login`)
- Bugfix: `fix/issue-id-desc`
- Hotfix: `hotfix/critical-fix`

### Commit Messages
```
<type>(<scope>): <subject>

<body>
```
- **Types**: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`
- **Example**: `feat(auth): add JWT token validation`

### PR Rules
- 1 PR = 1 REQ (가능한 경우)
- Self-review 후 요청
- CI 통과 필수

---

## 6. Smart Spec Boundaries (STRICT)

### ✅ Always (항상 수행)
- `RUN` 문서 작성 시 `Verification` 섹션에 구체적인 **검증 명령어**를 포함할 것. (예: `pytest tests/auth/`)
- 모든 퍼블릭 API/함수에는 **Docstring**과 **Type Hint**를 포함할 것.

### 🙋 Ask First (물어볼 것)
- `requirements.txt`, `package.json` 등 **의존성 추가/변경**.
- **DB 스키마 변경** (`migration` 파일 생성).
- 기존 `01_CONVENTIONS`나 시스템 템플릿 수정.

### 🚫 Never (절대 금지)
- **Secret Key**, Password, API Key를 코드나 문서에 하드코딩.
- **Mock Data**를 프로덕션 코드에 남기는 행위.
- `REQ` 문서의 **Decision** 섹션을 수정하지 않고 하단에 "추가 사항"으로 덧붙이는 행위.

---

## 7. Documentation Maintenance Policy
1. **SSOT (Single Source of Truth)**: `REQ` 문서는 항상 **현재 시점의 최종 명세**여야 한다.
2. **Rewrite, Don't Append**: 요구사항이 변경되면 기존 텍스트를 수정(Refactor)하라. 밑에 "Update 1..." 식으로 덧붙이지 마라.
3. **Change Log**: 변경 이력은 문서 최상단의 `Change Log` 테이블에만 기록하라.

---

## 8. AI Agent Quick Reference

### Reading Priority (P0 = Must Read)
1. **P0**: 이 파일 (`01_CONVENTIONS.md`)
2. **P0**: Target REQ의 `**Must-Read**` 필드
3. **P1**: `02_REQUIREMENTS/business_rules/` (전체)
4. **P2**: `98_KNOWLEDGE/` (복잡한 기능 시)

### Execution Checklist
1. [ ] CONVENTIONS의 Boundaries 확인
2. [ ] Target REQ 읽기
3. [ ] Must-Read 문서 읽기
4. [ ] RUN 문서 작성 (Self-Check 포함)
5. [ ] 구현 → 테스트 → 검증
6. [ ] RUN 문서 완료 처리
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
Use the following rules so humans and LLMs can both parse and act on documents reliably.

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

### Rule 6: Human-Centric Readability (사람 중심 가독성)
사람이 3초 안에 핵심을 파악할 수 있도록 작성하라.

1. **BLUF (Bottom Line Up Front)**: 모든 섹션은 **결론(Conclusion)**이나 **한 줄 요약(Summary)**으로 시작하라.
2. **Visual Anchors (Emojis)**: 텍스트의 성격을 아이콘으로 표시하라.
   - 📕 **Critical**: 주의사항, 보안 이슈
   - ✨ **Feature**: 새로운 기능
   - 💡 **Note**: 참고, 팁
   - ❓ **Open**: 미결정 사항

### Rule 7: Diagram Over Text (텍스트보다 다이어그램)
조건 분기나 흐름이 3단계 이상 넘어가면 줄글 사용을 금지한다.

1. **Decision Matrix**: 복잡한 조건(권한, 상태 등)은 반드시 **마크다운 표(Table)**로 작성하라.
2. **Mermaid.js**: 데이터 흐름이나 상태 변화는 `mermaid` 코드 블록으로 시각화하라.

## Expected Effects (Current vs Proposed)

| 구분 | 현재 상태 (Current) | 추가 적용 후 (Proposed) |
|------|---------------------|-------------------------|
| 복잡한 로직 설명 | "관리자는 읽기 쓰기가 되는데 유저는 읽기만 되고..." (줄글) | 권한 테이블(Table) + 흐름도(Mermaid) |
| 요구사항 변경 시 | 문서 맨 아래에 `## 추가 요청사항` 섹션이 계속 생김 (스파게티) | Decision 본문이 깔끔하게 수정되고, 상단 Change Log만 한 줄 추가됨 |
| 위험한 작업 시 | AI가 임의로 판단해서 진행할 수 있음 | Ask First 규칙에 걸려 "의존성을 추가해도 될까요?"라고 물어봄 |
| 가독성 | 흑백 텍스트 위주라 눈에 잘 안 들어옴 | 이모지(📕, ✨, 💡, ❓)와 요약 덕분에 훑어보기 편함 |

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

    # =========================================================================
    # 02_REQUIREMENTS (v2.3 - Smart Spec Edition)
    # =========================================================================
    "02_REQUIREMENTS/README.md": f"""# Requirements (Authority Layer)

> **Template-Version**: {TEMPLATE_VERSION}
>
> 이 폴더는 **"무엇을 만들 것인가?"**의 **최종 결정**을 저장합니다.
> 논의/조율 기록은 `discussions/`에 분리합니다.

## Authority Model (v2.3)

```
문서 등급:
├── features/        → DECISION (Authority) - 최종 결정만
│                      + Constraints & Boundaries (Optional)
├── business_rules/  → DECISION (Authority) - 최종 결정만
└── discussions/     → DISCUSSION (Reference) - 조율 기록
```

### Smart Spec Integration (v2.3)
- **Boundaries**: 프로젝트 전역 규칙은 `01_CONVENTIONS.md`의 Boundaries 섹션
- **Constraints**: 기능별 추가 제약은 각 REQ의 `Constraints & Boundaries` 섹션 (Optional)

### Why Separate?
- **DECISION (features/, business_rules/)**: LLM이 반드시 읽어야 함
- **DISCUSSION (discussions/)**: LLM이 기본적으로 안 읽음. 명시적 참조 시만.

이렇게 분리하면:
1. 최종 결정이 명확해짐
2. LLM이 "무엇이 결정인지" 확률적 판단 불필요
3. 필수 규칙 누락/과다 참조 방지

## Structure

```
02_REQUIREMENTS/
├── features/           # REQ-* (DECISION only)
│   └── REQ-AUTH-001.md
├── business_rules/     # RULE-* (DECISION only)
│   └── RULE-DATA-001.md
└── discussions/        # DISC-* (조율 기록)
    └── DISC-AUTH-001.md
```

## Naming Convention (STRICT)

| Type | Pattern | Example | Location |
|------|---------|---------|----------|
| Feature | `REQ-[DOMAIN]-[NNN].md` | `REQ-AUTH-001.md` | features/ |
| Rule | `RULE-[DOMAIN]-[NNN].md` | `RULE-DATA-001.md` | business_rules/ |
| Discussion | `DISC-[DOMAIN]-[NNN].md` | `DISC-AUTH-001.md` | discussions/ |

## Must-Read Field (Required in v2.2)

모든 REQ/RULE 문서에는 `**Must-Read**` 필드가 필수입니다:

```markdown
> **Must-Read**: RULE-DATA-001, RULE-SEC-001, ADR-003
```

이 필드에 나열된 문서는 해당 REQ 구현 시 **반드시** 읽어야 합니다.

- Must-Read allows only RULE/ADR IDs (CTX is P0 and not allowed here).
- If you use markdown links, the link text must be the ID (e.g. `[RULE-DATA-001](path)`).
""",

    "02_REQUIREMENTS/features/README.md": f"""# Feature Requirements (DECISION)

> **Template-Version**: {TEMPLATE_VERSION}
>
> 이곳에는 **최종 결정**만 저장합니다.
> 논의/대안 검토는 `../discussions/`에 작성하세요.

## Template

```markdown
# [REQ-XXX-001] Feature Name

> **ID**: REQ-XXX-001
> **Domain**: (도메인)
> **Status**: [Draft | Active | Deprecated]
> **Last Updated**: YYYY-MM-DD
> **Must-Read**: RULE-XXX-001, ADR-XXX
> **Template-Version**: {TEMPLATE_VERSION}

---

## Decision (최종 결정)

(기능에 대한 명확한 결정. 짧고 단단하게.)

## Input

- `param1` (type): description

## Output

- `result` (type): description

## Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2

## Constraints & Boundaries (Optional)

> 이 기능 구현 시 적용되는 특별한 제약.
> 프로젝트 전역 Boundaries(`01_CONVENTIONS.md`)를 넘어서는 경우만 작성.

### ⚠️ Ask First
- (이 기능에서 사람 승인이 필요한 것)

### 🚫 Never
- (이 기능에서 절대 금지)

## Related

- Discussion: [DISC-XXX-001](../discussions/DISC-XXX-001.md)
- Tech Spec: [API Spec](../../03_TECH_SPECS/api_specs/)
```

## Rules

1. **결정만 적는다**: 논의/대안은 discussions/에
2. **짧게 유지**: 한 REQ = 하나의 명확한 결정
3. **Must-Read 필수**: RULE/ADR ID만, 링크 텍스트는 ID
4. **ID 일치**: 파일명 = **ID**: = 헤더 [ID]
5. **Boundaries 선택적**: 프로젝트 전역 규칙 외 추가 제약 시만 작성
""",

    "02_REQUIREMENTS/business_rules/README.md": f"""# Business Rules (DECISION)

> **Template-Version**: {TEMPLATE_VERSION}
>
> 비즈니스 로직, 공식, 변하지 않는 규칙의 **최종 결정**을 저장합니다.

## Template

```markdown
# [RULE-XXX-001] Rule Name

> **ID**: RULE-XXX-001
> **Domain**: (도메인)
> **Priority**: [Critical | High | Medium | Low]
> **Last Updated**: YYYY-MM-DD
> **Must-Read**: RULE-XXX-001, ADR-XXX
> **Template-Version**: {TEMPLATE_VERSION}

---

## Rule Statement (최종 결정)

(규칙을 명확하게 한 문장으로)

## Rationale

(왜 이 규칙이 필요한가? 간단히)

## Examples

### Correct
(올바른 예시)

### Incorrect
(잘못된 예시)

## Exceptions

(예외 상황이 있다면)
```

## Common Domains

- **DATA**: 데이터 형식, 저장 규칙
- **PERF**: 성능 제약
- **SEC**: 보안 규칙
- **UX**: 사용자 경험 규칙
""",

    "02_REQUIREMENTS/discussions/README.md": f"""# Discussions (Reference Layer)

> **Template-Version**: {TEMPLATE_VERSION}
>
> 사람-AI 조율 기록을 저장합니다.
> **LLM은 기본적으로 이 폴더를 읽지 않습니다.**

## When to Use

- 요구사항 논의 과정 기록
- 대안 검토 및 비교
- 결정 근거 상세 설명
- 이해관계자 의견 조율

## Template

```markdown
# [DISC-XXX-001] Discussion Title

> **ID**: DISC-XXX-001
> **Related-REQ**: REQ-XXX-001 (or RULE-XXX-001)
> **Date**: YYYY-MM-DD
> **Participants**: (참여자)
> **Template-Version**: {TEMPLATE_VERSION}

---

## Context

(논의 배경)

## Options Considered

### Option A: (대안 1)
- Pros: ...
- Cons: ...

### Option B: (대안 2)
- Pros: ...
- Cons: ...

## Discussion Log

### YYYY-MM-DD
- [Person/AI]: 의견 1
- [Person/AI]: 의견 2

## Conclusion

(결론 → REQ/RULE에 반영됨)
```

## Important Notes

1. **LLM 기본 무시**: 명시적으로 참조하지 않으면 읽지 않음
2. **REQ와 연결**: `Related-REQ` 필드로 관련 결정 문서 연결
3. **Archive 정책**: 오래된 논의는 `99_ARCHIVE/discussions/`로 이동
""",

    # =========================================================================
    # 03_TECH_SPECS
    # =========================================================================
    "03_TECH_SPECS/README.md": f"""# Technical Specifications (HOW)

> **Template-Version**: {TEMPLATE_VERSION}
>
> **"어떻게 만들 것인가?"**를 정의합니다.

## Structure

```
03_TECH_SPECS/
├── architecture/       # 구조도, DB 스키마
├── api_specs/          # 입출력 명세
└── decisions/          # ADR (RATIONALE)
```

## Relation to Authority

```
REQ (Authority) → TECH_SPEC (Implementation) → CODE
```

TECH_SPEC은 REQ의 결정을 **구현**하는 방법을 정의합니다.
REQ와 충돌 시, REQ가 우선합니다.
""",

    "03_TECH_SPECS/architecture/README.md": f"""# Architecture Documents

> **Template-Version**: {TEMPLATE_VERSION}

## Template: System Architecture

```markdown
# System Architecture

> **Last Updated**: YYYY-MM-DD
> **Template-Version**: {TEMPLATE_VERSION}

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

1. User -> Frontend
2. Frontend -> Backend API
3. Backend -> Database
```
""",

    "03_TECH_SPECS/api_specs/README.md": f"""# API Specifications

> **Template-Version**: {TEMPLATE_VERSION}

## Template

```markdown
# [Module Name] API Specification

> **Module**: (모듈명)
> **Last Updated**: YYYY-MM-DD
> **Related-REQ**: REQ-XXX-001
> **Template-Version**: {TEMPLATE_VERSION}

---

## Endpoints / Functions

### `GET /api/users/{{id}}`

- **Description**: 사용자 정보 조회
- **Parameters**: `id` (UUID)
- **Response**: User object
- **Error Codes**: 404, 500
```
""",

    "03_TECH_SPECS/decisions/README.md": f"""# Architecture Decision Records (RATIONALE)

> **Template-Version**: {TEMPLATE_VERSION}
>
> 기술적 의사결정과 그 **근거**를 기록합니다.

## Why ADR?

"왜 MongoDB 대신 PostgreSQL을 썼는가?"에 대한 답을 남깁니다.
구조를 뒤집을 때, 이 기록을 보지 않으면 같은 실수를 반복합니다.

## Template

```markdown
# ADR-001: [Decision Title]

> **Status**: [Proposed | Accepted | Deprecated | Superseded]
> **Date**: YYYY-MM-DD
> **Deciders**: (결정자)
> **Related-REQ**: REQ-XXX-001
> **Template-Version**: {TEMPLATE_VERSION}

---

## Context

(문제 상황을 설명)

## Decision

(무엇을 결정했는가?)

## Alternatives Considered

### Option A
- Pros: ...
- Cons: ...

### Option B
- Pros: ...
- Cons: ...

## Consequences

### Positive
- ...

### Negative
- ...
```
""",

    # =========================================================================
    # 04_TASK_LOGS (v2.2 - Execution Unit)
    # =========================================================================
    "04_TASK_LOGS/README.md": f"""# Task Logs (Execution Layer)

> **Template-Version**: {TEMPLATE_VERSION}
>
> 실행 기록을 관리합니다.

## Execution Unit Model (v2.2)

```
실행 문서 1개 = 1목적 + 1검증 + 1결과

RUN-REQ-AUTH-001-step-01.md  (로그인 폼 구현)
RUN-REQ-AUTH-001-step-02.md  (API 연동)
RUN-REQ-AUTH-001-step-03.md  (테스트 작성)
```

### Why Small Units?

- 큰 RUN 금지: 한번 실행에 너무 많은 변경이 묶이면 추적 불가
- 1:1 대응: 변경 이유를 명확히 추적 가능
- 검색 가능: 로그가 쌓여도 의미있는 검색

## Structure

```
04_TASK_LOGS/
├── active/             # 실행 중 (RUN-*)
│   └── RUN-REQ-AUTH-001-step-01.md
└── archive/            # 완료된 작업
    └── YYYY-MM/
        └── RUN-*.md
```

## Naming Convention

`RUN-[REQ|RULE]-[DOMAIN]-[NNN]-step-[NN].md`

Examples:
- `RUN-REQ-AUTH-001-step-01.md`
- `RUN-REQ-AUTH-001-step-02.md`
- `RUN-RULE-DATA-001-step-01.md`
""",

    "04_TASK_LOGS/active/README.md": f"""# Active Tasks (Execution)

> **Template-Version**: {TEMPLATE_VERSION}

## RUN Document Template

```markdown
# [RUN-REQ-XXX-001-step-01] Step Title

> **ID**: RUN-REQ-XXX-001-step-01
> **Status**: [Active | Blocked | Done]
> **Started**: YYYY-MM-DD
> **Input**: REQ-XXX-001, RULE-YYY-001, 01_CONVENTIONS.md
> **Verification**: (성공 조건 - 한 줄 요약)
> **Template-Version**: {TEMPLATE_VERSION}

---

## Objective

(이 단계의 목표 - 하나만)

## Steps

1. [ ] Step 1
2. [ ] Step 2

## Verification (Self-Check)

> 작업 완료 전 반드시 확인하는 체크리스트

- [ ] **Test**: `pytest tests/test_xxx.py` 통과?
- [ ] **Boundary**: Secret 커밋 없음? (`01_CONVENTIONS.md` Boundaries 준수?)
- [ ] **Spec**: 구현이 `REQ-XXX-001`과 일치?

### Success Condition
(성공 조건 상세)

## Output

(생성/수정된 파일 목록)

- `src/auth/login.py` - Created
- `tests/test_login.py` - Created
```

## Rules

1. **1 RUN = 1 목적**: 여러 목적을 섞지 않음
2. **Input 명시**: 읽어야 할 문서 ID 목록 (Must-Read 포함)
3. **Verification 명시**: 성공 조건 + Self-Check 체크리스트
4. **Output 기록**: 생성/수정 파일 목록
5. **Self-Check 필수**: 테스트, Boundary, Spec 일치 확인
""",

    "04_TASK_LOGS/archive/README.md": f"""# Archived Tasks

> **Template-Version**: {TEMPLATE_VERSION}

## Structure

```
archive/
├── 2024-01/
│   ├── RUN-REQ-AUTH-001-step-01.md
│   └── RUN-REQ-AUTH-001-step-02.md
├── 2024-02/
│   └── ...
```

## Archive Criteria

- Status가 `Done`으로 변경된 RUN 문서
- 월별로 자동 정리
""",

    # =========================================================================
    # 98_KNOWLEDGE
    # =========================================================================
    "98_KNOWLEDGE/README.md": """# Knowledge Base (ASSET)

> 프로젝트를 진행하면서 배운 **"일반적인 지식"**을 저장합니다.

## Why This Folder?

- Task Log에 "파이썬 asyncio 에러 해결법"을 적어두면, 나중에 로그가 쌓여서 검색이 안 됩니다.
- 배운 점을 별도로 저장해야 과거의 실수를 반복하지 않습니다.

## Structure

```
98_KNOWLEDGE/
├── troubleshooting/    # 해결된 난제들
│   └── [topic]/        # 주제별 분류
└── [other_topics]/     # 필요에 따라 추가
```
""",

    "98_KNOWLEDGE/troubleshooting/README.md": f"""# Troubleshooting Guide

> **Template-Version**: {TEMPLATE_VERSION}

## Template

```markdown
# [Issue Title]

> **Category**: [Python | JavaScript | Database | DevOps | ...]
> **Date Discovered**: YYYY-MM-DD
> **Related Task**: RUN-REQ-XXX-001-step-NN
> **Template-Version**: {TEMPLATE_VERSION}

---

## Problem

(문제 상황 설명)

## Root Cause

(원인 분석)

## Solution

(해결 방법)

## Prevention

(다시 발생하지 않으려면?)
```
""",

    # =========================================================================
    # 00_SYSTEM
    # =========================================================================
    "00_SYSTEM/README.md": f"""# System Management

> [!CAUTION]
> ## SYSTEM-MANAGED FOLDER
>
> 이 폴더는 `memory_manager.py`에 의해 **자동 관리**됩니다.
>
> ### Overwrite Policy
> - **AGENT_RULES.md**: 시스템 업데이트 시 덮어쓰기됨
> - **scripts/**: 시스템 업데이트 시 덮어쓰기됨
> - 사용자/에이전트 수정 -> 다음 업데이트에서 원복
>
> ### For Customization
> 커스텀 규칙이 필요하면 `01_PROJECT_CONTEXT/01_CONVENTIONS.md`에 작성하세요.

## Version Info

- **Manager Version**: {CURRENT_VERSION}
- **Template Version**: {TEMPLATE_VERSION}
""",
}

# ============================================================================
# BOOTSTRAP TEMPLATES (v2.4 - Context Bootstrapping)
# ============================================================================
BOOTSTRAP_PROMPT_TEMPLATE = f"""# 🚀 프로젝트 킥오프 (Context Bootstrapping)

> **MemoryAtlas v{CURRENT_VERSION}**
>
> 이 파일을 AI 에이전트(Claude, GPT 등)에게 전달하세요.
> AI가 아래 주제로 인터뷰 후, 프로젝트 헌법을 완성합니다.

---

## 사용 방법

1. 이 파일 내용을 AI 채팅창에 복사하거나, AI에게 이 파일을 읽게 하세요.
2. AI가 아래 아젠다에 따라 질문합니다.
3. 대화가 끝나면 AI가 완성된 문서를 출력합니다.
4. 출력된 내용을 해당 파일에 저장하세요.
5. `python memory_manager.py --doctor`로 검증하세요.

---

## 🎯 토의 아젠다 (AI에게 전달할 내용)

### 1. Project Identity (프로젝트 정체성)

나에게 다음을 질문해주세요:
- 프로젝트 이름은 무엇인가요?
- 한 문장으로 설명하면?
- 주요 사용자는 누구인가요?
- 핵심 가치/목표는 무엇인가요?

### 2. Tech Stack (기술 스택)

나에게 다음을 질문해주세요:
- 프로그래밍 언어는? (Python, TypeScript, Go 등)
- 프레임워크는? (FastAPI, Django, React, Next.js 등)
- 테스트 도구는? (pytest, jest, vitest 등)
- 린터/포매터는? (ruff, black, eslint, prettier 등)
- 빌드/배포 도구는?

### 3. Smart Spec Boundaries (경계 설정) ⭐

**가장 중요합니다.** 나에게 다음을 질문해주세요:

#### ✅ Always (AI가 항상 해야 할 것)
- 테스트 관련 규칙은?
- 코드 품질 관련 규칙은?
- 문서화 관련 규칙은?

#### ⚠️ Ask First (사전 승인 필요)
- 어떤 변경에 대해 먼저 물어봐야 하나요?
- 의존성 추가/삭제는 어떻게?
- DB나 API 변경은?

#### 🚫 Never (절대 금지)
- 이 프로젝트에서 절대 하면 안 되는 것은?
- 보안 관련 금지 사항은?
- 데이터 관련 금지 사항은?

### 4. Project Structure (프로젝트 구조)

나에게 다음을 질문해주세요:
- 소스 코드 폴더 구조는?
- 테스트 폴더 구조는?
- 설정 파일들은 어디에?

### 5. Git Workflow (Git 규칙)

나에게 다음을 질문해주세요:
- 브랜치 네이밍 규칙은?
- 커밋 메시지 형식은?
- PR 규칙은?

---

## 📋 AI에게 지시

위 아젠다에 따라 나를 인터뷰한 후, **다음 2개 파일을 완성된 형태로 출력**해주세요:

1. **`01_PROJECT_CONTEXT/00_GOALS.md`**
   - 프로젝트 정체성, 목표, 범위

2. **`01_PROJECT_CONTEXT/01_CONVENTIONS.md`**
   - Commands 테이블 (실제 명령어로 채움)
   - Project Structure (실제 구조로 채움)
   - Code Style (실제 도구와 규칙으로 채움)
   - Testing Strategy (실제 전략으로 채움)
   - Git Workflow (실제 규칙으로 채움)
   - **Boundaries** (인터뷰 결과로 채움) ⭐

---

## ⚠️ 주의사항

- 기본 템플릿의 예시가 아닌, **실제 프로젝트에 맞는 내용**으로 채워주세요.
- Boundaries는 프로젝트 특성에 맞게 구체적으로 작성해주세요.
- 불확실한 부분은 `[TODO: 확정 필요]`로 표시해주세요.

---

## 완료 후

1. AI가 출력한 내용을 각 파일에 저장
2. `python memory_manager.py --doctor` 실행하여 검증
3. 이 파일(`BOOTSTRAP_PROMPT.md`)은 삭제하거나 `99_ARCHIVE/`로 이동
"""

BOOTSTRAP_CONVENTIONS_TEMPLATE = f"""# Coding Conventions & Rules (Smart Spec)

> **ID**: CTX-CONV-001
> **Last Updated**: [TODO: AI와 토의하여 결정]
> **Template-Version**: {TEMPLATE_VERSION}

---

## 1. Commands (실행 명령어)

> [TODO: AI와 토의하여 결정]

| Action | Command | Description |
|--------|---------|-------------|
| **Test** | `[TODO]` | Run all unit tests |
| **Test (specific)** | `[TODO]` | Run specific test file |
| **Lint** | `[TODO]` | Check code style |
| **Format** | `[TODO]` | Auto-format code |
| **Run** | `[TODO]` | Run the application |
| **Build** | `[TODO]` | Build for production |

---

## 2. Project Structure (프로젝트 구조)

> [TODO: AI와 토의하여 결정]

```
project_root/
├── [TODO]/              # 소스 코드
├── [TODO]/              # 테스트 코드
├── .memory/             # 프로젝트 문서 (MemoryAtlas)
└── [TODO]               # 기타 파일들
```

---

## 3. Code Style (코드 스타일)

> [TODO: AI와 토의하여 결정]

### [Language]
- **Formatter**: `[TODO]`
- **Linter**: `[TODO]`
- **Type Hints**: [TODO]
- **Docstrings**: [TODO]

### Naming Conventions
| Type | Style | Example |
|------|-------|---------|
| Variables/Functions | `[TODO]` | |
| Classes | `[TODO]` | |
| Constants | `[TODO]` | |
| Files | `[TODO]` | |

---

## 4. Testing Strategy (테스트 전략)

> [TODO: AI와 토의하여 결정]

### Requirements
- [TODO]

### Coverage
- 목표: [TODO]

---

## 5. Git Workflow (Git 규칙)

> [TODO: AI와 토의하여 결정]

### Branch Naming
- Feature: `[TODO]`
- Bugfix: `[TODO]`

### Commit Messages
- Format: `[TODO]`

---

## 6. Smart Spec Boundaries (STRICT)

### ✅ Always (항상 수행)
- `RUN` 문서 작성 시 `Verification` 섹션에 구체적인 **검증 명령어**를 포함할 것. (예: `pytest tests/auth/`)
- 모든 퍼블릭 API/함수에는 **Docstring**과 **Type Hint**를 포함할 것.

### 🙋 Ask First (물어볼 것)
- `requirements.txt`, `package.json` 등 **의존성 추가/변경**.
- **DB 스키마 변경** (`migration` 파일 생성).
- 기존 `01_CONVENTIONS`나 시스템 템플릿 수정.

### 🚫 Never (절대 금지)
- **Secret Key**, Password, API Key를 코드나 문서에 하드코딩.
- **Mock Data**를 프로덕션 코드에 남기는 행위.
- `REQ` 문서의 **Decision** 섹션을 수정하지 않고 하단에 "추가 사항"으로 덧붙이는 행위.

---

## 7. Documentation Maintenance Policy
1. **SSOT (Single Source of Truth)**: `REQ` 문서는 항상 **현재 시점의 최종 명세**여야 한다.
2. **Rewrite, Don't Append**: 요구사항이 변경되면 기존 텍스트를 수정(Refactor)하라. 밑에 "Update 1..." 식으로 덧붙이지 마라.
3. **Change Log**: 변경 이력은 문서 최상단의 `Change Log` 테이블에만 기록하라.

---

## 8. AI Agent Quick Reference

### Reading Priority (P0 = Must Read)
1. **P0**: 이 파일 (`01_CONVENTIONS.md`)
2. **P0**: Target REQ의 `**Must-Read**` 필드
3. **P1**: `02_REQUIREMENTS/business_rules/` (전체)
4. **P2**: `98_KNOWLEDGE/` (복잡한 기능 시)

### Execution Checklist
1. [ ] CONVENTIONS의 Boundaries 확인
2. [ ] Target REQ 읽기
3. [ ] Must-Read 문서 읽기
4. [ ] RUN 문서 작성 (Self-Check 포함)
5. [ ] 구현 → 테스트 → 검증
6. [ ] RUN 문서 완료 처리
"""

BOOTSTRAP_GOALS_TEMPLATE = f"""# Project Goals

> **ID**: CTX-GOALS-001
> **Last Updated**: [TODO: AI와 토의하여 결정]
> **Template-Version**: {TEMPLATE_VERSION}

---

## 1. Project Identity

### Name
[TODO: AI와 토의하여 결정]

### One-Line Summary
[TODO: AI와 토의하여 결정]

### Core Value
[TODO: AI와 토의하여 결정]

---

## 2. Target Users

- **Primary**: [TODO: AI와 토의하여 결정]
- **Secondary**: [TODO: AI와 토의하여 결정]

---

## 3. Success Criteria

- [ ] [TODO: AI와 토의하여 결정]

---

## 4. Scope

### In-Scope
- [TODO: AI와 토의하여 결정]

### Out-of-Scope
- [TODO: AI와 토의하여 결정]

---

## 5. Milestones

| Phase | Description | Target Date | Status |
|-------|-------------|-------------|--------|
| Phase 1 | [TODO] | [TODO] | Not Started |
"""

BOOTSTRAP_TEMPLATES = {
    "BOOTSTRAP_PROMPT.md": BOOTSTRAP_PROMPT_TEMPLATE,
}

# ============================================================================
# SYSTEM TEMPLATES
# ============================================================================
AGENT_RULES_TEMPLATE = f"""# MemoryAtlas Agent Rules (v{CURRENT_VERSION}) - Smart Spec Edition

> **SYSTEM FILE**: Managed by `memory_manager.py`. DO NOT EDIT.
> **For custom rules**: Use `01_PROJECT_CONTEXT/01_CONVENTIONS.md`.

---

## 1. Smart Spec Model

```
6 Core Sections in CONVENTIONS:
  1. Commands: Test, Lint, Run 명령어
  2. Project Structure: 디렉토리 구조
  3. Code Style: 포맷팅, 네이밍 규칙
  4. Testing Strategy: 테스트 요구사항
  5. Git Workflow: 브랜치/커밋 규칙
  6. Boundaries: Always / Ask First / Never 규칙

Boundaries (STRICT):
  ✅ Always: AI가 항상 수행해야 하는 행동
  ⚠️ Ask First: 사람 승인 후 진행
  🚫 Never: AI가 절대 수행하면 안 되는 행동
```

---

## 2. Authority Model

```
권위의 흐름 (Authority Flow):
  REQ (Authority) → TECH_SPEC → CODE → RUN/LOG

문서 등급:
  - DECISION: 최종 결정 (REQ-*, RULE-*) - MUST READ
  - DISCUSSION: 조율 기록 (DISC-*) - DEFAULT SKIP
  - RATIONALE: 결정 근거 (ADR-*) - READ IF REFERENCED
  - EXECUTION: 작업 단위 (RUN-*) - CREATE/UPDATE
```

---

## 3. Reading Priority

### P0 (Always Read)
1. `01_PROJECT_CONTEXT/01_CONVENTIONS.md` - **특히 Boundaries 섹션**
2. Target REQ's `**Must-Read**` field
3. All referenced RULE-* documents

### P1 (Read for Context)
- `02_REQUIREMENTS/business_rules/` (all active)
- Referenced ADR-* documents

### Default Skip
- `02_REQUIREMENTS/discussions/` - Only when explicitly referenced
- `04_TASK_LOGS/archive/` - Only for historical context
- `99_ARCHIVE/` - Deprecated content

---

## 4. Boundaries Compliance (STRICT)

### ✅ Always (항상 수행)
- RUN 문서 종료 전 **테스트 통과** 확인
- 모든 퍼블릭 함수에 **Type Hint** 추가
- 기존 코드 수정 시 **기존 테스트 통과** 확인
- 새 기능 추가 시 **REQ 문서 참조** 확인

### ⚠️ Ask First (사전 승인 필요)
- `requirements.txt` 등 **의존성 추가/삭제**
- `.memory/00_SYSTEM/` 내부 파일 수정
- **DB 스키마 변경** (migration 등)
- **API 엔드포인트 삭제/변경**
- 설정 파일 구조 변경

### 🚫 Never (절대 금지)
- **Secret 커밋 금지**: API Key, Password, Token 등
- **하드코딩 금지**: 프로덕션 데이터, mock 데이터
- **물리적 삭제 금지**: Soft Delete 사용
- **Force Push 금지**: main/master 브랜치
- **테스트 스킵 금지**: @skip으로 무시하지 않음

---

## 5. Writing Rules

### REQ/RULE Documents (Authority)
- **결정만 적는다**: 논의/대안은 discussions/에
- **짧게 유지**: 한 REQ = 하나의 명확한 결정
- **Must-Read 필수**: RULE/ADR ID만, 링크 텍스트는 ID
- **Constraints 선택적**: 기능별 추가 제약 시만 작성

### RUN Documents (Execution)
- **1 RUN = 1 목적**: 여러 목적을 섞지 않음
- **Input 명시**: 읽어야 할 문서 ID 목록
- **Verification 명시**: 성공 조건 + Self-Check
- **Output 기록**: 생성/수정 파일 목록

---

## 6. Validation Requirements

### Three-Way ID Consistency
- `**ID**:` metadata (Authority)
- Filename
- Header `[ID]`

All three must match.

### Must-Read Validation
- Must-Read allows only RULE/ADR IDs (CTX is P0 and excluded)
- Link text must be the ID if markdown links are used
- All documents in `**Must-Read**` must exist

---

## 7. Workflow

### Starting a Task
1. Read P0 documents (**CONVENTIONS의 Boundaries 확인**)
2. Read target REQ and its Must-Read
3. Check REQ's Constraints & Boundaries (있는 경우)
4. Create RUN-* document in `04_TASK_LOGS/active/`
5. Implement in small steps

### Before Completing a Step (Self-Check)
- [ ] **Test**: 테스트 통과?
- [ ] **Boundary**: CONVENTIONS Boundaries 준수?
- [ ] **Spec**: REQ와 일치?

### Completing a Step
1. Self-Check 완료 확인
2. Mark RUN as Done
3. Move to `04_TASK_LOGS/archive/YYYY-MM/`
4. Create next step if needed

### When Discussion Needed
1. Create DISC-* in `02_REQUIREMENTS/discussions/`
2. Reference from REQ's `Related` section
3. Update REQ with final decision
"""

SYSTEM_TEMPLATES = {
    "00_SYSTEM/AGENT_RULES.md": AGENT_RULES_TEMPLATE,
}

# ============================================================================
# MIGRATION
# ============================================================================
MIGRATION_MAP = {
    "01_PROJECT_CONTEXT/00_IDENTITY.md": None,
    "01_PROJECT_CONTEXT/01_OVERVIEW.md": None,
    "01_PROJECT_CONTEXT/02_ARCHITECTURE.md": "03_TECH_SPECS/architecture/SYSTEM_ARCHITECTURE.md",
    "01_PROJECT_CONTEXT/03_DATA_MODEL.md": "03_TECH_SPECS/architecture/DATA_MODEL.md",
    "01_PROJECT_CONTEXT/04_AGENT_GUIDE.md": None,
    "02_SERVICES": "02_REQUIREMENTS/features",
    "03_MANAGEMENT/STATUS.md": "04_TASK_LOGS/STATUS.md",
    "03_MANAGEMENT/CHANGELOG.md": "04_TASK_LOGS/CHANGELOG.md",
    "03_MANAGEMENT/WORKLOG.md": None,
    "03_MANAGEMENT/COMPONENTS.md": None,
    "03_MANAGEMENT/MISSING_COMPONENTS.md": None,
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
