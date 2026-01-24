# MemoryAtlas

> Document-Driven Development with MCP

[한국어](README.md) | [English](README.en.md)

## 3-Step Workflow

MemoryAtlas는 **Intake → Plan → Finish** 3단계로 모든 작업을 관리합니다.

```
[00_INBOX] → Intake → [BRIEF] → Plan → [RUN] → 구현 → Finish → [완료]
```

### Step 1: Intake (요구 수집)

정리되지 않은 아이디어를 규칙 없이 `00_INBOX/`에 던져두거나, 한 줄로 요청합니다. 시스템은 이를 읽어 BRIEF 문서로 구조화합니다.

```python
# MCP
intake("사용자 인증 기능 추가") 
# 또는 파일 입력 (긴 문맥)
intake("00_INBOX/idea.md")

# 결과
# → .memory/02_REQUIREMENTS/discussions/briefs/BRIEF-GEN-001.md 생성
# → 01_PROJECT_BOARD.md의 'Queue'에 추가
```

### Step 2: Plan (계획 확정)

BRIEF를 기반으로 구체적인 실행 계획(RUN/Task)을 확정합니다.

```python
# MCP
plan("BRIEF-GEN-001")

# 결과
# → REQ(요구사항) 자동 생성/갱신
# → .memory/04_TASK_LOGS/active/RUN-BRIEF-GEN-001-step-01.md 생성
# → 01_PROJECT_BOARD.md의 'Active'로 이동
```

### Step 3: Finish (검증 및 종료)

구현된 기능을 검증하고 작업 공간을 정리합니다.

```python
# MCP
finish("RUN-BRIEF-GEN-001-step-01", git_hash="abc1234")

# 결과
# → Status: Completed 업데이트 (Git Evidence 기록)
# → RUN 문서를 archive/ 폴더로 이동 (Clean Workspace)
# → 01_PROJECT_BOARD.md의 'Completed'로 이동
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

## 핵심 구조 (Directory Structure)

사용자는 다음 폴더의 역할만 알면 됩니다.

| 폴더/파일 | 역할 |
|---|---|
| `00_INBOX/` | **아이디어 덤프**. 아무 파일이나 자유롭게 던져두는 곳. |
| `01_PROJECT_BOARD.md` | **자동 현황판**. Queue(대기) → Active(진행) → Completed(완료) 흐름을 한눈에 확인. |
| `.memory/02_REQUIREMENTS/` | **Capabilities(REQ)** & **Competencies(CQ)**. 시스템의 권위(Authority)를 담는 곳. |
| `.memory/04_TASK_LOGS/` | **Active(현재 작업)** & **Archive(지난 작업)**. |

## 철학 (Authority)

1. **CQ First**: 모든 기능은 **CQ(핵심 질문, Competencies)**에 답하기 위해 존재해야 한다. 기준 없는 기능 추가 방지.
2. **Inbox & Board**: 생각은 자유롭게(`Inbox`), 관리는 체계적으로(`Board`).
3. **Clean Workspace**: 끝난 작업(`RUN`)은 즉시 `archive/`로 치워 집중력을 유지한다.

## MCP 도구

| 도구 | 역할 |
|---|---|
| `intake(input)` | 파일/텍스트 → BRIEF 생성 & Board 등록 |
| `plan(brief_id)` | BRIEF → RUN 생성 & Active 이동 |
| `finish(run_id)` | 검증 → Archive 이동 & Completed 처리 |

### 보조 도구
- `req_status(req_id)`: 요구사항 상태 조회
- `validate(scope)`: 수동 검증 수행

## 검증 및 현황

```bash
# 전체 시스템 검증
python memory_manager.py --doctor

# RUN 목록 조회 (CLI)
python memory_manager.py --list-runs
```

---

상세 가이드: [.memory/00_INDEX.md](.memory/00_INDEX.md)
