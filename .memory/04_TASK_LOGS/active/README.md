# Active Tasks (Execution)

> **Template-Version**: 3.1

## RUN Document Template

```markdown
# [RUN-REQ-XXX-001-step-01] Step Title

> **ID**: RUN-REQ-XXX-001-step-01
> **Status**: [Active | Blocked | Done]
> **Started**: YYYY-MM-DD
> **Input**: REQ-XXX-001, RULE-YYY-001, 01_CONVENTIONS.md
> **Verification**: (성공 조건 - 한 줄 요약)
> **Template-Version**: 3.1

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
6. **Scope ??**: In Scope / Out of Scope? ?? ?? ??
7. **Evidence ??**: ???/???/?? ?? ??