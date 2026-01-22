# [REQ-MGT-001] Initialize and Update Memory Structure

> **ID**: REQ-MGT-001
> **Domain**: MGT
> **Status**: Active
> **Last Updated**: 2026-01-20
> **Must-Read**: RULE-DIR-001, RULE-META-001
> **Template-Version**: 2.4

---

## Decision (최종 결정)

MemoryAtlas 시스템을 초기화하거나 최신 버전으로 업데이트한다. 누락된 폴더와 필수 파일을 생성하고, 버전 불일치 시 마이그레이션을 트리거한다.

**Source**: `src/core/update.py:init_or_update()`

---

## Input

- `root` (str): `.memory` 디렉토리 경로
- `dry_run` (bool): 변경 사항 미리보기 모드
- `force_migrate` (bool): 강제 마이그레이션 모드

---

## Output
 - MCP definitions: `.memory/00_SYSTEM/mcp/README.md` auto-generated
- Console output: 생성/업데이트된 파일 및 폴더 로그
- File system changes: `.memory/` 구조 생성 및 업데이트

---

## Logic

1. 현재 설치된 버전 확인 (`read_version()`)
2. 마이그레이션 필요 여부 확인 (v1.x → v2.x 또는 `force_migrate`)
   - 필요 시 `migrate_v1_to_v2()` 실행
3. 필수 디렉토리 구조 확보 (`ensure_structure()`)
4. 누락된 문서 생성 (`create_missing_docs()`)
5. 시스템 템플릿 업데이트 (`update_system_templates()`)
6. 도구 스크립트 업데이트 (`update_tooling()`)
7. MCP documentation updated (`00_SYSTEM/mcp/README.md`)
8. 버전 파일 갱신 (`write_version()`)

---

## Acceptance Criteria

- [x] 설치된 버전 감지
- [x] v1 구조일 경우 자동 마이그레이션
- [x] 필수 디렉토리 14개 자동 생성
- [x] 필수 파일(`00_INDEX.md`, `GOALS.md` 등) 생성
- [x] `memory_manager.py`를 `00_SYSTEM/scripts/`로 복사
- [x] `00_SYSTEM/mcp/README.md` contains the generated MCP definitions
- [x] `00_SYSTEM/mcp/README.md` contains auto-generated MCP definitions
- [x] `VERSION` 파일 업데이트
- [x] Dry Run 모드 지원

---

## Validation

```bash
# 초기화 또는 업데이트
python memory_manager.py

# 미리보기
python memory_manager.py --dry-run
```
