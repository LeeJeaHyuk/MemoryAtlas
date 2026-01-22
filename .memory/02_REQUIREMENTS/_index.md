# 02_REQUIREMENTS 읽기 가이드

> **Template-Version**: 3.1
>
> 이 문서는 사람과 LLM이 요구사항 문서를 **어디서부터 읽어야 하는지** 안내합니다.

## 📖 읽는 순서

### 1단계: 전역 규칙 (필수)

아래 규칙들은 모든 REQ 구현 전에 반드시 읽어야 합니다:

| 순서 | 문서 | 설명 |
|------|------|------|
| 1 | [RULE-ID-001](invariants/RULE-ID-001.md) | ID 명명 규칙 |
| 2 | [RULE-META-001](invariants/RULE-META-001.md) | 메타데이터 필드 규칙 |
| 3 | [RULE-MUST-001](invariants/RULE-MUST-001.md) | Must-Read 참조 규칙 |

### 2단계: 대상 기능 (선택)

구현할 기능의 REQ 문서를 읽고, 해당 문서의 `**Must-Read**` 필드에 명시된 문서들을 따라 읽습니다.

## 🏷️ 폴더 구조

| 폴더 | 질문 | 내용 |
|------|------|------|
| `capabilities/` | "무엇을 만드는가?" | REQ-* (기능/행동) |
| `invariants/` | "무엇이 항상 참인가?" | RULE-* (불변 규칙) |
| `discussions/` | "어떻게 결정했는가?" | DISC-* (조율 기록) |

## REQ vs RULE 빠른 판정

```
REQ (capabilities/)
  → "시스템은 ~해야 한다" (동작 중심)
  → Input/Output/AC 필수

RULE (invariants/)
  → "항상 ~이다 / ~는 금지" (불변 중심)
  → Scope/Violation/Examples 필수
```

## 🔗 Quick Links

- 구조 설명: [README.md](README.md)
- 프로젝트 규칙: [01_CONVENTIONS.md](../01_PROJECT_CONTEXT/01_CONVENTIONS.md)

## ⚠️ 주의사항

- `discussions/`는 **기본적으로 읽지 않습니다** (명시적 참조 시만)
- 각 REQ의 `**Must-Read**` 필드가 **읽기 우선순위의 권위**입니다
