# [RULE-META-001] Document Metadata Header Fields

> **ID**: RULE-META-001
> **Domain**: FORMAT
> **Priority**: High
> **Last Updated**: 2026-01-20
> **Must-Read**: RULE-ID-001
> **Template-Version**: 2.4

---

## Rule Statement (최종 결정)

모든 MemoryAtlas 문서는 문서 타입에 따라 정해진 메타데이터 필드를 문서 상단에 포함해야 한다.

---

## Rationale

**Source**: `src/core/config.py:77-85`

```python
HEADER_FIELDS_BY_TYPE = {
    "default": ["**ID**", "**Last Updated**"],
    "features": ["**ID**", "**Domain**", "**Status**", "**Last Updated**", "**Must-Read**"],
    "business_rules": ["**ID**", "**Domain**", "**Priority**", "**Last Updated**", "**Must-Read**"],
    "decisions": ["**Status**", "**Date**"],
    "discussions": ["**ID**", "**Related-REQ**", "**Date**"],
    "runs": ["**ID**", "**Input**", "**Verification**"],
}
```

메타데이터는 문서 자동 색인, 검증, 종속성 추적의 기반이 된다.

---

## Required Fields by Document Type

### 1️⃣ REQ (Feature Requirements)
**Location**: `02_REQUIREMENTS/features/`

```markdown
> **ID**: REQ-[DOMAIN]-[NNN]
> **Domain**: [도메인명]
> **Status**: [Draft | Active | Deprecated]
> **Last Updated**: YYYY-MM-DD
> **Must-Read**: [RULE/ADR ID 목록]
```

### 2️⃣ RULE (Business Rules)
**Location**: `02_REQUIREMENTS/business_rules/`

```markdown
> **ID**: RULE-[DOMAIN]-[NNN]
> **Domain**: [도메인명]
> **Priority**: [Critical | High | Medium | Low]
> **Last Updated**: YYYY-MM-DD
> **Must-Read**: [RULE/ADR ID 목록 또는 None]
```

### 3️⃣ ADR (Architecture Decision Records)
**Location**: `03_TECH_SPECS/decisions/`

```markdown
> **Status**: [Proposed | Accepted | Deprecated | Superseded]
> **Date**: YYYY-MM-DD
```

### 4️⃣ DISC (Discussions)
**Location**: `02_REQUIREMENTS/discussions/`

```markdown
> **ID**: DISC-[DOMAIN]-[NNN]
> **Related-REQ**: [REQ-XXX-NNN 또는 RULE-XXX-NNN]
> **Date**: YYYY-MM-DD
```

### 5️⃣ RUN (Execution Logs)
**Location**: `04_TASK_LOGS/active/`

```markdown
> **ID**: RUN-(REQ|RULE)-[DOMAIN]-[NNN]-step-[NN]
> **Input**: [읽을 문서 ID 목록]
> **Verification**: [검증 조건 한 줄 요약]
```

### 6️⃣ Default (기타 문서)
```markdown
> **ID**: [문서 ID]
> **Last Updated**: YYYY-MM-DD
```

---

## Examples

### ✅ Correct (REQ 문서)

```markdown
# [REQ-AUTH-001] User Login

> **ID**: REQ-AUTH-001
> **Domain**: AUTH
> **Status**: Active
> **Last Updated**: 2026-01-20
> **Must-Read**: RULE-SEC-001, ADR-003
```

### ❌ Incorrect

```markdown
# [REQ-AUTH-001] User Login

> **ID**: REQ-AUTH-001
> **Last Updated**: 2026-01-20
```

**문제**: `**Domain**`, `**Status**`, `**Must-Read**` 필드 누락.

---

## Validation

```bash
python memory_manager.py --lint
```

메타데이터 누락 시 오류:
```
! Missing header fields in 02_REQUIREMENTS/features/REQ-AUTH-001.md: **Domain**, **Must-Read**
Metadata lint: 1 issue(s)
```

---

## Exceptions

**README.md** 파일은 메타데이터 검증에서 제외됨 (`LINT_SKIP_FILES`).
