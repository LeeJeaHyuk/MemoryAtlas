# [REQ-SYNC-001] 상태 동기화 도구 (atlas sync)

> **ID**: REQ-SYNC-001
> **Domain**: SYNC
> **Status**: Draft
> **Last Updated**: 2026-01-26
> **Answers**: [CQ-SYNC-001](../cq/CQ-SYNC-001.md)
> **Must-Read**: None

---

## 핵심 원칙

| 문서 유형 | 역할 | 자동 수정 |
|-----------|------|-----------|
| **RUN** | 사실 기록 (증거/결과) | ✅ 허용 |
| **BRIEF** | 작업 상태 문서 | ✅ 허용 |
| **REQ** | 권위 (Authority) | ❌ Patch만 생성 |

---

## Decision

### 1. CLI 명령어 구조
```bash
# 동기화 명령어 (dry-run이 기본)
atlas sync <RUN-ID> [options]

# 완료 명령어 (내부에서 sync 호출)
atlas finish <RUN-ID> [options]
```

### 2. 동기화 동작 규칙

| 대상 | 기본 동작 | 옵션 |
|------|-----------|------|
| RUN 자체 | 체크박스/Status 업데이트 | (항상) |
| BRIEF | diff 출력만 | `--apply-brief` |
| REQ | Patch 파일 생성 | `--write-req-patch` |
| REQ 실제 적용 | 금지 | `--apply-req` (명시적) |

### 3. 안전장치
- **기본값 = dry-run**: 실제 변경 없이 diff만 출력
- **명시적 옵션 필수**: 실제 수정은 옵션으로만 허용
- **Patch 분리**: REQ 변경 제안은 별도 파일로 생성

---

## Input
- `<RUN-ID>`: 동기화 대상 RUN 문서 ID (예: `RUN-BRIEF-GEN-001-step-01`)
- RUN 문서 내 체크박스 상태 (`[ ]`, `[x]`)
- RUN 문서 내 Status 필드
- RUN → BRIEF → REQ 연결 정보 (Traceability)

## Output

### 기본 출력 (dry-run)
```
[SYNC] RUN-BRIEF-GEN-001-step-01
  → BRIEF-GEN-001: Status Draft → InProgress
  → REQ-GEN-001: [Patch required] checkbox line 15
```

### 파일 출력
- `--apply-brief`: BRIEF 문서 직접 수정
- `--write-req-patch`: `.atlas/patch/REQ-XXX-001.patch.md` 생성
- `--apply-req`: REQ 문서 직접 수정 (주의 필요)

---

## Acceptance Criteria
- [ ] `atlas sync <RUN-ID>` 실행 시 dry-run으로 diff 출력
- [ ] `--apply-brief` 옵션으로 BRIEF 문서 자동 수정
- [ ] `--write-req-patch` 옵션으로 REQ Patch 파일 생성
- [ ] `--apply-req` 옵션으로 REQ 직접 수정 (경고 메시지 포함)
- [ ] `atlas finish` 명령어가 내부에서 sync 호출
- [ ] Traceability 링크를 따라 연결된 문서 탐색 가능

---

## 사용 예시

```bash
# 1. 작업 완료 후 상태 확인 (dry-run)
atlas sync RUN-BRIEF-GEN-001-step-01

# 2. BRIEF만 자동 업데이트
atlas sync RUN-BRIEF-GEN-001-step-01 --apply-brief

# 3. REQ Patch 생성
atlas sync RUN-BRIEF-GEN-001-step-01 --write-req-patch

# 4. finish 명령어로 일괄 처리
atlas finish RUN-BRIEF-GEN-001-step-01 --apply-brief --write-req-patch

# 5. (주의) REQ 직접 수정
atlas sync RUN-BRIEF-GEN-001-step-01 --apply-req
```

---

## Traceability
- **Answers**: [CQ-SYNC-001](../cq/CQ-SYNC-001.md)
- **Implemented by**: [BRIEF-SYNC-001](../brief/BRIEF-SYNC-001.md)
- **Source**: [요구사항.md](../idea/요구사항.md)
