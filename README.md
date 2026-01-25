# MemoryAtlas

> Document-Driven Development with Atlas CLI

[한국어](README.md) | [English](README.en.md)

## 3-Step Workflow

Atlas는 **Intake → Plan → Finish** 3단계로 작업을 관리합니다.

```
[idea] → Intake → [BRIEF] → Plan → [RUN] → 구현 → Finish
```

### Step 0: Init (최초 1회)

```bash
python atlas.py init
```

- `.atlas/` 구조와 기본 문서/템플릿을 생성합니다.
- 온보딩 프롬프트: `.atlas/.system/prompts/onboarding.md`

### Step 1: Intake (요구 수집)

```bash
python atlas.py intake "사용자 인증 기능 추가" --domain GEN
```

- `.atlas/brief/BRIEF-GEN-001.md` 생성

### Step 2: Plan (계획 확정)

```bash
python atlas.py plan BRIEF-GEN-001
```

- `.atlas/runs/RUN-BRIEF-GEN-001-step-01.md` 생성
- BRIEF 내 REQ ID가 있으면 스텁 생성

### Step 3: Finish (검증 및 종료)

```bash
python atlas.py finish RUN-BRIEF-GEN-001-step-01 --git abc1234 --success true
```

- RUN 메타데이터(Status/Git/Completed) 갱신

### Doctor (검증)

```bash
python atlas.py doctor
```

- 구조/링크/필수 문서 유무 점검

## 핵심 구조

| 경로 | 역할 |
|---|---|
| `.atlas/FRONT.md` | 프로젝트 개요/빠른 사용법 |
| `.atlas/BOARD.md` | 현재 작업 상태 |
| `.atlas/CONVENTIONS.md` | 작업 규칙 |
| `.atlas/GOALS.md` | 목표/범위 |
| `.atlas/req/` | REQ 문서 |
| `.atlas/rule/` | RULE 문서 |
| `.atlas/cq/` | CQ 문서 |
| `.atlas/brief/` | BRIEF 문서 |
| `.atlas/runs/` | RUN 문서 |
| `.atlas/idea/` | 자유 메모 |
| `.atlas/.system/templates/` | 실제 사용되는 템플릿 |
| `src/.system_defaults/` | 기본 템플릿/문서/프롬프트 소스 |

## 템플릿 갱신

- 기본값을 다시 적용하려면:
  ```bash
  python atlas.py init --overwrite
  ```

## 개발 빌드

- `src/` 수정 후 단일 실행 파일을 갱신하려면:
  ```bash
  python build.py
  ```
