# Discussions (Reference Layer)

> **Template-Version**: 2.2
>
> 사람-AI 조율 기록을 저장합니다.
> **LLM은 기본적으로 이 폴더를 읽지 않습니다.**

## When to Use

- 요구사항 논의 과정 기록
- 대안 검토 및 비교
- 결정 근거 상세 설명
- 이해관계자 의견 조율

## Template

```markdown
# [DISC-XXX-001] Discussion Title

> **ID**: DISC-XXX-001
> **Related-REQ**: REQ-XXX-001 (or RULE-XXX-001)
> **Date**: YYYY-MM-DD
> **Participants**: (참여자)
> **Template-Version**: 2.2

---

## Context

(논의 배경)

## Options Considered

### Option A: (대안 1)
- Pros: ...
- Cons: ...

### Option B: (대안 2)
- Pros: ...
- Cons: ...

## Discussion Log

### YYYY-MM-DD
- [Person/AI]: 의견 1
- [Person/AI]: 의견 2

## Conclusion

(결론 → REQ/RULE에 반영됨)
```

## Important Notes

1. **LLM 기본 무시**: 명시적으로 참조하지 않으면 읽지 않음
2. **REQ와 연결**: `Related-REQ` 필드로 관련 결정 문서 연결
3. **Archive 정책**: 오래된 논의는 `99_ARCHIVE/discussions/`로 이동
