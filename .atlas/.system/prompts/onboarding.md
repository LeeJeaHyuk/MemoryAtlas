# Atlas Onboarding Prompt

이 프롬프트를 Claude에게 전달하여 프로젝트 초기 설정을 완료하세요.

---

## Prompt

```
이 프로젝트에 Atlas 문서 시스템이 설치되었습니다.
.atlas/ 폴더의 GOALS.md, CONVENTIONS.md, BOARD.md, FRONT.md를 프로젝트에 맞게 설정해주세요.

다음 질문에 답변해주세요:

1. **프로젝트 목적** (GOALS.md용)
   - 이 프로젝트의 핵심 목표는 무엇인가요?
   - 범위 내(In scope)와 범위 외(Out of scope)를 구분해주세요.

2. **작업 규칙** (CONVENTIONS.md용)
   - 항상 지켜야 할 규칙은? (Always)
   - 먼저 물어봐야 할 것은? (Ask First)
   - 절대 하면 안 되는 것은? (Never)

3. **현재 작업 상태** (BOARD.md용)
   - 대기 중인 작업은? (Queue)
   - 진행 중인 작업은? (Active)

4. **추가 컨텍스트** (FRONT.md용)
   - 이 프로젝트의 기술 스택은?
   - 특별히 알아야 할 것이 있나요?

답변을 받으면 해당 파일들을 자동으로 업데이트하겠습니다.
```

---

## After Onboarding

설정 완료 후: `python atlas.py doctor` 실행하여 검증
