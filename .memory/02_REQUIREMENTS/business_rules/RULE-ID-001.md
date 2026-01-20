# [RULE-ID-001] Document ID Naming Convention

> **ID**: RULE-ID-001
> **Domain**: VALIDATION
> **Priority**: Critical
> **Last Updated**: 2026-01-20
> **Must-Read**: RULE-DIR-001
> **Template-Version**: 2.4

---

## Rule Statement (최종 결정)

모든 MemoryAtlas 문서 ID는 특정 패턴을 따라야 하며, 각 문서 타입별로 정해진 형식을 준수해야 한다.

---

## Rationale

**Source**: `src/core/config.py:87-92`

코드에 하드코딩된 ID 검증 패턴들:
```python
REQ_ID_PATTERN = re.compile(r"^REQ-([A-Z]+)-(\d{3})$")
RULE_ID_PATTERN = re.compile(r"^RULE-([A-Z]+)-(\d{3})$")
ADR_ID_PATTERN = re.compile(r"^ADR-(\d{3})$")
DISC_ID_PATTERN = re.compile(r"^DISC-([A-Z]+)-(\d{3})$")
RUN_ID_PATTERN = re.compile(r"^RUN-(REQ|RULE)-([A-Z]+)-(\d{3})-step-(\d{2})$")
```

이 규칙이 없으면 문서 ID 검증(3-way consistency)이 불가능하고, 자동화된 링크 검증이 작동하지 않는다.

---

## ID Formats by Document Type

| Document Type | Pattern | Example | Location |
|---------------|---------|---------|----------|
| **REQ** (Feature) | `REQ-[DOMAIN]-[NNN]` | `REQ-AUTH-001` | `02_REQUIREMENTS/features/` |
| **RULE** (Business Rule) | `RULE-[DOMAIN]-[NNN]` | `RULE-DATA-001` | `02_REQUIREMENTS/business_rules/` |
| **ADR** (Architecture Decision) | `ADR-[NNN]` | `ADR-001` | `03_TECH_SPECS/decisions/` |
| **DISC** (Discussion) | `DISC-[DOMAIN]-[NNN]` | `DISC-AUTH-001` | `02_REQUIREMENTS/discussions/` |
| **RUN** (Execution Log) | `RUN-(REQ\|RULE)-[DOMAIN]-[NNN]-step-[NN]` | `RUN-REQ-AUTH-001-step-01` | `04_TASK_LOGS/active/` |

### Format Rules:
- **[DOMAIN]**: 대문자 영문자만 (예: `AUTH`, `DATA`, `PAYMENT`)
- **[NNN]**: 3자리 숫자 (001~999)
- **[NN]**: 2자리 숫자 (RUN step번호, 01~99)

---

## Examples

### ✅ Correct

```
REQ-AUTH-001.md
RULE-SEC-001.md
ADR-003.md
DISC-PAYMENT-001.md
RUN-REQ-AUTH-001-step-01.md
```

### ❌ Incorrect

```
REQ-auth-001.md           # 소문자 도메인 금지
RULE-DATA-1.md            # 3자리 숫자 필수 (001)
ADR-SEC-001.md            # ADR은 도메인 없음 (ADR-001)
RUN-AUTH-001.md           # RUN은 REQ/RULE 명시 필수
REQ-AUTH-1000.md          # 3자리 초과 금지
```

---

## Exceptions

없음. 이 규칙은 예외 없이 적용된다.

---

## Validation

`--doctor` 명령어가 이 규칙을 자동으로 검증한다:
```bash
python memory_manager.py --doctor
```

검증 항목:
1. 파일명이 패턴과 일치하는가?
2. 파일 내 `> **ID**:` 메타데이터가 파일명과 일치하는가?
3. 문서 헤더 `# [ID]`가 파일명과 일치하는가? (3-way consistency)
