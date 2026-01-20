# Coding Conventions & Rules (Smart Spec)

> **ID**: CTX-CONV-001
> **Last Updated**: [TODO: AI와 토의하여 결정]
> **Template-Version**: 2.4

---

## 1. Commands (실행 명령어)

> [TODO: AI와 토의하여 결정]

| Action | Command | Description |
|--------|---------|-------------|
| **Test** | `[TODO]` | Run all unit tests |
| **Test (specific)** | `[TODO]` | Run specific test file |
| **Lint** | `[TODO]` | Check code style |
| **Format** | `[TODO]` | Auto-format code |
| **Run** | `[TODO]` | Run the application |
| **Build** | `[TODO]` | Build for production |

---

## 2. Project Structure (프로젝트 구조)

> [TODO: AI와 토의하여 결정]

```
project_root/
├── [TODO]/              # 소스 코드
├── [TODO]/              # 테스트 코드
├── .memory/             # 프로젝트 문서 (MemoryAtlas)
└── [TODO]               # 기타 파일들
```

---

## 3. Code Style (코드 스타일)

> [TODO: AI와 토의하여 결정]

### [Language]
- **Formatter**: `[TODO]`
- **Linter**: `[TODO]`
- **Type Hints**: [TODO]
- **Docstrings**: [TODO]

### Naming Conventions
| Type | Style | Example |
|------|-------|---------|
| Variables/Functions | `[TODO]` | |
| Classes | `[TODO]` | |
| Constants | `[TODO]` | |
| Files | `[TODO]` | |

---

## 4. Testing Strategy (테스트 전략)

> [TODO: AI와 토의하여 결정]

### Requirements
- [TODO]

### Coverage
- 목표: [TODO]

---

## 5. Git Workflow (Git 규칙)

> [TODO: AI와 토의하여 결정]

### Branch Naming
- Feature: `[TODO]`
- Bugfix: `[TODO]`

### Commit Messages
- Format: `[TODO]`

---

## 6. Smart Spec Boundaries (STRICT)

### ✅ Always (항상 수행)
- `RUN` 문서 작성 시 `Verification` 섹션에 구체적인 **검증 명령어**를 포함할 것. (예: `pytest tests/auth/`)
- 모든 퍼블릭 API/함수에는 **Docstring**과 **Type Hint**를 포함할 것.

### 🙋 Ask First (물어볼 것)
- `requirements.txt`, `package.json` 등 **의존성 추가/변경**.
- **DB 스키마 변경** (`migration` 파일 생성).
- 기존 `01_CONVENTIONS`나 시스템 템플릿 수정.

### 🚫 Never (절대 금지)
- **Secret Key**, Password, API Key를 코드나 문서에 하드코딩.
- **Mock Data**를 프로덕션 코드에 남기는 행위.
- `REQ` 문서의 **Decision** 섹션을 수정하지 않고 하단에 "추가 사항"으로 덧붙이는 행위.

---

## 7. Documentation Maintenance Policy
1. **SSOT (Single Source of Truth)**: `REQ` 문서는 항상 **현재 시점의 최종 명세**여야 한다.
2. **Rewrite, Don't Append**: 요구사항이 변경되면 기존 텍스트를 수정(Refactor)하라. 밑에 "Update 1..." 식으로 덧붙이지 마라.
3. **Change Log**: 변경 이력은 문서 최상단의 `Change Log` 테이블에만 기록하라.

---

## 8. AI Agent Quick Reference

### Reading Priority (P0 = Must Read)
1. **P0**: 이 파일 (`01_CONVENTIONS.md`)
2. **P0**: Target REQ의 `**Must-Read**` 필드
3. **P1**: `02_REQUIREMENTS/business_rules/` (전체)
4. **P2**: `98_KNOWLEDGE/` (복잡한 기능 시)

### Execution Checklist
1. [ ] CONVENTIONS의 Boundaries 확인
2. [ ] Target REQ 읽기
3. [ ] Must-Read 문서 읽기
4. [ ] RUN 문서 작성 (Self-Check 포함)
5. [ ] 구현 → 테스트 → 검증
6. [ ] RUN 문서 완료 처리
