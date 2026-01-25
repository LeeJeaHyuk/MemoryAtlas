# [REQ-REV-001] Incremental Reverse Engineering

> **ID**: REQ-REV-001
> **Domain**: REV
> **Status**: Draft
> **Last Updated**: 2026-01-20
> **Must-Read**: RULE-ID-001, RULE-DIR-001
> **Template-Version**: 2.4

---

## Decision (최종 결정)

이미 존재하는 프로젝트 코드를 분석하여 MemoryAtlas 문서(REQ/RULE)를 역으로 생성하는 **Reverse Engineering** 기능을 제공한다. 
특히 거대 프로젝트를 감안하여, **"Divide and Conquer (분할 정복)"** 전략을 지원하는 `--focus` 옵션을 핵심으로 한다.

---

## Input

- `root` (str): 프로젝트 루트 경로
- `--reverse` (flag): 역설계 모드 활성화
- `--focus` (str): 분석할 특정 디렉토리 또는 파일 경로 (예: `src/auth`)

---

## Output

- `00_REVERSE_PROMPT.md`: AI 에이전트에게 전달할 프롬프트 파일

---

## Logic

### 1. Context Scanning (기존 지식 파악)
- 이미 존재하는 `02_REQUIREMENTS/business_rules/` 목록 스캔
- 이미 존재하는 `02_REQUIREMENTS/features/` 목록 스캔
- 목적: AI가 중복된 규칙을 생성하거나 기존 ID 체계를 벗어나는 것을 방지

### 2. Target Code Collection (분석 대상 수집)
- `--focus`로 지정된 경로 하위의 모든 소스 코드 파일 스캔
- `.gitignore`에 등록된 파일은 제외

### 3. Prompt Generation (프롬프트 생성)
다음 3단 구조를 가진 `00_REVERSE_PROMPT.md` 파일을 생성한다:

1.  **Global Context**: "현재 프로젝트에는 이미 `RULE-ID-001`, `REQ-AUTH-001` 등이 존재합니다."
2.  **Instructions**: "이것은 전체 중 일부(`{focus_path}`)입니다. 모르는 부분은 가정하지 말고 현재 코드 로직에만 집중하세요."
3.  **Target Code**: 실제 소스 코드 내용 (`src/auth/login.py` 등)

---

## Acceptance Criteria

- [ ] `python memory_manager.py --reverse --focus src/core` 실행 시 `00_REVERSE_PROMPT.md` 생성
- [ ] 생성된 프롬프트에 **기존 RULE 목록**이 포함되어야 함
- [ ] 생성된 프롬프트에 **기존 REQ 목록**이 포함되어야 함
- [ ] 생성된 프롬프트에 **Target Code** 내용이 포함되어야 함
- [ ] 지정된 경로가 없으면 오류 메시지 출력

---

## User Workflow (Example)

1.  **Core 분석 (기반 닦기)**
    ```bash
    python memory_manager.py --reverse --focus src/core
    # -> AI: RULE-CORE-xxx 위주 생성
    ```
2.  **Auth 모듈 분석**
    ```bash
    python memory_manager.py --reverse --focus src/auth
    # -> AI: 기존 RULE 참고하여 REQ-AUTH-xxx 생성
    ```
3.  **Payment 모듈 분석**
    ```bash
    python memory_manager.py --reverse --focus src/payment
    # -> AI: 기존 RULE/REQ 참고하여 REQ-PAY-xxx 생성
    ```

---

## Rationale

한 번에 모든 코드를 분석하는 것은 토큰 제한으로 불가능하며, AI의 할루시네이션(없는 규칙 창조)을 유발한다. 
따라서 **"이미 있는 것(Context)"**과 **"지금 분석할 것(Focus)"**을 명확히 분리하여 제공하는 점진적 접근이 필수적이다.
