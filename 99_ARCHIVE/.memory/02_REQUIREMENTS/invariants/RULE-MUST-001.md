# [RULE-MUST-001] Must-Read Field Constraints

> **ID**: RULE-MUST-001
> **Domain**: VALIDATION
> **Priority**: Critical
> **Last Updated**: 2026-01-20
> **Must-Read**: RULE-ID-001
> **Template-Version**: 2.4

---

## Rule Statement (최종 결정)

REQ와 RULE 문서의 `**Must-Read**` 필드는 **RULE 또는 ADR ID만** 포함할 수 있으며, 최소 1개 이상의 ID를 명시해야 한다 (또는 명시적으로 "None" 작성).

---

## Rationale

**Source**: `src/core/config.py:102-104`

```python
MUST_READ_RE = re.compile(r"^\s*>\s*\*\*Must-Read\*\*:\s*(.+)$", re.M)
MUST_READ_ALLOWED_ID_RE = re.compile(r"(?:RULE)-[A-Z]+-\d{3}|ADR-\d{3}")
```

**Source**: `src/core/checks.py:parse_must_read(), check_requirements()`

Must-Read는 **Authority Chain**을 구현:
- REQ (기능) → RULE (공통 규칙) → 구현
- 이를 통해 모든 기능이 비즈니스 규칙을 준수하도록 강제

---

## Allowed ID Types

| Type | Pattern | Example | Why Allowed? |
|------|---------|---------|--------------|
| **RULE** | `RULE-[DOMAIN]-[NNN]` | `RULE-SEC-001` | 비즈니스 규칙 (여러 REQ에서 공통 사용) |
| **ADR** | `ADR-[NNN]` | `ADR-003` | 기술 결정 근거 (구현 방향 제시) |

### ❌ Disallowed (자동 검증 실패)

| Type | Pattern | Example | Why Forbidden? |
|------|---------|---------|----------------|
| REQ | `REQ-[DOMAIN]-[NNN]` | `REQ-AUTH-001` | 기능은 다른 기능에 의존하면 안 됨 (순환 참조 위험) |
| DISC | `DISC-[DOMAIN]-[NNN]` | `DISC-AUTH-001` | 논의는 Reference Layer (LLM 기본 무시) |
| CTX | `CTX-*` | `CTX-CONV-001` | P0 문서는 항상 읽으므로 명시 불필요 |

---

## Format Rules

### 1️⃣ Plain ID (권장)
```markdown
> **Must-Read**: RULE-SEC-001, RULE-DATA-001, ADR-003
```

### 2️⃣ Markdown Link (허용)
```markdown
> **Must-Read**: [RULE-SEC-001](../business_rules/RULE-SEC-001.md), ADR-003
```

**주의**: 링크 사용 시 **링크 텍스트는 반드시 ID여야 함**.

### 3️⃣ None (독립 규칙인 경우)
```markdown
> **Must-Read**: None
```

---

## Examples

### ✅ Correct

```markdown
# REQ 문서
> **Must-Read**: RULE-SEC-001, RULE-DATA-001, ADR-003

# RULE 문서 (다른 RULE 참조)
> **Must-Read**: RULE-CORE-001, ADR-002

# 독립 RULE
> **Must-Read**: None
```

### ❌ Incorrect

```markdown
# 빈 Must-Read (RULE-MUST-001 위반)
> **Must-Read**: 

# REQ 참조 (금지된 타입)
> **Must-Read**: REQ-AUTH-001, RULE-SEC-001

# CTX 참조 (불필요)
> **Must-Read**: CTX-CONV-001, RULE-SEC-001

# 존재하지 않는 ID
> **Must-Read**: RULE-FAKE-999

# 링크 텍스트가 ID 아님
> **Must-Read**: [보안 규칙](../business_rules/RULE-SEC-001.md)
```

---

## Validation

```bash
python memory_manager.py --req
```

**검증 항목**:
1. Must-Read 필드 존재 여부
2. 빈 Must-Read 금지 (최소 1개 또는 "None")
3. RULE/ADR 외 ID 사용 금지
4. 참조된 문서 실제 존재 확인
5. 링크 사용 시 텍스트=ID 확인

**오류 예시**:
```
! Empty **Must-Read**: list in 02_REQUIREMENTS/features/REQ-AUTH-001.md
! Must-Read allows only RULE/ADR IDs in REQ-AUTH-002.md: REQ-DATA-001
! Must-Read reference not found in REQ-AUTH-003.md: RULE-FAKE-999
Requirement check: 3 issue(s)
```

---

## Exceptions

**01_PROJECT_CONTEXT/** 문서들(`CTX-*`)은 Must-Read 필드가 선택적임.
