# [REQ-MGT-003] Version Migration (v1 to v2)

> **ID**: REQ-MGT-003
> **Domain**: MGT
> **Status**: Active
> **Last Updated**: 2026-01-20
> **Must-Read**: RULE-DIR-001
> **Template-Version**: 2.4

---

## Decision (최종 결정)

레거시 v1.x 구조를 최신 v2.x MemoryAtlas 구조로 마이그레이션한다. 기존 데이터 손실 없이 파일을 이동하고 폴더명을 변경한다.

**Source**: `src/core/migrate.py:migrate_v1_to_v2()`

---

## Input

- `root` (str): `.memory` 디렉토리 경로
- `dry_run` (bool): 변경 사항 미리보기 모드

---

## Output

- Updated file system: v2 구조로 재배치된 파일들
- Archive: 사용되지 않는 구버전 폴더 아카이빙

---

## Logic

1. v1 구조 감지 (`01_CONTEXT` 폴더 등 확인)
2. 폴더 매핑에 따라 이동 (`MIGRATION_MAP`):
   - `01_CONTEXT` → `01_PROJECT_CONTEXT`
   - `02_SPEC` → `02_REQUIREMENTS`
   - `03_IMPLEMENTATION` → `03_TECH_SPECS`
   - `04_HISTORY` → `04_TASK_LOGS`
3. 레거시 폴더 아카이빙 (`LEGACY_DIRS_TO_ARCHIVE`)
4. 파일 이동 시 안전한 `shutil.move` 사용 (이름 충돌 처리 없음 - 덮어쓸 수 있음 주의)

---

## Acceptance Criteria

- [x] v1 구조일 때만 동작 (또는 강제 flag)
- [x] 핵심 4개 폴더 매핑대로 이동
- [x] 구버전 폴더 `99_ARCHIVE`로 이동
- [x] Dry Run 모드 지원

---

## Validation

```bash
# 강제 마이그레이션 테스트
python memory_manager.py --migrate --dry-run
```
