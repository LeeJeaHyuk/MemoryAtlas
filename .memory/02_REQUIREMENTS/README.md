# Requirements (Authority Layer)

> **Template-Version**: 2.4
>
> 이 폴더는 **"무엇을 만들 것인가?"**의 **최종 결정**을 저장합니다.
> 논의/조율 기록은 `discussions/`에 분리합니다.

## Authority Model (v2.3)

```
문서 등급:
├── features/        → DECISION (Authority) - 최종 결정만
│                      + Constraints & Boundaries (Optional)
├── business_rules/  → DECISION (Authority) - 최종 결정만
└── discussions/     → DISCUSSION (Reference) - 조율 기록
```

### Smart Spec Integration (v2.3)
- **Boundaries**: 프로젝트 전역 규칙은 `01_CONVENTIONS.md`의 Boundaries 섹션
- **Constraints**: 기능별 추가 제약은 각 REQ의 `Constraints & Boundaries` 섹션 (Optional)

### Why Separate?
- **DECISION (features/, business_rules/)**: LLM이 반드시 읽어야 함
- **DISCUSSION (discussions/)**: LLM이 기본적으로 안 읽음. 명시적 참조 시만.

이렇게 분리하면:
1. 최종 결정이 명확해짐
2. LLM이 "무엇이 결정인지" 확률적 판단 불필요
3. 필수 규칙 누락/과다 참조 방지

## Structure

```
02_REQUIREMENTS/
├── features/           # REQ-* (DECISION only)
│   └── REQ-AUTH-001.md
├── business_rules/     # RULE-* (DECISION only)
│   └── RULE-DATA-001.md
└── discussions/        # DISC-* (조율 기록)
    └── DISC-AUTH-001.md
```

## Naming Convention (STRICT)

| Type | Pattern | Example | Location |
|------|---------|---------|----------|
| Feature | `REQ-[DOMAIN]-[NNN].md` | `REQ-AUTH-001.md` | features/ |
| Rule | `RULE-[DOMAIN]-[NNN].md` | `RULE-DATA-001.md` | business_rules/ |
| Discussion | `DISC-[DOMAIN]-[NNN].md` | `DISC-AUTH-001.md` | discussions/ |

## Must-Read Field (Required in v2.2)

모든 REQ/RULE 문서에는 `**Must-Read**` 필드가 필수입니다:

```markdown
> **Must-Read**: RULE-DATA-001, RULE-SEC-001, ADR-003
```

이 필드에 나열된 문서는 해당 REQ 구현 시 **반드시** 읽어야 합니다.

- Must-Read allows only RULE/ADR IDs (CTX is P0 and not allowed here).
- If you use markdown links, the link text must be the ID (e.g. `[RULE-ID-001](business_rules/RULE-ID-001.md)`).
