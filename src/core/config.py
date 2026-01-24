
import re

CURRENT_VERSION = "3.4.1"
ROOT_DIR = ".memory"
TEMPLATE_VERSION = "3.4"  # Template schema version (Quick Start + Direct Execute)

# ============================================================================
# STRUCTURE (v3.1) - Capabilities, Invariants & Competencies Edition
# ============================================================================
# .memory/
# ├── 00_SYSTEM/                  # 시스템 관리 (시스템만 수정)
# ├── 01_PROJECT_CONTEXT/         # [프로젝트 헌법]
# │   ├── 00_GOALS.md
# │   └── 01_CONVENTIONS.md
# ├── 02_REQUIREMENTS/            # [WHAT: Authority Layer]
# │   ├── capabilities/           # REQ-* (기능/행동 - "시스템은 ~해야 한다")
# │   ├── invariants/             # RULE-* (불변 규칙 - "항상 ~이다")
# │   ├── competencies/           # CQ-* (역량 질문 - "시스템은 ~에 답할 수 있는가?")
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
    "00_SYSTEM/mcp",
    "00_SYSTEM/mcp/templates",
    "00_SYSTEM/state",
    "01_PROJECT_CONTEXT",
    "02_REQUIREMENTS/capabilities",
    "02_REQUIREMENTS/invariants",
    "02_REQUIREMENTS/competencies",
    "02_REQUIREMENTS/discussions",
    "02_REQUIREMENTS/discussions/briefs",
    "03_TECH_SPECS/architecture",
    "03_TECH_SPECS/api_specs",
    "03_TECH_SPECS/decisions",
    "04_TASK_LOGS/active",
    "04_TASK_LOGS/archive",
    "98_KNOWLEDGE/troubleshooting",
    "99_ARCHIVE",
    "99_ARCHIVE/discussions",
]

# ============================================================================
# LINT / CHECK CONFIGURATION
# ============================================================================
LINT_DIRS = [
    "01_PROJECT_CONTEXT",
    "02_REQUIREMENTS/capabilities",
    "02_REQUIREMENTS/invariants",
    "02_REQUIREMENTS/competencies",
    "02_REQUIREMENTS/discussions",
    "04_TASK_LOGS/active",
]

LINK_SCAN_DIRS = [
    "01_PROJECT_CONTEXT",
    "02_REQUIREMENTS",
    "03_TECH_SPECS",
    "04_TASK_LOGS",
]

REQ_SCAN_DIRS = [
    "02_REQUIREMENTS/capabilities",
    "02_REQUIREMENTS/invariants",
    "02_REQUIREMENTS/competencies",
]

RUN_SCAN_DIRS = [
    "04_TASK_LOGS/active",
]


BRIEF_SCAN_DIRS = [
    "02_REQUIREMENTS/discussions/briefs",
]

LINT_SKIP_FILES = {"README.md", "00_INDEX.md", "_index.md"}

# Document type-specific header requirements
HEADER_FIELDS_BY_TYPE = {
    "default": ["**ID**", "**Last Updated**"],
    "capabilities": ["**ID**", "**Domain**", "**Status**", "**Last Updated**", "**Must-Read**"],
    "invariants": ["**ID**", "**Domain**", "**Priority**", "**Last Updated**", "**Must-Read**"],
    "competencies": ["**ID**", "**Domain**", "**Status**", "**Last Updated**"],
    "decisions": ["**Status**", "**Date**"],
    "discussions": ["**ID**", "**Related-REQ**", "**Date**"],
    "runs": ["**ID**", "**Input**", "**Verification**"],
    "briefs": ["**ID**", "**Date**"],
}

# ID patterns
REQ_ID_PATTERN = re.compile(r"^REQ-([A-Z]+)-(\d{3})$")
RULE_ID_PATTERN = re.compile(r"^RULE-([A-Z]+)-(\d{3})$")
CQ_ID_PATTERN = re.compile(r"^CQ-([A-Z]+)-(\d{3})$")
ADR_ID_PATTERN = re.compile(r"^ADR-(\d{3})$")
DISC_ID_PATTERN = re.compile(r"^DISC-([A-Z]+)-(\d{3})$")
RUN_ID_PATTERN = re.compile(r"^RUN-(REQ|RULE|BRIEF)-([A-Z]+)-(\d{3})-step-(\d{2})$")
BRIEF_ID_PATTERN = re.compile(r"^BRIEF-([A-Z]+)-(\d{3})$")

# Regex patterns
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")

# Authority source: **ID**: line in document metadata
# Fix A: Include ADR in META_ID_RE
META_ID_RE = re.compile(r"^\s*>\s*\*\*ID\*\*:\s*((?:REQ|RULE|CQ|DISC|RUN|ADR|BRIEF)-[A-Z0-9-]+(?:-step-\d{2})?)\s*$", re.M)

# Must-Read field (v2.2)
MUST_READ_RE = re.compile(r"^\s*>\s*\*\*Must-Read\*\*:\s*(.+)$", re.M)
MUST_READ_ANY_ID_RE = re.compile(r"(?:REQ|RULE|CQ|DISC|CTX)-[A-Z]+-\d{3}|ADR-\d{3}")
MUST_READ_ALLOWED_ID_RE = re.compile(r"(?:RULE)-[A-Z]+-\d{3}|ADR-\d{3}")
MUST_READ_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")

# Header patterns (v2.2.1: Support H1-H3, i.e. #, ##, ###)
# P0 fix: Templates use # [REQ-...] (H1), so regex must match #{1,3}
REQ_HEADER_RE = re.compile(r"^#{1,3}\s+\[(REQ-[A-Z]+-\d{3})\]", re.M)
RULE_HEADER_RE = re.compile(r"^#{1,3}\s+\[(RULE-[A-Z]+-\d{3})\]", re.M)
CQ_HEADER_RE = re.compile(r"^#{1,3}\s+\[(CQ-[A-Z]+-\d{3})\]", re.M)
RUN_HEADER_RE = re.compile(r"^#{1,3}\s+\[(RUN-(?:REQ|RULE|BRIEF)-[A-Z]+-\d{3}-step-\d{2})\]", re.M)
DISC_HEADER_RE = re.compile(r"^#{1,3}\s+\[(DISC-[A-Z]+-\d{3})\]", re.M)
BRIEF_HEADER_RE = re.compile(r"^#{1,3}\s+\[(BRIEF-[A-Z]+-\d{3})\]", re.M)

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

## Capabilities, Invariants & Competencies Model (v3.1)

```
02_REQUIREMENTS/ 구조:
  capabilities/   - REQ-* (기능/행동) "시스템은 ~해야 한다"
  invariants/     - RULE-* (불변 규칙) "항상 ~이다 / ~는 금지"
  competencies/  - CQ-* (역량 질문) "시스템은 ~에 답할 수 있는가?"
  discussions/    - DISC-* (조율 기록) LLM 기본 무시

REQ vs RULE vs CQ 판정:
  REQ  = Input/Output/Acceptance Criteria 필수 (동작 중심)
  RULE = Scope/Violation/Examples 필수 (불변 중심)
  CQ   = Question/Expected Answer/Traceability 필수 (검증 중심)
```

## Quick Navigation

| Folder | Purpose | Authority Level |
|--------|---------|-----------------|
| `01_PROJECT_CONTEXT/` | 프로젝트 헌법 + **Boundaries** | Constitution |
| `02_REQUIREMENTS/capabilities/` | 기능 **결정** (REQ-*) | Authority |
| `02_REQUIREMENTS/invariants/` | 불변 규칙 **결정** (RULE-*) | Authority |
| `02_REQUIREMENTS/competencies/` | 역량 질문 **검증** (CQ-*) | Authority |
| `02_REQUIREMENTS/discussions/` | 조율 기록 (DISC-*) | Reference |
| `03_TECH_SPECS/` | 기술 설계 & ADR | Implementation |
| `04_TASK_LOGS/` | 실행 기록 (RUN-*) | Execution |
| `98_KNOWLEDGE/` | 배운 점 | Asset |

## Start Here (For AI Agents)

### Reading Priority (P0 = Must Read)
1. **P0**: `01_PROJECT_CONTEXT/01_CONVENTIONS.md` - **특히 Boundaries 섹션** ⭐
2. **P0**: Target REQ's `**Must-Read**` field
3. **P1**: `02_REQUIREMENTS/invariants/` (all active)
4. **P1.5**: `02_REQUIREMENTS/competencies/` (referenced CQs only)
5. **P2**: `98_KNOWLEDGE/` (if complex feature)

## 3-Step Workflow (Intake → Plan → Finish)

1. **Intake**: 생각/메모 → BRIEF 생성 (`02_REQUIREMENTS/discussions/briefs/`)
2. **Plan**: BRIEF → RUN 생성 (`04_TASK_LOGS/active/`)
3. **Finish**: 구현 완료 → Status 업데이트 + Git 증거

> MCP 도구: `intake()` → `plan()` → `finish()`

### Execution Checklist
1. [ ] **Intake**: BRIEF 생성 및 검토
2. [ ] **Plan**: RUN 문서 생성 및 검토
3. [ ] 구현 → 테스트 → Git 커밋
4. [ ] **Finish**: Self-Check 통과 후 finish() 호출 (Status → Completed)

## Quick Start (MCP 도구 사용법)

### 1. "Intake 해줘"
```python
intake("사용자 요청 내용", domain="GEN")
```
→ 반환: BRIEF 파일 경로 (예: `BRIEF-GEN-001`)

### 2. "Plan 만들어줘"
```python
plan("BRIEF-GEN-001")
```
→ 반환: RUN ID (예: `RUN-BRIEF-GEN-001-step-01`)

### 3. "작업 완료"
1. RUN 문서의 Steps 실행
2. Self-Check 확인
3. Git 커밋 생성
4. 완료 후:
```python
finish("RUN-BRIEF-GEN-001-step-01", git_hash="abc123")
```
→ Status가 Completed로 변경 + Git 증거 기록

### 예시 대화
```
User: "로그인 기능 추가해줘. intake 해"
LLM:  intake("로그인 기능 추가", domain="AUTH") 호출
LLM:  BRIEF 생성 → 사용자 검토 요청
User: "plan 만들어"
LLM:  plan("BRIEF-AUTH-001") 호출
LLM:  RUN 생성 → 사용자 검토 요청
User: "run 해"
LLM:  RUN Steps 실행 → Self-Check → finish()
```

## Manual Fallback (MCP 없이)

MCP 도구 사용이 불가능하거나 원하지 않는 경우, 동일한 워크플로우를 수동으로 수행할 수 있습니다.

### 1. BRIEF 직접 작성
- **템플릿**: `02_REQUIREMENTS/discussions/briefs/README.md` 참조
- **위치**: `02_REQUIREMENTS/discussions/briefs/BRIEF-DOMAIN-001.md`
- **필수 섹션**: User Request, Intent Summary, Affected Artifacts, Proposed Changes, Verification Criteria

### 2. REQ/RUN 직접 작성
- **REQ 템플릿**: `02_REQUIREMENTS/capabilities/README.md` 참조
- **REQ 위치**: `02_REQUIREMENTS/capabilities/REQ-DOMAIN-001.md`
- **RUN 템플릿**: `04_TASK_LOGS/active/README.md` 참조
- **RUN 위치**: `04_TASK_LOGS/active/RUN-BRIEF-DOMAIN-001-step-01.md`

### 3. 완료 처리 (수동)
- RUN 문서의 Status를 `Completed` 또는 `Failed`로 변경
- Git 커밋 해시를 Evidence에 기록
- RUN은 `active/`에 유지 (이동 없음)

> ⚠️ MCP 도구 사용이 권장됩니다. 수동 프로세스는 동일한 결과를 만들지만 더 많은 작업이 필요합니다.

## Direct Execute (간단한 작업)

다음 조건을 **모두** 만족하면 BRIEF/RUN 없이 바로 실행 가능:

### Skip 가능 조건
- 단일 파일 수정
- 아키텍처 영향 없음
- 명백한 변경 (typo 수정, 단순 버그 픽스)
- 새 의존성 없음
- 검증이 자명함 (에러 해결 = 성공)

### 예시
| 작업 | 경로 |
|------|------|
| README 오타 수정 | ✅ Direct Execute |
| 로그 메시지 추가 | ✅ Direct Execute |
| 단순 import 수정 | ✅ Direct Execute |
| 새 API 엔드포인트 | ❌ 3-Phase 필요 |
| 인증 로직 변경 | ❌ 3-Phase 필요 |
| 다중 파일 리팩토링 | ❌ 3-Phase 필요 |

### 주의사항
- Skip 시에도 **커밋 메시지에 변경 이유 명시**
- 불확실하면 → Intake 진행 권장

### What NOT to Read by Default
- `02_REQUIREMENTS/discussions/` - Only when explicitly referenced
- `04_TASK_LOGS/archive/` - Only for historical context
- `99_ARCHIVE/` - Deprecated content

## Document Map

### 01_PROJECT_CONTEXT (프로젝트 헌법)
- [00_GOALS.md](01_PROJECT_CONTEXT/00_GOALS.md) - 프로젝트 목표
- [01_CONVENTIONS.md](01_PROJECT_CONTEXT/01_CONVENTIONS.md) - 코딩 규칙 + **Boundaries** ⭐

### 02_REQUIREMENTS (요구사항)
- [capabilities/](02_REQUIREMENTS/capabilities/) - 기능 **결정** (REQ-*)
- [invariants/](02_REQUIREMENTS/invariants/) - 불변 규칙 **결정** (RULE-*)
- [competencies/](02_REQUIREMENTS/competencies/) - 역량 질문 **검증** (CQ-*)
- [discussions/](02_REQUIREMENTS/discussions/) - 조율 기록 (DISC-*)

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
3. **P1**: `02_REQUIREMENTS/invariants/` (전체)
4. **P1.5**: `02_REQUIREMENTS/competencies/` (참조된 CQ만)
5. **P2**: `98_KNOWLEDGE/` (복잡한 기능 시)

### Execution Checklist (3-Step Workflow)
1. [ ] **Intake**: BRIEF 생성 및 검토
2. [ ] **Plan**: RUN 문서 생성 및 검토
3. [ ] 구현 → 테스트 → 검증
4. [ ] **Finish**: Self-Check 통과 후 finish() 호출
""",

    "01_PROJECT_CONTEXT/04_AGENT_GUIDE.md": """# Agent Guide

## Source of Truth
- Always start with 00_INDEX.md.
- Prefer .memory documents over ad-hoc assumptions.

## Update Rules
- Update 02_REQUIREMENTS when requirements or specs change.
- Update 01_PROJECT_CONTEXT when architecture or scope changes.
- Update 03_TECH_SPECS after implementing or deferring work.

## 3-Phase Workflow
1. **Intake**: Idea -> BRIEF
2. **Plan**: BRIEF -> RUN
3. **Execute**: RUN -> Code/Test -> Archive

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

## Capabilities, Invariants & Competencies Model (v3.1)

```
문서 등급:
├── capabilities/     → REQ-* (기능/행동) "시스템은 ~해야 한다"
├── invariants/       → RULE-* (불변 규칙) "항상 ~이다 / ~는 금지"
├── competencies/     → CQ-* (역량 질문) "시스템은 ~에 답할 수 있는가?"
└── discussions/      → DISC-* (조율 기록, LLM 기본 무시)
```

## REQ vs RULE vs CQ 판정 기준

### REQ (capabilities/에만 존재)
- **문장 형태**: "시스템은 ~~해야 한다" (동작 중심)
- **필수 섹션**: Input, Output, Acceptance Criteria
- **규칙 작성 금지**: 형식/제약/금지는 Must-Read로 RULE 참조

### RULE (invariants/에만 존재)
- **문장 형태**: "항상 ~~이다 / ~~는 금지" (불변 중심)
- **필수 섹션**: Scope, Violation 판정 기준, Examples
- **테스트 가능**: 단독으로 참/거짓 판정 가능해야 함

### CQ (competencies/에만 존재)
- **문장 형태**: "시스템은 ~~에 답할 수 있는가?" (검증 중심)
- **필수 섹션**: Question, Expected Answer, Traceability
- **REQ/RULE 연결**: Solves by / Constrained by 링크로 추적성 확보

## Structure

```
02_REQUIREMENTS/
├── capabilities/       # REQ-* (기능/행동)
│   └── REQ-AUTH-001.md
├── invariants/         # RULE-* (불변 규칙)
│   └── RULE-ID-001.md
├── competencies/       # CQ-* (역량 질문)
│   └── CQ-AUTH-001.md
└── discussions/        # DISC-* (조율 기록)
    └── DISC-AUTH-001.md
```

## Naming Convention (STRICT)

| Type | Pattern | Example | Location |
|------|---------|---------|----------|
| Capability | `REQ-[DOMAIN]-[NNN].md` | `REQ-AUTH-001.md` | capabilities/ |
| Invariant | `RULE-[DOMAIN]-[NNN].md` | `RULE-ID-001.md` | invariants/ |
| Competency | `CQ-[DOMAIN]-[NNN].md` | `CQ-AUTH-001.md` | competencies/ |
| Discussion | `DISC-[DOMAIN]-[NNN].md` | `DISC-AUTH-001.md` | discussions/ |

## Must-Read Field (Required)

모든 REQ/RULE 문서에는 `**Must-Read**` 필드가 필수입니다:

```markdown
> **Must-Read**: RULE-ID-001, RULE-META-001, ADR-003
```

이 필드에 나열된 문서는 해당 REQ 구현 시 **반드시** 읽어야 합니다.

CQ 문서는 Must-Read 대신 **Traceability 섹션**으로 REQ/RULE을 연결합니다.

- Must-Read allows only RULE/ADR IDs (CTX is P0 and not allowed here).
- If you use markdown links, the link text must be the ID (e.g. `[RULE-ID-001](invariants/RULE-ID-001.md)`).

## Partial Updates Policy (Recommended)

- Keep REQ as the full contract; `Status=Active` means the whole REQ is executable.
- Do not mix "pending/later" items inside an Active REQ. Use DISC or a new Draft REQ.
- When only part changes, narrow scope in RUN (In Scope / Out of Scope) and reference the target sections.
- Record evidence in RUN for "already implemented" vs "needs work":
  tests passed, commands run, and code locations.

### When to Revisit a Pending Section Model

Adopt a formal Pending section only if at least two are true:
- A single REQ routinely contains 10+ sub-features and only a subset is delivered each time.
- Agents frequently misjudge scope, causing repeated rework.
- There are multiple collaborators and explicit sprint deferrals are required.
- Roadmap-level proposals must live inside the REQ.

## MCP Automation Notes

- `Automator.apply_req(req_id[, dry_run, create_spec])` drives the pipeline: validate REQ, build a spec draft (optional), create a RUN, and generate DISC drafts on failure.
- The CLI exposes `python memory_manager.py apply-req --id REQ-XXX-001 [--dry-run] [--no-spec]`; it prints artifacts or failure/discussion links.
- FastMCP agents can call `src/mcp_server.py::apply_req` to run the same flow and receive a JSON-like report.
- Read-only MCP helpers: `req_status(req_id)` for readiness checks, `run_report(run_id)` for structured RUN summaries.


""",

    "02_REQUIREMENTS/capabilities/README.md": f"""# Capabilities (REQ-*)

> **Template-Version**: {TEMPLATE_VERSION}
>
> **"시스템은 ~해야 한다"** 형태의 기능/행동을 정의합니다.
> 논의/대안 검토는 `../discussions/`에 작성하세요.

## REQ 판정 기준

- ✅ "시스템은 ~~해야 한다"로 시작 가능 (동작 중심)
- ✅ Input / Output / Acceptance Criteria 필수
- ❌ 규칙/형식/제약은 본문에 쓰지 말고 Must-Read로 RULE 참조

## Template

```markdown
# [REQ-XXX-001] Capability Name

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

## In/Out of Scope (Optional)

### In Scope
- (이 기능에 포함되는 것)

### Out of Scope
- (이 기능에 포함되지 않는 것)

## Related

- Discussion: [DISC-XXX-001](../discussions/DISC-XXX-001.md)
- Tech Spec: [API Spec](../../03_TECH_SPECS/api_specs/)
```

## Rules

1. **동작만 적는다**: 규칙/제약은 invariants/에
2. **짧게 유지**: 한 REQ = 하나의 명확한 기능
3. **Must-Read 필수**: RULE/ADR ID만, 링크 텍스트는 ID
4. **ID 일치**: 파일명 = **ID**: = 헤더 [ID]
5. **AC 필수**: Acceptance Criteria 없으면 REQ가 아님
""",

    "02_REQUIREMENTS/invariants/README.md": f"""# Invariants (RULE-*)

> **Template-Version**: {TEMPLATE_VERSION}
>
> **"항상 ~이다 / ~는 금지"** 형태의 불변 규칙을 정의합니다.

## RULE 판정 기준

- ✅ "항상 ~~이다 / ~~는 금지 / ~~를 만족해야 한다"로 시작 가능 (불변 중심)
- ✅ Scope / Violation 판정 기준 / Examples 필수
- ✅ 단독으로 참/거짓 판정 가능 (테스트 가능한 문장)

## Template

```markdown
# [RULE-XXX-001] Invariant Name

> **ID**: RULE-XXX-001
> **Domain**: (도메인)
> **Priority**: [Critical | High | Medium | Low]
> **Last Updated**: YYYY-MM-DD
> **Must-Read**: RULE-XXX-001, ADR-XXX
> **Template-Version**: {TEMPLATE_VERSION}

---

## Rule Statement (최종 결정)

(규칙을 명확하게 한 문장으로. "항상 ~이다" 또는 "~는 금지")

## Scope

(이 규칙이 적용되는 범위)

## Violation (위반 판정 기준)

(어떤 경우 이 규칙을 위반한 것인가?)

## Examples

### Correct
(올바른 예시)

### Incorrect
(잘못된 예시)

## Exceptions

(예외 상황이 있다면)
```

## Common Domains

- **ID**: ID 명명 규칙
- **META**: 메타데이터 규칙
- **DATA**: 데이터 형식, 저장 규칙
- **SEC**: 보안 규칙
- **VER**: 버전 관리 규칙

## Rules

1. **불변만 적는다**: 기능/동작은 capabilities/에
2. **테스트 가능**: 단독으로 참/거짓 판정 가능해야 함
3. **Violation 필수**: 위반 기준 없으면 RULE이 아님
4. **ID 일치**: 파일명 = **ID**: = 헤더 [ID]
""",

    "02_REQUIREMENTS/competencies/README.md": f"""# Competencies (CQ-*)

> **Template-Version**: {TEMPLATE_VERSION}
>
> 시스템이 반드시 답해야 하는 질문(검증 시나리오)을 정의합니다.
> CQ는 REQ/RULE의 완결성을 확인하는 테스트 케이스 역할입니다.

## CQ 판정 기준

- ✅ "시스템은 ~~에 답할 수 있는가?" 형태 (검증 중심)
- ✅ Question / Expected Answer / Traceability 필수
- ✅ REQ/RULE과 링크로 추적성 확보

## Template

```markdown
# [CQ-XXX-001] Competency Question Title

> **ID**: CQ-XXX-001
> **Domain**: (도메인)
> **Status**: [Draft | Active | Deprecated]
> **Last Updated**: YYYY-MM-DD
> **Template-Version**: {TEMPLATE_VERSION}

---

## Question
(검증 질문)

## Expected Answer (Criteria)
1. ...
2. ...

## Traceability
- **Solves by**: [REQ-XXX-001](../capabilities/REQ-XXX-001.md)
- **Constrained by**: [RULE-XXX-001](../invariants/RULE-XXX-001.md)
```

## Rules

1. **질문 중심**: 구현 방법이 아니라 답변 가능성에 집중
2. **추적성 필수**: 최소 1개 REQ/RULE 링크
3. **ID 일치**: 파일명 = **ID**: = 헤더 [ID]
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

    "02_REQUIREMENTS/discussions/briefs/README.md": f"""# Briefs (Intake Layer)

> **Template-Version**: {TEMPLATE_VERSION}
>
> **Idea/User Request**를 빠르고 가볍게 기록하는 곳입니다.
> `intake()` 명령어를 통해 생성됩니다.

## Workflow

1. `intake("설명")` -> `BRIEF-XXX-001.md` 생성
2. BRIEF 검토 및 구체화 (LLM/Human)
3. `plan("BRIEF-ID")` -> `RUN` 및 `REQ` 생성

## Template

```markdown
# [BRIEF-DOMAIN-001] Title

> **ID**: BRIEF-DOMAIN-001
> **Date**: YYYY-MM-DD
> **Status**: Active

## 1. User Request (원본 요청)
(사용자의 원래 텍스트 보존)

## 2. Intent Summary (의도 요약)
- **Goal**: ...
- **Problem**: ...

## 3. Affected Artifacts
- Create: ...
- Modify: ...

## 4. Proposed Changes
1. ...
2. ...

## 5. Verification Criteria
- [ ] ...
```
""",

    # =========================================================================
    # 02_REQUIREMENTS/_index.md (Human Entry Point)
    # =========================================================================
    "02_REQUIREMENTS/_index.md": f"""# 02_REQUIREMENTS 읽기 가이드

> **Template-Version**: {TEMPLATE_VERSION}
>
> 이 문서는 사람과 LLM이 요구사항 문서를 **어디서부터 읽어야 하는지** 안내합니다.

## 📖 읽는 순서

### 1단계: 전역 규칙 (필수)

아래 규칙들은 모든 REQ 구현 전에 반드시 읽어야 합니다:

| 순서 | 문서 | 설명 |
|------|------|------|
| 1 | [RULE-ID-001](invariants/RULE-ID-001.md) | ID 명명 규칙 |
| 2 | [RULE-META-001](invariants/RULE-META-001.md) | 메타데이터 필드 규칙 |
| 3 | [RULE-MUST-001](invariants/RULE-MUST-001.md) | Must-Read 참조 규칙 |

### 2단계: 대상 기능 및 검증 (선택)

1. 구현할 기능의 REQ 문서를 읽습니다.
2. 해당 기능에 연결된 CQ 문서를 읽습니다. (있다면)
3. REQ와 CQ가 `**Must-Read**`로 참조하는 RULE/ADR을 읽습니다.

## 🏷️ 폴더 구조

| 폴더 | 질문 | 내용 |
|------|------|------|
| `capabilities/` | "무엇을 만드는가?" | REQ-* (기능/행동) |
| `invariants/` | "무엇이 항상 참인가?" | RULE-* (불변 규칙) |
| `competencies/` | "무엇을 해결하는가?" | CQ-* (역량 질문/시나리오) |
| `discussions/` | "어떻게 결정했는가?" | DISC-* (조율 기록) |

## REQ vs RULE vs CQ 빠른 판정

```
REQ (capabilities/)
  → "시스템은 ~해야 한다" (동작 중심)
  → Input/Output/AC 필수

RULE (invariants/)
  → "항상 ~이다 / ~는 금지" (불변 중심)
  → Scope/Violation/Examples 필수

CQ (competencies/)
  → "시스템은 ~에 답할 수 있는가?" (검증 중심)
  → Question/Expected Answer/Traceability 필수
```

## 🔗 Quick Links

- 구조 설명: [README.md](README.md)
- 프로젝트 규칙: [01_CONVENTIONS.md](../01_PROJECT_CONTEXT/01_CONVENTIONS.md)

## ⚠️ 주의사항

- `competencies/`는 **참조된 경우에만 읽습니다** (REQ/CQ 연결 시)
- `discussions/`는 **기본적으로 읽지 않습니다** (명시적 참조 시만)
- 각 REQ의 `**Must-Read**` 필드가 **읽기 우선순위의 권위**입니다
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

## Scope for Partial Updates

When only part of a REQ changes, define In Scope / Out of Scope in the RUN.
Keep the REQ as the full contract; use DISC or a new Draft REQ for pending work.

""",

    "04_TASK_LOGS/active/README.md": f"""# Active Tasks (Execution)

> **Template-Version**: {TEMPLATE_VERSION}

## Dashboard (자동 갱신)

| Status | RUN ID | Started | Summary | Git |
|--------|--------|---------|---------|-----|
| (자동 생성) | | | | |

> 이 테이블은 `--runs` 명령 또는 시스템 업데이트 시 자동 갱신됩니다.

## RUN Document Template

```markdown
# [RUN-REQ-XXX-001-step-01] Step Title

> **ID**: RUN-REQ-XXX-001-step-01
> **Summary**: (사람용 1줄 요약)
> **Status**: Active | Completed | Failed
> **Started**: YYYY-MM-DD
> **Completed**: (완료 시 자동 기록)
> **Git**: (커밋 해시 또는 no-commit)
> **Input**: BRIEF-XXX-001, REQ-XXX-001
> **Verification**: (성공 조건 - 한 줄 요약)
> **Template-Version**: {TEMPLATE_VERSION}

---

## Objective

(이 단계의 목표 - 하나만)

## Scope

### In Scope

- (List the parts of the REQ you will change)

### Out of Scope

- (Explicitly state what will not be touched this run)

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

## Evidence (Implementation Proof)

- Tests: (what passed)
- Commands: (what was executed)
- Code references: (files/functions showing current behavior)
- **Git**: (커밋 해시 기록)

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
6. **Scope 명확화**: In Scope / Out of Scope 구분 필수
7. **Evidence 확보**: Git 커밋 해시 필수 기록

## Archive 정책 (v3.4+)

- **RUN은 이동하지 않음**: 모든 RUN은 `active/`에 유지
- **완료 표시**: Status 메타데이터로만 관리 (Active → Completed/Failed)
- **증거**: Git 커밋 해시가 유일한 증거
- **가독성**: 이 README의 Dashboard 테이블로 조회""",

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
> - **ONBOARDING_PROMPT.md**: 시스템 업데이트 시 덮어쓰기됨
> - **scripts/**: 시스템 업데이트 시 덮어쓰기됨
> - **mcp/**: auto-generated MCP definitions (overwritten on update)
> - 사용자/에이전트 수정 -> 다음 업데이트에서 원복
>
> ### For Customization
> 커스텀 규칙이 필요하면 `01_PROJECT_CONTEXT/01_CONVENTIONS.md`에 작성하세요.

## MCP Auto-Launch

- STDIO clients can auto-spawn the MCP server using the configured command.
- This means the server does not need to be running manually in the background.
- HTTP mode still requires a long-running server process.
- Use `python memory_manager.py --bootstrap-mcp --target <client> --os <windows|unix>` to generate MCP bootstrap prompts and templates.
- Validate with `python memory_manager.py --mcp-check --target <client>`.

## Version Info

- **Manager Version**: {CURRENT_VERSION}
- **Template Version**: {TEMPLATE_VERSION}""",

    # =========================================================================
    # GETTING_STARTED.md (User-facing Guide)
    # =========================================================================
    "GETTING_STARTED.md": f"""# 🚀 MemoryAtlas 시작하기

> **Version**: {CURRENT_VERSION} | **Template**: {TEMPLATE_VERSION}
>
> 이 문서는 MemoryAtlas를 처음 사용하는 사용자를 위한 설정 가이드입니다.

## Quick Start

```bash
# 1. 온보딩 시작 (대화형 설정)
python memory_manager.py --guide

# 2. 출력된 프롬프트를 LLM에게 전달
# 3. LLM의 질문에 답하며 설정 완료
```

## 설정 체크리스트

### Phase 1: 프로젝트 기본 정보
- [ ] 프로젝트 이름 설정 <!-- id:phase1.project_name -->
- [ ] 프로젝트 목표 정의 (`01_PROJECT_CONTEXT/00_GOALS.md`) <!-- id:phase1.project_goal -->
- [ ] 기술 스택 결정 <!-- id:phase1.tech_stack -->

### Phase 2: 개발 규칙 설정
- [ ] 코딩 컨벤션 정의 (`01_PROJECT_CONTEXT/01_CONVENTIONS.md`) <!-- id:phase2.coding_style -->
- [ ] Boundaries 설정 (금지 사항) <!-- id:phase2.boundaries -->
- [ ] 테스트 정책 결정 <!-- id:phase2.testing_policy -->

### Phase 3: MCP 연동 (선택)
- [ ] MCP 서버 설정 확인 <!-- id:phase3.mcp_server -->
- [ ] 클라이언트 연동 테스트 <!-- id:phase3.mcp_client -->
- [ ] `intake()`, `plan()`, `finish()` 동작 확인 <!-- id:phase3.mcp_tools -->

## 설정 완료 후

설정이 완료되면 다음 명령어를 사용할 수 있습니다:

| 명령어 | 설명 |
|--------|------|
| `intake("요청")` | 아이디어 → BRIEF 생성 |
| `plan("BRIEF-ID")` | BRIEF → RUN 생성 |
| `finish("RUN-ID", git_hash="...")` | Status 완료 + Git 증거 기록 |

## 도움이 필요하면

- 📖 [README.md](../README.md) - 전체 시스템 이해
- 📋 [00_INDEX.md](00_INDEX.md) - 문서 네비게이션
- 🔧 `python memory_manager.py --doctor` - 시스템 검증

## 온보딩 상태

> **Status**: {{STATUS}}
> **Last Updated**: {{LAST_UPDATED}}

## 사용자 메모
<!-- NOTES:BEGIN -->
(자유롭게 기록)
<!-- NOTES:END -->
""",

    # =========================================================================
    # 00_SYSTEM/ONBOARDING_PROMPT.md (CLI Reference for LLM)
    # =========================================================================
    "00_SYSTEM/ONBOARDING_PROMPT.md": f"""# MemoryAtlas 온보딩 프롬프트

> **Version**: {CURRENT_VERSION}
>
> 이 파일은 `--guide` 명령 시 LLM에게 전달되는 온보딩 프롬프트입니다.

---

## 🤖 LLM 지시사항

당신은 MemoryAtlas 프로젝트 설정을 도와주는 온보딩 어시스턴트입니다.
사용자가 이 프롬프트를 전달하면, 아래 단계에 따라 대화하며 설정을 완료하세요.

### 진행 규칙
1. 시작 시 `GETTING_STARTED.md`를 읽고 Status/체크리스트를 확인한 뒤, 미완료 단계부터 이어서 진행하세요
2. 한 번에 1-2개 질문만 하세요
3. 사용자 답변을 받으면 해당 파일에 직접 반영하세요
4. 각 Phase 완료 시 `GETTING_STARTED.md`의 체크리스트와 Status/Last Updated를 업데이트하세요
5. 체크리스트 변경 시 `00_SYSTEM/state/onboarding.json`도 함께 갱신하세요
6. 모든 Phase 완료 시 축하 메시지와 다음 단계 안내

---

## Phase 1: 프로젝트 기본 정보

### Q1. 프로젝트 이름
> "이 프로젝트의 이름은 무엇인가요?"

→ 반영 위치: `01_PROJECT_CONTEXT/00_GOALS.md` > Name

### Q2. 프로젝트 목표
> "이 프로젝트가 해결하려는 문제는 무엇인가요? 한 문장으로 설명해주세요."

→ 반영 위치: `01_PROJECT_CONTEXT/00_GOALS.md` > One-Line Summary

### Q3. 기술 스택
> "사용할 주요 기술 스택은 무엇인가요? (예: Python, TypeScript, React 등)"

→ 반영 위치: `01_PROJECT_CONTEXT/00_GOALS.md` > Tech Stack

---

## Phase 2: 개발 규칙 설정

### Q4. 코딩 스타일
> "선호하는 코딩 스타일이 있나요? (예: PEP8, ESLint, Prettier 등)"

→ 반영 위치: `01_PROJECT_CONTEXT/01_CONVENTIONS.md` > Coding Style

### Q5. Boundaries (금지 사항)
> "이 프로젝트에서 절대 해서는 안 되는 것이 있나요? (예: 특정 라이브러리 사용 금지, 특정 패턴 금지)"

→ 반영 위치: `01_PROJECT_CONTEXT/01_CONVENTIONS.md` > Boundaries

### Q6. 테스트 정책
> "테스트는 어떻게 진행할 예정인가요? (예: pytest, jest, 커버리지 목표 등)"

→ 반영 위치: `01_PROJECT_CONTEXT/01_CONVENTIONS.md` > Testing Policy

---

## Phase 3: MCP 연동 확인 (선택)

### Q7. MCP 사용 여부
> "MCP(Model Context Protocol) 도구를 사용할 예정인가요? (intake, plan, run 자동화)"

- Yes → MCP 설정 안내 진행
- No → Phase 완료

### Q8. MCP 테스트 (Yes인 경우)
> "MCP 서버가 정상 동작하는지 확인해보겠습니다."

실행: `python memory_manager.py --mcp-check`

---

## 완료 시 행동

1. `GETTING_STARTED.md`의 모든 체크박스를 [x]로 변경
2. `GETTING_STARTED.md`의 Status를 "Completed"로 변경하고 Last Updated를 갱신
3. `00_SYSTEM/state/onboarding.json`의 항목을 Completed로 갱신
4. 사용자에게 다음 안내:
   - "설정이 완료되었습니다! 이제 'intake 해줘'로 첫 작업을 시작해보세요."

---

## 현재 진행 상태

> 실제 진행 상태는 `GETTING_STARTED.md`에서 관리합니다. 이 섹션은 참고용입니다.

- Phase 1: [ ] Not Started
- Phase 2: [ ] Not Started
- Phase 3: [ ] Not Started
- Overall: [ ] Not Started
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
3. **P1**: `02_REQUIREMENTS/invariants/` (전체)
4. **P1.5**: `02_REQUIREMENTS/competencies/` (참조된 CQ만)
5. **P2**: `98_KNOWLEDGE/` (복잡한 기능 시)

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
# MCP DEFINITIONS (SYSTEM-GENERATED)
# ============================================================================
MCP_DEFINITIONS = {
    "apply_req": {
        "signature": "apply_req(req_id, dry_run=false, create_spec=\"auto\")",
        "summary": "Orchestrate the REQ -> RUN pipeline with validation gates.",
        "inputs": [
            "`req_id` (str): Target REQ ID.",
            "`dry_run` (bool): Preview only.",
            "`create_spec` (bool | \"auto\"): Create spec draft when true or auto-triggered.",
        ],
        "outputs": [
            "RUN document created/updated in `04_TASK_LOGS/active/`.",
            "DISC draft path on failure.",
            "Stage/result report.",
        ],
        "behavior": [
            "Requires REQ `Status=Active`.",
            "Runs `validate(lint)`, `validate(req)`, `validate(links)` gates.",
            "Creates 03 specs when `create_spec` is true or auto-triggered.",
            "Does not edit code by default.",
        ],
    },
    "apply_req_full": {
        "signature": "apply_req_full(req_id, dry_run=false)",
        "summary": "One-shot orchestration that drives the state machine and returns follow-up hints.",
        "inputs": [
            "`req_id` (str): Target REQ ID.",
            "`dry_run` (bool): Preview only.",
        ],
        "outputs": [
            "State-aware report (`state`, `run_id`, `next_action`).",
            "`instructions` plus `continue_with` / `continue_args` for client-driven steps.",
            "DISC draft path on failure.",
        ],
        "behavior": [
            "Runs lint/req/links validation on the first pass.",
            "Creates RUN when validation passes.",
            "Returns implementation instructions; code edits are performed by the client/agent.",
            "Runs `--doctor` and finalizes when state is ready.",
        ],
    },
    "continue_req": {
        "signature": "continue_req(req_id, implementation_done=false)",
        "summary": "Advance the REQ state machine after implementation or verification.",
        "inputs": [
            "`req_id` (str): Target REQ ID.",
            "`implementation_done` (bool): Set true when implementation is complete.",
        ],
        "outputs": [
            "State-aware report with next action and any validation errors.",
        ],
        "behavior": [
            "Transitions RUN_CREATED → IMPLEMENTING.",
            "Transitions IMPLEMENTING → VERIFYING/READY_TO_FINALIZE based on checks.",
            "Re-runs validation gates when requested.",
        ],
    },
    "validate": {
        "signature": "validate(scope)",
        "summary": "Run a single validation check and return issue count.",
        "inputs": [
            "`scope` (str): lint | req | links | doctor.",
        ],
        "outputs": [
            "Issue count and console report.",
        ],
        "behavior": [
            "Uses the same checks as `memory_manager.py`.",
        ],
    },
    "create_run": {
        "signature": "create_run(req_id)",
        "summary": "Create a RUN document from template for a REQ.",
        "inputs": [
            "`req_id` (str): Target REQ ID.",
        ],
        "outputs": [
            "RUN document created in `04_TASK_LOGS/active/`.",
        ],
        "behavior": [
            "Includes Objective/Scope/Plan, Design Summary, Validation Gates, Exit Criteria.",
            "Keeps required RUN metadata fields.",
        ],
    },
    "finish": {
        "signature": "finish(run_id, success=True, git_hash='')",
        "summary": "Mark a RUN as completed with Git evidence.",
        "inputs": [
            "`run_id` (str): RUN ID.",
            "`success` (bool): Whether the run succeeded.",
            "`git_hash` (str): Git commit hash as evidence.",
        ],
        "outputs": [
            "RUN updated in `04_TASK_LOGS/active/` (no archive move).",
        ],
        "behavior": [
            "Updates Status to Completed/Failed.",
            "Records Git hash as evidence.",
            "RUN stays in active/ (v3.4+ policy).",
        ],
    },
    "finalize_run": {
        "signature": "finalize_run(run_id, success=True, git_hash='')",
        "summary": "(Alias) See finish().",
        "inputs": ["`run_id` (str)", "`success` (bool)", "`git_hash` (str)"],
        "outputs": ["Same as finish()."],
        "behavior": ["Alias for finish() - kept for backward compatibility."],
    },
    "create_disc_from_failure": {
        "signature": "create_disc_from_failure(context)",
        "summary": "Generate a DISC draft for a failed stage.",
        "inputs": [
            "`context` (dict): stage, errors, files, rules, logs, req_id/target_id.",
        ],
        "outputs": [
            "DISC draft created in `02_REQUIREMENTS/discussions/`.",
        ],
        "behavior": [
            "Includes summary, evidence, hypotheses, fix options, next steps.",
            "One DISC per failure event.",
        ],
    },
    "intake": {
        "signature": "intake(description, domain='GEN')",
        "summary": "Intake a new user request and create a BRIEF document.",
        "inputs": [
            "`description` (str): User request logic/features.",
            "`domain` (str): Domain code (default 'GEN')."
        ],
        "outputs": [
            "BRIEF document path (key: `brief_path`)."
        ],
        "behavior": [
            "Creates a new BRIEF in active logs.",
            "Use this to start a new feature or task."
        ],
    },
    "plan": {
        "signature": "plan(brief_id)",
        "summary": "Create a RUN document from an existing BRIEF.",
        "inputs": [
            "`brief_id` (str): Target Brief ID."
        ],
        "outputs": [
            "RUN ID (key: `run_id`).",
            "RUN document path (key: `run_path`)."
        ],
        "behavior": [
            "Creates a RUN document linked to the Brief.",
            "Auto-creates/updates REQ documents.",
            "Moves workflow from Intake to Execution."
        ],
    },
    "plan_from_brief": {
        "signature": "plan_from_brief(brief_id)",
        "summary": "(Alias) See plan().",
        "inputs": ["`brief_id` (str)"],
        "outputs": ["Same as plan()."],
        "behavior": ["Alias for plan() - kept for backward compatibility."],
    },
    "apply_req": {
        "signature": "apply_req(req_id, dry_run=False) (Deprecated)",
        "summary": "(Deprecated) Use plan() instead.",
        "inputs": ["`req_id` (str)", "`dry_run` (bool)"],
        "outputs": ["Report dict"],
        "behavior": ["Triggers deprecation warning."],
    },
    "apply_req_full": {
        "signature": "apply_req_full(req_id) (Deprecated)",
        "summary": "(Deprecated) One-shot orchestration.",
        "inputs": ["`req_id` (str)"],
        "outputs": ["State dict"],
        "behavior": ["See plan()."],
    },
    "req_status": {
        "signature": "req_status(req_id)",
        "summary": "Inspect REQ readiness without executing pipeline.",
        "inputs": [
            "`req_id` (str): Target REQ ID.",
        ],
        "outputs": [
            "`status`: metadata status value.",
            "`metadata`: parsed REQ metadata.",
            "`readiness`: true/false.",
            "`blocking_issues`: list of reasons.",
        ],
        "behavior": [
            "Does not write any files.",
            "Useful for preflight checks in UIs.",
        ],
    },
    "run_report": {
        "signature": "run_report(run_id)",
        "summary": "Return a structured summary of a RUN document.",
        "inputs": [
            "`run_id` (str): RUN ID.",
        ],
        "outputs": [
            "`objective`, `scope`, `status`, `validation_state`, `artifacts`.",
        ],
        "behavior": [
            "Read-only; does not move or update RUN files.",
        ],
    },
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
- `02_REQUIREMENTS/invariants/` (all active)
- `02_REQUIREMENTS/competencies/` (referenced CQs only)
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
    "00_SYSTEM/ONBOARDING_PROMPT.md": DOC_TEMPLATES["00_SYSTEM/ONBOARDING_PROMPT.md"],
}

# README files that should be updated on version upgrade
# These are system-managed and will be overwritten during update
UPDATABLE_READMES = [
    "00_INDEX.md",
    "00_SYSTEM/README.md",
    "02_REQUIREMENTS/README.md",
    "02_REQUIREMENTS/_index.md",
    "02_REQUIREMENTS/capabilities/README.md",
    "02_REQUIREMENTS/invariants/README.md",
    "02_REQUIREMENTS/competencies/README.md",
    "02_REQUIREMENTS/discussions/README.md",
    "03_TECH_SPECS/README.md",
    "04_TASK_LOGS/README.md",
    "04_TASK_LOGS/active/README.md",
]

# ============================================================================
# MIGRATION
# ============================================================================

# v1.x → v2.x migration (legacy)
MIGRATION_MAP_V1 = {
    "01_PROJECT_CONTEXT/00_IDENTITY.md": None,
    "01_PROJECT_CONTEXT/01_OVERVIEW.md": None,
    "01_PROJECT_CONTEXT/02_ARCHITECTURE.md": "03_TECH_SPECS/architecture/SYSTEM_ARCHITECTURE.md",
    "01_PROJECT_CONTEXT/03_DATA_MODEL.md": "03_TECH_SPECS/architecture/DATA_MODEL.md",
    "01_PROJECT_CONTEXT/04_AGENT_GUIDE.md": None,
    "02_SERVICES": "02_REQUIREMENTS/capabilities",
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

# v2.x → v3.0 migration (capabilities & invariants)
MIGRATION_MAP_V2_TO_V3 = {
    "02_REQUIREMENTS/features": "02_REQUIREMENTS/capabilities",
    "02_REQUIREMENTS/business_rules": "02_REQUIREMENTS/invariants",
}

# Combined for backward compatibility
MIGRATION_MAP = {**MIGRATION_MAP_V1, **MIGRATION_MAP_V2_TO_V3}

LEGACY_DIRS_TO_ARCHIVE = [
    "02_SERVICES",
    "03_MANAGEMENT",
    "90_TOOLING",
]
