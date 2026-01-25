# [RULE-VALID-001] Three-Way ID Consistency

> **ID**: RULE-VALID-001
> **Domain**: VALIDATION
> **Priority**: Critical
> **Last Updated**: 2026-01-20
> **Must-Read**: RULE-ID-001
> **Template-Version**: 2.4

---

## Rule Statement (최종 결정)

모든 MemoryAtlas 문서는 **파일명**, **메타데이터 ID**, **헤더 ID**가 정확히 일치해야 한다 (3-way consistency).

---

## Rationale

**Source**: `src/core/checks.py:check_requirements(), check_runs()`
**Patterns**: 
- **Filename Extraction**: `extract_id_from_filename()`
- **Metadata Extraction**: `META_ID_RE = re.compile(r"^\s*>\s*\*\*ID\*\*:\s*(...)")`
- **Header Extraction**: `REQ_HEADER_RE`, `RULE_HEADER_RE`, `RUN_HEADER_RE`, etc.

3-way 일치성이 없으면:
1. 문서 자동 색인 실패
2. 검색/참조 시 혼란 (ID가 여러 곳에서 다름)
3. 링크 무결성 검증 불가

---

## The Three Parts

### 1️⃣ Filename
```
REQ-AUTH-001.md
```

### 2️⃣ Metadata ID
```markdown
> **ID**: REQ-AUTH-001
```

### 3️⃣ Header ID
```markdown
# [REQ-AUTH-001] User Login Feature
```

**모든 부분이 `REQ-AUTH-001`로 정확히 일치해야 함.**

---

## Examples

### ✅ Correct

**File**: `RULE-SEC-001.md`
```markdown
# [RULE-SEC-001] Password Validation Rule

> **ID**: RULE-SEC-001
> **Domain**: SEC
```

**검증 통과**: 파일명 = 메타데이터 = 헤더

---

### ❌ Incorrect

#### Case 1: 메타데이터 불일치
**File**: `REQ-AUTH-001.md`
```markdown
# [REQ-AUTH-001] User Login

> **ID**: REQ-AUTH-002  ← 잘못됨!
```

**오류**:
```
! Filename does not match **ID**: in REQ-AUTH-001.md
  -> **ID**: REQ-AUTH-002
  -> Filename: REQ-AUTH-001
```

#### Case 2: 헤더 불일치
**File**: `REQ-AUTH-001.md`
```markdown
# [REQ-AUTH-002] User Login  ← 잘못됨!

> **ID**: REQ-AUTH-001
```

**오류**:
```
! Header does not match **ID**: in REQ-AUTH-001.md
  -> **ID**: REQ-AUTH-001
  -> Header: REQ-AUTH-002
```

#### Case 3: 메타데이터 누락
**File**: `REQ-AUTH-001.md`
```markdown
# [REQ-AUTH-001] User Login

(메타데이터 없음)
```

**오류**:
```
! Missing **ID**: metadata in REQ-AUTH-001.md
  -> Add: > **ID**: REQ-AUTH-001
```

---

## Validation

```bash
# REQ/RULE 문서 검증
python memory_manager.py --req

# RUN 문서 검증
python memory_manager.py --runs

# 전체 검증
python memory_manager.py --doctor
```

---

## Document-Specific Rules

### REQ/RULE/DISC Documents
검증 대상:
1. 파일명 패턴 확인
2. `> **ID**:` 메타데이터 존재 확인
3. `# [ID]` 헤더 존재 확인
4. 3개 ID 일치 확인

### RUN Documents
RUN은 더 엄격:
```
Filename: RUN-REQ-AUTH-001-step-01.md
Metadata: > **ID**: RUN-REQ-AUTH-001-step-01
Header:   # [RUN-REQ-AUTH-001-step-01] Login Form Implementation
```

모두 `RUN-REQ-AUTH-001-step-01`로 정확히 일치.

---

## Exceptions

- `README.md`, `00_INDEX.md` 파일은 검증 제외
- `01_PROJECT_CONTEXT/` 내 템플릿 파일들은 별도 규칙 적용
