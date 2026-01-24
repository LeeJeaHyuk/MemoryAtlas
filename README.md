# MemoryAtlas

> Document-Driven Development with MCP

[한국어](README.md) | [English](README.en.md)

## 3-Step Workflow

MemoryAtlas는 **Intake → Plan → Finish** 3단계로 모든 작업을 관리합니다.

```
[생각/요청] → Intake → [BRIEF] → Plan → [RUN] → 구현 → Finish → [완료]
```

### Step 1: Intake (요구 수집)

생각이나 요청을 BRIEF 문서로 변환합니다.

```python
# MCP
intake("사용자 인증 기능 추가")
# → .memory/02_REQUIREMENTS/discussions/briefs/BRIEF-GEN-001.md 생성

# Manual (briefs/ 폴더에 직접 파일 생성도 가능)
```

### Step 2: Plan (계획 수립)

BRIEF를 검토하고 RUN 실행 계획을 생성합니다.

```python
# MCP
plan("BRIEF-GEN-001")
# → REQ 자동 생성/갱신
# → .memory/04_TASK_LOGS/active/RUN-BRIEF-GEN-001-step-01.md 생성
```

### Step 3: Finish (완료 처리)

구현 완료 후 RUN을 종료합니다.

```python
# MCP
finish("RUN-BRIEF-GEN-001-step-01", success=True, git_hash="abc1234")
# → Status: Completed 업데이트
# → Git Evidence 기록
# → RUN은 active/에 유지 (Archive 이동 없음)
```

## Quick Start

```bash
# 1. 설치
pip install -r requirements.txt

# 2. 메모리 초기화
python memory_manager.py --init

# 3. 건강 검사
python memory_manager.py --doctor

# 4. 사용 시작
# "기능 추가해줘" → Intake 호출
# BRIEF 검토 → Plan 호출
# 구현 완료 → Finish 호출
```

## MCP 도구

| 도구 | 역할 | 트리거 예시 |
|------|------|-------------|
| `intake(description)` | 요청 → BRIEF 생성 | "이 기능 추가해줘" |
| `plan(brief_id)` | BRIEF → RUN 생성 | "계획 확정해" |
| `finish(run_id, success, git_hash)` | RUN 완료 처리 | "작업 끝" |

**보조 도구**

- `validate(scope)`: 수동 검증 (lint, links, doctor)
- `req_status(req_id)`: 요구사항 상태 조회
- `create_disc_from_failure(context)`: 실패 분석 문서 생성

**하위 호환 별칭** (v3.4 이전 사용자용)

- `plan_from_brief()` → `plan()`
- `finalize_run()` → `finish()`

## 핵심 문서

| 문서 | 역할 | 위치 |
|------|------|------|
| **BRIEF** | 요청/생각 정리 | `02_REQUIREMENTS/discussions/briefs/` |
| **REQ** | 요구사항 명세 | `02_REQUIREMENTS/capabilities/` |
| **RUN** | 실행 계획 및 추적 | `04_TASK_LOGS/active/` |

## v3.4 변경사항

- **Archive 폐지**: RUN은 active/에 유지, Status로 완료 관리
- **Git Evidence**: 변경 증거는 Git 커밋 해시로 기록
- **함수 리네이밍**: `plan()`, `finish()` (기존 함수는 별칭 유지)
- **REQ 자동관리**: `plan()` 호출 시 REQ 자동 생성/갱신

## 검증

```bash
# 전체 검증
python memory_manager.py --doctor

# RUN 목록 조회
python memory_manager.py --list-runs
python memory_manager.py --list-runs active
python memory_manager.py --list-runs completed
```

## 철학

1. **문서가 권위**: 코드는 문서에서 파생되는 결과물
2. **사용자는 의사결정만**: 실행/정리/검증은 LLM이 담당
3. **생각 → Intake**: 정리 안 된 생각도 시스템이 구조화

---

상세 가이드: [.memory/00_INDEX.md](.memory/00_INDEX.md)
