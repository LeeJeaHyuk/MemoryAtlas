# Active Tasks (Execution)

> **Template-Version**: 3.4

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
> **Template-Version**: 3.4

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
- **가독성**: 이 README의 Dashboard 테이블로 조회