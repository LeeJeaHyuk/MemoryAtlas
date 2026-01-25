# [RULE-VER-001] Version Management Policy

> **ID**: RULE-VER-001
> **Domain**: VER
> **Priority**: High
> **Last Updated**: 2026-01-22
> **Must-Read**: RULE-ID-001
> **Template-Version**: 3.3

---

## Rule Statement (최종 결정)

MemoryAtlas는 **두 개의 독립적인 버전**을 관리하며, Semantic Versioning(SemVer)을 따른다.

---

## Two Version System

| 버전 | 변수명 | 현재 값 | 용도 |
|------|--------|---------|------|
| **Manager Version** | `CURRENT_VERSION` | 3.3.0 | CLI 도구 버전 (코드 변경) |
| **Template Version** | `TEMPLATE_VERSION` | 3.3 | 문서 스키마 버전 (템플릿 구조 변경) |

### CURRENT_VERSION (Manager Version)

CLI 도구(`memory_manager.py`)의 버전. 코드 변경 시 업데이트.

**위치**: `src/core/config.py:4`

```python
CURRENT_VERSION = "3.3.0"
```

### TEMPLATE_VERSION (Template Version)

문서 템플릿 스키마의 버전. 템플릿 구조/필드 변경 시 업데이트.

**위치**: `src/core/config.py:6`

```python
TEMPLATE_VERSION = "3.3"
```

---

## Semantic Versioning Rules

형식: `MAJOR.MINOR.PATCH`

### MAJOR (X.0.0)

**호환성을 깨는 변경**

- 기존 `.memory` 구조와 호환되지 않는 변경
- 마이그레이션 스크립트 필요
- 예: 폴더 구조 전면 개편, 필수 필드 대폭 변경

### MINOR (0.X.0)

**하위 호환되는 기능 추가**

- 새로운 명령어 추가 (`memory new-command`)
- 새로운 선택적 필드/템플릿 추가
- 새로운 검증 규칙 추가 (기존 문서는 통과)
- 예: `_index.md` 자동 생성 기능 추가

### PATCH (0.0.X)

**버그 수정 및 사소한 개선**

- 버그 수정
- 오타 수정
- 성능 개선 (동작 변경 없음)
- 문서 보완

---

## Version Update Checklist

### CURRENT_VERSION 업데이트 시

1. [ ] `src/core/config.py`의 `CURRENT_VERSION` 변경
2. [ ] `python build.py` 실행하여 `memory_manager.py` 재생성
3. [ ] Git commit message에 버전 포함: `vX.Y.Z <설명>`

### TEMPLATE_VERSION 업데이트 시

1. [ ] `src/core/config.py`의 `TEMPLATE_VERSION` 변경
2. [ ] 영향받는 `DOC_TEMPLATES` 내용 업데이트
3. [ ] `python build.py` 실행
4. [ ] (필요시) 마이그레이션 로직 추가

---

## Examples

### Correct

| 변경 내용 | 버전 변경 |
|-----------|-----------|
| `_index.md` 자동 생성 기능 추가 | `3.2.0` → `3.3.0` (MINOR) |
| doctor 출력 오타 수정 | `3.3.0` → `3.3.1` (PATCH) |
| Must-Read 필드 형식 변경 | `3.2` → `3.3` (TEMPLATE MINOR) |
| 폴더 구조 전면 개편 | `3.3.0` → `4.0.0` (MAJOR) |

### Incorrect

| 잘못된 예 | 이유 |
|-----------|------|
| 기능 추가 후 PATCH만 올림 | MINOR여야 함 |
| 템플릿 변경 후 CURRENT_VERSION만 변경 | TEMPLATE_VERSION도 변경 필요 |
| 버전 변경 후 build.py 미실행 | memory_manager.py와 불일치 |

---

## Rationale

1. **두 버전 분리**: 코드 변경과 스키마 변경은 독립적인 릴리즈 주기를 가질 수 있음
2. **SemVer 채택**: 업계 표준으로, 변경 영향도를 버전 번호만으로 파악 가능
3. **명시적 체크리스트**: 버전 업데이트 누락 방지

---

## Related

- **Source**: `src/core/config.py` (CURRENT_VERSION, TEMPLATE_VERSION)
- **Build**: [REQ-BUILD-001](../capabilities/REQ-BUILD-001.md)
- **Migration**: [REQ-MGT-003](../capabilities/REQ-MGT-003.md)
