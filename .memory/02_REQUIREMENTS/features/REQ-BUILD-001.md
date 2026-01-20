# [REQ-BUILD-001] Single-File Build with Stickytape

> **ID**: REQ-BUILD-001
> **Domain**: BUILD
> **Status**: Active
> **Last Updated**: 2026-01-20
> **Must-Read**: RULE-META-001
> **Template-Version**: 2.4

---

## Decision (최종 결정)

`src/` 폴더 내의 여러 파이썬 모듈을 `stickytape`를 사용하여 배포 가능한 단일 파일 `memory_manager.py`로 번들링한다.

**Source**: `build.py`

---

## Input

- `src/cli.py` (Entry point)
- `src/core/*` (Modules)
- `src/utils/*` (Modules)

---

## Output

- `memory_manager.py` (Root directory)

---

## Logic

1. `stickytape` 실행 파일 경로 찾기
2. `PYTHONIOENCODING=utf-8` 환경 변수 설정 (유니코드 이슈 방지)
3. `cli.py`를 진입점으로 하여 의존성 탐색 및 번들링
4. `__future__` import 문제 해결을 위해 소스 코드 전처리 필요 (CLI에서 문자열 타입 힌트 사용 등)
5. 결과물을 `memory_manager.py`에 저장

---

## Acceptance Criteria

- [x] `python build.py` 실행 시 오류 없이 완료
- [x] 생성된 `memory_manager.py`가 독립적으로 실행 가능해야 함
- [x] `SyntaxError` (특히 `from __future__` 위치 문제)가 없어야 함
- [x] UTF-8 인코딩 지원

---

## Validation

```bash
# 빌드
python build.py

# 생성된 파일 실행 테스트
python memory_manager.py --version
```
