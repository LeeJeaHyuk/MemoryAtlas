# Coding Conventions & Rules

> **ID**: CTX-CONV-001
> **Last Updated**: (TBD)

---

## 1. Naming Conventions

### Variables & Functions
- Style: `snake_case`
- Example: `user_name`, `get_user_data()`

### Classes
- Style: `PascalCase`
- Example: `UserManager`, `DataProcessor`

### Constants
- Style: `UPPER_SNAKE_CASE`
- Example: `MAX_RETRY_COUNT`, `DEFAULT_TIMEOUT`

### Files & Directories
- Style: `lowercase_with_underscores`
- Example: `user_service.py`, `data_models/`

---

## 2. Code Style

### Language-Specific Rules

#### Python
- Formatter: `black`
- Linter: `ruff` or `flake8`
- Type hints: Required for public functions
- Docstrings: Google style

#### JavaScript/TypeScript
- Formatter: `prettier`
- Linter: `eslint`

---

## 3. Git Conventions

### Branch Naming
- Feature: `feature/short-description`
- Bugfix: `fix/issue-description`
- Hotfix: `hotfix/critical-fix`

### Commit Messages
```
<type>(<scope>): <subject>

<body>
```
- Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`

---

## 4. Universal Constraints

### Performance
- (예: 응답 시간은 1초 이내)

### Data
- (예: 모든 시간은 UTC로 저장)

### Security
- (예: 비밀번호는 bcrypt로 해싱)

---

## 5. Documentation Rules

### Required for Every Feature
- [ ] Description in `02_REQUIREMENTS/features/`
- [ ] API spec in `03_TECH_SPECS/api_specs/`
- [ ] Test coverage

### AI Agent Instructions
- **Before coding**: Read `01_CONVENTIONS.md` first
- **After coding**: Update relevant docs in `02_REQUIREMENTS/`
