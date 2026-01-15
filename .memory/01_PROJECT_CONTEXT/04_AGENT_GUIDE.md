# Agent Guide

## Source of Truth
- Always start with 00_INDEX.md.
- Prefer .memory documents over ad-hoc assumptions.

## Update Rules
- Update 02_SERVICES when requirements or specs change.
- Update 01_PROJECT_CONTEXT when architecture or scope changes.
- Update 03_MANAGEMENT after implementing or deferring work.

## Documentation Standard: Structured Natural Language
Use the following 5 rules so humans and LLMs can both parse and act on documents reliably.

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
