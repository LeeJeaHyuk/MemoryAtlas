# Coding Conventions & Rules (Smart Spec)

> **ID**: CTX-CONV-001
> **Last Updated**: 2026-01-20
> **Template-Version**: 2.4

---

## 1. Commands (실행 명령어)

> MemoryAtlas 프로젝트 자체의 명령어

| Action | Command | Description |
|--------|---------|-------------|
| **Init/Update** | `python memory_manager.py` | Initialize or update .memory structure |
| **Doctor (All Checks)** | `python memory_manager.py --doctor` | Run all validation checks |
| **Check Structure** | `python memory_manager.py --check` | Validate directory structure |
| **Lint Metadata** | `python memory_manager.py --lint` | Check document headers |
| **Validate Links** | `python memory_manager.py --links` | Check broken links |
| **Validate REQ** | `python memory_manager.py --req` | Validate requirement docs |
| **Validate RUN** | `python memory_manager.py --runs` | Validate execution logs |
| **Status Report** | `python memory_manager.py --status` | Show active tasks summary |
| **Bootstrap** | `python memory_manager.py --bootstrap` | Create AI kick-off files |
| **Build** | `python build.py` | Bundle into single file (stickytape) |

---

## 2. Project Structure (프로젝트 구조)

```
memory/
├── src/                    # 소스 코드 (비즈니스 로직)
│   ├── cli.py             # CLI 진입점
│   ├── core/              # 핵심 모듈
│   │   ├── __init__.py
│   │   ├── bootstrap.py   # 프로젝트 초기화
│   │   ├── checks.py      # 문서 검증 로직
│   │   ├── config.py      # 전역 설정 & 템플릿
│   │   ├── migrate.py     # 버전 마이그레이션
│   │   ├── status.py      # 상태 리포트
│   │   └── update.py      # 구조 업데이트
│   └── utils/             # 유틸리티
│       ├── __init__.py
│       └── fs.py          # 파일시스템 헬퍼
├── .memory/               # 프로젝트 문서 (MemoryAtlas)
│   ├── 00_SYSTEM/         # 시스템 관리 (자동 생성)
│   ├── 01_PROJECT_CONTEXT/# 프로젝트 헌법
│   ├── 02_REQUIREMENTS/   # 요구사항 (Authority)
│   ├── 03_TECH_SPECS/     # 기술 명세
│   ├── 04_TASK_LOGS/      # 실행 로그 (RUN)
│   └── 98_KNOWLEDGE/      # 지식 베이스
├── build.py               # 빌드 스크립트 (stickytape)
├── memory_manager.py      # 배포용 단일 파일 (생성됨)
└── README.md              # 프로젝트 소개
```

---

## 3. Code Style (코드 스타일)

### Python
- **Language**: Python 3.8+
- **Formatter**: ruff format (권장) 또는 black
- **Linter**: ruff check (권장) 또는 flake8
- **Type Hints**: **필수** - 모든 함수 시그니처에 타입 힌트 포함
- **Docstrings**: Google style (복잡한 함수만)

### Naming Conventions
| Type | Style | Example |
|------|-------|---------|
| Variables/Functions | `snake_case` | `check_structure()`, `meta_id` |
| Classes | `PascalCase` | `ConfigManager` |
| Constants | `UPPER_SNAKE_CASE` | `CURRENT_VERSION`, `ROOT_DIR` |
| Files | `lowercase_underscores` | `memory_manager.py`, `fs.py` |
| Private | `_leading_underscore` | `_internal_helper()` |

### Comments
- 복잡한 로직에만 **"Why"**를 적는다
- 명백한 코드에 주석 금지
- TODO: `# TODO(author): description`

---

## 4. Testing Strategy (테스트 전략)

### Requirements
- 모든 기능(`REQ`)은 최소 1개의 테스트 파일을 가져야 함
- 테스트 파일명: `test_<module_name>.py`
- 테스트 함수명: `test_<behavior>_<expected_result>()`

### Tools (권장)
- **Framework**: pytest
- **Coverage**: pytest-cov
- **목표**: 핵심 검증 로직 80% 이상

### TDD Workflow (권장)
1. `RUN` 문서 작성 시 테스트 케이스 먼저 정의
2. 실패하는 테스트 작성
3. 테스트 통과하는 최소 코드 작성
4. 리팩토링

---

## 5. Git Workflow (Git 규칙)

### Branch Naming
- Feature: `feat/REQ-ID-short-desc` (예: `feat/REQ-AUTH-001-login`)
- Bugfix: `fix/REQ-ID-desc` (예: `fix/REQ-DATA-003-validation`)
- Hotfix: `hotfix/critical-issue`

### Commit Messages
**Format**: Conventional Commits
```
<type>(<scope>): <subject>

<body>
```

- **Types**: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `style`
- **Scope**: 영향받는 모듈/도메인 (예: `core`, `checks`, `cli`)
- **Example**: `feat(checks): add 3-way ID validation for RUN documents`

### PR Rules
- **1 PR = 1 REQ/RUN**: 하나의 PR은 하나의 요구사항 문서와 매핑
- **Squash Merge**: 병합 시 Squash Merge 사용하여 커밋 히스토리 간결화
- **Self-review**: PR 생성 전 스스로 코드 리뷰
- **CI 통과 필수**: 모든 검증 통과 후 병합

---

## 6. Smart Spec Boundaries (STRICT)

### ✅ Always (항상 수행)
- **3-way ID 일치**: 모든 REQ/RUN 문서는 파일명 = 헤더 = 메타데이터 ID가 일치해야 함
  - 예: `REQ-AUTH-001.md` → `# [REQ-AUTH-001] ...` → `> **ID**: REQ-AUTH-001`
- **Python Type Hint 필수**: 모든 함수 시그니처에 타입 힌트 포함
  - 예: `def check_structure(root: str) -> int:`
- **Must-Read 명시**: REQ 문서 작성 시 반드시 `**Must-Read**` 필드에 상위 규칙(RULE) 명시
  - 예: `> **Must-Read**: RULE-DATA-001, ADR-003`
- **RUN 문서 완료 전 테스트 통과 확인**: Verification 섹션 체크리스트 완료 필수

### ⚠️ Ask First (사전 승인 필요)
- **시스템 코드 수정**: `memory_manager.py`, `build.py`, `core/config.py` 등 핵심 시스템 파일 수정 시
- **외부 패키지 추가**: `requirements.txt`에 새로운 라이브러리 추가 시
- **프로젝트 규칙 변경**: `01_CONVENTIONS.md`, `00_SYSTEM/AGENT_RULES.md` 수정 시
- **DB 스키마 변경**: (향후 DB 사용 시)
- **문서 템플릿 구조 변경**: `core/config.py`의 `DOC_TEMPLATES` 수정 시

### 🚫 Never (절대 금지)
- **Secret 하드코딩 금지**: API Key, Password, Token 등을 코드나 문서에 직접 작성
  - ✅ 올바른 방법: 환경 변수 또는 `.env` 파일 사용
- **REQ 문서 Append 금지**: 요구사항 변경 시 기존 텍스트를 수정(Refactor)하라. 밑에 "Update 1..." 식으로 덧붙이지 마라.
  - ✅ 올바른 방법: Decision 본문을 깔끔하게 수정하고, 상단 Change Log에만 이력 추가
- **허위 참조 금지**: 존재하지 않는 문서 ID를 링크로 거는 것 금지
  - 예: `[RULE-XXX-999](...)` (실제로 없는 문서)
  - `--doctor`가 자동으로 검증하므로 반드시 통과해야 함
- **Force Push 금지**: `main`/`master` 브랜치에 `git push --force` 금지
- **테스트 스킵 남용 금지**: `@pytest.mark.skip` 또는 `@pytest.mark.xfail` 남용 지양

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
