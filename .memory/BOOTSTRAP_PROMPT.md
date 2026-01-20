# 🚀 프로젝트 킥오프 (Context Bootstrapping)

> **MemoryAtlas v2.4.0**
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
