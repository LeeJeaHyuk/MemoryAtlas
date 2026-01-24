# [REQ-DOC-001] BRIEF and RUN Template Quality Requirements

> **ID**: REQ-DOC-001
> **Domain**: DOC
> **Status**: Active
> **Last Updated**: 2026-01-23
> **Must-Read**: RULE-META-001, RULE-FLOW-002, REQ-MCP-001
> **Template-Version**: 5.0

---

## 1. Decision (결정 사항)

**Problem**: README.md에 명시된 BRIEF/RUN 문서 작성 원칙과 `automation.py`의 실제 템플릿 생성 로직 간에 gap이 존재한다.

**Gap Summary**:
1. **BRIEF 생성**: Affected Artifacts에 플레이스홀더(`REQ-XXX-001`) 사용, LLM 분석 없이 하드코딩된 예시만 삽입
2. **RUN 생성**: Self-Check/Evidence 섹션 누락, Scope가 In/Out으로 구분되지 않음
3. **CQ 원칙**: README Section 7에서 언급된 CQ 기반 입력이 BRIEF 템플릿에 반영되지 않음

**Decision**: 
- BRIEF/RUN 템플릿 생성 시 LLM이 수행해야 할 분석/채워야 할 항목을 명시적으로 표기
- 플레이스홀더 사용 시 `(TBD - LLM이 분석)` 형태로 명확한 지시 포함
- README 원칙과 템플릿 간 일관성 확보

---

## 2. Gap Analysis (격차 분석)

### Gap 1: BRIEF - Affected Artifacts 플레이스홀더

**README 원칙** (Section 3.2, 5.1):
- "Intake → System: BRIEF 생성 → 사용자 확인: BRIEF 검토"
- "Affected Artifacts 규칙: 경로 또는 링크로 표기"
- REQ-MCP-001 Line 39: "Affected Artifacts must use full paths or markdown links"

**실제 생성** (`automation.py:398-399`):
```python
"## 2. Affected Artifacts (영향받는 문서)\n"
"- Modify: 02_REQUIREMENTS/capabilities/REQ-XXX-001.md\n"  # ❌ 플레이스홀더
"- Create: 02_REQUIREMENTS/invariants/RULE-YYY-001.md\n\n"  # ❌ 구체화 안됨
```

**Impact**: 
- LLM이 사용자 요청을 분석해서 구체적인 영향 문서를 식별해야 하는데, 템플릿에 분석 필요성이 명시되지 않음
- `plan_from_brief()`는 구체적인 경로를 기대하므로, 플레이스홀더 상태로는 실행 불가

### Gap 2: BRIEF - Intent Summary vs User Request 구분 미흡

**README 원칙**:
- "사용자 의도(Intent) 파악" (REQ-MCP-001 Line 34)
- Intent는 원본 요청을 분석/요약한 결과여야 함

**실제 생성** (`automation.py:395-396`):
```python
"## 1. Intent Summary (의도 요약)\n"
f"{description}\n\n"  # ❌ 원본을 그대로 복사, 분석/요약 없음
```

**Impact**: 
- 원본 요청과 분석된 의도를 구분하지 않아, LLM이 추가 분석을 수행해야 함을 인지하기 어려움

### Gap 3: RUN - Self-Check Section 누락

**README 템플릿** (`04_TASK_LOGS/active/README.md` 기대 구조):
```markdown
## Verification (Self-Check)
- [ ] **Test**: 테스트 통과?
- [ ] **Boundary**: Boundaries 준수?
- [ ] **Spec**: REQ와 일치?
```

**실제 생성** (`automation.py:165-168`):
```python
"## Verification (Self-Check)\n"
"- [ ] Tests\n"        # ❌ 구체성 부족
"- [ ] Boundaries\n"   # ❌ 검증 기준 불명확
"- [ ] Spec reference\n\n"  # ❌ 어떤 REQ와 일치해야 하는지 명시 없음
```

**Impact**: 
- 사용자가 실행 완료 전 확인해야 할 구체적 기준이 없음
- `finalize_run()` 전 검증 지점이 모호함

### Gap 4: RUN - Evidence Section 누락

**README 기대 구조**:
```markdown
## Evidence (Implementation Proof)
- Tests: (통과한 테스트)
- Commands: (실행한 명령어)
- Code: (관련 파일)
```

**실제 생성**: Evidence 섹션 자체가 없음 (`automation.py:557-575`)

**Impact**: 
- 구현 증거 기록 불가
- Archive 이동 후 무엇이 수행되었는지 추적 어려움

### Gap 5: RUN - Scope 구체화 부족

**README 기대 구조**:
```markdown
## Scope (범위)
### In Scope
- (BRIEF의 Affected Artifacts 기반 구체적 범위)
### Out of Scope
- (명시적으로 제외되는 것)
```

**실제 생성** (`automation.py:567-568`):
```python
"## Scope (범위)\n"
"- Implement changes requested in the Brief. (브리프 요청사항 구현)\n\n"  # ❌ In/Out 구분 없음
```

**Impact**: 
- 작업 경계가 불명확하여 scope creep 발생 가능

### Gap 6: CQ 원칙 미반영

**README Section 7**:
- "CQ(Competency Question) 기반 문서 입력은 형식이 자유롭습니다"
- "정리 안 된 생각 → Intake"가 허용되는 시스템

**실제 BRIEF 템플릿**: CQ 관련 안내 섹션 없음

**Impact**: 
- 사용자가 비정형 입력(메모, 대화 로그)을 제출할 수 있음을 템플릿에서 알 수 없음

---

## 3. Input (입력 요구사항)

**입력 1: User Description**
- 사용자가 `intake()` 호출 시 제공하는 자연어 요청
- 형식: 자유 (메모, 대화 로그, 음성 기록 텍스트 등)

**입력 2: Current Templates**
- `automation.py:intake()` (Lines 383-408)
- `automation.py:plan_from_brief()` (Lines 500-578)

**입력 3: README Principles**
- README.md Section 3.2, 5.1
- REQ-MCP-001 Sections 2, 4

---

## 4. Output (산출물 요구사항)

### Output 1: Improved BRIEF Template

**Location**: `automation.py:intake()` 메서드 수정

**Required Sections**:

```markdown
## 1. User Request (원본 요청)
> {description}

## 2. Intent Summary (의도 요약)
> ⚠️ LLM 작업: 아래 요청의 핵심 의도를 분석하세요.

- 주요 목표: (TBD - LLM이 분석)
- 해결할 문제: (TBD - LLM이 분석)
- CQ 형식 입력 허용: 정리 안 된 생각/메모도 가능

## 3. Affected Artifacts (영향받는 문서)
> ⚠️ 반드시 구체적인 경로/링크로 작성 (REQ-XXX 금지)
> 예: 02_REQUIREMENTS/capabilities/REQ-AUTH-001.md

- Modify: (TBD - LLM이 분석)
- Create: (TBD - LLM이 분석)
- Read: (TBD - 참고 문서)

## 4. Proposed Changes (변경 제안)
> ⚠️ LLM 작업: 구체적인 변경사항을 나열하세요.

1. (TBD - 구체적 변경사항)

## 5. Verification Criteria (검증 기준)
> ⚠️ LLM 작업: 검증 가능한 구체적 조건을 작성하세요.

- [ ] (TBD - 구체적 검증 조건)
```

**Key Changes**:
1. User Request와 Intent Summary 명확히 구분
2. 모든 TBD 항목에 "LLM이 분석" 지시 추가
3. Affected Artifacts에 경로 형식 예시 및 경고 추가
4. CQ 기반 입력 허용 명시

### Output 2: Improved RUN Template

**Location**: `automation.py:plan_from_brief()` 메서드 수정

**Required Sections**:

```markdown
## Objective (목표)
{BRIEF의 Intent Summary 복사}

## Scope (범위)
### In Scope
- {BRIEF의 Affected Artifacts 기반 구체적 범위}
- {구현해야 할 기능}

### Out of Scope
- {명시적으로 제외되는 것}

## Steps (단계)
> ⚠️ LLM 작업: BRIEF 내용을 반영한 구체적 단계를 작성하세요.

1. [ ] {BRIEF 기반 구체적 단계}

## Verification (Self-Check)
> 작업 완료 전 반드시 확인

- [ ] **Test**: `pytest` 또는 관련 테스트 통과?
- [ ] **Boundary**: CONVENTIONS Boundaries 준수?
- [ ] **Spec**: {related_req}과 일치?
- [ ] **Doctor**: `python memory_manager.py --doctor` 통과?

## Evidence (Implementation Proof)
> 구현 완료 후 작성

- **Tests**: (통과한 테스트 파일/결과)
- **Commands**: (실행한 명령어)
- **Code**: (생성/수정된 파일)
- **Logs**: (관련 로그)

## Output (결과물)
- {생성/수정된 파일 목록}
```

**Key Changes**:
1. Scope를 In/Out으로 명확히 구분
2. Self-Check에 구체적 검증 항목 추가 (Test, Boundary, Spec, Doctor)
3. Evidence 섹션 추가 (구현 증거 기록)
4. Steps에 BRIEF 내용 반영 필요성 명시

### Output 3: README Section 6.1 추가

**Location**: `README.md` Section 6 뒤에 추가

**Content**:

```markdown
## 6.1 BRIEF 작성 가이드라인 (LLM 필수 작업)

Intake 도구 호출 후, LLM은 다음을 수행해야 합니다:

### 1. Intent Summary (의도 요약)
- 사용자 요청의 핵심 의도 분석
- 주요 목표와 해결할 문제 명확히 식별

### 2. Affected Artifacts (영향받는 문서)
- **반드시 구체적 경로 사용**: 
  - ❌ `REQ-XXX-001` (플레이스홀더)
  - ✅ `02_REQUIREMENTS/capabilities/REQ-AUTH-001.md` (구체적 경로)
- 존재하지 않는 파일은 `Create:`, 기존 파일은 `Modify:`
- 참고만 하는 문서는 `Read:`

### 3. Proposed Changes (변경 제안)
- 구체적이고 실행 가능한 변경사항 나열
- 코드 수정, 문서 수정, 테스트 추가 등 구체화

### 4. Verification Criteria (검증 기준)
- 검증 가능한 구체적 조건 작성
- 테스트, 명령어 실행 결과 등 객관적 기준

### 금지 사항
- ❌ 플레이스홀더(`XXX`, `YYY`) 그대로 두기
- ❌ 검증 기준 없이 BRIEF 완료 처리
- ❌ Affected Artifacts에 상대 경로만 사용 (도메인 명시 필요)

### CQ 기반 입력
- 메모, 대화 로그, 음성 기록 텍스트 등 비정형 입력 허용
- LLM이 이를 구조화된 BRIEF로 변환

## 6.2 RUN 작성 가이드라인 (LLM 필수 작업)

`plan_from_brief()` 호출 후, LLM은 다음을 수행해야 합니다:

### 1. BRIEF 파싱
- Intent Summary → RUN의 Objective로 복사
- Affected Artifacts → Scope (In Scope)로 변환
- Verification Criteria → Self-Check로 변환

### 2. Scope 구체화
- **In Scope**: BRIEF의 Affected Artifacts 기반으로 구체적 범위 명시
- **Out of Scope**: 명시적으로 제외되는 것 (scope creep 방지)

### 3. Steps 구체화
- BRIEF의 Proposed Changes를 실행 단계로 변환
- 체크박스 형식으로 진행 상황 추적 가능하게 작성

### 4. Self-Check 필수 항목
- **Test**: 단위/통합 테스트 통과 여부
- **Boundary**: Conventions 경계 규칙 준수 여부
- **Spec**: 관련 REQ 문서와 일치 여부
- **Doctor**: `--doctor` 검증 통과 여부

### 5. Evidence 기록
- 구현 완료 후 작성
- 테스트 결과, 실행 명령어, 수정 파일 목록 등 포함
```

---

## 5. Acceptance Criteria (완료 조건)

- [ ] **BRIEF Template**: `automation.py:intake()` 수정 완료
  - [ ] User Request와 Intent Summary 구분
  - [ ] TBD 항목에 "LLM 작업" 지시 추가
  - [ ] Affected Artifacts 경로 형식 예시 및 경고 추가
  - [ ] CQ 기반 입력 허용 명시

- [ ] **RUN Template**: `automation.py:plan_from_brief()` 수정 완료
  - [ ] Scope를 In/Out으로 구분
  - [ ] Self-Check에 구체적 검증 항목 추가
  - [ ] Evidence 섹션 추가
  - [ ] Steps에 BRIEF 내용 반영 필요성 명시

- [ ] **README Update**: Section 6.1, 6.2 추가 완료
  - [ ] BRIEF 작성 가이드라인
  - [ ] RUN 작성 가이드라인
  - [ ] 금지 사항 명시

- [ ] **Gap Closure**: 모든 Gap이 해소되었는지 확인
  - [ ] Gap 1: Affected Artifacts 플레이스홀더 → 구체적 경로 요구
  - [ ] Gap 2: Intent Summary → 원본과 분석 구분
  - [ ] Gap 3: Self-Check → 구체적 검증 항목 추가
  - [ ] Gap 4: Evidence → 섹션 추가
  - [ ] Gap 5: Scope → In/Out 구분
  - [ ] Gap 6: CQ 원칙 → 템플릿에 명시

- [ ] **Validation**: 수정된 템플릿으로 BRIEF/RUN 생성 테스트
  - [ ] `intake("신규 기능 추가")` 호출 → BRIEF 검증
  - [ ] `plan_from_brief(brief_id)` 호출 → RUN 검증

---

## 6. Validation

```bash
# 1. BRIEF 생성 테스트
python -c "
from src.core.automation import Automator
auto = Automator()
brief_path = auto.intake('사용자 인증 기능 추가')
print(f'BRIEF created: {brief_path}')
"

# 2. BRIEF 내용 검증
# - User Request 섹션 존재 확인
# - Intent Summary에 "LLM 작업" 지시 확인
# - Affected Artifacts에 경로 예시 확인
# - CQ 기반 입력 허용 명시 확인

# 3. RUN 생성 테스트 (BRIEF 구체화 후)
python -c "
from src.core.automation import Automator
auto = Automator()
run_path = auto.plan_from_brief('BRIEF-GEN-001')
print(f'RUN created: {run_path}')
"

# 4. RUN 내용 검증
# - Scope가 In/Out으로 구분되어 있는지 확인
# - Self-Check에 Test, Boundary, Spec, Doctor 항목 확인
# - Evidence 섹션 존재 확인
# - Steps에 체크박스 형식 확인

# 5. README 검증
grep -A 30 "## 6.1 BRIEF 작성 가이드라인" .memory/README.md
grep -A 30 "## 6.2 RUN 작성 가이드라인" .memory/README.md
```

---

## 7. Implementation Notes (구현 참고사항)

### 우선순위

**Priority 1 (High)**: Gap 1, 3, 4
- BRIEF의 Affected Artifacts 구체화 요구 (Gap 1)
- RUN의 Self-Check 개선 (Gap 3)
- RUN의 Evidence 섹션 추가 (Gap 4)
- 이유: `plan_from_brief()` 실행에 직접 영향

**Priority 2 (Medium)**: Gap 2, 5
- BRIEF의 Intent Summary 구분 (Gap 2)
- RUN의 Scope In/Out 구분 (Gap 5)
- 이유: 사용성 개선, 명확성 향상

**Priority 3 (Low)**: Gap 6
- CQ 원칙 템플릿 반영 (Gap 6)
- 이유: README에 이미 설명되어 있으나, 템플릿에 재명시

### 관련 파일

- `src/core/automation.py`: 템플릿 생성 로직
- `README.md`: 사용자 가이드
- `04_TASK_LOGS/active/README.md`: RUN 템플릿 참고
- `02_REQUIREMENTS/discussions/briefs/README.md`: BRIEF 템플릿 참고 (있다면)

### 역호환성

- 기존 BRIEF/RUN 문서는 수동 수정 필요 없음
- 새로 생성되는 문서만 개선된 템플릿 적용
- 기존 `intake()`, `plan_from_brief()` 함수 시그니처 변경 없음

---

## 8. Related Documents

- **REQ-MCP-001**: MCP Workflow Evolution (Intake-Plan-Execute)
- **RULE-FLOW-002**: 3-Phase Workflow Rules
- **RULE-META-001**: Metadata Standards
- **README.md**: Section 3.2, 5.1, 7

---

## 9. Version History

| Version | Date       | Changes                                      |
|---------|------------|----------------------------------------------|
| 1.0     | 2026-01-23 | Initial creation - Gap analysis documented   |
