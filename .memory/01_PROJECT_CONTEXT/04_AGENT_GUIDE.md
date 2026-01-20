# Agent Guide

## Source of Truth
- Always start with 00_INDEX.md.
- Prefer .memory documents over ad-hoc assumptions.

## Update Rules
- Update 02_SERVICES when requirements or specs change.
- Update 01_PROJECT_CONTEXT when architecture or scope changes.
- Update 03_MANAGEMENT after implementing or deferring work.

## Documentation Standard: Structured Natural Language
Use the following rules so humans and LLMs can both parse and act on documents reliably.

### Rule 1: Metadata Header (Context Injection)
Place a header at the very top to declare what the document is, who it is for, and its freshness.

```markdown
# Document Title (e.g., News Classification Service Requirements)

> **ID**: DOC-ING-001
> **Service**: Ingestion Service
> **Scope**: News article category classification and tagging logic
> **Last Updated**: 2026-01-15

---
```

### Rule 2: Atomic Requirements (ID-Scoped Blocks)
Write each requirement as its own block with an ID and explicit fields.

```markdown
### [REQ-CLS-001] Rule-Based Disclosure Classification

- **Description**: If the title contains certain keywords, classify immediately without an LLM.
- **Input**: `Article` (title, content)
- **Output**: `ClassificationResult` (category='CORP_EVENT', confidence=1.0)
- **Rules**:
  - If the title contains "[공시]" or "[IR]", classify as `CORP_EVENT`.
  - If the title contains "속보", increase weight.
```

### Rule 3: Checkbox State Tracking
Track implementation inside the requirement using checkboxes.

```markdown
- **Acceptance Criteria**:
  - [x] "[공시]" keyword handling implemented
  - [ ] "[IR]" keyword handling implemented
  - [ ] Unit tests written
```

### Rule 4: Explicit Schemas via Code Blocks
Define schemas and examples inside code blocks (json, python, etc.).

```markdown
**Output Format Example**:
```json
{
  "category": "MACRO",
  "confidence": 0.95,
  "reasoning": "Multiple mentions of rate hikes"
}
```
```

### Rule 5: Explicit Linking
Use relative links to related documents.

```markdown
## Related Documents
- **Data Model**: [../../01_PROJECT_CONTEXT/03_DATA_MODEL.md](../../01_PROJECT_CONTEXT/03_DATA_MODEL.md)
- **Architecture**: [../../01_PROJECT_CONTEXT/02_ARCHITECTURE.md](../../01_PROJECT_CONTEXT/02_ARCHITECTURE.md)
```

### Rule 6: Human-Centric Readability (사람 중심 가독성)
사람이 3초 안에 핵심을 파악할 수 있도록 작성하라.

1. **BLUF (Bottom Line Up Front)**: 모든 섹션은 **결론(Conclusion)**이나 **한 줄 요약(Summary)**으로 시작하라.
2. **Visual Anchors (Emojis)**: 텍스트의 성격을 아이콘으로 표시하라.
   - 📕 **Critical**: 주의사항, 보안 이슈
   - ✨ **Feature**: 새로운 기능
   - 💡 **Note**: 참고, 팁
   - ❓ **Open**: 미결정 사항

### Rule 7: Diagram Over Text (텍스트보다 다이어그램)
조건 분기나 흐름이 3단계 이상 넘어가면 줄글 사용을 금지한다.

1. **Decision Matrix**: 복잡한 조건(권한, 상태 등)은 반드시 **마크다운 표(Table)**로 작성하라.
2. **Mermaid.js**: 데이터 흐름이나 상태 변화는 `mermaid` 코드 블록으로 시각화하라.

## Expected Effects (Current vs Proposed)

| 구분 | 현재 상태 (Current) | 추가 적용 후 (Proposed) |
|------|---------------------|-------------------------|
| 복잡한 로직 설명 | "관리자는 읽기 쓰기가 되는데 유저는 읽기만 되고..." (줄글) | 권한 테이블(Table) + 흐름도(Mermaid) |
| 요구사항 변경 시 | 문서 맨 아래에 `## 추가 요청사항` 섹션이 계속 생김 (스파게티) | Decision 본문이 깔끔하게 수정되고, 상단 Change Log만 한 줄 추가됨 |
| 위험한 작업 시 | AI가 임의로 판단해서 진행할 수 있음 | Ask First 규칙에 걸려 "의존성을 추가해도 될까요?"라고 물어봄 |
| 가독성 | 흑백 텍스트 위주라 눈에 잘 안 들어옴 | 이모지(📕, ✨, 💡, ❓)와 요약 덕분에 훑어보기 편함 |

## Standard Template (Copy/Paste)
```markdown
# [Service Name] Requirements

> **Service**: [Service name, e.g., Ingestion]
> **Component**: [Component name, e.g., Classification Pipeline]
> **Status**: [Draft / Active / Deprecated]

---

## 1. Overview
Briefly describe what this document defines.

## 2. Requirements

### [REQ-AAA-001] [Feature Name]
- **Description**: Clear statement of what must be done.
- **Input**:
  - `text` (str): input description
- **Output**:
  - `result` (dict): output description
- **Logic/Rules**:
  1. First rule
  2. Second rule
- **Acceptance Criteria**:
  - [ ] Feature implemented
  - [ ] Edge cases handled
  - [ ] Tests passing

### [REQ-AAA-002] [Feature Name]
...

## 3. Data Structures
```python
# Pydantic-style or JSON example
class OutputDTO:
    id: str
    value: int
```

## 4. References
List related documents here.
```
