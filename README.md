# MemoryAtlas (Refactored)

> SSOT-First Development with Atlas CLI

[한국어] | [English](README.en.md)

## Core Philosophy
- SSOT (정답): 기계와 시스템이 참조하는 원천 데이터 (REQ, RULE, ADR)
- Views (표현): 사람이 읽고 이해하기 위한 맥락 문서 (views/)
- Execution (증거): 실행 계획과 결과, 그리고 코드의 Git Hash (RUN)

## 3-Step Workflow
Atlas는 Capture -> Run -> Finish 3단계로 작업을 관리합니다.

### Step 0: Init (최초 1회)
```bash
python atlas.py init
```
- `.atlas/` 구조와 기본 템플릿을 생성합니다.

### Step 1: Capture (입력 및 반영)
Brief 없이 SSOT(REQ)와 View를 직접 갱신합니다.
```bash
python atlas.py capture "사용자 로그인 기능 추가" --domain GEN
```
결과:
- `.atlas/req/REQ-GEN-001.md` 생성/수정
- `.atlas/views/REQ-GEN-001.md` 생성/갱신

호환 옵션:
```bash
python atlas.py capture "..." --domain GEN --to brief
```
- `.atlas/drafts/brief/BRIEF-GEN-001.md` 생성

### Step 2: Run (실행 계획)
구현 대상 REQ를 지정해 RUN 문서를 만듭니다.
```bash
python atlas.py run REQ-GEN-001
```
결과:
- `.atlas/runs/RUN-REQ-GEN-001-step-01.md` 생성
- RUN 문서에 Plan/Verification 포함

### Step 3: Finish (증거 기록)
구현이 끝나면 Git Hash를 남겨 추적성을 확보합니다.
```bash
python atlas.py finish RUN-REQ-GEN-001-step-01 --git a1b2c3d --success true
```
결과:
- RUN 상태 Completed로 갱신
- REQ 헤더에 Implemented-Git/Linked-RUN 기록

### Doctor (무결성 검증)
```bash
python atlas.py doctor
```
- View 링크의 REQ 연결성 검사
- Implemented REQ의 Git 증거 누락 경고

## 폴더 구조

| 경로 | 역할 |
|---|---|
| `.atlas/FRONT.md` | 프로젝트 개요/가이드 |
| `.atlas/BOARD.md` | 작업 상태 보드 |
| `.atlas/CONVENTIONS.md` | 규칙 |
| `.atlas/GOALS.md` | 목표/범위 |
| `.atlas/req/` | REQ 문서 (SSOT) |
| `.atlas/rule/` | RULE 문서 (SSOT) |
| `.atlas/adr/` | ADR 문서 (SSOT) |
| `.atlas/cq/` | CQ 문서 |
| `.atlas/views/` | View 문서 |
| `.atlas/drafts/brief/` | BRIEF 초안 (옵션) |
| `.atlas/runs/` | RUN 문서 |
| `.atlas/inbox/` | 외부 입력/아이디어 버퍼 |
| `.atlas/archive/` | 보관 |
| `.atlas/.system/templates/` | 실제 사용 템플릿 |
| `src/.system_defaults/` | 기본 템플릿/프롬프트 |

## 템플릿 갱신
- 기본값을 다시 적용하려면:
  ```bash
  python atlas.py init --overwrite
  ```

## 개발 빌드
- `src/` 수정 후 단일 파일 CLI를 갱신하려면:
  ```bash
  python build.py
  ```
